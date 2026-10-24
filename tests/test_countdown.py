import datetime
import json
import os
import subprocess
import sys
import tempfile
import unittest

from _load import load_tool

cd = load_tool("launch", "countdown")
D = datetime.date

TASKS = [
    {"id": "test", "task": "Demand test", "days": 14, "gate": True},
    {"id": "permit", "task": "Permit", "days": 30},
    {"id": "menu", "task": "Menu", "days": 5, "after": ["test"]},
    {"id": "soft", "task": "Soft open", "days": 2, "after": ["permit", "menu"]},
]


class Countdown(unittest.TestCase):
    def test_earliest_is_longest_chain(self):
        plan = cd.schedule(TASKS, None, D(2026, 11, 1))
        self.assertEqual(plan["earliest"], D(2026, 12, 3))  # permit 30 + soft 2
        self.assertTrue(plan["fits"])
        self.assertEqual(sorted(plan["critical"]), ["permit", "soft"])

    def test_launch_with_room(self):
        plan = cd.schedule(TASKS, D(2026, 12, 13), D(2026, 11, 1))
        self.assertTrue(plan["fits"])
        self.assertEqual(sorted(plan["critical"]), ["permit", "soft"])
        self.assertEqual(plan["buffer_days"], 10)
        self.assertIn("10 spare days before the launch date", cd.report(plan))
        permit = [r for r in plan["rows"] if r["id"] == "permit"][0]
        self.assertEqual(permit["start_by"], D(2026, 11, 11))
        self.assertEqual(permit["finish_by"], D(2026, 12, 11))

    def test_launch_too_soon(self):
        plan = cd.schedule(TASKS, D(2026, 11, 20), D(2026, 11, 1))
        self.assertFalse(plan["fits"])
        late = [r["id"] for r in plan["rows"] if r["late"]]
        self.assertIn("permit", late)
        self.assertIn("does not fit", cd.report(plan))

    def test_gate_shown(self):
        text = cd.report(cd.schedule(TASKS, None, D(2026, 11, 1)))
        self.assertIn("Gates: the launch goes ahead only if these pass: Demand test.", text)

    def test_no_buffer_warning_and_spare_wording(self):
        text = cd.report(cd.schedule(TASKS, None, D(2026, 11, 1)))
        self.assertIn("No spare days on the critical path", text)
        text = cd.report(cd.schedule(TASKS, D(2026, 12, 13), D(2026, 11, 1)))
        self.assertNotIn("No spare days", text)
        self.assertIn("10 days spare", text)
        one = [{"id": "a", "days": 3}, {"id": "b", "days": 2}]
        self.assertIn("1 day spare", cd.report(cd.schedule(one, None, D(2026, 1, 1))))

    def test_loop_is_error(self):
        bad = [{"id": "a", "days": 1, "after": ["b"]}, {"id": "b", "days": 1, "after": ["a"]}]
        with self.assertRaises(cd.PlanError):
            cd.schedule(bad, None, D(2026, 1, 1))

    def test_unknown_dependency(self):
        with self.assertRaises(cd.PlanError):
            cd.schedule([{"id": "a", "days": 1, "after": ["zzz"]}], None, D(2026, 1, 1))

    def test_bad_days(self):
        for days in (None, "two", -1):
            with self.assertRaises(cd.PlanError):
                cd.schedule([{"id": "a", "days": days}], None, D(2026, 1, 1))

    def test_duplicate_id(self):
        with self.assertRaises(cd.PlanError):
            cd.schedule([{"id": "a", "days": 1}, {"id": "a", "days": 2}], None, D(2026, 1, 1))

    def test_cli(self):
        path = os.path.join(os.path.dirname(__file__), "..", "skills", "launch", "scripts", "countdown.py")
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "t.json")
            with open(f, "w", encoding="utf-8") as fh:
                json.dump({"tasks": TASKS}, fh)
            run = lambda *a: subprocess.run([sys.executable, "-I", path, f] + list(a), capture_output=True, text=True)
            self.assertEqual(run("--launch", "2026-12-31", "--today", "2026-11-01").returncode, 0)
            self.assertEqual(run("--launch", "2026-11-10", "--today", "2026-11-01").returncode, 1)
            self.assertEqual(run("--today", "2026-11-01").returncode, 2)
            self.assertEqual(run("--launch", "2026-10-01", "--today", "2026-11-01").returncode, 2)
            out = os.path.join(tmp, "c.md")
            r = run("--earliest", "--today", "2026-11-01", "--out", out)
            self.assertEqual(r.returncode, 0)
            self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
