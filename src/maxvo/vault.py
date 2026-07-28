"""Helpers for locating and reading notes in the Obsidian vault."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter

DEFAULT_VAULT_DIR = Path(__file__).resolve().parents[2] / "vault"
VAULT_PATH_ENV_VAR = "MAXVO_VAULT_PATH"

INLINE_TAG_RE = re.compile(r"(?<!\S)#([A-Za-z0-9_/-]+)")


@dataclass
class Note:
    path: Path
    metadata: dict
    content: str

    @property
    def title(self) -> str:
        return self.path.stem

    @property
    def tags(self) -> set[str]:
        tags = set(self.metadata.get("tags") or [])
        tags.update(INLINE_TAG_RE.findall(self.content))
        return tags


def get_vault_path() -> Path:
    """Resolve the vault directory, honoring MAXVO_VAULT_PATH if set."""
    override = os.environ.get(VAULT_PATH_ENV_VAR)
    return Path(override).expanduser() if override else DEFAULT_VAULT_DIR


def iter_notes(vault_path: Path | None = None):
    """Yield a Note for every markdown file in the vault, skipping .obsidian/."""
    vault_path = vault_path or get_vault_path()
    for path in sorted(vault_path.rglob("*.md")):
        if ".obsidian" in path.parts:
            continue
        post = frontmatter.load(path)
        yield Note(path=path, metadata=post.metadata, content=post.content)
