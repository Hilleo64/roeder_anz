from datetime import timedelta

DOMAIN = "roedertal_anzeiger"

BASE_URL = "https://www.grossroehrsdorf.de"

ARCHIVE_URL = (
    "https://www.grossroehrsdorf.de/web/aktuelles/amtsblatt-online"
)

CONF_SCAN_INTERVAL = "scan_interval"
CONF_KEEP_DAYS = "keep_days"
CONF_NOTIFY = "notify"

DEFAULT_SCAN_INTERVAL = 6
DEFAULT_KEEP_DAYS = 183
DEFAULT_NOTIFY = True

EVENT_NEW_ISSUE = "roedertal_anzeiger_new_issue"

UPDATE_INTERVAL = timedelta(hours=DEFAULT_SCAN_INTERVAL)