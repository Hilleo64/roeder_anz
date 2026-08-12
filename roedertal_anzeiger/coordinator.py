"""Coordinator für den Rödertal-Anzeiger."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .archive import get_archive
from .cleanup import cleanup_archive
from .const import (
    ARCHIVE_URL,
    CONF_KEEP_DAYS,
    CONF_SCAN_INTERVAL,
    DEFAULT_KEEP_DAYS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    EVENT_NEW_ISSUE,
)
from .downloader import download_issue, set_selected_issue
from .parser import Issue, parse_archive

_LOGGER = logging.getLogger(__name__)


class RoedertalCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator für den Rödertal-Anzeiger."""

    def __init__(self, hass, entry: ConfigEntry) -> None:
        self.hass = hass
        self.config_entry = entry
        self._last_issue: str | None = None
        self._initialized = False

        interval = timedelta(
            hours=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=interval,
        )

    async def _async_update_data(self) -> dict:
        """Aktualisiert die sechs neuesten Ausgaben."""

        session = async_get_clientsession(self.hass)

        try:
            async with session.get(ARCHIVE_URL) as response:
                response.raise_for_status()
                html = await response.text()

            issues = parse_archive(html, limit=6)
            downloaded_issues: list[Issue] = []
            paths: list[Path] = []

            for issue in issues:
                pdf_path, downloaded = await download_issue(
                    session=session,
                    issue=issue,
                    config_dir=self.hass.config.config_dir,
                )
                paths.append(pdf_path)
                if downloaded:
                    downloaded_issues.append(issue)

            newest = issues[0]
            is_first_update = not self._initialized
            self._initialized = True

            # Beim ersten Lauf werden die letzten sechs Ausgaben nachgeladen,
            # aber dafür keine sechs Pushmeldungen erzeugt.
            if not is_first_update and self._last_issue != newest.issue:
                for issue in downloaded_issues:
                    self.hass.bus.async_fire(
                        EVENT_NEW_ISSUE,
                        {
                            "issue": issue.issue,
                            "title": issue.title,
                            "date": issue.date.isoformat() if issue.date else None,
                            "filename": issue.filename,
                            "url": issue.url,
                        },
                    )

            self._last_issue = newest.issue

            archive_dir = Path(self.hass.config.path("www")) / "anzeiger" / "archiv"
            cleanup_archive(
                archive_dir,
                self.config_entry.options.get(CONF_KEEP_DAYS, DEFAULT_KEEP_DAYS),
                keep_count=6,
            )

            archive = get_archive(archive_dir.parent)
            available = {issue.filename for issue in issues}
            archive = [name for name in archive if name in available]

            # Bereits ausgewählte Ausgabe beibehalten, solange sie noch im Archiv liegt.
            previous_selected = self.data.get("selected_filename") if self.data else None
            selected = previous_selected if previous_selected in archive else (archive[0] if archive else paths[0].name)
            selected_path = archive_dir / selected
            set_selected_issue(self.hass.config.config_dir, selected_path)

            return {
                "issue": newest.issue,
                "title": newest.title,
                "date": newest.date,
                "filename": newest.filename,
                "url": newest.url,
                "pdf": "/local/anzeiger/aktuell.pdf",
                "selected_pdf": "/local/anzeiger/aktuell.pdf",
                "local": str(paths[0]),
                "downloaded": bool(downloaded_issues),
                "archive": [
                    {
                        "issue": issue.issue,
                        "title": issue.title,
                        "date": issue.date,
                        "filename": issue.filename,
                        "url": issue.url,
                        "local": str(archive_dir / issue.filename),
                    }
                    for issue in issues
                    if (archive_dir / issue.filename).exists()
                ],
                "archive_count": len(archive),
                "selected_filename": selected,
                "last_update": datetime.now().isoformat(),
            }

        except ClientError as err:
            raise UpdateFailed(f"Netzwerkfehler: {err}") from err
        except Exception as err:
            raise UpdateFailed(str(err)) from err

    def select_issue(self, filename: str) -> None:
        """Wählt eine archivierte Ausgabe für die Anzeige aus."""

        for issue in self.data.get("archive", []):
            if issue["filename"] == filename:
                set_selected_issue(
                    self.hass.config.config_dir,
                    Path(issue["local"]),
                )
                self.data["selected_filename"] = filename
                self.async_update_listeners()
                return

    async def async_manual_refresh(self) -> None:
        """Manuelle Aktualisierung."""

        await self.async_request_refresh()
