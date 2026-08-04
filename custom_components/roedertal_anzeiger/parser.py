from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .const import BASE_URL


@dataclass(slots=True)
class Issue:
    """Beschreibt eine Ausgabe des Rödertal-Anzeigers."""

    title: str
    url: str
    date: datetime | None


def parse_archive(html: str) -> Issue:
    """Liest die neueste Ausgabe aus der Archivseite."""

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if not href.lower().endswith(".pdf"):
            continue

        title = link.get_text(" ", strip=True)

        date = None

        for parent in link.parents:

            text = parent.get_text(" ", strip=True)

            import re

            match = re.search(
                r"(\d{2}\.\d{2}\.\d{4})",
                text,
            )

            if match:

                try:

                    date = datetime.strptime(
                        match.group(1),
                        "%d.%m.%Y",
                    )

                except ValueError:
                    pass

                break

        return Issue(
            title=title,
            url=urljoin(BASE_URL, href),
            date=date,
        )

    raise RuntimeError(
        "Keine PDF-Ausgabe gefunden."
    )