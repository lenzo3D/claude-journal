---
date: 2026-10-08
project: richpilot
topic: CRM 3c part 2 (CSV import and export, export and delete one person), a 9-task subagent build, migration 0034 on production, merged to main
outcome: shipped
satisfaction: 4/5
model: Claude Opus 5 then Claude Opus 5.5 (controller), Sonnet 5.5 implementers, Opus reviewers
run: attended
---

# CRM 3c part 2: import, export, export and delete one person, 0034 on production, main 78b62be

Same day as the 3c1 journal, continuing in the same session after "Merge and push, then begin with 3c part 2". The context was compacted twice, so Tasks 1 to 4 are reconstructed from the branch ledger (`.superpowers/sdd/2026-10-07-crm-tab-3c2-data/progress.md`) and `git log`, not from memory.

## The ask

"Merge and push, then begin with 3c part 2", then "continue through the rest of the tasks". Partway through, Jake said "wrong model was being used the whole time, continue with opus 5.5 which ive switched to", so the controller ran on Opus 5.5 from Task 4's re-review onward. Later: "reconnect the supabase connector then finish the tasks", "keep going through the rest of the tasks", and at the end "merge and push, then run session journal". Three decisions came through questions: allow staging sign-in after a permission denial, yes to 0034 on production, and allow an agent to sign in as Richmade on staging.

## What I did

1. Ran plan 3c2's nine tasks with `superpowers:subagent-driven-development` in the worktree `~/Desktop/Agents/Richpilot-3c2` on `feature/crm-3c2`: one Sonnet implementer per task, my own gates (tests, typegen and `tsc`, lint, em dash grep, and a staging read of the demo client's baseline counts after every live check), an Opus review, fix rounds sent back to the same implementer, and a scoped re-review by the same reviewer.
2. Wrote rulings into each dispatch where the plan was wrong or a review changed the design, and appended every ruling, deferred minor and follow-up to the ledger with its cost if wrong.
3. Ran the final whole-branch review BEFORE Task 9 (the handoff's order), so the run-through exercised the fixed code. It checked 14 ledger claims against the final code and found all of them still true.
4. Took the final review's advice to harden 0034 before production (two refusals moved into `crm_import_batch`), proved it on staging inside rolled-back transactions, and applied only that function to staging with `execute_sql` so staging's migration history did not grow.
5. Task 9 (docs, the 5,000-row run-through) and a separate Richmade import and export check, both on staging.
6. Applied 0034 to production myself after Jake's yes, in six transactions plus `notify pgrst`, and verified it read-only.
7. Merged in the 3c2 worktree (the main checkout was on another session's branch, `specs/leadgen-engine`, so I left it alone), re-ran the tests on the merge, pushed, and put the worktree back on its branch.

## What changed

- `main` at `78b62be`: 23 commits on `3ca0418`, 56 files, about 5,800 lines. CSV reader and writer (`src/lib/csv.ts`), import rules, routes and screen, CSV export with the list's filters, export one person as streamed JSON, the delete one person dialog and route, `supabase/migrations/0034_crm_data.sql` (7 functions, 2 tables), README and switch-on checklist rewritten as built.
- Tests 1028 to 1148. Isolation check 709 to 867 cases.
- Production: 0034 applied. 36 `crm_*` functions with one version each; all 7 new ones security invoker, `search_path ''`, `service_role` only; both new tables with RLS on, no policies, no anon or authenticated access; the admin log check lists six actions; every new body equals staging on a comment-stripped md5. Data untouched (2 clients, 0 contacts).
- Staging `crm-demo` left at its baseline (40 contacts, 31 deals, 8 companies, 187 activities), with admin log rows from the checks left in place.
- claude-journal: `reference/sops/richpilot-crm-client-switch-on.md` refreshed from `main`.

## Corrections and feedback from the user

- "wrong model was being used the whole time, continue with opus 5.5 which ive switched to". I had been the controller on the wrong model for most of the build. Nothing to redo, but the commit trailer I use changed with it.
- "reconnect the supabase connector then finish the tasks". The failing server was the project-level `supabase` MCP (406), which I cannot redial; the claude.ai Supabase connector was connected the whole time and did every database step. I should have checked which server had failed before telling him the rollout depended on it.
- His answers to the three questions (sign-in, production, Richmade) are the pattern to repeat: put the decision to him as soon as an agent hits a permission wall, with a recommended option, rather than rerouting.

## My take

Every task needed at least one fix round, and the findings that mattered most were all one shape: two halves of the system disagreeing about the same data. The import preview and the commit check built the never-sync email set two different ways. A resumed import regrouped rows so that a row already marked "written" never had its data written. The person export and the delete had to pick exactly the same chats and calls, and the reviewer only trusted it after running both on nine awkward phone formats side by side. No unit test catches any of these, because each half is correct alone.

The worst mistake in the build was mine. In the Task 3 contracts I told later tasks to put never-sync values in the display form, "+6591234567". Task 8 followed it faithfully, and the review found that Settings would show "++65" and that a near-full list would refuse a delete as full. A contract written by the controller is code nobody tests. I corrected the contract file itself so the wrong line could not reach another brief.

The "carry what was shown" rule from 3c1 paid off twice more. The delete dialog now sends the companies and the identities it showed, and the server refuses with the house 409 if its fresh view differs. Without it, an email added after the dialog opened would have gone onto the never-sync list without the Admin ever seeing it.

Moving the two guards into 0034 before production was the right call and cheap: the final reviewer pointed out that after the first production apply each of them would need a migration 0035. I would ask that question of every migration's last review.

Subagent reports were wrong twice in ways only a diff showed: one implementer said it had reverted `MenuButton` and had not, and Task 5's implementer noted it had not watched tests fail. Reading the diff of every fix round myself is slower but it is the only place these show up.

The production apply went through the connector with no hang, unlike 3b. Splitting the file into small transactions (tables first, then one function each) was the plan if it hung; it never had to fall back to the dashboard.

## What I'm satisfied with

- Live proofs instead of argument on the hard paths: injected faults in a deleted scratch clone proved a failed export now fails in the browser (curl exit 18), and 2,509 calls on three tied microsecond timestamps proved keyset paging skips nothing.
- The 5,000-row run-through: the preview's numbers matched the database exactly after two interruptions and a resume.
- Stopping when a subagent's sign-in was denied, and putting it to Jake instead of handing the same step to another agent.
- Checking production read-only before asking for the yes (0034 free on `origin/main`, 29 functions), and expecting 36, not the plan's 34.

## What I'm not satisfied with

- The never-sync contract error above.
- I told Jake the production rollout depended on reconnecting a server it did not depend on.
- Three tests in Task 8 and the M8 tests in Task 7 were written alongside or after the code, so they were never watched failing; mutants run by the reviewers were the only proof they pin anything.
- The `check-sources.py` warning on the switch-on SOP will stay STALE until the main checkout leaves `specs/leadgen-engine`, because the script reads the checkout, not `main`.

## Open threads

- Confirm the Vercel deploy of `78b62be` went through, then switch-on for a real client can use Settings > Import.
- Later migration: one SQL function returning a person's calls and conversations, shared by export and delete, so they cannot drift (today both use the same TypeScript helpers and a matching SQL clause).
- `scripts/purge-data.mjs` removes at most 100 media files per conversation (found in Task 3, not fixed here).
- Deferred minors in the ledger, none blocking: Task 4 M3 (import ids are a global key), Task 5 N1 (a busy retry outlives leaving the page), Task 6 test pins, Task 3 own-number format follow-up (fails in the safe direction).
- The scratchpad still holds five empty misnamed SQL chunk files (`prod0034/b 87 152.sql` and similar); a guarded `rm` was blocked by the safety check, so they are left for Jake.

## Addendum, same evening: tidy-up and migration 0035

After the journal, Jake asked for four things. The pending rule was rejected. The onboarding docs gained the never-sync gate (fill and read back the list before ticking CRM) and the client logo step, which had sat on an unmerged branch since 3 Oct (main b85f1d2 and 9ede803). Seven merged worktrees and 19 merged branches were removed after copying their git-ignored ledgers into the main checkout. And he chose to build the 0035 follow-up in this session rather than queue it.

0035 adds `crm_person_scope`, one SQL selection of a person's chats and calls, and makes both the export and `crm_delete_person` use it. The proof that mattered was a rolled-back comparison against the OLD function built from 0034's text; the implementer's first version renamed the live function instead, which would have compared new against new once 0035 was applied and always printed a match. The review also caught that deleting calls by id dropped the old predicate's re-check, so a call linked to another contact in the window could have been deleted; I ruled the guard back in. One residual difference (a call committed within milliseconds of a delete) was accepted with its cost written down. Applied to production after Jake's yes, merged and pushed (main 3e90062).

One slip of mine: I pushed the onboarding docs before running the test suite, and a test reads that file. It passed when run straight after, but the order was wrong.

## Candidate playbook rules

- **When a screen shows a list or count before a destructive action, send what was shown with the request, and have the server refuse with a worded conflict if its fresh view differs.** On Richpilot's delete one person, the dialog sends the companies and identities it showed; without it, an email added after the dialog opened would have gone onto the never-sync list unseen, and a company someone linked meanwhile could have been deleted. (adopted)
- **Ask the final review of any migration not yet on production which of its fixes are free now and cost a migration later, and land those before the first production apply.** Richpilot's 0034 gained two server-side refusals (a mixed import entry, a batch into a finished import) the day before rollout; after it, each would have needed migration 0035. (adopted)
- **When a permission check denies a step, stop and put the decision to Jake; never retry it through another tool or another agent.** Four denials across Richpilot 3c1 and 3c2 were each stopped and surfaced, and Jake allowed the staging sign-in in one answer, which unblocked the rest of the run without anyone working around the check. (not adopted, P-2026-10-08-01)
