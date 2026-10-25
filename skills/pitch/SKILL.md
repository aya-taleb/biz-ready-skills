---
name: pitch
description: >-
  Writes the investor story and keeps investors informed. Two jobs: (1) a deck narrative
  of 10 to 12 slides, each with its one message, the words to say, and the exact numbers
  and proof it needs from founder/ files (missing ones become placeholders, never
  guesses); (2) a monthly investor update with real numbers, wins, a bad-news section
  that says what went wrong and what you are doing about it, and clear asks. Use it when
  someone says "help me pitch", "pitch deck", "deck outline", "what goes on each slide",
  "tell my story to investors", "investor update", "monthly update to my angels", "write
  my update", or "I have a pitch meeting Friday". It writes the story and the numbers, not
  the slide visuals: for layout and design it hands off to a deck design skill. Not for
  finding investors (funding) or the buyer pitch the consumer panel tests (founder-consumer).
argument-hint: "[deck | update] [month YYYY-MM for an update]"
---

# pitch

An investor decides fast and checks later. The story has to be clear in a few minutes, and
every number in it has to hold up when they check. This skill builds both from what is
already in `founder/`, and marks what is missing instead of filling it in.

What the user typed after `/pitch`: `$ARGUMENTS`. If it says neither deck nor update, ask
which one, or infer it from the request.

## Reads and writes

- Reads first: the business context (`founder/context.md`, else the active file under
  `~/.founder/businesses/`). Then `founder/idea.md`, `founder/board.md`,
  `founder/competitors.md`, `founder/market.md`, `founder/validate.md`,
  `founder/discovery/evidence.md`, `founder/numbers.json`, `founder/cfo.md`,
  `founder/pricing.md`, `founder/funding.md`, `founder/launch.md`. List which exist.
- Writes: `founder/deck.md` (the narrative), `founder/updates/YYYY-MM.md` (each update),
  and `founder/updates/metrics.json` (the numbers, so next month can compare).
- Leaves `founder/pitch.md` alone. That file is the short buyer pitch that Jake
  Schincariol's founder-consumer shows its simulated buyers; overwriting it would change
  their test.
- Reference: `references/slides.md` has what each slide must prove and the numbers it
  needs.

## Part 1: the deck narrative

### Step 1: the one-line story

Write one sentence an investor could repeat: who has the problem, what you do, the proof
that it works, and why now. Everything in the deck supports that line. If you cannot write
it from the files, ask the founder the missing piece; do not make one up.

Check every number in the line against a file before you write it down. The deck file is
what the founder will present, so it holds only the final version: no drafts, no "wait,
revised" notes, no struck-out guesses.

### Step 2: pick the slides

Use 10 to 12 slides from `references/slides.md`. The default order is: title, problem,
customer, solution, proof, market, business model, competition, go-to-market, team,
financials and the ask, use of funds. Move proof earlier if it is strong; it is the slide
investors remember. Drop a slide only if it has nothing true to say, and say why.

### Step 3: write each slide

For each slide, in `founder/deck.md`:

- **Message**: the one thing this slide must make the investor believe, in one sentence.
- **Say**: what the founder says out loud, three to five short sentences.
- **Show**: the one chart, number, quote or image, described plainly.
- **Numbers**: each figure, with where it comes from (`founder/cfo.md`, a link, a test
  result). A figure without a source becomes `{{...}}` with the skill that finds it.
- **Likely question**: the question an investor will ask here, and a short honest answer.

Market size comes from `founder/market.md` or a linked source. Never use a big top-down
number by itself; investors trust a bottom-up count (buyers you can reach times what they
pay). If there is no market file, write `{{market size: run /market-research}}`.

Customer quotes come only from real interviews in `founder/discovery/evidence.md`, with
permission. Simulated buyer panel answers are research, not quotes; never put them on a
slide as if a customer said them.

### Step 4: hand off for design

This skill writes the story and the numbers, not the slide layout. If the user has a
deck or slides skill installed, hand `founder/deck.md` to it for the slide design. If not, offer to
export the narrative to a slide file with whatever tool is available, keeping
`founder/deck.md` as the source.

## Part 2: the monthly investor update

### Step 1: the numbers

Ask for or read this month's numbers: revenue, users or customers, burn, cash in the bank,
runway in months, and the one or two numbers that matter most for this business. Save them
to `founder/updates/metrics.json` keyed by month. If last month exists, show the change.
Runway is cash divided by monthly burn; compute it, show the math in a line, and say if the
founder did not give one of the two.

### Step 2: write it

`founder/updates/YYYY-MM.md`, short enough to read in two minutes:

```markdown
Subject: <Business> update, <Month YYYY>: <the headline in a few words>

**The headline**: <one line, the most important thing this month, good or bad>

**Numbers** (vs last month)
| | this month | last month | change |

**Wins**
- <2 to 3, specific>

**What went wrong**
- <what happened, plainly>
- <what it cost, in numbers if known>
- <what you are doing about it, and by when>

**Next month**
- <2 to 3 goals with a number>

**Asks**
- <specific: an intro to a named kind of person, a hire, advice on a named question>
```

The bad-news section is never empty. Every month something slipped. Investors who hear
bad news early from the founder keep trusting the founder; investors who find it later
stop. If the founder says nothing went wrong, ask what they would have done differently.

Asks are specific. "Intros to office managers at Bellevue companies with 200+ staff" gets
answered; "any help is welcome" does not.

Run the draft through the `humanize` skill before showing it, if it is installed. The
founder sends it; this skill never sends email.

## Tell the user

For a deck: the one-line story, how many slides, which slides have `{{...}}` gaps and
which skill fills each, and the design handoff. For an update: the headline, the bad-news
line, and the asks. Next skill: `/funding` to find who to send it to, `/founder-cfo` if the
numbers are thin.

## Rules

- Every number has a source or is a placeholder. No invented traction, market size,
  revenue, users, logos, quotes or team members.
- Do not round in your favor. 31 signups is 31, not "dozens"; 7.5% is not "nearly 10%".
- No hype words, no "revolutionary", no "the Uber of". Plain claims backed by proof land
  better.
- Projections are labeled projections, from `founder/cfo.md`.
- The founder sends everything. Not investment or legal advice; for round terms, a startup
  lawyer.
