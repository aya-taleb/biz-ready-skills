---
name: offer
description: >-
  Builds the offer around a product so buyers find it easier to say yes: what is included,
  extras that each answer a real objection, a guarantee the business can afford, honest
  urgency (a real date, cohort or capacity, never a fake timer), and a plain name. Starts
  from the objections buyers actually raised (interviews, reviews, the buyer panel), costs
  every piece per sale so the margin stays visible, and ends with the offer as a buyer will
  read it plus a test to run. Use it when someone says "make my offer better", "why aren't
  people buying", "what bonuses should I add", "should I offer a guarantee", "how do I add
  urgency", "package my service", "name my offer", "irresistible offer", or "people say
  it's too expensive". Not for picking the price itself (founder-pricing) or ads
  (marketing).
argument-hint: "[product and price, if not in founder/]"
---

# offer

People rarely say no to a product. They say no to a risk, a cost, a hassle or a delay. The
offer is the set of answers to those, wrapped around the product. This skill builds it from
the objections buyers really have, and keeps an eye on what each answer costs.

What the user typed after `/offer`: `$ARGUMENTS`

## Reads and writes

- Reads first: the business context (`founder/context.md`, else the active file under
  `~/.founder/businesses/`). Then `founder/idea.md`, `founder/pricing.md`,
  `founder/competitors.md` (complaints), `founder/discovery/evidence.md` (interviews),
  `founder/panel/results.md` (simulated buyer objections), `founder/numbers.json` and
  `founder/cfo.md` (unit cost and margin). List what exists.
- Writes: `founder/offer.md`.

## Step 1: the objections, ranked, with sources

List the reasons buyers give for not buying. Take them from, in this order of trust:

1. Real conversations (`founder/discovery/evidence.md`, or what the founder says buyers told
   them).
2. Public complaints about rivals (`founder/competitors.md`), since they show what buyers
   fear will go wrong.
3. The simulated panel (`founder/panel/results.md`). Label these "simulated". They are
   useful for wording, weak as proof.

If there are no sources, ask the founder for the three things buyers say most. If they do
not know, say that the offer will be built on guesses, mark each objection `assumed`, and
suggest `/customer-discovery` or `/founder-consumer --quick` to check.

Rank by how often each comes up and how much it blocks a sale. Keep the top three to five.
Most fall into a few kinds: price or value, doubt it works, effort or change, timing, and
trust in a new business.

## Step 2: one answer per objection

For each top objection, design the piece of the offer that answers it. Pick what fits the
business; there is no fixed menu. Examples of what a piece can be:

| objection kind | pieces that can answer it |
| --- | --- |
| price or value | a smaller first step (trial week, starter size), a bundle that lowers the per-unit price, payment split |
| doubt it works | a guarantee, a first result fast, a demo or sample, proof from real customers |
| effort or change | setup done for them, a template, a migration, a reminder system |
| timing | a start date that suits them, a pause option, a founding cohort that starts on a set date |
| trust in a new business | a named person to call, a local pickup, a short first commitment |

For each piece write: what it is, which objection it answers, and its cost to the business
per sale (from `founder/numbers.json` or the founder; else `{{cost per sale}}`). A piece that
answers no objection does not go in. Extras pile up cost and make the offer harder to read.

## Step 3: the guarantee

Write one guarantee, only if the business can honor it. State it plainly: what is promised,
the time window, what the buyer has to do, and what they get back. Then the cost: if
{{refund rate}} of buyers use it, what does it cost per month? If the founder cannot afford
a full refund, offer a smaller honest one (redo the job, a credit, the first week free).

Refund and auto-renewal rules differ by state and country. Add one line saying the founder
should check the terms with a local lawyer or their payment provider's rules.

## Step 4: honest urgency

Only add a reason to decide now if it is true:
- a real date (the founding cohort starts on March 2; the intro price ends when the pop-up
  closes on June 30),
- real capacity (the kitchen makes 80 meals a day; 12 setup slots this month),
- a real cost of waiting for the buyer (the season, a deadline they face).

Write the reason and the fact behind it. If there is no true reason, say so and leave
urgency out. A fake timer, a "only 3 left" that resets, or a "was $X" price that was never
charged costs trust when buyers notice, and in many places it breaks consumer protection
rules.

## Step 5: the name

Three plain names for the offer that say what the buyer gets ("Founding Lunch Club: 4
weeks, 20 lunches"). Avoid hype words. Pick one and say why.

## Step 6: write it out and test it

Write `founder/offer.md`:

```markdown
# Offer: <name>

Built: YYYY-MM-DD. Sources: <files used>.

## As the buyer reads it
<5 to 8 short lines: what you get, the price, the guarantee, the reason to start now>

## Objections and answers
| objection | source | answered by | cost per sale |
| --- | --- | --- | --- |

## Guarantee
<terms> Cost if {{refund rate}} use it: <math or placeholder>.

## Why now
<the true reason and the fact behind it, or "none: no urgency used">

## What it does to the margin
<price, minus the added cost per sale; or "run /founder-cfo with these costs">

## Test it
<one test: show it to {{n}} buyers, a landing page, a pre-sale; with a pass line>
```

Before the founder uses the buyer-facing lines anywhere, run them through the `humanize`
skill if it is installed.

If the founder wants to see the offer on the simulated buyer panel, copy the current
`founder/pitch.md` to `founder/pitch-v1.md` first, then write the buyer-facing lines into
`founder/pitch.md`, and suggest `/founder-consumer --quick` with the same seed as before.
Keeping the old version means the two runs can be compared. Real buyers still decide; the
panel only shows whether the objections moved.

When a cost is derived (a free week as a share of a monthly cost), show the math in one
line so the founder can check it.

## Tell the user

The offer in its buyer-facing lines, the top objection and how it is answered, what it
does to the margin, and the test. Next: `/founder-cfo` to rerun the numbers with the new
costs, `/founder-consumer` to show the new offer to the simulated panel, or `/marketing` to
build the message around it.

## Rules

- Every piece answers a named objection. Nothing added for show.
- Every cost is from the founder's numbers or a placeholder. No invented costs or refund
  rates.
- No fake urgency, scarcity, anchors, reviews or testimonials. Panel answers are never
  testimonials.
- No result claims the founder cannot prove (health, income, weight, savings). Flag
  regulated claims for a lawyer.
- Not legal advice.
