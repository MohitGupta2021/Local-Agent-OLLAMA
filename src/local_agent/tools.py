import ast
import json
import logging
import operator
from datetime import datetime, timezone
from pathlib import Path

from local_agent.config import get_settings

logger = logging.getLogger(__name__)

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def get_current_time() -> str:
    """Get the current date and time (UTC)."""
    return datetime.now(timezone.utc).strftime("%A, %B %d, %Y at %I:%M %p UTC")


def calculate(expression: str) -> str:
    """Evaluate a basic math expression, e.g. '23 * 7 + 1'."""
    try:
        result = _safe_eval(ast.parse(expression.strip(), mode="eval"))
        return str(result)
    except Exception as error:
        logger.warning("calculation failed expr=%r err=%s", expression, error)
        return f"Error: could not evaluate {expression!r}."


def save_note(note: str) -> str:
    """Save a short note so it can be recalled later."""
    settings = get_settings()
    settings.notes_file.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": datetime.now(timezone.utc).isoformat(), "note": note[:2000]}
    with settings.notes_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")
    return "Note saved."


def read_notes(limit: int = 50) -> str:
    """Read back previously saved notes, most recent first."""
    settings = get_settings()
    if not settings.notes_file.exists():
        return "No notes saved yet."
    lines = settings.notes_file.read_text(encoding="utf-8").splitlines()[-limit:]
    notes = [json.loads(line)["note"] for line in lines if line.strip()]
    return "\n".join(f"- {n}" for n in reversed(notes)) or "No notes saved yet."
