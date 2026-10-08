# Tool-Using AI Agent

A dependency-free Python mini-project that routes requests to three local tools: a safe calculator, keyword search over sample notes, and a sandboxed file reader. It runs without API keys or external services. This deterministic demo is not an LLM-powered conversational agent.

## Features

- Arithmetic parsed from a restricted syntax tree, never Python `eval`.
- Case-insensitive keyword search of `.txt` files in `data/`.
- File access constrained to the project data directory and `.txt`, `.md`, or `.csv` files.
- One-shot command-line interface and standard-library unit tests.

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

Run a calculator request:

```bash
python agent.py 'calc: 12 * (3 + 2)'
```

Search the bundled sample data or read it directly:

```bash
python agent.py 'search: RAG'
python agent.py 'read: sample_notes.txt'
```

Supported tool forms are `calc: EXPRESSION`, `search: TERM`, and `read: RELATIVE_PATH`. The calculator supports `+`, `-`, `*`, `/`, `//`, `%`, `**`, and parentheses.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover arithmetic, unsafe-expression rejection, tool routing, local search, file reading, and path-traversal protection.

## Project files

- `agent.py`: agent router and tool implementations
- `data/sample_notes.txt`: example search/read corpus
- `requirements.txt`: documents the Python version; no external dependencies
- `tests/test_agent.py`: automated unit tests

## Safety notes

The calculator permits only known syntax-tree nodes and limits expression size, numeric literals, and exponents. The reader resolves requested paths and rejects anything outside its data directory. This is a learning example, not a security boundary for hostile multi-user environments.
