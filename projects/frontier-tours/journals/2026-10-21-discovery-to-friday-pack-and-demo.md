---
date: 2026-10-21
project: frontier-tours
topic: Discovery call to Friday pack, Claude Design demo, audit and site studies
outcome: shipped
satisfaction: 3/5
model: Claude Opus 5.5
run: attended
related: [leisure-frontier, richpilot]
---

# Discovery call to Friday pack, Claude Design demo, audit and site studies

## The ask
Jake brought in a new prospect: Frontier Tours Sdn Bhd, the Malaysian company of the Luxury Coach team (Rachel; referred by Terence). They want a bilingual (EN and 中文) tour-package site with online deposit booking and a staff admin. The follow-up call is Fri 23 Oct 2026, 1pm. Over one long day Jake asked me to:
- process the discovery call;
- research Malaysian payment gateways;
- tear down the two reference sites Rachel named;
- brainstorm the site and a Hormozi-style sales process;
- write specs and a Friday pack plan, including a VSL script he could record the same day;
- build the pack.

Later in the day he asked me to:
- rebuild the demo his usual way, in Claude Design;
- move it to the Leisure Frontier family look;
- push to a new GitHub repo;
- audit the demo and study luxurycoach.com.sg, euholidays.com.sg and webuytravel.sg in depth, adopting their good patterns and avoiding their bad ones;
- hand the rest of the build to a Sonnet 5.5 session to save cost.

Constraints he set:
- No pricing or proposals in writing; everything is closed on the call.
- Never push without his yes.

## What I did
1. **Call and research.**
   - Processed the call notes into memory and `meetings/2026-10-21-01-discovery/notes.md`.
   - Researched gateways (`research/payment-gateways.md`: HitPay primary, Fiuu fallback, Stripe not primary).
   - Tore down Webuy and EU Holidays (`research/reference-sites.md`).
   - Most of this is known to me only through the compaction summary, so commit hashes are reliable and the finer detail is thinner.
2. **Brainstorm and specs.** Ran superpowers brainstorming into two specs (the sales system, and the Tour Desk plus booking site). Jake approved both.
   - He raised a worry that staff would end up using two systems. I turned it into a question for Rachel ("who runs MY bookings, and do you want one system?"); her answer decides what we build. I put it in both specs, the call script and `CLIENT-QUESTIONS.md`.
3. **Friday pack.** Wrote the plan and built five tasks natively: the VSL script and visuals, offer deck with a live-only price slide, call sheet, check script and tests, and a first HTML demo. Ran one combined review and one fix pass.
4. **Demo rejected.** Jake said the demo "looks bad" and asked for his usual approach. I rebuilt it in Claude Design:
   - a design system scraped from the reference sites, then a canvas of 7 artboards;
   - a local export that runs `support.js` (the Design runtime) so it works offline at 127.0.0.1:8091.
5. **Brand corrected.** I had inferred a Luxury Coach plum look. Jake said Frontier Tours is separate from Leisure Frontier but shares its colours and design elements, and sent a photo of the coach livery. I rebased the DS on LF tokens plus a `LiveryStripe` element taken from the coach swoosh.
6. **Pushed** to the new private repo lenzo3D/frontiertours, after checking it was private (anonymous API 404) and empty, and that every commit used the noreply author.
7. **Audit.**
   - Captured every screen at 1440px and at 390px with real CDP device emulation (the new `cdp_shot.py`), and read each page's `innerText`.
   - The worst problems were in copy I had written myself: the "full price" slogan four times; company claims nobody had confirmed ("direct flights from KLIA", "Mandarin-speaking guides", WhatsApp "evenings and weekends"); a search bar that did nothing; two of three tour cards dead-ending at a sign-up form.
   - Wrote `research/demo-audit.md`.
8. **Rebuild.**
   - `tours-data.js`: one data file holding four sample tours in EN and ZH. Departure status, seats left and balance due date are derived from seats, paid and held counts, never typed.
   - `site-chrome.js`: a shared header, footer and Photo component.
   - Main, Tour and Booking now take a `lang` prop, and the ZH pages are `dc-import` wrappers, which removed a brittle string-replacement generator.
9. **Site studies.**
   - Ran three background research subagents, one per site, while I rebuilt. Cloudflare blocked curl and headless Chrome on luxurycoach, so that agent used the browser pane.
   - Adopted the Luxury Coach items myself: dates on cards, date tiles, a bilingual reading mode, two-language WhatsApp prefill.
10. **Handoff.**
    - At Jake's request, wrote `docs/handoff/2026-10-21-demo-rebuild.md` and started a Sonnet 5.5 session in the same folder.
    - Forwarded the EU study to it with guidance, including one finding against us: per-departure codes shown to customers.
    - It shipped `a5f8a66` and `3382a0f` and synced the canvas. I spot-checked four pages at 390px (no sideways scroll, no em dashes), then pushed on Jake's yes.

## What changed
- Repo `~/Documents/AI Agency/frontier-tours`, branch `feature/friday-pack`, pushed at `3382a0f`; `main` at `2376f00` (specs and plan).
- Key commits:
  - `a5f1ddc`, `a7b8c26`: specs and the two-systems question;
  - `2376f00`: the plan;
  - `11e29b2` to `ac41d5d`: the Friday pack;
  - `744b639`: the Claude Design prototype;
  - `8f2d8fd`: the LF family look;
  - `b336a9e`: the audit and shared-data rebuild;
  - `1c71085`: the Webuy study and handoff;
  - `a5f8a66`, `3382a0f`: Sonnet's adoptions.
- Research files: `demo-audit.md` and `site-study-{luxurycoach,webuy,euholidays}.md`.
- Outside the repo:
  - Claude Design DS artifact RrS6VcaAa9b8wDrJZZEvbn and canvas 98URQ5Tmf2LYMb3oSX6rkk, both private and synced;
  - the new GitHub repo;
  - the memory note `frontier-tours-malaysia-discovery.md`.
- Tests: `friday-pack/test_check.py` 12 passing at the time of the pack. The demo has no automated tests; it was verified by screenshots and browser checks.

## Corrections and feedback from the user
- "Demo site looks bad, lets not take this approach but instead use my existing approach". The plain HTML/CSS demo was rejected for Claude Design with a scraped design system. Jake's standard for a client demo is a designed artefact, not a functional mock.
- On the brand: Frontier Tours "is seperate from leisure frontier but it should share similar design elements and colourways". I had guessed Luxury Coach's plum from the transcript. A group company's brand family is Jake's call, not an inference.
- "No pricing or proposals should be sent, all things that need to be closed should be done on call."
- He asked for the remaining build on Sonnet 5.5, a cost decision once the design work was settled.

## My take
- The day went well once the method matched Jake's. It went badly whenever I chose the method or the brand myself: the first HTML demo and the plum palette both cost a rebuild.
- The audit was the most useful hour. Most of what it found was mine: slogan repetition and claims about the client's operations that nobody had said. That is the "never fabricate" rule breaking quietly inside sample copy, because "it's a demo" made invented claims feel harmless. Rachel would have spotted "direct flights from KLIA" as made up within a minute.
- Moving the demo onto one data file was the right structural call. Luxury Coach's own site shows the failure it prevents: its Hainan price reads S$958 in English and S$888 in Chinese.
- Handing the build to Sonnet with a written brief worked. Its two commits matched the brief, it rang the right placeholder bells, and it found a tool quirk (the Artifact tool refusing a path with a folder called `prototype`).
- Risk ahead: `deck/decisions.json` still has all 8 pricing values unset, and the whole Friday pitch depends on Jake filling them and rehearsing the new demo, which is much bigger than the one in the VSL.

## What I'm satisfied with
- Derived seat status and balance dates. Booking, tour pages and Tour Desk now cannot disagree.
- Research fan-out. Three background agents wrote one file each while I rebuilt, so no wall-clock was wasted, and each study ended with a ranked adopt and avoid list I could act on.
- True phone-width checks through CDP device emulation, instead of `--window-size`, which can't go below about 500px.

## What I'm not satisfied with
- I wrote unconfirmed operational claims into two builds before auditing them.
- `research/demo-audit.md` marked rows "Fixed" before the fixes existed. I flagged it in the handoff for re-checking, but the doc briefly said something untrue.
- Two brand or method rebuilds in one day. I should have asked about the brand family before building the DS.

## Open threads
Jake, before Friday:
- text Rachel to confirm Fri 1pm;
- record and send the VSL;
- fill `deck/decisions.json` and run `check.py`;
- have someone fluent check the new Chinese copy;
- rehearse the demo;
- decide whether to merge `feature/friday-pack` into `main`.

On the call:
- ask the two-systems question first;
- collect the logo, MOTAC number, contact details, the WhatsApp Business number, real photos, staff photos and review links to replace the labelled placeholders.

Journal housekeeping: `check-sources.py` reports `reference/sops/richpilot-crm-client-switch-on.md` as stale against Richpilot HEAD `0d6638d`. The copy still matches Richpilot `main` (latest change `b85f1d2`), so the drift is on an unmerged branch. Refresh it when that branch lands.

## Candidate playbook rules
- **Build every demo screen from one shared data file, and derive statuses, counts and dates from it rather than typing them per screen.** Hand-typed values drift: luxurycoach.com.sg shows different Hainan prices in English and Chinese. Our first demo had dead-end cards and per-page numbers until it moved onto `tours-data.js`. (adopted)
- **Before a client sees a demo or page, read its visible text end to end (an innerText dump per screen) for repeated slogans and claims about the client's business that nobody confirmed, and replace or label them as sample.** Sample copy is where invention slips past the never-fabricate rule: this demo claimed direct flights, Mandarin guides and weekend replies that Rachel never mentioned. (adopted)
- **When the client belongs to a group of companies, ask Jake which sibling brand's look it follows before building the design system.** I inferred Luxury Coach from the transcript; Jake wanted Leisure Frontier's family look, and the design system and seven screens had to be redone. (adopted)
