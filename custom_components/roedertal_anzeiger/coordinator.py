"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import timedelta

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .cleanup import cleanup_archive
from .const import (
    ARCHIVE_URL,
    CONF_KEEP_DAYS,
    CONF_SCAN_INTERVAL,
    DEFAULT_KEEP_DAYS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .downloader import download_issue
from .parser import parse_archive

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(DataUpdateCoordinator[dict]):
    """Koordiniert den Abruf des Rödertal-Anzeigers."""

    def __init__(self, hass, entry: ConfigEntry) -> None:
        """Initialisieren."""

        self.hass = hass
        self.config_entry = entry

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

            pdf_path, downloaded = await download_issue(
                session=session,
                issue=issue,
                config_dir=self.hass.config.config_dir,
            )

            cleanup_archive(
                pdf_path.parent,
                self.config_entry.options.get(
                    CONF_KEEP_DAYS,
                    DEFAULT_KEEP_DAYS,
                ),
            )

            from datetime import datetime
            from .const import EVENT_NEW_ISSUE

            previous = getattr(self, "_last_issue", None)

            if downloaded and previous != issue.issue:
                self.hass.bus.async_fire(
                    EVENT_NEW_ISSUE,
                    {
                        "issue": issue.issue,
                        "title": issue.title,
                        "date": issue.date.isoformat() if issue.date else None,
                        "filename": issue.filename,
                        "url": issue.url,
                    },
                )

            self._last_issue = issue.issue

            return {
                "issue": issue.issue,
                "title": issue.title,
                "date": issue.date,
                "filename": issue.filename,
                "url": issue.url,
                "downloaded": downloaded,
                "local": str(pdf_path),
                "last_update": datetime.now().isoformat(),
            }

        except ClientError as err:
            raise UpdateFailed(
                f"Netzwerkfehler: {err}"
            ) from err

        except Exception as err:
            raise UpdateFailed(str(err)) from err

    async def async_manual_refresh(self) -> None:
        """Manuelles Aktualisieren."""

        await self.async_request_refresh()