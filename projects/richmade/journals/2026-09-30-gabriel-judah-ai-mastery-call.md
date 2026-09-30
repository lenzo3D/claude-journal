---
date: 2026-09-30
project: richmade
topic: Gabriel Judah AI mastery call, company harness and second brain
outcome: exploratory
satisfaction: 3/5
model: Claude Sonnet 5.5
run: attended
related: [richpilot, leisure-frontier]
---

# Gabriel Judah AI mastery call, company harness and second brain

## The ask
Jake pasted the full Fathom transcript of an impromptu Zoom on 30 Sep 2026 (125 minutes, run by Gabriel Judah with a guest, Mark) and asked me to process it and run the session journal. The transcript is a sales webinar about running a company on AI agents. No code was written and no repo was touched. This entry is the processed record of the call, filed under `richmade` because it is agency strategy, not one client build.

## What I did
1. Read the whole transcript, separating the speaker's content (labelled "Speaker 1") from lines labelled Jake Loh. Jake's lines are not part of the webinar. He was dictating tasks to another Claude session while the call played, and Fathom captured the dictation.
2. Ran `scripts/check-sources.py` (all three reference copies OK) and read PLAYBOOK, PENDING and REJECTED so I would not duplicate a rule.
3. Wrote this entry and the index line. I did not verify any of the speaker's claims, because nothing in the session could check them.

## What the call taught (the useful part)
**The "company harness" framing.** The speaker's central idea is that the model is a swappable engine and what a company owns is the harness: a brain (knowledge store), AI employees each with a written job, skills (SOPs an agent can run), and contracts (guardrails and standards for "done"). His pitch is that an agent without a job description and a brain is an intern on day one, every day. This is close to what Richmade is already building with the claude-journal repo (brain), PLAYBOOK (skills and contracts) and Richpilot (employees), so it gives us vocabulary for pitching, not a new architecture.

**The CLOSE loop for a second brain.** Capture (a nightly job pulls WhatsApp, Slack, email, meetings and Drive into an inbox), Link (an overnight pass connects notes about the same person or deal), Organize (triage into folders, PARA plus an inbox), Signal (a weekly or daily pass distils what moved and flags it, for example a burnt-out staff member or a lag that changed 25%), Execute (outputs like briefs, replies and scripts are better because of the signal, then get recaptured). The distinctive part is Signal: sorting notes is not learning, so a scheduled agent must read everything and say what it means. Our journal repo covers Capture and Organize for our own work but has nothing at Signal yet.

**Five starter agents, mapped to five business pillars.** Attract (media buyer, content), Convert (sales follow-up, with a rule to contact new leads within 60 seconds), Deliver (client success), Run the office (chief of staff, morning brief), Count the money (finance, invoice collection). Mark's "time and energy audit" is a simple client discovery tool: list every task, minutes spent, and a 1 to 5 score for how much energy it gives, then automate the ones and twos first. That is directly reusable in Richmade discovery calls.

**Operating claims worth copying.** Skills are the same SOPs a company always needed, written so an agent can run them. A separate "skills agent" reads other agents' results and rewrites their SOPs. Model-agnostic setups (he uses the open-source Hermes agent) beat platform-locked ones because the best model changes monthly. Give agents limited debit cards, not a real card. Prefer a WhatsApp API or a CRM that hosts WhatsApp over unofficial WhatsApp automation, because unofficial use gets numbers banned. Store agent personas and instructions as plain markdown files.

**Competitive context.** The offer sold at the end was a two-day in-person "Company Harness Intensive" on 20 and 21 Oct 2026 in Singapore, with an install pack, five starter agents, about 196 marketing skills and a voice "Jarvis" mode. List value was quoted as S$23,997, with a call-day price of S$1,997 (S$2,994 for two seats), 50 seats, and a money-back guarantee. Note for Richmade pricing: this shows the going rate for "learn to do it yourself" is under S$2,000 per person, so Richmade's done-for-you AI agency offers need to be clearly a different product.

## What changed
- `projects/richmade/journals/2026-09-30-gabriel-judah-ai-mastery-call.md`: this entry.
- `projects/richmade/README.md`: index line.
- Nothing else. No code, deploys, or settings.

## Corrections and feedback from the user
None. Jake gave no corrections in this session. The only user input was the pasted transcript and the request.

## Jake's own dictated tasks caught in the transcript
These are lines attributed to Jake Loh inside the transcript, spoken to another Claude session on the Leisure Frontier and Richpilot voice engine. Speech-to-text garbled some of them (for example "Maine" for main and "Superbase" for Supabase). I did not act on any of them. They are Jake's own words from a different session, and this session had no repo or task for them, so they are recorded here as open threads to confirm, not as instructions.
- About 1:00:00 to 1:07:00: the voice agent should be called something generic (AI voice agent or receptionist), should stand alone and not depend on the "order desk", which is a Leisure Frontier specific automation.
- 1:07:08 (Fathom action item): write a Twilio setup checklist for the voice engine.
- 1:07:18 (Fathom action item): generate an SVG logo and favicon.
- 1:11:57: Jake noted the sending domain on Resend had finished verifying, so the paused task could continue.
- 1:32:00 (Fathom action item): write the voice migration plan, then merge the voice branch into main after verifying the code and blocks are fixed.
- 1:38:24: Jake asked why he had to paste SQL into the Supabase SQL editor himself when the Supabase MCP was connected. Note: the Supabase MCP failed to connect in this session (406), so it is not available here.
- 1:51:37 to 1:53:20: Jake asked for a step-by-step to set up Twilio, then said he has no cash flow right now and would rather wait for a deposit or first payment before paying for Twilio, and asked whether there is a free way to run a voice engine.

## My take
As a source of ideas, the call is worth a page of notes and not more than that. It is a sales webinar. The headline claims (US$100k in 60 days, zero employees, "a client fully automated at 100K a month", 21 billion tokens spent) are unverified, given by the seller, and I would not repeat any of them to a client. The concepts underneath (job descriptions plus a brain plus skills plus guardrails, and a Signal step that turns stored notes into decisions) are sound and match how Richmade already works, which is probably why it felt convincing.

The one thing I'd push back on is the "AI employees never make mistakes or cause harm" tone. The speaker gives a risk answer of "use a limited debit card". That is not enough for client work. Our playbook's rules (never deploy, spend or send without Jake's yes; never trust a summary for commitments) are stricter, and they should stay stricter.

On Jake's dictated threads: the last one is the important decision. A Twilio voice engine will need money before it earns any, and Jake has said cash flow is tight. That should be settled by an explicit choice (free tier or wait for deposit), not left as a blocked task in another session.

## What I'm satisfied with
- Kept the speaker's content and Jake's dictation separate, so nothing dictated to another session is mistaken for a webinar claim or acted on here.
- Recorded the competitor price points and dates with the source attached, so a later agent can check them.

## What I'm not satisfied with
- I could not check any factual claim in the transcript, and there is no recording review, only text. Fathom said "No highlights", and the transcript has visible transcription errors (for example "US,000", "Cygnis" and "Gabriel Brack"), so figures in it may be wrong.
- The journal is thin on outcomes because the session produced no work product beyond notes. I would rather say that than pad it.

## Open threads
- Confirm with Jake whether the dictated action items above (Twilio checklist, SVG logo, voice migration plan, merge voice branch into main) were done in another session, and if not which repo they belong to (most likely Richpilot or Leisure Frontier).
- Merging the voice branch into main needs Jake's explicit yes at merge time, per the playbook's "Never do" rule, even though his dictation says to do it after verification.
- Decide the voice engine funding path: free tier, or wait for the 9 Solar or Leisure Frontier deposit before paying for Twilio.
- Optional: add a Signal-style weekly digest to the journal system (a scheduled agent that reads all recent journals and reports what changed and what keeps recurring). Not started, and not proposed as a rule because it is a build decision.
- Optional: turn Mark's time and energy audit into a one-page Richmade discovery worksheet.

## Candidate playbook rules
None. Nothing in this session generalizes beyond what the playbook already says, and I would rather not invent a rule to fill this section.
