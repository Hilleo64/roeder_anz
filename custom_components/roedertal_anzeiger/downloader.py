"""PDF-Downloader."""

from __future__ import annotations

import shutil
from pathlib import Path

from aiohttp import ClientSession

from .exceptions import DownloadError
from .models import Issue


async def download_issue(
    session: ClientSession,
    issue: Issue,
    config_dir: str,
) -> tuple[Path, bool]:
    """Lädt eine Ausgabe herunter und aktualisiert aktuell.pdf."""

    base = Path(config_dir) / "www" / "anzeiger"
    archive = base / "archiv"

    archive.mkdir(parents=True, exist_ok=True)

    pdf_path = archive / issue.filename

    if not pdf_path.exists():

        async with session.get(issue.url) as response:

            if response.status != 200:
                raise DownloadError(
                    f"Download fehlgeschlagen ({response.status})"
                )

            pdf_path.write_bytes(
                await response.read()
            )

    current = base / "aktuell.pdf"

    shutil.copy2(
        pdf_path,
        current,
    )

    return pdf_path, downloaded