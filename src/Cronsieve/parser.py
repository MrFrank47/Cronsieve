"""Parser di file crontab.

Legge righe vuote, commenti, variabili d'ambiente e macro standard
(@hourly, @daily, @weekly, @monthly, @yearly). Implementato interamente
da zero, senza dipendenze esterne.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


MACROS = {
    "@hourly": "0 * * * *",
    "@daily": "0 0 * * *",
    "@weekly": "0 0 * * 0",
    "@monthly": "0 0 1 * *",
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@midnight": "0 0 * * *",
}

ENV_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


@dataclass
class CronJob:
    """Un singolo job cron parsato."""

    line_no: int
    minute: str
    hour: str
    dom: str
    month: str
    dow: str
    command: str
    raw_line: str


@dataclass
class CronEnv:
    """Una variabile d'ambiente definita nel crontab."""

    line_no: int
    name: str
    value: str


@dataclass
class CronFile:
    """Risultato del parsing di un intero file crontab."""

    jobs: list[CronJob] = field(default_factory=list)
    envs: list[CronEnv] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _expand_macro(fields: list[str]) -> list[str] | None:
    """Espande una macro @... in testa alla riga nei 5 campi cron.

    Restituisce la lista dei 5 campi espansi, oppure None se il primo
    token non è una macro.
    """
    if not fields:
        return None
    first = fields[0].strip()
    if first in MACROS:
        return MACROS[first].split()
    return None


def parse_file(path: str | Path) -> CronFile:
    """Parsa un file crontab e restituisce una :class:`CronFile`.

    Ogni errore di sintassi viene registrato in ``errors`` con il numero
    di riga; il parsing prosegue sulle righe successive.
    """
    result = CronFile()
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()

        # Righe vuote e commenti
        if not line or line.startswith("#"):
            continue

        # Variabili d'ambiente: NOME=valore
        env_match = ENV_RE.match(line)
        if env_match:
            result.envs.append(
                CronEnv(
                    line_no=idx,
                    name=env_match.group(1),
                    value=env_match.group(2).strip(),
                )
            )
            continue

        # Righe cron: 5 campi + comando (il comando puo' contenere spazi)
        tokens = line.split(None, 5)

        macro_fields = _expand_macro(tokens)
        if macro_fields is not None:
            if len(tokens) > 1:
                fields = macro_fields + [tokens[1]]
            else:
                fields = macro_fields + [""]
        else:
            fields = tokens

        if len(fields) < 6:
            result.errors.append(
                f"riga {idx}: campi insufficienti (attesi 5 campi + comando, "
                f"trovati {len(fields) - 1}): {raw}"
            )
            continue

        minute, hour, dom, month, dow, command = (
            fields[0],
            fields[1],
            fields[2],
            fields[3],
            fields[4],
            fields[5],
        )

        result.jobs.append(
            CronJob(
                line_no=idx,
                minute=minute,
                hour=hour,
                dom=dom,
                month=month,
                dow=dow,
                command=command,
                raw_line=raw,
            )
        )

    return result
