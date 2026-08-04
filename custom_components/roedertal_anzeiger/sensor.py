from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            RoedertalSensor(coordinator),
        ]
    )


class RoedertalSensor(
    CoordinatorEntity,
    SensorEntity,
):

    _attr_name = "Rödertal-Anzeiger"

    @property
    def native_value(self):

        return self.coordinator.data["pdf"]