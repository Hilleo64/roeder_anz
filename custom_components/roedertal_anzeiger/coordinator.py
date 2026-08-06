"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import datetime

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .archive import archive_count, list_archive
from .cleanup import cleanup_archive
from .const import (
    ARCHIVE_URL,
    CONF_KEEP_DAYS,
    CONF_KEEP_FILES,
    DEFAULT_KEEP_DAYS,
    DEFAULT_KEEP_FILES,
    DOMAIN,
    UPDATE_INTERVAL,
)
from .downloader import download_issue
from .exceptions import (
    DownloadError,
    ParseError,
)
from .parser import parse_archive

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(
    DataUpdateCoordinator[dict],
):
    """Coordinator."""

    def __init__(
        self,
        hass,
        entry: ConfigEntry,
    ) -> None:

        self.entry = entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict:
        """Aktualisiert die Daten."""

        session = async_get_clientsession(
            self.hass
        )

        try:

            #
            # Archivseite laden
            #

            async with session.get(
                ARCHIVE_URL
            ) as response:

                response.raise_for_status()

                html = await response.text()

            #
            # Parser
            #

            issue = parse_archive(
                html
            )

            #
            # Download
            #

            pdf = await download_issue(
                session=session,
                issue=issue,
                config_dir=self.hass.config.config_dir,
            )

            #
            # Archiv bereinigen
            #

            cleanup_archive(
                pdf.parent,
                keep_days=self.entry.options.get(
                    CONF_KEEP_DAYS,
                    DEFAULT_KEEP_DAYS,
                ),
                keep_files=self.entry.options.get(
                    CONF_KEEP_FILES,
                    DEFAULT_KEEP_FILES,
                ),
            )

            #
            # Archiv lesen
            #

            archive = list_archive(
                self.hass.config.config_dir
            )

            return {

                "status": "ok",

                "issue": issue.issue,

                "title": issue.title,

                "date": issue.date,

                "filename": issue.filename,

                "url": issue.url,

                "pdf": "/local/anzeiger/aktuell.pdf",

                "archive": [
                    pdf.name
                    for pdf in archive
                ],

                "archive_count": archive_count(
                    self.hass.config.config_dir
                ),

                "last_update": datetime.now().isoformat(),

            }

        except ParseError as err:

            raise UpdateFailed(
                f"Parserfehler: {err}"
            ) from err

        except DownloadError as err:

            raise UpdateFailed(
                f"Downloadfehler: {err}"
            ) from err

        except ClientError as err:

            raise UpdateFailed(
                f"Netzwerkfehler: {err}"
            ) from err

        except Exception as err:

            raise UpdateFailed(
                str(err)
            ) from err