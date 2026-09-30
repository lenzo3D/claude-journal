---
date: 2026-09-30
project: richpilot
topic: Naming Richpilot, the HubSpot detour, and planning the in-app CRM
outcome: shipped
satisfaction: 4/5 (my estimate; Jake did not rate it)
model: Claude Opus 5.5
run: attended
related: [richmade]
---

# Naming Richpilot, the HubSpot detour, and planning the in-app CRM

One long session from 28 to 30 Sep 2026. The context was compacted once, part
way through the CRM spec work, so the early steps below come from the
compaction summary and the git history rather than the full conversation.
Commit hashes and file contents were rechecked against the repos before
writing this.

## The ask

It moved through five requests, each growing out of the last:

1. Name the platform. A product name only, no domain needed ("Our business
   name is Richmade and we already have domains"), then "use a name with Rich
   in it". Jake chose **Richpilot**.
2. After Jake renamed the GitHub repo and Vercel project himself: "I'm worried
   my workflows may break, can you communicate to all other Claude sessions
   that everything has been renamed?"
3. HubSpot as the CRM: next steps, a spec, the client onboarding SOP, then an
   implementation plan.
4. "Will HubSpot actually live in our dashboard?", then research into what AI
   automation agencies actually offer, then: build it better and more
   customisable than GoHighLevel, as "a proper full-blown CRM with full
   integrations... I want there to be no stone left unturned", in a tab called
   CRM. Scoped with "Only do 1" (CRM core).
5. Approve the spec, write the plan, then "just save the plan and write a
   handoff which I will then carry the tasks out in another session".

Standing constraints: never push `main` or touch production without his yes;
Jake pastes production SQL himself; no em dashes; commit as lenzo3D noreply.

## What I did

1. **Naming.** Updated `AI Agency/Richmade Assets/platform-naming.md`. I had
   been screening domains; Jake corrected that domains don't matter, so the
   screen became existing software brands and trade marks only. Round 3 ("Rich"
   names) found Richpilot, Richreply and Richfront clean; Richflow, Richdesk and
   Richloop clash with existing brands.
2. **Renames without breakage.** Local folder moved to
   `~/Desktop/Agents/Richpilot` with the old path left as a symlink; Claude's
   project memory key symlinked to the old one; git origin repointed to
   `lenzo3D/richpilot`; `.vercel/project.json` renamed. I told the other
   sessions. Later deploy checks (by another session) found the old
   `whatsappagent.vercel.app` hostname had come loose from the project, and the
   real one is `richpilot.vercel.app`.
3. **HubSpot spec and plan.** Brainstormed with AskUserQuestion (each client's
   own HubSpot, leads worked in HubSpot, a per-client service key), wrote the
   spec with a Step 0 pilot and an onboarding SOP, then a 16-task plan whose
   pure code I pre-ran against its own tests (104 passing). Branch
   `specs/hubspot-sync`, commits `8b1665b`, `237efd2`.
4. **The question that should have come first.** Jake asked whether HubSpot
   lives inside our dashboard. It can't: HubSpot blocks iframes
   (`frame-ancestors`), and app cards need a paid plan. Staff would work in two
   tabs. That reframed everything. I researched the agency market
   (GoHighLevel's white-label all-in-one model, its pricing) and Jake chose to
   build the CRM in Richpilot instead.
5. **CRM roadmap and core spec.** Split "everything feeds in" into six
   sub-projects (core, email in, API and webhooks, automations, connectors,
   reports) under one design rule, "one pipe": every source writes a contact
   plus an activity. Brainstormed core (deals per enquiry; custom stages each
   with a type; named staff accounts; the AI acts on facts and only suggests
   judgement calls, never setting a deal's value). Wrote the roadmap and a
   447-line spec; marked the HubSpot spec and plan shelved. Commit `c4ad5c3`
   on `specs/crm-core`, in a git worktree so I didn't disturb another session
   working in the main checkout.
6. **Dead end on delivery.** I linked the spec by repo path; Jake got
   "Couldn't find this file", because the file only existed on the branch, not
   in the checked-out `main`. I exported it with `git show` and sent it as a
   file.
7. **Phase 1 plan (staff accounts).** I chose to write one plan per phase,
   each against the previous phase's merged code, and said why (a plan text
   went stale mid-build in the modules plan). Then I built the whole phase in
   a throwaway copy of the repo and ran it: 299 tests, `next typegen`, `tsc`,
   lint and a no-env `next build`, all clean. A script pasted that verified
   code into the plan, so nothing was retyped. 14 tasks, commit `675947d`.
8. **Handoff.** Wrote `handoff.md`, a progress ledger and a plan copy into
   the git-ignored `.superpowers/sdd/2026-09-29-crm-staff-accounts/` in the
   Richpilot repo, so a session on `main` can read them, plus a kickoff prompt.
   Removed my scratch worktree.
9. Answered why `~/Documents/Web Agency` still exists: it's the compatibility
   symlink from the 27 Sep rename, kept on purpose.

## What changed

- `~/Desktop/Agents/Richpilot` (branch `specs/hubspot-sync`, local): HubSpot
  spec `8b1665b`, 16-task plan `237efd2`. Shelved.
- Same repo, branch `specs/crm-core`, local, not pushed: merge `33282ae`,
  roadmap and core spec `c4ad5c3`, merge of main 78417e0 `a612ce1`, phase 1
  plan `675947d` (`docs/superpowers/plans/2026-09-29-crm-staff-accounts.md`).
- Same repo, git-ignored: `.superpowers/sdd/2026-09-29-crm-staff-accounts/`
  (`handoff.md`, `progress.md`, `plan.md`).
- Outside the repo: folder rename plus symlinks; memory notes
  `richmade-ai-agency-pivot` and `wa-automation-agent` updated; the naming
  doc in `Richmade Assets`.
- No production changes. No pushes.

## Corrections and feedback from the user

- "We don't need a domain as this is just a name for our software." I had been
  filtering names by domain availability.
- "Use a name with Rich in it", after my shortlist of neutral names.
- The HubSpot direction was his, and so was abandoning it, via one question I
  should have raised: "Will HubSpot actually live in our dashboard?"
- "Instead of calling it leads, maybe just call it a CRM tab", and "Only do 1".
- The broken spec link (a screenshot of the error). Fair: I pointed him at a
  file on a branch he didn't have checked out.
- He chose to run the build in a separate session rather than here.

## My take

The biggest miss is mine. I took HubSpot from "decided" to a spec, a 16-task
plan and 104 pre-run tests before anyone asked where the client's staff would
actually spend their day. The iframe block was one fetch away. It was knowable
at the brainstorming stage, and it's the fact that killed the whole direction.
The work wasn't wasted (contacts, hooks and the quiet-chat sweep carry into
CRM core, and HubSpot comes back as a connector), but a day of spec-and-plan
effort went on a product experience Jake didn't want. For any third-party
integration, the first question should be "where does the user work, and can
that tool live there?"

Jake's pivot to an in-app CRM is the right call for an agency selling one
dashboard, and splitting "no stone unturned" into six sub-projects with only
core in scope kept it buildable. My concern is size: CRM core alone is three
phases, and the other five sub-projects are each real products. The "one
pipe" rule is what will keep them from turning into five separate systems.

Pre-running the plan paid off. It caught things an implementer would
otherwise have hit mid-task: the `react-hooks/set-state-in-effect` lint rule,
a Supabase `rpc()` typing trap, Postgres 500s on malformed uuids, Turbopack
refusing a symlinked `node_modules`, and one real security hole in my own
design. Once cookies can be revoked, `scopedClientId()` returning null for a
dead session would have meant "every client". It now throws a 401. But
pre-running isn't review. The build session's reviewers still found two
Important issues in Task 2 (a malformed stored hash, and a Unicode test that
proved nothing) and one in Task 5, and main moved underneath the plan (the
migration became 0026). Pre-running removes transcription and toolchain
surprises, and the plan still gets a reviewer.

## What I'm satisfied with

- Renames done with symlinks and redirects, so nothing broke for other
  sessions.
- Worktrees for all spec and plan work, so the session using the main
  checkout was never disturbed.
- The fail-closed session design, caught while pre-running, not in production.
- One plan per phase, with a handoff that names the non-obvious traps and what
  was and wasn't verified (no database step had run).

## What I'm not satisfied with

- The HubSpot spec and plan before the "does it live in our dashboard" check.
- Linking a branch-only file by path. I've now hit that once; export or send
  the file.
- The Write tool turned a backslash-u-2014 escape I typed into a real em dash, twice (it just did it a third time, in this entry)
  (in the plan template and the handoff). I caught both with a byte-level
  grep, but only because I checked.

## Open threads

- The phase 1 build is running in another session on
  `feature/crm-staff-accounts` (at `cc72dee`, migration renumbered to 0026).
  Its ledger has two parked review findings for Jake: user cookies have no
  signed expiry (revocation only by version bump or cookie age), and the
  last-Admin guard also blocks removing a mistaken, never-accepted Admin
  invite.
- Jake to provide a Resend-verified sender for `AUTH_EMAIL_FROM`, and
  `APP_URL=https://richpilot.vercel.app` in Vercel, at rollout.
- Heads-up for Jake: Leisure Frontier's staff will see the "get your own
  account" banner as soon as phase 1 deploys.
- After phase 1 merges: write the phase 2 plan (data model, the pipe, the AI)
  against the merged code, reusing the shelved HubSpot plan's pieces.
- Later renames: `package.json` name `wa-agent`, doc mentions, optionally
  `app.richmade.sg`. Remove the `Web Agency` and `WA Automation Agent`
  symlinks only once nothing references them.

## Candidate playbook rules

- **Before speccing an integration with a third-party app, establish where the client's staff will work day to day, and check whether that app can live there (embedding, iframe and plan limits).** HubSpot blocks iframes, which only surfaced after a full spec and 16-task plan, and the direction was shelved. (not adopted, P-2026-09-30-01)
- **Pre-run a plan's code in a scratch copy of the repo (tests, type check, lint, build) and paste the verified code into the plan by script; still review each task when it's built.** Pre-running caught five toolchain and design traps before implementation, but reviewers still found three Important issues. (adopted)
- **When renaming a folder, repo or project other sessions use, leave a symlink or redirect at the old name, tell the other sessions, and remove the old name only once nothing references it.** The Richpilot rename broke nothing, and `Web Agency` still resolves for old sessions. (adopted)
