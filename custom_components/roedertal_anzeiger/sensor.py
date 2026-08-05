"""Sensor platform."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class RoedertalSensorDescription(SensorEntityDescription):
    value_key: str


SENSORS = (
    RoedertalSensorDescription(
        key="issue",
        name="Ausgabe",
        icon="mdi:newspaper",
        value_key="issue",
    ),
    RoedertalSensorDescription(
        key="date",
        name="Datum",
        icon="mdi:calendar",
        value_key="date",
    ),
    RoedertalSensorDescription(
        key="filename",
        name="Datei",
        icon="mdi:file-pdf-box",
        value_key="filename",
    ),
    RoedertalSensorDescription(
        key="status",
        name="Status",
        icon="mdi:download",
        value_key="downloaded",
    ),
)


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RoedertalSensor(coordinator, description)
        for description in SENSORS
    )

from .entity import RoedertalEntity

class RoedertalSensor(RoedertalEntity, SensorEntity):

    def __init__(self, coordinator, description):
        super().__init__(coordinator)

        self.entity_description = description

        self._attr_has_entity_name = True

        self._attr_unique_id = f"{DOMAIN}_{description.key}"

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

        return self.coordinator.data.get(
            self.entity_description.value_key
        )