---
date: 2026-10-04
project: 9solar-platform
topic: From a verbal yes to a deposit pack, a draft contract and a lost deal
outcome: partial
satisfaction: 3/5
model: Claude Opus 5, then Sonnet 5 and Sonnet 5.5 (Jake switched with /model)
run: attended
related: [9solar-news, richmade, richpilot]
---

# From a verbal yes to a deposit pack, a draft contract and a lost deal

## The ask
One long session from 20 Sep to 4 Oct 2026. Jake pasted the Fathom summary and transcript of the 19 Sep closing call with Kerr Sun, the 9 Solar founder, and asked for a "database" he could pull key information from. A chain of requests followed: classify a deposit agreement Rich had drafted and say what other documents were needed; fix it and add payment details; build an invoice numbering system; slim it; combine it with its invoice; highlight Clause 3.2; align three documents; drop the Growth plan because "we agreed on a $900 retainer"; polish a WhatsApp message to Kerr; draft the full Phase 1 contract and walk him through signing, since it was his first time. On 4 Oct he told me Kerr had signed with another AI company, and asked whether to resell the build to other solar companies.

Constraints he set: the deposit document is "just a DEPOSIT AGREEMENT, not the FINAL CONTRACT", the S$9,999 never changes, and from now on signature blocks are prefilled with his details.

## What I did
1. Mirrored the Leisure Frontier Automation Database conventions: verbatim transcript and summary under `meetings/`, cited derived files under `knowledge/`, a cite checker, and CLAUDE.md answering rules. Reading the transcript against the summary found Fathom's errors: the S$900/month retainer reported as "approved" when Richard had deferred it, "the Fathom project" (Fathom mishearing "phase"), speaker labels wrong at scale, and Action Items carrying the stale pre-call S$11k/S$2k plan.
2. Read Rich's deposit PDF with pypdf (no pdftotext), copied it into the repo, and told Jake it was a reservation agreement, not a contract or proposal. Argued against taking the S$1,000 "to fund the UEN" (registration costs about S$115), pointed out that two owners are a partnership and not a sole proprietorship, and advised against an NRIC as a payment handle.
3. Rebuilt the agreement as HTML rendered to PDF with headless Chrome. The first render used the old print flag and printed the file path in the page header; `--headless=new --no-pdf-header-footer` fixed it. There is no pdftoppm, so I checked layout with HTML screenshots and page count and breaks with pypdf text extraction.
4. Created a business-wide register one level above the client repos: `RM-<TYPE>-<YY>-<NNN>`, one global sequence, payment reference equal to the invoice number.
5. Iterated the pack on Jake's corrections (below): slimmed it, added the FAST and UEN statements, renamed "pre-payment" to "first payment", combined agreement and invoice into one PDF, retightened it to two pages, highlighted Clause 3.2.
6. Swept for consistency after each decision. That found a leftover "pre-payment" in the register, a missing UEN statement in the Proposal, and later two stale references in the Proposal ("sign the Deposit Agreement", "select a Service Plan").
7. Recorded Jake's S$900 as `[Jake 2026-09-20]` beside the transcript instead of rewriting M1, removed the Growth tier, and rewrote Clauses 7.1, 7.3 and 7.5 so the plan no longer claimed what it had stopped covering.
8. Built the Phase 1 Contract (`RM-AGR-26-002`, 8 pages, Schedules A to D) from wording already in the Proposal and Deposit Agreement. Grepped every "Clause N" and "Schedule X" reference and found three wrong ones. Wrote a before-sending note and a before, during and after walkthrough, and flagged the two real blockers: no registered entity, and a Proposal the register still showed as unsent.
9. On 4 Oct: wrote `knowledge/outcome.md`, put status banners on the stale files instead of rewriting them, cancelled the register rows, and updated memory. Read the Richpilot and pivot memory notes before answering the white-label question, so the advice used Richmade's actual direction.

## What changed
- `9 Solar Platform Database/`: 14 commits of mine, `af85f74` through `e7c6b81` (database `af85f74`, deposit pack `fab1b1b` to `3467f49`, retainer decision `063af75`, contract `9eac59d`, closed-lost `9d44f55` and `e7c6b81`). Four other commits in the log came from other sessions (`74b6e04`, `44429c9`, `68f7c86`, `043c6c6`).
- Cite checker: 350 cites at the first run, 399 at the last, 0 bad every time.
- Outside the repo: `RICHMADE-DOCUMENT-REGISTER.md` (new, later cancelled rows), the `Richmade Assets/signatures/` README, and the Claude memory entry for this database. Nothing was deployed, emailed or pushed (the repo has no remote). Jake sent the deposit pack to Kerr himself.

## Corrections and feedback from the user
- "This is just a DEPOSIT AGREEMENT, not the FINAL CONTRACT", and don't fill in our ACRA or UEN details. I had added jurisdiction, a notices clause, a balance schedule, a cost schedule and addresses. I cut them, kept the payment block, the extendable 15 Oct longstop and the later-phases carve-out, and added a transfer clause because there was no entity yet.
- "Remove the pre-payment invoice and reference number as it has not been done and confirmed yet." I had cited `RM-INV-26-002` for a payment nobody had confirmed, against the register rule I wrote myself (allocate at issue).
- Rename "pre-payment" to "the first payment" (Kerr's own phrase on the call).
- "Make sure all 3 documents align... and don't contradict each other or make any errors or hallucinations."
- "Remove the signature section... combine the invoice and the agreement into one document and make the invoice the second page." I did it, saw a three-page PDF in my own check, called it clean, and Jake sent a screenshot: "Page 2 and 3 needs to be separated." The agreement had spilled onto a second sheet, so the invoice was page 3 under footers that said "Page 2 of 2". I tightened the CSS to a true two pages.
- "We agreed on a $900 retainer" contradicted the transcript at M1 52:51. I flagged it once, recorded it as his instruction with its own cite, and carried on.
- His message to me cut off at "Then,". I said so instead of guessing the rest.

## My take
The paperwork was good and the audit habit paid off, but I think the session spent two weeks perfecting documents for a deal that never had a written commitment. I named the real blockers myself on 25 Sep (no registered entity, Proposal still unsent) and then kept building. I also wrote "deal closed 19 Sep" into the README and memory on the strength of a verbal yes, a Fathom summary and Jake's label "closing call". Nothing in writing from Kerr ever existed.

The bigger miss is in the transcript. Kerr said on the call that he was already working with another AI company [M1 39:57]. I logged it as Q19, "take the meeting, check for overlap", and read the firm as a possible partner because Kerr himself called it operational and separate. I never raised it as a competitive risk, and I never suggested getting the Proposal and deposit to him fast to hold the slot. I don't know that this caused the loss, and I don't know it is the same firm he signed, but I should have weighed it.

Jake's directions were strong: slim the deposit document, make payment the acceptance, use Kerr's own words for "first payment". I would not have found "no signature block" myself, and it is the right shape for a refundable S$1,000. His resale instinct for the build is sound. The part of it I would hold firm on is the 27 Sep decision to sell automations rather than websites: the reusable asset is Richpilot, and the calculator is the hook.

## What I'm satisfied with
- Reading the transcript instead of the summary, and keeping Jake's later decision as a separate cite instead of rewriting the call record.
- The reference audit on the contract. It found three real errors (a schedule citing a clause that does not exist, a wrong authority clause, two clauses defining the same trigger) before anyone read it.
- Telling Jake his draft message said "percentage deposit" and "continue works" when the document says a flat S$1,000 that only reserves capacity.
- The closed-lost record: banners and a new outcome file, so the history survives and a later session can't mistake a dead deal for a live one.

## What I'm not satisfied with
- I called a three-page render clean against an explicit "invoice is page 2" instruction. I had the page count in front of me.
- I built the deposit agreement too heavy first. It took about four passes to reach what Jake described in one line.
- Text searches for "Growth" and "Essential" passed while "select a Service Plan" was still in the Proposal. Only looking at the rendered page caught it.
- Mid-edit I wrote a citation to "Clause 7.3" for the acceptance mechanism before it was a numbered clause. I caught it before sending, but only by re-reading.
- I couldn't save the signature: an inline paste has no file path my tools can read. I set up the folder and asked Jake to drop the file. He saved it under a different name than I specified, which I found a session later.

## Open threads
- Where does the finished site and calculator live? It is not under `AI Agency`. Asked, unanswered.
- Did the Proposal ever go to Kerr? Not recorded.
- Why did Kerr leave, and does it touch the news site (same company, `RM-AGR-26-003` and `RM-INV-26-002` are addressed to it)?
- The business entity is still unregistered. The news site needs it.
- Decide whether to turn the build into a solar lead-gen template on Richpilot, after stripping 9 Solar's brand assets and anything Kerr said in confidence.
- Jake's standing instruction to prefill his signature details lives only in the `Richmade Assets/signatures/` README, not in the playbook. The PNG has a white background, not a transparent one.

## Candidate playbook rules

- **After a decision changes how a deal works (not just a number), sweep the register and every sibling document for what the old mechanism said, not only the changed word. Cite only documents and numbers that have been issued ("to be issued" otherwise), and proof-read the rendered PDF before calling the set consistent.** A search for "Growth" passed while "select a Service Plan" survived, and I cited an invoice number nobody had confirmed. (adopted)
- **Keep each deal document to its own job: a deposit or reservation document states how much, how it is paid, when it is refunded and what it does not commit anyone to; IP, liability, termination, jurisdiction and entity details belong in the contract.** Jake's correction: "this is just a DEPOSIT AGREEMENT, not the FINAL CONTRACT". (adopted)
- **Make client PDFs from HTML with headless Chrome (`--headless=new --no-pdf-header-footer --print-to-pdf`) and verify page count and breaks with pypdf plus an HTML screenshot; a document that must be N pages is not done until the PDF has N pages.** I called a 3-page render clean when the brief was 2. (adopted)
