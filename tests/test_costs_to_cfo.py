import glob
import json
import os
import subprocess
import sys
import tempfile
import unittest

from _load import ROOT, load_tool

cc = load_tool("ops", "costs_to_cfo")
TOOL = os.path.join(ROOT, "skills", "ops", "scripts", "costs_to_cfo.py")

NUMBERS = {"unit": "meal", "price": 14, "variable": [{"label": "Food", "cost": 4.0}],
           "fixed_monthly": [], "startup": []}
COSTS = [
    {"list": "variable", "label": "Container", "cost": 0.42, "source": "https://s.example.com/1", "date": "2026-10-23"},
    {"list": "variable", "label": "Food", "cost": 4.6, "source": "supplier quote 2026-10-20"},
    {"list": "fixed_monthly", "label": "Kitchen", "cost": 1200, "source": "quote"},
    {"list": "startup", "label": "Permit", "cost": None, "source": "to confirm with the county"},
]


def _write(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class CostsToCfo(unittest.TestCase):
    def test_merge(self):
        new, changes, gaps, sources = cc.merge(NUMBERS, COSTS)
        self.assertEqual(new["price"], 14)
        self.assertEqual([i["cost"] for i in new["variable"]], [4.6, 0.42])
        self.assertEqual(new["fixed_monthly"], [{"label": "Kitchen", "cost": 1200.0}])
        self.assertEqual(new["startup"], [])
        self.assertEqual(len(gaps), 1)
        self.assertIn("Food: 4.0 -> 4.6", " ".join(changes))
        self.assertEqual(len(sources), 3)
        self.assertEqual(NUMBERS["variable"][0]["cost"], 4.0, "input must not change")

    def test_new_file(self):
        new, _, _, _ = cc.merge(None, COSTS[:1])
        self.assertEqual(new, {"variable": [{"label": "Container", "cost": 0.42}]})

    def test_errors(self):
        for bad in ({"list": "monthly", "label": "x", "cost": 1, "source": "s"},
                    {"list": "variable", "label": "", "cost": 1, "source": "s"},
                    {"list": "variable", "label": "x", "cost": 1, "source": ""},
                    {"list": "variable", "label": "x", "cost": "lots", "source": "s"},
                    {"list": "variable", "label": "x", "cost": -1, "source": "s"}):
            with self.assertRaises(cc.CostError):
                cc.merge(NUMBERS, [bad])

    def test_cli_backup_sources_and_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            nums = os.path.join(tmp, "founder", "numbers.json")
            os.makedirs(os.path.dirname(nums))
            _write(nums, NUMBERS)
            costs = os.path.join(tmp, "ops-costs.json")
            _write(costs, {"costs": COSTS})
            r = subprocess.run([sys.executable, "-I", TOOL, costs, "--numbers", nums], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stderr)
            self.assertEqual(len(glob.glob(nums + ".bak-*")), 1)
            with open(nums, encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["fixed_monthly"][0]["cost"], 1200.0)
            with open(os.path.join(tmp, "founder", "cfo-sources.md"), encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn("GAP Permit", text)
            self.assertIn("https://s.example.com/1", text)
            _write(costs, {"costs": COSTS[:1]})
            r = subprocess.run([sys.executable, "-I", TOOL, costs, "--numbers", nums, "--dry-run"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            _write(costs, {"nope": []})
            r = subprocess.run([sys.executable, "-I", TOOL, costs, "--numbers", nums], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
