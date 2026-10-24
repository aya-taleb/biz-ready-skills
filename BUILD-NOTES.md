# Build notes

Built 2026-10-23. Validate is clean and all 58 unit tests pass (`python3 -I -m unittest
discover -s tests`).

## Unfinished

- **Synced skills are not copied in yet.** customer-discovery and validate (from
  entrepreneur-skills) and launch-video (from multimedia-skills) are listed in skills.json
  and arrive with the sync step. The README already lists them.
- **Scores are self-graded.** No subagent tool was available, so I ran and graded every
  case myself. Rerun the evals with `claude plugin eval` before trusting the numbers.
- **Live trigger tests were not run.** Trigger fit was judged by reading the descriptions.

## Needs Aya

- **founder-plan's "Not done yet" list names Jake's skills.** His compile.py says "run
  /founder-competitors", "/founder-offer" and so on for missing sections. With our skills
  installed, the right names are /competitors, /offer, /marketing, /brand, /ops, /launch,
  /board. We can't change his linked file. Options: ask Jake to make the names
  configurable, or add a line to the README. I added nothing yet.
- **Shared kitchen example.** The local test runs used Twelve Baskets (Kirkland) from a
  public listing as a commissary example for Curbside Lunch Club. That's a test fixture,
  not a recommendation. Check it yourself if it's useful.
- **pitchnarrative handoff.** pitch hands slide design to a deck design skill and names
  your pitchnarrative as the example. If you'd rather not name it in a public repo, change
  one line in `skills/pitch/SKILL.md` (Step 4).

## Calls to review

- **Exact copy of source_check.py in funding.** A unit test keeps it equal to the one in
  competitors. If you'd rather funding depend on competitors being installed, delete the
  copy and point the command at the competitors folder.
- **Default "safer target" in max_cac.py is a third of customer value.** It's a stated
  rule of thumb, labeled in the output and changeable with `--share`. Change it if you
  prefer a different default.
- **fit.py thresholds:** "closing soon" is 21 days and "check again" is 30 days.
- **Board lens list** (references/lenses.md): Jobs to be Done, riskiest assumption first,
  engines of growth, Bullseye, 7 Powers or Five Forces, and a pre-mortem. These are all
  published frameworks, credited, and none are a person's persona. Swap any you dislike.
- **SBIR note in funding/references/where-to-look.md** says the programs were reauthorized
  in 2026 with new rules. That was true on 2026-10-23 (checked on news pages and
  sbir.gov). The skill still tells users to check the live pages.

## Fix round after review

- User data moved out of `~/.claude` (protected by Claude Code) to `~/.founder`: business files, social folders and the media ledger. Tools honor `FOUNDER_HOME`; tests use a temp one.
- launch: with no break-even, the pass line is a real count and deadline from what the founder knows (default floors such as 20 paid pre-orders in 14 days), with the reasoning shown. `{{...}}` only for numbers the founder must give. New grader in local-no-test-yet. Aya: check the floors suit you.
