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

### P-2026-10-08-01 · Stop on a permission denial
- **Rule:** When a permission check denies a step, stop and put the decision to Jake; never retry it through another tool or another agent.
- **Why:** Four denials across Richpilot 3c1 and 3c2 (a browser step, a SQL restore, a record write, a staging sign-in) were each stopped and surfaced, and one answer from Jake unblocked the rest of the 3c2 run without anyone working around the check.
- **Section:** Never do
- **Proposed by:** session, decision deferred (not chosen when the other two were adopted)
- **Evidence:** [richpilot/2026-10-08](projects/richpilot/journals/2026-10-08-crm-3c2-import-export-delete-and-production.md), [richpilot/2026-10-08 (3c1)](projects/richpilot/journals/2026-10-08-crm-3c1-settings-build-and-production-migration.md)
