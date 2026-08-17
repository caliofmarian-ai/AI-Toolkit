from __future__ import annotations

import json

import python.ai_platform.context_builder as context_module
from python.ai_platform.context_builder import AIContextBuilder


class _ForbiddenRepositoryEngine:
    def __init__(self, repository_root):
        raise AssertionError(
            "Permanent Orientation must not instantiate RepositoryEngine"
        )


class _ForbiddenSerializer:
    @staticmethod
    def to_dict(profile):
        raise AssertionError(
            "Permanent Orientation must not serialize RepositoryProfile"
        )


def _patch_orientation_sources(monkeypatch):
    monkeypatch.setattr(
        context_module,
        "RepositoryEngine",
        _ForbiddenRepositoryEngine,
    )
    monkeypatch.setattr(
        context_module,
        "RepositoryProfileSerializer",
        _ForbiddenSerializer,
    )
    monkeypatch.setattr(
        context_module.GitContextProvider,
        "collect",
        lambda self: {
            "current_branch": "main",
        },
    )
    monkeypatch.setattr(
        context_module.DevelopmentContextProvider,
        "collect",
        lambda self: {
            "planning": {
                "current_sprint": "FUSION-02",
            },
            "current_context": {
                "current_epic": "EPISTEMIC-COGNITIVE-PHYSIOLOGY",
                "current_issue": "PERMANENT-ORIENTATION",
            },
        },
    )
    monkeypatch.setattr(
        AIContextBuilder,
        "_read_json",
        lambda self, path: {
            "runtime": {
                "state": "characterized",
            }
        },
    )


def _serialized_size(value):
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def test_permanent_orientation_is_bounded_and_does_not_profile_repository(
    monkeypatch,
    tmp_path,
):
    _patch_orientation_sources(monkeypatch)

    builder = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    orientation = builder.build_permanent_orientation()

    assert orientation["schema"] == (
        "ai-toolkit/permanent-epistemic-orientation/v1"
    )
    assert orientation["organism"] == "AI-Toolkit"

    assert "repository_profile" not in orientation
    assert "repository_health" not in orientation
    assert "technology_stack" not in orientation
    assert "dependencies" not in orientation
    assert "workspace" not in orientation
    assert "recent_reports" not in orientation
    assert "canonical_documents" not in orientation

    assert orientation["current_branch"] == "main"
    assert orientation["current_sprint"] == "FUSION-02"

    assert orientation["human_authority"] == {
        "authority": "human",
        "ai_may_promote_authority": False,
    }

    constraints = orientation["constraints"]

    assert constraints[
        "knowledge_availability_is_not_working_context"
    ] is True
    assert constraints["retrieval_confers_authority"] is False
    assert constraints["semantic_identity_is_physical_location"] is False
    assert constraints["navigation_read_only"] is True
    assert constraints["unknown_is_valid"] is True
    assert constraints["full_repository_profile_default_payload"] is False

    assert _serialized_size(orientation) < 8192


def test_permanent_orientation_declares_organs_without_materializing_them(
    monkeypatch,
    tmp_path,
):
    _patch_orientation_sources(monkeypatch)

    orientation = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    ).build_permanent_orientation()

    assert orientation["available_organs"] == [
        "csl_uem",
        "canon",
        "knowledge_graph",
        "repository",
        "provenance",
        "layered_memory",
        "persistent_experience",
    ]

    assert orientation["navigation_capabilities"] == [
        "search",
        "resolve",
        "read",
        "inspect",
        "traverse",
        "trace_provenance",
    ]

    serialized = json.dumps(
        orientation,
        ensure_ascii=False,
        sort_keys=True,
    )

    assert "RepositoryProfile" not in serialized
    assert "repository_profile" not in orientation


def test_permanent_orientation_is_deterministic_for_same_observed_state(
    monkeypatch,
    tmp_path,
):
    _patch_orientation_sources(monkeypatch)

    builder = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    first = builder.build_permanent_orientation()
    second = builder.build_permanent_orientation()

    assert first == second


def test_legacy_context_builder_remains_available_for_shadow_transition(
    monkeypatch,
    tmp_path,
):
    class _Profile:
        pass

    class _RepositoryEngine:
        calls = 0

        def __init__(self, repository_root):
            self.repository_root = repository_root

        def profile(self):
            type(self).calls += 1
            return _Profile()

    class _Serializer:
        calls = 0

        @staticmethod
        def to_dict(profile):
            assert isinstance(profile, _Profile)
            _Serializer.calls += 1
            return {
                "health_summary": {},
                "tech_stack": [],
                "dependencies": {},
            }

    monkeypatch.setattr(
        context_module,
        "RepositoryEngine",
        _RepositoryEngine,
    )
    monkeypatch.setattr(
        context_module,
        "RepositoryProfileSerializer",
        _Serializer,
    )
    monkeypatch.setattr(
        context_module.GitContextProvider,
        "collect",
        lambda self: {
            "current_branch": "main",
        },
    )
    monkeypatch.setattr(
        context_module.DevelopmentContextProvider,
        "collect",
        lambda self: {
            "planning": {},
            "current_context": {},
        },
    )
    monkeypatch.setattr(
        context_module.WorkspaceContextProvider,
        "collect",
        lambda self: {},
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

    context = AIContextBuilder(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    ).build()

    assert _RepositoryEngine.calls == 1
    assert _Serializer.calls == 1
    assert "repository_profile" in context
