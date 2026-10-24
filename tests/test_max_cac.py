import json
import os
import subprocess
import sys
import tempfile
import unittest

from _load import ROOT, load_tool

mc = load_tool("marketing", "max_cac")
TOOL = os.path.join(ROOT, "skills", "marketing", "scripts", "max_cac.py")


class MaxCac(unittest.TestCase):
    def test_basic(self):
        r = mc.compute(14, 6.5, 8, 4)
        self.assertEqual(r["contribution"], 7.5)
        self.assertEqual(r["monthly_contribution"], 60.0)
        self.assertEqual(r["customer_value"], 240.0)
        self.assertEqual(r["max_cac"], 240.0)
        self.assertEqual(r["target_cac"], 79.2)
        self.assertEqual(r["warnings"], [])

    def test_payback_caps_at_months(self):
        self.assertEqual(mc.compute(10, 4, 1, 3, payback=6)["payback_cac"], 18.0)
        self.assertEqual(mc.compute(10, 4, 1, 12, payback=6)["payback_cac"], 36.0)

    def test_negative_contribution(self):
        r = mc.compute(5, 6, 4, 6)
        self.assertEqual(r["max_cac"], 0)
        self.assertTrue(r["warnings"])

    def test_short_stay_warning(self):
        self.assertTrue(any("under a month" in w for w in mc.compute(10, 2, 1, 0.5)["warnings"]))

    def test_bad_inputs(self):
        with self.assertRaises(mc.CacError):
            mc.compute(-1, 0, 1, 1)
        with self.assertRaises(mc.CacError):
            mc.compute(1, 0, 1, 1, share=0)

    def test_report_shows_math(self):
        r = mc.compute(14, 6.5, 8, 4)
        text = mc.report(r, 14, 6.5, 8, "meal")
        self.assertIn("$14.00 price - $6.50 direct cost = $7.50", text)
        self.assertIn("$60.00 x 4 months = $240.00", text)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-I", TOOL] + list(args), capture_output=True, text=True)

    def test_cli_churn_and_numbers(self):
        r = self.run_cli("--price", "8", "--unit-cost", "2", "--per-month", "1", "--churn", "0.25", "--json")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["customer_value"], 24.0)
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "numbers.json")
            with open(p, "w") as fh:
                json.dump({"unit": "cup", "price": 6.5, "variable": [{"label": "a", "cost": 1.0}, {"label": "b", "cost": 0.5}]}, fh)
            r = self.run_cli("--numbers", p, "--per-month", "10", "--months", "2", "--json")
            self.assertEqual(json.loads(r.stdout)["customer_value"], 100.0)

    def test_cli_errors(self):
        self.assertEqual(self.run_cli("--per-month", "1", "--months", "2").returncode, 2)
        self.assertEqual(self.run_cli("--price", "1", "--unit-cost", "0", "--per-month", "1", "--churn", "2").returncode, 2)


if __name__ == "__main__":
    unittest.main()
