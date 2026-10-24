# Testing

How these were tested, said once: I (the building agent) ran every case myself by
following each SKILL.md, and graded the outputs myself against the graders in
`skills/<skill>/evals/`. No subagent tool was available in this build session, so the
runs were not blind. I wrote the skills and graded them with full context, which favors
them. Treat the scores as a careful self-check, not an outside measure. Aya can rerun the
same cases with `claude plugin eval`.

The web research in the runs was real (pages fetched on 2026-10-23, with links in the
outputs). Run outputs and grade notes are in `_work/biz-ready-skills/<skill>/round-N/`
in the build folder, outside this repo.

Rubric (TEST-PROTOCOL section 2): graders 40, follows its own rules 15, nothing made up
15, tone and format 10, handoff 10, trigger fit 10. Trigger fit was judged by reading each
description against the 12 prompts in `evals/triggers.json`, not by a live trigger run.

In later rounds I reran the case or cases a change touched and carried the other cases'
grades forward. Where that happened, the round line says so.

| skill | baseline | final | rounds | beats baseline? |
| --- | --- | --- | --- | --- |
| competitors | 78 (Jake founder-competitors) | 96 | 2 | yes |
| board | 74 (Jake founder-board) | 96 | 1 | yes |
| launch | 55 (Jake founder-launch, the original) | 98 | 2 | yes |
| funding | 36 (no skill) | 98 | 1 | yes |
| pitch | 24 (no skill) | 97 | 2 | yes |
| offer | 61 (Jake founder-offer) | 98 | 1 | yes |
| marketing | 58 (Jake founder-marketing) | 98 | 1 | yes |
| brand | 74 (Jake founder-brand) | 98 | 1 | yes |
| ops | 67 (Jake founder-ops) | 98 | 1 | yes |

Linked skills (founder-consumer, founder-pricing, founder-cfo, founder-plan) got a
read-through check only: their file names and formats are what our skills write. Synced
skills (customer-discovery, validate, launch-video) are tested in their home repos.

---

### competitors  (rewritten, HOME, synced to entrepreneur and mimic)
baseline: 78 (Jake's founder-competitors run on the same 3 cases)
final: 96 after 2 rounds. Stopped because the score was 95+ and the last round gained 1.
rounds:
- r0 (ours v1): 83. Lost points on unlinked map review quotes, a one-mention "pattern", and no chat reply naming the next skill.
- r1: 95. Map results linked by place ID, headlines copied for the top three rivals, one-mention complaints dropped, the reply always names the next skill, the tool skips the scope line, a near-miss line added to the description. All 3 cases rerun.
- r2: 96. Substitute costs may be estimates marked `est.` with a reason. Local case rerun; others carried.
open issues: the source check tool cannot tell whether a link really supports a fact, only that one is there.

### board  (rewritten)
baseline: 74 (Jake's founder-board)
final: 96 after 1 round. Stopped because the score was 95+ and the last round gained 4.
rounds:
- r0 (ours v1): 92. Lost points on an unlinked app store fee claim and long table cells.
- r1: 96. Platform fees need a link or a placeholder, and "why" cells are capped at two lines. App and local cases rerun; edge carried.
open issues: lens independence relies on instructions (or subagents if present); without subagents, one model still scores all lenses.

### launch  (reworked from Jake's founder-launch)
baseline: 55 (Jake's original on the same cases: it never reads validate.md, schedules a lease before the test, and builds a countdown on a failed test)
final: 98 after 2 rounds. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r0 (ours v1): 96. Lost a point on an invented 30-day trigger level.
- r1: 98. Trigger levels tied to test results or left as `{{your trigger}}`. App case rerun; others carried.
- r2: 98. Lined up with the validate skill's real files (validate-plan.json, validate-results.json, its testplan.py), "unclear" or "too early" counts as not passed. No grader changes.
open issues: none.

### funding  (ours)
baseline: 36 (no skill: a plain answer listed remembered programs and amounts with no links or dates, and said AI apps qualify for SBIR)
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained 3.
rounds:
- r0 (ours v1): 95. The local run wrote the ranked table by hand instead of with fit.py, and assumed a $14 price the founder had not given in that prompt (the source check tool caught it).
- r1: 98. The ranked table must come from fit.py even for short lists; the founder's own numbers are used only if given. Local case rerun; others carried.
open issues: program facts go stale fast; fit.py flags anything found more than 30 days ago.

### pitch  (ours)
baseline: 24 (no skill: invented market size and time-saved stats, rounded 7.5% to "nearly 10%", softened the bad news, called 2.8 months "healthy runway", and suggested harvesting angel emails)
final: 97 after 2 rounds. Stopped because the score was 95+ and the last round gained 1.
rounds:
- r0 (ours v1): 91. The deck file shipped with a draft one-liner holding an unsourced number and a self-correction note.
- r1: 96. Numbers in the one-line story are checked against files, and deck.md holds only the final version. Deck case rerun.
- r2: 97. The description now says it does not do slide visuals, so a Figma design request should not fire it. No case rerun needed.
open issues: slide design is handed off (for example to pitchnarrative); this skill does not make slides.

### offer  (rewritten)
baseline: 61 (Jake's founder-offer: invented a 10% claim rate, used made-up "this month" urgency, and gave a guarantee with no window)
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained 3.
rounds:
- r0 (ours v1): 95. Lost points on a derived cost with no math shown, and no step to keep the old buyer pitch before a panel re-test.
- r1: 98. Copy pitch.md to pitch-v1.md before a panel re-test (an idea from Jake's version, credited), and show the math for derived costs. App case rerun.
open issues: none.

### marketing  (rewritten)
baseline: 58 (Jake's founder-marketing: no max cost per customer when panel data was missing, social-first channels for a local office business, a budget split with no budget, no hours or dates)
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained 4.
rounds:
- r0 (ours v1): 94. Lost points on stop levels not tied to the max cost per customer and no reply naming the next skill.
- r1: 98. Stop levels come from the max cost with the math, give-aways are costed, and the reply names the next skill. App and local cases rerun.
open issues: none.

### brand  (rewritten)
baseline: 74 (Jake's founder-brand: said fridgeplan.com "appears to be free" when the registry shows it registered since 2025, and dated no checks)
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained 2.
rounds:
- r0 (ours v1): 96. Lost points for no color contrast check.
- r1: 98. A contrast check added to name_checks.py (an idea from Jake's version, credited), plus a font licensing line. App and local cases rerun.
open issues: the USPTO search is a browser app, so trademark checks come back "not checked" with the link unless the founder or a browser tool runs them.

### ops  (rewritten)
baseline: 67 (Jake's founder-ops: edited numbers.json by hand with no backup or gap list, gave tools with no prices, and had no lead times for launch)
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained 2.
rounds:
- r0 (ours v1): 96. Lost points on a permit row linked to a page that only mentions it, and an estimate with no basis.
- r1: 98. Permit rows link the issuing office's own page or say "mentioned on", and an estimate with no basis becomes `{{ask the office}}`. Local case rerun.
open issues: none.

---

## Calls I made

- **Shared tool copy.** `source_check.py` lives in competitors (the shared skill) and an
  exact copy lives in funding, because a synced skill folder must stand alone. A unit test
  fails if the two copies drift.
- **Baseline for "ours" skills** (funding, pitch) was a plain answer with no skill, as the
  protocol says. Those baselines are weak, so the gap looks large.
- **Jake's runs.** I ran Jake's SKILL.md text as written, on the same inputs and with the
  same web research I had, so the comparison is about the instructions, not the data.
  His sub-agent steps (board members, panel re-tests) were not run, since no subagent tool
  was available; I noted that in those outputs and did not grade against it.
- **USPTO.** The trademark search could not be run from the build environment. Brand
  records it as "not checked" with the link, which is the honest result, rather than
  treating a web search as a trademark check.
- **Launch and validate.** Launch reads validate's `validate-plan.json` and
  `validate-results.json` and uses validate's own `testplan.py read` when installed,
  rather than parsing results itself, so there is one source of truth for pass and fail.
- **pitch.md is Jake's file.** Our pitch skill writes `founder/deck.md` and never touches
  `founder/pitch.md`, which founder-consumer shows its simulated buyers. The offer skill
  writes to pitch.md only for a panel re-test, after saving the old one as pitch-v1.md.

## Independent review (blind)

Done 2026-10-23 by a separate reviewer agent, following REVIEW-PROTOCOL.md. Each case was
run twice in a fresh `claude -p` (fresh empty folder, own HOME, model claude-sonnet-5-5):
once with our skill, once with the baseline. The baseline was Jake's SKILL.md text only
(plus lenses.md for founder-board), never his code; for funding and pitch it was a plain
answer with no skill. Both arms got the same tools (files, Bash, WebSearch, WebFetch,
subagents) and the same two notes: the founder can't answer questions this run, and if the
skill says to run a tool that isn't there, do that step by hand. A separate `claude -p`
judge saw the prompt, the expected outcome, the input files and the two outputs as A and B
in random order (key kept outside its folder), and scored each 0 to 10 on did the job,
nothing made up, safety, clear and usable, and tone (total out of 50).

Handicaps to keep in mind: Jake's runs had no tools of his own, so any tool step was done
by hand. The expected outcomes were written by the builder with our skills, and some name
our file paths (name-checks.json, metrics.json, updates/2026-10.md), which favors ours.
The judge is noisy: the same Jake output scored 38 in one judging and 33 in the next.
Run outputs: `_work/review/biz-ready/<skill>/<case>/` in the build folder.

| skill | case | winner | ours score | baseline score | fix rounds | one-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| board | app-ai-meal-planner | ours | 43 | 35 | 0 | Credited lenses fit for an app, low evidence score, conditions with numbers, deadlines and skills; Jake's had none of those. |
| board | local-lunch-subscription | ours | 43 | 32 | 0 | Five Forces, potluck praise read as weak, hybrid-work pre-mortem, $8k caution; Jake's conditions had no numbers. |
| competitors | online-invoicing-app | baseline (r0), ours (r1) | 38 then 41 | 38 then 33 | 1 | r0 lost: unsourced `est. $0` substitutes, one complaint pattern, fewer rivals. r1 fix: look up posted substitute prices, two review sources per main rival, a buyer's-terms cost table. |
| competitors | local-lunch-subscription | ours | 40 (r0), 38 (r1) | 35, 34 | 1 (rerun after the fix) | Linked prices turned into a five-lunch week vs the $14 plan; both arms still thin on complaints and distances. |
| offer | app-subscription-objections | ours | 42 | 36 | 0 | Panel labeled simulated, every piece tied to an objection with a cost, a pass line; Jake's had no pass line. |
| offer | local-cleaning-service | ours | 43 | 34 | 0 | Concrete test with a pass line and placeholders; Jake's guessed a 5% claim rate and self-scored value tables. |
| marketing | app-marketing-plan | ours | 39 | 35 | 0 | Keep/stop levels tied to the max cost with the half-retention line; Jake's levels were placeholders. |
| marketing | local-lunch-marketing | ours | 42 | 29 | 0 | Dated 30-day plan with the $240 and $79.20 math; Jake's declined to plan without files. |
| brand | app-name-check | ours | 43 | 35 | 0 | Dated registry lookups and name-checks.json; Jake's found the real Fridgeplan name clash but logged no dated checks. |
| brand | local-food-brand | ours | 40 | 39 | 0 | Near tie: ours dated its checks and linked the not-checked ones; Jake's had strong cultural care but an undated domain check. |
| ops | app-ops | ours | 41 | 34 | 0 | Vendor pricing pages linked, CFO cost files written; Jake's leaned on blogs and wrote no numbers. |
| ops | local-lunch-ops | ours | 42 | 33 | 0 | Permits by level, each linked and marked to confirm, backup and gap list; Jake's wrote its own cost guesses. |
| launch | app-waitlist-passed | ours | 39 | 36 | 0 | Built tasks and ran the countdown (Dec 1 does not fit, Dec 7 earliest); Jake's asserted a hand-built schedule. |
| launch | local-no-test-yet | ours | 34 | 36 | 0 | Won on the gate, `/validate` and the honest "Jan 12 does not fit", but scored lower: pass line left as `{{N}}`, too many placeholders. |
| funding | app-preseed-seattle | ours | 40 | 31 | 0 | Live programs with amount, equity and a dated, flagged YC deadline; the plain answer gave blog-sourced advice with no dates. |
| funding | local-lunch-startup-money | ours | 40 | 30 | 0 | Ranked loans and advising with links and rolling or closed status; the plain answer leaned on a 2021 fund it could not confirm. |
| pitch | app-deck-narrative | ours | 44 | 37 | 0 | 12 slides with message, say, show, sourced numbers and likely question; the plain answer stated an unsourced App Store fee. |
| pitch | local-investor-update | ours | 42 | 37 | 0 | Runway math shown both ways (2.8 months gross), plain bad news, files saved where expected. |

Funding link spot-check (2026-10-23): all 12 URLs in both funding runs resolve. 10 return
200 by curl; allianceofangels.com (429) and businessimpactnw.org (403) block curl but load
in a fetch tool. Checked against the live pages: YC Winter 2027 deadline Nov 2 at 8pm PT and
the $500k deal ($125k for 7% plus $375k MFN SAFE); SBA microloan up to $50,000, average
about $13,000, 8% to 13%, 7 years; Business Impact NW $5,000 to $750,000 at 11% to 13%; NSF
up to $2 million; Bellevue Community Programming Fund $2,500 to $10,000, closed Sept 27;
Startup425 15 weeks with a partner-city preference. All match. Soft spots: two SBA
microloan lenders (Ventures, New Roots Fund) are named without their own links, and the
Craft3 line "lends to people who cannot get bank loans" was not checked.

Changed in review: `skills/competitors/SKILL.md` (substitutes with a posted price get looked
up and linked; at least two review sources per main rival before saying there is no
pattern; main prices put in the buyer's terms with the math) and
`skills/competitors/references/output-shape.md` (new "In the buyer's terms" table).
validate and unit tests pass after the change. competitors is a shared skill, so the
synced copies in entrepreneur-skills and mimic-skills need the sync rerun.

Still weak: launch leaves the pass line as `{{N}}` when there is no break-even; local
competitors runs find few complaints and no distances; the brand local case is close to a
tie with Jake's.
