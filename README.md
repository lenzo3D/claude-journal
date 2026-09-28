# claude-journal

Richmade's working memory. Every meaningful Claude session on a client or agency project ends with a journal entry here: what was asked, how the work was done, what changed, what the user corrected, and Claude's honest view of it. The lessons that hold across projects are distilled into `PLAYBOOK.md` once the user approves them.

It is written for an autonomous agent that will eventually run whole projects on its own.

## If you are an agent starting work

1. Read `PLAYBOOK.md` in full. Those rules are the SOP. Where a rule conflicts with your defaults, the rule wins.
2. Read `projects/<slug>/README.md` for the project you are working on, then its three most recent journals.
3. Search the other projects' journals for a similar task (`grep -ril "<keyword>" projects`) and follow the workflow that worked there.
4. When you finish, write a journal entry of your own in the same format.

## Layout

```
PLAYBOOK.md                        approved rules, grouped by section
projects/<slug>/README.md          index of journals, newest first
projects/<slug>/journals/*.md      one entry per session
```

Entries are written by the `session-journal` skill (`~/.claude/skills/session-journal/`).

## House rules

- No em dashes anywhere in this repo.
- No secrets: keys, tokens, passwords and `.env` contents are referred to by name only.
- Absolute dates only.
