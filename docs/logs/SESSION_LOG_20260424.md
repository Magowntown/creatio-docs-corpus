# Session Log — 2026-04-24

**Context:** Day after the 4/23 live diagnostic loop with Dmytro/Danlyn on TR-02150 + TR-00126. Watching for replies, confirming overnight flow health, fielding Danlyn's strategic check-in.

---

## Headline

- **Overnight flow healthy.** IWReady4QB 250 → 267 (+17), 0 orphans on the settled+paired+NotReady query, 10 inbound QB→Creatio payments landed at 04:04 UTC, 32 new IWTransactions since 4/23 19:00 UTC.
- **TR-02150 / INV 66318 / $298.55 still stuck on QB side.** Today's inbound batch covered invoices 66286–66356 — 66318 is not in it. Danlyn confirmed the rest of yesterday's outbound batch reached QB cleanly.
- **No reply from Dmytro all day** to either the 4/23 19:15 UTC PO answer or the 4/24 13:07 UTC AM update.
- **Danlyn shifted from individual-issue to strategic** — asked end of day whether the daily flow is staying live and what's the ETA on the 4-day bulk load. Forwarded to Dmytro 20:29 UTC.
- **Alex's "Fixed" (14:33 UTC) was Southernlamps** on Bruce's "Possible Connection issues" thread — not Pampa.

---

## PROD state (verified live ~6 AM ET, 2026-04-24)

| Signal | 4/23 EOD | 4/24 AM | Delta |
|---|---:|---:|---:|
| `IWReady4QB=true` | 250 | 267 | +17 |
| Settled total | 266 | 287 | +21 |
| Settled + paired + NotReady (orphan candidates) | 0 | 0 | clean |
| New IWTransactions since 4/23 19:00 UTC | — | 32 | flowing |
| Inbound IWPayments today | — | 10 (inv 66286–66356) | batch landed 04:04 UTC |

The 287 − 267 = 20 gap is **not** orphans — it's settled-but-unpaired txns (no `IWTROrderId`), which correctly don't flip because the listener requires a linked Order. Latest 3 IWTransactions (TR-02208 / 2209 / 2210, all 05:00 UTC) settled + paired + Ready4QB=true. The TR-02141 race fix from 4/23 is holding.

---

## Communication timeline (today)

| UTC | Sender | Thread | Note |
|---|---|---|---|
| 13:07 | Me → Dmytro (CC Bruce/Alex/Danlyn) | Invoice Errors | AM update with PROD overnight state + reopened tax question on INV 66318 |
| 14:33 | Alex → Bruce (CC Dmytro/me) | Possible Connection issues | "Fixed" — for **Southernlamps**, not Pampa |
| 16:57 | Danlyn → me (CC all) | Invoice Errors | "Payment for 63318 [sic — 66318] still hasn't come through. I checked the payments received yesterday and **all orders that had invoices last night are applied on QB!**" |
| 16:58 | Me → Danlyn | Invoice Errors | "Understood! We are looking into it." |
| 20:26 | Danlyn → me (CC all) | Invoice Errors | **Strategic check-in:** "I wanted to confirm that the payment flow into QB will be staying live and running every day and we're just waiting on the bulk load to be done for those 4 days – correct? Do we know when the bulk load will be completed?" |
| 20:29 | Me → Dmytro (CC Bruce/Alex) | Fw: Invoice Errors | Forwarded Danlyn's question. "Is this something Alex can do, or do we still need to configure something? I would like to update her before EOD." |

**Dmytro silent all day** on every Pampa thread.

---

## Outbound→inbound roundtrip — Danlyn's 16:57 UTC verification

Material confirmation that the entire chain — Auth.Net inbound → IWTransactions Ready4QB flip → middleware Creatio2QBPR push → QB invoice apply → QB→Creatio inbound IWPayment write-back — is functioning end-to-end **except** for invoices that hit the QB-side amount-due mismatch (currently 1: INV 66318).

PROD-side check confirms Danlyn's narrative:
- `IWPayments` for `IWQBInvoiceNumber='66318'`: count 0
- `IWPayments` with `IWAmount=298.55`: count 0
- Today's batch invoice range: 66286–66356, 66318 absent

So 66318 is alone — the structural issue affects only invoices QB rejects on amount-due, and as of 4/24 AM that's a single invoice.

---

## TR-02150 / INV 66318 — diagnosis state unchanged

No new data since 4/23 EOD. Open candidates remain:
- (a) invoice-level tax item override on 66318 = NO_TAX
- (b) per-line Tax/Non flag = "Non" on these lines despite customer default NJ
- (c) tax rate at invoice creation time differed from current

All three need an Alex QODBC read on INV 66318 (invoice tax item, per-line Tax/Non flags, calculated tax total) to discriminate. Danlyn already disproved the customer-level Tax Item theory yesterday.

---

## TR-00126 triple-split — diagnosis state unchanged

No new data. Question still open: why did QB auto-apply IWPayment 163428 (which specified `IWQBInvoiceNumber=64888`) onto 62403/62373/59533? PO recycle was disproved 4/23. Needs Alex QODBC read on the IWPayment 163428 application history.

---

## Strategic split surfaced by Danlyn's 20:26 UTC question

Danlyn cleanly bisected the Pampa universe into two tracks:

1. **Ongoing daily flow** — She's treating this as resolved and just wants confirmation it stays on. Our morning update covered this with live data.
2. **4-day historical bulk load** — Still outstanding. ETA depends on Dmytro's Option-B / delete-create scheduling. We have not given her a date because Dmytro hasn't confirmed one.

That bisection is correct and useful. It shifts the framing: Pampa is no longer "in incident response" — they're in "scheduled-cleanup-of-known-backlog" mode.

---

## State of work streams going out of today

| Stream | Status | Blocker |
|---|---|---|
| IWReady4QB listener | LIVE, 267 flipped | None |
| IWInvoiceLineRate listener | LIVE | Kill-switch retrofit outstanding (task #26) |
| Inbound QB→Creatio payments | Running daily | — |
| Outbound Creatio→QB payments | Running, only 66318 stuck | Alex QODBC on INV 66318 |
| TR-00126 triple-split investigation | No new data | Alex QODBC on IWPayment 163428 application history |
| 4-day historical bulk load | Designed, not scheduled | Dmytro decision (Option B+Delete/Create + bulk re-push window) |
| Nightly Ready4QB reconcile sweep | Designed, not built (task #31) | Implementation |
| Dmytro comms | Silent all day | Awaiting reply on 13:07 + 20:29 UTC threads |
| Danlyn | Asking strategic questions, not firefighting | Awaiting Dmytro on bulk-load ETA |

---

## Pickup for Monday (4/27)

**Note: 4/25 + 4/26 are weekend. Dmytro and Danlyn likely won't move until Monday.**

1. **First action Monday morning**: Watch for Dmytro reply over the weekend. If still silent, bundle the two open asks (tax-flattening + bulk-load ETA) into a single short Monday follow-up tagged for action.
2. **Reply to Danlyn directly** with daily-flow confirmation if Dmytro hasn't moved by Monday EOD — she asked for "before EOD" on Friday and we missed that window already (forward sent 20:29 UTC = 4:29 PM ET Friday).
3. **Possible direct ask to Alex** for the QODBC reads on INV 66318 + IWPayment 163428 — bypassing Dmytro if he stays silent. Lower-friction than waiting another business day.
4. **Continue holding** on tasks #26 (kill-switch retrofit), #27 (reconcile sweep design), #31 (Ready4QB sweep promotion). No urgency, all design work.
5. **Do NOT disclose `IWInvoiceLineRate` proactively** — Dmytro hasn't engaged with the 4/23 "something I've been looking into" framing. If he asks Monday, disclose; otherwise keep it as floated-but-not-pressed.

---

## What changed in our memory/docs at end of day

- `SESSION_LOG_20260424.md` (this file)
- `project_pampabay_qb_export_issues.md` — prepended 4/24 EOD section
- `reference_pampabay_tr02150_qodbc_tax_rejection.md` — added 4/24 status note (Danlyn's "all others applied" verification confirms 66318 isolated)
- `MEMORY.md` — Pampa line refreshed
- `docs-corpus/CLAUDE.md` — status banner bumped from 4/23 to 4/24
