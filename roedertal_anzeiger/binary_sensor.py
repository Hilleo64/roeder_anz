"""Binary Sensor."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import RoedertalEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            RoedertalDownloadSensor(coordinator),
        ]
    )


class RoedertalDownloadSensor(
    RoedertalEntity,
    BinarySensorEntity,
):

    _attr_has_entity_name = True
    _attr_name = "Neue Ausgabe"

    @property
    def is_on(self):

        return bool(
            self.coordinator.data.get(
                "downloaded",
                False,
            )
        )

    @property
    def icon(self):

        if self.is_on:
            return "mdi:newspaper-plus"

        return "mdi:newspaper-minus"