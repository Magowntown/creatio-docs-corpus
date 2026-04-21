# Session Log — 2026-04-21

**Context**: Pampa Bay QB integration — continuation of 4/20 work. Dmytro's Create/Update flip (now actually **Delete/Create**) scheduled for tonight 5 PM ET+.

## Morning — escalation and de-escalation

- **12:13 UTC** — Sent "Priority #4" escalation email to Dmytro (prior draft, without the Danlyn manual-2-months framing)
- **13:47 UTC** — Dmytro responded harshly: *"What's? Remanage my queue? Do you understand what you are writing? If I hear anything like that one more time, I'll shut down Pampa Bay project. Period."*
- **14:09 UTC** — Call placed (call log entry from my account)
- **14:22 UTC** — Danlyn: *"Is there any update on this? We need to apply payments. Can I manually update these invoices?"*
- **14:38 UTC** — Dmytro back to operational tone: *"There is a plan from the yesterday's email. Make sure that BGHasInvoice checkbox is unchecked after Invoice is paid... I'll switch the configuration..."*
- **15:06 UTC** — Sent Danlyn the "test-pair tonight" plan email
- **15:18 UTC** — Danlyn: *"I've already started updating them manually. We are now a month behind..."*
- **15:28 UTC** — Dmytro flagged conflation: *"Danlyn was asking about payments. I was asking to confirm if she was asking about Payments from Transactions. You suddenly said that this was about Invoices."*
- **15:57 UTC** — Sent Dmytro disambiguated email separating (1) Payments flow status, (2) 21-invoice list, (3) 4/13 Missing Invoices

## PROD state confirmed this morning

- **IWTransactionAutoPairSweepProcess** (04-21 07:00:01 UTC) — **Completed clean** after 4/20 fix. Prior 3 runs on 4/20 had been Error (pre-fix ESQ bug).
- **IWOrderBGHasInvoiceAutoUncheckEnabled** SysSetting — `BooleanValue=true`, ModifiedOn `2026-04-20T22:30:43`. Listener armed.
- **Unpaired IWTransactions**: 0 (backlog clean).
- **Customer orders with stuck BGHasInvoice=true since 04-14**: 0.

## InterWeave middleware configuration — full capture

User shared screenshots of all middleware config pages. Key findings:

### Scheduler (first screen)
- **Creatio2QBCustInvoice** — RUNNING every 10 min. 560 successes / 8 failures. Last run today 12:26.
- **Creatio2QBItem** — RUNNING but hasn't succeeded since 2026-03-31. 0/7 runs. **Silently failing for 3 weeks.** Likely contributing to 4/13 "Missing Invoices".
- **Creatio2QBVendorPO** — RUNNING. 6/1.
- **QBInvoices2Creatio** — RUNNING every 3 hrs. Limited to Balance/Payments writes only (row 46 of config).
- **NO Payment flow scheduled.** Config exists (see PO/PR/Bill page rows 51-68) but never started. This is what Dmytro is turning on tonight.
- All 12 "Utility" flows STOPPED since 2006 — legacy/unused.

### Invoice config (CRM Order → QB Invoice)
- **Row 3 (THE CRITICAL SETTING)**: "Permitted sync operations from CRM Order to QB Invoice" = **Create Only** → flipping to **Delete/Create** mode tonight (not Create/Update as initially assumed).
- **Row 11/12 (the gate)**: `BGHasInvoice = true` is the trigger field. Our listener flipping it to false on payment = the safety valve.
- **Row 46**: Reverse flow limited to "Update Balance/Payments Only" — QB staleness can't overwrite Creatio.
- **Row 51**: "Update CRM Order amounts with calculated QB Invoice amounts" = Never — Creatio is source of truth.
- **Row 15**: Line item rate field — EMPTY. In practice the middleware pulls OrderProduct.Price (verified via log analysis). This is what reads retail pricing correctly.

### Products config
- **Row 5**: "CRM Field Name For Sales Price" = **BGWholesalePrice** — Products sync to QB with wholesale as Sales Price. **Initially misread as root cause of mismatches; log analysis showed it's NOT affecting invoice line rates.**
- **Row 18**: "Permitted sync operations from CRM Products to QB Items" = Create Only
- **Row 50**: Reverse = Update Only

### PO/PR/Bill config (page 3)
- **Payment flow fully configured** (rows 51-68):
  - Object = IWTransactions
  - Trigger field = IWTransactionStatus = "settledSuccessfully"
  - Permitted ops = **Create and Update**
  - Amount field = IWAuthNetTransactionAmount
  - Unidirectional CRM → QB
- **But never scheduled.** This is the turn-on tonight.

### Brandwise SysSettings — identified as MarketTime SFTP
- BGBrandwiseHost = `files.markettime.com`
- BGBrandwiseUser = `SftpUser_M56121`
- BGBrandwisePort = 22 (SFTP)
- Credentials rotated 2025-05-19/20 (active).
- Brandwise = MarketTime, B2B wholesale trade-show platform. Pampa imports wholesale orders via SFTP file drops.
- Not related to today's issues but worth knowing as a second Order inflow path.

## Log analysis — major reframing

**Initial theory (wrong)**: The 21 invoice mismatches showed 0.40 ratio = BGWholesalePrice/BGMSRP = structural pricing mismatch.

**Actual finding from middleware logs**: The flow is currently pushing **retail prices with discount applied** correctly on Website Sales invoices. Example from 04-21 log:
```
insert into InvoiceLine values('Website Sales', '66153', 'CER1723W',
  'Large Oval Platter - 15% Discount', 1, 85.0, ...)
```
$85 = $100 retail × 0.85 (matches WooCommerce retail - 15% discount). If it were pushing wholesale, rate would be $40.

**Conclusion**: The 21 mismatches are **stale pre-fix records**. Current flow is pricing correctly. Create/Update (or Delete/Create) re-push will correct them.

## Infrastructure concerns (separate)

Middleware running on ancient stack:
```
java.runtime.name=Java(TM) 2 Runtime Environment
java.version=1.5.0_22                    # Released January 2009
java.vm.vendor=Sun Microsystems Inc.     # Sun was acquired 2010
os.name=Windows NT (unknown)
```

**2x JVM crashes today** (07:07:25 and 08:12:13). Service auto-restarts.

**Plaintext credentials in logs**:
```
{"UserName":"Supervisor","UserPassword":"123*Pampa?"}
```
Every Login entry. Security concern, separate from integration logic.

**QODBC connector flakiness**:
- `Error Packet Data - Incorrect Response Received: 108`
- `ExecDirect Packet Data - Incorrect Response Received: 60 - QRemote Client is retrying - 5 - QRemote Client exceeded retry limit - 5`
- Middleware emails Danlyn directly (`iwn_alert18@interweave.biz → danlyn@pampabay.com`) when these fail — explains why she's been seeing errors raw.

## Invoice 64484 — refund reconciliation finding

In the Auth.Net bulk-load CSV pull, row **TR-00130 on 2026-04-07**:
```
2026-04-07T05:00:50,64484 R,7.44,TR-00130,,
```

The "64484 R" refers to invoice 64484 **Refund**. The amount $7.44 matches exactly the delta between Danlyn's originally-flagged Creatio value ($127.50) and Pamela's current value ($120.06).

**Pamela's edits were legitimate refund reconciliation, not errors.** The 21-invoice mismatch pattern reframes as: staff edit orders to reconcile real refunds/returns, but edits silently don't reach QB when invoice is already sent or paid. This strengthens the case for the post-payment edit alert listener.

## Editor patterns

From 500-order sample (2026-04-08 → 2026-04-21):

| Editor | Count | % | Notes |
|---|---|---|---|
| Pamela Murphy | 260 | 52% | Known; edits Order-level fields post-creation |
| Maria Victoria | 152 | 30% | **Second primary editor.** Previously not tracked in our mental model. |
| Danlyn Milito | 50 | 10% | Expected (payments/invoices) |
| Krutika | 29 | 6% | Minor |
| **Rommel @ e6solutions.com** | 2-4 | <1% | **External vendor editing Orders** — flag for visibility |
| Paula | 1 | <1% | |

Any edit-prevention listener must cover both Pamela AND Maria (together = 82% of edits).

## Bruce's call with Dmytro (afternoon)

Bruce spoke with Dmytro directly. Key outcomes captured in Bruce's notes:

### Invoice plan
- Test **2 specific invoices** (Dmytro picks)
- Switching to **"delete and create"** mode (not Create/Update — actually more aggressive)
- Dmytro flagged: **product names are broken on some QB invoices** (NEW issue)
- Rule: *"If checkbox is checked, they should not edit in Creatio"*
- *"If invoice is paid, you cannot alter it"* (confirms our listener design)

### Payment plan
- Payments flow was **never started**
- Dmytro ran one test; Danlyn sent screenshot of invoice
- Dmytro will turn on the scheduled flow tonight
- After Danlyn confirms payments coming in → **bulk load**
- **Bulk load runs TWICE** — one for Payments, one for Invoices (disconnected pipelines)
- Cadence change: payments currently running once a day, Dmytro wants **hourly**

### Tonight's sequence (from Bruce's notes)
1. Start scheduled Payment flow
2. Verify payments arriving in QB → Danlyn confirms tomorrow AM
3. If clean → bulk load #1 (Payments)
4. Test 2 invoices in create-only first
5. Danlyn confirms test invoices correct
6. If clean → switch to Delete/Create mode
7. Bulk load #2 (Invoices)

## Data pulled for Dmytro

1. **Auth.Net Transactions CSV for bulk load (2026-04-02 → present)**
   - 317 rows, 252 paired / 65 unpaired
   - ~15 duplicates (Auth.Net webhook redelivery)
   - ~15 blank-description rows (Auth.Net batch summaries/voids)
   - Refund rows identified (R-suffix): 64484, 63748, 64765, 63870, 65109, 64739, 64435
   - Saved to `/tmp/iwtransactions_2026-04-02.csv`

2. **21 mismatch invoices current state**: all still BGHasInvoice=true, eligible for re-push
   - 20/21 still match Danlyn's original flagged values
   - Invoice 64484 now $120.06 (was $127.50) — explained by TR-00130 refund

3. **4/13 Missing Invoices current state**: all 3 still in Creatio with BGHasInvoice=true
   - 62987 Louisiana Casual Living: $455.40 (10 lines, sum $396.00)
   - 63363 Breed & Co: $1,546.18 (25 lines, sum $1,344.50)
   - 62886 Kentrikon & Noufaro: $4,347.00 (2 lines, sum $3,780.00)

4. **Post-flip scope**: 446 of last 500 Orders have BGHasInvoice=true → first Delete/Create cycle will re-evaluate a large batch

## Email drafts produced

- Dmytro email (post-flip data dump + edit-alert listener proposal) — 340 words, casual tone
- Danlyn email (tomorrow's confirmation checklist + workflow note) — 225 words, decision-prompt structure
- Bruce cheat sheet for his Dmytro call — all pre-call (used by Bruce)
- Bruce writeup (for context if Pampa calls) — 580 words

## Open questions for tomorrow

1. **"Product name is broken"** — specifics? Which products? Which invoices? Ask Dmytro or Danlyn.
2. **Canary invoice numbers** — which 2 did Dmytro pick?
3. **Two bulk loads timing** — same night or spread?
4. **Payments cadence hourly** — does our auto-pair sweep need tuning for race conditions?
5. **Creatio2QBItem has been failing 3 weeks** — is this contributing to the 4/13 missing invoices? Should Dmytro investigate?
6. **Rommel @ e6solutions.com** — who authorized his access? Should be audited.

## Status going into tonight

- **Our side done**: Sweep BP fix (4/20), BGHasInvoice listener (4/20), data pulled and ready
- **Dmytro's turn**: Flip config tonight 5 PM+
- **Danlyn's turn**: Verify tomorrow AM
- **Post-tonight**: Edit-prevention listener proposal pending Dmytro's greenlight
