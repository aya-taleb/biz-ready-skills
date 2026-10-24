# Contributing

Thanks for helping. Fixes, better examples and new test cases are all welcome.

## Where to send a fix

Some skills here are shared across several of my repos. Each one has a single home.
Fix it in its home repo, and the change gets copied everywhere else.

| skill | home repo |
| --- | --- |
| competitors | biz-ready-skills (this repo) |
| board | biz-ready-skills (this repo) |
| launch | biz-ready-skills (this repo) |
| funding | biz-ready-skills (this repo) |
| pitch | biz-ready-skills (this repo) |
| offer | biz-ready-skills (this repo) |
| marketing | biz-ready-skills (this repo) |
| brand | biz-ready-skills (this repo) |
| ops | biz-ready-skills (this repo) |
| customer-discovery | [entrepreneur-skills](https://github.com/aya-taleb/entrepreneur-skills) |
| validate | [entrepreneur-skills](https://github.com/aya-taleb/entrepreneur-skills) |
| launch-video | [multimedia-skills](https://github.com/aya-taleb/multimedia-skills) |
| founder-consumer, founder-pricing, founder-cfo, founder-plan | [Jake Schincariol's founder-skill](https://github.com/Jakeschincariol/founder-skill) (linked, not copied here; send fixes to Jake) |

If you edit a copy here instead of the home, the pull request check will fail and point
you to the right repo. That's on purpose, so your fix doesn't get wiped on the next sync.

## How to make a change

1. Fork the repo and make your change on a branch.
2. If you changed a Python tool, run its tests:
   `python3 -m unittest discover -s tests -v`
3. Run the checks: `python3 scripts/validate.py`
4. If you changed how a skill behaves, add or update a test case in
   `skills/<skill>/evals/`. Each case is a folder with a prompt and a few checkable
   statements. Copy an existing case to start.
5. Open a pull request. Say what you changed and why, in a few lines.

## House rules for writing

- Plain words, short sentences. Write like a person.
- No em dashes.
- Skip the stock AI words listed in `scripts/validate.py`. The check will flag them.
- Never make up facts, numbers, quotes or sources in a skill or an example.

## Good first issues

Look for the `good first issue` label. A new test case, a clearer example, or a better
"where to look" source for competitors or funding are all great places to start.
