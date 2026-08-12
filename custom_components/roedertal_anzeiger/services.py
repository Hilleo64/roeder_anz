"""Services für den Rödertal-Anzeiger."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_services(hass: HomeAssistant):

    async def handle_update(call):

        for coordinator in hass.data.get(DOMAIN, {}).values():
            # hass.data[DOMAIN] may also contain metadata entries such as
            # ``last_issue``. Only actual coordinators can be refreshed.
            if coordinator is None or not hasattr(coordinator, "async_request_refresh"):
                continue
            await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN,
        "update",
        handle_update,
    )