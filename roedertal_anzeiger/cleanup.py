"""Archivbereinigung für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

_LOGGER = logging.getLogger(__name__)


def cleanup_archive(folder: Path, keep_days: int) -> int:
    """Löscht PDF-Dateien, die älter als ``keep_days`` Tage sind.

    Args:
        folder: Archivordner mit den PDF-Dateien.
        keep_days: Anzahl der Tage, die Dateien aufbewahrt werden.

    Returns:
        Anzahl der gelöschten Dateien.
    """

    if not folder.exists():
        return 0

    cutoff = datetime.now() - timedelta(days=keep_days)

    deleted = 0

    for pdf in folder.glob("*.pdf"):

        # aktuelle Ausgabe niemals löschen
        if pdf.name == "aktuell.pdf":
            continue

        modified = datetime.fromtimestamp(pdf.stat().st_mtime)

        if modified >= cutoff:
            continue

        try:
            pdf.unlink()
            deleted += 1
            _LOGGER.info("Archivdatei gelöscht: %s", pdf.name)

        except OSError as err:
            _LOGGER.warning(
                "Konnte %s nicht löschen: %s",
                pdf.name,
                err,
            )

    return deleted