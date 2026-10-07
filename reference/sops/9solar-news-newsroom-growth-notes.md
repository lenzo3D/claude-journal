# 9 Solar News newsroom: notes and future options

Internal. Written 7 Oct 2026, after the build and the whole-branch review. Nothing here is scheduled work. It is the list of things worth knowing as the site grows.

## 1. Running costs, and the one lever worth pulling

Measured from the role table and real call counts (23 model calls per cycle, 4 cycles a day, 3 stories per cycle):

| Item | Monthly |
|---|---|
| Anthropic API | about $20 realistic, $51 worst case |
| Cloudflare Workers Paid | $5 |
| Sanity, Unsplash | free tier at this volume |
| Hard ceiling (monthlyCapUsd $100) | about $105 |

Against a $1,200 retainer that is roughly 98% gross margin.

**The lever to pull as you grow is volume, not model cost.** About $75 a month of the cap sits unused. Raising `storiesPerCycle` from 3 to 6 after shadow mode roughly doubles per-story spend to about $40 a month, stays inside the cap, and doubles what the client is paying for. That is worth more than any saving on model choice.

**Already taken, so do not go looking for them again:** the Batch API (50% off, `src/llm/gateway.ts`) and prompt caching (`src/agents/format.ts`). Those are the two large levers and both are in the build.

**Decided against, with the reason:** moving the Editor, Writer, Writer-meta and Localiser to Haiku 4.5 saves $5.69 a month. The golden set only exercises the Verifier and the Risk Classifier, so an article-quality or Malay-quality downgrade cannot be measured by any test we have. Unmeasurable quality risk for five dollars.

**Third-party routers (OpenRouter and similar):** revisit only if two things change together. They lose the 50% batch discount, which roughly doubles the model bill, and they do not surface Anthropic Citations, which the Verifier checks claims against and which is the POFMA defence. Price alone will not make this worth it.

**Watch as traffic grows:** the Sanity free tier and the Cloudflare included allowances will bind eventually. Neither is close at launch volume.

**Re-verify at go-live:** the price table in `newsroom/src/llm/models.ts` carries a date and a re-verify comment. Checked against current rates on 7 Oct 2026 and correct.

## 2. Coverage is limited by source terms, not by the software

Only NASA, data.gov.sg and Eco-Business can be cited as evidence. Everything else is a signal: it can point the newsroom at a story but cannot be quoted. Al Jazeera and Bernama explicitly ban the use.

**The highest-value growth move is editorial, not technical:** written permission from CNA, Bernama or Malay Mail for excerpt use with credit would widen Singapore and Malaysia coverage more than any code change. Worth asking once the site has a track record to point at.

UNEP, CNA, BBC and the Guardian terms pages were blocked to Claude's tools. A manual read could upgrade any of them, UNEP most likely.

## 3. Open risks carried out of the review

Fixed but unverified against live services:
- The takedown now unsets homepage references before deleting in Sanity. The unset filter syntax has never run against real Sanity.
- The source-change monitor hashes main page text with a 20,000 character cut. Dynamic news pages may still look changed every day, which triggers paid re-checks. Check on staging before stage 1.
- A number swapped for another number with no unit (two years, for example) is not caught by the Malay back-check. Unit-bearing swaps and number words are caught.
- A correction note appears in English on the Malay version. No model translation of a legally sensitive note was the deliberate choice.
- The Studio action filter keys on the `nr-` id prefix, because `aiGenerated` is not available to it. A human-written article given an `nr-` id would also lose delete, unpublish and duplicate.

Never testable offline, so check once staging exists:
- Sanity `patch` with `setIfMissing` plus `insert after corrections[-1]` on an empty array.
- The real Telegram webhook payload shape.
- A real Cloudflare Access JWT.
- KV propagation time for a takedown.
- Workflows `create` idempotency on a repeated cycle id.

Pre-existing, not caused by this work:
- `tests/shorts.checks` `loops-forward-to-first` fails intermittently, on the untouched base branch too.
- `studio/schemaTypes/article.ts` has a plain-tsc error.
- Literal em dashes remain in older docs and code comments. The branch adds none.

## 4. Legal and compliance thresholds to watch

- **IMDA licensing applies at 50,000 Singapore unique visitors a month.** The spec's own alert threshold is 30,000, to give warning. The automatic alert is not built (ruling R21) because it needs an analytics source. Until then an operator checks analytics monthly, which is in the ops guide. **Connect Google Analytics 4 or Cloudflare Web Analytics and this becomes buildable.**
- The publisher of record, the liability terms with Mr Saat and the IMDA bond figure are all still open.
- Chinese and Arabic UI strings were drafted by Claude and are gated off. They need a native check before either language is switched on.

## 5. Already specified for later

The spec names four follow-on specs: distribution and auto-posting, the reader loop (real or hallucination voting, labelled comments, moderation), the agent surface (MCP server and llms.txt), and self-improvement (prompts improved against the golden set and shadow scores, never automatic for the Verifier or the Risk Classifier).

Smaller items: the Pexels key when issuance reopens (the code already tolerates its absence and uses Unsplash only), and a second operator Telegram id when someone else shares the alert load.

## 6. The real cost of this contract

The API is about 2% of the retainer. The actual cost is operator time: answering held-story alerts, the 14 days of shadow-mode scoring, and the POFMA or takedown path. If the margin ever comes under pressure, systemise that, not the model bill.
