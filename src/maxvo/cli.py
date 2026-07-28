"""Command-line entry point: `maxvo`."""

from __future__ import annotations

import click

from .vault import get_vault_path, iter_notes


@click.group()
def main() -> None:
    """Scripts for working with the maxvo Obsidian vault."""


@main.command("list")
def list_notes() -> None:
    """List every note in the vault, relative to the vault root."""
    vault_path = get_vault_path()
    for note in iter_notes(vault_path):
        click.echo(note.path.relative_to(vault_path))


@main.command("tags")
def list_tags() -> None:
    """List every unique tag (frontmatter + inline #tags) used in the vault."""
    tags: set[str] = set()
    for note in iter_notes():
        tags.update(note.tags)
    for tag in sorted(tags):
        click.echo(tag)


if __name__ == "__main__":
    main()
