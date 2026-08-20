from dataclasses import dataclass

import pytest

from python.ai_platform.adapters import (
    ProviderDescriptor,
    StaticProviderAdapter,
)
from python.ai_platform.cognitive_coordination import WorkingContext
from python.ai_platform.pipeline import AIRequestPipeline
from python.ai_platform.registry import ProviderRegistry


class DummyModelManager:
    def discover_models(self, providers):
        result={}
        for provider in providers:
            for model in provider["models"]:
                result[model]=provider["id"]
        return result

    def resolve_roles(self, settings, discovered):
        return {
            "engineering_model": settings.get(
                "engineering_model",
                "",
            ),
            "default_model": settings.get(
                "default_model",
                "",
            ),
        }


class DummyContextBuilder:
    def build(self):
        return {"legacy": True}


class RecordingAdapter(StaticProviderAdapter):
    def __init__(self, descriptor):
        super().__init__(descriptor)
        self.received=[]

    def complete(
        self,
        question,
        context,
        model,
        provider_settings=None,
    ):
        self.received.append(
            {
                "question":question,
                "context":dict(context),
                "model":model,
            }
        )
        return {
            "answer":"ok",
            "usage":{
                "input_tokens":1,
                "output_tokens":1,
                "estimated_cost":0.0,
                "latency_ms":1,
            },
        }


def working_context():
    return WorkingContext(
        schema="FUSION-02-WORKING-CONTEXT-1",
        need_id="need",
        journey_id="journey",
        status="PARTIAL",
        human_question="What evidence matters?",
        constraints={
            "human_authority_preserved":True,
            "retrieval_confers_authority":False,
        },
        source_identity_kind="repository-relative-path",
        source_paths=("a.py","b.py"),
        evidence=(
            {
                "source_path":"a.py",
                "result":"A"*500,
            },
            {
                "source_path":"b.py",
                "result":"B"*500,
            },
        ),
        provenance=(
            {
                "source_path":"a.py",
                "authority_conferred":False,
            },
            {
                "source_path":"b.py",
                "authority_conferred":False,
            },
        ),
        epistemic_results=(
            {
                "identity":"a",
                "source_path":"a.py",
                "epistemic_class":"EVIDENCE",
                "authority":"TECHNICAL_OBSERVATION",
            },
            {
                "identity":"b",
                "source_path":"b.py",
                "epistemic_class":"EVIDENCE",
                "authority":"TECHNICAL_OBSERVATION",
            },
        ),
        semantic_identities=("a","b"),
        epistemic_classes=("EVIDENCE",),
        uncertainties=("runtime-unverified",),
        relationships=(),
        journey_summary={
            "status":"IN_PROGRESS",
            "step_count":2,
            "epistemic_gain":True,
            "stopping_reason":"",
        },
        authority_conferred=False,
        human_authority_preserved=True,
        unknown_is_valid=True,
        bounded=True,
    )


def make_pipeline():
    registry=ProviderRegistry()

    descriptor=ProviderDescriptor(
        provider_id="test-provider",
        name="Test Provider",
        env_vars=(),
        models=(
            {
                "id":"small-model",
                "token_limit":700,
            },
            {
                "id":"large-model",
                "token_limit":4000,
            },
        ),
        capabilities=("chat",),
        token_limit=4000,
        estimated_cost_per_1k_tokens=0.0,
    )

    adapter=RecordingAdapter(descriptor)
    registry.register(adapter)

    pipeline=AIRequestPipeline(
        registry=registry,
        model_manager=DummyModelManager(),
        context_builder=DummyContextBuilder(),
    )

    return pipeline,registry,adapter


def test_registry_resolves_exact_model_capacity():
    _,registry,_=make_pipeline()

    assert registry.model_token_limit(
        "test-provider",
        "small-model",
    ) == 700

    assert registry.model_token_limit(
        "test-provider",
        "large-model",
    ) == 4000

    assert registry.model_token_limit(
        "test-provider",
        "missing-model",
    ) is None

    assert registry.model_token_limit(
        "missing-provider",
        "large-model",
    ) is None


def test_large_model_receives_governed_working_context():
    pipeline,_,adapter=make_pipeline()
    original=working_context()
    before=original.to_dict()

    result=pipeline.run(
        "question",
        {
            "providers":{"test-provider":{}},
            "default_provider":"test-provider",
        },
        provider_id="test-provider",
        model="large-model",
        working_context=original,
        reserved_orientation=100,
        reserved_question=100,
        reserved_instructions=100,
        reserved_answer=500,
    )

    assert result["context_governance"] is not None
    assert (
        result["context_governance"]["provider_capacity"]
        == 4000
    )
    assert result["context_governance"]["rejected"] is False

    assert adapter.received[-1]["context"] == result["context"]
    assert adapter.received[-1]["model"] == "large-model"

    assert original.to_dict() == before


def test_smaller_model_compacts_before_provider_invocation():
    pipeline,_,adapter=make_pipeline()

    result=pipeline.run(
        "question",
        {
            "providers":{"test-provider":{}},
            "default_provider":"test-provider",
        },
        provider_id="test-provider",
        model="small-model",
        working_context=working_context(),
        reserved_orientation=50,
        reserved_question=50,
        reserved_instructions=50,
        reserved_answer=100,
    )

    governance=result["context_governance"]

    assert governance["provider_capacity"] == 700
    assert governance["available_context"] == 450
    assert governance["estimated_context_units"] <= 450
    assert governance["compacted"] is True
    assert governance["rejected"] is False

    assert adapter.received[-1]["context"] == result["context"]


def test_unknown_model_capacity_fails_before_provider():
    pipeline,_,adapter=make_pipeline()

    with pytest.raises(
        ValueError,
        match="provider capacity must be known",
    ):
        pipeline.run(
            "question",
            {
                "providers":{"test-provider":{}},
                "default_provider":"test-provider",
            },
            provider_id="test-provider",
            model="unknown-model",
            working_context=working_context(),
        )

    assert adapter.received == []


def test_legacy_context_override_remains_compatible():
    pipeline,_,adapter=make_pipeline()

    result=pipeline.run(
        "question",
        {
            "providers":{"test-provider":{}},
            "default_provider":"test-provider",
        },
        provider_id="test-provider",
        model="large-model",
        context_override={"legacy":"preserved"},
    )

    assert result["context"] == {"legacy":"preserved"}
    assert result["context_governance"] is None
    assert adapter.received[-1]["context"] == {
        "legacy":"preserved"
    }


def test_double_context_authority_is_rejected():
    pipeline,_,adapter=make_pipeline()

    with pytest.raises(
        ValueError,
        match="mutually exclusive",
    ):
        pipeline.run(
            "question",
            {
                "providers":{"test-provider":{}},
                "default_provider":"test-provider",
            },
            provider_id="test-provider",
            model="large-model",
            context_override={"legacy":True},
            working_context=working_context(),
        )

    assert adapter.received == []
