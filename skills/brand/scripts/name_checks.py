#!/usr/bin/env python3
"""Keep name checks honest. Standard library only, no network.

You run the lookups (registry data for domains, the trademark office search, handles by
hand). This tool reads what you recorded, screens each name with a few quick local tests,
and prints a table where every result says what was checked, where and when. It never
prints "available": a domain with no record is "no record found", and trademark
clearance is always a lawyer's call.

    python3 name_checks.py founder/name-checks.json
    python3 name_checks.py founder/name-checks.json --rivals "Mealime,Paprika" --out founder/name-table.md
    python3 name_checks.py --contrast "#222222" "#F6F1E7"      # WCAG contrast of text on a background

File shape:

    {"names": [
      {"name": "Fridgeplan",
       "checks": [
         {"type": "domain", "target": "fridgeplan.com", "result": "registered",
          "source": "https://rdap.verisign.com/com/v1/domain/fridgeplan.com", "date": "2026-10-23"},
         {"type": "trademark", "target": "FRIDGEPLAN, class 9", "result": "no live mark found",
          "source": "https://tmsearch.uspto.gov/", "date": "2026-10-23"},
         {"type": "handle", "target": "instagram @fridgeplan", "result": "not checked"}]}]}

    type    domain, trademark, handle, business-name, other
    result  registered, no record found, live mark found, no live mark found, similar mark
            found, taken, not checked, or your own short words

Quick screens (local, rough): length, letters that are often misheard or misspelled,
numbers or hyphens, and closeness to rival names you pass with --rivals.
Exit code 0 when every result has a source and date (or is "not checked"), 1 otherwise,
2 on bad input.
"""

import argparse
import datetime
import difflib
import json
import re
import sys

BANNED_RESULT_WORDS = ("available", "clear", "free to use", "safe to use")
TRICKY = [("ph", "f"), ("c", "k"), ("ck", "k"), ("x", "ks"), ("ie", "y"), ("ei", "ie"),
          ("ou", "ow"), ("z", "s"), ("qu", "kw")]


class CheckError(Exception):
    pass


def screens(name, rivals=()):
    """Quick local screens. Returns a list of short notes. Pure function."""
    notes = []
    letters = re.sub(r"[^a-z0-9]", "", name.lower())
    if len(letters) > 12:
        notes.append("long (%d letters): harder to type and fit on a sign" % len(letters))
    if re.search(r"[0-9]", name):
        notes.append("has a number: people will ask 'the digit or the word?'")
    if "-" in name:
        notes.append("has a hyphen: often dropped when said out loud")
    hits = [a for a, _ in TRICKY if a in letters]
    if hits:
        notes.append("spelling could be misheard (%s)" % ", ".join(hits))
    if re.search(r"(.)\1\1", letters):
        notes.append("three repeated letters")
    for r in rivals:
        r2 = re.sub(r"[^a-z0-9]", "", r.lower())
        if not r2:
            continue
        ratio = difflib.SequenceMatcher(None, letters, r2).ratio()
        if ratio >= 0.7 or (len(r2) >= 4 and (r2 in letters or letters in r2)):
            notes.append("close to rival %r (%.0f%% similar)" % (r, ratio * 100))
    return notes


def contrast(fg, bg):
    """WCAG contrast ratio between two hex colors, e.g. contrast('#222222', '#F6F1E7')."""
    def lum(h):
        h = h.lstrip("#")
        if len(h) != 6 or not re.match(r"^[0-9a-fA-F]{6}$", h):
            raise CheckError("colors must be 6-digit hex like #1A2B3C, got %r" % h)
        out = []
        for i in (0, 2, 4):
            c = int(h[i:i + 2], 16) / 255.0
            out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return round((a + 0.05) / (b + 0.05), 2)


def review(data, rivals=()):
    """Return rows and problems. Pure function."""
    if not isinstance(data, dict) or not isinstance(data.get("names"), list):
        raise CheckError("the file needs a 'names' list")
    rows, problems = [], []
    for n in data["names"]:
        name = n.get("name")
        if not name:
            raise CheckError("every entry needs a 'name'")
        checks = n.get("checks") or []
        done = 0
        out = []
        for c in checks:
            result = str(c.get("result") or "not checked").strip()
            low = result.lower()
            for w in BANNED_RESULT_WORDS:
                if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                    problems.append("%s: result %r says %r. Write what the lookup showed, e.g. 'no record found'."
                                    % (name, result, w))
            if low != "not checked":
                done += 1
                if not str(c.get("source", "")).startswith(("http://", "https://")):
                    problems.append("%s: %s check has no source link" % (name, c.get("type", "?")))
                try:
                    datetime.date.fromisoformat(str(c.get("date")))
                except ValueError:
                    problems.append("%s: %s check has no date (YYYY-MM-DD)" % (name, c.get("type", "?")))
            out.append({"type": c.get("type", "other"), "target": c.get("target", ""), "result": result,
                        "source": c.get("source", ""), "date": c.get("date", "")})
        types = {c["type"] for c in out if c["result"].lower() != "not checked"}
        rows.append({"name": name, "screens": screens(name, rivals), "checks": out,
                     "checked": done, "missing": [t for t in ("domain", "trademark", "handle") if t not in types]})
    return rows, problems


def report(rows):
    L = ["| name | check | target | result | source | date |", "| --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        if not r["checks"]:
            L.append("| %s | none | | not checked | | |" % r["name"])
        for c in r["checks"]:
            L.append("| %s | %s | %s | %s | %s | %s |" % (r["name"], c["type"], c["target"], c["result"],
                                                       c["source"] or "", c["date"] or ""))
    L.append("")
    for r in rows:
        bits = []
        if r["screens"]:
            bits.append("screens: " + "; ".join(r["screens"]))
        if r["missing"]:
            bits.append("not yet checked: " + ", ".join(r["missing"]))
        if bits:
            L.append("- %s: %s" % (r["name"], ". ".join(bits)))
    L.append("")
    L.append("No record found is not the same as yours to use. Register what you choose, and have a "
             "trademark lawyer run a clearance search before you spend on the brand.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keep name checks honest.")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--rivals", default="", help="comma-separated rival names")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--contrast", nargs=2, metavar=("TEXT", "BACKGROUND"),
                    help="print the WCAG contrast ratio of two hex colors and exit")
    a = ap.parse_args(argv)
    if a.contrast:
        try:
            r = contrast(*a.contrast)
        except CheckError as exc:
            print("name_checks: %s" % exc, file=sys.stderr)
            return 2
        verdict = "passes AA for body text" if r >= 4.5 else ("large text only (AA 3:1)" if r >= 3 else "fails AA")
        print("%s on %s: %.2f:1, %s" % (a.contrast[0], a.contrast[1], r, verdict))
        return 0
    if not a.path:
        ap.error("give the name-checks file, or --contrast TEXT BACKGROUND")
    rivals = [r.strip() for r in a.rivals.split(",") if r.strip()]
    try:
        with open(a.path, encoding="utf-8") as fh:
            data = json.load(fh)
        rows, problems = review(data, rivals)
    except (OSError, ValueError, CheckError) as exc:
        print("name_checks: %s" % exc, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"rows": rows, "problems": problems}, indent=2))
    else:
        text = report(rows)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("wrote %s" % a.out)
        print(text, end="")
        if problems:
            print("\nProblems:")
            for p in problems:
                print("  - " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
