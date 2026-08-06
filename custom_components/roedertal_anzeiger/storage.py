"""Speichert Integrationsdaten."""

from __future__ import annotations

import json

from .state import state_file


def load_last_issue(config_dir: str) -> str | None:

    file = state_file(config_dir)

    if not file.exists():
        return None

    return json.loads(
        file.read_text(
            encoding="utf-8"
        )
    ).get("last_issue")


def save_last_issue(
    config_dir: str,
    issue: str,
):

    file = state_file(config_dir)

    file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file.write_text(
        json.dumps(
            {
                "last_issue": issue
            },
            indent=2,
        ),
        encoding="utf-8",
    )