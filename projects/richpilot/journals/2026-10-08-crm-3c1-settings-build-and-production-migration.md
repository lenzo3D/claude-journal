---
date: 2026-10-08
project: richpilot
topic: CRM 3c part 1 (Settings), an 8-task subagent build, the final review, migration 0033 on production and the live run-through
outcome: partial
satisfaction: 4/5
model: Claude Sonnet 5.5 then Claude Opus 5 (controller), Sonnet 5.5 implementers, Opus reviewers
run: attended
---

# CRM 3c part 1 (Settings): 8 tasks, 28 commits, 0033 on production, and the run-through that was blocked three times

Spans 7 to 8 Oct 2026. The session began as a check on a cloud session's CRM work and became the whole of plan 3c1.

## The ask

Jake opened with "i completed the CRM build in a cloud session. Check the progress and see whether it is actually completed and check for anything wrong." The honest answer was no: plans 3a and 3b were on `main` and working, but 3c did not exist, so Settings, CSV import and export, and deleting one person were all unbuilt.

Then, in order: "First, fix the issues."; "Untick the CRM for now, then plan 3c"; "Use your defaults for all five and start building" (after I put five open questions to him); and at the end "yes apply 0033 to production, yes do number 2, use a demo client on staging and allow staging writes."

He also switched the session model to Opus 5 partway through the first dispatch and said "Try again", which put the controller on a stronger model than the implementers for the rest of the run.

## What I did

1. Audited `origin/main` at `88e6bff` on a clean worktree: 953 tests passing, `tsc` clean once Next's route types are generated, lint clean, no em dashes. Confirmed 3a and 3b shipped and 3c absent, and checked production's schema and function ACLs against staging by hashing every CRM function definition.
2. Found and reported seven issues. Four were not real (the switch-on doc was already updated by another session; the migration history gap predated this work; production's hand-applied function bodies matched staging exactly; the two 15-second caches were sound). One was real and needed Jake: `9-solar-fintech` had the CRM switched on in production with an empty never-sync list, so the first staff message would have become a customer record. On his word I unticked it.
3. Had an Opus agent write the 3c plans, split into 3c1 (Settings, 8 tasks, migration 0033) and 3c2 (import, export, one person, migration 0034), with the SQL and pure code pre-run in a scratch copy.
4. Ran plan 3c1 with `superpowers:subagent-driven-development` in a worktree on `feature/crm-3c1`: one Sonnet implementer per task, an Opus review of each committed diff, fix rounds, a scoped re-review per round, then a final Opus review of the whole branch and one fix wave. I gated every task myself (tests, typegen and `tsc`, lint, a production build and `npm run crm:isolation` for route tasks) and kept a ledger of every verdict, deferred minor and ruling.
5. Applied migration `0033_crm_admin.sql` to production myself after Jake's yes, as one script through the Supabase connector, then re-applied two functions with their comments so the file and production match, and proved it by comparing an md5 fingerprint of all 29 CRM function definitions against staging.
6. Removed and reseeded staging's `crm-demo` to its exact baseline, then ran the live run-through with two Opus agents on strictly partitioned areas (pipelines and stages; fields, retention, never-sync and the Richmade picker), with instructions to look for problems rather than confirm success.
7. Took one last copy-only fix from the run-through's findings and verified it myself after the agent's report came back empty.

## What changed

- Branch `feature/crm-3c1` at `cff0c90`, 29 commits off `88e6bff`, 64 files, about 10,200 lines added, not pushed. Five Settings pages (pipelines and stages, custom fields and list columns, Lost reasons, never-sync, retention), 18 new or changed routes all gated on `crm.configure`, `supabase/migrations/0033_crm_admin.sql` (12 functions, all service-role only), README and `docs/crm-client-switch-on.md` rewritten for Settings.
- Tests 953 to 1024, all passing. Isolation check 497 to 709 cases, staging left clean after every run.
- Production database: `0033` applied. Verified 29 CRM functions, no duplicate names, the retention ceiling present as a NOT VALID check, no security-definer function, nothing executable by `anon` or `authenticated` except the three trigger functions, and the all-function fingerprint identical to staging. Production data untouched: 2 clients, 0 contacts, 0 deals, 68 messages.
- Production `9-solar-fintech`: CRM module unticked, now `whatsapp` and `voice`.
- Staging `crm-demo`: removed and reseeded to baseline, then restored deal for deal by both run-through agents. Activities stand at 187 rather than 155 because the run-through's own moves wrote 32 genuine system timeline entries.

## Corrections and feedback from the user

- "First, fix the issues." I had reported seven findings and asked which way to go. He wanted the fixing done before any planning, which was right: three of the seven dissolved under checking and only one needed him.
- "Use your defaults for all five and start building." I had put five product questions to him (consent wording, import timeline entries, retention delay, which calls a delete removes, re-importing a file). He did not want to answer questions a plan had already picked sensible defaults for. Noted: put a default in front of him, not a question, unless the choice is genuinely his.
- The model switch and "Try again". He moved the session to Opus 5 while my first implementer dispatch was in flight. That interrupted agent had already written files and applied `0033` to staging, which I then had to reconcile rather than redo.

## My take

The review loop earned its cost again, and this time the single most valuable finding was one no test would ever have produced. The rule that stops the AI writing prices into a client's CRM did not know the words a coach operator would actually type. "Deposit" and "Quoted price" were caught; "Coach fare", "Bus fare", "GST", "VAT", "Surcharge", "Commission", "Balance due", and every Malay money word were not. A "GST" number field ticked AI fillable would have let the model propose prices for staff to accept, and the text-level money filter cannot help because a number is not a string. It took four widenings, and each one found more: the third was found only by a reviewer probing a market vocabulary, and the fourth by diffing a 210-label corpus after my own fix wave introduced a regression. A money rule written in English by people who do not live in the market is a rule with holes in it.

I was wrong twice in ways the reviewers caught. I ruled that a delete conflict should close the dialog; that silently reverted the chosen destination to the default pipeline, which is a worse hazard on a destructive action than the thing I was fixing. I dropped "toll" as a money word on the reasoning that compound forms are caught anyway; the reviewer pointed out the asymmetry only bites on number fields, where the text filter cannot see a price, which is the same argument I had used to keep `sewa`. Being argued out of a ruling by a reviewer I briefed is the loop working, and the reversals are in the ledger where Jake can see them.

My ledger also drifted from the code twice, and the final whole-branch review caught both: a claim about what a comparison refuses that a later relaxation had made false, and a bundle-safety judgement from task 4 that task 7 silently invalidated by adding an import to a shared module. Notes about code go stale exactly like comments do.

The three permission stops were handled right every time. A subagent's browser step, my own SQL restore and a record-value write were each denied, and each time the agent stopped instead of working around it. That cost real verification and left staging non-baseline for several hours, and I put the decision to Jake rather than rerouting the action to another agent. I would do the same again, but I should have asked for the permission earlier instead of continuing for two more tasks with a known hole in the evidence.

Risk ahead: the code is not deployed. The migration is on production and safe before the code, as designed, but nothing in Settings has been exercised against production data, and no client has the CRM on.

## What I'm satisfied with

- Applying `0033` to production and then proving it, not asserting it. The fingerprint comparison across all 29 functions is a stronger check than any count, and it caught that my first apply had stripped the comments the documented check keys on.
- Catching that the plan's own production check expected 28 functions when the answer is 29. That would have failed during a production rollout and sent us hunting a non-problem.
- The run-through finding a real trap that three code reviews could not: the never-sync page never said which country code it adds, so a Malaysian local number silently became an eleven-digit Singapore number matching nobody, leaving that person unprotected while the list looked right.
- Partitioning the two run-through agents so they could work the same client in parallel without destroying each other's state, and having both restore it.

## What I'm not satisfied with

- I handed an implementer a SQL signature I had not checked, and it corrected me. Small, but it was in a verification query heading for a rollout document.
- I let the plan's stale expected test count and function count reach task briefs unchallenged until a reviewer flagged the second one.
- Five of the eight tasks needed at least one fix round, and task 5 needed three, all on the same theme: a dialog promising something the database would not do. The plan pre-ran its SQL and its pure code but not its product promises, which is the same gap phase 2's journal recorded.
- The Supabase connector failed intermittently for several agents (406), so some reviews fell back to reading code where a query would have settled it. I absorbed those checks myself, but it slowed the loop.

## Open threads

- Jake: merge and push `feature/crm-3c1`. The migration is already on production and the code is safe to deploy after it.
- `reference/sops/richpilot-crm-client-switch-on.md` here is a copy of the version on `main`. It needs refreshing once this branch merges, because the branch rewrites that document for Settings.
- 3c part 2: CSV import and export, export one person, delete one person, migration `0034`. The plan is written and committed on `specs/crm-3c`.
- 11 minors triaged to 3c part 2, 11 dropped, listed in the branch ledger. The ones worth remembering: an empty multi-select array counts as having a value and so locks a field's type; Richmade naming a CRM-off client by hand sits on a loading skeleton for ever; retention and reordering take no version, so two Admins can overwrite each other's setting.
- The last corner of spec "Done means" 6: proving a pipelines write under agency scope cannot reach a second client. Staging has one pipeline across all clients, so it needs a second seeded client.
- Accepted known costs in the price rule: "Euro tour", "Bags per person", "Tax ID", and Malay hire labels like "Tempoh sewa" are refused AI filling. Each costs staff one field they fill by hand.

## Candidate playbook rules

- **Test a rule that protects money or safety against the words a real client in that market would actually type, including the local language, before calling it done.** Richpilot's price rule passed every unit test while allowing "Coach fare", "GST", "Harga" and "Bayaran"; it took four widenings, and the market vocabulary was found by a reviewer, not by the tests. (adopted)
- **Run every verification query you write into a rollout step once, against a real database, before handing it over.** This session's plan expected 28 functions where the answer is 29, and the suggested body check searched for a phrase that spans a line break in the file and so can never match. Both would have failed in production for the wrong reason. (adopted)
- **After applying a migration by hand, compare a fingerprint of every affected function definition against the environment it was tested on, rather than counting objects.** A count cannot tell an older copy of the file from the current one; the fingerprint caught that a first apply had stripped the comments a documented check relies on. (adopted)
