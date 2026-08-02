# maxvo

A personal Obsidian vault plus Python scripts for working with it.

Open this repo root in Obsidian — that's the vault (`.obsidian/` config lives here), so skills,
docs, and CLAUDE.md are all editable from within Obsidian too, not just the notes.

- `vault/` — the markdown notes the `maxvo` tooling operates on.
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
