"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .archive import get_archive
from .cleanup import cleanup_archive
from .const import (
    ARCHIVE_URL,
    CONF_KEEP_DAYS,
    CONF_SCAN_INTERVAL,
    DEFAULT_KEEP_DAYS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    EVENT_NEW_ISSUE,
)
from .downloader import download_issue
from .parser import parse_archive

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator für den Rödertal-Anzeiger."""

    def __init__(self, hass, entry: ConfigEntry) -> None:
        """Initialisieren."""

        self.hass = hass
        self.config_entry = entry
        self._last_issue: str | None = None

        interval = timedelta(
            hours=entry.options.get(
                CONF_SCAN_INTERVAL,
                DEFAULT_SCAN_INTERVAL,
            )
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=interval,
        )

    async def _async_update_data(self) -> dict:
        """Aktualisiert die Daten."""

        session = async_get_clientsession(self.hass)

        try:
            async with session.get(ARCHIVE_URL) as response:
                response.raise_for_status()
                html = await response.text()

            issue = parse_archive(html)

            downloaded = False

            if self._last_issue != issue.issue:

                pdf_path, downloaded = await download_issue(
                    session=session,
                    issue=issue,
                    config_dir=self.hass.config.config_dir,
                )

                self._last_issue = issue.issue

                cleanup_archive(
                    pdf_path.parent,
                    self.config_entry.options.get(
                        CONF_KEEP_DAYS,
                        DEFAULT_KEEP_DAYS,
                    ),
                )

                if downloaded:
                    self.hass.bus.async_fire(
                        EVENT_NEW_ISSUE,
                        {
                            "issue": issue.issue,
                            "title": issue.title,
                            "date": issue.date.isoformat()
                            if issue.date
                            else None,
                            "filename": issue.filename,
                            "url": issue.url,
                        },
                    )

            else:
                pdf_path = (
                    Path(self.hass.config.path("www"))
                    / "anzeiger"
                    / "aktuell.pdf"
                )

            base = pdf_path.parent.parent

            archive = get_archive(base)

            return {
                "issue": issue.issue,
                "title": issue.title,
                "date": issue.date,
                "filename": issue.filename,
                "url": issue.url,
                "pdf": "/local/anzeiger/aktuell.pdf",
                "local": str(pdf_path),
                "downloaded": downloaded,
                "archive": archive,
                "archive_count": len(archive),
                "last_update": datetime.now().isoformat(),
            }

        except ClientError as err:
            raise UpdateFailed(
                f"Netzwerkfehler: {err}"
            ) from err

        except Exception as err:
            raise UpdateFailed(str(err)) from err

    async def async_manual_refresh(self) -> None:
        """Manuelle Aktualisierung."""

        await self.async_request_refresh()