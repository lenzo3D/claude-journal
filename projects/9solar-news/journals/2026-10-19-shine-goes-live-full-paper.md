---
date: 2026-10-19
project: 9solar-news
topic: From shadow to a live daily paper: volume, go-live, preview promote, photos
outcome: shipped
satisfaction: 4/5
model: Claude Opus 5.5
run: attended
related: []
---

# From shadow to a live daily paper: volume, go-live, preview promote, photos

Covers 16 to 19 Oct 2026, one long session that was compacted at least once. The early part (16 to 17 Oct) is reconstructed from the compaction summary and the 18 Oct checkpoint file, so some detail of those days is thinner than the rest.

## The ask
- Get the Shine newsroom (formerly 9 Solar News) from 0 to 3 stories a day up to "an entire newspaper every day". Jake is charging the client S$1.2k a month and woke up to zero stories published.
- Go live on Mr Saat's verbal yes ("go with B": stage `live-low`, attributed news public). Then move every story already on the preview site to the live site.
- Fix the missing photos, from the website session's handoff.
- Standing constraints: no em dash, commit as lenzo3D, never send anything to the client, secrets by pipe only, and the kill switch is Jake's. I also held one line of my own: I would not build anything that hides where a story comes from. Citations and fact-checking stay.

## What I did
1. **Volume.** Jake pushed back hard: "You are prohibiting yourself... You need to go through them." I agreed to loosen everything that was caution rather than safety. Unchecked outlets became "attributed news": the feed headline and summary only, credited, pages never fetched. I added the switches `minPublishers`, `attributedNews`, `morningBriefing`, `minScore` and `storiesPerCycle`. The code defaults stay strict and Jake flips the settings in `/ops`. The auto-mode classifier blocked the loosening edit twice. Jake switched the session to Ask mode and I made the edit then. I did not try to get around the block.
2. **Making the pipeline actually publish.** Each fix came from reading why stories were held:
   - Scout and Editor go direct instead of batch (one batch had waited an hour)
   - citation repair, and one rewrite round for wording holds
   - the Verifier lists only real problems
   - an explicit competitor list replaces the model guessing (the golden eval had held 5 of 15 clean drafts on that guess; afterwards 0 of 15)
   - over-long headlines go to the rewrite round instead of failing the parse
3. **Go live, 18 Oct 13:45 SGT.** I triggered the first live cycle by hand: 6 published (4 English, 2 Malay), 1 high-risk story waiting for a Release, 2 held. I checked every article page on the live site and the AI label in both languages.
4. **Promote.** I built `/ops/promote` to copy preview documents from the `staging` dataset to `production`. It keeps any edits made in Studio, re-uploads the photos and skips high-risk stories unless ticked. I also fixed the homepage pointing at preview-only stories (empty slots). `/ops` sits behind Jake's Cloudflare Access login, so the click was his. Afterwards I confirmed 29 articles in production and checked all 29 pages: each returned 200.
5. **Standing yes.** Jake: "Stop making me approve push main and stop making me deploy by myself... Just do it yourself from now on." From then on I fetched and rebased, ran the tests, pushed and ran `npx wrangler deploy` myself. I saved this as a memory and queued P-2026-10-18-01.
6. **Photos.** The handoff guessed the vision check was rejecting photos. The `/ops` picture gate records said otherwise: most of the 11 had `checked: []`, meaning Unsplash had returned nothing for long descriptions like "small business owner in shop counting money Kuala Lumpur". Telegram releases also skipped the photo step entirely ("released without a photo"). What I built:
   - up to 6 candidates
   - broader retries (the first 3, then the first 2 content words, then a generic scene for the section)
   - a photo check on release
   - an ops job `photos` that backfills published stories (English plus its Malay version) in each dataset that holds them
   I ran the job myself with `npx wrangler workflows trigger newsroom-ops '{"kind":"photos",...}'`, which needs no Access login. Result: 12 filled.
7. **Pexels was not issuing keys, so I used Openverse instead** (no key, 200 searches a day anonymously). I tested it with curl first. Its results lean towards politicians' events, so I kept only CC0, public domain and CC BY licences, used it only as a backup, and added to the photo prompt that posters, logos and political events are not relevant. The last two stories still failed, and the gate records showed why: every candidate had a person, because the searches asked for people. I fixed the meta prompt to ask for a place or object, with a scene retry for backfills. End state: 38 of 39 live stories have a photo.
8. Also did: a reminder task for Monday 20 Oct 10:00 (WhatsApp to Mr Saat, UN News email), click-by-click steps for Cloudflare Web Analytics and for scoring, and a reply appended to the website handoff file.

## What changed
- `9solarnews` main, my commits in this stretch: `84f1b19` through `2beaad8` (volume and publish fixes, pipeline 1.1.x to 1.3.0), `cdb63d8` (promote), `e4968fd`, `3e18969` and `0b9e40b` (photos). Final newsroom Worker version `a8729522`.
- Tests: about 286 at the start of the stretch, 301 at the end, all passing.
- Outside the repo:
  - D1 settings: `live-low`, `attributedNews` public, `minScore` 5, `storiesPerCycle` 8, cap US$100
  - Sanity production now holds 39 newsroom articles
  - the scheduled task `shine-saat-and-un-news-reminder`
  - memory `feedback-push-and-deploy-myself`

## Corrections and feedback from the user
- "You are prohibiting yourself. You are restricting yourself behind too many restrictions." I had treated outlets' terms of use as a hard stop. He was right that most of the strictness was caution, not safety. I still kept attribution and the fact-check.
- "What's the point?" This was about Release buttons on Telegram alerts that could never succeed, because the gate failures they reported could not be released. I now offer Release only where a release can work.
- "Stop making me approve push main... I've done it over 10 times." The per-push yes had stopped protecting anything and had become friction.
- "Can't we just bypass these rules... We are not going to get sued." I did not drop the credit line or the fact-check. I did move the legal tasks (UN News notice, written confirmation) off the critical path, as later tasks.

## My take
The biggest lesson: read the system's own records before trusting the explanation in a handoff. Both photo diagnoses were wrong (the vision check, then "few person-free stock photos"), and the gate records settled each one in a single query. The same thing happened with the holds on 16 to 17 Oct. Every fix that moved volume came from the hold reasons, not from loosening prompts blindly.

Jake's push for volume was the right business call. My early defaults would have shipped a beautiful empty newspaper. I'm less comfortable about where we are now. Attributed news rests on a verbal yes, and six high-risk stories went public on a single tick (Jake asked for "all"). One of them names Indonesian firms blamed for the haze. I flagged it, but I did not block it, and I think that was the right split of roles.

The standing yes on pushes conflicts with a seeded playbook rule. It has to be resolved in PLAYBOOK.md, not left to memory alone.

## What I'm satisfied with
- Running the backfill through the Workflow trigger instead of asking Jake to log in.
- Checking every live page after each change instead of sampling.
- Testing Openverse with curl, including its rate-limit headers, before writing code for it.

## What I'm not satisfied with
- Two backfilled photos are weak: a pump bottle for Ebola, a grayscale crowd for the Grand Mosque. Relevance is judged by a cheap vision call and it is lenient.
- I said "the curated library needs licence checks" and deferred it. That is right, but it leaves one story on the placeholder.
- Early on I wrongly told Jake that `minScore` was 6 when it had never been saved.

## Open threads
- Mr Saat: written confirmation and competitor names (reminder fires 20 Oct). UN News email. Domain choice, then SITE_URL, Turnstile and Access.
- Jake: Cloudflare Web Analytics snippet (I add it), Bitwarden, scoring on `/ops`.
- Consider `live-medium` around 1 Nov if there are 0 critical errors and 0 takedowns.
- `check-sources.py` reports `reference/sops/richpilot-crm-client-switch-on.md` as STALE. That is a Richpilot file, not touched here.

## Candidate playbook rules
- **Before acting on someone's diagnosis of a pipeline failure, query the system's own records (gate results, audit rows) for a few failing cases and fix what they show.** The photo handoff blamed the vision check, but the records showed the search returned nothing, and then that every photo had a person. Each was one query, and it changed the fix both times. (adopted)
- **When a client asks to loosen safety rules, keep the code defaults strict and expose each loosening as a named operator setting that is logged when flipped.** The tests stay meaningful, the change can be reversed in one click, and the audit trail shows who chose what. On Shine, flipping the defaults directly broke dozens of tests. Settings let Jake go live in minutes. (adopted)
- **Only show an action button (Release, Retry) where pressing it can succeed. Otherwise say why it can't and what would fix it.** Jake pressed Release on every Telegram alert, every one was refused, and he asked "What's the point?" (adopted)
- **Standing yes to push and deploy, per project** (P-2026-10-18-01, queued 18 Oct). (adopted, P-2026-10-18-01)
