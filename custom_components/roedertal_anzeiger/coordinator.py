"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging

from aiohttp import ClientError

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .cleanup import cleanup_archive
from .const import (
    ARCHIVE_URL,
    DOMAIN,
    KEEP_DAYS,
    UPDATE_INTERVAL,
)
from .downloader import download_issue
from .parser import parse_archive

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(DataUpdateCoordinator):
    """Koordiniert den Abruf der Daten."""

    def __init__(self, hass) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):

        session = async_get_clientsession(self.hass)

        try:

            async with session.get(ARCHIVE_URL) as response:
                response.raise_for_status()
                html = await response.text()

            issue = parse_archive(html)

            issue, pdf_path, downloaded = await download_issue(
                session=session,
                issue=issue,
                config_dir=self.hass.config.config_dir,
            )

            cleanup_archive(
                pdf_path.parent,
                KEEP_DAYS,
            )

            return {
                "title": issue.title,
                "issue": issue.issue,
                "date": issue.date,
                "filename": issue.filename,
                "url": issue.url,
                "downloaded": downloaded,
                "local": str(pdf_path),
            }

        except ClientError as err:
            raise UpdateFailed(f"Netzwerkfehler: {err}") from err

        except Exception as err:
            raise UpdateFailed(str(err)) from err