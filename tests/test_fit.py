import datetime
import filecmp
import json
import os
import subprocess
import sys
import tempfile
import unittest

from _load import ROOT, load_tool

fit = load_tool("funding", "fit")
T = datetime.date(2026, 10, 23)


def prog(**kw):
    base = {"name": "P", "kind": "grant", "url": "https://p.example.org", "amount": "$10,000",
            "deadline": "2026-12-31", "found": "2026-10-23",
            "checks": [{"need": "a", "meets": "yes"}, {"need": "b", "meets": "unsure"}]}
    base.update(kw)
    return base


def _write(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class Fit(unittest.TestCase):
    def test_score_and_days(self):
        r = fit.rank({"programs": [prog()]}, T)[0]
        self.assertEqual(r["fit"], 75)
        self.assertEqual(r["days_left"], 69)
        self.assertEqual(r["eligible"], "check")
        self.assertEqual(r["flags"], [])

    def test_must_no_blocks(self):
        p = prog(checks=[{"need": "US company", "meets": "no", "must": True}, {"need": "x", "meets": "yes"}])
        r = fit.rank({"programs": [p]}, T)[0]
        self.assertEqual(r["eligible"], "no")

    def test_order_best_first_and_blocked_last(self):
        a = prog(name="A", checks=[{"need": "x", "meets": "yes"}])
        b = prog(name="B", checks=[{"need": "x", "meets": "unsure"}])
        c = prog(name="C", checks=[{"need": "x", "meets": "no", "must": True}])
        names = [r["name"] for r in fit.rank({"programs": [c, b, a]}, T)]
        self.assertEqual(names, ["A", "B", "C"])

    def test_closed_soon_and_undated(self):
        rows = fit.rank({"programs": [prog(name="old", deadline="2026-10-01"),
                                      prog(name="soon", deadline="2026-11-02"),
                                      prog(name="nd", deadline="")]}, T)
        by = {r["name"]: r for r in rows}
        self.assertTrue(by["old"]["closed"])
        self.assertIn("deadline passed", by["old"]["flags"][0])
        self.assertIn("closes in 10 days", by["soon"]["flags"])
        self.assertEqual(by["nd"]["deadline"], "not listed")
        self.assertEqual(rows[-1]["name"], "old")

    def test_rolling_ok(self):
        r = fit.rank({"programs": [prog(deadline="Rolling")]}, T)[0]
        self.assertEqual(r["flags"], [])
        self.assertEqual(r["deadline"], "rolling")

    def test_no_link_and_stale(self):
        r = fit.rank({"programs": [prog(url="", found="2026-08-01")]}, T)[0]
        self.assertTrue(any(f.startswith("no link") for f in r["flags"]))
        self.assertTrue(any("check the page again" in f for f in r["flags"]))

    def test_found_falls_back_to_checked(self):
        p = prog()
        del p["found"]
        self.assertEqual(fit.rank({"checked": "2026-10-20", "programs": [p]}, T)[0]["flags"], [])

    def test_bad_meets(self):
        with self.assertRaises(fit.FitError):
            fit.rank({"programs": [prog(checks=[{"need": "x", "meets": "maybe"}])]}, T)

    def test_bad_shape(self):
        with self.assertRaises(fit.FitError):
            fit.rank([], T)

    def test_report_has_checked_and_source(self):
        text = fit.report(fit.rank({"programs": [prog()]}, T), T)
        self.assertIn("Checked: 2026-10-23", text)
        self.assertIn("https://p.example.org", text)

    def test_cli(self):
        path = os.path.join(ROOT, "skills", "funding", "scripts", "fit.py")
        with tempfile.TemporaryDirectory() as tmp:
            good = os.path.join(tmp, "g.json")
            bad = os.path.join(tmp, "b.json")
            _write(good, {"programs": [prog()]})
            _write(bad, {"programs": [prog(url="")]})
            run = lambda p: subprocess.run([sys.executable, "-I", path, p, "--today", "2026-10-23"], capture_output=True, text=True)
            self.assertEqual(run(good).returncode, 0)
            self.assertEqual(run(bad).returncode, 1)
            self.assertEqual(run(os.path.join(tmp, "none.json")).returncode, 2)

    def test_source_check_copy_matches_home(self):
        home = os.path.join(ROOT, "skills", "competitors", "scripts", "source_check.py")
        copy = os.path.join(ROOT, "skills", "funding", "scripts", "source_check.py")
        self.assertTrue(filecmp.cmp(home, copy, shallow=False),
                        "funding/scripts/source_check.py must be an exact copy of the competitors one")


if __name__ == "__main__":
    unittest.main()
