"""Parser für den Rödertal-Anzeiger."""

from __future__ import annotations

import re
from datetime import datetime

from bs4 import BeautifulSoup

from .exceptions import ParseError
from .models import Issue


def parse_archive(html: str) -> Issue:
    """Liest die aktuelle Ausgabe aus der Archivseite."""

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if not href.lower().endswith(".pdf"):
            continue

        filename = href.split("/")[-1]

        title = link.get_text(strip=True)

        issue = filename.replace(".pdf", "")

        date = _parse_date(title)

        return Issue(
            issue=issue,
            title=title,
            filename=filename,
            url=href,
            date=date,
        )

    raise ParseError("Keine PDF gefunden")


def _parse_date(text: str):
    """Versucht ein Datum zu erkennen."""

    match = re.search(
        r"(\d{2}\.\d{2}\.\d{4})",
        text,
    )

    if not match:
        return None

    try:
        return datetime.strptime(
            match.group(1),
            "%d.%m.%Y",
        ).date()

    except ValueError:
        return None