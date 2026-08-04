from __future__ import annotations

import logging

from bs4 import BeautifulSoup

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import ARCHIVE_URL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(DataUpdateCoordinator):

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="Rödertal-Anzeiger",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):

        session = async_get_clientsession(self.hass)

        try:

            response = await session.get(ARCHIVE_URL)

            html = await response.text()

        except Exception as err:
            raise UpdateFailed(err) from err

        soup = BeautifulSoup(html, "html.parser")

        pdf = None

        for link in soup.find_all("a"):

            href = link.get("href")

            if href and href.endswith(".pdf"):
                pdf = href
                break

        if pdf is None:
            raise UpdateFailed("Keine PDF gefunden")

        return {
            "pdf": pdf,
        }