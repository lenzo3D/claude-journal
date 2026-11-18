# Pending rules

Rules proposed for the playbook that Jake hasn't decided on yet. **None of these are in force.** Don't follow them as rules, and don't copy them into `PLAYBOOK.md` yourself.

Rules land here when nobody is available to approve them: an unattended or overnight run, or a session where Jake chose "decide later". Jake reviews them by saying "review pending rules" in any Claude Code session. Adopted rules move to `PLAYBOOK.md`, rejected ones to `REJECTED.md`, and either way the entry is removed from this file.

Before adding an entry, check `PLAYBOOK.md`, this file, and `REJECTED.md`. If the same rule is already pending, don't duplicate it: add your journal to its **Evidence** list. Rules that several sessions arrive at on their own are the strongest candidates.

Entry format (newest at the bottom):

```
### P-YYYY-MM-DD-NN · Short title
- **Rule:** the instruction, as it would appear in the playbook
- **Why:** the reason, with the incident behind it
- **Section:** which PLAYBOOK.md section it belongs in
- **Proposed by:** unattended run | session, decision deferred
- **Evidence:** [project/date](projects/slug/journals/file.md), then one more link per session that arrives at the same rule
```

## Waiting for review

### P-2026-11-18-01 · Build on Sonnet, plan and judge on Opus
- **Rule:** When executing an approved plan, dispatch the implementer and reviewer agents on Sonnet 5.5; keep planning, rulings and the final go or no-go in the main session.
- **Why:** cost. Jake, 18 Nov 2026: "remember if doing a build, build with sonnet 5.5".
- **Section:** Working with subagents (or the closest section)
- **Proposed by:** Jake's stated preference
- **Evidence:** [9solar-news/2026-11-18](projects/9solar-news/checkpoints/2026-11-18.md)
