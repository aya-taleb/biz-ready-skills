---
name: launch
description: >-
  Your launch lead. Builds a dated launch plan that starts with the demand tests from the
  validate skill and their pass/fail lines, so nothing big is paid for until real buyers
  say yes. Then a countdown to launch day with owners, deadlines and the critical path
  (computed by a small tool), a launch-day run sheet, and the first 30 days of numbers to
  watch with the level that triggers a change. Works for local businesses (pop-up, soft
  open, permits) and online ones (waitlist, pre-sale, launch posts). Use it when someone
  says "how do I launch", "launch plan", "when can I open", "launch checklist", "go live",
  "soft open", "plan my launch date", "what do I do before opening day", or "we passed the
  test, now what". Not for the demand test design itself (that is validate) or a promo
  video (launch-video).
argument-hint: "[target launch date YYYY-MM-DD]"
---

# launch

> Based on founder-launch by Jake Schincariol (MIT). Changed by Aya Taleb: starts from the validate skill's tests and pass/fail lines, adds a go/no-go gate, a countdown tool with a critical path, and local and online paths.

Launching is a project with a date. This skill turns everything in `founder/` into a dated
plan, and it starts with proof: the cheapest test that shows real people will pay, run
before the big money goes out.

What the user typed after `/launch`: `$ARGUMENTS`

## Reads and writes

- Reads first: the business context (`founder/context.md`, else the active file under
  `~/.founder/businesses/`). Then the validate skill's files: `founder/validate.md`
  (the tests, the call), `founder/validate-plan.json` (the locked pass and fail lines) and
  `founder/validate-results.json` (the counts), then `founder/idea.md`, `founder/ops.md` (lead times, permits), `founder/numbers.json`
  and `founder/cfo.md` (break-even), `founder/marketing.md`, `founder/brand.md`,
  `founder/board.md` (conditions). Say which ones exist and which are missing.
- Writes: `founder/launch-tasks.json`, `founder/countdown.md` (from the tool) and
  `founder/launch.md`.
- Tool: `scripts/countdown.py` turns tasks with lead times into dates and a critical path.

## Step 1: the test comes first

Open `founder/validate.md`. It holds the riskiest assumption, one to three demand tests,
and a pass/fail line written before each test ran. Copy those into the top of the plan as
they are. Do not loosen a pass line after the fact; that line exists so the founder cannot
talk themselves into a launch.

If `founder/validate-plan.json` and `founder/validate-results.json` exist and the validate
skill is installed, let its tool read the result rather than reading it yourself:
`python3 <validate skill dir>/scripts/testplan.py read founder/validate-plan.json founder/validate-results.json`.
It also flags any line that moved after it was locked. If it says a line moved, treat the
result as soft and say so. "Unclear" or "too early" counts as not passed yet.

Then read where each test stands:

| status | what the plan does |
| --- | --- |
| unclear or too early | not passed yet: the test stays task 1 and a gate, with its end date |
| passed | note the result and the date; the countdown starts now |
| failed | stop here. Say so plainly, and send the founder to `/validate` for a pivot or stop call, or to `/offer` or `/founder-pricing` if the test points at price or offer. Do not build a countdown on a failed test |
| not run yet | the test is task 1 in the countdown and a gate: nothing that costs real money is scheduled before it finishes |
| no validate.md | ask once if they ran a test. If not, offer `/validate` first. If they want to go on, pick the cheapest test below, set a pass line as in "Setting the pass line" below, and mark it a gate |

The cheapest real test by business type:

| business | the test |
| --- | --- |
| local shop, café, food | a pop-up, a market stall or a pre-order list with a price and a date |
| online product or app | a landing page with the price and a pre-order or waitlist button |
| service or agency | three paid pilot clients at the planned price |
| subscription | a founding-member offer, paid up front |

### Setting the pass line

A pass line is a real number and a deadline, written before the test starts. Never leave it
as `{{N}}`: a blank line can't fail, so the test can't stop a bad launch.

If `founder/cfo.md` has a break-even, base the line on it: enough paid orders in the test
window to show the break-even pace is reachable. Show the sum in one line.

If there is no break-even, set the line from what the founder can tell you now, and show
the reasoning so they can change it before the test starts:

1. Ask for two things they know: the planned price, and how many customers a month would
   make them keep going (or how many they can serve). Ask once, in one message.
2. Pass line = paid commitments (pre-orders, deposits or paid pilots) at the planned price,
   from people who aren't friends or family, within 14 days. Count: about a quarter of the
   monthly number they gave, rounded, so it shows the first month is within reach.
3. If they can't give a monthly number, use these floors and say they are a starting line,
   not a fact: 20 paid pre-orders (local, food, subscription, product), 3 paid pilots
   (service or agency), 20 paid pre-orders or deposits from the landing page (online).
   Why: few enough to reach by hand in two weeks, too many to come from friends alone.
4. Add a fail line under it ("under 8 by day 14: stop and rethink the offer or price") and
   what "unclear" means (between the two: run one more week, then decide).

Write it like this in the plan:

> Pass: 20 paid pre-orders at $12 a lunch by Nov 20 (14 days). Fail: under 8.
> Why 20: no break-even yet; you said 80 regular customers a month would keep you going,
> and a quarter of that in two weeks shows the first month is reachable.

Keep `{{...}}` only for a number only the founder can give, such as a price they haven't
set: "20 paid pre-orders at {{your planned price}} by Nov 20". The count and the deadline
are always filled in. Suggest `/founder-cfo` to get a real break-even before the money
spend after the gate.

If the simulated buyer panel from `/founder-consumer` ran, compare the real result with its
buy rate. Trust real buyers over simulated ones when they disagree.

## Step 2: the countdown

Ask for the target date once. If there is none, plan to the earliest realistic date.

Write `founder/launch-tasks.json`: each task with an id, owner, days (including lead times
from `founder/ops.md` and supplier quotes), what it waits for, and `"gate": true` on the
demand test. The shape is in the tool's header. Cover:

- Legal and money: registration, bank account, insurance, permits from `founder/ops.md`.
- Build: fit-out or website, suppliers ordered by their lead times.
- Brand: sign, packaging, profiles from `founder/brand.md`.
- Marketing: the calendar in `founder/marketing.md`, starting launch minus 14 days.
- Team: hiring and training on the routines in `founder/ops.md`.
- A soft open (local) or a private beta (online) before the public launch.

Then run:

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/countdown.py" founder/launch-tasks.json --launch YYYY-MM-DD --out founder/countdown.md
```

It gives the start-by and finish-by date of every task, the critical path, and whether the
date fits. If it says the date does not fit, tell the founder the earliest date it gives,
and which task to shorten to keep their date. Never move dates by hand to make it fit.

Lead times you do not know (a permit, a supplier) go in as the founder's best estimate,
marked `est.` in the task name, with a task to confirm them in week 1.

## Step 3: launch day

An hour-by-hour run sheet: who is where, what goes out on which channel, the opening offer
(from `founder/offer.md` if present), and what to do if something breaks (from the risk
register in `founder/ops.md`). The founder posts and sends everything themselves; the plan
says what and when.

If the founder wants a short promo video for launch day, the `launch-video` skill makes a
script and scene plan from the product or brief.

## Step 4: the first 30 days

The weekly numbers to track: units a day against break-even (from `founder/cfo.md`), and
the channel numbers from `founder/marketing.md`. For each, the level that triggers a change
and what the change is. Reviews on days 7, 14 and 30, each with three questions to answer.
If there is no break-even yet, track against the pass-line pace from Step 1 (20 orders in
14 days is about 10 a week), mark it "interim until /founder-cfo", and list
`/founder-cfo` under what is missing. Never make up a break-even. Trigger
levels are the founder's call: base them on a test result where one exists ("the concierge
test kept 80%, so act under 60%") and say so, or leave `{{your trigger}}`.

## Output

`founder/launch.md`, in this order:

1. The test: assumption, test, pass line, status, result.
2. Go or no-go: one line.
3. The countdown (paste `founder/countdown.md`) and the critical path.
4. Launch-day run sheet.
5. First 30 days: numbers, triggers, review dates.
6. What is missing, and which skill fills it.

In chat: the go or no-go line, the launch date and whether it fits, the critical path in a
line, and the next step. Next: `/founder-plan` compiles everything into the business plan.

## Rules

- No countdown on a failed test. No big spend scheduled before a gate passes.
- Every date comes from the tool and the task file, not from memory.
- No invented lead times, numbers or results. Unknown is `{{...}}` or `est.` with a task to
  confirm it.
- The founder posts, sends and signs. The plan never says a post "goes out automatically".
- Not legal advice. Permits and registrations depend on the city and state; the plan says
  what to check and with whom.
