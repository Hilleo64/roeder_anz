"""REST API."""

from __future__ import annotations

from homeassistant.components.http import HomeAssistantView

from homeassistant.core import HomeAssistant

from .const import DOMAIN


class RoedertalStateView(HomeAssistantView):
    """Liefert den aktuellen Zustand."""

    url = "/api/roedertal_anzeiger/state"

    name = "api:roedertal_anzeiger:state"

    requires_auth = True

    async def get(self, request):

        hass: HomeAssistant = request.app["hass"]

        entries = hass.data.get(DOMAIN, {})

        if not entries:

            return self.json(
                {
                    "status": "not_loaded",
                }
            )

        coordinator = next(iter(entries.values()))

        return self.json(
            coordinator.data
        )


async def async_setup_api(
    hass: HomeAssistant,
):

    hass.http.register_view(
        RoedertalStateView
    )