# Journal entry template

Copy this structure. Drop any section that would be empty or filler, except "The ask", "What I did", "My take" and "Candidate playbook rules", which every entry keeps.

```markdown
---
date: 2026-09-28
project: richpilot
topic: Admin page for picking client modules
outcome: shipped | partial | blocked | exploratory
satisfaction: 4/5
model: Claude Opus 5.5
run: attended | unattended
related: [leisure-frontier]
---

# Admin page for picking client modules

## The ask
What the user wanted, in their words where it matters, plus the goal behind it if they gave one.
Note any constraints they set ("never push main without my yes").

## What I did
1. Numbered steps in the order they actually happened.
2. Include tools, skills and subagents used, and why.
3. Include dead ends: what I tried, why it failed, what I switched to.

## What changed
- `repo/path/file.ts`: what changed (commit `abc1234`)
- Outside the repo: deploys, migrations, emails, artifacts, settings.
- Tests: before → after count, and whether they pass.

## Corrections and feedback from the user
- What they corrected, close to their words, and what I had done before it.
- Why they wanted it, if they said (or my best guess, labelled as a guess).

## My take
My honest opinion of the session: whether the approach was right, where the user's direction was
strong or where I'd push back, what surprised me, and the risks I see ahead.

## What I'm satisfied with
Specific things that went well and are worth repeating.

## What I'm not satisfied with
What went badly or is still weak, including my own mistakes, and what I'd do differently.

## Open threads
- Next steps, blockers, and anything only a human can do (accounts, payments, approvals).

## Candidate playbook rules
- **Rule as an instruction.** Why it matters. (adopted | not adopted | pending, P-2026-09-28-01)
```

## Example of the level of detail wanted

Weak:
> Fixed the spend cap bug and tested it.

Strong:
> The round-1 fix for the spend-cap typo added `type="number"` to the input as a defensive extra. That quietly reopened the bug: the browser sanitises "1e" to an empty string, which the API reads as "no cap". An independent re-review caught it. I confirmed it live on staging by typing "1e" into the field before and after the second fix. Lesson: a defensive extra added by a fix needs the same scrutiny as the fix itself.
