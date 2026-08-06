"""Config Flow für den Rödertal-Anzeiger."""

from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class RoedertalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Erster Schritt."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Rödertal-Anzeiger",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=None,
        )