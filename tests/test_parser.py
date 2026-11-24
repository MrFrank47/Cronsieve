"""Test per il parser di file crontab (parser.py)."""

from __future__ import annotations

import os
import unittest

from cronsieve.parser import CronFile, CronJob, CronEnv, parse_file

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class TestParser(unittest.TestCase):
    def _read(self, name: str) -> CronFile:
        return parse_file(os.path.join(FIXTURES, name))

    def test_valid_file_jobs_and_envs(self):
        cron = self._read("valid.crontab")
        self.assertEqual(len(cron.errors), 0, msg=cron.errors)
        self.assertGreaterEqual(len(cron.jobs), 4)
        self.assertGreaterEqual(len(cron.envs), 2)
        env_names = {e.name for e in cron.envs}
        self.assertIn("SHELL", env_names)
        self.assertIn("PATH", env_names)

    def test_macro_expansion(self):
        cron = self._read("valid.crontab")
        hourly = [j for j in cron.jobs if j.command.endswith("hourly_check.sh")]
        self.assertTrue(hourly, "nessun job hourly_check.sh trovato")
        job = hourly[0]
        self.assertEqual(job.minute, "0")
        self.assertEqual(job.hour, "*")
        self.assertEqual(job.dom, "*")
        self.assertEqual(job.month, "*")
        self.assertEqual(job.dow, "*")

    def test_comments_and_blank_lines_skipped(self):
        cron = self._read("valid.crontab")
        # Nessun job dovrebbe avere commento o riga vuota come comando
        for job in cron.jobs:
            self.assertNotEqual(job.command.strip(), "")
            self.assertFalse(job.command.strip().startswith("#"))

    def test_line_numbers_preserved(self):
        cron = self._read("valid.crontab")
        for job in cron.jobs:
            self.assertIsInstance(job.line_no, int)
            self.assertGreater(job.line_no, 0)

    def test_malformed_line_recorded_as_error(self):
        cron = self._read("invalid.crontab")
        self.assertGreater(len(cron.errors), 0, "ci si aspettavano errori di sintassi")
        for err in cron.errors:
            self.assertIn("riga", err)

    def test_edge_cases_parse_without_errors(self):
        cron = self._read("edge_cases.crontab")
        self.assertEqual(len(cron.errors), 0, msg=cron.errors)
        self.assertGreater(len(cron.jobs), 0)


if __name__ == "__main__":
    unittest.main()
