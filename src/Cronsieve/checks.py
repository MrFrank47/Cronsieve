"""Controlli strutturali e temporali sulle schedule cron.

Stub: implementazione completa nella Sessione 5.
"""

from __future__ import annotations


class Issue:
    """Un problema rilevato durante i controlli."""

    def __init__(self, severity: str, line_no: int, message: str) -> None:
        self.severity = severity
        self.line_no = line_no
        self.message = message


def run_checks(jobs) -> list[Issue]:
    """Esegue tutti i controlli sui job forniti."""
    raise NotImplementedError("run_checks verra' implementato nella Sessione 5")
