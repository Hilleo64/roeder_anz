"""Download der Ausgaben."""

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
    """Lädt eine Ausgabe herunter, falls sie noch nicht vorhanden ist."""

    base = Path(config_dir) / "www" / "anzeiger"
    archive = base / "archiv"
    archive.mkdir(parents=True, exist_ok=True)

    pdf_path = archive / issue.filename
    downloaded = False

    if not pdf_path.exists():
        _LOGGER.info("Lade %s", issue.url)
        async with session.get(issue.url) as response:
            response.raise_for_status()
            pdf_path.write_bytes(await response.read())
        downloaded = True

    current = base / "aktuell.pdf"
    shutil.copy2(pdf_path, current)

    return pdf_path, downloaded


def set_selected_issue(config_dir: str, pdf_path: Path) -> Path:
    """Kopiert die ausgewählte Ausgabe auf den bestehenden Viewer-Pfad."""

    base = Path(config_dir) / "www" / "anzeiger"
    base.mkdir(parents=True, exist_ok=True)
    selected = base / "aktuell.pdf"
    shutil.copy2(pdf_path, selected)
    return selected
