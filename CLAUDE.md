# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Obsidian vault (`vault/`) plus a Python package (`src/maxvo/`) of scripts/tooling
that operate on it. The vault's markdown notes are committed alongside the code that processes
them — this is not a general-purpose library, it's tooling for one specific vault.

## Commands

```bash
pip install -e ".[dev]"   # install package + dev deps (click, python-frontmatter, pytest, ruff)

pytest                    # run all tests
pytest tests/test_vault.py::test_iter_notes_skips_obsidian_dir   # run a single test

ruff check .               # lint

maxvo list                 # list all notes in the vault (paths relative to vault root)
maxvo tags                  # list all unique tags (frontmatter `tags:` + inline #tags) across the vault
```

## Architecture

- `src/maxvo/vault.py` is the only place that knows how to locate and read the vault. All
  scripts should go through `iter_notes()` / `get_vault_path()` rather than walking `vault/`
  directly, so vault location and note-parsing stay consistent.
  - Vault location resolution: `MAXVO_VAULT_PATH` env var if set, otherwise `vault/` at the repo
    root (`DEFAULT_VAULT_DIR` in `vault.py`).
  - `iter_notes()` skips anything under `.obsidian/` and yields a `Note` per `.md` file, parsed
    with `python-frontmatter` (so `note.metadata` is the YAML frontmatter dict and
    `note.content` is the body with frontmatter stripped).
  - `Note.tags` merges frontmatter `tags:` with inline `#tags` scraped from the body via regex
    — use this instead of reading `metadata["tags"]` directly, since notes mix both styles.
- `src/maxvo/cli.py` is a thin `click` CLI (`maxvo` entry point) over `vault.py`. New scripts
  should generally be added as new `@main.command()`s here, built on top of `iter_notes()`.
- `vault/.obsidian/workspace*.json` and `.obsidian/cache` are gitignored (machine-specific
  Obsidian UI state); `.obsidian/` config and installed plugins are otherwise kept in the repo.
