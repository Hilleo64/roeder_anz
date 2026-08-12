from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import RoedertalCoordinator
from .const import DOMAIN
from .services import async_setup_services
from .viewer import register_views

PLATFORMS = [
    "sensor",
    "button",
    "binary_sensor",
    "select",
]

async def async_setup(hass, config):
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    coordinator = RoedertalCoordinator(
        hass,
        entry,
    )

    await coordinator.async_config_entry_first_refresh()
    register_views(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault("last_issue", None)

    hass.data.setdefault(DOMAIN, {})[
        entry.entry_id
    ] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True