"""Löscht alte Ausgaben."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path


def cleanup_archive(folder: Path, keep_days: int = 183) -> None:
    """Entfernt alte PDF-Dateien."""

    limit = datetime.now() - timedelta(days=keep_days)

    for pdf in folder.glob("*.pdf"):

        if pdf.name == "aktuell.pdf":
            continue

        modified = datetime.fromtimestamp(pdf.stat().st_mtime)

        if modified < limit:
            pdf.unlink()