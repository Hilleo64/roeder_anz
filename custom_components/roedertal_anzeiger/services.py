"""Services für den Rödertal-Anzeiger."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_services(hass: HomeAssistant):

    async def handle_update(call):

        for coordinator in hass.data.get(DOMAIN, {}).values():

            await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN,
        "update",
        handle_update,
    )