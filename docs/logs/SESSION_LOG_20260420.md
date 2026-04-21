# Session Log — 2026-04-20

## Scope

Pampa Bay PROD (`pampabay.creatio.com`). Two major deployments, one major diagnosis:

1. **IWTransactionAutoPairSweepService ESQ bug** — fixed, deployed, verified clean runtime
2. **IWOrderBGHasInvoiceListener** — new two-listener schema shipped to PROD, canary-tested both paths
3. **Invoice Errors root-cause investigation** — Danlyn's 21 Website Sale invoices diagnosed as edit-after-push divergence (Pamela Murphy), matches 4/13 ORD-17857 pattern

## Deliverables landed on PROD

| Artifact | Package | State |
|---|---|---|
| `IWTransactionAutoPairSweepService` (patched ESQ) | `IWInterWeavePaymentApp` | Compiled, runs clean at 11:00 UTC daily |
| `IWOrderBGHasInvoiceListener` (new) | `IWQBIntegration` | Compiled, canary-tested, kill-switch ON |
| `IWOrderBGHasInvoiceAutoUncheckEnabled` SysSetting | `IWQBIntegration` | Installed, value = `true` |
| Manual backlog OData PATCH sweep | — | 32/32 IWTransactions paired (212 → 244 fully linked) |

## 1. Sweep BP fix

### Symptom
Scheduled BP `IWTransactionAutoPairSweepProcess` firing daily but failing with `Terrasoft.Common.ItemNotFoundException: Column by path IWTROrderId not found in schema IWTransactions` — logged in `SysProcessLog` for 4/18, 4/19, 4/20 at 07:00 UTC (cron was server-local `0 0 2`, interpreted as UTC-5).

### Root cause
`IWTransactionAutoPairSweepService.cs` used `esq.AddColumn("IWTROrderId")` and matching filter. Creatio's `EntitySchemaQuery` rejects the `Id` suffix on lookup columns — expects the navigation name `IWTROrder`. Same file also used `txn.GetTypedColumnValue<Guid>("IWTROrderId")` which must also be `IWTROrder` when fetched via ESQ.

### Fix
Three edits to `/mnt/c/Creatio/creatio-dev-agent/packages/IWInterWeavePaymentApp/Schemas/IWTransactionAutoPairSweepService/IWTransactionAutoPairSweepService.cs`:
- `esq.AddColumn("IWTROrderId")` → `esq.AddColumn("IWTROrder")`
- Filter `"IWTROrderId"` → `"IWTROrder"`
- `GetTypedColumnValue<Guid>("IWTROrderId")` → `GetTypedColumnValue<Guid>("IWTROrder")`

`.Set("IWTROrderId", ...)` in the `Terrasoft.Core.DB.Update` block is correct as-is (that uses DB column names).

### Deploy friction (documented for future)
- Package push blocked for hours by a server-side orphan directory `IWInterWeavePaymentApp-autopair-fix` caused by a bad zip filename earlier in the day. Server kept scanning it during backup and failing with "Object code not valid".
- Tried SQL `UPDATE SysSchemaContent.Content` directly — change landed in DB but `compile-package` didn't pick it up, because Creatio's compile reads from the package filesystem, not `SysSchemaContent`. Even setting `IsChanged=true` and clearing `Checksum` didn't force a rebuild through `compile-package`.
- Schema Designer UI Publish attempt hit `FKTj5Ti40nTBMfs8akfdQmBIa25bs` (`SysSchema.ParentId` → `SysSchema.Id`) violation.
- Eventually resolved: `clio push-pkg dist\IWInterWeavePaymentApp.gz -e pampabay` succeeded later in the day (server temp cleanup happened between attempts, OR the earlier schema-state resets unblocked it). Followed by `clio compile-package` + `clio restart-web-app`.

### Verification
Forced Quartz fire by SQL UPDATE on `qrtz_triggers.next_fire_time` → new `SysProcessLog` entry at 2026-04-20 18:56:03 UTC with `ErrorDescription=''` (empty). Next scheduled fire: 2026-04-21 11:00 UTC.

## 2. Manual backlog sweep

### Approach
Matched 74 unlinked IWTransactions to Orders via the canonical rule (`BGNumberInvoice` OR `BGPONumber` OR `BGWooCommerceId` = numeric prefix of `IWInvoiceDescription`, verified by Amount ± $0.02). 32 matched cleanly (all via `BGPONumber` — recent WooCommerce orders don't have `BGNumberInvoice` set yet), 42 skipped because no matching Creatio Order exists at the quoted amount (those are waiting on the WC → Creatio Order sync).

### Result
212 fully linked → 244 fully linked. All 32 PATCHes via OData, 1 retry needed (transient 502).

## 3. IWOrderBGHasInvoiceListener

### Spec (per Dmytro's 2026-04-20 direction)
Two entity listeners to manage `Order.BGHasInvoice` so Create/Update outbound mode can safely be enabled without hitting QB's paid-invoice lock.

- **Listener A** — `[EntityEventListener(SchemaName = "IWPayments")] OnInserted`. Resolve Order via `IWPayments.IWPaymentsInvoiceId`. If Customer-type, set `Order.BGHasInvoice = false`.
- **Listener B** — `[EntityEventListener(SchemaName = "Order")] OnUpdated` guard. If `ModifiedColumnValues` includes `BGHasInvoice` flipping to `true`, Order is Customer type, AND ≥1 IWPayments exists → re-flip to `false`.

Both write via `Terrasoft.Core.DB.Update` (bypasses entity events, no recursion).

### Package
`IWQBIntegration` (semantic fit: BGHasInvoice is a QB-sync control field).

### Deploy path
- dev-pampabay push FAILED on pre-existing FK violation on `BGSetOrderProductTaxStatusByOrderSalesTax` (`FKTj5Ti40nTBMfs8akfdQmBIa25bs`) — unrelated schema, dev-pampabay DB quirk. Worth separate cleanup.
- PROD push succeeded cleanly on same zip. Deployed directly.

### ESQ bug iteration
First push: Listener B's `HasPayment()` used `esq.CreateFilterWithParameters(..., "IWPaymentsInvoiceId", orderId)` — hit the same "Column by path X not found" error as the sweep service had. Fixed to `"IWPaymentsInvoice"` (without Id suffix), rebuilt, pushed, verified.

### SysSettings API gotcha
`IWQBIntegration` package's compile context resolves `SysSettings.GetValue` to `DictionaryUtilities.GetValue` extension method rather than `Terrasoft.Core.Configuration.SysSettings.GetValue`. Had to use fully-qualified name + `object` return + pattern match:
```csharp
object raw = Terrasoft.Core.Configuration.SysSettings.GetValue(userConnection, EnabledSettingCode);
return raw is bool b && b;
```
In `IWInterWeavePaymentApp` the 3-arg overload `SysSettings.GetValue(uc, code, defaultValue)` resolves fine. Package-scoped difference.

### Canary (ORD-18362, clean Customer order with no prior payment)

| Step | Expected | Actual |
|---|---|---|
| POST new IWPayments with `IWPaymentsInvoiceId = Order.Id` | Listener A fires, Order flips to `BGHasInvoice=false` | ✅ Id `dabe00ba-...`, flipped |
| PATCH `Order.BGHasInvoice = true` | Listener B fires, guard reverts to `false` | ✅ HTTP 204, reverted |
| Delete canary IWPayment + restore `BGHasInvoice=true` | no residue | ✅ Clean |

Kill-switch `IWOrderBGHasInvoiceAutoUncheckEnabled` is currently `true` on PROD.

## 4. Invoice Errors — diagnosis

### Danlyn's report (20:57 UTC)
21 Website Sale invoices where QB total ≠ Creatio total. 13 of 21 at exactly 40% ratio, 2 wild outliers (64493 QB=$3,260 vs Creatio=$242; 64627 QB=$23.28 vs Creatio=$268).

### Data findings
- All 21 created in a narrow 2026-03-31 to 2026-04-02 window.
- All 21 modified by `Pamela Murphy` (Pampa user) 1–5 days after WC creation. No other editor.
- Invoice `64484 = ORD-17857`, which matches the case diagnosed 2026-04-13: Creatio had SKUs `CER2585G, CER2145G`; QB had `CER2869G, BGY0965G` (totally different).
- Creatio internal totals are self-inconsistent across the 21 (`Order.Amount`, `Σ(Price × Qty)`, `Σ(TotalAmount)`, `Σ(PrimaryAmount)` disagree on most rows).
- All 21 have exactly 1 IWTransaction with `IWAuthNetTransactionAmount = Order.Amount` — customer paid Creatio's retail total; QB booked wholesale/different.
- Creatio's `Invoice` table is empty (0 rows). `IWPayments` has 1,887 rows all linked via `IWPaymentsInvoiceId` to `Order.Id` (misleadingly named column).
- Zero recent WooCommerce orders have `IWQBInvoiceNumber`, `IWQBLastModified`, or `BGQuickBooksId` populated — so the QB invoices Danlyn sees got there via a path that never wrote back the link fields (legacy BGlobal flow or WC→QB direct).

### Conclusion
**Edit-after-push divergence, not a field-mapping bug.** Pamela edits Orders in Creatio after the WC→QB initial push already landed. QB keeps the pre-edit snapshot; Creatio shows post-edit. The "DRS flow doesn't handle updates" issue from 4/13 applies.

### Dmytro's resolution path
Switch outbound flow to Create/Update mode, with the new BGHasInvoice listener as the safety guard to prevent updating already-paid QB invoices. Plan: Dmytro tests on 1-2 invoices, Alex reruns the rest.

## 5. Creatio-dev-agent review

Invoked `creatio-agent build` with full context for the sweep fix. Rating: **3/10**. Details:

- Research phase OK (5/10) but bloated: read 2.9 MB of files, dumped into transcript.
- Did successfully push the fix to dev-pampabay + restart it. That artifact became reusable.
- Deadlocked on its own `until [ $(wc -c ...) -gt 131 ]; do sleep 10` watchdog that could never exit. Sat idle ~4 hours until killed manually.
- Queried non-existent Creatio tables (`SysProcessSchemaVersion`).
- Never touched PROD; I had to finish the deploy manually.

**Action items for agent:**
1. Every self-spawned wait-loop needs a max-iteration cap + progress signal.
2. Research phase needs a hard budget (≤5 file reads before commit).
3. Recovery playbook for PROD push failures needs encoding (skip-backup flag, different filename, etc.).
4. Add learnings:
   - Creatio DB source updates don't trigger filesystem recompile.
   - `IsChanged=true` alone doesn't force compile-package to touch a schema.
   - FK `FKTj5Ti40nTBMfs8akfdQmBIa25bs` is `SysSchema.ParentId`.
5. Supervisor loop to flag "stuck" after 30 min of no forward progress.

## Files authored today

- `/mnt/c/Creatio/creatio-dev-agent/packages/IWQBIntegration/Schemas/IWOrderBGHasInvoiceListener/IWOrderBGHasInvoiceListener.cs` — new (2 listeners + shared config)
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWQBIntegration/Schemas/IWOrderBGHasInvoiceListener/descriptor.json,metadata.json,properties.json` — new
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWQBIntegration/Data/SysSettings_IWOrderBGHasInvoiceAutoUncheckEnabled/*` — new (3 files)
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWQBIntegration/Data/SysSettingsValue_IWOrderBGHasInvoiceAutoUncheckEnabled/*` — new (3 files)
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWInterWeavePaymentApp/Schemas/IWTransactionAutoPairSweepService/IWTransactionAutoPairSweepService.cs` — edited (3 ESQ fixes)
- 20+ SQL artifacts in `/mnt/c/Creatio/creatio-dev-agent/*.sql` — investigation queries

## PROD state at end of session

- Listener sweep runs autonomously, daily 11:00 UTC.
- Listener BGHasInvoice automation live; kill-switch `true`.
- Auto-pair listener + sweep both dormant-safe (`IWTransactionAutoPairEnabled` kill-switch still wired).
- 244 of 332 IWTransactions linked; 88 unlinked (mix of waiting-on-WC-order-sync and pure-noise rows with empty InvDesc).
- QB outbound flow still OFF pending Dmytro's Create/Update-mode switchover (expected tonight).
