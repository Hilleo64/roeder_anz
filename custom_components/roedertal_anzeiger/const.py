"""Konstanten für den Rödertal-Anzeiger."""

from datetime import timedelta

DOMAIN = "roedertal_anzeiger"

NAME = "Rödertal-Anzeiger"

ARCHIVE_URL = (
    "https://www.roedertal-anzeiger.de/archiv"
)

DEFAULT_SCAN_INTERVAL = 6
DEFAULT_KEEP_DAYS = 183

UPDATE_INTERVAL = timedelta(
    hours=DEFAULT_SCAN_INTERVAL,
)

PDF_FOLDER = "anzeiger"
ARCHIVE_FOLDER = "archiv"
CURRENT_PDF = "aktuell.pdf"

EVENT_NEW_ISSUE = (
    "roedertal_anzeiger_new_issue"
)

CONF_SCAN_INTERVAL = "scan_interval"
CONF_KEEP_DAYS = "keep_days"