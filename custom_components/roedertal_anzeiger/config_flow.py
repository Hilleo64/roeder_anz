from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN

from homeassistant.core import callback
import voluptuous as vol

from .const import (
    CONF_KEEP_DAYS,
    CONF_NOTIFY,
    CONF_SCAN_INTERVAL,
    DEFAULT_KEEP_DAYS,
    DEFAULT_NOTIFY,
    DEFAULT_SCAN_INTERVAL,
)

class RoedertalAnzeigerConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance_allowed"
            )

        return self.async_create_entry(
            title="Rödertal-Anzeiger",
            data={},
        )

@staticmethod
@callback
def async_get_options_flow(config_entry):
    return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=options.get(
                            CONF_SCAN_INTERVAL,
                            DEFAULT_SCAN_INTERVAL,
                        ),
                    ): vol.All(
                        int,
                        vol.Range(min=1, max=24),
                    ),

                    vol.Required(
                        CONF_KEEP_DAYS,
                        default=options.get(
                            CONF_KEEP_DAYS,
                            DEFAULT_KEEP_DAYS,
                        ),
                    ): vol.All(
                        int,
                        vol.Range(min=30, max=365),
                    ),

                    vol.Required(
                        CONF_NOTIFY,
                        default=options.get(
                            CONF_NOTIFY,
                            DEFAULT_NOTIFY,
                        ),
                    ): bool,
                }
            ),
        )