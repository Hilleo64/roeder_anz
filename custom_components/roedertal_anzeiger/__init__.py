from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import RoedertalCoordinator
from .const import DOMAIN
from .services import async_setup_services

PLATFORMS = [
    "sensor",
    "button",
]

async def async_setup(hass, config):
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    coordinator = RoedertalCoordinator(hass)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[
        entry.entry_id
    ] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True