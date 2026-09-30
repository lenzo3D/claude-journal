# Richmade Playbook

The SOP for any agent working on Richmade projects. Every rule here was approved by Jake, and links to where it came from. Read the whole file before starting work.

Format for each rule:

- **Rule, written as an instruction.** Why it matters. _(source: [project/date](projects/slug/journals/file.md))_

A rule with several sources lists them all: `_(source: [richmade/2026-09-28](...), [richpilot/2026-10-02](...))_`.

Rules marked "seeded" were adopted on 28 Sep 2026 from lessons already recorded in Claude's memory notes on Jake's Mac, before the journal existed. The note named is a historical label only. Each seeded rule carries its full reason and incident, so you never need the note itself to follow it.

Everything a rule depends on lives in this repo. Reference material copied from other repos is in `reference/`, and `python3 scripts/check-sources.py` reports when an original has changed since it was copied.

Rules proposed but not yet approved are in `PENDING.md`. They are **not** in force. Rules Jake turned down are in `REJECTED.md`.

## Writing and copy

- **Never use em dashes in anything written for Richmade or its clients: copy, UI strings, documents, decks, journals.** Replace each one with whatever that sentence needs (a comma, colon, parentheses, or a new sentence), not a mechanical swap. Where a codebase allows it, enforce the rule with a test, as Red Dot News does with `no-em-dash.test.ts`. Em dashes are a well-known tell of AI writing. _(seeded, memory: `reddot-news-no-em-dash-rule`; overrides the July 2026 note that allowed them in Richmade copy)_
- **Don't write chains of clipped fragment pairs** ("Two people. No account managers."). Write flowing sentences, with at most one poster-style pair per page. Jake reads fragment chains as AI-generated. _(seeded, memory: `design-direction-no-claude-aesthetic`)_
- **Never fabricate or overclaim.** Don't invent facts, contact details, reviews, ratings or credentials (for example, Richmade is not a pre-approved PSG vendor), and don't make hard delivery promises ("21 days"). If real data is missing, ship the feature switched off and list the gap as a human TODO. Fabrication misleads clients and creates legal exposure, including POFMA for news content. _(seeded, memory: `richmade-site-project`, `9solar-news-pivot-and-terms`)_

## Design

- **Use the Richmade design system only for Richmade-branded material:** non-legal documents, PDFs and slide decks that carry Richmade branding. It does not apply to client websites or client content, which follow each client's own brief. The full system (colours, type, layout, voice, kill list) is in `reference/richmade-design-system.md`, with the font files in `reference/fonts/`. In short: white canvas `#FFFFFF`, ink `#0B0C0E`, one electric-blue accent `#0E63F4` used only for key emphasis, Schibsted Grotesk headings with Instrument Sans body, and generous whitespace. Never use cream/terracotta/serif combinations or AI-default fonts (Inter, Space Grotesk) for Richmade material, because that look reads as Claude's own style. _(seeded, memory: `design-direction-no-claude-aesthetic`; scope set by Jake 28 Sep 2026)_

## Engineering and verification

- **Don't call anything done without direct evidence.** Receive the actual email or sheet row, run lint and tests yourself, and test with real input in a real browser. A 200 response, a subagent's report, or a script-dispatched event is not proof. The Leisure Frontier enquiry handler returns 200 for honeypot bot submissions, subagents missed a lint break that only the controller caught by running `npm run lint`, and script-dispatched wheel events never scroll a page. _(seeded, memory: `leisure-frontier-enquiry-blocker`, `wa-automation-agent`, `9solar-shorts-feed-direction`)_
- **Test anything defensive a fix adds as hard as the fix itself.** On Richpilot, adding `type="number"` to fix a spend-cap bug quietly reopened it, because the browser turns "1e" into an empty value, which the API read as "no cap". _(seeded, memory: `wa-automation-agent`)_
- **Give security-sensitive changes (auth, webhooks, admin routes, secrets) an independent review on the strongest available model, and re-review every fix round.** On Richpilot Task 6, an Opus review caught two real holes, and the fix for the first one created the second. _(seeded, memory: `wa-automation-agent`)_
- **Never hand-edit generated files.** Edit the source and regenerate. Make bulk changes such as domain migrations with a script, then grep for leftovers, including inside build and generator scripts. On Leisure Frontier, a manual find-and-replace would have missed `BASE_URL` in `gen_zh.py`, and the next regeneration would have silently reverted every Chinese page. _(seeded, memory: `leisure-frontier-seo-geo-audit`)_
- **Before any long or expensive batch run (evals, bulk migrations, agent fan-outs), run it on 3 or 4 items first and check the result is plausible, and keep parallel runs low on Jake's plan.** The first description-tuning run reported 0% recall from a broken harness that a 4-item check caught in two minutes, and 10 parallel Opus sessions got throttled into a 72-minute round. _(source: [richmade/2026-09-28](projects/richmade/journals/2026-09-28-journal-queue-and-headless-tests.md))_

- **Pre-run a plan's code in a scratch copy of the repo (tests, type check, lint, build) and paste the verified code into the plan by script, then still review each task when it is built.** Pre-running the Richpilot staff-accounts plan caught a lint rule, a Supabase typing trap, uuid errors surfacing as 500s, a Turbopack symlink failure and a fail-open session design before any implementer met them, but the build's reviewers still found three Important issues. _(source: [richpilot/2026-09-30](projects/richpilot/journals/2026-09-30-name-hubspot-pivot-crm-plan.md))_

## Tools and environment

- **Assume Jake's Mac has a bare toolchain:** no Homebrew, no gh CLI, no ffmpeg, LibreOffice, pandoc or pdftoppm. Use the known workarounds: portable Node 22 under `~/.local`, `pip install imageio-ffmpeg` for ffmpeg, `certifi` with `SSL_CERT_FILE` for Python HTTPS, and hand-built OOXML for .docx files. Use `127.0.0.1`, not `localhost`, for local servers. When the Claude browser pane freezes, take screenshots with headless Chrome over CDP. Each of these has cost real time before. _(seeded, memory: `mac-toolchain-gaps`, `browser-pane-freeze-workaround`)_
- **Commit as `43843967+lenzo3D@users.noreply.github.com` in any repo deployed on Vercel Hobby.** Vercel blocks the deploy when GitHub can't match the commit author to Jake's account. _(seeded, memory: `vercel-hobby-committer-rule`)_
- **In interactive UI, prefer native browser behaviour (CSS scroll-snap, instant playback) over hand-rolled animation, curtains or poster frames.** On the 9 Solar News Shorts feed, every workaround that traded responsiveness for polish got reported as broken or laggy. _(seeded, memory: `9solar-shorts-feed-direction`)_
- **When something must happen after another task (logging, cleanup, a notification), put it in a standing instruction (CLAUDE.md) or a hook, not only in a skill description.** Claude picks skills at the start of a request; in headless tests "remember" and "commit and push" only opened the journal skill once the global CLAUDE.md line existed. _(source: [richmade/2026-09-28](projects/richmade/journals/2026-09-28-journal-queue-and-headless-tests.md))_

- **When renaming a folder, repo or project that other sessions use, leave a symlink or redirect at the old name, tell the other sessions, and remove the old name only once nothing references it.** The Richpilot and AI Agency renames broke nothing for sessions and docs still using the old paths. _(source: [richpilot/2026-09-30](projects/richpilot/journals/2026-09-30-name-hubspot-pivot-crm-plan.md))_

## Client work and communication

- **Never act on Fathom or other AI meeting summaries for pricing, approvals or commitments.** Check the raw transcript and cite timestamps. Fathom reported the 9 Solar S$900/month retainer as approved when it had been deferred, a S$13,200/year mistake if acted on. _(seeded, memory: `9solar-platform-meeting-db`, `leisure-frontier-meeting-db`)_
- **Keep internal strategy private.** Never share or volunteer internal repos, pre- or post-call transcript sections, pricing floors, or effort facts ("the site is 90% pre-built") with clients. Those recordings contain Richmade's private pricing strategy. _(seeded, memory: `9solar-platform-meeting-db`, `9solar-news-pivot-and-terms`)_

## Project process

- **For multi-step builds, write a spec, then a plan, then do one task per session.** Keep a progress ledger, and treat it and `git log` as the source of truth for where the plan stands. Work Jake has parked stays parked until he raises it again. This kept the 15-task Richpilot build on track across many sessions. _(seeded, memory: `wa-automation-agent`, `9solar-shorts-feed-direction`)_
- **Record human-only work in a TODO or runbook file with exact steps:** account creation, payments, domains and DNS, credentials, and client approvals. Don't work around them. An agent can't and shouldn't do them, and hidden blockers stall launches. _(seeded, memory: `leisure-frontier-enquiry-blocker`, `aura-9solar-news-site`)_
- **Before turning an older note or past decision into a standing rule, confirm its scope with Jake.** Scope is what drifts: the July 2026 design note said "Richmade and client work", and by September it meant Richmade-branded documents only. _(source: [richmade/2026-09-28](projects/richmade/journals/2026-09-28-session-journal-skill.md))_
- **Keep everything the playbook depends on inside this repo.** The overnight agent may only have claude-journal, so the source notes and design tokens it needs must be copied here rather than linked from `~/.claude` or other repos. _(source: [richmade/2026-09-28](projects/richmade/journals/2026-09-28-session-journal-skill.md))_
- **When Jake's input would change what a system does, not just how well it does it, confirm the intended behaviour before building or running anything at scale.** Six flipped eval labels were really a scope decision ("do it, then log it") plus one mis-click; tuning straight to them would have made the journal skill take over article writing. _(source: [richmade/2026-09-28](projects/richmade/journals/2026-09-28-journal-queue-and-headless-tests.md))_

## Never do

- **Never push to main, touch a production database, deploy, send anything to a client, or spend money without Jake's explicit yes for that specific action.** Approval doesn't carry over to the next action. This is the main safety gate for an autonomous agent. _(seeded, memory: `wa-automation-agent`)_
