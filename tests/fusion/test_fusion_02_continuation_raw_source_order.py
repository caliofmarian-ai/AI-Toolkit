from pathlib import Path
import ast


SERVICE = Path(
    "lib/python/ai_platform/service.py"
)


def _ask_repository():
    tree = ast.parse(SERVICE.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == "ask_repository"
        ):
            return node

    raise AssertionError("ask_repository not found")


def test_interruption_is_recovered_before_human_raw_source_creation():
    fn = _ask_repository()

    recovery_line = None
    raw_source_line = None

    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id
                == "recover_interrupted_human_turn"
            ):
                recovery_line = node.lineno

            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "raw_source"
            ):
                raw_source_line = node.lineno

    assert recovery_line is not None
    assert raw_source_line is not None
    assert recovery_line < raw_source_line


def test_raw_source_creation_belongs_to_non_resume_branch():
    fn = _ask_repository()

    resume_if = None

    for node in fn.body:
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "resume_interrupted_turn"
        ):
            resume_if = node
            break

    assert resume_if is not None

    resume_calls = [
        node
        for statement in resume_if.body
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {
            "raw_source",
            "append_raw_source",
        }
    ]

    normal_calls = [
        node
        for statement in resume_if.orelse
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {
            "raw_source",
            "append_raw_source",
        }
    ]

    assert resume_calls == []
    assert any(
        node.func.attr == "raw_source"
        for node in normal_calls
    )
    assert any(
        node.func.attr == "append_raw_source"
        for node in normal_calls
    )


def test_resume_branch_uses_preserved_interrupted_content():
    fn = _ask_repository()

    resume_if = next(
        node
        for node in fn.body
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "resume_interrupted_turn"
        )
    )

    assignments = [
        node
        for statement in resume_if.body
        for node in ast.walk(statement)
        if isinstance(node, ast.Assign)
    ]

    assert any(
        any(
            isinstance(target, ast.Name)
            and target.id == "effective_question"
            for target in assignment.targets
        )
        and isinstance(assignment.value, ast.Attribute)
        and assignment.value.attr == "content"
        for assignment in assignments
    )
