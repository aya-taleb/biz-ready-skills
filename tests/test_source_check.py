import datetime
import os
import subprocess
import sys
import tempfile
import unittest

from _load import load_tool

sc = load_tool("competitors", "source_check")

GOOD = """# Competitors: Test

Scope: lunch for office workers in Bellevue.
Checked: 2026-10-20

## Summary

- The gap: lunch under $15 that arrives warm, about 40% cheaper.

## Direct

| name | price | source |
| --- | --- | --- |
| Alpha | $13 a bowl | https://alpha.example.com/menu |
| Beta | not listed | https://beta.example.com |

## Not found

- Gamma price: $?? looked at search, not listed.
"""


class SourceCheck(unittest.TestCase):
    def test_clean_file(self):
        self.assertEqual(sc.check(GOOD), [])

    def test_missing_check_date(self):
        probs = sc.check(GOOD.replace("Checked: 2026-10-20", ""))
        self.assertIn("no-check-date", [p["kind"] for p in probs])

    def test_bold_check_date_is_read(self):
        self.assertEqual(sc.check(GOOD.replace("Checked: 2026-10-20", "**Checked:** 2026-10-20")), [])

    def test_row_without_link(self):
        text = GOOD.replace("| Alpha | $13 a bowl | https://alpha.example.com/menu |", "| Alpha | $13 a bowl | their site |")
        kinds = [p["kind"] for p in sc.check(text)]
        self.assertEqual(kinds, ["row-without-link"])

    def test_not_listed_row_is_exempt(self):
        text = GOOD.replace("https://beta.example.com", "no site")
        self.assertEqual(sc.check(text), [])

    def test_price_in_body_needs_link(self):
        text = GOOD + "\n## Notes\n\nMost rivals charge $16 a meal.\n"
        kinds = [p["kind"] for p in sc.check(text)]
        self.assertEqual(kinds, ["number-without-link"])

    def test_percent_needs_link_outside_summary(self):
        text = GOOD + "\n## Notes\n\nAbout 30% of reviews mention cold food.\n"
        self.assertEqual(len(sc.check(text)), 1)

    def test_placeholder_is_allowed(self):
        text = GOOD + "\n## Notes\n\nYour cost per meal: {{your number}} or $5 est.\n"
        self.assertEqual(sc.check(text), [])

    def test_derived_heading_skipped(self):
        text = GOOD + "\n## Recap\n\nWe are 20% cheaper.\n"
        self.assertEqual(len(sc.check(text)), 1)
        self.assertEqual(sc.check(text, derived=("recap",)), [])

    def test_scope_line_skipped(self):
        text = GOOD.replace("Scope: lunch for office workers in Bellevue.", "Scope: lunch at about $14 a meal in Bellevue.")
        self.assertEqual(sc.check(text), [])

    def test_code_fence_ignored(self):
        text = GOOD + "\n```\n| x | $5 | none |\n```\n"
        self.assertEqual(sc.check(text), [])

    def test_date_column(self):
        text = """Checked: 2026-10-20

| program | amount | deadline | source |
| --- | --- | --- | --- |
| A | $50,000 | 2026-12-01 | https://a.example.org |
| B | $10,000 | rolling | https://b.example.org |
| C | $5,000 | soon | https://c.example.org |
"""
        probs = sc.check(text, date_column="deadline")
        self.assertEqual([p["kind"] for p in probs], ["undated"])
        self.assertIn("soon", probs[0]["text"])

    def test_missing_date_column(self):
        probs = sc.check(GOOD, date_column="deadline")
        self.assertIn("no-date-column", [p["kind"] for p in probs])

    def test_stale(self):
        probs = sc.check(GOOD, today=datetime.date(2026, 12, 31), max_age_days=30)
        self.assertEqual([p["kind"] for p in probs], ["stale"])
        self.assertEqual(sc.check(GOOD, today=datetime.date(2026, 10, 25), max_age_days=30), [])

    def test_cli_exit_codes(self):
        path = os.path.join(os.path.dirname(__file__), "..", "skills", "competitors", "scripts", "source_check.py")
        with tempfile.TemporaryDirectory() as tmp:
            good = os.path.join(tmp, "good.md")
            bad = os.path.join(tmp, "bad.md")
            with open(good, "w", encoding="utf-8") as fh:
                fh.write(GOOD)
            with open(bad, "w", encoding="utf-8") as fh:
                fh.write("no date here\n\n| a | $5 |\n| --- | --- |\n| b | $6 |\n")
            run = lambda p: subprocess.run([sys.executable, "-I", path, p], capture_output=True, text=True)
            self.assertEqual(run(good).returncode, 0)
            self.assertEqual(run(bad).returncode, 1)
            self.assertEqual(run(os.path.join(tmp, "missing.md")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
