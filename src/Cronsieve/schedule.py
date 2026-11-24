"""Parsing e calcolo delle prossime esecuzioni di una schedule cron.

Stub: implementazione completa nelle Sessioni 2 e 3.
"""

from __future__ import annotations


class Schedule:
    """Rappresenta i 5 campi di una schedule cron."""

    def __init__(self) -> None:
        raise NotImplementedError("Schedule verra' implementato nelle Sessioni 2-3")


def build_schedule(fields: list[str]) -> Schedule:
    """Costruisce una Schedule dai 5 campi cron."""
    raise NotImplementedError("build_schedule verra' implementato nella Sessione 2")


def next_executions(
    schedule: Schedule,
    from_datetime,
    n: int,
    max_iterations: int = 500000,
):
    """Restituisce le prossime N date/ore di esecuzione."""
    raise NotImplementedError("next_executions verra' implementato nella Sessione 3")
