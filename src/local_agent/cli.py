import logging
import sys

from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior

from local_agent.agent import OllamaUnavailable, build_agent, ensure_ollama_running
from local_agent.config import get_settings

MAX_TURNS = 20  # small local models degrade with long context


def main() -> int:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    try:
        ensure_ollama_running()
        agent = build_agent()
    except OllamaUnavailable as error:
        print(f"Startup failed: {error}", file=sys.stderr)
        return 1

    print("Local agent ready! Type 'quit' to exit.\n")
    history: list = []
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break
        try:
            result = agent.run_sync(user_input, message_history=history)
        except UnexpectedModelBehavior as error:
            print(f"Agent error (check model tag / Ollama logs): {error}\n")
            continue
        history = result.all_messages()[-MAX_TURNS:]
        print(f"\nAgent: {result.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
