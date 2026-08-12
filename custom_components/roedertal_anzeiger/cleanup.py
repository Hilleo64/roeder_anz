"""Archivbereinigung für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

_LOGGER = logging.getLogger(__name__)


def cleanup_archive(folder: Path, keep_days: int, keep_count: int = 6) -> int:
    """Hält maximal ``keep_count`` PDFs und entfernt sehr alte Dateien."""

    if not folder.exists():
        return 0

    files = sorted(
        (pdf for pdf in folder.glob("*.pdf") if pdf.name != "aktuell.pdf"),
        key=lambda pdf: pdf.stat().st_mtime,
        reverse=True,
    )
    cutoff = datetime.now() - timedelta(days=keep_days)
    deleted = 0

    for index, pdf in enumerate(files):
        if index < keep_count and datetime.fromtimestamp(pdf.stat().st_mtime) >= cutoff:
            continue
        try:
            pdf.unlink()
            deleted += 1
            _LOGGER.info("Archivdatei gelöscht: %s", pdf)
        except OSError as err:
            _LOGGER.warning("Konnte %s nicht löschen: %s", pdf, err)

    return deleted
