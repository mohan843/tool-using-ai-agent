# Tool-Using AI Agent

A small, dependency-free Python mini-project that demonstrates an agent routing requests to useful tools: a safe calculator, keyword search over sample notes, and a sandboxed local file reader. It is designed to be runnable and testable without API keys or external services.

> This is a deterministic tool-use demonstration, not an LLM-powered conversational agent. The explicit routing and narrow tool interfaces make the agent's actions easy to inspect.

## Features

- Arithmetic evaluation via a restricted Python syntax tree, never `eval`.
- Case-insensitive search across `.txt` files in the local `data/` directory.
- File reading restricted to the configured data directory and text-like file extensions.
- Interactive REPL and one-shot command-line interface.
- Unit tests using only Python's standard library.

## Setup

Requires Python 3.10 or newer.

```bash
git clone https://github.com/mohan843/tool-using-ai-agent.git
cd tool-using-ai-agent
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

There are no third-party packages to install.

## Usage

Start the interactive agent with `python agent.py`, then try `calc: 12 * (3 + 2)`, `search: RAG`, or `read: sample_notes.txt`. One-shot examples: `python agent.py "calc: 12 * (3 + 2)"`, `python agent.py "search: calculator"`, and `python agent.py "read: sample_notes.txt"`. The file reader supports `.txt`, `.md`, and `.csv` files placed under `data/`.

## Tests

Run `python -m unittest discover -s tests -v`. Tests cover arithmetic, operator restrictions, tool routing, local search, reading, and path-traversal protection.

## Project layout

```text
.
├── agent.py
├── data/
│   └── sample_notes.txt
├── requirements.txt
└── tests/
    └── test_agent.py
```

## Safety notes

The calculator only permits known AST node types and caps expression length, numeric literal size, and exponent magnitude. The file reader resolves requested paths and rejects paths outside its data directory. This is a learning example, not a security boundary for hostile multi-user environments.
