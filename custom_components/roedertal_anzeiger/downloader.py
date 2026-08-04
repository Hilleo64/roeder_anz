"""Download der aktuellen Ausgabe."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from aiohttp import ClientSession

from .parser import Issue

_LOGGER = logging.getLogger(__name__)


async def download_issue(
    session: ClientSession,
    issue: Issue,
    config_dir: str,
) -> tuple[Path, bool]:
    """Lädt eine Ausgabe herunter.

    Rückgabe:
        (Dateipfad, neu_heruntergeladen)
    """

    folder = Path(config_dir) / "www" / "anzeiger"
    folder.mkdir(parents=True, exist_ok=True)

    filename = issue.url.split("/")[-1]
    pdf_path = folder / filename

    downloaded = False

    if not pdf_path.exists():
        _LOGGER.info("Lade %s", issue.url)

        async with session.get(issue.url) as response:
            response.raise_for_status()
            pdf_path.write_bytes(await response.read())

        downloaded = True

    current = folder / "aktuell.pdf"

    shutil.copy2(pdf_path, current)

    return issue, pdf_path, downloaded