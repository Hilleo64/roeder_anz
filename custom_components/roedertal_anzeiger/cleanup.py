"""Archivbereinigung."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

_LOGGER = logging.getLogger(__name__)


def cleanup_archive(
    archive: Path,
    keep_days: int,
    keep_files: int | None = None,
) -> int:
    """
    Bereinigt das Archiv.

    Rückgabe:
        Anzahl gelöschter Dateien.
    """

    if not archive.exists():
        return 0

    deleted = 0

    files = sorted(
        archive.glob("*.pdf"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )

    #
    # 1. Nach Alter löschen
    #

    limit = datetime.now() - timedelta(days=keep_days)

    for pdf in files.copy():

        modified = datetime.fromtimestamp(
            pdf.stat().st_mtime
        )

        if modified >= limit:
            continue

        try:
            pdf.unlink()

            deleted += 1

            files.remove(pdf)

            _LOGGER.info(
                "Archivdatei gelöscht: %s",
                pdf.name,
            )

        except OSError as err:

            _LOGGER.warning(
                "Datei konnte nicht gelöscht werden: %s (%s)",
                pdf.name,
                err,
            )

    #
    # 2. Maximale Anzahl Dateien
    #

    if keep_files is not None:

        for pdf in files[keep_files:]:

            try:

                pdf.unlink()

                deleted += 1

                _LOGGER.info(
                    "Archivdatei gelöscht (Limit): %s",
                    pdf.name,
                )

            except OSError as err:

                _LOGGER.warning(
                    "Datei konnte nicht gelöscht werden: %s (%s)",
                    pdf.name,
                    err,
                )

    return deleted