# 9 Solar News newsroom: your setup checklist (step by step)

Internal. Not for the client. Built from `docs/newsroom-ops.md` on the branch `build/autonomous-newsroom`.

How to use this: do the steps in order. After each "Send me" line, paste the value into the chat and I will put it in the right file and run the checks. Never paste a secret (a key or token) into the chat: secrets go straight into Cloudflare with `wrangler secret put`, which asks you to type them in your own terminal.

Legend: FREE = costs nothing. PAID = needs your pending payment to land first. DECISION = a person has to decide, not a tool.

---

## Part A. Do these now (FREE, no payment needed)

### A1. Sanity project (FREE plan is enough to start)
1. Go to sanity.io/manage and click "Create new project". Name it "9 Solar News".
2. In the project, open Datasets. Keep `production`. Click "Add dataset", name it `staging`, choose Public or Private as you like (Private is safer).
3. Open API > Tokens > "Add API token". Name: `newsroom-write`. Permission: Editor. Copy the token once and keep it in your password manager. This is a secret.
4. Copy the Project ID from the project home page.
Send me: the Project ID (not the token).

### A2. Sanity webhook filter
1. In Sanity, open API > Webhooks and find the webhook that triggers the site build.
2. Edit its Filter and append: `&& !(_id in path("nr-**")) && !(_id in path("translation.metadata.article.nr-**"))`
3. Save. Reason: the newsroom triggers one build per cycle itself, so it must not trigger one per document.

### A3. Telegram bot
1. In Telegram, open @BotFather and send `/newbot`. Name it "9 Solar News Desk" and pick a username ending in `bot`.
2. BotFather replies with a token. Keep it as a secret.
3. Find your own Telegram user id: message @userinfobot and note the number it replies with. Do the same for any second operator.
4. Make up a long random string for the webhook secret (a password manager can generate 32 characters, letters and digits only). Keep it as a secret.
Send me: the user id(s) (these are not secret).
Note: add the bot only in a private chat with each operator, never in a group.

### A4. Image search keys (both have free plans)
1. unsplash.com/developers: create an app, copy the Access Key.
2. pexels.com/api: request an API key.
Keep both as secrets.

### A5. Turnstile widget (the spam check on the Report an error form)
1. Cloudflare dashboard > Turnstile > Add widget. Domain: the site's domain (the workers.dev one for now). Mode: Managed.
2. Copy the Site Key (public) and the Secret Key (secret).
Send me: the Site Key.

### A6. Source terms checks (the one that blocks everything)
This is a human job, 20 to 30 minutes per source. Open `docs/newsroom-ops.md`, then for each source in the newsroom (list at `/ops/sources` once deployed, or in `newsroom/migrations/0002_sources.sql`):
1. Open the source's terms of use or copyright page.
2. Decide: may we quote short excerpts with a link and credit? May we use the full text? Or is it a signal only?
3. Write down who checked, the date, and what the terms allow.
Until a source has a recorded terms check, the newsroom may find stories from it but cannot cite it, so in shadow mode almost every story would be killed.

---

## Part B. Needs your payment (PAID, wait until it has landed)

### B1. Cloudflare Workers Paid plan
1. Cloudflare dashboard > Workers & Pages > Plans > choose Workers Paid (US$5 a month). This is required for Workflows, Cron and D1 at the volumes the newsroom uses.
2. Run `npx wrangler login` in a terminal to sign this machine in. Run it from `newsroom/` after `export PATH="$HOME/.local/bin:$PATH"`.

### B2. Create the Cloudflare resources
Run these in `newsroom/`:
```bash
npx wrangler d1 create newsroom
npx wrangler r2 bucket create newsroom-evidence
npx wrangler kv namespace create EDGE
```
Each prints an id. Send me: the D1 database id and the KV namespace id. I put them in `newsroom/wrangler.jsonc` and `/wrangler.jsonc` (replacing `REPLACE_WITH_D1_ID` and `REPLACE_WITH_KV_ID`), the Sanity project id, the Telegram user ids and the Turnstile site key.

### B3. Create the database tables
After I have updated the config:
```bash
cd newsroom && npx wrangler d1 migrations apply newsroom --remote
```

### B4. Anthropic key in the client's name
1. console.anthropic.com: create the organisation or workspace in Mr Saat's name, add the payment method, and set a monthly spend limit of US$100 there as well (belt and braces with the newsroom's own cap).
2. Create an API key named `9solar-news-newsroom`. Keep it as a secret.

### B5. Put the secrets into Cloudflare
Run each line in `newsroom/`; it asks you to type or paste the value:
```bash
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put SANITY_WRITE_TOKEN
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
npx wrangler secret put TURNSTILE_SECRET
npx wrangler secret put UNSPLASH_ACCESS_KEY
npx wrangler secret put PEXELS_API_KEY
npx wrangler secret put CF_DEPLOY_HOOK_URL
npx wrangler secret put CF_PREVIEW_DEPLOY_HOOK_URL
```
The two deploy hook URLs come from B6 and B7.

### B6. Production deploy hook
Cloudflare > the site Worker `9solarnews` > Settings > Builds > Deploy hooks > create one. Confirm in the same place that the Worker name is `9solarnews` and the deploy command is `npx wrangler deploy`. Use the hook URL for `CF_DEPLOY_HOOK_URL`.

### B7. Staging site for shadow mode
1. Create a second Workers project from the same GitHub repo, named `9solarnews-preview`, with the build variable `SANITY_DATASET=staging` (and the same Sanity project id).
2. Put it behind Cloudflare Access (Zero Trust > Access > Applications) so only you and Mr Saat's team can see it.
3. Create its deploy hook and use it for `CF_PREVIEW_DEPLOY_HOOK_URL`.

### B8. Deploy the newsroom Worker
```bash
cd newsroom && npx wrangler deploy
```
Send me: the Worker's URL it prints (the "newsroom host").

### B9. Point Telegram at the Worker
Open this in a browser, with your own values filled in (this one is safe to do in a browser, but do not paste it into the chat):
`https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<newsroom-host>/telegram&secret_token=<TELEGRAM_WEBHOOK_SECRET>`
Then message your bot `/status` in a private chat to test.

### B10. Protect the dashboard with Cloudflare Access
1. Zero Trust > Access > Applications > Add > Self-hosted. Domain: `<newsroom-host>`, path `/ops*`. Policy: allow only the operators' emails.
2. Copy the Application Audience (AUD) tag and your Zero Trust team domain.
Send me: the AUD tag and the team domain. I set `ACCESS_AUD` and `ACCESS_TEAM_DOMAIN`, then you redeploy with `npx wrangler deploy`.

### B11. Site build settings for the report form
On the site Worker's build variables add `PUBLIC_TURNSTILE_SITEKEY` (the site key from A5) and `PUBLIC_REPORT_ENDPOINT=https://<newsroom-host>/report-error`.

### B12. Merging and deploying the site
Merging `build/autonomous-newsroom` to `main` and pushing deploys production. Tell me "merge and push main" when you are ready and I will do exactly that push after you confirm once more. Do B1 to B11 first, so the site Worker has its KV binding.

---

## Part C. Decisions and people (DECISION)

| # | Who | What | Why it blocks |
|---|---|---|---|
| C1 | You with Mr Saat | Publisher of record, and the liability terms for AI-published stories | A legal owner is needed before anything is live |
| C2 | You | The IMDA bond figure, and a check whether a licence applies at your traffic | See the 50,000 Singapore visitors a month rule in the ops guide |
| C3 | A fluent Malay speaker (once) | Review the Malay output during shadow mode, plus the Malay UI strings | The Malay check is a back-translation, not a native check |
| C4 | A native speaker | Check the Chinese and Arabic UI strings (drafted by Claude) | Those languages stay switched off until checked |
| C5 | You with Mr Saat | Brand name and a real contact email | The site still has no real contact address; nothing is invented |
| C6 | You | An analytics source (Google Analytics 4 or Cloudflare Web Analytics) | The audience alert is not built until a source and token exist |

---

## Part D. Switching it on (after A to C)

1. **Stage 0a, golden run.** Tell me "run the golden set". It costs about US$3 on the Anthropic key and I will ask you for the key in your own terminal, not the chat. It must exit 0.
2. **Stage 0b, shadow mode** (the default setting). It publishes only to the staging site. For at least 14 days, open `/ops/story/<id>` on the stories and score them. When `/ops/shadow` says every criterion is met, move on.
3. **Stage 1.** Open `https://<newsroom-host>/ops`, set Stage to `live-low` in the settings form (or ask me to walk you through it). Run 14 days with zero critical errors and zero takedowns.
4. **Stage 2.** Set Stage to `live-medium` the same way. Drop back to `live-low` after any critical error.
5. **Daily:** answer Telegram alerts. Emergencies: `/kill`, `/takedown <url> <notice>`, `/banner <url> <exact wording>`. The runbook is at `/ops/runbook`.

---

## What I can do the moment you send values
- Fill the ids into the config files and re-run all tests.
- Run the Sanity seed import once the project and token exist (you run it, it needs the token).
- Check the staging site and the report form in a headless browser.
- Write the monthly analytics check into the runbook once C6 is chosen.

## Known open items I am fixing now
The last review's open items (reader-triggered corrections must always be a proposal, the source-change re-check cost, the terms-note check, Studio delete buttons, one link colour) are being fixed on the branch. Check `docs/newsroom-ops.md` again after that lands.
