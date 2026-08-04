from homeassistant.components.sensor import SensorEntity


class RoedertalAnzeigerSensor(SensorEntity):

    _attr_name = "Rödertal-Anzeiger"

    _attr_native_value = "Initialisierung"