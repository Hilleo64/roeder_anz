"""Auswahl der im Dashboard angezeigten Ausgabe."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RoedertalIssueSelect(coordinator)])


class RoedertalIssueSelect(CoordinatorEntity, SelectEntity):
    """Dropdown mit den sechs letzten Ausgaben."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:newspaper-variant-outline"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_ausgabe_auswahl"
        self._attr_name = "Ausgabe zum Lesen"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer="Stadt Großröhrsdorf",
            model="Rödertal-Anzeiger",
            name="Rödertal-Anzeiger",
        )

    @property
    def options(self) -> list[str]:
        return [issue["filename"] for issue in self.coordinator.data.get("archive", [])]

    @property
    def current_option(self) -> str | None:
        selected = self.coordinator.data.get("selected_filename")
        if selected in self.options:
            return selected
        return self.options[0] if self.options else None

    async def async_select_option(self, option: str) -> None:
        self.coordinator.select_issue(option)
        self.async_write_ha_state()
