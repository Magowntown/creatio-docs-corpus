# Session Log — 2026-05-05 (Pampa Bay PayPal Cascade — Dmytro Directive + Code Prep)

## Headline

PayPal mis-application cascade still active. Three new mis-applications today, including one on a check-pay account that doesn't use Auth.Net (containment break). Email exchange with Dmytro produced two architectural directives — PO-only matching rule and a `BGHasInvoice` gate on `IWReady4QB`. Code changes prepared in active workspace, awaiting Dmytro signoff before deploy.

## Crisis state through the day (UTC)

| Time | Source | Event |
|---|---|---|
| 17:01 | Alex Umanets | QB stack crashed mid-day; restarted QB + QRemote + flows. |
| 19:38 | Danlyn | "Is there any update on the payments that were applied to the Website Sales invoices paid via PayPal? It still looks like the payments are applied." |
| 20:05 | Danlyn | "This issue has not been resolved. There is now an additional Authorize.net payment transaction on this account." |
| 20:06 | Danlyn | Forensic spreadsheet `4.22.26.xlsx` attached — annotated 4/22 Auth.Net transactions, one tab per problem PO. Plus: "We are now behind again on applying payments... unable to pay commission reports on time for the last 3 months due to the issues with the QB integration." |
| 20:50 | Danlyn | "I just found another Authorize.net payment applied to a customer account. Again, **not applied to an invoice and on a customer account who pays via check — not Authoriz.net.**" — cascade has spread beyond the Website Sales pool. |
| 20:57 | Danlyn | Confirmed she turned off Pampa-side flows during 5/4 backup; they auto-restarted by morning. Pampa-side flow stop did not stick. |

## PROD diagnosis (Andrew, evening 5/5)

Authenticated to `pampabay.creatio.com` via `/ServiceModel/AuthService.svc/Login` and ran OData queries:

| Query | Finding |
|---|---|
| `IWTransactions ModifiedOn > 2026-05-04T00:00Z` | **43 records**, all with `CreatedOn == ModifiedOn` (not re-modified existing) |
| Latest 10 by `ModifiedOn desc` | All created in a single batch at 2026-05-05 05:00:44–46 UTC (1 AM ET) |
| Sample (TR-02432) full read | `IWReady4QB = true` on creation; `IWQBLastModified = 0001-01-01` (never pushed); `CreatedById = 410006e1…` (Supervisor account) |
| Field probe on Order | `IWReady4QB` does NOT exist on Order — lives on `IWTransactions`. Memory note `feedback_creatio_transaction_order_matching` had this misattributed; corrected. |

Confirms Danlyn's claim: Auth.Net inbound is still creating new IWTransactions on schedule, all auto-flagged Ready4QB=true and queued for next outbound cycle. The cascade isn't "leftover" — it's actively replenishing.

## Email thread with Dmytro (Pampa Bay - Issues Thread)

### 5/5 23:12 UTC — Dmytro pushback

Dmytro replied to Andrew's 21:26 update with three substantive points:

1. **AppliedToTxnRefNumber correction**: "It is read only field! Not sure why you even looking into that direction. Don't trust AI in this — it is bad in all QB related cases. No single correct answer after 10+ requests. I have all these sessions stored…" Field name was wrong on the question Andrew posed; correct path for routing payments is `AppliedToTxnAdd.TxnID` aggregate.
2. **TR-02141 diagnosis**: TR-02141 (Invoice 39316, created 4/23) was originally linked to ORD-18427 (`BGPONumber = 39316`). Modified on 4/28; now linked to **ORD-2120** which has `BGPONumber = 6970` but `BGNumberInvoice = 39316`. Dmytro's read: "instead of the binding Transaction Invoice Number to Order PO Number we have binding Transaction Invoice Number to Order Invoice Number."
3. **Direct accusation of `IWTransactionAutoPairSweepService`**: "That fully AI generated code includes 'canonical rule'. This rule includes comparison with BGNumberInvoice that creates a mess."
4. **Direct question**: "are there new requirements that suggest comparison Transaction Invoice number to both Order PO Number and Order Invoice Number?"

### 5/6 00:27 UTC — Andrew reply (sent)

Five-numbered response addressing each of Dmytro's points:

1. Acknowledged AppliedToTxnRefNumber field-name miss; clarified the underlying question is about `AppliedToTxnAdd.TxnID`.
2. Quoted Dmytro's 4/17 email verbatim — "PO number equals to the Order's Invoice number" — explaining `BGNumberInvoice` came from reading "Order's Invoice number" literally as the `BGNumberInvoice` field.
3. Explained `BGPONumber` and `BGWooCommerceId` were defensive OR-branches added during the 4/17 manual patch of 212 unlinked Transactions (many on Orders not yet invoiced; some WC late-Orders).
4. Confirmed: no new Pampa requirements drove the BGNumberInvoice branch.
5. Offered to run TR-02141's PROD history first to confirm whether the sweep did the 4/28 relink, and committed to holding the halt PATCH until aligned.

### 5/6 00:59 UTC — Dmytro directive

Three numbered points, marking a tone shift from prickly to instructional:

1. **Stay out of QODBC reasoning**: "QB SDK rules are mostly not applicable to what we are doing. They are hidden behind QODBC driver that is very often using completely undocumented SDK features. I had long conversations about 9 years ago with the guy who wrote the driver. Some of that knowledge is lost now even in FLEXquarter. Also, most of QODBC features are hidden from AI, so its recommendations may be very harmful to Customer's data integrity."
2. **Canonical rule**: "Just to confirm. **Invoice Number is the field in the Transaction. PO Number is the field in the Order. No other matching rules are applicable.** We can discuss with Danlyn what kind of report she wants for 'stranded' Transactions that don't have Orders linked."
3. **Two fix paths + new architectural rule**: "In order to fix you have two options: a) throw away this AI generated monster and write 20+ lines of code to match two records; b) ask AI to change the matching rule and regenerate the code. Again, **IWReady4QB in Transaction can be set only after BGHasInvoice in the matching Order is set to true**. Otherwise, we won't have an invoice in QB to apply the payment."

## Code changes (option b — modify and regenerate)

Three files patched in the active workspace at `/mnt/c/Creatio/creatio-dev-agent/packages/IWInterWeavePaymentApp/Schemas/`:

### `IWTransactionAutoPairSweepService.cs`
- `FindMatchingOrder()` — collapsed three OR branches to a single `BGPONumber == numericPrefix` filter. Removed unused `wooId` / `hasWooId` locals.
- Doc-comment header updated to reflect PO-only canonical rule.

### `IWTransactionAutoPairListener.cs`
- Same `FindMatchingOrder` surgery as the sweep.

### `IWTransactionReady4QBListener.cs`
- **Restored to active workspace from `pampa-cleanup-20260427` snapshot** — was missing post-4/27 consolidation. Active workspace + cleanup-20260427 had drifted; this brings the canonical source back into the deployment tree.
- Added `OrderHasInvoice()` helper using `Terrasoft.Core.DB.Select` against `Order.BGHasInvoice`.
- New gate placed in `Evaluate()` between the `IWTROrderId` non-empty check and the `Update` that sets `IWReady4QB = true`. If the linked Order's `BGHasInvoice` is false (or the Order doesn't exist), the listener bails.
- Doc-comment header updated to reflect the three-condition gate.

All three .cs files mirrored to `C:\Users\amago\Downloads\` for attachment to the review email to Dmytro.

## Open items for Wednesday 5/6

1. **Send code-review email to Dmytro** — drafted with diff snippets + three .cs attachments. Acknowledges his "20+ lines" framing and offers full rewrite per option (a) if preferred.
2. **Halt PATCH still pending** — 209 records (166 from 5/1 list + 43 new since 5/4) should have `IWReady4QB = false` set as immediate stop-gap. Holding until Dmytro signs off on the matching/gate changes.
3. **Stranded-Transaction report** — Dmytro suggested discussing with Danlyn what she wants for Transactions where no Order matches the PO Number. Separate scoping conversation.
4. **Amount ±$0.02 disambiguator open question** — strict reading of "no other matching rules are applicable" arguably excludes the Amount check too. Flagged in code-review email; awaiting Dmytro's call.
5. **Edge case in BGHasInvoice gate** — if Order's `BGHasInvoice` flips false→true *after* Transaction is paired, the Transaction-side listener won't refire. Either an Order entity event listener or a periodic sweep is needed. Not yet implemented.
6. **Source-of-truth gap** — the `pampa-cleanup-20260427` tree had `IWTransactionReady4QBListener.cs` but the active workspace did not. Restored tonight, but worth investigating whether anything else from the 4/27 consolidation got lost.

## Memory updates

- `feedback_creatio_transaction_order_matching.md` — replaced with PO-only rule (cites Dmytro 5/6 directive, retains historical context for the OR-rule origin).
- `feedback_creatio_ready4qb_bghasinvoice_gate.md` — new feedback documenting the BGHasInvoice gate as architectural rule.
- `project_pampabay_qb_export_issues.md` — appended 5/5 section, description updated.

## Reference doc updates

- `reference/SWEEP_IWTRANSACTION_AUTO_PAIR_SPEC.md` — §3 "Match rule" updated to PO-only with directive citation.
- `reference/BP_IWTRANSACTION_AUTO_PAIR_SPEC.md` — §4 ESQ block updated to single-filter form.
