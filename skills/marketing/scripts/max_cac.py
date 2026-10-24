#!/usr/bin/env python3
"""The most you can pay to get one customer. Standard library only, no network.

A customer is worth what they leave you after their own costs, over the time they stay.
Spend more than that to win them and every sale loses money. This tool does the math
from your inputs and shows each step, so nothing is a black box.

    python3 max_cac.py --price 14 --unit-cost 6.5 --per-month 8 --months 4
    python3 max_cac.py --numbers founder/numbers.json --per-month 8 --months 4
    python3 max_cac.py --price 7.99 --unit-cost 1.80 --per-month 1 --churn 0.12 --payback 6

Inputs:
  --price        price of one unit (a meal, a subscriber-month, a job)
  --unit-cost    direct cost of one unit (food, fees, AI, delivery); or --numbers to read
                 price and the sum of "variable" costs from Jake Schincariol's founder-cfo
                 numbers.json
  --per-month    units one customer buys a month (1 for a subscription)
  --months       how many months a customer stays; or --churn (share who leave each
                 month, 0 to 1), which gives months = 1 / churn
  --share        share of a customer's value you are willing to spend to win them
                 (default 0.33: keep two thirds to pay fixed costs and profit)
  --payback      months within which ad spend must be earned back (optional)

Prints: contribution per unit, value per customer, the max you can pay, a safer target,
and the max if it must pay back within --payback months.
Exit code 0, or 2 on bad input.
"""

import argparse
import json
import sys


class CacError(Exception):
    pass


def compute(price, unit_cost, per_month, months, share=0.33, payback=None):
    """Return a dict of every number with the steps. Pure function."""
    for name, v in (("price", price), ("unit cost", unit_cost), ("per month", per_month), ("months", months)):
        if v is None or v < 0:
            raise CacError("%s must be a number 0 or more" % name)
    if not 0 < share <= 1:
        raise CacError("share must be between 0 and 1")
    contribution = price - unit_cost
    monthly = contribution * per_month
    value = monthly * months
    out = {
        "contribution": round(contribution, 2),
        "monthly_contribution": round(monthly, 2),
        "months": round(months, 2),
        "customer_value": round(value, 2),
        "max_cac": round(max(value, 0), 2),
        "target_cac": round(max(value * share, 0), 2),
        "share": share,
        "payback_cac": None,
        "warnings": [],
    }
    if contribution <= 0:
        out["warnings"].append("each unit loses money before marketing: fix price or cost first")
    if payback is not None:
        out["payback_cac"] = round(max(monthly * min(payback, months), 0), 2)
    if months < 1:
        out["warnings"].append("customers stay under a month: repeat buying is the first problem")
    return out


def from_numbers(path):
    try:
        with open(path, encoding="utf-8") as fh:
            spec = json.load(fh)
    except (OSError, ValueError) as exc:
        raise CacError("cannot read %s: %s" % (path, exc))
    try:
        price = float(spec["price"])
        cost = sum(float(i["cost"]) for i in spec.get("variable", []))
    except (KeyError, TypeError, ValueError):
        raise CacError("%s needs 'price' and 'variable' [{label, cost}]" % path)
    return price, cost, spec.get("unit", "unit")


def report(r, price, unit_cost, per_month, unit="unit"):
    L = ["Contribution per %s: $%.2f price - $%.2f direct cost = $%.2f" % (unit, price, unit_cost, r["contribution"]),
         "Per customer per month: $%.2f x %g = $%.2f" % (r["contribution"], per_month, r["monthly_contribution"]),
         "Customer value: $%.2f x %g months = $%.2f" % (r["monthly_contribution"], r["months"], r["customer_value"]),
         "Most you can pay to win a customer (break-even on them): $%.2f" % r["max_cac"],
         "Safer target (%d%% of value, the rest pays fixed costs and profit): $%.2f" % (round(r["share"] * 100), r["target_cac"])]
    if r["payback_cac"] is not None:
        L.append("If ad spend must pay back within the payback window: $%.2f" % r["payback_cac"])
    for w in r["warnings"]:
        L.append("Warning: " + w)
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="The most you can pay to get one customer.")
    ap.add_argument("--price", type=float)
    ap.add_argument("--unit-cost", type=float)
    ap.add_argument("--numbers")
    ap.add_argument("--per-month", type=float, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--months", type=float)
    g.add_argument("--churn", type=float)
    ap.add_argument("--share", type=float, default=0.33)
    ap.add_argument("--payback", type=float)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        unit = "unit"
        if a.numbers:
            price, cost, unit = from_numbers(a.numbers)
        else:
            if a.price is None or a.unit_cost is None:
                raise CacError("give --price and --unit-cost, or --numbers")
            price, cost = a.price, a.unit_cost
        if a.churn is not None:
            if not 0 < a.churn <= 1:
                raise CacError("churn must be between 0 and 1, e.g. 0.12 for 12% a month")
            months = 1.0 / a.churn
        else:
            months = a.months
        r = compute(price, cost, a.per_month, months, a.share, a.payback)
    except CacError as exc:
        print("max_cac: %s" % exc, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(report(r, price, cost, a.per_month, unit), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
