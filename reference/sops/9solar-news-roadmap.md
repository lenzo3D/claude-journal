# 9 Solar News: phased roadmap and commercial structure

Internal Richmade document. Written 7 Oct 2026. Not for the client. Supersedes nothing; it sits alongside `9solar-news-client-strategy.md` (research and contract clauses) and `9solar-news-growth-notes.md` (build-level notes and open risks).

Contract position as at 7 Oct 2026: S$5,000 one-time setup (S$1,000 deposit paid, S$1,500 on signing the Services Agreement, S$2,500 on launch) plus S$1,200 a month. Phase 1 scope is the 63 deliverables in `Richmade-9Solar-News-Site-Proposal.pdf`. The client has said Richmade may quote and bill for additions as the site grows.

## 1. What the client is actually buying

Mr Saat wants all three of these, in descending order of urgency:

1. **A news property that earns revenue.** The site is a business in its own right.
2. **A credible Singapore title.** He is ex-SPH Straits Times. Reputation and influence matter to him.
3. **Eventually, more customers for 9 Solar,** explicitly without obviously promoting solar, green energy or 9 Solar itself.

**The principle that follows:** credibility is the asset that pays for all three. Sponsors pay for trust, the legacy needs trust, and the 9 Solar halo only has value if no reader can see the wire. So the roadmap is optimised for revenue, but the route runs through audience and authority, never through visible funnels or early ad clutter.

**What this rules out:** prominent solar lead generation, a visible 9 Solar integration beyond the existing sanctioned Solar Quest funnel, and any on-site commerce that gives the newsroom a commercial interest in what it covers.

## 2. Operating model

Richmade supplies everything: the platform, the autonomous newsroom, and all production, using freelancers that Richmade sources and manages directly. The client gives editorial direction and ideas. He does not manage anyone and does not write.

That makes this a **managed media operation**, not website maintenance. It is the single most important fact for pricing, because the retainer was originally scoped as maintenance. See section 5.

## 3. Immediate correction before the newsroom goes live

The autonomous newsroom as built will skew green, which works against goals 1 and 2 and devalues goal 3.

Of the three sources cleared for citation on 7 Oct 2026, two are environment-focused (NASA, Eco-Business) and the third is MOM retrenchment data. The settings also carry a `sustainability` section and a `solar-news` section in the quota map.

Fix in Phase 2: widen the cleared general-news sources, drop `solar-news` as a section, and check the published mix against the quotas (Singapore 30%, regional and world 40%, business 30%) during shadow mode. Small work, but it is the difference between a news title and a content-marketing site.

## 4. The phases

Timings are relative to launch day (L), because the launch date is still open. The proposal targeted "next week" from 20 September and has not launched, so every date below has already slipped with it. **Launching is the highest-value single action available: it releases S$2,500 and starts every other phase.**

### Phase 1, now. Build and launch
Contracted and in progress. Roughly 90% built. No further billing.

### Phase 2, L to L+6 weeks. Newsroom live, rebalanced to general news
The rollout is already specified: 14 days shadow mode on staging, then 14 days live-low with zero critical errors and zero takedowns, then live-medium. Includes the correction in section 3.

Gated on: the client's Cloudflare Workers Paid plan, the resource ids and secrets, source terms records, and publisher of record.

**Billing: absorbed.** It is what makes S$1,200 viable while the client writes nothing. The rebalance fits inside the change allowance. This changes at Tier 1 (section 5).

### Phase 3, from L+2 weeks, continuous. Audience engine: shorts and podcasts
Answers the client's own brief: young non-readers, hooks, viral, Mothership-like. The Shorts feed is already built, so what is missing is production, not platform. Podcasts do double duty, because transcripts feed the answer-engine and generative-engine work already in Phase 1.

**Billing: two lines, kept separate.**
- Platform build (podcast hosting, RSS, transcripts, episode pages, any Shorts upload tooling): one-off quote. Jake's earlier scoping figure for work of this class was S$8,000 to S$20,000 each.
- Production (filming, editing, publishing cadence): its own monthly content retainer, never inside the S$1,200.

If production is ever absorbed into the retainer, this phase destroys the margin on the account. It is the main commercial risk in the whole roadmap.

### Phase 4, from L+2 to 3 months. Editorial authority
The credibility engine, and what lets Richmade charge properly for sponsorship in Phase 5.

Order within the phase matters: named interviews with business leaders, academics and community figures first. **Politicians last,** and only after publisher of record, the liability terms and the bond figure are settled, and never during an election period. Singapore politics is a risk tier the newsroom never auto-publishes, so this is human journalism by definition.

**Billing: per piece, or a journalism retainer.** Delivered by a freelance journalist Richmade manages.

### Phase 5, from L+4 to 6 months, gated on audience. Revenue
Direct-sold sponsorship and clearly labelled advertorial first. Programmatic networks pay almost nothing below roughly 100,000 pageviews a month, so they come later if at all.

One real build item: wire an advertiser blocklist into the newsroom's existing conflict-names check, so the autonomous newsroom can never write about a sponsor. That is both a safeguard and a selling point when pitching sponsors.

**This is where IMDA licensing becomes likely.** See section 6.

### Phase 6, L+6 months, optional. Commerce
Affiliate and referral links out to existing booking platforms, measured for real demand. No payment handling, no merchant of record, no refunds.

Own the transaction only if one vertical clearly proves out, and then as its own product with its own contract. **Recommendation: do not build on-site restaurant bookings.** It gives the newsroom a commercial interest in what it covers, it makes Richmade merchant of record with the payments, refunds, data-protection and consumer-protection duties that follow, and it adds human operations load that scales with transaction volume while Richmade absorbs costs.

Solar lead generation stays deliberately quiet per the client's constraint: a soft integration, not a funnel.

## 5. Retainer step-up

The newsroom is absorbed now and gets billed as its own line as viewership and capacity grow. Triggers are objective so each step is a scheduled review, not a negotiation.

| Tier | Trigger | Scope | Indicative monthly |
|---|---|---|---|
| 0, now | Launch to steady state | Hosting, maintenance, monitoring, backups, SEO upkeep, newsroom operation, 4 to 6 hours of change requests | S$1,200 |
| 1 | Newsroom at live-medium and sustained daily publishing, or published volume rises above the launch cadence | Tier 0 plus the newsroom billed as the editorial operation it is | To be set at the review, above Tier 0 |
| 2 | Approaching 50,000 Singapore uniques a month, or two or more content formats in production, or ads live | Full managed media operation. Earlier research put this class of work at S$3,000 to S$7,000 a month | To be set at the review |

Note on what drives cost: infrastructure does not. The newsroom runs at about US$25 a month and stays near that even at double the volume. **The cost driver is freelance human capacity.** Price every tier and every phase off actual freelancer quotes.

**To source before any phase or tier is quoted:** real rates from Singapore freelancers for videography and editing, per-article journalism, and podcast editing. Do not quote from estimates.

## 6. Risk and gate register

| Item | Status 7 Oct 2026 | Blocks |
|---|---|---|
| Publisher of record and liability terms with Mr Saat | Open | Everything editorially risky, and Phase 4 entirely |
| IMDA Online News Licensing: one Singapore news article a week plus 50,000 unique Singapore visitors a month triggers an individual licence and a S$50,000 performance bond | Bond figure open | Phase 5. Decide and budget before crossing the threshold, not after |
| Analytics source (GA4 or Cloudflare Web Analytics) | Not connected | The audience alert cannot be built; until then an operator checks monthly |
| POFMA exposure on any fabricated fact | Mitigated in the build, never zero | Peaks in Phase 4 with politics |
| Advertiser and newsroom conflict of interest | Not built | Phase 5. Needs the blocklist |
| Green content skew | Identified, not fixed | Phase 2. Damages goals 1 and 2 |
| Chinese and Arabic UI strings drafted by Claude | Need a native check | Those languages staying switched off |
| Election period | Setting exists in the build | Any political coverage during one |

## 7. Contract changes to make before signing

The proposal prices the retainer as "Hosting, maintenance, ongoing SEO and a scope of new features and improvements you request." That last clause is an unbounded obligation and contradicts the client's own verbal position that Richmade may quote as it goes.

Replace it with:
- A fixed inclusion list: hosting, maintenance, monitoring, backups, uptime, security updates, SEO upkeep, newsroom operation.
- A stated change allowance of **4 to 6 hours a month**, with unused hours not carried forward.
- An explicit line that new features, new formats, new languages, production services and anything in Phases 3 to 6 are quoted separately.
- A scheduled retainer review tied to the Tier triggers in section 5.

Without this, every phase in this document arrives as something the client believes he has already paid for.

## 8. Open decisions

- Launch date. Everything keys off it and it has already slipped.
- Whether Mr Saat or a freelancer fronts the Phase 4 interviews. He is the credible byline; he writes nothing today.
- Freelancer rates, to be sourced before quoting.
- Whether to present this roadmap to the client at all, or use it to shape the formal proposal and quote phase by phase as he asks. Nothing in this document should be sent to him as written.
