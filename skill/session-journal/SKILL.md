---
name: session-journal
description: Write an end-of-session journal entry reflecting on the whole session (what the user asked, the workflow Claude followed, what changed, the user's corrections, Claude's candid opinion, what went well and badly), save it to the claude-journal repo under the right project, then propose new playbook (SOP) rules, which the user approves on the spot or which wait in a pending queue when nobody is around. Use this whenever the user says "wrap up", "journal this", "log this session", "end of session", "write the journal", "/session-journal", "reflect on this session", or signals they are done and want the work documented, even if they never say the word "journal". Also use when an unattended or overnight run finishes its work, and when the user asks to "review pending rules" or to review, update, or add to the playbook or SOP built from past sessions.
---

# Session Journal

Richmade (Jake's AI agency) is building a knowledge base from its real project work. The end goal is an autonomous agent that runs whole client projects overnight, using what was learned here as its SOP: what to do, in what order, and what never to do.

Your underlying model does not change when you write a journal. The learning happens through this repo, which a future agent reads before it starts work. So write for that reader: an agent with none of this session's context, who needs to know how Jake and Claude actually work, and why.

The repo has three layers:

- **Journals**: one per session, candid and specific. The raw record.
- **PLAYBOOK.md**: short, distilled rules that hold across projects. This is the SOP the agent follows. It only grows with Jake's approval, because one wrong rule repeated by an autonomous agent is expensive.
- **PENDING.md / REJECTED.md**: rules waiting for Jake's decision, and rules he turned down.

## The repo

On Jake's Mac: `~/Documents/AI Agency/claude-journal/` (private GitHub remote `lenzo3D/claude-journal`). This skill's own files live inside that repo at `skill/session-journal/`, and `~/.claude/skills/session-journal` is a symlink to them. So on any other machine, the repo root is two folders above this file.

```
claude-journal/
├── README.md                 how an agent should use this repo
├── PLAYBOOK.md               approved rules, grouped by section (in force)
├── PENDING.md                proposed rules waiting for Jake (not in force)
├── REJECTED.md               rules Jake turned down (don't re-propose)
├── reference/                material the rules depend on, copied from other repos
├── scripts/check-sources.py  reports reference copies whose original changed
├── skill/session-journal/    this skill
└── projects/<slug>/
    ├── README.md             one line per journal, newest first
    └── journals/YYYY-MM-DD-<topic>.md
```

Project slugs (create a new one if the session fits none):

| Slug | Project |
|---|---|
| `9solar-platform` | 9 Solar platform build and the universe pitch demo (`AI Agency/9solar`) |
| `9solar-news` | Red Dot News / 9 Solar News site and AI newsroom (`AI Agency/9SolarNewsWebsite`) |
| `richpilot` | Richpilot, Richmade's automation platform (formerly WA Automation Agent): WhatsApp, orders, voice modules (`~/Desktop/Agents/Richpilot`, github lenzo3D/richpilot) |
| `leisure-frontier` | Leisure Frontier site, SEO/GEO, enquiries (`AI Agency/leisure-frontier`) |
| `richmade` | Agency operations, the Richmade site, internal tooling and skills |

If the session touched several projects, file it under the main one and mention the others in the entry. If you can't tell which project it was, ask. If you're unattended, pick the closest one and say in the entry that you weren't sure.

## Attended or unattended?

Decide this first, because it changes step 4.

- **Attended:** Jake (or another Richmade person) is in the conversation and can answer questions.
- **Unattended:** a scheduled task, a headless `claude -p` run, an Agent SDK job, or any run where the prompt says nobody is available, or where AskUserQuestion isn't available. Also treat the run as unattended if Jake asks you to wrap up and then says he'll decide on rules later.

When unattended, never edit `PLAYBOOK.md`. Every proposed rule goes to `PENDING.md` instead. That queue is the only thing standing between an agent's guess and the SOP every future run follows.

## Workflow

### 1. Gather the facts before writing

Reconstruct the session from the conversation, including any compaction summary. Then check the facts instead of relying on recall:

- For every repo you touched, run `git status` and `git log` for this session's commits so the "What changed" list is accurate (commit hashes, files, test counts).
- Note anything outside the filesystem that changed: deploys, database migrations, emails drafted, artifacts published, settings changed.
- Pull out every correction the user made, close to their own words. These are the most valuable part of the journal, because corrections are exactly where Claude's defaults differ from how this agency works.
- Run `python3 scripts/check-sources.py` from the repo root. If it reports a STALE copy (for example, the Richmade site's design tokens changed), refresh it when attended and the change is clear. Otherwise list it under "Open threads".

If the context was compacted and a detail is gone, say so in the entry. A journal that invents details teaches the future agent something false.

### 2. Write the entry

Save it to `projects/<slug>/journals/YYYY-MM-DD-<short-topic>.md` using the template in `references/journal-template.md`. If a file with that name already exists (a second session on the same day), add `-2`.

How to write it:

- **First person, candid.** Your opinion is wanted: whether the approach was right, whether the user's call was right, what you'd push back on. Don't flatter the user or yourself. "I shipped a fix that reopened the bug because I didn't retest the extra guard I added" is worth ten "the session went smoothly" lines.
- **Specific over general.** Name the files, commands, numbers and decisions. "Ran `npm run lint` myself and caught a broken link neither subagent saw" is reusable. "Was thorough with testing" isn't.
- **Write the workflow as steps.** The "What I did" section is the raw material for SOPs. Record the real order, including dead ends and why you left them.
- **Scale it to the session.** A 20-minute fix might need 250 words. A day-long build might need 1,000. Leave out filler sections rather than padding them. `projects/richmade/journals/2026-09-28-session-journal-skill.md` is the entry Jake approved as the right tone and depth.
- **Use absolute dates** (28 Sep 2026, not "today"). In IDs, file names, index lines and the PENDING/REJECTED files, use `YYYY-MM-DD`.
- **Unattended runs:** say so in the frontmatter (`run: unattended`), and state plainly any decision you made that Jake would normally have made.

### 3. House rules for everything written into this repo

- **No em dashes** (the U+2014 character). The agency treats them as a tell of AI writing. Use commas, colons, parentheses, or separate sentences, whichever fits that sentence. Check before you commit (step 6).
- **No secrets.** Leave out API keys, tokens, passwords, connection strings, bank or card details, and the contents of `.env` files. Refer to them by name ("the staging `TOKEN_ENCRYPTION_KEY`"). The repo is private, but it gets pushed to GitHub and will be read by agents.
- **Keep client people to their roles.** Use names and roles where they help ("Kerr Sun, the 9 Solar founder, closed at S$9,999"). Leave out personal phone numbers, emails and addresses.

### 4. Propose playbook rules

Read `PLAYBOOK.md`, `PENDING.md` and `REJECTED.md` first. Then pick out candidate rules from this session that would hold on another project or client. Good candidates come from user corrections, from mistakes you caught (or didn't catch), and from workflows that worked well enough to repeat.

For each candidate:

- Write it as an instruction with its reason: **Rule.** Why it matters.
- **Already in PLAYBOOK.md:** don't add it. If this session is new evidence for the rule, or contradicts it, say so in the journal.
- **Already in PENDING.md:** don't duplicate it. Add this journal to that entry's **Evidence** list. A rule several sessions arrive at on their own is a strong candidate, and the evidence count shows Jake that.
- **In REJECTED.md:** don't re-propose it unless this session is genuinely new evidence. If it is, propose it again with a link to the rejection and a note on what's new.
- Leave out project-specific facts ("LF staging ref is X"). Those belong in the journal, not the SOP.
- Propose three at most, and keep the strongest. Long lists invite rubber-stamping.

List the candidates in the journal's last section. What happens next depends on whether anyone is there.

**Attended:** ask Jake which to adopt, using AskUserQuestion with `multiSelect: true`. Put the full rule text in the option description so he can judge it without scrolling. Also offer a "Decide later" option.

- **Approved:** append the rule to the right section of `PLAYBOOK.md` in the format that file shows, with a source link to the journal. Mark it `(adopted)` in the journal.
- **Rejected:** give it an ID (`P-YYYY-MM-DD-NN`), add it to `REJECTED.md` in that file's format (with his reason, if he gave one), and mark it `(not adopted, P-...)` in the journal.
- **Reworded:** use his wording.
- **Decide later**, or no answer: treat it as unattended (below).

**Unattended:** add each candidate to `PENDING.md` under "Waiting for review", in the format that file shows, with an ID `P-YYYY-MM-DD-NN`. Remove the "_None._" placeholder if it's there. Mark it `(pending, P-...)` in the journal. Don't follow your own pending rules later in the run. They aren't in force until Jake says so.

If the session produced nothing that generalizes, say so and skip this step. Don't invent rules to fill the section.

### 5. Update the project index

Add a line at the top of the list in `projects/<slug>/README.md` (create the file from the pattern in an existing project if needed):

```
- 2026-09-28 · [Short topic](journals/2026-09-28-short-topic.md) · outcome · one-line summary
```

### 6. Commit and push

```bash
cd <repo root>
grep -rn "$(printf '\342\200\224')" --exclude-dir=.git --exclude-dir=fonts .   # finds em dashes; must print nothing
git add -A
git commit -m "journal: <slug> <YYYY-MM-DD> <topic>"
git push
```

Commit with the repo's existing git identity (the lenzo3D noreply address), and follow the session's commit attribution instructions for the trailer. If the repo has no remote, skip the push and say so. If the push fails (no network, expired credentials), leave the commit in place and tell the user. Don't retry in a loop.

### 7. Report back

Keep it to a few lines: where the entry was saved, which rules were adopted or queued, and whether the push worked. If `PENDING.md` has entries waiting, say how many and offer to review them now. Don't paste the journal into chat. It lives in the repo.

Give the user the entry itself, not a relative link. The app resolves relative links from the session's working folder, which is usually not the journal repo, so a link like `projects/richmade/journals/...` opens as "Couldn't find this file". If a file-sending tool (SendUserFile) is available, send the entry with it. Otherwise give the full absolute path. When unattended, put the summary in the run's final output instead.

## Reviewing pending rules

When Jake says "review pending rules" (or similar), or accepts the offer in step 7.

Every decision must come from Jake in this session. An unattended run never clears the queue, however obvious a rule looks.

1. Read `PENDING.md`. If it's empty, say so and stop.
2. Present the entries with AskUserQuestion, `multiSelect: true`, at most 4 per question. Put the rule, its reason and its evidence count in each option's description. List the entries with the most evidence first.
3. Apply each decision:
   - **Adopted:** append the rule to the right section of `PLAYBOOK.md`. Cite every journal in its evidence list: `_(source: [richmade/2026-09-28](...), [richpilot/2026-10-02](...))_`.
   - **Rejected:** move the entry's Rule, Why, Section and Evidence lines to the bottom of `REJECTED.md` (drop **Proposed by**) and add a **Rejected:** line with the date and Jake's reason, quoted in his own words. If his reason refers to a playbook rule, name that rule after the quote. If it isn't clear which rule he means, ask him. The full entry matters, because a later agent needs the Why to judge whether new evidence is really new.
   - **Reworded:** adopt his wording.
   - **Not chosen and not rejected:** ask whether to reject it or keep it pending. Don't guess.
4. Remove decided entries from `PENDING.md`. In each source journal, change `(pending, P-...)` to `(adopted, P-...)` or `(not adopted, P-...)`, keeping the ID so the trail from journal to decision survives. Leave project index lines alone; they're a historical record.
5. Keep the placeholders consistent: both files show `_None._` when their list is empty. Remove it when adding the first entry, and put it back when removing the last.
6. Commit (`playbook: review pending rules YYYY-MM-DD`) and push, as in step 6.
7. Tell Jake in a few lines what was adopted, what was rejected, and what is still pending.

## Other requests

- **"What's in the playbook?" / "review the SOP"**: read PLAYBOOK.md and summarise it by section. Point out rules that conflict or have gone stale.
- **"What did we learn on <project>?"**: read that project's README.md and recent journals and summarise the patterns across them.
- **Claude Code memory** (`~/.claude/projects/.../memory/`) is a separate system that helps Claude recall things during sessions. Don't edit it from this skill unless the user asks. A rule can live in both places.
