from pathlib import Path

from maxvo.vault import get_vault_path, iter_notes


def test_get_vault_path_default():
    assert get_vault_path().name == "vault"


def test_iter_notes_finds_welcome_note():
    vault_path = get_vault_path()
    titles = {note.title for note in iter_notes(vault_path)}
    assert "Welcome" in titles


def test_iter_notes_skips_obsidian_dir(tmp_path: Path):
    (tmp_path / ".obsidian").mkdir()
    (tmp_path / ".obsidian" / "config.md").write_text("# not a note")
    (tmp_path / "Real Note.md").write_text("---\ntags: [demo]\n---\n\nHello #inline-tag")

    notes = list(iter_notes(tmp_path))

    assert len(notes) == 1
    assert notes[0].title == "Real Note"
    assert notes[0].tags == {"demo", "inline-tag"}
