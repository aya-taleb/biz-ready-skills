#!/usr/bin/env python3
"""Rank funding programs by fit and flag deadlines. Standard library only, no network.

Reads a JSON file of programs you found (with links) and the founder's answers, scores
each program on the checks you list, works out days left to each deadline, and flags
programs that are closed, closing soon, undated, unsourced or found too long ago.

    python3 fit.py founder/funding.json
    python3 fit.py founder/funding.json --today 2026-10-23 --out founder/funding-table.md

File shape:

    {"checked": "2026-10-23",
     "programs": [
       {"name": "NSF SBIR Phase I", "kind": "grant", "url": "https://seedfund.nsf.gov/",
        "amount": "up to $305,000", "equity": "none",
        "deadline": "2026-12-01",          # or "rolling", "not listed", "closed"
        "found": "2026-10-23",             # the day you read the page
        "checks": [
          {"need": "US for-profit, under 500 staff", "meets": "yes"},
          {"need": "deep tech R&D, not a plain app", "meets": "unsure"},
          {"need": "a Project Pitch accepted first", "meets": "no"}]}]}

    kind     grant, accelerator, angel, fund, loan, competition, other
    meets    yes, no or unsure. Any "no" on a check marked "must": true makes it not eligible.

Fit score: yes = 2, unsure = 1, no = 0, out of 2 per check, shown as 0 to 100.
Nothing is looked up. The tool only does arithmetic on what you wrote, so every program
needs a url, and every amount and deadline comes from that page.
Exit code 0 when no problems, 1 when a program has a problem flag, 2 on bad input.
"""

import argparse
import datetime
import json
import sys

POINTS = {"yes": 2, "unsure": 1, "no": 0}
SOON_DAYS = 21
STALE_DAYS = 30


class FitError(Exception):
    pass


def _date(value, field, name):
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        raise FitError("%s: %s must be YYYY-MM-DD, got %r" % (name, field, value))


def rank(data, today):
    """Return a list of rows sorted best first, plus overall problems. Pure function."""
    if not isinstance(data, dict) or not isinstance(data.get("programs"), list):
        raise FitError("the file needs a 'programs' list")
    rows = []
    for i, p in enumerate(data["programs"]):
        name = p.get("name") or "program %d" % (i + 1)
        flags = []
        url = str(p.get("url") or "")
        if not url.startswith(("http://", "https://")):
            flags.append("no link: find the program's own page or drop it")
        checks = p.get("checks") or []
        if not checks:
            flags.append("no eligibility checks written")
        got = 0
        blocked = False
        for c in checks:
            meets = str(c.get("meets", "")).lower()
            if meets not in POINTS:
                raise FitError("%s: check %r needs meets = yes, no or unsure" % (name, c.get("need")))
            got += POINTS[meets]
            if meets == "no" and c.get("must"):
                blocked = True
        score = round(100.0 * got / (2 * len(checks))) if checks else 0
        deadline = str(p.get("deadline") or "not listed").strip().lower()
        days_left = None
        status = deadline
        if deadline[:4].isdigit():
            d = _date(deadline[:10], "deadline", name)
            days_left = (d - today).days
            if days_left < 0:
                status = "closed %s" % d
                flags.append("deadline passed: look for the next round")
            elif days_left <= SOON_DAYS:
                status = "%s (%d days left)" % (d, days_left)
                flags.append("closes in %d days" % days_left)
            else:
                status = "%s (%d days left)" % (d, days_left)
        elif deadline in ("rolling", "closed"):
            pass
        else:
            status = "not listed"
            flags.append("deadline not listed: check the page or ask the program")
        found = p.get("found") or data.get("checked")
        if not found:
            flags.append("no date for when this was found")
        else:
            age = (today - _date(found, "found", name)).days
            if age > STALE_DAYS:
                flags.append("found %d days ago: check the page again" % age)
        rows.append({
            "name": name, "kind": p.get("kind", "other"), "url": url,
            "amount": p.get("amount") or "not listed", "equity": p.get("equity") or "not listed",
            "deadline": status, "days_left": days_left, "fit": score,
            "eligible": "no" if blocked else ("check" if any(str(c.get("meets")).lower() == "unsure" for c in checks) else "yes"),
            "flags": flags, "closed": status.startswith("closed"),
        })
    rows.sort(key=lambda r: (r["eligible"] == "no", r["closed"], -r["fit"],
                             r["days_left"] if r["days_left"] is not None else 10 ** 6))
    return rows


def report(rows, today):
    L = ["Checked: %s" % today, "",
         "| rank | program | kind | amount | equity | deadline | fit | eligible | source |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, r in enumerate(rows, 1):
        L.append("| %d | %s | %s | %s | %s | %s | %d | %s | %s |" % (
            n, r["name"], r["kind"], r["amount"], r["equity"], r["deadline"], r["fit"], r["eligible"], r["url"] or "not found"))
    flagged = [r for r in rows if r["flags"]]
    if flagged:
        L += ["", "Flags:"]
        for r in flagged:
            L.append("- %s: %s" % (r["name"], "; ".join(r["flags"])))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rank funding programs by fit and flag deadlines.")
    ap.add_argument("path")
    ap.add_argument("--today", help="YYYY-MM-DD, default today")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        today = _date(a.today, "--today", "args") if a.today else datetime.date.today()
        with open(a.path, encoding="utf-8") as fh:
            data = json.load(fh)
        rows = rank(data, today)
    except (OSError, ValueError, FitError) as exc:
        print("fit: %s" % exc, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(rows, indent=2))
    else:
        text = report(rows, today)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("wrote %s" % a.out)
        print(text)
    hard = [r for r in rows if any(f.startswith(("no link", "deadline passed", "deadline not listed", "no date", "found")) for f in r["flags"])]
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
