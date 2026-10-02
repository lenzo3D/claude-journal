---
date: 2026-10-02
project: richpilot
topic: CRM core phase 2, data model, pipe and AI: 20-task build, final review, production rollout
outcome: shipped
satisfaction: 4/5
model: Claude Sonnet 5.5 (building), Claude Opus 5.5 (every review)
run: attended
related: [richmade]
---

# CRM core phase 2, data model, pipe and AI: 20-task build, final review, production rollout

Spans 1 to 2 Oct 2026, straight after the staff-accounts phase went live. The CRM tab and every screen (manual entry, CSV import, settings) are phase 3 and were out of scope.

## The ask
"Carry on with phase 2", then "Go ahead and build phase 2 instantly once the plan is ready", with the phase 1 rules still standing: Sonnet 5.5 builds, Opus 5.5 reviews, no approvals asked until everything is built, never push `main`, never touch production without his yes, no em dashes, commit as the lenzo3D noreply address.

At the end: "Lets do the production rollout now. Tell me the steps i need to take manually e.g. Vercel envs. However, you MUST do the things that you are able to do e.g. Supabase stuff, as ive connected the MCP and you need to do it yourself." Then: "Save the instructions on how to switch on and onboard a client. After this is done, wrap up and write a session journal."

## What I did
1. Wrote and pre-ran the phase 2 plan (20 tasks, plan commit `aa0024d`) in a scratch copy, then built in the worktree `~/Desktop/Agents/Richpilot-crm2` on `feature/crm-phase2`, with a ledger (`progress.md`), one brief file per task and a review diff per round. Staging (`dluscofjcdcptjhzuqec`) only; the Supabase connector can see production too, so the ledger carried a rule that the production project id is never used before the go.
2. Ran the phase 1 loop for Tasks 1 to 20: one Sonnet implementer per task, an Opus review of the committed diff, a fix round by resuming the same implementer, a scoped Opus re-review of each fix diff, and a live staging check by me or a Sonnet agent for the tasks that touch a database or a route. Every ruling went into the ledger, with the deferred minors.
3. Task 1 (schema) was the hardest: the SQL had never run before staging. Reviews drove three fix rounds (version bump from pipe writes, retention floor, composite foreign keys, undo predicate), each applied to staging as a patch file and re-checked live.
4. Task 15 (WhatsApp and voice hooks) split into three parallel Opus reviews because it touches the live webhook. They found hooks sitting in the customer-facing path, bursts for never-sync senders, Twilio's anonymous-caller placeholder numbers becoming one shared contact, and a handover hook registered after `deliver()` (which can throw). Two fix rounds, then a live staging run.
5. Task 16 (the five-minute sweep) took three rounds. The first review found the sweep bumped `orders.updated_at`, which is the order desk's optimistic-lock version, so staff Confirm would fail after the sweep linked an order, plus endless re-work loops and a retry budget that any outage could burn. The fix needed two new `crm_bursts` columns and a redefined orders trigger inside the still-unreleased migration, applied to staging by me from a patch file.
6. Task 17 (history build) had one Critical: an old confirmed order could attach to a contact's current open deal, including a staff-made one, and move it to Won with no undo. Fixed with a pure deal-attach rule; a re-review then found a new endless-re-work bug in the same rule, fixed in a small second round. Live check passed nine checks, including a full-row snapshot diff proving the second press wrote nothing.
7. Tasks 18 and 19 (chat-header chip, docs) were quick. The chip review found `conversations.updated_at` does not move when the CRM changes a deal, so the chip refreshes on a poll tick instead.
8. Task 20: a Sonnet agent ran all 11 plan checks plus extras (voice callback, orders trigger, backoff, browser) on two throwaway clients. It found the chat header overflowing at 375 px.
9. Final whole-branch review in three parallel Opus slices (tenancy and auth, AI and money rules, migration and rollout), one fix wave of nine commits, a scoped re-review, then a last small fix after that re-review found the purge script could delete another person's chats across clients when given a local-format number.
10. Re-ran the final `0028` file on staging as one script (a Sonnet agent, with a rolled-back smoke test). It found the usage view still had write grants for the public roles, which I fixed in the file and on staging.
11. Rollout, after Jake's go: re-fetched `origin/main` (unchanged, `0028` free), ran read-only checks on production (Postgres 17.6, `pg_trgm` absent, 2 clients, no odd modules), created `pg_trgm` in the `extensions` schema, applied the whole `0028` as one script through the connector, and verified tables, grants, function ACLs, columns and untouched row counts. Jake pushed `main`; I checked the deploy from outside.
12. Wrote `docs/crm-client-switch-on.md` (branch `docs/crm-switch-on-sop`, commit `af36062`, not pushed) and copied it to `reference/sops/richpilot-crm-client-switch-on.md` here, registered in `reference/sources.json`.

## What changed
- Repo `lenzo3D/richpilot`, `main` now at `2a0c109` (fast-forward from `b9aac41`, 61 commits, 90 files, about 14,800 lines): `src/crm/*` (pipe, sweep, history build, AI prompts and rules, store and writes), `/api/cron/crm`, `/api/admin/clients/[slug]/crm-history`, `/api/conversations/[id]/crm`, `CrmChip`, call rows and order card, `.github/workflows/crm-sweep.yml` (its own workflow), README and handoff CRM sections, `scripts/purge-data.mjs` (erases the CRM contact, international form only).
- Production database: `pg_trgm` created in `extensions`, then `0028_crm_core.sql` applied (13 tables with row level security, 6 service-role-only functions, 1 view, 2 replaced functions). Existing data unchanged (2 clients, 3 conversations, 68 messages, 0 orders, 0 calls). No client has the CRM switched on yet.
- Tests: 400 before, 602 after, all passing; `tsc`, lint and build clean at every checkpoint.
- Not pushed: `docs/crm-switch-on-sop` in the Richpilot repo.
- Cost of the live staging checks that recorded their spend: a few cents of model usage in total.

## Corrections and feedback from the user
- "you MUST do the things that you are able to do e.g. Supabase stuff, as ive connected the MCP": my final report listed "paste `0028` into the production SQL editor" as Jake's step, the same mistake he corrected in phase 1 ("Do it yourself and only hand me the ACTUAL manual tasks"). I had carried the plan's wording ("Jake applies 0028") instead of the standing correction. After his yes I applied it myself and handed him only the Vercel check and the `main` push.
- "check on the planner's progress, it seems to have stalled" (while the plan was being written): I was waiting on the planner agent without telling him it had gone quiet. The plan did land and the build went ahead; the exact recovery steps were lost when the context was compacted, so I cannot record them.

## My take
The method held up for a second long build, and the strongest argument for it is still that every review round found something real. What changed this time is where the worst bugs lived. The per-task reviews were good at local correctness, but the nastiest problems were between tasks: text from the platform's other models (a handover reason, a voice note, an order description) reached CRM records without price redaction even though every CRM prompt was guarded; the CRM's spend check reserved only its own call, so after a cap reset it could have pushed the global hourly breaker and handed every client's customers to a person; the documented switch-on order would have synced staff before the never-sync list was filled in; and sender emails could merge different customers. None of those was inside one task. The sliced whole-branch review is what found them, and it is cheap compared with what they would have cost in production.

Two review habits paid off again. Re-reviewing fix rounds caught a new endless-re-work bug in Task 17's own fix, and the earlier-phase lesson held: fixes are where new bugs enter. And the reviewers' sharpest point was that "press twice adds 0 rows" looked green while a bug redid seven round trips per order on every press; I only trust idempotency checks now that diff every row and count writes, as the Task 17 live check did.

I would push back on one thing in how the plan was written: it assumed `conversations.updated_at` moves on CRM changes, assumed the orders trigger bumps were harmless, and had the sweep inside the email-ingest workflow. Each cost a review round. The plan was pre-run for compile errors but not for the product assumptions behind it.

Risk ahead: the final `0028` file has still never run from scratch on a fresh database. Staging got version 1 plus patches, and I re-ran the whole file on it afterwards, which is strong but not the same. Production got the file as one script, which worked, and nothing depended on the old schema, so the risk is now low.

## What I'm satisfied with
- Never acting past the gate. Production work started only after Jake's explicit go, I re-fetched `origin/main` right before touching it, and I stopped for the `main` push because that is his.
- Verifying from outside after the push: the new route went 404 to 401, login and `/admin` behaved as before, and the production database counts were unchanged.
- Live checks by someone other than the implementer, with a full-row snapshot diff for the history build and a rolled-back smoke test for the migration. The smoke test found a real gap (write grants on the usage view) that no review had.
- The ledger. About 140 lines of rulings, carries and accepted risks meant a context compaction in the middle cost almost nothing.

## What I'm not satisfied with
- Repeating the phase 1 mistake of handing Jake a step I could do. The standing correction was in the journal, not in front of me when I wrote the rollout list.
- Reviewer agents stalled many times ("no progress for 600s") after delivering their reports. I handled it by asking for incremental findings files, but it cost time.
- The deadline cursor for the history build and a short-retention delete were never exercised for real (the budget is a hardcoded constant), and the documented behaviour for them rests on reading the code.
- I did not test the phone-width fix in a browser after the final wave; it was verified by the earlier live DOM edit only.
- The standalone switch-on checklist has not been walked end to end by anyone yet; the first real client will be its test.

## Open threads
- Jake: check the GitHub Actions "CRM sweep" runs are green (HTTP 200, empty results while no client is on the CRM). A 401 means the Vercel and GitHub `CRON_SECRET` values differ.
- Jake: push `docs/crm-switch-on-sop` (the checklist) with the next merge, or ask me to put it on `main`'s path another way.
- Decide which client switches on first, whether to build their history, and agree their retention. Their staff phones and forwarding emails must go in `crm_never_sync` by SQL first.
- Phase 3: the CRM tab, settings screens (including a never-sync editor), delete-person that also removes bursts, a `crm_touched_at` column so the chip needs no polling, and passing only the session's own staff id into the `decided_by`, `undone_by`, `actor_user_id` and `created_by_user_id` columns.
- Optional: run `0028` from scratch on a throwaway Postgres (a Supabase branch costs money, so it is Jake's call).
- Accepted risks, all in the ledger: price filter edge cases, contacts from history looking recently active, `closed_at` on old wins, dismissed merge suggestions recurring, a "will retry" alert hiding the final "abandoned" one, non-CRM client retention starved in a busy sweep, staff-made Call back tasks not deduplicating AI ones.

## Candidate playbook rules
- **When Jake has connected a tool (a database connector, a deploy tool) and given the yes for a step, do every step you can do with it yourself, and hand him only what only he can do (Vercel or GitHub settings, the push to `main`).** Never write "Jake applies the migration" into a rollout list when the connector can. He corrected this in two consecutive phases ("Do it yourself and only hand me the ACTUAL manual tasks", then "you MUST do the things that you are able to do"). (adopted, P-2026-10-02-01)
- **For a multi-task build, finish with a whole-branch review split into parallel slices by concern (tenant isolation and auth; AI, money and privacy rules; migration, rollout order and regressions), on the strongest model, after the per-task reviews.** Per-task reviews missed four cross-task problems on Richpilot phase 2 (unredacted text from other models, a spend reserve that could pause every client's replies, a switch-on order that synced staff, sender emails merging customers). (adopted, P-2026-10-02-02)
- **Before applying a migration to production that was developed with patches on staging, re-run the final file in full on staging, then check row level security, grants and function ACLs, and run a smoke test inside a transaction you roll back.** The staging schema is a product of the original run plus patches, not of the file production will run; the re-run found write grants left on a view. (adopted, P-2026-10-02-03)
