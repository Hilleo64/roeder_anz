"""Basisklasse aller Entitäten."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN


class RoedertalEntity(
    CoordinatorEntity,
):
    """Basisklasse."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
    ) -> None:

        super().__init__(
            coordinator,
        )

    @property
    def device_info(
        self,
    ):

        return {
            "identifiers": {
                (
                    DOMAIN,
                    DOMAIN,
                )
            },
            "manufacturer": "Hilleo64",
            "name": "Rödertal-Anzeiger",
            "model": "Online-Ausgaben",
        }