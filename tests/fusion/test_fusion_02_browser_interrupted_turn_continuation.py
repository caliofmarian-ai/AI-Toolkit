import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_service_exposes_explicit_resume_contract():
    source = read("lib/python/ai_platform/service.py")
    tree = ast.parse(source)

    assert "resume_interrupted_turn: bool = False" in source

    ask_repository = next(
        node
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == "ask_repository"
        )
    )

    resume_branch = next(
        node
        for node in ask_repository.body
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "resume_interrupted_turn"
        )
    )

    assert any(
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "interrupted_turn"
        and any(
            isinstance(operator, ast.Is)
            for operator in node.test.ops
        )
        and any(
            isinstance(comparator, ast.Constant)
            and comparator.value is None
            for comparator in node.test.comparators
        )
        for statement in resume_branch.body
        for node in ast.walk(statement)
    )

    assert any(
        isinstance(node, ast.Raise)
        for statement in resume_branch.body
        for node in ast.walk(statement)
    )
    assert "effective_question = interrupted_turn.content" in source


def test_http_parses_resume_signal():
    source = read(
        "lib/python/runtime/interfaces/http_server.py"
    )

    assert "resume_interrupted_turn = bool(" in source
    assert 'payload.get("resume_interrupted_turn", False)' in source


def test_http_allows_empty_question_for_resume_only():
    source = read(
        "lib/python/runtime/interfaces/http_server.py"
    )

    assert "and not resume_interrupted_turn" in source


def test_http_forwards_resume_signal():
    source = read(
        "lib/python/runtime/interfaces/http_server.py"
    )

    assert (
        "resume_interrupted_turn=resume_interrupted_turn"
        in source
    )


def test_dashboard_exposes_continue_control():
    source = read("lib/python/dashboard/service.py")

    assert 'id="chat-continue"' in source
    assert "Continue interrupted turn" in source


def test_browser_resume_uses_existing_session():
    source = read("lib/python/dashboard/service.py")

    assert "resume_interrupted_turn:true" in source
    assert "session_id:session.value" in source


def test_browser_resume_does_not_resend_question():
    source = read("lib/python/dashboard/service.py")

    marker = "resume_interrupted_turn:true"
    index = source.index(marker)

    nearby = source[max(0, index - 500):index + 200]

    assert 'question:""' in nearby


def test_normal_send_remains_available():
    source = read("lib/python/dashboard/service.py")

    assert 'id="chat-send"' in source
    assert "question.value.trim()" in source
    assert '"/api/ai/chat"' in source


def test_durable_browser_session_binding_remains():
    source = read("lib/python/dashboard/service.py")

    assert "ai_toolkit_partner_session_id" in source
    assert "localStorage.setItem" in source
    assert "localStorage.getItem" in source
