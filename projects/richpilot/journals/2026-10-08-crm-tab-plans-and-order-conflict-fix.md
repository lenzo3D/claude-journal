---
date: 2026-10-08
project: richpilot
topic: CRM tab spec and pre-run plans, the PostgREST 40001 hang, and the order desk conflict fix
outcome: shipped
satisfaction: 4/5
model: Claude Opus 5.5
run: attended
related: []
---

# CRM tab spec and pre-run plans, the PostgREST 40001 hang, and the order desk conflict fix

Covers 4 to 8 Oct 2026 in one long session (with context compactions; details from before the last compaction come from the summary and the commits). Earlier in the same session, on 3 Oct, I wrote the design-system build handoff; that build is journaled in `2026-10-03-design-system-build-and-rollout.md`.

## The ask

Jake handed me a handoff written by the CRM phase 2 builder (`.superpowers/sdd/2026-10-04-crm-phase3/handoff.md`): write the spec and implementation plans for CRM phase 3, the CRM tab, in his plan format (Review Focus, pre-run code pasted by script), then stop and write a handoff for the builder session. "Implement this handoff and tell me the next steps." Later, mid-way: "Do this task here" for the order desk fix I had flagged, then "push and merge the order desk fix", then "apply 0030 to production", then "wrap up and do all the cleanup except crm-demo".

## What I did

1. Brainstorming skill, architectural path. Read the core CRM spec, roadmap and design spec myself; sent two Explore subagents for the phase 2 ledger (every deferred carry item) and an exact inventory of `src/crm/*`, the shell and the tests. Checked production read-only: 0029 applied, zero CRM rows anywhere, so every live check would need seeded staging data.
2. Four product questions, one at a time, each with a recommendation; Jake took every recommendation: three plans work-first (3a see and work the AI's output, 3b create and edit, 3c admin and compliance), Richmade's client picker inside the CRM only (`?client=<slug>`), a Lost reason pick list plus Other, and deleting a person also deletes companies nobody else uses. Two technical choices (live isolation script plus a guard test; client screens over JSON routes) I presented as section 1. Jake then said "do all the sections in one pass then ill do a review only at the end", so I wrote the whole spec at once (saved as a memory). He approved it.
3. Pre-ran plan 3a in a scratch worktree (`scratch/crm-tab-prerun`), one Opus subagent per task from a shared `common.md` brief plus a per-task brief, with "From Task N" notes appended as tasks finished. I gated every commit myself (tests, `next typegen` + tsc, lint), applied each migration to staging through the Supabase connector, ran the isolation check, and looked at screens in the browser pane. 15 tasks, 689 to 870 tests, the isolation check grew to 207 cases.
4. Task 3's subagent reported that a stale-version refusal hung. I reproduced it: `crm_patch_record` with a stale version took 125,323 ms and returned "upstream request timeout" with no code, while P0002 came back in 917 ms. PostgREST retries SQLSTATE 40001. Every CRM refusal and the order desk's `apply_order_change` raised 40001, all live in production. I folded a PT409 fix into Tasks 1 and 2 by interactive rebase, re-applied on staging: 126 ms. The order desk I flagged as a separate task chip.
5. Jake chose "Do this task here" for the order fix. Found a second victim, `commit_order_email`: the mailbox reader got a code-less timeout, did not count it as transient, and would park an email after three. Wrote `0030_order_conflicts.sql` (a diff against 0027 and 0017 shows only the errcode changed), a pure `conflict.ts` accepting both codes, measured 125 s before and 118 ms after on staging. That took 0030, so I renumbered the CRM migrations to 0031 to 0033 with `git filter-branch`. My first filter used a loose pattern that would also have changed numbers in the voice code; it failed on BSD `xargs -r` before rewriting anything, and the second run was scoped to CRM files.
6. Wrote a plan generator (`gen_plan3.py`) and a rebuild check (`verify_plan3.py`). Plan 3a: 19,785 lines, all 15 tasks rebuilt from the plan text identical to the pre-run commits. Committed on `specs/crm-tab`. Moved the "apply to staging" step after the step that writes the migration (it was first, before the file existed).
7. Plan 3b: Tasks 1 to 4 pre-run (migration 0032 applied to staging by a subagent restricted to the staging project, 910 tests, 319 isolation cases). Task 5's subagent died on the weekly usage limit.
8. Jake continued in a cloud session, which built 3a and 3b for real on top of my scratch branch, merged them, got 0031 and 0032 onto production (part by Jake in the dashboard SQL editor, because the connector hung on function bodies with `delete`), and moved the functions to Tokyo with two shared caches. Another session is now building 3c. When Jake asked me to check its progress, I read the repo's own session journal on `main`, updated memory and marked this session complete.
9. Order fix rollout: rebased onto `main` 88e6bff, 957 tests, build clean, pushed the branch. `gh` is not installed, and my fast-forward push to `main` was blocked by the permission classifier ("merge without review"), so Jake fast-forwarded `main` himself. I could not confirm the Vercel deploy (needs sign-in; the app shows its build only to signed-in sessions), reasoned that applying 0030 first is never worse than today, and applied it to production after his yes. Checked: both functions raise PT409, service_role only.
10. Wrap-up: lesson L-018 and a repo journal entry on a new branch `docs/order-conflict-lesson` (with the spec renumber, which had never reached `main`), removed six worktrees and the merged branches, refreshed the stale switch-on checklist copy here.

## What changed

- Richpilot `main`: `70c7b2a` (order conflicts answer at once, migration 0030). Earlier, via the cloud session, the CRM tab 3a and 3b built from this session's pre-run.
- Branch `docs/order-conflict-lesson` (pushed, not merged): spec renumber `2343263`, lesson L-018 and journal entry `037b926`.
- Supabase: 0031 and 0032 applied to staging by me; 0030 applied to staging and production by me (production after Jake's yes).
- Deleted: worktrees `Richpilot-crm3-prerun`, `-orderfix`, `-crm-tab`, `-prerun`, `-design`, `-wrapup`; local and remote branches `scratch/crm-tab-prerun`, `specs/crm-tab`, `fix/order-conflict-fast`, plus local `scratch/design-prerun`, `specs/design-system`. Kept: the staging client `crm-demo` (the 3c session uses it).
- `.claude/launch.json` in AI Agency: removed `richpilot-prerun` and `richpilot-crm3`.
- claude-journal: refreshed `reference/sops/richpilot-crm-client-switch-on.md` to fb79901.

## Corrections and feedback from the user

- "do all the sections in one pass then ill do a review only at the end": I had presented the design section by section per the brainstorming skill. Saved as memory `feedback-whole-design-one-pass`.
- Standing rules a later session recorded in Richpilot's `AGENTS.md`: never ask the owner to run SQL; apply migrations yourself, production only after a specific yes. My rollout messages here already followed that.

## My take

The pre-run was worth it, and not for the reason the playbook gives. Its stated value is removing compile surprises for the builder; its real payoff here was finding a production bug (the 40001 hang) that phase 2's unit tests and reviews had all missed, because nobody had ever caused a real stale write. The plan itself then became less important: the cloud session built from the scratch branch, not by replaying the 19,785-line plan. A plan that large is close to a transcript of the code; for future phases I would pre-run on the real feature branch and let the plan carry decisions and interfaces, not every line.

I am less happy with how much the controller depended on the subagents' own browser checks. I looked at the board and the contact page myself, but most screens were seen only by subagents through a CDP script. Jake's own testing in the cloud session then found the whole app scrolling sideways (sr-only text escaping the shell) and cramped lists, which a person scrolling once would have caught.

The renumbering scare is the other lesson: a repo-wide `sed` for "0030" was one flag away from corrupting voice cost constants. Scope a history rewrite to named files and named phrases, and read the diff before trusting it.

## What I'm satisfied with

- Reproducing the subagent's hang report myself with a timed script before acting on it, then measuring before and after on both the CRM and the order desk.
- The rebuild check: every task of plan 3a reproduced byte for byte from the plan text.
- Stopping cleanly at the classifier blocks (the progress-ledger append, the merge) instead of routing around them.

## What I'm not satisfied with

- My first plan 3a put "apply the migration to staging" before the step that writes it; caught only when generating 3b.
- A substitution I ran on the generated plan blanked one header line (a `.` in the pattern matched an apostrophe); I fixed it at the source and regenerated, but it should not have been a blind `sed`.
- Before the usage limit hit, I had not pushed the scratch branch or the plans; the continuation worked because the cloud session reached them anyway, but the state should have been pushed at each milestone.

## Open threads

- Jake: merge `docs/order-conflict-lesson` (lesson L-018, the repo journal entry, the spec renumber). It may clash on `lessons.md` numbering if the 3c session adds an L-018 first; renumber on merge.
- Plan 3c (3c1 Settings, 0033; 3c2 data, 0034) is with another session on `feature/crm-3c1`.
- No client has the CRM switched on yet; piloting needs Jake's go (`docs/crm-client-switch-on.md`).
- Shared client passwords still on, no client Admin yet; the WhatsApp template send is parked for onboarding.
- Remove `crm-demo` from staging once 3c is done.

## Candidate playbook rules

- **In a Supabase (PostgREST) app, raise a database function's refusals with SQLSTATE PT409 (or P0002 for a missing row), never 40001.** PostgREST retries 40001 as a serialization failure until the gateway times out: "changed since you opened it" took 125 seconds and arrived as "upstream request timeout" on Richpilot's order desk and CRM, live in production, until migrations 0030 and 0031. (adopted)
- **Trigger every refusal path (stale version, already undone, not allowed) at least once against the real stack, and time it, before calling concurrency handling done.** Unit tests of the error mapping cannot see what the infrastructure does to the error: phase 2 mapped 40001 to "Changed since you opened it" in tested code, but nobody caused a real stale write, so the hang shipped. (adopted)
- **When subagents build a multi-task plan one task at a time, keep one shared brief file and append each finished task's decisions to it ("From Task N") before dispatching the next.** On the CRM tab pre-run, later tasks inherited seed records, the isolation table's ordering rule and the PT409 fix without rediscovering them. (adopted)
