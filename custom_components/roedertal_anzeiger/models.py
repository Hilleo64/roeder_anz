from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Issue:
    """Eine Ausgabe des Rödertal-Anzeigers."""

    issue: str
    title: str
    filename: str
    url: str
    date: date | None = None