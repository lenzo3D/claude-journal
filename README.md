# claude-journal

Richmade's working memory. Every meaningful Claude session on a client or agency project ends with a journal entry here: what was asked, how the work was done, what changed, what the user corrected, and Claude's honest view of it. The lessons that hold across projects are distilled into `PLAYBOOK.md` once Jake approves them.

It is written for an autonomous agent that will eventually run whole projects on its own. Everything that agent needs is in this repo, including the skill that writes the journals.

## If you are an agent starting work

1. Read `PLAYBOOK.md` in full. Those rules are the SOP. Where a rule conflicts with your defaults, the rule wins.
2. Read `projects/<slug>/README.md` for the project you are working on, then its three most recent journals.
3. Search the other projects' journals for a similar task (`grep -ril "<keyword>" projects`) and follow the workflow that worked there.
4. `PENDING.md` holds proposed rules that are **not** approved. Don't follow them. `REJECTED.md` holds rules Jake turned down. Don't propose them again without new evidence.
5. When you finish, write a journal entry using `skill/session-journal/SKILL.md`. If you are running unattended, it sends new rule proposals to `PENDING.md` instead of the playbook. Never edit `PLAYBOOK.md` without Jake's approval in the same session.

## Layout

```
PLAYBOOK.md                        approved rules, grouped by section (in force)
PENDING.md                         proposed rules waiting for Jake (not in force)
REJECTED.md                        rules Jake turned down (don't re-propose)
projects/<slug>/README.md          index of journals, newest first
projects/<slug>/journals/*.md      one entry per session
projects/<slug>/checkpoints/*.md   one line per commit-and-push, per day (read at wrap-up)
reference/                         material the rules depend on, copied in from other repos
reference/sops/                    SOP and process documents written in sessions
reference/repo-docs/               copies of project repos' CLAUDE.md files
reference/sources.json             where each copy came from, and at which commit
scripts/check-sources.py           reports copies whose original has changed since
scripts/lint.py                    house-rule check (em dashes, secrets); run before every commit
skill/session-journal/             the skill that writes journals (symlinked into ~/.claude/skills on Jake's Mac)
```

## How a rule gets into the playbook

1. A session's journal lists candidate rules.
2. If Jake is present, he approves or rejects them there and then.
3. If he isn't (an overnight run, or he said "decide later"), they go to `PENDING.md`. When several sessions propose the same rule, it collects more evidence links instead of being duplicated.
4. Jake says "review pending rules" in any session. Adopted rules move to `PLAYBOOK.md`, rejected ones to `REJECTED.md`.

## Setting up a machine to run as Richmade's agent

1. Clone this repo and symlink `skill/session-journal` into `~/.claude/skills/session-journal`.
2. Put the contents of `reference/setup/global-CLAUDE.md` into that machine's `~/.claude/CLAUDE.md`. Without it, everyday moments (commits, preferences, SOPs, CLAUDE.md edits, weekly wraps) are only logged some of the time, because a skill description alone can't reliably trigger after another task.
3. Allow at least `Bash(git:*)` and `Bash(python3:*)` for scheduled runs. The skill's commands are written to need nothing more.

## House rules

- No em dashes anywhere in this repo.
- No secrets: keys, tokens, passwords and `.env` contents are referred to by name only.
- Absolute dates only.
