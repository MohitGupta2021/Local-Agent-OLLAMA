local-agent/
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── src/local_agent/
│   ├── __init__.py
│   ├── config.py        # env-driven settings
│   ├── tools.py         # safe tool implementations
│   ├── agent.py         # agent factory + model wiring
│   └── cli.py           # entrypoint (REPL)
└── tests/
    └── test_tools.py