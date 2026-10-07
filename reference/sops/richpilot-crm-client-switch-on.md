# Switching the CRM on for a client

The checklist for putting one client on the CRM, from a brand new client to a live one. It is the short version of the README ("CRM") and `docs/new-client-handoff.md` ("CRM"). If the two ever disagree, the README and the code win.

Who does what: **you** means whoever is running the rollout (an agent with the Supabase connector can do every database step; the admin page ticks and Vercel and GitHub settings need a person). Never touch a client's CRM without their go-ahead.

## 0. One-off checks (once per environment, not per client)

Only needed the first time. Items 1 and 2 were done for production on 2 Oct 2026; re-check if something looks wrong.

1. The CRM migration `0028_crm_core.sql` is applied to the database. Check: `select to_regclass('public.contacts');` returns a name, not null.
2. The phase 2 code is deployed. Check: `GET <app>/api/cron/crm` without a header returns 401, not 404.
3. The CRM tab's migration `0031_crm_tab.sql` is applied, before the tab's code (README, "Rolling out the CRM tab: migration 0031"). Check: `select count(*) from information_schema.columns where table_name = 'clients' and column_name = 'crm_lost_reasons';` returns 1.
4. The CRM tab is deployed. Check: signed in to `/admin`, `<app>/crm` shows "Pick a client to see their CRM", not a 404.
5. `CRON_SECRET` is set in Vercel (Production), and the repository secrets `CRON_SECRET` and `WA_AGENT_APP_URL` exist in GitHub.
6. The **CRM sweep** workflow (Actions tab) runs every five minutes and prints HTTP 200. With no client on the CRM it returns empty results. A 401 means the two `CRON_SECRET` values differ; a 503 means a step failed, so read the log.

## 1. A new client that is not set up yet

Do the normal onboarding first: follow `docs/new-client-handoff.md` (profile, `npm run client:onboard`, `npm run client:check`). The CRM is an add-on, so the client should already be answering WhatsApp correctly before you switch it on. Nothing in the CRM changes how the agent replies.

## 2. Gather what you need from the client

1. Every phone number that messages or calls the business and is not a customer: staff, suppliers, drivers, the owner's personal number.
2. Every email address that is not a customer: the mailbox that forwards bookings into the order desk, office addresses, and the personal addresses staff send from.
3. Whether they want their past chats, calls and orders imported (the history build), and whether they agree to the default retention: contacts with no activity for 24 months are deleted automatically (the minimum is 6 months). Agree the number before you switch on.
4. Their country code if it is not Singapore (default 65). It decides how a local number like `9123 4567` is read.
5. Whether the five default Lost reasons fit (Price, Went with another company, No reply, Date not available, Not a fit). Staff pick one when a deal moves to Lost, or type their own under Other.
6. Whether they have a contact list to bring in (a spreadsheet, another CRM). There is no import screen until plan 3c, so Richmade loads it.

## 3. Step 0: the never-sync list (before anything else)

This list is what stops staff becoming customers. Fill it in before you tick the CRM and before you build history. An entry with an `@` is an email, anything else a phone number. Use bare values (`desk@staffmail.example`, not `Desk <desk@staffmail.example>`). The client's alert number, driver number and voice number are already excluded without being listed.

```sql
update clients
set crm_never_sync = array['+65 9111 2222', '9333 4444', 'desk@staffmail.example']
where slug = '<slug>';

-- or add to what is already there
update clients
set crm_never_sync = crm_never_sync || array['office@staffmail.example']
where slug = '<slug>';

select slug, crm_never_sync from clients where slug = '<slug>';
```

Nothing validates entries, so read the list back and check it. Adding an entry later stops future records only; a contact already made for that number stays.

If the client's country code is not 65, set it now (digits only, 1 to 4, no plus sign):

```sql
update clients set default_country_code = '<code>' where slug = '<slug>';
```

If they want different Lost reasons (at most 20; "Other" is always offered and is not in the list; changing the list does not change deals already lost):

```sql
update clients
set crm_lost_reasons = array['Price', 'Went with another company', 'No reply', 'Date not available', 'Not a fit']
where slug = '<slug>';
```

The never-sync list, the Lost reasons and the country code stay in SQL, done by Richmade, until the CRM settings screens ship in plan 3c.

## 4. Switch it on

1. Open `/admin`, find the client, tick **CRM** under Modules, save. It builds the client's pipeline from the industry template (Coach charter for a coach operator, General otherwise) and the CRM section shows **Active**.
2. Check the template landed:

   ```sql
   select p.name as pipeline, count(s.id) as stages
   from pipelines p left join pipeline_stages s on s.pipeline_id = p.id
   where p.client_id = (select id from clients where slug = '<slug>')
   group by p.name;
   ```

   There should be one default pipeline with a New, a Won and a Lost stage among its stages.
3. Check retention and country code in the CRM section of `/admin`. They should match what you agreed.

## 5. Build from history (optional)

Only if the client wants their past imported, and only after step 3. In the CRM section, press **Build the CRM from history**. It needs an agency session, runs no AI, and can take a few minutes. Keep the page open until it says it is finished.

What it does: reads the last 12 months (never further back than the retention cut-off) and writes contacts, chat, call and order entries on their timelines. It opens deals only for orders: confirmed or keyed orders go straight to Won, and orders still open only if they changed in the last 30 days. It never moves a deal someone else made to Won. Pressing it again is safe and adds nothing that is already there. Old chats are not summarised.

Check afterwards:

```sql
select action, count, created_at from crm_admin_log
where client_id = (select id from clients where slug = '<slug>')
order by created_at desc limit 5;

select (select count(*) from contacts where client_id = c.id) as contacts,
       (select count(*) from deals where client_id = c.id) as deals,
       (select count(*) from activities where client_id = c.id) as activities
from clients c where c.slug = '<slug>';
```

If a staff member shows up as a contact, add them to the never-sync list and delete that contact by hand. The list only stops future records.

## 6. Check the CRM tab as the client's Admin

The client's Admin needs their own staff account first (`docs/new-client-handoff.md`, "Staff accounts"). Go through these with them signed in (on a call or sharing their screen), so you see exactly what their staff will. You can look first as Richmade, with the client picked in the CRM header (`/crm/deals?client=<slug>`), but that does not replace their check: only their session shows the sidebar count and proves the tab is scoped to their client.

1. **CRM** is in their sidebar after Calls, and there is no Client picker in the CRM header.
2. **Deals board:** one column per stage of their template, in order, with the deals from history (confirmed orders under Won, recent open orders under New). Deals the AI or the history build opened have no value until staff set one, so the Open pipeline card counts them as without a value.
3. **A contact page:** open a contact you recognise. Their phone and email, their open deals and their timeline (chats, calls, orders) match what you know of them, and nobody on the never-sync list appears as a contact (search for a staff name or number).
4. **My tasks:** Mine, Unassigned and Everyone load. Right after the history build there are usually none, which is fine; the AI's Call back tasks appear here after a handover.
5. **Suggestions:** loads, and the count on its section tab matches the list. It is usually empty until the AI has read a few new chats.

## 7. Watch the first two sweeps

1. After the next two **CRM sweep** runs, confirm they are green (HTTP 200).
2. Have a test number message the client's WhatsApp line with a real enquiry (for example a coach hire with a date and a headcount). Within seconds the chat header shows the contact and, for a genuine enquiry, a deal at the first New stage, which also appears on the CRM tab's board. The header refreshes about every 30 seconds.
3. After 30 minutes of quiet in that chat, the next sweep writes a one or two sentence summary on the contact's timeline. Check there is no price in it. The AI never writes a price or sets a deal's value.
4. Look for stuck work:

   ```sql
   select b.id, b.last_message_at, b.ai_attempts, b.repair_attempts,
          b.last_attempt_at, b.last_error,
          (b.ai_attempts >= 3 or b.repair_attempts >= 5) as abandoned
   from crm_bursts b
   where b.client_id = (select id from clients where slug = '<slug>')
     and b.summarised_at is null
   order by b.last_message_at;
   ```

   After fixing the cause, reset the abandoned ones you choose:

   ```sql
   update crm_bursts
   set ai_attempts = 0, repair_attempts = 0, last_attempt_at = null
   where client_id = (select id from clients where slug = '<slug>')
     and summarised_at is null
     and id in ('<burst id>', '<burst id>');
   ```

## 8. What to tell the client

The AI opens a deal when a new chat is a genuine enquiry, raises a Call back task when a chat is handed to a person, moves a deal to Won when an order is confirmed, and summarises each chat when it goes quiet. It only suggests a move to Quoted or Lost, field values and merging two contacts, and staff decide (merge suggestions wait, unshown, until merging ships in plan 3b). It never sets a deal's value or writes a price. Its cost counts toward the same monthly cap as the replies, and over the cap the CRM's AI steps wait until the cap resets while contacts and timelines keep being recorded.

Staff work it in the **CRM** tab: drag a deal to another stage (or use Move; Lost asks for the reason), add notes and tasks, complete tasks, accept or dismiss the AI's suggestions, and undo the AI's changes from the timeline. The chat header, call rows and the order card link into it.

Be honest about the limits: staff cannot yet add or edit a contact, company or deal, merge two contacts, or delete anything (plan 3b), and there are no settings, import or export screens (plan 3c). Until then Richmade changes the never-sync list and the Lost reasons, and loads any contact list. Contacts with no activity for the retention period are deleted automatically, with their timeline, tasks and deals (chats, calls and orders stay). Deleting one person on request is done by the agency with `npm run purge -- --phone +65... --apply` (international form only; try it without `--apply` first to see what it would delete) until plan 3c adds it to the contact page.

## 9. Switching it off, or a problem

- **Untick CRM** on `/admin`: the CRM tab goes from their sidebar, and the AI steps, history and sweep stop for that client. Existing contacts stay and still age out under retention, even if the client is deactivated.
- **Wrong person became a contact:** add them to the never-sync list, then delete the contact in SQL. There is no screen for it until plan 3c.
- **Summary never appears:** run the stuck-work query in step 7.
- **Accept on a suggestion fails, or a refused change takes two minutes:** migration `0031_crm_tab.sql` is not applied (step 0, item 3).
- **Sweep red in GitHub:** open the run log. A 401 is a secret mismatch, a 503 names the failing step by code only. After a Vercel instant rollback to a build from before the CRM, disable the **CRM sweep** workflow until the CRM build is live again.
- **Everything broke after a deploy:** the migrations must be applied before the code, never after. Redeploying the previous build is safe, because the old code ignores the new tables and columns.

## Known limits to remember

Do not promise these away: the chat header chip refreshes about every 30 seconds; the board's Won and Lost columns show the last 30 days only (the list view shows every deal); contacts built from history look recently active; a company created from an order's customer name is not removed by retention; deleting one person does not yet remove their chat burst records (the purge script does); a "will retry" alert can hide the final "abandoned" alert for a chat summary, so check the table rather than the alert.
