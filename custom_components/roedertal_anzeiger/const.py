from datetime import timedelta

DOMAIN = "roedertal_anzeiger"

BASE_URL = "https://www.grossroehrsdorf.de"

ARCHIVE_URL = (
    "https://www.grossroehrsdorf.de/web/aktuelles/amtsblatt-online"
)

UPDATE_INTERVAL = timedelta(hours=6)

KEEP_DAYS = 183