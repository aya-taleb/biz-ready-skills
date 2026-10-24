# biz-ready-skills

Claude skills that help a founder turn an idea into a business that makes money.

## What do you want to do?

| I want to... | run this |
| --- | --- |
| know who I'm up against, what they charge and what buyers hate | /competitors |
| get a hard, fair review of my idea before I spend money | /board |
| talk to customers the right way and log what I learn | /customer-discovery |
| test if people will pay before I build | /validate |
| see how simulated buyers react to my pitch | /founder-consumer |
| set a price buyers accept and the margin needs | /founder-pricing |
| make the offer easier to say yes to | /offer |
| check the numbers: margin, break-even, cash needed | /founder-cfo |
| get a 30-day marketing plan I can keep up alone | /marketing |
| pick a name, a voice and a look, with real checks | /brand |
| know how it runs day to day and what it really costs | /ops |
| find grants, loans, accelerators and angels that fit | /funding |
| write my deck story or my monthly investor update | /pitch |
| plan a dated launch that starts with proof | /launch |
| make a short launch video | /launch-video |
| put it all into one business plan | /founder-plan |

## Install

```
/plugin marketplace add aya-taleb/biz-ready-skills
/plugin install biz-ready-skills@biz-ready-skills
```

Some skills here use tools from Jake Schincariol's
[founder-skill](https://github.com/Jakeschincariol/founder-skill): founder-consumer,
founder-pricing, founder-cfo and founder-plan. Get them with:

```
python3 scripts/get_linked.py
```

## Start here

Run `/competitors` with what you sell and where. It writes `founder/competitors.md` in
your project. Then `/board` reviews the idea, and each skill after that reads what the
others wrote in the same `founder/` folder. A common order: competitors, board, validate,
founder-consumer, founder-pricing, offer, founder-cfo, marketing, brand, ops, launch,
funding, pitch, founder-plan.

## Good to know

- Nothing made up. Every competitor, price, program and deadline has a link and a date.
  Missing numbers become `{{your number}}`, never a guess.
- Nothing is called "available" unless a lookup showed it, and even then trademark
  clearance goes to a lawyer.
- You post, send, sign up and submit everything yourself. No scraping, no bots, no
  automated posting on any platform.
- Funding programs and permits change. The skills look them up live on the day and tell
  you who confirms them.
- Not legal, tax or investment advice. Each skill says who to ask.
- Jake's founder-plan may point you to his own skill names, like /founder-offer. Here,
  use /offer, /marketing, /brand, /ops, /launch and /competitors instead. They write the
  same files in `founder/`, so his plan still finds them.

## Credits

Made by Aya Taleb (github.com/aya-taleb). Uses four tools from Jake Schincariol's
founder-skill (MIT). launch is based on his founder-launch. See CREDITS.md. MIT.
