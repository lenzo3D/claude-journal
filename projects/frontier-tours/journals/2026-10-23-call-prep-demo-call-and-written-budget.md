---
date: 2026-10-23
project: frontier-tours
topic: Call prep, the demo call, and the written rough budget
outcome: partial
satisfaction: 3/5
model: Claude Opus 5.5
run: attended
related: [leisure-frontier]
---

# Call prep, the demo call, and the written rough budget

The context was compacted part-way through this session (it continued from the 21 Oct session). The order of the prep edits below comes from the commit log and the compaction summary, not from memory, so some reasons for individual edits are lost.

## The ask
In the three hours before the 1pm demo call with Rachel (Frontier Tours Sdn Bhd), Jake wanted the call pack ready: the offer, a Hormozi-style call script with a subtraction close and a downsell ladder, the deck and a price slide. He decided against recording the VSL. After the call he gave me the transcript and asked for next steps and whether to start a new session. Standing constraints: Richmade is strictly an AI agency (no videos, filming or content); no pricing in writing; no em dashes; never push without his yes.

## What I did
1. Laid out the offer and demo plan so Jake could see what was wrong with it, then took his edits one at a time. He dropped a new backend, then brought it back as a question for the call ("ask her: build new or integrate the old one"). Then:
   - pricing: first S$5k setup, then market-based (S$11,800 setup + S$1,200 a month, with a sourced market table in `call-script.md`);
   - removed: video and content, the Catalogue Launch Kit, the S$7,800 Launch tier, Ads-to-Bookings Tracking, the guarantee slide;
   - added: SEO, AEO and GEO as "Found First";
   - currency: SGD for our prices, RM for her booking values.
2. Pushed back on one ask. He wanted a promise that she'd rank number one on Google and AI. I framed it as a goal, not a guarantee, everywhere, because nobody controls rankings.
3. Rebuilt the price slide so the calculator shows first and the prices are revealed by scrolling or the arrow keys. I fixed two bugs found in the browser: Down in a number box changed the number instead of moving on, and `display:flex` overrode the `hidden` attribute.
4. Pointed the call pack at the Cloudflare demo, since the Vercel link was still showing the old build.
5. Recommended against a booking commission: thin tour margins; we don't control her traffic; in path B we can't see the bookings; and 3% of RM3,000 is about S$28 a booking.
6. Processed the transcript after the call:
   - saved it with notes in `meetings/2026-10-23-02-demo-call/`;
   - filled in F1 to F12 in `CLIENT-QUESTIONS.md` with timestamps;
   - updated memory;
   - proposed a fresh session for the written budget. Jake started it, and it produced `proposal/frontier-tours-rough-budget.pdf` (later moved to a 50/50 payment plan).

## What changed
- Prep commits in `frontier-tours`, `71f6109` to `8002dcd` (14 commits): `friday-pack/` deck, price slide, `call-script.md`, `call-sheet.md`, `decisions.json`, plus `docs/offer-explained.md`. `check.py` prints nothing; unittest OK.
- `beda6bc`: call transcript, notes and F1 to F12 answers.
- `d10e101`, `2090162` (proposal session): rough budget HTML and PDF. Uncommitted edits to both were still in the tree at wrap-up, from that session.
- Nothing since `09d0fe4` is pushed. Pushing `main` may redeploy the Cloudflare demo from `website/`.

## Corrections and feedback from the user
- "We are strictly an AI agency, and we do not do videos or things like that or shoot content." I had video and catalogue content in the offer.
- "Scrap this new script you gave me and instead use the old call script.md": he didn't want a diagnose-first rewrite.
- Price on market values, not on my first number.
- "remove all the weird little things, like the bracket that says 'guaranteed not set'... Just remove the whole slide if it's not necessary." I had left unset placeholders visible in a client-facing deck.

## What the call taught us
These points, from the raw transcript, matter more than anything above:
- Rachel wants a **brand-new, separate backend** [17:48].
- **The Chinese New Year deadline didn't work as urgency:** "it doesn't affect whatever we are doing in the Singapore end" [09:58].
- **The "price jumps at checkout" leak didn't apply:** "for us, we don't do that" [31:13].
- Her customer service team already chases unpaid bookings, so the rescue bonus is weaker than we thought.
- **She never saw the price slide.** Nobody asked F7 (bookings a month and average value), so the calculator had nothing to work with.
- **She asked for a written rough budget** covering build, maintenance, after-service and commission. The team pushed back once, then agreed, so the no-written-pricing rule broke on the first ask.
- The team committed out loud to "3 to 4 weeks" to go live and to help with the first photo uploads. The offer had excluded loading.

I checked the AI summary at the top of the transcript against the raw text before writing the notes, as the playbook's Fathom rule says.

## My take
Most of the prep was polish that never reached the client. The deck, the price reveal and the downsell ladder went unused, because the call turned into a requirements walkthrough and a request for something in writing. Half of my pitch levers were assumptions. I built urgency on Chinese New Year and a pain point on price jumps without either having been confirmed, and each one was rejected in a single sentence. The work with the best return was the backend question and the guest-checkout point, both of which came from things she had actually said.

The pre-call pricing chat (open at 12 to 12.5 and let her bargain down to 11.8) contradicts the script's "never cut the price". The team's real behaviour is to negotiate, and the script should match that rather than pretend otherwise.

## What I'm not satisfied with
- Earlier in the session I committed an empty `call-sheet.md` (`9a0317a`) with `open(p,'w').write(open(p).read()...)`: opening the file for writing truncated it before it was read. I restored it from git, but I should have run `git diff --stat` before committing.
- I let unset placeholders show in the client deck until Jake noticed them.

## Open threads
- Jake: review and approve the rough budget, then send it, ideally before Rachel flies next week. Send the demo link in the group chat (Richard) and chase the logo.
- Demo updates for 6 Nov: an optional member prompt after payment, room-type rules (twin booked as pax x2), a payments view, and image size limits in the admin. These are waiting for Jake's yes to send to the ft-demo-rebuild session.
- Before 6 Nov: send a reminder and confirm the time; ask whether Terence joins; drop the CNY urgency and leak #1 from the deck; ask F7 and F8.
- Push decision for every commit since `09d0fe4`.
- Unrelated: `reference/sops/richpilot-crm-client-switch-on.md` is STALE in check-sources.

## Candidate playbook rules
- **Before a sales call, mark each pitch lever (urgency, pain point) as confirmed by the client, with a quote, or as assumed, and prepare a fallback for each assumed one.** On Frontier Tours, the assumed Chinese New Year deadline and the "price jumps at checkout" leak were each rejected in one sentence, and the script had nothing behind them. (adopted)
- **Before any call where a price is planned, prepare a one-page written budget as a fallback: one bundled price, no line items, "to be confirmed on our call".** Prospects whose decision-maker isn't on the call ask for pricing in writing. Rachel did on the first call where we planned to show a price, and the team agreed on the spot with nothing ready. (adopted)
- **Ask the questions the price depends on (volume and average value) in the first ten minutes, before the demo, and don't move to price without them.** F7 was skipped, so the value calculator couldn't run and the price was never shown. (adopted)
