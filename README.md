# Local Agent

Local Agent is a command-line personal assistant that runs against a model served
by [Ollama](https://ollama.com). It uses Pydantic AI to connect to Ollama's
OpenAI-compatible API and provide a small set of local tools.

## Features

- Interactive terminal chat with an Ollama model.
- UTC date and time lookup.
- Basic arithmetic evaluation.
- Save and retrieve notes stored locally as JSON Lines.
- Configuration through environment variables or a `.env` file.

## Requirements

- Python 3.15 or newer.
- [uv](https://docs.astral.sh/uv/) for dependency management and running the app.
- [Ollama](https://ollama.com/download) installed and running.
- The model configured in `AGENT_MODEL` pulled into Ollama.

The example configuration uses `qwen3:4b-instruct`. Pull it with:

```powershell
ollama pull qwen3:4b-instruct
```

If Ollama is not already running as a background service, start it in a
separate terminal:

```powershell
ollama serve
```

## Setup

From the project directory, create your local configuration and install the
project:

```powershell
Copy-Item .env.example .env
uv sync
```

Edit `.env` if needed. In particular, `AGENT_MODEL` must exactly match a model
tag shown by `ollama list`.

## Run

```powershell
uv run local-agent
```

Type a message at the `You:` prompt. Enter `quit` or `exit` to stop the
assistant. Ctrl+C also exits; on Windows, Ctrl+Z followed by Enter sends EOF.

The app checks that Ollama is reachable at startup. Notes are written to
`data/notes.jsonl` by default, and the `data` directory is created when a note
is first saved.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama's OpenAI-compatible API base URL. |
| `AGENT_MODEL` | `qwen2.5:3b` | Ollama model tag to use. The `.env.example` file selects `qwen3:4b-instruct`. |
| `AGENT_TIMEOUT` | `60` | HTTP timeout in seconds; must be greater than zero. |
| `NOTES_FILE` | `data/notes.jsonl` | File used to store notes. Relative paths are resolved from the current working directory. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

Values in `.env` override the defaults. The application reads `.env` from the
current working directory.

## Troubleshooting

- **Cannot reach Ollama:** Start Ollama and check that
  `OLLAMA_BASE_URL` points to its OpenAI-compatible API. The default local URL
  is `http://localhost:11434/v1`.
- **Model not found or unavailable:** Run `ollama list`, then set `AGENT_MODEL`
  to the exact installed tag. Pull a model with `ollama pull <model-tag>`.
- **Startup fails while constructing the agent:** Confirm dependencies are
  installed with `uv sync`, then retry `uv run local-agent`.

## Project layout

```text
src/local_agent/
├── agent.py   # Ollama connection and agent construction
├── cli.py     # Command-line REPL and entry point
├── config.py  # Environment-based settings
└── tools.py   # Time, calculator, and note tools
```
