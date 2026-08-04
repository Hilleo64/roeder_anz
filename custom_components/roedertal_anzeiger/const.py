from datetime import timedelta

DOMAIN = "roedertal_anzeiger"

NAME = "Rödertal-Anzeiger"

BASE_URL = "https://www.grossroehrsdorf.de"

ARCHIVE_URL = (
    "https://www.grossroehrsdorf.de/web/aktuelles/amtsblatt-online"
)

UPDATE_INTERVAL = timedelta(hours=1)