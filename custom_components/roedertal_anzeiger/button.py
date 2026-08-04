"""Button-Plattform."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([UpdateButton(coordinator)])


class UpdateButton(CoordinatorEntity, ButtonEntity):
    """Button zum manuellen Aktualisieren."""

    _attr_name = "Jetzt aktualisieren"
    _attr_has_entity_name = True
    _attr_unique_id = "roedertal_update"

    @property
    def icon(self):
        return "mdi:refresh"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer="Stadt Großröhrsdorf",
            model="Rödertal-Anzeiger",
            name="Rödertal-Anzeiger",
        )

    async def async_press(self):
        await self.coordinator.async_request_refresh()