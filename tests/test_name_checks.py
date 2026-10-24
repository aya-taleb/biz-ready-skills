import json
import os
import subprocess
import sys
import tempfile
import unittest

from _load import ROOT, load_tool

nc = load_tool("brand", "name_checks")
TOOL = os.path.join(ROOT, "skills", "brand", "scripts", "name_checks.py")

GOOD = {"names": [{"name": "Fridgeplan", "checks": [
    {"type": "domain", "target": "fridgeplan.com", "result": "registered",
     "source": "https://rdap.verisign.com/com/v1/domain/fridgeplan.com", "date": "2026-10-23"},
    {"type": "trademark", "target": "FRIDGEPLAN", "result": "no live mark found",
     "source": "https://tmsearch.uspto.gov/", "date": "2026-10-23"},
    {"type": "handle", "target": "@fridgeplan", "result": "not checked"}]}]}


def _write(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class NameChecks(unittest.TestCase):
    def test_good(self):
        rows, problems = nc.review(GOOD)
        self.assertEqual(problems, [])
        self.assertEqual(rows[0]["checked"], 2)
        self.assertEqual(rows[0]["missing"], ["handle"])

    def test_available_is_refused(self):
        bad = json.loads(json.dumps(GOOD))
        bad["names"][0]["checks"][0]["result"] = "available"
        _, problems = nc.review(bad)
        self.assertTrue(any("available" in p for p in problems))

    def test_clear_is_refused_but_not_inside_words(self):
        bad = json.loads(json.dumps(GOOD))
        bad["names"][0]["checks"][1]["result"] = "Clear to use"
        self.assertTrue(nc.review(bad)[1])
        ok = json.loads(json.dumps(GOOD))
        ok["names"][0]["checks"][1]["result"] = "unclear, similar mark found"
        self.assertEqual(nc.review(ok)[1], [])

    def test_missing_source_and_date(self):
        bad = json.loads(json.dumps(GOOD))
        del bad["names"][0]["checks"][0]["source"]
        bad["names"][0]["checks"][1]["date"] = "today"
        _, problems = nc.review(bad)
        self.assertEqual(len(problems), 2)

    def test_screens(self):
        self.assertTrue(any("number" in s for s in nc.screens("Lunch4U")))
        self.assertTrue(any("hyphen" in s for s in nc.screens("Back-Street")))
        self.assertTrue(any("long" in s for s in nc.screens("Supercalifragilistic")))
        self.assertTrue(any("rival" in s for s in nc.screens("Mealimee", ["Mealime"])))
        self.assertFalse(any("rival" in s for s in nc.screens("Fridgeplan", ["Paprika"])))
        self.assertTrue(any("misheard" in s for s in nc.screens("Phresh")))

    def test_report_never_says_available(self):
        text = nc.report(nc.review(GOOD)[0])
        self.assertNotIn("available", text.lower())
        self.assertIn("trademark lawyer", text)

    def test_contrast(self):
        self.assertEqual(nc.contrast("#000000", "#FFFFFF"), 21.0)
        self.assertEqual(nc.contrast("#FFFFFF", "#FFFFFF"), 1.0)
        self.assertGreater(nc.contrast("#222222", "#F6F1E7"), 4.5)
        with self.assertRaises(nc.CheckError):
            nc.contrast("#12", "#FFFFFF")
        r = subprocess.run([sys.executable, "-I", TOOL, "--contrast", "#FFFFFF", "#D9483B"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn(":1", r.stdout)

    def test_bad_shape(self):
        with self.assertRaises(nc.CheckError):
            nc.review({"names": [{"checks": []}]})

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "n.json")
            _write(p, GOOD)
            r = subprocess.run([sys.executable, "-I", TOOL, p, "--rivals", "Mealime"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            bad = json.loads(json.dumps(GOOD))
            bad["names"][0]["checks"][0]["result"] = "available!"
            _write(p, bad)
            r = subprocess.run([sys.executable, "-I", TOOL, p], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
