# Rejected rules

Rules Jake decided not to adopt. They are kept so that no agent proposes the same rule again, night after night.

Don't re-propose a rule listed here unless a session produces genuinely new evidence. If one does, add it to `PENDING.md` with a link to this entry and a short note on what's new.

Entry format (newest at the bottom):

```
### P-YYYY-MM-DD-NN · Short title
- **Rule:** the proposed instruction
- **Why:** the reason it was proposed
- **Section:** the PLAYBOOK.md section it would have gone in
- **Evidence:** the journal links from the pending entry
- **Rejected:** YYYY-MM-DD. Jake's reason in his own words, naming any playbook rule it refers to
```

## Rejected

### P-2026-09-30-01 · Check where users work before speccing an integration
- **Rule:** Before speccing an integration with a third-party app, establish where the client's staff will work day to day, and check whether that app can live there (embedding, iframe and plan limits).
- **Why:** HubSpot blocks iframes, which only surfaced after a full spec and 16-task plan, and the direction was shelved.
- **Section:** Project process
- **Evidence:** [richpilot/2026-09-30](projects/richpilot/journals/2026-09-30-name-hubspot-pivot-crm-plan.md)
- **Rejected:** 2026-09-30. No reason given.

### P-2026-10-08-01 · Stop on a permission denial
- **Rule:** When a permission check denies a step, stop and put the decision to Jake; never retry it through another tool or another agent.
- **Why:** Four denials across Richpilot 3c1 and 3c2 (a browser step, a SQL restore, a record write, a staging sign-in) were each stopped and surfaced, and one answer from Jake unblocked the rest of the 3c2 run without anyone working around the check.
- **Section:** Never do
- **Evidence:** [richpilot/2026-10-08](projects/richpilot/journals/2026-10-08-crm-3c2-import-export-delete-and-production.md), [richpilot/2026-10-08 (3c1)](projects/richpilot/journals/2026-10-08-crm-3c1-settings-build-and-production-migration.md)
- **Rejected:** 2026-10-08. No reason given.
