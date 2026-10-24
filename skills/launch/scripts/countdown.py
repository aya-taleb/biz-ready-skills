#!/usr/bin/env python3
"""Dated launch countdown with a critical path. Standard library only, no network.

Reads a JSON list of tasks and a target launch date, works backward from the launch,
and prints when each task must start and finish, which tasks are on the critical path
(any slip moves the launch), and whether the date is realistic from today.

    python3 countdown.py founder/launch-tasks.json --launch 2026-12-01
    python3 countdown.py founder/launch-tasks.json --launch 2026-12-01 --today 2026-10-23 --out founder/countdown.md
    python3 countdown.py founder/launch-tasks.json --earliest          # earliest realistic launch date

Task file shape (a list, or {"tasks": [...]}):

    [{"id": "permit", "task": "Food permit approved", "owner": "Nora", "days": 30,
      "after": []},
     {"id": "menu", "task": "Final menu and costs", "owner": "Nora", "days": 5,
      "after": ["test"]}]

    id      short unique name
    task    what gets done
    owner   who does it (default "you")
    days    working time in calendar days (lead times included, e.g. a supplier's 14 days)
    after   ids that must finish first (default none)
    gate    optional true: the launch does not go ahead unless this passes (e.g. the demand test)

Every date comes from these inputs. Nothing is guessed. A loop in "after" is an error.
Exit code 0 when the plan fits, 1 when the launch date is not reachable, 2 on bad input.
"""

import argparse
import datetime
import json
import sys


class PlanError(Exception):
    pass


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        raise PlanError("no such file: %s" % path)
    except json.JSONDecodeError as exc:
        raise PlanError("%s is not valid JSON: %s" % (path, exc))
    tasks = data.get("tasks") if isinstance(data, dict) else data
    if not isinstance(tasks, list) or not tasks:
        raise PlanError("the file needs a list of tasks")
    return tasks


def _validate(tasks):
    by_id = {}
    for i, t in enumerate(tasks):
        if not isinstance(t, dict) or not t.get("id"):
            raise PlanError("task %d needs an 'id'" % i)
        if t["id"] in by_id:
            raise PlanError("duplicate id %r" % t["id"])
        try:
            days = int(t.get("days"))
        except (TypeError, ValueError):
            raise PlanError("task %r needs 'days' as a whole number" % t["id"])
        if days < 0:
            raise PlanError("task %r has negative days" % t["id"])
        by_id[t["id"]] = dict(t, days=days, after=list(t.get("after") or []),
                              owner=t.get("owner") or "you", task=t.get("task") or t["id"])
    for t in by_id.values():
        for dep in t["after"]:
            if dep not in by_id:
                raise PlanError("task %r waits for unknown id %r" % (t["id"], dep))
    return by_id


def _order(by_id):
    """Topological order; raises on a loop."""
    seen, temp, out = set(), set(), []

    def visit(i):
        if i in seen:
            return
        if i in temp:
            raise PlanError("loop in 'after' at %r" % i)
        temp.add(i)
        for dep in by_id[i]["after"]:
            visit(dep)
        temp.discard(i)
        seen.add(i)
        out.append(i)

    for i in by_id:
        visit(i)
    return out


def schedule(tasks, launch, today):
    """Return dict with rows, critical ids, earliest launch, fits. Pure function."""
    by_id = _validate(tasks)
    order = _order(by_id)
    # forward pass: earliest finish from today
    ef = {}
    for i in order:
        start = max([ef[d] for d in by_id[i]["after"]] or [0])
        ef[i] = start + by_id[i]["days"]
    total = max(ef.values())
    earliest = today + datetime.timedelta(days=total)
    # backward pass: latest finish so the launch holds
    successors = {i: [] for i in by_id}
    for i, t in by_id.items():
        for d in t["after"]:
            successors[d].append(i)
    horizon = (launch - today).days if launch else total
    lf = {}
    for i in reversed(order):
        lf[i] = min([lf[s] - by_id[s]["days"] for s in successors[i]] or [horizon])
    rows = []
    for i in order:
        t = by_id[i]
        latest_start = lf[i] - t["days"]
        earliest_start = ef[i] - t["days"]
        slack = latest_start - earliest_start
        rows.append({
            "id": i, "task": t["task"], "owner": t["owner"], "days": t["days"],
            "after": t["after"], "gate": bool(t.get("gate")),
            "can_start": today + datetime.timedelta(days=earliest_start),
            "start_by": today + datetime.timedelta(days=latest_start),
            "finish_by": today + datetime.timedelta(days=lf[i]),
            "slack_days": slack, "late": latest_start < 0,
        })
    # the critical path is the longest chain: zero float against the earliest finish
    lf0 = {}
    for i in reversed(order):
        lf0[i] = min([lf0[s] - by_id[s]["days"] for s in successors[i]] or [total])
    critical = [i for i in order if lf0[i] == ef[i]]
    buffer_days = horizon - total
    rows.sort(key=lambda r: (r["can_start"], r["start_by"]))
    return {"rows": rows, "critical": critical, "earliest": earliest, "buffer_days": buffer_days,
            "launch": launch or earliest, "today": today,
            "fits": launch is None or earliest <= launch}


def _week(d, today):
    return 1 + (d - today).days // 7


def report(plan):
    today, launch = plan["today"], plan["launch"]
    L = ["# Launch countdown", ""]
    L.append("Today: %s. Launch: %s (%d days)." % (today, launch, (launch - today).days))
    L.append("Earliest realistic launch from these tasks: %s." % plan["earliest"])
    if not plan["fits"]:
        L.append("")
        L.append("**The launch date does not fit.** These tasks should already have started:")
        for r in plan["rows"]:
            if r["late"]:
                L.append("- %s (start by %s, %d days late)" % (r["task"], r["start_by"], -(r["start_by"] - today).days))
        L.append("Move the launch to %s or later, or cut the time on a critical task." % plan["earliest"])
    L += ["", "| week | can start | start by | finish by | task | owner | critical | gate |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in plan["rows"]:
        spare = "%d day%s spare" % (r["slack_days"], "" if r["slack_days"] == 1 else "s")
        L.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (
            max(1, _week(r["can_start"], today)), r["can_start"], r["start_by"], r["finish_by"], r["task"],
            r["owner"], "yes" if r["id"] in plan["critical"] and r["slack_days"] <= 0 else ("path, " + spare if r["id"] in plan["critical"] else spare),
            "go/no-go" if r["gate"] else ""))
    L.append("")
    names = ", ".join(r["task"] for r in plan["rows"] if r["id"] in plan["critical"])
    if plan["fits"] and plan["buffer_days"] == 0:
        L.append("Critical path (the longest chain): %s." % names)
        L.append("No spare days on the critical path: one slip moves the launch. Add a buffer week "
                 "or start the first critical task now.")
    elif plan["fits"]:
        L.append("Critical path (the longest chain): %s. It has %d spare days before the launch date; "
                 "a slip longer than that moves the launch." % (names, plan["buffer_days"]))
    else:
        L.append("Critical path (the longest chain): %s." % names)
    gates = [r["task"] for r in plan["rows"] if r["gate"]]
    if gates:
        L.append("Gates: the launch goes ahead only if these pass: %s." % ", ".join(gates))
    return "\n".join(L) + "\n"


def _date(s, name):
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        raise PlanError("%s must be YYYY-MM-DD, got %r" % (name, s))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dated launch countdown with a critical path.")
    ap.add_argument("tasks")
    ap.add_argument("--launch", help="target launch date YYYY-MM-DD")
    ap.add_argument("--today", help="YYYY-MM-DD, default today")
    ap.add_argument("--earliest", action="store_true", help="plan to the earliest realistic date")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        today = _date(a.today, "--today") if a.today else datetime.date.today()
        if not a.launch and not a.earliest:
            raise PlanError("give --launch YYYY-MM-DD or --earliest")
        launch = None if a.earliest else _date(a.launch, "--launch")
        if launch and launch < today:
            raise PlanError("the launch date is before today")
        plan = schedule(load(a.tasks), launch, today)
    except PlanError as exc:
        print("countdown: %s" % exc, file=sys.stderr)
        return 2
    if a.json:
        out = dict(plan)
        for k in ("earliest", "launch", "today"):
            out[k] = str(out[k])
        out["rows"] = [dict(r, can_start=str(r["can_start"]), start_by=str(r["start_by"]),
                            finish_by=str(r["finish_by"])) for r in plan["rows"]]
        print(json.dumps(out, indent=2))
    else:
        text = report(plan)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("wrote %s" % a.out)
        print(text)
    return 0 if plan["fits"] else 1


if __name__ == "__main__":
    sys.exit(main())
