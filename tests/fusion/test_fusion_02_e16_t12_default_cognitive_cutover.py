from copy import deepcopy
import inspect

from python.ai_platform.adapters import (
    ProviderDescriptor,
    StaticProviderAdapter,
)
from python.ai_platform.cognitive_coordination import WorkingContext
from python.ai_platform.pipeline import AIRequestPipeline
from python.ai_platform.registry import ProviderRegistry


class Models:
    def discover_models(self, providers):
        return {"model-hi": "provider-hi"}

    def resolve_roles(self, settings, discovered):
        return {
            "engineering_model": "model-hi",
            "default_model": "model-hi",
        }


class Builder:
    def build(self):
        return {"legacy_builder": True}


class Adapter(StaticProviderAdapter):
    def __init__(self):
        super().__init__(
            ProviderDescriptor(
                provider_id="provider-hi",
                name="Provider Hi",
                env_vars=(),
                models=(
                    {
                        "id": "model-hi",
                        "token_limit": 4096,
                    },
                ),
                capabilities=("chat",),
                token_limit=4096,
                estimated_cost_per_1k_tokens=0.0,
            )
        )
        self.calls=[]

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
                "context": deepcopy(context),
                "model": model,
            }
        )
        return {
            "answer": "hello",
            "usage": {
                "input_tokens": 8,
                "output_tokens": 2,
                "estimated_cost": 0.0,
                "latency_ms": 1,
            },
        }


def context(question="hi"):
    return WorkingContext(
        schema="FUSION-02-WORKING-CONTEXT-1",
        need_id="need-hi",
        journey_id="journey-hi",
        status="UNKNOWN",
        human_question=question,
        constraints={
            "human_authority_preserved": True,
            "retrieval_confers_authority": False,
        },
        source_identity_kind="repository-relative-path",
        source_paths=(),
        evidence=(),
        provenance=(),
        epistemic_results=(),
        semantic_identities=(),
        epistemic_classes=(),
        uncertainties=(
            "no-research-required",
        ),
        relationships=(),
        journey_summary={
            "status": "IN_PROGRESS",
            "step_count": 0,
            "epistemic_gain": False,
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

    pipeline=AIRequestPipeline(
        registry=registry,
        model_manager=Models(),
        context_builder=Builder(),
    )

    settings={
        "providers": {
            "provider-hi": {},
        },
        "default_provider": "provider-hi",
    }

    return pipeline, adapter, settings


def test_hi_default_cutover_sends_governed_cognitive_context():
    pipeline, adapter, settings=system()

    legacy={
        "schema": "LEGACY-CONTEXT-1",
        "legacy_marker": "MUST-NOT-REACH-PROVIDER",
    }

    pipeline.use_cognitive_working_context(
        context("hi")
    )

    result=pipeline.run(
        "hi",
        settings,
        provider_id="provider-hi",
        model="model-hi",
        context_override=legacy,
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    sent=adapter.calls[-1]["context"]

    assert result["answer"] == "hello"
    assert sent["human_question"] == "hi"
    assert sent["need_id"] == "need-hi"
    assert sent["journey_id"] == "journey-hi"
    assert sent["human_authority_preserved"] is True
    assert sent["authority_conferred"] is False
    assert "legacy_marker" not in sent

    governance=result["context_governance"]

    assert governance is not None
    assert governance["rejected"] is False
    assert (
        governance["estimated_context_units"]
        <= governance["available_context"]
    )


def test_default_cutover_is_consumed_once():
    pipeline, adapter, settings=system()

    pipeline.use_cognitive_working_context(
        context("hi")
    )

    first=pipeline.run(
        "hi",
        settings,
        context_override={"legacy": "first"},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    second=pipeline.run(
        "second",
        settings,
        context_override={"legacy": "second"},
    )

    assert first["context_governance"] is not None
    assert second["context_governance"] is None
    assert adapter.calls[-1]["context"] == {
        "legacy": "second"
    }


def test_default_cutover_preserves_provider_and_model():
    pipeline, adapter, settings=system()

    pipeline.use_cognitive_working_context(
        context()
    )

    result=pipeline.run(
        "hi",
        settings,
        provider_id="provider-hi",
        model="model-hi",
        context_override={"legacy": True},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["provider"] == "provider-hi"
    assert result["model"] == "model-hi"
    assert adapter.calls[-1]["model"] == "model-hi"


def test_default_cutover_does_not_create_shadow_observation():
    pipeline, _, settings=system()

    pipeline.use_cognitive_working_context(
        context()
    )

    result=pipeline.run(
        "hi",
        settings,
        context_override={"legacy": True},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["shadow_comparison"] is None


def test_absent_default_cutover_keeps_legacy_path():
    pipeline, adapter, settings=system()

    legacy={"legacy": "preserved"}

    result=pipeline.run(
        "hi",
        settings,
        context_override=legacy,
    )

    assert result["context_governance"] is None
    assert result["context"] == legacy
    assert adapter.calls[-1]["context"] == legacy


def test_explicit_working_context_path_still_works():
    pipeline, adapter, settings=system()

    result=pipeline.run(
        "hi",
        settings,
        working_context=context(),
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["context_governance"] is not None
    assert adapter.calls[-1]["context"]["human_question"] == "hi"


def test_historical_run_signature_not_expanded_for_cutover():
    parameters=inspect.signature(
        AIRequestPipeline.run
    ).parameters

    assert "default_cognitive_working_context" not in parameters
    assert "context_override" in parameters
    assert "working_context" in parameters


def test_human_authority_and_unknown_survive_cutover():
    pipeline, adapter, settings=system()

    pipeline.use_cognitive_working_context(
        context()
    )

    pipeline.run(
        "hi",
        settings,
        context_override={"legacy": True},
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    sent=adapter.calls[-1]["context"]

    assert sent["status"] == "UNKNOWN"
    assert sent["unknown_is_valid"] is True
    assert sent["authority_conferred"] is False
    assert sent["human_authority_preserved"] is True
