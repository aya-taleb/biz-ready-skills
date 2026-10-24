#!/usr/bin/env python3
"""Write the real costs from ops into the CFO's numbers file. Standard library only.

Jake Schincariol's founder-cfo reads founder/numbers.json with three cost lists:
variable (per unit), fixed_monthly and startup, each [{label, cost}]. This tool merges
the costs you found in ops into that file, keeps a dated backup of the old one, writes
each cost's source into founder/cfo-sources.md, and prints what changed.

    python3 costs_to_cfo.py founder/ops-costs.json --numbers founder/numbers.json
    python3 costs_to_cfo.py founder/ops-costs.json --numbers founder/numbers.json --dry-run

ops-costs.json shape:

    {"costs": [
      {"list": "variable", "label": "Container and lid", "cost": 0.42,
       "source": "https://supplier.example.com/item/123", "date": "2026-10-23"},
      {"list": "fixed_monthly", "label": "Commissary kitchen", "cost": 1200,
       "source": "quote from the kitchen, 2026-10-20", "date": "2026-10-20"},
      {"list": "startup", "label": "Food business permit", "cost": null,
       "source": "to confirm with the county"}]}

    list    variable, fixed_monthly or startup
    cost    a number, or null when unknown (kept out of numbers.json and listed as a gap,
            so the CFO tool never runs on a guess)
    source  a URL, or the quote or invoice it came from. Required.

A label that already exists in that list is replaced (same label, new cost), so you can
rerun it. Nothing is deleted. If numbers.json does not exist, a new one is started and
the fields only the founder knows (price, volume) are left for founder-cfo to ask.
Exit code 0, 1 if any cost is unknown (gaps listed), 2 on bad input.
"""

import argparse
import datetime
import json
import os
import shutil
import sys

LISTS = ("variable", "fixed_monthly", "startup")


class CostError(Exception):
    pass


def merge(numbers, costs):
    """Return (new_numbers, changes, gaps, sources). Pure function; inputs are not changed."""
    out = json.loads(json.dumps(numbers or {}))
    changes, gaps, sources = [], [], []
    for i, c in enumerate(costs):
        lst = c.get("list")
        if lst not in LISTS:
            raise CostError("cost %d: list must be one of %s" % (i, ", ".join(LISTS)))
        label = (c.get("label") or "").strip()
        if not label:
            raise CostError("cost %d needs a label" % i)
        if not str(c.get("source") or "").strip():
            raise CostError("%s needs a source (a URL, a quote or an invoice)" % label)
        value = c.get("cost")
        if value is None:
            gaps.append("%s (%s): %s" % (label, lst, c["source"]))
            continue
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise CostError("%s: cost must be a number or null" % label)
        if value < 0:
            raise CostError("%s: cost is negative" % label)
        items = out.setdefault(lst, [])
        for it in items:
            if it.get("label") == label:
                if float(it.get("cost", 0)) != value:
                    changes.append("%s %s: %s -> %s" % (lst, label, it.get("cost"), value))
                it["cost"] = value
                break
        else:
            items.append({"label": label, "cost": value})
            changes.append("%s %s: added %s" % (lst, label, value))
        sources.append("- %s (%s): %s, %s. Source: %s" % (
            label, lst, value, c.get("date") or "undated", c["source"]))
    return out, changes, gaps, sources


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge ops costs into founder/numbers.json.")
    ap.add_argument("costs")
    ap.add_argument("--numbers", default="founder/numbers.json")
    ap.add_argument("--sources", help="default: cfo-sources.md next to numbers.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.costs, encoding="utf-8") as fh:
            costs = json.load(fh).get("costs")
        if not isinstance(costs, list):
            raise CostError("%s needs a 'costs' list" % a.costs)
        numbers = None
        if os.path.exists(a.numbers):
            with open(a.numbers, encoding="utf-8") as fh:
                numbers = json.load(fh)
        new, changes, gaps, sources = merge(numbers, costs)
    except (OSError, ValueError, AttributeError, CostError) as exc:
        print("costs_to_cfo: %s" % exc, file=sys.stderr)
        return 2
    print("Changes to %s:" % a.numbers)
    for c in changes or ["none"]:
        print("  " + c)
    if gaps:
        print("Unknown costs (not written; get a quote, then rerun):")
        for g in gaps:
            print("  " + g)
    if numbers is None:
        print("Started a new numbers file. founder-cfo will ask for price, unit and volume.")
    if a.dry_run:
        return 1 if gaps else 0
    if numbers is not None:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = "%s.bak-%s" % (a.numbers, stamp)
        shutil.copyfile(a.numbers, backup)
        print("Backup: %s" % backup)
    os.makedirs(os.path.dirname(os.path.abspath(a.numbers)), exist_ok=True)
    with open(a.numbers, "w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=2)
        fh.write("\n")
    src = a.sources or os.path.join(os.path.dirname(os.path.abspath(a.numbers)), "cfo-sources.md")
    with open(src, "a", encoding="utf-8") as fh:
        fh.write("\n## From ops, %s\n\n" % datetime.date.today().isoformat())
        fh.write("\n".join(sources) + "\n")
        for g in gaps:
            fh.write("- GAP %s\n" % g)
    print("Wrote %s and %s" % (a.numbers, src))
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
