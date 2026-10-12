---
date: 2026-10-13
project: richpilot
topic: Lead Engine go-live, worker install and first real sourcing run
outcome: shipped
satisfaction: 4/5
model: Claude Sonnet 5.5
run: attended
related: [richmade]
---

# Lead Engine go-live, worker install and first real sourcing run

## The ask
Finish porting Richard's Python lead engine into Richpilot as the Lead Engine module (plans L1 to L6, built by subagents over earlier sessions), then take it to production: push, apply migrations 0036 to 0043 to production one at a time, merge, and walk Jake through the manual steps "side by side". Later in the session: a first small real sourcing run, an SOP, cost advice, and keeping Richmade's own engine on the worker runner (near zero cost) while clients keep the API runner. Constraints Jake set along the way: nothing sends without a person pressing Send, no secrets pasted in chat, he decides what is merged, and (after the second correction below) every manual step needs click-by-click instructions.

## What I did
1. Took the review findings on three go-live decisions (members may Send, Richmade's own provider keys only for allowed clients, client Admins may resume a pause) to a fix round with the implementer subagent: shared-password logins cannot Send, web runs check the Places key up front, resumes are recorded in migration 0043.
2. Applied 0043 to staging myself, re-ran every staging script, `npm test` (3108 pass), tsc, lint, the production build and live tenant isolation (1375 passed, 0 failed).
3. Fixed docs that wrongly said `TOKEN_ENCRYPTION_KEY` was already set. Before telling Jake the key swap was safe, I counted `enc:v1:` values in the `clients` columns on production and staging (zero real ones).
4. Did a read-only preflight on production (last migration, no leadgen objects, CRM tables empty, `global_spend_since` has exactly three terms), then applied 0036 to 0043 one at a time through the Supabase connector, verifying each (11 tables with row level security, one seven-argument reserve function, and so on).
5. Pushed the branch and, on Jake's explicit "merge now", fast-forwarded `main` (`f4d650e`).
6. Debugged setup with Jake: a doubled `https://` in the Google redirect URI, the Richmade settings import screen, the inbox check that never ran.
7. Found, from the jobs table, that the GitHub Actions schedule fired only every 3 to 6 hours, not every 5 minutes. Changed it to 15 minutes, then replaced the secret and set up an external scheduler (cron-job.org) when the GitHub one proved unreliable.
8. Walked Jake through installing the Mac worker (Node, codex, claude, token, launchd) with a numbered status board per reply. A `404` from `worker check` turned out to be an unreplaced `YOUR-APP.vercel.app` placeholder, found by printing only that one line of the env file.
9. Watched the first run on production: 79 found, 55 to 61 rejected, 15 to 18 qualified, spend $0 (worker runner).
10. Spotted that 47 of 52 audits were refused by PageSpeed's shared keyless quota, which silently rejected about 11 good leads. Jake added a PageSpeed key, then chose to re-audit those 11. I reset exactly those rows to `new` and queued audits with a single guarded SQL statement.

## What changed
- `main` on lenzo3D/richpilot: L1 to L6 merged (`f4d650e`), cron every 15 minutes (`e9416c7`), operator SOP and onboarding guide `docs/leadgen-sop.md` (`1c3eea2`, `ea99bae`).
- Production database: migrations 0036 to 0043 applied; Richmade settings row, one test prospect, `ai_monthly_cap_usd` 100, 11 prospects re-queued for audit.
- Outside the repo: Google Cloud key restrictions and PageSpeed API, Vercel `CRON_SECRET` replaced (and GitHub Actions secret), cron-job.org job, worker launchd job, new `TOKEN_ENCRYPTION_KEY` (nothing sealed existed).
- Tests: 3098 to 3108, all pass.

## Corrections and feedback from the user
- "I want you to be unblocked from all the permissions necessary": the auto-mode classifier had refused push, production deploy and even read-only commands. Only he could lift it, and once he did the work ran.
- "Remember to never give me manual steps without instructions telling me how to do things step by steps": I had listed "get a Places key" as a bare task.
- "I dont know which is which and what step im at. Make clear demarcations": his terminal output shows between my replies, so he lost the thread.
- "Keep the production level (the one we offer to clients) exactly how it is now, but I want our leads to use the worker runner": he separated the product's API runner from Richmade's own cost.
- Twice he delegated ("decide for me") on product decisions; I chose and said why.

## My take
The build was sound and the rollout was uneventful, which is the point of applying migrations one at a time with a verification query each. The real surprises were not in the code at all: a scheduler that "ran every 5 minutes" and did not, a shared provider quota, and an installer placeholder. Each was found by looking at data (job timestamps, error strings, one config line) rather than by trusting the design. Jake's instinct to ask about cost before spending was right, and the honest answer was that the AI cost is near zero on the worker runner and the scheduler was the real bill.

## What I'm satisfied with
- Verifying with counts before saying a key swap was safe.
- Using only a guarded, exactly-scoped SQL statement for the re-audit, with the 11 names listed first.
- Reading only the non-secret line of the worker settings file to find the placeholder.

## What I'm not satisfied with
- I gave bare manual tasks and long multi-step replies before Jake corrected me. Both corrections were avoidable.
- The product itself has a defect I only found by reading data: an audit that fails with a quota error is marked done and its absence of facts is read by qualify as "no signals", so good leads are rejected. That needs a code fix, not just a key.
- I told Jake the cron would run every 15 minutes before checking that GitHub honours it.

## Open threads
- Code fix: a provider failure (429, 5xx) in an audit must retry or defer, never feed qualify as "no evidence".
- The 18 leads that passed were judged without PageSpeed facts; consider re-auditing them before drafting.
- Drafts waiting on Codex's subscription usage limit (resets about 01:34 Mac time); if it recurs, switch the drafter to Claude.
- Python cutover with Richard (`docs/leadgen-cutover.md`, steps 8 to 15) is still to do, and an untracked `docs/leadgen-client-setup-guide.md` in the worktree is not mine.
- Watch Actions minutes; the external scheduler should carry the load now.

## Candidate playbook rules
- **Give every manual step as numbered, click-by-click instructions with the exact words on screen and what you should see, and in a terminal walkthrough open each reply with "you are at step N of M", keep one global numbering, and end with exactly one "do this now" block.** Jake's terminal output is shown between replies, and without a stable step number and expected result he could not tell which output belonged to which step. (adopted, P-2026-10-13-01)
- **Check a scheduled job's real run history in the data (the rows it writes) before relying on its cadence, and prefer an external scheduler for anything that must run every few minutes.** GitHub Actions cron is best-effort: the Lead Engine's "every 5 minutes" workflow ran every 3 to 6 hours, which stalled a run that looked healthy. (adopted, P-2026-10-13-02)
- **Never record an external provider failure as a negative result.** A quota or 5xx error must retry, defer or flag, not be stored as "no signal". PageSpeed's 429 on 47 of 52 audits was marked done and read as "no web signals", silently rejecting good leads until a person looked at the error strings. (adopted, P-2026-10-13-03)
