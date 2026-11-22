import httpx
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from local_agent.config import get_settings
from local_agent.tools import calculate, get_current_time, read_notes, save_note


class OllamaUnavailable(RuntimeError):
    pass


def build_agent() -> Agent:
    settings = get_settings()
    client = httpx.AsyncClient(timeout=settings.agent_timeout)
    model = OllamaModel(
        settings.agent_model,
        provider=OllamaProvider(base_url=settings.ollama_base_url, http_client=client),
    )
    return Agent(
        model,
        tools=[get_current_time, calculate, save_note, read_notes],
        retries=2,
        instructions=(
            "You are a helpful personal assistant running 100% locally. "
            "Use your tools whenever they can help answer the question. "
            "Keep your answers short and friendly."
        ),
    )


def ensure_ollama_running() -> None:
    """Fail fast with a clear message instead of a cryptic connection error."""
    base = get_settings().ollama_base_url.removesuffix("/v1")
    try:
        httpx.get(f"{base}/api/tags", timeout=5).raise_for_status()
    except httpx.HTTPError as error:
        raise OllamaUnavailable(
            f"Cannot reach Ollama at {base}. Start it with `ollama serve` "
            "and confirm the model is pulled (`ollama list`)."
        ) from error
