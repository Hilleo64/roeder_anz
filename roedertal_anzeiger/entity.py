"""Gemeinsame Basisklasse für alle Entities."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class RoedertalEntity(CoordinatorEntity):
    """Basisklasse für alle Rödertal-Anzeiger-Entities."""

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer="Stadt Großröhrsdorf",
            model="Rödertal-Anzeiger",
            name="Rödertal-Anzeiger",
        )