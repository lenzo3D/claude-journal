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

### P-2026-10-18-01 · Standing yes to push and deploy, per project
- **Rule:** When Jake gives a standing yes for a project ("stop making me approve push main, just do it yourself"), push `main` and run that project's deploy yourself after tests pass, without asking each time. Still fetch and rebase first and report each push and deploy. The standing yes covers only pushing and deploying in that project: not client messages, the kill switch, or paid runs.
- **Why:** On 9 Solar News, Jake had approved pushes and run `npx wrangler deploy` by hand over 10 times in one session and called it "incredibly inefficient". This narrows the "explicit yes for that specific action" safety rule in Working with Jake for a project where he has granted a standing yes.
- **Section:** Working with Jake
- **Proposed by:** Jake's stated preference (18 Oct 2026, 9 Solar News)
- **Evidence:** [9solar-news/2026-10-18 checkpoint](projects/9solar-news/checkpoints/2026-10-18.md)
