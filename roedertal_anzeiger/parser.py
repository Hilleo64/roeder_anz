"""Parser für den Rödertal-Anzeiger."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .const import BASE_URL


@dataclass(slots=True)
class Issue:
    """Eine Ausgabe des Rödertal-Anzeigers."""

    issue: str
    title: str
    url: str
    filename: str
    date: datetime | None


def parse_archive(html: str, limit: int = 6) -> list[Issue]:
    """Ermittelt die neuesten PDF-Ausgaben."""

    soup = BeautifulSoup(html, "html.parser")
    issues: list[Issue] = []
    seen: set[str] = set()

    for link in soup.select("a[href$='.pdf'], a[href$='.PDF']"):
        href = link.get("href")
        if not href:
            continue

        filename = href.split("/")[-1]
        key = filename.lower()
        if key in seen:
            continue
        seen.add(key)

        title = link.get_text(" ", strip=True) or filename
        issue = filename.rsplit(".", 1)[0]
        date = None

        # Das Datum steht je nach Seitenlayout im direkten Umfeld des Links.
        context = " ".join(
            part.get_text(" ", strip=True)
            for part in [link.parent, link.parent.parent if link.parent else None]
            if part is not None
        )
        match = re.search(r"(\d{2}\.\d{2}\.\d{4})", context)
        if match:
            try:
                date = datetime.strptime(match.group(1), "%d.%m.%Y")
            except ValueError:
                pass

        issues.append(
            Issue(
                issue=issue,
                title=title,
                url=urljoin(BASE_URL, href),
                filename=filename,
                date=date,
            )
        )

        if len(issues) >= limit:
            break

    if not issues:
        raise RuntimeError("Keine PDF-Ausgaben gefunden.")

    return issues
