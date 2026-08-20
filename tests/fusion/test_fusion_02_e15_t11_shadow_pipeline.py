from python.ai_platform.adapters import (
    ProviderDescriptor,
    StaticProviderAdapter,
)
from python.ai_platform.cognitive_coordination import WorkingContext
from python.ai_platform.pipeline import AIRequestPipeline
from python.ai_platform.registry import ProviderRegistry


class Models:
    def discover_models(self, providers):
        return {
            "shadow-model": "shadow-provider",
        }

    def resolve_roles(self, settings, discovered):
        return {
            "engineering_model": "shadow-model",
            "default_model": "shadow-model",
        }


class Builder:
    def __init__(self):
        self.calls = 0

    def build(self):
        self.calls += 1
        return {
            "legacy_marker": "AUTHORITATIVE_PROVIDER_PAYLOAD",
            "legacy_repository_profile": {
                "large": "L" * 800,
            },
        }


class Adapter(StaticProviderAdapter):
    def __init__(self):
        super().__init__(
            ProviderDescriptor(
                provider_id="shadow-provider",
                name="Shadow Provider",
                env_vars=(),
                models=(
                    {
                        "id": "shadow-model",
                        "token_limit": 4000,
                    },
                ),
                capabilities=("chat",),
                token_limit=4000,
                estimated_cost_per_1k_tokens=0.0,
            )
        )
        self.calls = []

    def complete(
        self,
        question,
        context,
        model,
        provider_settings=None,
    ):
        self.calls.append(
            {
                "question": question,
                "context": dict(context),
                "model": model,
            }
        )
        return {
            "answer": "legacy-provider-answer",
            "usage": {
                "input_tokens": 10,
                "output_tokens": 5,
                "estimated_cost": 0.0,
                "latency_ms": 1,
            },
        }


def cognitive_context():
    return WorkingContext(
        schema="FUSION-02-WORKING-CONTEXT-1",
        need_id="n",
        journey_id="j",
        status="PARTIAL",
        human_question="inspect evidence",
        constraints={
            "human_authority_preserved": True,
            "retrieval_confers_authority": False,
        },
        source_identity_kind="repository-relative-path",
        source_paths=("a.py",),
        evidence=(
            {
                "source_path": "a.py",
                "result": "bounded evidence",
            },
        ),
        provenance=(
            {
                "source_path": "a.py",
                "authority_conferred": False,
            },
        ),
        epistemic_results=(
            {
                "identity": "A",
                "source_path": "a.py",
                "epistemic_class": "REPOSITORY_IMPLEMENTATION",
                "authority": "TECHNICAL_OBSERVATION",
            },
        ),
        semantic_identities=("A",),
        epistemic_classes=("REPOSITORY_IMPLEMENTATION",),
        uncertainties=("runtime-unverified",),
        relationships=(),
        journey_summary={
            "status": "IN_PROGRESS",
            "step_count": 1,
            "epistemic_gain": True,
            "stopping_reason": "",
        },
        authority_conferred=False,
        human_authority_preserved=True,
        unknown_is_valid=True,
        bounded=True,
    )


def system():
    registry=ProviderRegistry()
    adapter=Adapter()
    registry.register(adapter)

    builder=Builder()

    pipeline=AIRequestPipeline(
        registry=registry,
        model_manager=Models(),
        context_builder=builder,
    )

    return pipeline, adapter, builder


def settings():
    return {
        "providers": {
            "shadow-provider": {},
        },
        "default_provider": "shadow-provider",
    }


def test_shadow_observation_preserves_provider_payload():
    pipeline, adapter, builder=system()

    legacy={
        "legacy_marker": "AUTHORITATIVE_PROVIDER_PAYLOAD",
        "conversation": {
            "preserved": True,
        },
    }

    pipeline.observe_working_context(
        cognitive_context()
    )

    result=pipeline.run(
        "question",
        settings(),
        provider_id="shadow-provider",
        model="shadow-model",
        context_override=legacy,
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["answer"] == "legacy-provider-answer"
    assert adapter.calls[-1]["context"] == legacy
    assert result["context"] == legacy
    assert builder.calls == 0

    shadow=result["shadow_comparison"]

    assert shadow["mode"] == "SHADOW"
    assert shadow["provider_payload_source"] == "LEGACY"
    assert shadow["shadow_payload_sent_to_provider"] is False
    assert shadow["cognitive_rejected"] is False
    assert shadow["authority_conferred"] is False
    assert shadow["human_authority_preserved"] is True
    assert shadow["cognitive_source_count"] == 1
    assert shadow["cognitive_epistemic_result_count"] == 1
    assert shadow["cognitive_provenance_count"] == 1


def test_shadow_is_consumed_exactly_once():
    pipeline, _, _=system()

    pipeline.observe_working_context(
        cognitive_context()
    )

    first=pipeline.run(
        "first",
        settings(),
        context_override={"legacy": 1},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    second=pipeline.run(
        "second",
        settings(),
        context_override={"legacy": 2},
    )

    assert first["shadow_comparison"] is not None
    assert second["shadow_comparison"] is None


def test_shadow_does_not_change_provider_or_model():
    pipeline, adapter, _=system()

    pipeline.observe_working_context(
        cognitive_context()
    )

    result=pipeline.run(
        "question",
        settings(),
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["provider"] == "shadow-provider"
    assert result["model"] == "shadow-model"
    assert adapter.calls[-1]["model"] == "shadow-model"
    assert result["answer"] == "legacy-provider-answer"


def test_shadow_record_does_not_copy_knowledge_payload():
    pipeline, _, _=system()

    pipeline.observe_working_context(
        cognitive_context()
    )

    result=pipeline.run(
        "question",
        settings(),
        context_override={"legacy": True},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    shadow=result["shadow_comparison"]

    assert "context" not in shadow
    assert "evidence" not in shadow
    assert "provenance" not in shadow
    assert "epistemic_results" not in shadow


def test_absent_shadow_preserves_previous_behavior():
    pipeline, adapter, _=system()

    legacy={"legacy": "unchanged"}

    result=pipeline.run(
        "question",
        settings(),
        context_override=legacy,
    )

    assert result["shadow_comparison"] is None
    assert adapter.calls[-1]["context"] == legacy


def test_public_run_signature_has_no_shadow_keyword():
    import inspect

    parameters=inspect.signature(
        AIRequestPipeline.run
    ).parameters

    assert "shadow_working_context" not in parameters
    assert "context_override" in parameters
    assert "working_context" in parameters
