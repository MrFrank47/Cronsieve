# Cronsieve

A zero-dependency, offline Python CLI utility that parses `crontab` files, translates schedules into plain human-readable descriptions, calculates upcoming execution times, and flags syntax errors or scheduling overlaps.

## Key Features

- **Plain-Language Translation:** Converts standard 5-field cron expressions and macros (`@daily`, `@weekly`, `@hourly`, etc.) into clear, deterministic descriptions.
- **Upcoming Executions (`--next N`):** Computes the exact next $N$ run timestamps, handling leap years, month lengths, and standard cron `OR` semantics between day-of-month and day-of-week.
- **Static Schedule Diagnostics:** Detects invalid field ranges, impossible calendar dates (e.g., February 31), duplicate jobs, and overlapping executions within the same minute.
- **Structured Output (`--json`):** Supports machine-readable JSON reporting alongside clean terminal output.

## Scope & Design Principles

- **100% Local & Read-Only:** Reads plain-text crontab files without modifying the system crontab or executing any scheduled commands.
- **Zero External Dependencies:** Built purely on the Python standard library with no network calls, external APIs, or AI services.

## Project Structure

```text
Cronsieve/
├── pyproject.toml
├── src/
│   └── Cronsieve/
│       ├── __init__.py
│       ├── cli.py          # Command-line argument parsing and output formatting
│       ├── parser.py       # Crontab line tokenization, comments, variables, and macros
│       ├── schedule.py     # 5-field expression parsing and next-N timestamp calculation
│       ├── describe.py     # Deterministic human-readable schedule descriptions
│       └── checks.py       # Syntax validation, impossible dates, duplicates, and overlaps
└── tests/
    ├── test_parser.py
    └── fixtures/
