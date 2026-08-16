from __future__ import annotations

import json
from pathlib import Path

from python.ai_platform import pipeline as pipeline_module
from python.ai_platform.context_builder import AIContextBuilder


class _FakeProfile:
    pass


class _FakeRepositoryEngine:
    calls = 0

    def __init__(self, repository_root):
        self.repository_root = repository_root

    def profile(self):
        type(self).calls += 1
        return _FakeProfile()


class _FakeSerializer:
    calls = 0

    @staticmethod
    def to_dict(profile):
        assert isinstance(profile, _FakeProfile)
        _FakeSerializer.calls += 1

        return {
            "health_summary": {
                "status": "characterized",
            },
            "tech_stack": [
                "python",
            ],
            "dependencies": {
                "runtime": [
                    "example",
                ],
            },
            "engineering": {
                "inventory": [
                    {
                        "semantic_identity": (
                            f"artifact-{index:04d}"
                        ),
                        "path": (
                            f"lib/example/{index:04d}.py"
                        ),
                        "description": "x" * 160,
                    }
                    for index in range(500)
                ],
            },
        }


class _ProviderAdapter:
    def __init__(self):
        self.question = None
        self.context = None
        self.model = None

    def complete(
        self,
        question,
        context,
        model,
        provider_settings=None,
    ):
        self.question = question
        self.context = context
        self.model = model

        return {
            "answer": "characterization",
            "usage": {
                "input_tokens": 1,
                "output_tokens": 1,
                "estimated_cost": 0.0,
                "latency_ms": 1,
            },
        }


class _Registry:
    def __init__(self, adapter):
        self._adapter = adapter

    def list_providers(self, settings):
        return [
            {
                "id": "characterization",
            }
        ]

    def adapter(self, provider_id):
        assert provider_id == "characterization"
        return self._adapter


class _ModelManager:
    def discover_models(self, providers):
        return {
            "characterization": [
                {
                    "id": "model",
                }
            ],
        }

    def resolve_roles(self, settings, discovered):
        return {
            "engineering_model": "model",
            "default_model": "model",
        }


def _patch_context_sources(monkeypatch):
    import python.ai_platform.context_builder as module

    monkeypatch.setattr(
        module,
        "RepositoryEngine",
        _FakeRepositoryEngine,
    )

    monkeypatch.setattr(
        module,
        "RepositoryProfileSerializer",
        _FakeSerializer,
    )

    monkeypatch.setattr(
        module.GitContextProvider,
        "collect",
        lambda self: {
            "current_branch": "main",
        },
    )

    monkeypatch.setattr(
        module.DevelopmentContextProvider,
        "collect",
        lambda self: {
            "planning": {
                "current_sprint": "T1",
            },
            "current_context": {
                "current_epic": "FUSION-02",
                "current_issue": "T1",
            },
        },
    )

    monkeypatch.setattr(
        module.WorkspaceContextProvider,
        "collect",
        lambda self: {
            "repositories": [],
        },
    )

    monkeypatch.setattr(
        AIContextBuilder,
        "_read_json",
        lambda self, path: {},
    )

    monkeypatch.setattr(
        AIContextBuilder,
        "_recent_reports",
        lambda self, limit=5: [],
    )

    monkeypatch.setattr(
        AIContextBuilder,
        "_canonical_documents",
        lambda self, limit=12: [],
    )


def _serialized_size(value):
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        ).encode("utf-8")
    )


def test_t1_builder_materializes_repository_profile_before_reasoning(
    monkeypatch,
    tmp_path,
):
    _FakeRepositoryEngine.calls = 0
    _FakeSerializer.calls = 0

    _patch_context_sources(monkeypatch)

    builder = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    context = builder.build()

    assert _FakeRepositoryEngine.calls == 1
    assert _FakeSerializer.calls == 1

    assert "repository_profile" in context

    assert (
        context["repository_profile"]["health_summary"]
        == {
            "status": "characterized",
        }
    )

    assert context["repository_health"] == {
        "status": "characterized",
    }

    assert context["technology_stack"] == [
        "python",
    ]

    assert context["dependencies"] == {
        "runtime": [
            "example",
        ],
    }


def test_t1_pipeline_default_path_transports_built_profile(
    monkeypatch,
    tmp_path,
):
    _FakeRepositoryEngine.calls = 0
    _FakeSerializer.calls = 0

    _patch_context_sources(monkeypatch)

    adapter = _ProviderAdapter()

    pipeline = pipeline_module.AIRequestPipeline(
        registry=_Registry(adapter),
        model_manager=_ModelManager(),
        context_builder=AIContextBuilder(
            repository_root=str(tmp_path),
            workspace_root=str(tmp_path),
        ),
    )

    result = pipeline.run(
        question="hi",
        settings={
            "default_provider": "characterization",
        },
    )

    assert _FakeRepositoryEngine.calls == 1
    assert _FakeSerializer.calls == 1

    assert adapter.question == "hi"
    assert adapter.context is not None

    assert "repository_profile" in adapter.context

    assert result["context"] == adapter.context


def test_t1_context_override_bypasses_builder():
    class _ForbiddenBuilder:
        def build(self):
            raise AssertionError(
                "context builder must not run "
                "when context_override exists"
            )

    adapter = _ProviderAdapter()

    pipeline = pipeline_module.AIRequestPipeline(
        registry=_Registry(adapter),
        model_manager=_ModelManager(),
        context_builder=_ForbiddenBuilder(),
    )

    override = {
        "schema": "t1-characterization-override/v1",
        "bounded": True,
    }

    result = pipeline.run(
        question="hi",
        settings={
            "default_provider": "characterization",
        },
        context_override=override,
    )

    assert adapter.context == override
    assert result["context"] == override


def test_t1_repository_profile_dominates_synthetic_legacy_context(
    monkeypatch,
    tmp_path,
):
    _FakeRepositoryEngine.calls = 0
    _FakeSerializer.calls = 0

    _patch_context_sources(monkeypatch)

    context = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    ).build()

    total_bytes = _serialized_size(context)

    profile_bytes = _serialized_size(
        context["repository_profile"]
    )

    assert total_bytes > 0
    assert profile_bytes > 0

    assert profile_bytes / total_bytes > 0.90


def test_t1_production_characterization_contract_is_still_present():
    context_source = Path(
        "lib/python/ai_platform/context_builder.py"
    ).read_text(
        encoding="utf-8"
    )

    pipeline_source = Path(
        "lib/python/ai_platform/pipeline.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "RepositoryEngine(self.repository_root).profile()"
        in context_source
    )

    assert (
        '"repository_profile": profile'
        in context_source
    )

    assert (
        "self.context_builder.build()"
        in pipeline_source
    )

    assert (
        "adapter.complete("
        in pipeline_source
    )
