"""Sensoren für den Rödertal-Anzeiger."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            RoedertalIssueSensor(coordinator),
        ]
    )


class RoedertalIssueSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Sensor der aktuellen Ausgabe."""

    _attr_has_entity_name = True
    _attr_name = "Aktuelle Ausgabe"
    _attr_unique_id = "roedertal_current_issue"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer="Stadt Großröhrsdorf",
            model="Rödertal-Anzeiger",
            name="Rödertal-Anzeiger",
        )

    @property
    def native_value(self):
        return self.coordinator.data["filename"]

    @property
    def extra_state_attributes(self):

        return {
            "Titel": self.coordinator.data["title"],
            "Datum": self.coordinator.data["date"],
            "PDF": self.coordinator.data["url"],
            "Lokale Datei": self.coordinator.data["local"],
            "Neu heruntergeladen": self.coordinator.data["downloaded"],
        }

    @property
    def icon(self):
        return "mdi:newspaper"