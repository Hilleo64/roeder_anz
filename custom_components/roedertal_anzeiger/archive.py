"""Archivverwaltung."""

from __future__ import annotations

from pathlib import Path

from .const import (
    ARCHIVE_FOLDER,
    PDF_FOLDER,
)


def archive_path(config_dir: str) -> Path:
    """Liefert den Archivordner."""

    return (
        Path(config_dir)
        / "www"
        / PDF_FOLDER
        / ARCHIVE_FOLDER
    )


def list_archive(config_dir: str) -> list[Path]:
    """Liefert alle PDFs im Archiv."""

    folder = archive_path(config_dir)

    if not folder.exists():
        return []

    return sorted(
        folder.glob("*.pdf"),
        reverse=True,
    )


def archive_count(config_dir: str) -> int:
    """Anzahl der archivierten PDFs."""

    return len(
        list_archive(config_dir)
    )


def latest_issue(config_dir: str) -> Path | None:
    """Liefert die neueste Ausgabe."""

    archive = list_archive(config_dir)

    if not archive:
        return None

    return archive[0]

def contains_issue(
    config_dir: str,
    filename: str,
) -> bool:
    """Prüft, ob eine Ausgabe bereits existiert."""

    return (
        archive_path(config_dir)
        / filename
    ).exists()