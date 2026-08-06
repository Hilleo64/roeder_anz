"""Sensorplattform."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)

from .const import DOMAIN
from .entity import RoedertalEntity


@dataclass(frozen=True, kw_only=True)
class RoedertalSensorDescription(
    SensorEntityDescription,
):
    """Beschreibung eines Sensors."""

    value_key: str


SENSORS = (
    RoedertalSensorDescription(
        key="status",
        name="Status",
        icon="mdi:newspaper",
        value_key="status",
    ),
)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Sensoren laden."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RoedertalSensor(
            coordinator,
            description,
        )
        for description in SENSORS
    )


class RoedertalSensor(
    RoedertalEntity,
    SensorEntity,
):
    """Sensor."""

    entity_description: RoedertalSensorDescription

    def __init__(
        self,
        coordinator,
        description,
    ) -> None:

        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = (
            f"{DOMAIN}_{description.key}"
        )

    @property
    def native_value(
        self,
    ):
        """Sensorwert."""

        return self.coordinator.data.get(
            self.entity_description.value_key
        )

    @property
    def icon(
        self,
    ):
        """Icon."""

        return self.entity_description.icon