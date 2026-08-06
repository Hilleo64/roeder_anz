"""Registriert das Frontend-Panel."""

from __future__ import annotations

from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.core import HomeAssistant


async def async_setup_panel(
    hass: HomeAssistant,
) -> None:
    """Registriert das Panel."""

    async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="Rödertal-Anzeiger",
        sidebar_icon="mdi:newspaper",
        frontend_url_path="roedertal-anzeiger",
        config={
            "module_url": "/local/roedertal_anzeiger/panel.js",
        },
        require_admin=False,
    )