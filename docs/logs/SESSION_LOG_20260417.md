# Session Log — 2026-04-17

## Focus
Pampa Bay PROD — IWTransaction → Order pairing repair + Business Process design for forward-going automation.

## Context entering session
From project memory (end of 4/16 work): QB file remediation complete, 3 Freshdesk tickets filed, all outstanding items with Dmytro. Two live client issues around inbound transaction pairing surfaced: (a) ~126 fully-unlinked IWTransactions with valid InvoiceDescription but empty IWTROrderId, (b) ~109 Order-linked rows missing IWAccountId stamp.

## What changed

### 1. Backlog repair — 215 IWTransactions patched
- Ran `/tmp/patch_txns_v2.py` against `pampabay.creatio.com`
- **Phase 1** — matched 89 unlinked rows via `BGWooCommerceId == numeric(IWInvoiceDescription) AND abs(Order.Amount - Txn.Amount) < 0.02`, stamped both `IWTROrderId` and `IWAccountId`
- **Phase 2** — stamped `IWAccountId` on 123 Order-linked-Account-missing rows using each Order's `AccountId`
- Result: 215 fully linked (was 17), 41 legitimately unlinked (R-suffix refunds, card retries without matching WC order, $0 authOnly records — all expected to stay unlinked)

### 2. Audit of the patched rows
- Ran `/tmp/audit_linked_txns.py` — 200 clean matches, 12 amount-mismatches, 0 wrong-account stamps
- Secondary audit (`/tmp/audit_mismatches.py`) against 4 sampled mismatches found **3 cases of PO-number recycling** where a newer Order matched the transaction's amount exactly:
  - `TR-00088` ($100.00, PO 38901) → corrected from `ORD-5742` to `ORD-17971`
  - `TR-00089` ($100.00, PO 38901) → corrected from `ORD-5742` to `ORD-17971`
  - `TR-00975` ($236.71, PO 39097) → corrected from `ORD-7143` to `ORD-18155`
- Remaining 9 mismatches fit a **card-retry pattern** (same customer, same PO, same amount, multiple attempts) documented in prior 4/10 memory. User directive: leave as-is, likely legitimate split-cart behavior. Partial confirmation from Pampa's 6.625% sales tax (PO 38814's $7.44 gap on $127.50 ≈ 6.2%).

### 3. Memory hardened — canonical match rule
Created `feedback_creatio_transaction_order_matching.md`: the forward-looking rule is `Order.BGNumberInvoice == InvDesc_numeric OR Order.BGPONumber == InvDesc_numeric OR Order.BGWooCommerceId == InvDesc_numeric`, verified by `abs(Order.Amount - Txn.Amount) < 0.02`. **Never match on `BGPONumber` alone** — PO numbers recycle across Orders in Pampa Bay's workflow.

### 4. Business Process spec authored
Wrote `reference/BP_IWTRANSACTION_AUTO_PAIR_SPEC.md`. Key design choices:
- **Package home: `IWInterWeavePaymentApp`** (owns the `IWTransactions` schema — correct co-location per Creatio conventions)
- **Build location:** `C:\Creatio\creatio-dev-agent\packages\IWInterWeavePaymentApp\Schemas\IWTransactionAutoPair\` — leverages the clio MCP workspace with cross-env deploy
- **Shape:** Start Signal (Record added) → single Script Task → Terminate. No gateways, no UserTasks — the match/verify/stamp happens in one transactional C# call
- **Trigger scope:** Record added only (v1). No Modified trigger, no retroactive sweep — avoids churn and self-fire loops
- **Direct DB Update** (not `Entity.Save()`) — bypasses listener cascades and won't re-fire the BP on itself
- **Three-phase rollout:** (A) author in dev-agent workspace via Designer stub + hand-patched `CH1`, (B) validate on dev-pampabay with 3 smoke tests, (C) careful PROD rollout with pre-flight checklist, monitoring window, and 30-second rollback via deactivating the Start Signal

### 5. PROD env registration gap flagged
`pampabay-prod` is **not** in `/home/magown/creatio-hub/clio/appsettings.json` — only `dev-pampabay` is. For Phase C of the BP deploy, either register the PROD env with admin creds OR use Application Hub UI upload with the exported `.gz`. Non-blocking for Phase A/B.

## Current status

| Area | State |
|---|---|
| IWTransactions backlog | ✅ Repaired (215 linked, 41 legitimately unlinked) |
| 3 PO-recycling mislinks | ✅ Corrected |
| 9 card-retry mismatches | ℹ️ Left as-is (per user direction) |
| BP spec (superseded by listener) | ✅ Written and amended with pivot note: `reference/BP_IWTRANSACTION_AUTO_PAIR_SPEC.md` |
| **Pivot: BP → EntityEventListener** | ✅ Decision made 4/17 PM — listener fits dev-agent workspace + gets SysSetting kill switch |
| Listener implementation | ✅ **8 files written, clean `dotnet build` on dev-nf config (net472)** |
| Phase A (author) | ✅ Done |
| Phase B (dev-pampabay push + smoke test) | ✅ **Done — 5/5 cases passed** |
| Phase C (PROD install, disabled default) | ✅ **Installed 2026-04-17 13:42 UTC, disabled-flag smoke test passed** |
| Flip PROD `IWTransactionAutoPairEnabled=true` | ✅ **ENABLED 2026-04-17 18:27:03 UTC, canary test passed** |

## Phase C results (PROD, 2026-04-17)

- **Rollback snapshot:** `C:\Creatio\creatio-dev-agent\rollback\IWInterWeavePaymentApp_PROD_pre-autopair_20260417-173958.zip` (178 KB)
- **Listener schema on PROD:** Id=`f6f8066a-3d08-4772-a1b2-c787eee8a361`, ManagerName=`SourceCodeSchemaManager`
- **SysSetting on PROD:** Id=`43fe4299-...`, Code=`IWTransactionAutoPairEnabled`, default **false**
- **Disabled-flag smoke test:** Insert InvDesc=65851 Amt=$424 (would match ORD-18298) → IWTROrderId stayed empty → deleted → count back to 273 ✅
- **PROD drift finding (pre-existing, NOT caused by push):** Line 34 of install log: `IWTransactions` schema has a pending local PROD modification that blocked the install's overwrite attempt. Our listener is a new separate schema so this didn't affect us, but it's a latent issue that needs resolution before the next schema push to PROD. Someone edited `IWTransactions` directly via Source Code Designer and never committed to a package.
- **Client-side clio exception** (post-install): `CreatioClient.ExecutePostRequest` threw after line 130 "File content descriptors obtained" — this was AFTER the meaningful configuration build + data install completed. Likely a timeout/proxy hiccup on the clio side; no server-side impact.

## PROD live enable + canary (2026-04-17 18:27:03 UTC)

- **Trigger:** Danlyn's 14:14 EDT email explicitly accepting error-tolerance trade-off ("less work to clean up than to manually apply hundreds of payments")
- **Flip:** `SysSettingsValue(d9af4445-97d8-43ce-9b2a-740261ff770a).BooleanValue false → true` via OData PATCH → HTTP 204
- **Canary test on PROD:** Insert `PROD-CANARY-ENABLED-2026-04-17`, InvDesc=65851, Amt=$424.00 → listener stamped `IWTROrderId=2db8fc7a-46e7-4b44-b77c-5f8cd3d59a54 (ORD-18298)` + `IWAccountId=6841b95e-9331-4b22-a659-ea3ff5d4f4df` exactly as designed → deleted → PROD count back to 273 ✅
- **Live state:** Listener now fires on every new Auth.Net inbound IWTransactions row. Next observation point: after the nightly 05:00 UTC Auth.Net sync cycle.

## Dmytro architectural pushback + pivot to sweep service (2026-04-17 late PM)

**Dmytro's critique (condensed):** Real-time listener misses the actual gap — the "late Order" case where Order arrives *after* Transaction. Existing integration handles the Order-exists-at-insert case already. Proposed two solutions, recommended #1: nightly scheduled process scanning unlinked Transactions against current Orders. Recommended over the Order-trigger variant for API-call efficiency.

**Andrew's call:** follow his direction, he owns the flows.

**Built:** `IWTransactionAutoPairSweepService` static C# class in `IWInterWeavePaymentApp` — paginated scan over unlinked `IWTransactions`, same match rule as the listener, same `IWTransactionAutoPairEnabled` SysSetting kill switch. Single entry point: `Execute(UserConnection) → SweepResult`. Built with clean compile on `dev-nf` config.

**Spec doc for Dmytro review:** `reference/SWEEP_IWTRANSACTION_AUTO_PAIR_SPEC.md` (9 sections, 5 open decisions for his sign-off before dev/PROD push).

**Outbound reply draft to Dmytro:** sent — short confirmation we're building #1 + 2 alignment questions (listener disable now? build ownership?). Spec doc to follow by email for his review.

**Listener state unchanged:** still enabled on PROD pending Dmytro's decision. Doing no harm (idempotent, guards prevent double-link) but may be disabled depending on his preference.

## Phase B results (dev-pampabay, 2026-04-17)

| Case | Input | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Insert InvDesc=55804 Amt=261.63, flag OFF | no-op | IWTROrderId empty | ✅ |
| 2 | Insert InvDesc=55804 Amt=261.63, flag ON | stamp ORD-13091 | IWTROrderId=ORD-13091, IWAccountId correct | ✅ |
| 3a | Insert InvDesc=55804 Amt=266.63 (mismatch $5) | no-op | IWTROrderId empty | ✅ |
| 3b | PATCH case 3a's Amount to 261.63 | OnUpdated fires, stamps | IWTROrderId=ORD-13091 | ✅ |
| 4 | Insert InvDesc=9999999 Amt=500 (no such order) | no-op | IWTROrderId empty | ✅ |
| 5 | Insert InvDesc="" Amt=100 | no-op | IWTROrderId empty | ✅ |

All 5 test rows deleted post-test. SysSetting flipped back to false on dev-pampabay to keep it quiet.

**Key confirmation:** Case 3b validates the `OnUpdated` re-try path works end-to-end — an unlinked txn whose InvoiceDescription or Amount gets corrected later will auto-pair without a manual script. This is the behavior we want for human data-correction workflows.
| QB outbound flow turn-on | ⏳ Still with Dmytro (Freshdesk Ticket 1) |
| 5-day Auth.Net bulk load (3/24–3/28) | ⏳ Still with Dmytro |

## Files touched
- `/home/magown/creatio-hub/reference/BP_IWTRANSACTION_AUTO_PAIR_SPEC.md` (new)
- `/home/magown/creatio-hub/CLAUDE.md` (added reference index entry)
- `/home/magown/.claude/projects/-home-magown-creatio-hub/memory/project_pampabay_qb_export_issues.md` (appended 4/17 repair block)
- `/home/magown/.claude/projects/-home-magown-creatio-hub/memory/feedback_creatio_transaction_order_matching.md` (new)
- `/home/magown/.claude/projects/-home-magown-creatio-hub/memory/MEMORY.md` (added feedback pointer)
- `/tmp/patch_txns_v2.py`, `/tmp/audit_linked_txns.py`, `/tmp/audit_mismatches.py` (repair scripts — ephemeral)

## Next session resumes at
Phase A Step 2 — after user confirms the Designer stub is published on dev-pampabay, pull the schema into `C:\Creatio\creatio-dev-agent\packages\IWInterWeavePaymentApp\Schemas\IWTransactionAutoPair\` via `clio restore-from-package`, hand-patch the Script Task's `CH1` with the match logic from §4 of the spec, commit.
