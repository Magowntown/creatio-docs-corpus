# Session Log — 2026-05-01 (Pampa Bay PayPal Mis-Application Crisis)

## Headline

PayPal-tagged invoices in QB are being silently paid by Auth.Net charges via the Creatio→QB outbound flow. Two root causes identified, listener cleared, halt-list compiled. Awaiting Bruce/Dmytro green-light for action.

## Problem statement (per Danlyn)

> "On our website, customers can either checkout through Authorize.net or PayPal. All orders (regardless of payment terms) come in via the Website Sales customer. The Authorize.net Transactions that you are flowing into QB are applying to incorrect invoices. These invoices were not paid via Authorize.net, but rather PayPal. For Website Sale invoices that were paid via PayPal, we apply the payment manually."

> "Before the payments [import] went live we probably had at least 40+ invoices paid via PayPal open under the Website Sales customer and now there are none."

## Evidence

| Source | Finding |
|---|---|
| Danlyn TR-000014 / Inv 64981 example | TR-00014 ($124, Auth.Net source ORD-17837 / **BGInv 64435**, PO 38756) was applied in QB to **invoice 64981** (PayPal-paid, PO **38988** — different PO). |
| Danlyn TR-00015 example | Single Auth.Net charge $185.53 split across **3 separate February PayPal invoices** (62660 $9.37 + 62674 $160 + 62757 $16.16). |
| `PayPal.xlsx` attachment | 166 Website Sales Orders explicitly tagged `Terms = PayPal` since January. |
| `Open Balance.pdf` attachment | Customer balance $19K open / $20K amount; **35+ TR-NN payments showing negative open balance** (unapplied credits sitting in QB). Earliest dated **2026-02-12**. |
| PROD query — 4/28 backfill cluster | 303 IWTransactions modified within 12:47-12:49 UTC on 2026-04-28 — exact match to InterWeave-side backfill. |
| PROD sample drift check | 15 of 15 sampled records show current `IWTROrderId` matching the deterministic-rule Order (InvDesc prefix == BGPONumber + Amount match). Zero drift. |

## Root cause (two layers)

**Layer 1 — QB push lacks target invoice.** Integration sends `Customer + Amount + Reference` only. QB's auto-applier consumes oldest-open balance first across the entire Website Sales customer pool — which contains both Auth.Net and PayPal-paid invoices. PayPal invoices are intentionally held open until quarterly reconciliation by Pampa staff, so they're prime auto-apply targets.

**Layer 2 — 4/28 backfill cascade.** InterWeave's backfill PATCHed Account/Owner/Contact onto 303 IWTransactions to fix a separate listener regression. Each PATCH bumped `ModifiedOn`. The QB outbound flow triggers on `ModifiedOn` change (per Dmytro's design), so each of the 303 records re-pushed to QB. QB's auto-applier then distributed each Auth.Net charge across PayPal-paid invoices. This is the cascade source for the "40+ wrong applications + 35+ unapplied credits" Danlyn observed.

## Listener cleared (cannot relink)

```csharp
public override void OnUpdated(object sender, EntityAfterEventArgs e) {
    ...
    if (entity.GetTypedColumnValue<Guid>("IWTROrderId") != Guid.Empty) {
        return;   // hard guard against relink
    }
    ...
}
```

`OnUpdated` early-returns when `IWTROrderId` is set. Once paired, the listener will not re-evaluate. The 4/28 backfill PATCHed `IWAccountId`/`IWOwnerId`/`IWContactId` only — never `IWTROrderId`. So no relinking occurred via our code.

Empirical confirmation: 15 random samples from the 303 — every `IWTransaction.IWInvoiceDescription` prefix matches the linked `Order.BGPONumber` exactly, with matching Amount. Zero drift = no historical relinking.

## Audit-table situation

Creatio's data audit feature is **NOT enabled** on Pampa PROD's IWTransactions schema:

| Check | Result |
|---|---|
| `IWTransactionsLog` / `IWTransactionsAudit` / `IWTransactionsHistory` | Do not exist |
| `ChangeLogEntity` | Exists, **0 rows** |
| `SysSchema.LogChanges` | No such column |
| `SysOperationAudit` | Security operations only, not data audit |

So historical column changes cannot be queried. Verification relies on: code review + current-state drift sample + ModifiedOn timestamp clustering.

## Communication thread

| Time UTC | From | Key content |
|---|---|---|
| 13:20 | Danlyn | "QB has been updated and the payments reapplied to invoice 62539" — green light to flip create/update mode |
| 17:37 | Danlyn | Opens new issue: Auth.Net transactions applied to PayPal invoices in QB |
| 17:44 | Bruce | "We are not reading PayPal. Is this an integration with QuickBooks and PayPal?" |
| 18:05 | Danlyn | TR-000014 → inv 64981 example |
| 18:14 | Danlyn | Architecture explanation: Auth.Net + PayPal both checkout under Website Sales |
| 18:58 | Bruce | Forwarded Andrew's brief to Dmytro on separate "Update from Andrew on Pampa" thread |
| 19:11 | Bruce → Danlyn | "PO number should be declared Unique and this will not happen" + Andrew's analysis quoted |
| 19:20 | Danlyn | **POs ARE unique on both sides.** Inv 64435 = PO 38756. Inv 64981 = PO 38988. 40+ PayPal invoices were open before payments import; now none. |
| 19:25 | Danlyn | **Single TR-00015 split across 3 PayPal invoices** (impossible from Auth.Net source — proves QB auto-distribution) |
| 19:43 | Danlyn | Sends `PayPal.xlsx` (166 orders) + `Open Balance.pdf` |
| 20:18 | Bruce | Forwards Andrew's full hypothesis brief to Dmytro |
| 20:35 | Dmytro | Confirms QB integration is also POST-only. Asks: "why is it always relinked to a different Order — confirm from Creatio history?" |
| 20:47 | Andrew | "I'll take a closer look" — investigation queued |
| (drafted) | Andrew → Dmytro | Reply addressing each of Dmytro's points; ready to send |

## Outputs

| File | Contents |
|---|---|
| `~/Downloads/Pampa_PayPal_Halt_Targets_2026-05-01.csv` | 166 Orders + 6 paired IWTransactions to gate (`IWReady4QB=false`) |
| `~/Downloads/Pampa_PayPal_Unwind_2026-05-01.csv` | 0 rows (no PayPal-paired IWTransaction had `IWQBLastModified` set yet — the QB outage caught us before more pushed) |
| `~/creatio-hub/packages/Pampa_PayPal_MisPairings_2026-05-01.csv` | Earlier 9-row scan via `BGPaymentType='PP'` discriminator |

## Pending decisions

| Decision | Owner |
|---|---|
| Approve halt PATCH on 166 PayPal Orders + paired IWTransactions | **Bruce** |
| Confirm outbound flow trigger: ModifiedOn-based vs Ready4QB-transition-based | **Dmytro** |
| Confirm whether QB push payload currently carries target `BGNumberInvoice` | **Dmytro** |
| Run full Open Balance for Website Sales filtered to TR-NN-numbered payments | **Alex** (when QB is stable) |
| Unwind mis-applied + reapply correct (or hold as customer credit) | **Danlyn** (with Andrew's list) |

## Memory written today

- `feedback_creatio_modifiedon_repush_loop.md` — backfill PATCH cascades to outbound re-push
- `feedback_qb_push_target_invoice_required.md` — QB auto-distributes when target invoice is omitted
- `feedback_creatio_audit_not_enabled.md` — Pampa IWTransactions has no historical audit
- `project_pampabay_qb_export_issues.md` — updated with 5/1 section; description rewritten

## Pickup Monday 5/4

1. Send the drafted Dmytro reply.
2. Pending Bruce green-light: run halt PATCH on 166 PayPal Orders.
3. Capture Dmytro's answers on the two architectural questions.
4. Capture Alex's QB-side Open Balance run (the authoritative unwind list).
5. Listener regression on 5/1 morning batch (17 of 17 paired-no-Account/Owner) is **separate** from the PayPal cascade — defer unless it persists.
