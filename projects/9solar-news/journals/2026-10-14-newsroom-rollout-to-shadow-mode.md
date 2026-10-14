---
date: 2026-10-14
project: 9solar-news
topic: Newsroom rollout from deposit to shadow mode
outcome: shipped
satisfaction: 3/5
model: Claude Opus 5.5
run: attended
related: []
---

# Newsroom rollout from deposit to shadow mode

## The ask
On 14 Oct 2026 the client's deposit was credited, and Jake asked: "lets begin finalising the build before we ship. Tell me the steps using the built-up knowledge and skills. Refer to the claude journal." The work ran from 06:07 to about 16:10 UTC (14:07 SGT to 00:10 SGT on 15 Oct). It ended with the newsroom running in shadow mode, plus a saved 14-day plan and this wrap-up.

Standing constraints from the build session still applied: no em dashes, no fabrication, commit as lenzo3D, never push `main` without Jake's yes for that push, and the golden run only with his yes and his key.

Context note: this conversation was compacted once before 14 Oct. The 7 to 13 Oct work (the 16-task newsroom build, two review waves, the source-terms research, the cost model, the roadmap and pricing) was never journaled, and `projects/9solar-news/journals/` was empty until this entry. The SOP copies in `reference/sops/9solar-news-*` are the only record of that work here.

## What I did
1. Read the setup checklist SOP and checked the repo. `origin/main` was 32 commits ahead of `build/autonomous-newsroom`: another session had pushed a three-design compare build on 8 Oct, including a "Green Energy" nav section with a solar glossary, and an "AI-assisted, human-edited" byline badge on every article. Both contradicted standing decisions (no visible solar promotion, no human editor on each story), and a trial merge showed 12 conflicts. I put three questions to Jake: (a) keep the switcher, (b) drop Green Energy, (c) new badge wording.
2. Merged `main` into the branch by hand (`dcfaf32`). A hunk-picker script handled the mechanical sides. I wired the newsroom's correction notes, transparency panel and report link into all three article variants, and limited the badge to `aiGenerated` stories. Adapting the How We Work contrast test to the per-design token files caught a real defect: Studio links at 2.46:1.
3. Removed Green Energy (`5e351f0`): sections, nav, home bands, the glossary card, the virtual route and the tokens. Then I retargeted the browser checks. The fixture build caught duplicate `how-made-h` ids, because the panel now renders once per design. A headless contrast probe found Studio's panel and correction notes at 1.14:1, which I fixed and turned into a permanent check.
4. Cloudflare: Jake had already logged in, upgraded to Workers Paid and created D1 and R2. I created KV and filled in the ids. The auto-mode classifier blocked the remote migration and the dry-run deploy, so Jake ran those.
5. A read-only check found the live site Worker on a **different Cloudflare account** ("cygnisloh") from the one holding every new resource ("richmade-app"). Jake chose to consolidate on the Richmade account. The new site Worker needed the root `wrangler.jsonc`, which existed only on the branch, so the push to `main` moved early (`39931ef`, with Jake's yes).
6. The preview build failed with 276 broken links: `staging` is a private dataset, and the build reads Sanity without a token. I added an optional `SANITY_READ_TOKEN` (`182bf4a`, pushed with his yes), and Jake added it as a build Secret. Locking the preview took two tries, because the Cloudflare menus didn't match my instructions.
7. The newsroom deploy. I had Jake turn the kill switch on first, by D1 `INSERT`, after confirming in `src/llm/gateway.ts` that `killed` refuses every LLM call. Then came secrets (three rounds: blanks, then a missing Sanity write token he didn't know he needed), deploy, Telegram webhook, Access for `/ops`, Turnstile and the report endpoint.
8. Telegram `setWebhook` rejected the password-manager secret, which contained characters outside `A-Za-z0-9_-`. I then read his terminal while the regenerated `openssl` secret was on screen, which exposed it in the transcript. We regenerated it a third time via `openssl rand -hex 32 | pbcopy`, unseen.
9. I read the Access AUD tag from the `kid=` in the unauthenticated 302, instead of sending Jake to hunt for it. The `/ops` refusal turned out to be Access policy, not code: a session from the preview login didn't match the ops policy.
10. A reader-report test saved the report, but no Telegram alert arrived. Using `wrangler tail`, I found `TypeError: Illegal invocation`: `TelegramNotifier` and `SanityHttp` stored the global `fetch` as `this.fetchFn` and called it as a method, which Workers reject. Every Sanity publish would have failed too. I wrote a red-first test with a fetch stub enforcing the runtime's `this` rule, then the fix (`d195028`). The third report produced the alert.
11. Golden run: four attempts returned 401 "invalid x-api-key". The causes were a garbled paste into a hidden `read -s` prompt, then commands run from the chat box (each in a fresh shell, so the exported key was gone), then a clipboard overwritten by the previous output. A clipboard read guarded by an `sk-ant-` prefix check fixed it.
12. The first real run held all 15 clean drafts. The golden fixtures padded clean drafts to the 250-word minimum with 34 uncited filler sentences: the code gates allow them, because they contain no fact tokens, but the live Verifier rightly rejected them. That also meant the four Verifier-only faulty cases had never been tested in isolation. I rewrote the topics with enough written test evidence for 264 to 279 word drafts in which every sentence cites a passage (`7acd733`). Rerun: 0 bad drafts missed, 0 clean drafts held.
13. Jake sent `/resume`, and I confirmed `killed=false` in D1. I wrote the 14-day plan, `AI Agency/9solar-news-shadow-mode-plan.md`, and opened it in the file pane.

## What changed
- 9SolarNewsWebsite, pushed to `main` in three pushes (37b6d24..39931ef..182bf4a..d195028..7acd733):
  - `dcfaf32` merge; `5e351f0` Green Energy removal and panel fixes; `39931ef` real D1 and KV ids
  - `182bf4a` site read token; `4f49a19` and `c537dcc` newsroom site URL, Access team domain and AUD
  - `d195028` fetch binding fix plus `test/ops/fetch-binding.test.ts`; `7acd733` golden fixtures
- Tests: web 298 to 297 (Green Energy tests removed, one read-token test added), plus newsroom 241 to 243. All browser checks pass except the pre-existing Shorts `loops-forward-to-first` flake. Golden live result: 0 missed, 0 clean held.
- Outside the repo:
  - Cloudflare (Richmade account): Workers `9solarnews`, `9solarnews-preview` and `newsroom`, with D1 `newsroom` (3 migrations), R2 `newsroom-evidence` and KV `EDGE`
  - Access apps for the preview site and `/ops`, a new Turnstile widget, and deploy hooks
  - 8 newsroom secrets, the Telegram webhook, and the Sanity `staging` seed (119 documents)
  - Anthropic spend: about US$6 across two real golden runs
  - Live site: `https://9solarnews.richmade-app.workers.dev`
- Journal: checkpoints for each push, and `reference/sops/9solar-news-shadow-mode-plan.md`.

## Corrections and feedback from the user
- On the overall experience: "this whole process has been incredibily tedious." He asked for statistics and improvements: 8 h 25 min elapsed, about 47 min of my active work, and the rest waiting on manual steps.
- "wtf is a sanity write token when have i ever generated this": the setup checklist listed it in step A1.3, but I never re-surfaced it before asking for it. Re-state what each secret is and where it comes from at the moment you ask for it.
- "why do i have to lock a preview site and whats the point of the preview site": I had given instructions without the purpose. Explaining shadow mode and POFMA exposure settled it.
- "idk how to view AUD" and "there is no domains & routes in settings": dashboard paths I gave from memory were wrong. Reading values from the system (the 302's `kid`) beat giving directions.

## My take
The engineering held up. Every serious defect was found before shadow mode, not after: the Studio contrast, the duplicate ids, the fetch bug and the golden padding. The fetch bug is the one I'm most uneasy about. 243 passing tests and a whole-branch Opus review had all missed that publishing to Sanity could never work on the real runtime, because every test injected a fake fetch. The runtime found it in the first minute of real traffic.

The process was poor, and most of the cost is mine. Three of the day's detours (two Cloudflare accounts, a private staging dataset, a Turnstile widget on the old account) were findable with two minutes of read-only checks before Jake clicked anything. I found each only when it broke. The secrets handling was worse: I asked Jake to paste values into interactive prompts several times, which produced blanks, a garbled key and a clipboard mix-up. I also leaked one secret into the transcript myself by reading a terminal. Piping from the clipboard with a prefix check should have been the method from the first secret.

Jake's call to consolidate on the Richmade account was right. So was dropping Green Energy rather than renaming it. The design switcher on the public site is the main loose end: Mr Saat has to pick a design and a name before `live-low`.

One risk I'd flag for shadow mode: `/ops/shadow` needs 100 scored stories with fewer than 2% carrying a minor issue. Two minor notes in 100 fails it. Jake may be tempted to under-score to pass. The plan tells him to raise it instead.

## What I'm satisfied with
- Using `wrangler tail` plus one real report to turn "the bot didn't message me" into an exact stack trace in two steps.
- Turning the kill switch on before the first deploy, after checking in code that it blocks LLM calls and not just publishing. The newsroom went live with zero spend risk while the key was still broken.
- The golden rewrite: clean drafts that the live Verifier passes, which now actually test the four Verifier-only faults.

## What I'm not satisfied with
- No preflight. This should have been step 1 on any rollout: check the signed-in account against the live resources, and check each dataset's privacy against how the builds read it.
- Secrets went through interactive paste for most of the day. I exposed one by reading a terminal.
- Dashboard instructions written from memory sent Jake hunting twice.

## Open threads
- 15 Oct, 07:00 SGT: the first shadow cycle, and the first live Sanity write and preview rebuild. Go through `/ops` with Jake afterwards.
- Jake's 14-day plan: daily scoring, aiming for 100 scored stories.
- Decisions before `live-low`, the earliest being 29 Oct:
  - publisher of record, and the design and name pick (then remove the switcher)
  - a real contact email, the IMDA check, a Malay reviewer (including the new badge wording) and analytics
  - a real domain, and the NASA terms note in `/ops/sources`
- Delete the old cygnisloh Worker and Turnstile widget.
- Build an API-token provisioning script with a 1Password secrets loader for the next client.
- Unrelated, flagged by `check-sources.py`: `reference/sops/richpilot-crm-client-switch-on.md` is STALE against Richpilot `0d6638d`.
- The `newsroom` Worker has workers.dev Preview URLs enabled by default. `/ops` checks Access in code, so this is harmless, but `preview_urls: false` is tidier.

## Candidate playbook rules
- **Before the first provisioning or deploy step on any client rollout, run a read-only preflight and fix what it finds before asking the human to click anything.** The preflight compares the signed-in cloud account with the account hosting the live site and every existing resource (Workers, widgets, domains), and checks each data store's visibility against how the builds read it. On 9 Solar News, an account mismatch, a private dataset the preview build couldn't read, and a Turnstile widget on the old account each surfaced only after failing, and each cost Jake a detour. (adopted)
- **Move secrets by pipe, never by interactive paste: copy the value, then `pbpaste | tr -d '[:space:]' | <tool> secret put NAME` (or a password-manager CLI). Check a key's prefix and length without printing it, and never read a terminal that may be showing a secret.** On 14 Oct, interactive prompts produced blank secrets, a garbled API key behind four failed golden runs, and a clipboard overwritten by output. Reading a terminal leaked a webhook secret into the transcript. (adopted)
- **When a test injects a fake for a platform API (fetch, storage, queues), make the fake enforce the platform's rules, and exercise each outbound integration once against the real runtime (with live logs) before switching anything on.** 243 newsroom tests passed with fakes that ignored `this`, while on Workers both Telegram alerts and every Sanity publish threw "Illegal invocation". One real reader report, plus `wrangler tail`, found it. (adopted)
