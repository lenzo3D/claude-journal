# Source terms worksheet (step A6)

Purpose: the newsroom may only quote a source as evidence once someone has recorded that its terms allow it. Until then a source is a signal only: it can point at a story but cannot be cited. In shadow mode, with nothing checked, almost every story is killed for lack of evidence.

You do not need to check all 15 at once. Start with the ones marked START HERE. Even 4 or 5 checked sources is enough to begin shadow mode.

## How to check one source (about 15 minutes)
1. Open the site's footer and find "Terms of use", "Terms and conditions", "Copyright", "Syndication" or "RSS terms". Many news sites also have a separate "RSS feed terms" page.
2. Read for these questions and write the answers down in your own words:
   - Can we quote a short excerpt (a sentence or two) with a link and the outlet's name? (yes / no / only with permission)
   - Can we republish the full text? (usually no for news outlets)
   - Is use of the feed limited to personal or non-commercial use? (our site is commercial, so this matters)
   - Is there a rule on automated or AI use of the content? (many outlets now ban it)
3. If the terms are unclear, or ban AI or commercial use, treat the source as signal only and leave it unchecked. You can email the outlet for permission later.
4. Record who checked, the date, the terms page URL and the answers.

How the newsroom uses the answer: "excerpt allowed" sources are cited with short quotes only; "full text allowed" sources (government and open-licence bodies) can be cited fully.

## The sources

| # | Source | Feed or dataset | Declared role | Order |
|---|---|---|---|---|
| 1 | UN Environment Programme | https://www.unep.org/rss.xml | evidence-full | START HERE |
| 2 | NASA | https://www.nasa.gov/news-release/feed/ | evidence-full | START HERE |
| 3 | data.gov.sg: Retrenched Employees (MOM) | dataset d_000d49cda016c13522d7d5be6a050f59 | evidence-full | START HERE (look for the data.gov.sg Open Data Licence) |
| 4 | Eco-Business | https://www.eco-business.com/feeds/news/ | evidence-excerpt | START HERE (Singapore sustainability) |
| 5 | CNA | https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml | evidence-excerpt | next |
| 6 | CNA Singapore | https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511 | evidence-excerpt | next (same terms as CNA) |
| 7 | BBC News Asia | https://feeds.bbci.co.uk/news/world/asia/rss.xml | evidence-excerpt | next (BBC has a separate RSS terms page) |
| 8 | Al Jazeera | https://www.aljazeera.com/xml/rss/all.xml | evidence-excerpt | later |
| 9 | Bernama | https://www.bernama.com/en/rssfeed.php | evidence-excerpt | later |
| 10 | The Guardian Environment | https://www.theguardian.com/environment/rss | evidence-excerpt | later |
| 11 | The Straits Times Singapore | https://www.straitstimes.com/news/singapore/rss.xml | signal | leave as signal |
| 12 | The Straits Times Asia | https://www.straitstimes.com/news/asia/rss.xml | signal | leave as signal |
| 13 | The Business Times | https://www.businesstimes.com.sg/rss/singapore | signal | leave as signal |
| 14 | Mothership | https://mothership.sg/feed/ | signal | leave as signal |
| 15 | Malay Mail | https://www.malaymail.com/feed/rss/malaysia | signal | leave as signal |

"Signal" sources only help the newsroom notice what is happening. Their terms need no check, because the newsroom will not quote them.

## Record sheet (copy one block per source)

Source:
Checked by:
Date:
Terms page URL:
Short excerpt with link and credit allowed: yes / no / ask first
Full text republication allowed: yes / no
Commercial use allowed: yes / no / unclear
Automated or AI use banned: yes / no / unclear
Decision: cite as evidence (excerpt) / cite as evidence (full) / signal only

## Where it gets entered
After the newsroom is deployed (Part B), open `https://<newsroom-host>/ops/sources` (behind Cloudflare Access) and enter the checked-by name, date and the allowed use for each source. Until then, just fill in this sheet and keep it.

Do not guess. If you cannot find the terms page, leave the source as signal only. The system is built to fail closed.
