"""Archivfunktionen."""

from __future__ import annotations

from pathlib import Path


def get_archive(base: Path) -> list[str]:
    """Liefert alle PDF-Dateien im Archiv."""

    archive = base / "archiv"

    if not archive.exists():
        return []

    files = sorted(
        archive.glob("*.pdf"),
        reverse=True,
    )

    return [file.name for file in files]