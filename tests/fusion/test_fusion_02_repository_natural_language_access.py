from pathlib import Path

from python.evidence_engine.engine import EvidenceEngine


def repository(tmp_path: Path) -> Path:
    (tmp_path / "work" / "fusion").mkdir(
        parents=True
    )
    (tmp_path / "lib" / "python" / "ai_platform").mkdir(
        parents=True
    )

    (
        tmp_path
        / "work"
        / "fusion"
        / "FUSION_02_EVOLUTION_TREE.md"
    ).write_text(
        "# FUSION-02\n\nE0-E20\n",
        encoding="utf-8",
    )

    (
        tmp_path
        / "lib"
        / "python"
        / "ai_platform"
        / "service.py"
    ).write_text(
        "class AIPlatformService:\n    pass\n",
        encoding="utf-8",
    )

    (
        tmp_path
        / "lib"
        / "python"
        / "ai_platform"
        / "pipeline.py"
    ).write_text(
        "class AIRequestPipeline:\n    pass\n",
        encoding="utf-8",
    )

    return tmp_path


def flattened(result):
    return (
        result["python"]
        + result["shell"]
        + result["tests"]
        + result["docs"]
    )


def test_natural_language_can_find_fusion_tree(tmp_path):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    result=engine.find(
        "inspecteaza arborele FUSION 02 evolution tree"
    )

    assert (
        "work/fusion/FUSION_02_EVOLUTION_TREE.md"
        in result["docs"]
    )


def test_natural_language_can_find_service_file(tmp_path):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    result=engine.find(
        "inspecteaza AIPlatformService service"
    )

    assert (
        "lib/python/ai_platform/service.py"
        in result["python"]
    )


def test_repository_question_does_not_mean_read_everything(
    tmp_path,
):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    result=engine.find(
        "ce contine repository-ul despre FUSION 02"
    )

    paths=flattened(result)

    assert (
        "work/fusion/FUSION_02_EVOLUTION_TREE.md"
        in paths
    )

    assert (
        "lib/python/ai_platform/pipeline.py"
        not in paths
    )


def test_duplicate_query_terms_do_not_duplicate_results(
    tmp_path,
):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    result=engine.find(
        "fusion fusion FUSION 02 02"
    )

    path="work/fusion/FUSION_02_EVOLUTION_TREE.md"

    assert result["docs"].count(path)==1


def test_exact_filename_remains_supported(tmp_path):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    result=engine.find(
        "FUSION_02_EVOLUTION_TREE.md"
    )

    assert (
        "work/fusion/FUSION_02_EVOLUTION_TREE.md"
        in result["docs"]
    )


def test_repository_root_remains_real_filesystem_authority(
    tmp_path,
):
    root=repository(tmp_path)
    engine=EvidenceEngine(root)

    assert engine.root == root.resolve()

    result=engine.find("service")

    for path in flattened(result):
        target=(root / path).resolve()
        target.relative_to(root.resolve())
        assert target.is_file()
