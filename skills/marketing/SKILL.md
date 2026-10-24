---
name: marketing
description: >-
  A marketing plan one founder can actually run. Sets the positioning from the rivals and
  the objections (not adjectives), picks the channels these buyers already use, computes
  the most you can pay to get a customer with a small tool (math shown), and writes a
  dated 30-day plan paced for one person, with what to post, send or do each day and the
  number that says keep, change or stop. Local businesses get local channels (offices,
  walk-ins, partners, map listings, neighborhood groups). The founder posts and sends
  everything. Use it when someone says "marketing plan", "how do I get customers", "where
  do I find my first customers", "what should I post", "30 day plan", "how much can I
  spend on ads", "customer acquisition cost", "positioning", or "nobody knows we exist".
  Not for ad account management or writing one email (biz-boost skills do that).
argument-hint: "[start date YYYY-MM-DD]"
---

# marketing

Most early marketing fails for one of three reasons: the message is about the product
instead of the buyer, the founder is on channels their buyers do not use, or they spend
more to win a customer than the customer is worth. This skill fixes all three, then
gives the founder a month they can actually keep up.

What the user typed after `/marketing`: `$ARGUMENTS`

## Reads and writes

- Reads first: the business context (`founder/context.md`, else the active file under
  `~/.founder/businesses/`), for tone and words to avoid. Then `founder/idea.md`,
  `founder/competitors.md`, `founder/offer.md`, `founder/pricing.md`,
  `founder/numbers.json`, `founder/cfo.md`, `founder/discovery/evidence.md`,
  `founder/panel/results.md`, `founder/launch.md` (the launch date). List what exists.
- Writes: `founder/marketing.md`.
- Tool: `scripts/max_cac.py` computes the most you can pay for one customer.

## Step 1: positioning

Write one short statement in this order: for <who>, who <the situation>, <business> is the
<category> that <the one difference>, unlike <what they use now>, which <its weakness, from
the complaints>.

Take "what they use now" and "its weakness" from `founder/competitors.md` and the
objections. If those files are missing, ask the founder who they lose buyers to, and mark
the statement `assumed` until `/competitors` runs. A position nobody else can say is worth
more than a clever line.

Then three message lines, each answering one top objection from `founder/offer.md` or the
panel, in the buyer's words.

## Step 2: the most you can pay for a customer

Run:

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/max_cac.py" --numbers founder/numbers.json --per-month <units a month> --months <months a customer stays>
```

or with `--price` and `--unit-cost` if there is no numbers file. Use `--churn` for a
subscription if the founder knows it. It shows each step: contribution per unit, value per
customer, the break-even cost to win one, a safer target (a third of value by default), and
a payback cap if asked.

How long a customer stays and how often they buy are usually guesses at this stage. Say so,
use the founder's guess, and show what happens if it is half as long. If there is no
number at all, write the formula with `{{...}}` and point to `/founder-cfo`. Never invent a
retention rate.

Why it matters: the founder needs this number before any paid test, so they know when to
stop a channel that is too expensive.

## Step 3: pick the channels

List where these buyers already spend attention. Think about the buyer's day, not the
platforms you know. Then pick two or three to test, not ten. For each: why these buyers are
there, what a cheap test looks like, how many hours a week it takes, and what it costs.

| business | channels to consider first |
| --- | --- |
| local (food, services, shops) | the office or building manager, walk-in visits, partner businesses, neighborhood and workplace groups, the map listing, flyers where buyers wait, local events |
| online consumer | communities where the problem is discussed, short video showing the moment it works, search for the problem, creators the buyers follow, referrals |
| B2B | direct outreach to a named list, the communities the role belongs to, partners who already sell to them, content that answers the buyer's questions |

One person has about {{hours a week}} for marketing. Ask, and fit the plan to that number.
A plan that needs 30 hours a week from someone with 8 gets dropped by day 5.

## Step 4: the 30-day plan, with dates

Start on the date given, or `founder/launch.md` minus 14 days, or tomorrow. Write it in
four weekly blocks with real dates. For each day or task: what to do, which channel, who
does it (usually the founder), and the number to check. Put the first test of each channel
in week 1, so week 3 can double down on what worked.

At the end of each week, one line: the number to check and the level that says keep,
change or stop. Derive the level from the max cost per customer in step 2 and write the
math: "stop if a sign-up costs over $39.60, the safer target at half the stay". For a free
channel, count the founder's hours at {{your hourly value}} or the cost of what is given
away (samples, free meals, credits). A level with no reason behind it is just a guess.

Every give-away in the plan (a free meal per referral, a free week, samples) gets its cost
next to it, from the unit cost.

Write two or three example messages for the top channel: a post, a short outreach note, a
flyer line. The founder sends and posts them. Run them through the `humanize` skill if it
is installed. If a draft is a cold email, include the sender's physical address and an
opt-out line (CAN-SPAM). No made-up stats, results or testimonials in the copy.

## Step 5: save

Write `founder/marketing.md`:

```markdown
# Marketing: <business>

Written: YYYY-MM-DD. Read: <files>. Assumed: <what was a guess>.

## Positioning
## Messages (one per top objection)
## The most you can pay for a customer
<tool output, and the "half as long" line>
## Channels to test
| channel | why these buyers are there | test | hours a week | cost |
## 30 days (YYYY-MM-DD to YYYY-MM-DD)
### Week 1 (dates)
...
## Keep, change or stop
| channel | number | keep if | stop if |
## Example messages
```

## Tell the user

The positioning in a line, the max cost per customer, the two or three channels, and what
to do on day 1. Next: `/brand` if the name and look are not set, `/launch` for the dated
launch, or the biz-boost skills (`reach-plan`, `lead-gen`, `local-outreach`) and the
LinkedIn or Instagram plan skills to go deeper on one channel.

## Rules

- The founder posts, sends and calls. Never automate posting, messaging or scraping on any
  platform, and never buy or build contact lists against a site's terms.
- No invented stats, testimonials, reviews, results or retention numbers.
- Paid tests show their budget and wait for the founder's yes. This skill spends nothing.
- Cold email drafts carry a physical address and opt-out.
- Claims about health, money or results need proof; flag them for a lawyer if regulated.
