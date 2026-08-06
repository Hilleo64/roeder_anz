"""Parser für den Rödertal-Anzeiger."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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


def parse_archive(html: str) -> Issue:
    """Ermittelt die neueste Ausgabe."""

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.select("a[href$='.pdf']"):

        href = link["href"]

        title = link.get_text(" ", strip=True)

        filename = href.split("/")[-1]

        issue = filename.replace(".pdf", "")

        date = None

        parent = link.parent

        if parent:

            import re

            match = re.search(
                r"(\d{2}\.\d{2}\.\d{4})",
                parent.get_text(" ", strip=True),
            )

            if match:
                try:
                    date = datetime.strptime(
                        match.group(1),
                        "%d.%m.%Y",
                    )
                except ValueError:
                    pass

        return Issue(
            issue=issue,
            title=title,
            url=urljoin(BASE_URL, href),
            filename=filename,
            date=date,
        )

    raise RuntimeError("Keine PDF-Ausgabe gefunden.")