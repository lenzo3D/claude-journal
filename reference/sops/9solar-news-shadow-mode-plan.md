# 9 Solar News: your plan for shadow mode and launch

Internal. Not for the client. Written 15 Oct 2026.

**Where things stand:** the site is live at `https://9solarnews.richmade-app.workers.dev`. The newsroom is running in **shadow mode**. It writes real stories, but they go only to the locked preview site (`https://9solarnews-preview.richmade-app.workers.dev`), never to the public site. Kill switch: off. Golden test: passed (0 bad drafts missed, 0 good drafts held).

**Key dates**

| Date | What happens |
|---|---|
| Wed 15 Oct, 07:00 SGT | First shadow cycle. Cycles then run daily at 07:00, 11:30, 17:00 and 21:00 SGT |
| 15 Oct to 28 Oct | 14 days of shadow mode: you score stories every day |
| Wed 29 Oct, earliest | Move to `live-low` (public site), only if `/ops/shadow` shows every criterion met |
| 12 Nov, earliest | Move to `live-medium`, after 14 days of `live-low` with zero critical errors and zero takedowns |

---

## 1. Current tasks (do these first)

| # | Task | When |
|---|---|---|
| 1.1 | After 07:00 SGT on 15 Oct, open Telegram and `https://newsroom.richmade-app.workers.dev/ops`. Tell Claude what you see: stories published to the preview, stories held, and any alerts. The first cycle is the first live test of saving to Sanity and rebuilding the preview. | 15 Oct morning |
| 1.2 | Open the preview site (sign in with your email code) and check the first stories appear. | 15 Oct |
| 1.3 | Move all of today's secrets into one password manager (1Password recommended), one vault per client. The secrets are: the Anthropic key, 3 Sanity tokens (`newsroom-write`, `preview-build-read`, and any older ones), the Telegram bot token and webhook secret, the Unsplash key, 2 deploy hooks and the Turnstile secret. | This week |
| 1.4 | Delete the old **cygnisloh** Cloudflare Worker `9solarnews` and its old Turnstile widget, once you're happy with the new site. | This week |

---

## 2. Daily routine for the 14 days (about 20 minutes a day)

1. **Telegram:** read any alerts from @saatnewsbot. Held stories, budget warnings and reader error reports arrive there.
2. **Score every new story.** Open `/ops`, click each story, and on its `/ops/story/<id>` page record:
   - **Critical:** a factual error, a made-up claim, a legal or POFMA risk, or anything that must never be published.
   - **Minor:** awkward wording, a weak headline, small style issues.
   - **None:** fine as it is.
   Scoring calibrates the system. It isn't an approval step.
3. **Check cost** on the `/ops` dashboard. The daily and monthly totals should stay small, about US$1 a day.
4. **Glance at `/ops/shadow`** to see the progress bars.

**What `/ops/shadow` needs before you can go live:**

| Criterion | Target | Note |
|---|---|---|
| Stories scored | at least **100** | The bottleneck. At up to 12 stories a day, missing a day hurts. |
| Critical errors | **0** in the last 7 days | One critical error resets that clock. |
| Stories with a minor issue | **under 2%** | Strict: 2 minor issues in 100 stories fails it. If this looks unreachable, raise it with Claude rather than under-scoring. |
| Average cost per story | at or below the US$0.60 cap | |
| Skipped checks | **0** | Any skipped check means something broke. Tell Claude. |

**Emergency commands (Telegram, private chat with @saatnewsbot)**

| Command | What it does |
|---|---|
| `/kill` | Stops everything at the next step, including all AI calls |
| `/resume` | Restarts it |
| `/takedown <story id or URL> [notice]` | Removes a story |
| `/banner <story id or URL> <exact notice text>` | Adds a notice on a story |
| `/correct <story id or URL> <correction text>` | Publishes a correction |
| `/status` | Shows what the newsroom did in the last 24 hours |

---

## 3. Decisions to make during the 14 days (all needed before `live-low`)

| # | Decision | With whom | Why it blocks going live |
|---|---|---|---|
| 3.1 | **Publisher of record**, and who carries liability for AI-written stories | Mr Saat | A legal owner must exist before anything is public |
| 3.2 | **Design and brand name.** The site still shows the design switcher (3 designs, 2 names). Mr Saat picks one, and Claude removes the switcher. | Mr Saat | The public site can't launch with a comparison switcher |
| 3.3 | **A real contact email** for the site | Mr Saat | The site has no contact address. Nothing is invented. |
| 3.4 | **IMDA check:** the licence applies at 50,000 unique Singapore visitors a month, with a S$50,000 bond | You | Needed before traffic grows |
| 3.5 | **Malay reviewer** to check Malay stories and UI text once, including the new badge wording | A fluent speaker | The Malay check is currently a back-translation |
| 3.6 | **Analytics:** Google Analytics 4 or Cloudflare Web Analytics | You | The audience alert can't work without it |
| 3.7 | **Real domain** (instead of `richmade-app.workers.dev`) | Mr Saat | When it's ready, Claude updates SITE_URL, Turnstile and Access |

**Source coverage (unlocks more sections)**
- **World section:** in `/ops/sources`, add the terms note for NASA. The wording is in the source-terms decisions note.
- **Sustainability section:** needs a second cleared publisher alongside Eco-Business (UNEP needs a manual terms read).

---

## 4. Going live (from 29 Oct at the earliest)

1. `/ops/shadow` shows every criterion met, and decisions 3.1 to 3.3 are done.
2. Tell Claude "go live-low". Claude walks you through setting **Stage** to `live-low` in the `/ops` settings form.
3. Stories now publish to the public site (low-risk stories only).
4. Run 14 days with zero critical errors and zero takedowns, then set Stage to `live-medium`.
5. After any critical error, drop back to `live-low`.

High-risk stories are never published automatically: courts, crime, Singapore politics, race, religion, health claims, minors, named private individuals, and 9 Solar or its competitors. You can release one from `/ops`, and every check re-runs first.

---

## 5. Future tasks (after launch, no deadline)

| Task | Why |
|---|---|
| Build a Cloudflare API-token provisioning script with a 1Password secrets loader | Cuts the next client's setup from about 8 hours to under 1 |
| Commercial roadmap and pricing conversation with Mr Saat (phases, retainer tiers, revenue share) | See the roadmap and pricing notes |
| Source real Singapore freelancer rates (video, journalism, podcast) before quoting any phase | Production lines must be priced at 2.5x cost or more |

---

## 6. Later: two messages, ready to send (added 16 Oct 2026)

Not urgent. Nothing is public until `live-low` (29 Oct at the earliest), so send both before launch day, not now.

| # | Task | When |
|---|---|---|
| 6.1 | Send Mr Saat the risk message below and get his yes **in writing** (a WhatsApp reply counts). Then set `attributedNews` to `public` at `/ops/settings`. | Before launch day |
| 6.2 | Email UN News the notice below. Then record UN News's terms note at `/ops/sources` (role `evidence-full`). | Any time before launch; it adds 2 to 4 stories a day as soon as it's done |

**6.1 To Mr Saat (WhatsApp or email)**

> Hi Mr Saat, one decision before launch. To publish a full paper every day, the newsroom reports facts from outlets like CNA, The Straits Times and Bernama, written in its own words with credit and a link (for example "according to CNA"). It never copies their text. Their website terms say no reuse without permission, so there is a small risk of a letter to the publisher. Are you OK for us to go ahead on that basis? If you'd rather check with a media lawyer first, we can do that too.

**6.2 To UN News (email to the address on news.un.org's contact page)**

> Subject: Notice of use of UN News material
>
> Hello UN News team, as your copyright page asks, this is to let you know that [site name] ([site URL]), a Singapore news site, will report on UN News articles with credit to UN News and a link to each original story. Thank you for making your reporting available. [Your name], [Richmade, on behalf of the publisher]

Fill in the site name and URL once the name and domain are decided (3.2 and 3.7).

---

## 7. Questions for Mr Saat (one meeting, about 30 minutes)

**Must answer before launch**
1. **Publisher of record:** whose name, company and UEN go on the site as publisher? Who carries legal responsibility for what it publishes?
2. **Risk on outlet-based stories:** is he OK publishing stories built from CNA, Straits Times and Bernama reporting, in our words with credit? (See 6.1.)
3. **Name and design:** which of the 3 designs and which name? (Then the switcher comes off.)
4. **Domain:** which domain, and who buys and owns it?
5. **Contact email** for readers, corrections and legal notices, and who reads it.
6. **Launch date** he has in mind, and whether a quiet soft launch first is fine.
7. **POFMA and complaints:** if a government direction or a complaint arrives, who is the first person to call, and how fast does he expect a takedown?

**Shapes the product**
8. **Volume:** how many stories a day does he expect? (Today's realistic range is 20 to 30, rising with more sources.)
9. **Sections:** which sections matter most to him: Singapore, region, business, sustainability, lifestyle?
10. **Topics to avoid,** beyond the built-in ones (courts, crime, politics, race, religion, health claims, minors, 9 Solar and its competitors).
11. **9 Solar mentions:** confirm the site never promotes 9 Solar, even indirectly.
12. **Malay:** can he suggest a fluent reviewer to check the Malay versions once?
13. **Wire or syndication licence:** does he have contacts at Asia News Network, Bernama, AFP or Reuters from his SPH days? Would he budget for a licence to fill the World and Business pages?

**Business and operations**
14. **Running costs:** AI costs are about US$60 to US$100 a month on top of the retainer. Who pays if volume grows past that?
15. **Analytics:** Google Analytics or Cloudflare Web Analytics, and does he want a monthly report?
16. **IMDA:** he knows the online news licence applies at 50,000 Singapore visitors a month (S$50,000 bond)? Who handles it if traffic gets there?
17. **Social media:** does he want stories posted automatically to social channels, and which ones?
18. **Reporting:** a weekly or monthly summary from us (stories published, corrections, traffic)?
