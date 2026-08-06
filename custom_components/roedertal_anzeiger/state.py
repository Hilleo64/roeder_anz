"""Statusverwaltung."""

from __future__ import annotations

from pathlib import Path


def state_file(config_dir: str) -> Path:
    """Pfad der Statusdatei."""

    return (
        Path(config_dir)
        / ".storage"
        / "roedertal_anzeiger.json"
    )