# Session Log — 2026-04-23

**Context:** Continuation from `SESSION_LOG_20260422.md`. Morning: verified Pampa PROD flows live. Afternoon: live diagnostic loop with Dmytro on Danlyn's 4/22 verification issues.

---

## Headline

- **Ready4QB listener: live, 250 rows flipped, 1 orphan (TR-02141) healed**
- **Option B listener (IWOrderProductInvoiceLineRateListener) live, IWInvoiceLineRate populated on 227/239 new OrderProducts**
- **Inbound QB→Creatio payment flow running** (377 IWPayments in 48h, most recent batch 2026-04-23 04:05 UTC)
- **Outbound Creatio→QB flow running but rejecting on tax-amount mismatches** — first confirmed rejection: TR-02150 $298.55 against INV 66318
- **Dmytro's initial Tax Item = NO_TAX hypothesis debunked** by Danlyn (Customer is already NJ)
- **Dmytro's PO-recycle hypothesis debunked** (all 4 invoices have different POs)
- **Two QB-side diagnostic questions open** — tax flattening on 66318, and TR-00126 triple-invoice split

---

## PROD state verified live

| Pillar | Status |
|---|---|
| `IWTransactions.IWReady4QB` column | Live in PROD |
| `IWTransactionReady4QBListener` (package `IWInterWeavePaymentApp`) | Deployed, firing on inserts |
| `IWTransactionReady4QBEnabled` SysSettings kill-switch | true (IsDef=true) |
| `IWReady4QB=true` count | **250** |
| Settled total | 266 (250 Ready + 15 unpaired + 1 orphan) |
| Orphans (settled+paired+NotReady) | 1 → healed via reactive PATCH test |
| `OrderProduct.IWInvoiceLineRate` column | Live in PROD |
| `IWOrderProductInvoiceLineRateListener` | Deployed, firing (227/239 new OrderProducts populated) |
| Inbound IWPayments 48h | 377 (all linked, QB invoice number populated) |
| Latest inbound batch | 2026-04-23 04:05 UTC |
| Outbound Creatio→QB flow | Running, has started rejecting on tax mismatch |

---

## Orphan TR-02141 — OnInserted middleware race (investigated + closed)

One paired+settled IWTransaction was created with `IWReady4QB=false` despite matching all listener conditions:

- `Id=7215b03c-78b6-4079-bffb-744a611b6999`, `IWName=TR-02141`
- Created 2026-04-23 05:00:36 UTC, `ModifiedOn == CreatedOn` exactly
- Status=settledSuccessfully, IWTROrderId set, but IWReady4QB=false
- Other 11 paired+settled rows in the same 05:00 UTC batch flipped correctly

**Root cause (inferred):** middleware does insert+update inside the same Save() so `ModifiedOn == CreatedOn` at commit. `OnInserted` fires with Entity still in pre-settled state, listener correctly early-returns on status check, and `OnUpdated` never fires because the in-transaction status change is collapsed into the initial save.

**Verification:** Reactive PATCH on TR-02141 (changed `IWResultMessage` harmlessly) triggered `OnUpdated` → `IWReady4QB` flipped `false → true`. Then reverted the test marker. Listener is healthy; the miss was a one-row race inside middleware's save sequence.

**Memory captured:** `feedback_creatio_oninserted_middleware_race.md` — future listeners that depend on column values set during combined insert+update saves should always be backed by a reconcile sweep.

**Mitigation planned:** nightly or 15-min reconcile sweep (task #31) — `UPDATE IWTransactions SET IWReady4QB=true WHERE settled AND paired AND not ready`, kill-switch gated.

---

## Danlyn's 4/22 verification — two issues flagged

Danlyn sent her verification of the 4/22 outbound QB payment batch this morning (14:22 UTC).

### Issue 1: Missing payment ($298.55, INV 66318)

Full Creatio-side record trace:

| Field | Value |
|---|---|
| IWTransaction | TR-02150 (`41ebd3e2-4b6f-4dd9-98dc-e015098d6d4f`) |
| Auth.Net Transaction ID | 121587665323 |
| Amount | $298.55 |
| Ready4QB | true |
| Order | ORD-18414 / INV 66318 (`a665c0ad-6a2a-46bb-aea0-c7c376764796`) |
| BGPONumber | 39309 |
| Order.Amount | $298.55 |
| Created | 2026-04-22 15:28 UTC (matches Danlyn's "3:28 PM" note) |
| Account | Website Sales (`6841b95e-9331-4b22-a659-ea3ff5d4f4df`) |

**OrderProduct lines (Price == PrimaryPrice on all three):**

| Line | Product | Amount (pre-tax) | TotalAmount (w/ tax) |
|---|---|---:|---:|
| 1 | CER2144G | $100.00 | $106.63 |
| 2 | CER2585G | $130.00 | $138.61 |
| 3 | CER1140G | $50.00 | $53.31 |
| Sum | | **$280.00** | **$298.55** |

Delta $18.55 = 6.625% NJ sales tax on $280 merchandise. Creatio side is internally consistent; Auth.Net correctly charged $298.55. This is **not** the Price/PrimaryPrice pattern from the 22 historical rows.

**Bruce's middleware error log (captured by Dmytro and forwarded):**
```
2026-04-23 03:01:35.905 IW 2.41 TS Creatio2QBPR
ERROR XmlsqParams.statement
[QODBC] Error: 3210 - The "AppliedToTxnAdd payment amount" field has an invalid value "298.55".
QuickBooks error message: You cannot pay more than the amount due.
```

**Diagnosis chain:**
1. Dmytro's first hypothesis (16:38 UTC): Customer's Tax Item = NO_TAX (not NJ). Creatio sends pre-tax values to QB, QB computes tax from Customer Tax Item + per-line Tax/Non flag. If Tax Item = NO_TAX, QB computes $0 tax and amount-due is $280 instead of $298.55. He asked Danlyn to verify.
2. Danlyn (18:35 UTC): **Tax Item is already NJ on the Customer.** Hypothesis disproved. She'll check again tomorrow morning if payment appears after any adjustment.
3. **Open:** If Customer Tax Item = NJ, why does QB still compute amount-due = $280? Possible causes: invoice-level tax override on 66318, per-line Tax/Non flag = "Non", or tax calculated at a different rate at invoice-creation time. Needs Alex QODBC read on INV 66318 (invoice tax item, per-line Tax/Non flags, calculated tax total).

### Issue 2: TR-00126 applied to three invoices in QB

Danlyn flagged that the $168 payment for TR-00126 appeared on three unrelated invoices in QB, and confirmed **she did not apply it manually**:
- 62403 — order paid via PayPal
- 62373 — order paid via PayPal
- 59533 — invoice from 2025

**Creatio side:** Clean. One IWTransaction → one Order (ORD-18030, INV 64888, $168) → one IWPayment (163428, $168, `IWQBInvoiceNumber="64888"`, same Website Sales customer). Creatio sent one payment explicitly targeting invoice 64888.

**Dmytro's hypothesis (19:03 UTC):** Recycled PO numbers — all 4 invoices share the same PO?

**PO check (PROD query):**

| BGNumberInvoice | Order | PO | Amount | Created |
|---|---|---|---:|---|
| 64888 (TR-00126 target) | ORD-18030 | **38954** | $168.00 | 2026-04-07 |
| 62403 | ORD-16608 | **37908** | $104.50 | 2026-02-02 |
| 62373 | ORD-16554 | **37843** | $50.00 | 2026-01-30 |
| 59533 | ORD-14862 | **36571** | $91.25 | 2025-12-02 |

**All four POs are different.** PO recycle theory disproved. The common factor is shared customer (Account = Website Sales, `6841b95e`).

**Open:** Why did QB apply a payment explicitly tagged `IWQBInvoiceNumber=64888` onto three other customer invoices (different POs, two already PayPal-paid, one from 2025)? Likely a QB-side auto-apply behavior overriding the Creatio-specified target. Needs Alex QODBC read on the IWPayment 163428 application history in QB.

---

## Communication timeline (today)

| UTC | Sender | Thread | Note |
|---|---|---|---|
| 12:29 | Fireflies | AI Daily Digest | 4/22 meeting recap delivered |
| 14:22 | Danlyn → all | Invoice Errors | 4/22 verification: missing payment, TR-00126 split |
| 14:27 | Dmytro → me + Bruce | Invoice Errors | Forwards TR-02150 transaction record, suspects payment amount issue |
| 14:28 | Dmytro → me (HIGH) | Possible Connection issues | Forwards Bruce's QODBC error log + own 7:20 ET diagnosis |
| 15:07 | Me → Dmytro | Invoice Errors | First data-rich reply with TR-02150 tables |
| 16:38 | Dmytro → me + Bruce + Alex | Invoice Errors | NO_TAX hypothesis, asks Danlyn to verify |
| 17:26 | Me → Danlyn (CC all) | Invoice Errors | Translated ask to Danlyn for Tax Item check + TR-00126 history |
| 18:35 | Danlyn → all | Invoice Errors | Tax Item already NJ; TR-00126 auto-applied not manual |
| 18:58 | Me → Dmytro | Invoice Errors | Forward of Danlyn's update |
| 19:03 | Dmytro → me + Bruce + Alex | Invoice Errors | Recycled PO theory |
| 19:15 | Me → Dmytro + Bruce + Alex | Invoice Errors | PO answer (all different) + reopens tax question |

---

## State of work streams going out of today

| Stream | Status | Blocker |
|---|---|---|
| IWReady4QB listener | LIVE, 250 flipped | None (defense-in-depth sweep is task #31) |
| IWInvoiceLineRate listener | LIVE, 227 populated | Kill-switch retrofit outstanding (task #26) |
| Inbound QB→Creatio payments | Running nightly | — |
| Outbound Creatio→QB payments | Running, choking on amount mismatch | Alex QODBC on INV 66318 + TR-00126 |
| Nightly reconcile sweep for Ready4QB | Designed, not built (task #31) | Implementation |
| 22 historical invoice price divergence | Not addressed post-meeting | Dmytro's decision on upstream-fix vs Option B |
| Dmytro comms | Responsive, looping on diagnosis | Waiting on reply to 19:15 UTC |
| Danlyn | Waiting for tomorrow's AM verification | None |

---

## Open questions requiring QB-side reads

1. **INV 66318 tax:** Invoice-level tax item, per-line Tax/Non flags, calculated tax total. Need Alex QODBC.
2. **IWPayment 163428 QB application:** How was the payment that specified `IWQBInvoiceNumber=64888` routed onto 62403/62373/59533? Need Alex QODBC on transaction application history for the Website Sales customer.
3. **Broader cohort:** If Tax Item flattening is recurring, how many 4/22+ outbound attempts have had the same QODBC rejection? Bruce's log shows at least 1 ($298.55); there may be others.

---

## Captured learnings (memory writes)

- `feedback_creatio_oninserted_middleware_race.md` — OnInserted fires at commit; middleware's combined insert+update collapses into a single save, leaving OnInserted with pre-update Entity state. Always pair such listeners with a reconcile sweep.

---

## Suggestions raised but not yet committed

- **`IWInvoiceLineRate` authoritative per-line rate** — floated to Dmytro in the 15:07 reply (as an exploratory "something I've been looking into" framing). NOT disclosed as already deployed. Dmytro has not responded to the suggestion yet.

---

## Pickup for tomorrow (4/24)

1. Watch inbox for Danlyn's AM verification on INV 66318 payment appearance
2. Watch inbox for Dmytro's response to 19:15 UTC PO answer + reopened tax question
3. If Alex is asked to run QODBC reads, provide him the exact queries for INV 66318 and TR-00126 application history
4. Build nightly Ready4QB reconcile sweep (task #31) — low-risk, high-value safety net
5. Retrofit kill-switch on `IWOrderProductInvoiceLineRateListener` (task #26 variant)
6. If Dmytro asks about `IWInvoiceLineRate` as an approach, disclose that the column + listener are already deployed and explain coverage + gaps
