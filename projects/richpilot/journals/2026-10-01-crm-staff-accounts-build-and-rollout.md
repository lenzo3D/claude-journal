---
date: 2026-10-01
project: richpilot
topic: CRM core phase 1, named staff accounts: build, three reviews, production rollout
outcome: shipped
satisfaction: 4/5
model: Claude Sonnet 5.5 (building), Claude Opus 5.5 (every review)
run: attended
related: [richmade]
---

# CRM core phase 1, named staff accounts: build, three reviews, production rollout

Spans 29 Sep to 1 Oct 2026. The session started as "Tasks 1 to 5, then stop for my review" and grew into the whole plan and the production rollout as Jake widened the scope message by message.

## The ask
First message: build CRM core phase 1 in `~/Desktop/Agents/Richpilot` from `.superpowers/sdd/2026-09-29-crm-staff-accounts/handoff.md` and the plan it points to, using subagent-driven development, Tasks 1 to 5, then stop. Model split set by Jake: "Sonnet 5.5 for main building, and only use advanced models like Opus 5.5 for deep thinking and code review."

Later, in his words: "continue with task 9 and beyond by yourself, and continue with subagent code review after each task. don't ask me for any approvals or requests until all tasks are done", then "Run an Opus 5.5 subagent to do the full review of the whole thing, and then autonomously debug the fixes it found", then "You have full access to the supabase mcp ... Do it yourself and only hand me the ACTUAL manual tasks", and finally "verify the push to main and production ... only after it is completed, run a full session journal."

Constraints that held throughout: never push `main`, never apply anything to production without his yes, staging database only until rollout, no em dashes, commit as the repo's configured author.

## What I did
1. Read the handoff and plan, created `feature/crm-staff-accounts` from `main` and merged `specs/crm-core`. Wrote a pre-flight conflict table into the ledger (`progress.md`) before dispatching anything.
2. Ran the per-task loop for Tasks 1 to 14: brief file per task, one Sonnet implementer, one Opus reviewer given the diff as a file, a resumed implementer for fixes, a scoped Opus re-review of each fix diff. Ledger line after every step, including every ruling.
3. Tasks 1 to 5 (schema, passwords and tokens, permission table, cookies and session resolution, staff rules and emails) were pure code. Task 2's reviewer found the password verifier threw on a malformed stored hash and answered in 0.1 ms versus 30 ms for a missing account (a timing leak). Fixed in a second pass.
4. The migration could not be applied by an agent at that point, so I handed Jake copy-paste blocks for the staging SQL editor. One of mine ("pbcopy < file") was a Terminal command that I told him to paste into the SQL editor. He got a syntax error. After that I ran `pbcopy` myself and gave him only SQL.
5. Jake then connected the Supabase MCP. It could see production and a third project, so I wrote a ledger rule that only the staging project id may ever be used until rollout. Task 6's live check needed a write to staging (flip `shared_password_enabled`); the auto-mode classifier denied it, I did not work around it, Jake said go ahead, and I ran it.
6. The main checkout was switched to another branch by a different session partway through, so I built in a git worktree (`~/Desktop/Agents/Richpilot-crm`, `node_modules` cloned, ledger copied).
7. Live staging checks for Tasks 6, 8, 10, 11, 12, 14 were done by me, not the implementers, with throwaway accounts that I deleted afterwards. I minted a signed cookie with the app's own code instead of needing a client password. Task 11's browser check only worked on a production build, because `next dev` on `127.0.0.1` blocks hydration (`allowedDevOrigins`), so form submits did nothing.
8. A first whole-branch Opus review found two blockers I confirmed myself: `main` had moved (our `0024_staff_accounts.sql` clashed by number with main's `0024_call_messages.sql`) and deploying the code before the migration would break WhatsApp ingest, orders and `/admin`. That agent stalled after delivering its report, so I used the report as it stood.
9. At Jake's request: a second, fresh, full Opus review (0 Critical, 2 Important, 7 Minor), one fix dispatch, a scoped re-review, live verification on staging. Then the `requesting-code-review` pass: a third review found Richmade could not remove a client's last Admin, and my fix for that created a new hole (a null session was treated as Richmade). A fourth scoped re-review caught it and the fix was made explicit at the route.
10. Rollout: read-only probes of production, applied `0027_staff_accounts.sql` through the MCP after Jake fixed the permission setting, verified, handed Jake the Vercel variables and the push. The first push was rejected because `main` moved again. I merged `origin/main`, Jake pushed `b9aac41`, I verified the deploy from outside and then verified his account in the database.

## What changed
- Repo `lenzo3D/richpilot`, now on `main` at `b9aac41`: 31 non-merge commits on the branch (3 spec and plan, about 28 build and fix). New `src/lib/staff/*`, sign-in routes and pages, `/team`, staff lists on `/admin`, `author_user_id` on messages and order events, `staff:invite` script, docs.
- Migration `0027_staff_accounts.sql`: applied to staging under the old number `0024` (plus a hand-applied `staff_apply_change` patch) and to production as written, one transaction with `lock_timeout = '5s'`.
- Production verified: tables and columns present, only the new 8-argument `apply_order_change`, both clients keep their shared password on, 68 messages untouched. Jake's `agency` account `jake@richmade.app` exists, password set, first sign-in two minutes after the invite.
- Vercel: `APP_URL` and `AUTH_EMAIL_FROM` set by Jake, `RESEND_API_KEY` already present.
- Tests: 299 before, 400 after. `tsc`, lint and build clean at every checkpoint.
- Claude-journal: checkpoint line for the push (`980a0eb`) and this entry.

## Corrections and feedback from the user
- "don't ask me for any approvals or requests until all tasks are done": I had been stopping at the end of each task to report. I switched to continuous execution with rulings logged in the ledger and everything surfaced in one final list.
- "Do it yourself and only hand me the ACTUAL manual tasks": I had listed seven production steps including ones I could do. After the setting was fixed I applied the migration myself. Vercel variables and the `main` push stayed with him because I have no access.
- "do i actually put '<a sender on a Resend-verified domain>' in the env value": my instruction used a placeholder in angle brackets that read as literal text. I should write the shape of the value with a concrete example and say what to look up.
- "it asks me to use a work email and it says its incorrect": the first-ever sign-in needs the emergency password form, which is behind a small "Use a shared company password" link. My docs and my message said "sign in with the shared-password link" without describing the toggle. The UI is correct, my hand-off was thin.

## My take
The method worked: briefs as files, fresh implementers, reviewers on the strongest model, a ledger that survived long gaps. Every review pass produced real findings that the previous pass missed, which is the strongest argument for repeated independent review on auth code. The first review of a task was usually clean on spec and noisy on named risks (timing leaks, races, fail-open defaults), and almost all of those came from the plan's own pre-run code. Pre-running a plan removes compile and lint surprises but not design flaws.

The most valuable single catch was the third review's null-actor hole, because I had introduced it one commit earlier while fixing a different review finding. Fixing review findings is where new bugs enter. Jake's earlier playbook rule (re-review every fix round) paid for itself again here.

Where I'd push back: the plan wired the rate limit, the staff routes and the session reads so that React `cache` quietly did nothing in route handlers (2 to 3 session lookups per API call). It fails closed, but the whole design assumed otherwise, and two bugs (permission gate role race, null actor race) came from it. Phase 2 should resolve access once per request before building more on it.

The migration numbering problem is a process smell, not bad luck: a long-lived feature branch plus a fast-moving `main` plus numbered migrations clashes every time. It clashed twice during rollout.

## What I'm satisfied with
- Never acting past the gate. When the classifier refused a staging write and later a production write, I stopped, said so, and waited for Jake to change the setting. Nothing was worked around.
- Verifying from outside: after the deploy I curled the signed-out surface, then queried production for the account Jake created. "Email arrived" alone would not have shown the password was set or that sign-in worked.
- Live proofs on staging for the rules that matter (removal signs out on next request, lockout expires, removal spends unused links, Richmade can remove the last Admin, client Admin cannot).
- Keeping the ledger honest: ~16 explicit rulings, every deferred minor, the places where I deviated from the plan's code and why.

## What I'm not satisfied with
- I told Jake to paste a Terminal command into the SQL editor.
- My first draft of the README upgrade note said the emergency login would break if the code deployed before the migration. A reviewer proved that false (only shared-password clients, WhatsApp ingest and orders break). I had written the claim without tracing it.
- I probed production for a `call_messages` table that does not exist (migration 0024 only adds columns to `calls`) and briefly concluded a migration was missing. I read the migration before acting, but the wrong assumption cost a round-trip.
- Gave rollout steps before re-fetching `origin/main`. It had moved, and the push was rejected. I should fetch immediately before handing over a push command.
- The invite email path and forgot-password email were not testable on staging (no Resend key available to me), so the first real delivery test was in production, by Jake.
- The first whole-branch review agent stalled for 10 minutes after delivering its report. I used the report but did not recover the findings file.

## Open threads
- Jake: rotate `DASHBOARD_PASSWORD` in Vercel to a long random value (he set a temporary plain one to get in), save it in a password manager, redeploy.
- Jake: invite any other Richmade staff from `/admin`.
- Do not switch any client's shared password off until that client's Admin has set a password (per-client step in the README "Staff accounts" section). Leisure Frontier's staff will see a banner meanwhile.
- Decisions left open: signed expiry on user cookies; shared-password rotation does not kill already-issued shared cookies; no cap on invite emails per client; a removed person's email is reserved platform-wide (needs a Richmade move/delete tool); shelved HubSpot docs still on the branch and on `main`; narrow the Supabase connector to staging; `main` migration numbers 0024 to 0027 must be applied in order on any other database.
- Phase 2 plan (data model, the pipe, the AI) is next and should resolve access once per request.

## Candidate playbook rules
- **Immediately before handing Jake a production rollout (migration or push command), re-fetch `origin/main` and re-check migration numbers and what production already has, read-only.** `main` moved twice during this rollout, which renumbered the migration twice and made the first push fail. (adopted, P-2026-10-01-01)
- **Write a migration to be safe before the code that uses it: additive, new arguments defaulted, one transaction with a lock timeout, and state the apply order (migration, then environment variables, then deploy, then first account) in the runbook, including what breaks if the order is reversed.** The staff-accounts migration could be applied to production with the old code still running, which is why the rollout had no downtime window. (adopted, P-2026-10-01-02)
- Not proposed: "re-review every fix round on security code" is already in the playbook. This session is a third piece of evidence for it (a fix for one review finding introduced a null-actor hole that the next scoped re-review caught).
