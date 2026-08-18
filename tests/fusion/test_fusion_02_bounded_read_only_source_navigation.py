from pathlib import Path

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)
from python.executable_repository_intelligence.runtime_map import (
    _read_text,
)


def _coordinator(tmp_path):
    del tmp_path
    return EpistemicCognitiveCoordinator()


def test_read_navigation_reuses_real_repository_reader(tmp_path):
    source = tmp_path / "lib" / "python" / "sample.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        "VALUE = 42\n",
        encoding="utf-8",
    )

    coordinator = _coordinator(tmp_path)

    result = coordinator.execute_read_navigation(
        "lib/python/sample.py",
        read=_read_text,
        repository_root=tmp_path,
    )

    assert result["schema"] == (
        "FUSION-02-READ-ONLY-SOURCE-1"
    )
    assert result["capability"] == "read"
    assert result["status"] == "RETRIEVED"
    assert result["read_only"] is True
    assert result["bounded"] is True

    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True
    assert result["unknown_is_valid"] is True

    assert result["source_identity_kind"] == (
        "repository-relative-path"
    )
    assert result["source_path"] == (
        "lib/python/sample.py"
    )

    assert result["content"] == "VALUE = 42\n"
    assert result["epistemic_gain"] is True


def test_read_navigation_is_bounded_to_one_selected_source(
    tmp_path,
):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"

    first.write_text(
        "FIRST-SOURCE",
        encoding="utf-8",
    )
    second.write_text(
        "SECOND-MUST-NOT-ENTER",
        encoding="utf-8",
    )

    coordinator = _coordinator(tmp_path)

    result = coordinator.execute_read_navigation(
        "first.txt",
        read=_read_text,
        repository_root=tmp_path,
    )

    assert result["content"] == "FIRST-SOURCE"
    assert "SECOND-MUST-NOT-ENTER" not in repr(result)


def test_read_navigation_preserves_unknown_for_missing_source(
    tmp_path,
):
    coordinator = _coordinator(tmp_path)

    result = coordinator.execute_read_navigation(
        "missing.txt",
        read=_read_text,
        repository_root=tmp_path,
    )

    assert result["status"] == "UNKNOWN"
    assert result["content"] == ""
    assert result["epistemic_gain"] is False

    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True
    assert result["unknown_is_valid"] is True


def test_read_navigation_rejects_parent_escape(tmp_path):
    outside = tmp_path.parent / (
        "fusion02-outside-must-not-be-read.txt"
    )

    outside.write_text(
        "OUTSIDE",
        encoding="utf-8",
    )

    try:
        coordinator = _coordinator(tmp_path)

        result = coordinator.execute_read_navigation(
            "../fusion02-outside-must-not-be-read.txt",
            read=_read_text,
            repository_root=tmp_path,
        )

        assert result["status"] == "UNKNOWN"
        assert result["content"] == ""
        assert "OUTSIDE" not in repr(result)
        assert result["epistemic_gain"] is False
    finally:
        if outside.exists():
            outside.unlink()


def test_read_navigation_rejects_absolute_source_identity(
    tmp_path,
):
    source = tmp_path / "absolute.txt"

    source.write_text(
        "ABSOLUTE-MUST-NOT-BE-READ",
        encoding="utf-8",
    )

    coordinator = _coordinator(tmp_path)

    result = coordinator.execute_read_navigation(
        str(source.resolve()),
        read=_read_text,
        repository_root=tmp_path,
    )

    assert result["status"] == "UNKNOWN"
    assert result["content"] == ""
    assert "ABSOLUTE-MUST-NOT-BE-READ" not in repr(result)


def test_read_navigation_does_not_mutate_repository(tmp_path):
    source = tmp_path / "sample.txt"

    source.write_text(
        "immutable",
        encoding="utf-8",
    )

    before = {
        path.relative_to(tmp_path).as_posix():
        path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    coordinator = _coordinator(tmp_path)

    coordinator.execute_read_navigation(
        "sample.txt",
        read=_read_text,
        repository_root=tmp_path,
    )

    after = {
        path.relative_to(tmp_path).as_posix():
        path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    assert after == before
