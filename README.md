# maxvo

A personal Obsidian vault plus Python scripts for working with it.

- `vault/` — the Obsidian vault itself (markdown notes, `.obsidian/` config).
- `src/maxvo/` — Python package with scripts/tooling that operate on the vault.

## Setup

```bash
pip install -e ".[dev]"
```

## Usage

```bash
maxvo list   # list all notes in the vault
maxvo tags   # list all tags (frontmatter + inline #tags) used across the vault
```

## Development

```bash
pytest              # run tests
ruff check .         # lint
```

By default the tooling reads the vault at `vault/` next to this README. Point it at a
different location by setting `MAXVO_VAULT_PATH`.
