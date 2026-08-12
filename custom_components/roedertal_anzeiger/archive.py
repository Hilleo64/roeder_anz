"""Archivfunktionen."""

from __future__ import annotations

from pathlib import Path


def get_archive(base: Path) -> list[str]:
    """Liefert alle PDF-Dateien im Archiv, neueste zuerst."""

    archive = base / "archiv"
    if not archive.exists():
        return []

    files = sorted(
        archive.glob("*.pdf"),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )
    return [file.name for file in files]
