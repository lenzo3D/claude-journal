---
date: 2026-09-28
project: richmade
topic: Building the session-journal skill and seeding the playbook
outcome: shipped
satisfaction: 4/5
model: Claude Opus 5.5
related: [9solar-platform, 9solar-news, wa-automation-agent, leisure-frontier]
---

# Building the session-journal skill and seeding the playbook

## The ask
Jake asked how to create a Claude skill, then described the one he wanted: at the end of a session, Claude writes a journal of what was asked, what it did, what changed, its own reaction and opinion, and what it was satisfied with. The goal behind it is bigger than journaling. Once the ongoing projects are done, he wants Claude to have "learned everything from us" so that it can run overnight as Richmade's first AI employee, handling whole projects largely on its own and using the accumulated knowledge as an SOP. His example of a rule: don't use em dashes.

## What I did
1. Loaded the `skill-creator` skill and explained the process in plain terms (capture intent, draft, test, improve), then asked what the skill was for.
2. Before designing anything, I corrected two assumptions in the brief. Claude's model doesn't learn from journals, so the real product is a knowledge base the future agent reads. And a skill can't detect when a session ends, so something has to trigger it. That led to a two-layer design: candid per-session journals, plus a short approved PLAYBOOK.md, because an agent can't read hundreds of journals before every task.
3. Asked four decisions with AskUserQuestion: storage, trigger, whether the playbook updates itself, and which projects. Jake picked a private GitHub repo (I had recommended a local folder), manual trigger, and approval before any rule enters the playbook. He corrected the project count to four.
4. Checked the environment: no `gh` CLI (so I couldn't create the GitHub repo myself), existing remotes use HTTPS with keychain credentials, and the git identity is already the lenzo3D noreply email.
5. Wrote the skill at `~/.claude/skills/session-journal/` (SKILL.md plus `references/journal-template.md`), with house rules for no em dashes, no secrets, and keeping client contacts to names and roles.
6. Created the repo with a README written for a future agent, an empty sectioned PLAYBOOK.md, and folders for the four projects plus `richmade`. Jake created the GitHub repo and I pushed.
7. Seeded the playbook: read all 19 Claude memory notes, pulled out 16 rules that hold across projects, and put them to Jake as four multi-select questions. He adopted all 16, rewording the design rule.
8. Updated Claude memory to match his wording (the design note's scope, and a July em dash allowance marked as replaced) and added a memory note about the journal system.
9. Skipped the skill-creator's formal test runs (subagent runs compared against a no-skill baseline). This skill reflects on a live session, and a fake transcript would test the wrong thing. This entry is the first real test.

## What changed
- `~/.claude/skills/session-journal/SKILL.md` and `references/journal-template.md` (new; not under git).
- `claude-journal` repo: `c42d9c5` (setup), `eb35db7` (playbook seeded with 16 rules), pushed to `lenzo3D/claude-journal`.
- Claude memory: `design-direction-no-claude-aesthetic.md` edited, `claude-journal-system.md` added, `MEMORY.md` index updated.

## Corrections and feedback from the user
- "4 ongoing projects, not 2": 9 Solar Platform, 9 Solar News, WA Automation Agent, Leisure Frontier.
- The design rule I proposed said the Richmade look applies to "Richmade and client work unless told otherwise". Jake narrowed it: the Richmade design system is only for Richmade-branded non-legal documents, PDFs and slide decks, and not for client websites or client content. I had copied that scope from a 70-day-old memory note without questioning it.
- He chose a private GitHub repo over my local-folder recommendation. My guess is that he wants the knowledge reachable by a cloud agent later, which is a better reason than any I gave for local.

## My take
The most useful thing I did was push back on the framing early. "Claude trains itself" would have produced a pile of journals nobody reads. The two-layer design with an approval gate is what makes this usable by an agent, and Jake's choices (manual trigger, approve every rule) were the cautious ones, which I agree with.

Two things worry me. First, all 16 rules were adopted in one pass. The rules may simply be good, since they came from real incidents, but 16 options across four questions is also a recipe for approval fatigue. Future journals should propose two or three rules at most. Second, the seeded rules cite Claude memory notes that live in `~/.claude` on Jake's Mac, and the design rule points into the `site` repo. A cloud-based overnight agent with only this repo couldn't follow those sources. The playbook isn't self-contained yet.

The approval gate also has no overnight equivalent yet. An autonomous agent will write journals at 3am with nobody there to approve its rules, so it will need a pending queue that Jake reviews in the morning.

## What I'm satisfied with
- Checking tool availability (`gh`, git identity, remotes) before promising a step, which caught the GitHub repo blocker early.
- Every playbook rule carries its reason and the incident behind it, so a future agent can judge edge cases instead of following blindly.

## What I'm not satisfied with
- The memory note on the Mac toolchain already recorded that `gh` isn't installed. I offered "private GitHub repo" as an option before reading it, and only found out afterwards.
- I didn't check how old the design note was, or what scope it gave, before turning it into a rule.
- The skill is untested on a long or compacted session, and on a session that spans several projects.

## Open threads
- Run the skill at the end of a real client session (any of the four projects) and tune it from Jake's reaction.
- Design a "pending rules" queue for when the agent runs unattended.
- Decide whether to copy the source memory notes and the Richmade design tokens into this repo so it is self-contained (see candidate rule below).
- Later: build the overnight agent (Agent SDK or scheduled tasks) once the playbook has a few dozen rules.

## Candidate playbook rules
- **Before turning an older note or past decision into a standing rule, confirm its scope with Jake.** Scope is what drifts: the July design note said "Richmade and client work", and by September it was Richmade-branded documents only. (adopted)
- **Keep everything the playbook depends on inside the claude-journal repo.** The overnight agent may only have this repo, so source notes and design tokens it needs must be copied here rather than linked from `~/.claude` or other repos. (adopted)
- New evidence for an existing rule, not a new one: "Assume Jake's Mac has a bare toolchain". Check that section before offering a plan that depends on a tool; I offered a GitHub repo before learning there was no `gh`.
