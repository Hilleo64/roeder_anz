"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(
    DataUpdateCoordinator[dict],
):
    """Zentraler Coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:

        self.entry = entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                hours=DEFAULT_SCAN_INTERVAL,
            ),
        )

    async def _async_update_data(
        self,
    ) -> dict:
        """Aktualisiert die Daten."""

        #
        # Ab alpha4 werden hier
        #
        # parser.py
        # downloader.py
        # cleanup.py
        #
        # aufgerufen.
        #

        return {
            "issue": None,
            "title": None,
            "date": None,
            "pdf": "/local/anzeiger/aktuell.pdf",
            "archive": [],
            "status": "idle",
        }