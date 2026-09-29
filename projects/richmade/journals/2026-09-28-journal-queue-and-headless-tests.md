---
date: 2026-09-28
project: richmade
topic: Self-contained playbook, pending-rules queue, headless tests and trigger tuning
outcome: shipped
satisfaction: 4/5
model: Claude Opus 5.5
run: attended
related: [richpilot]
---

# Self-contained playbook, pending-rules queue, headless tests and trigger tuning

Second half of the session that built the session-journal skill (first entry: `2026-09-28-session-journal-skill.md`). Work ran on 28 Sep 2026; Jake wrapped up just after midnight on 29 Sep.

## The ask
1. Make the playbook self-contained, so an agent holding only this repo can follow every rule.
2. "Help me decide how unattended rules get approved, find a solution and implement it right away."
3. Later: "carry on where you left off and finish off this skill", including the steps that were blocked while the `claude` CLI was logged out.

## What I did
1. Fixed a broken link first. My report linked the first journal with a path relative to the journal repo, and the app resolved it from `AI Agency`, so Jake got "Couldn't find this file". I sent the file directly and changed the skill to always do that.
2. Applied a rename that arrived from another Claude session: WA Automation Agent is now Richpilot. I renamed the project slug to `richpilot` in the repo, skill and memory, and left the memory-note citations in the playbook alone, because that note file still has its old name.
3. Self-contained playbook: copied the Richmade design system into `reference/` (values from `site/css/styles.css`, decisions from `DESIGN_BRIEF.md`, both font files) and added `reference/sources.json` plus `scripts/check-sources.py` to flag drift. I chose not to copy the raw memory notes, since each rule already carries its incident and the notes hold client pricing. Then I moved the skill itself into the repo (`skill/session-journal/`) and symlinked it back into `~/.claude/skills`, because an overnight agent needs the skill as much as the rules.
4. Unattended approval: I recommended and built a pending queue (`PENDING.md`) with a rejects log (`REJECTED.md`). Unattended runs may never edit `PLAYBOOK.md`, repeat proposals collect evidence instead of duplicating, and Jake clears the queue with "review pending rules". GitHub pull requests are the upgrade path once a cloud agent exists.
5. Tested the queue with a subagent acting as an overnight run on a scratch clone, then tested the morning review twice with subagents asked to list every instruction they had to guess at. The first review test found 11 ambiguities (rejected rules lost their Why, journal markers lost the rule ID, mismatched placeholders, nothing stopping an unattended run from clearing the queue). I fixed them, and the second test came back with only two small wording points.
6. After Jake logged back in, I ran real headless `claude -p` overnight-style runs. The first showed that `$(...)` and `cd ... &&` commands get blocked without approval. I replaced the em dash grep with `scripts/lint.py` (em dashes plus secret-looking strings), switched the git steps to `git -C`, and reran: zero blocked commands, about US$0.43 per run, and the skill triggered from "wrap up and journal this run".
7. Trigger tuning with skill-creator's `run_loop`. I drafted 20 test messages. Jake flipped six of the "should not trigger" ones. I checked rather than tuning straight to them: one was a mis-click (the journal-style news article), and five were a real product decision, which he settled as "do it, then log it" (commit and push, remember a preference, write an SOP, edit a CLAUDE.md, weekly wrap). I added a "Capturing moments" section and a per-day `checkpoints/` log.
8. The first tuning run scored 0% recall. I ran one message by hand and found two harness problems: it counts a run as "no trigger" if Claude's first tool isn't Skill (headless Opus 5.5 looks around with Bash first), and it ran in a folder where Claude could read the answer sheet. I patched a copy, ran it from an empty folder, and confirmed on 4 messages that it worked. The second full run still scored near zero, and one round took 72 minutes. Three messages run one at a time all behaved correctly, so the cause was throttling of 10 parallel Opus sessions on Jake's plan. I stopped tuning and kept the hand-written description.
9. The tests also showed that a skill description can't reliably fire *after* another task: "remember that..." and "commit and push" never opened the skill. With Jake's yes, I created `~/.claude/CLAUDE.md` (he had none) with a standing instruction, retested, and both now open the skill after finishing the task. He declined a git-push hook. A copy lives at `reference/setup/global-CLAUDE.md`, drift-checked by content, with a three-step machine setup in the README.

## What changed
- `claude-journal`: `b43ee15` (Richpilot rename), `64193fd` (reference/, queue, skill moved in), `11ce656` (review-flow fixes), `e722b24` (lint.py, headless-safe commits), `f31c2c4` (capturing moments, checkpoints), `59e375e` (setup notes, global instruction copy, content drift check). All pushed to `lenzo3D/claude-journal`.
- Outside the repo: `~/.claude/skills/session-journal` is now a symlink; `~/.claude/CLAUDE.md` created; Claude memory note `claude-journal-system.md` updated several times.
- Nothing touched any client repo. Every test ran on scratch clones, and I checked the real repo was clean after each one.

## Corrections and feedback from the user
- The broken link, shown as a screenshot of "Couldn't find this file".
- On the first journal: "exactly what i was looking for, perfect length etc." That entry is now the skill's reference for tone and depth.
- "What does self-contained playbook mean". I had used the term without explaining it.
- The six eval flips, resolved into "do it, then log it" plus one mis-click.
- Chose the global CLAUDE.md line and declined the git-push hook.

## My take
The subagent and headless tests earned their cost. Each found problems that reading the skill never would have: 11 ambiguities in the review flow, blocked commands, and the fact that after-task triggers need a standing instruction. The design is now properly layered: the description handles "wrap up", CLAUDE.md handles the moments after other tasks, and the queue handles approval.

The description tuning was a mistake in how I ran it. I launched a 20-message, 3-round batch without first checking the harness on a handful of messages. It cost roughly 20 minutes, then another 90, plus plan usage, to learn nothing about the description. I did the 4-message check before the second run but not the first. I also didn't think about parallel runs on a subscription plan being throttled.

Checking Jake's eval flips instead of obeying them was the best call of the session. Tuning to all six would have made the journal skill take over requests for news articles, and the widening of scope was a product decision that needed his answer, not a label change.

One risk I created and didn't fully close: `~/.claude/CLAUDE.md` applies to every session on this Mac, not just Richmade ones. A commit in a non-Richmade repo (the ESGX hackathon, for example) could get logged into Richmade's journal. The instruction says "a project repo", which is loose.

## What I'm satisfied with
- The queue design: simple files, no infrastructure, an evidence count to show which rules keep recurring, and a rejects log to stop nightly re-proposals.
- Verifying from transcripts, not from agents' reports: I confirmed the skill really triggered by reading the `Skill` tool calls in the headless session files.

## What I'm not satisfied with
- Burned usage on the tuning without a smoke test first.
- The global CLAUDE.md scope is too loose (see above).
- The patched eval harness lives only in the session scratchpad, so re-tuning would mean patching again.

## Open threads
- Narrow `~/.claude/CLAUDE.md` to Richmade repos (the four project folders and `AI Agency/`), and update `reference/setup/global-CLAUDE.md` to match.
- Overnight agent: pick a scheduler (Agent SDK or scheduled tasks) and a login method. The CLI login expired once on 28 Sep, and an expired login stops scheduled runs silently.
- Only if "wrap up" misses in practice: re-tune the description sequentially (`--num-workers 1`) with the patched harness.

## Candidate playbook rules
- **Before any long or expensive batch run (evals, bulk migrations, agent fan-outs), run it on 3 or 4 items first and check the result is plausible, and keep parallel runs low on Jake's plan.** The first description-tuning run reported 0% recall from a broken harness; a 4-item check found the bug in two minutes, and 10 parallel Opus sessions got throttled into a 72-minute round. (adopted)
- **When something must happen after another task (logging, cleanup, a notification), put it in a standing instruction or hook, not only a skill description.** Claude picks skills at the start of a request; in headless tests "remember" and "commit and push" only opened the journal skill once the global CLAUDE.md line existed. (adopted)
- **When Jake's input would change what a system does, not just how well it does it, confirm the intended behaviour before building or running anything at scale.** Six flipped eval labels were really a scope decision ("do it, then log it") plus one mis-click; tuning straight to them would have made the journal skill take over article writing. (adopted)
- New evidence for "Don't call anything done without direct evidence": a subagent simulating an overnight run passed, but only a real headless run exposed the blocked commands.
