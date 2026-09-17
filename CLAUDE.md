# CLAUDE.md - Creatio Reports Fix

> **Status:** ✅ **Commission Report v3 DEPLOYED** | ✅ **Auth.net Inbound ACTIVE** | ✅ **QB File Repaired 4/14** | ✅ **IWTransactionAutoPair listener LIVE (4/17)** | ✅ **IWTransactionReady4QBListener LIVE (4/22)** | ✅ **IWOrderProductInvoiceLineRateListener LIVE (4/22)** | ✅ **9 stuck IWTransactions PATCHed 4/27** | ✅ **IWInterWeavePaymentApp child override consolidated 4/27** | 🔴 **ROOT CAUSE CONFIRMED 4/28**: Creatio→QB push runs but QB rejects (QODBC 3210) when invoice amount-due < charge amount (Alex flagged TR-02140 02:02 UTC). Same root cause as Danlyn's 4/20 21-invoice list. Affects 32+ records (21 + 9 PATCHed + TR-02141 + TR-02150 + weekend traffic). Halperin TR-02182 corrected — also stuck, not landed. | ⏳ **Dmytro testing Delete/Insert** on 1 paid invoice afternoon 4/28 — Pampa to confirm payment re-application. | ⏳ **Bulk-load list ready** in semicolon format for loader. | ⏳ **Kitchen Clique INV 62784** diagnosed: same-invoice-different-orders (extra IVY2611 in QB, $702). | ⏳ **TR-02141 Sharp Incentives**: Carol Small's $165 confirmed as unapplied credit — awaiting Danlyn decision.
> **2026-09-14 ACTIVE (non-Pampa) - Business Central Integration `IWMSDynamicsBCIntegration` = build 377 on D4 and mkpdev-2153, 2026-09-17 (two companies, outbound routed per connection, lookups resolved inside the flow's company; two-company proof 6/6, suite 9/9) (Astra 355–366 signed entitlement; Claude 367–373: review passes 2+3, practice payment and credit memo posted in BC, second company Tester, Inc. connected on 2153 with token-row and scheduler fixes) (batch A of Andrew's review; triage `BC_CONNECTOR_TRIAGE_2026-09-14_ANDREW_REVIEW.md`) (readability pass + Reconciliation tab + designer gate; D4 identical; InterWeave and JMT on 338)** (`~/creatio-hub/reference/bc-connector/`, README row 52). The exact archive is live on D4, `mkpdev-2153`, `mkpdev-interweave`, and JMT. It carries 15 flows / 243 mappings, 18 rules, 18 Knowledge Base articles, 20 Creatio.ai tools, stable Needs-attention links, posted-document hold guidance, and record guidance across all seven affected forms. 2153 suite 9/9; JMT grammar 19/19; JMT schedules remain off. Current truth and remaining owner gates: `BC_CONNECTOR_BUILD338_V161_FINAL_VERIFICATION_2026-09-08.md`.
>
> **2026-06-02 CURRENT STATUS — Creatio side COMPLETE & double-verified.** Pairing root cause fully fixed: (1) imports bypass entity events so listeners never fire on imports; (2) the BPMN sweep had errored every run since 5/22 (unpublished — "Publish the process before starting it"). Converted the sweep to a code-scheduled **IJobExecutor** (hourly, in `IWInterWeavePaymentApp`; needed a Quartz pkg ref for CS0012); it now pairs+stamps-5+arms via `TryPairById`; pagination bug fixed. Deployed clean (0 CS errors), **runtime-verified the job fired 6/03 00:04 UTC + reschedules hourly** (qrtz WAITING), and **independently re-checked via creatio-dev-agent** (health 🟢 + SQL). Backfilled **278 paired / armed 106→255 / 0 pairable backlog**. No conflicts (writes are IWTransactions-only raw Update, isolated from the order-churn storm). **Outbound stays HARD-OFF** until Dmytro ships Layer-1 (`AppliedToTxnRef` + clear-after-push). **Danlyn escalated 6/02 21:52** (removed bad payments herself; Carlos "finalize or move on"; wants a call). Full: `SESSION_LOG_20260602.md`. Memory: [[feedback_creatio_scheduled_sweep_ijobexecutor]], [[feedback_creatio_import_bypasses_entity_events]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-03 CURRENT STATUS — `BGHasInvoice` writer pinned; human edits re-verified; NO changes shipped (on hold).** PROD: 1,161 txns, **264 armed**, 0 unpaired-with-match, **0 pushed** (outbound hard-off), hourly sweep firing. **`BGHasInvoice=true` = two paths split by the invoice number:** (1) human **"Generate Invoice" button** (`PampaBayVer2/BGCustomerOrder_FormPage.js:251`) sets flag + `BGNumberInvoice` **atomically** → safe; (2) **external middleware writes it numberless** → **521 gap orders** (93% Supervisor-created) = premature-arm risk QODBC auto-applies to oldest-open. Armed cohort **264/264 with a number** → currently clean. 3 streams agree **no in-app server/listener/trigger** sets it true (only the button); our BP "IW Account Check Order For Invoiced" only *reads* `BGHasInvoice`, writes `Account.IWInvoiceCheckbox` — **the 521 are the middleware, not ours**. **Human edits verified genuine** (Maria Victoria 175 + Pamela Murphy 78 armed-cohort edits, 100% inside live browser sessions, 0 OAuth) — **reverses the 5/29 "Maria=service account" call** (high run-counts = re-entrant cascades under her connection). **Fix = Lever C** (gate arming on `BGNumberInvoice` — our ONLY control vs a middleware-set numberless flag; free today; revisits Dmytro's 6/01 boolean-only directive) — **NOT built, on hold**. Dmytro/Alex brief drafted, **not sent**. Full: `SESSION_LOG_20260603.md`. Memory: [[reference_pampabay_staff_actors]], [[feedback_creatio_human_vs_automation_session_overlap]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-05 CURRENT STATUS — QODBC tax-code crisis (3190 + 3140) FULLY FIXED both levels; permanent 15-min two-level sweep LIVE & verified firing.** Alex 6/4–6/5 escalation: blank `SalesTaxCode` rejecting Creatio2QBCustInvoice — 3190 on the order-level "Shipping and Handling" line, 3140 on product lines. Root cause = DataService imports bypass entity events so `IWTaxStatusListener` (A=OrderProduct, B=Order) never fires on imports → `IWTaxStatus` blank on **both** Order header and OrderProduct (Pampa uses the Order AS the invoice). **Fix (PROD, verified):** (1) raw-SQL backfill of all blank Order headers + **117 product lines** (106 Non / 11 Tax) + new imports, derived from parent `BGTaxCheckbox`, no `ModifiedOn` bump → `_setcheck.sql` ALL ZERO (North Woods 70980/71 = ORD-19713/14 Non/Non clean). (2) Extended `IWOrderTaxStatusSweep` (NEW schema, IWQBIntegration) to two phases `SweepOrders`+`SweepProducts`, **15-min** IJobExecutor+AppEventListener gated by `IWTaxStatusListenerEnabled`=true; Quartz `IWOrderTaxStatusSweepGroup` registered + verified firing (prev_fire set, next_fire +15min, single 900000ms trigger). Compile fixes: CS0234 `global::Common.Logging` (both sweep files — the AutoPair one was a latent bomb on PROD blocking Compile All), CS0012 Quartz `<Reference>` added to IWQBIntegration.csproj. MSB3106/CS0618 = pre-existing, not ours. Deploy = clio push-pkg ×3 → Andrew Compile All in UI (green). **Status for Bruce:** orders READY but NOT yet posted (failing orders show no `BGQuickBooksId`; Alex paused the flow 16:06 — un-pause + re-run = last mile). `Creatio2QBCustInvoice` (ours) ≠ `CreatioObj2QBPRN` "Column not found" (Dmytro testing his middleware). Payments outbound stays HARD-OFF pending Dmytro Layer-1; commissions frozen at 5/21, validate after payments post. Full: `SESSION_LOG_20260605.md`. Memory: [[feedback_creatio_import_bypasses_entity_events]], [[feedback_creatio_scheduled_sweep_ijobexecutor]], [[project_pampabay_iwtaxstatuslistener_live]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-09 CURRENT STATUS — IWOrderTaxStatusSweep FIXED + VALIDATED on PROD; QODBC 3190/3140 tax-code root cause permanently resolved at the automation level.** (1) The sweep's Quartz job was always **ALIVE** (qrtz-confirmed via `clio execute-sql-script` — which DOES work on Pampa cloud); the bug was its **ESQ blank-detection matching ZERO rows** (`IWTaxStatus` is non-nullable so `IS NULL`=0; Creatio auto-disables the empty-string `=''` filter). The 6/5 raw-SQL backfill had masked that the sweep never stamped anything. (Overturned an earlier same-day "dead trigger/DoesJobExist" misdiagnosis — corrected by reading qrtz directly.) (2) **The first fix attempt — ESQ `NotEqual('Tax')/('Non')` — ALSO matched 0 rows** (canary stayed blank after compile+restart): ESQ is unreliable for blank detection BOTH ways → `feedback_creatio_esq_empty_string_filter_silently_dropped`. (3) **WORKING fix:** rewrote `SweepOrders`/`SweepProducts` to the lower-level `Terrasoft.Core.DB.Update` (set-based, literal SQL: two Order updates keyed on `BGTaxCheckbox` with `.IsNotEqual(Column.Parameter(...))`; products scoped via `.And("OrderId").In(new Select(...).From("Order").Where("BGTaxCheckbox")...)` which also drops orphans). DB layer emits literal `col <> @p` with none of ESQ's empty-value auto-disable. (4) **Deploy gotchas (both bit me):** CLI compile **WEDGES** on Pampa (`clio compile-package` hung 30+min) → use **Andrew Compile All in the Studio UI**; and **compile THEN restart** (the Quartz scheduler reloads the assembly only on `restart-web-app`; restarting *before* compiling ran old code). Single-schema UI edit, **NOT** `push-pkg` (workspace was stale vs PROD — `Orders_FormPage.js` −388 lines — a package push would have regressed it → `feedback_creatio_pushpkg_regresses_stale_workspace`). (5) **Validated (effect, not just liveness):** SQL-blanked canary ORD-19806 (non-QB) → it flipped `'' → Non` on a **normal 15-min scheduled fire, no restart**; `orders_blank=0`, `orderproducts_blank_with_parent=0`; both qrtz jobs healthy. Bleed had already been stopped earlier via OData PATCH (62 Orders + 10 products). Order import recovered (middleware). Outbound payments stay HARD-OFF pending Dmytro Layer-1; armed 286. `OFOpp2QBInvN` "Column not found: Infinity" (Bruce 6/8) = separate Opportunity flow, likely middleware, not addressed here. Health SQL saved at `C:\Creatio\clio\pampa_health.sql`. Full: `SESSION_LOG_20260609.md`. Memory: [[feedback_creatio_esq_empty_string_filter_silently_dropped]], [[feedback_creatio_pushpkg_regresses_stale_workspace]], [[feedback_creatio_scheduled_sweep_ijobexecutor]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-11 CURRENT STATUS — DEEP AUDIT all fixes PASS (4 agents, ~536K rows) + SELF-HEALING job registration DEPLOYED & ACTIVE both sweeps + DI/AS 3100s = new-product first-use collisions (middleware, not Creatio).** Audit: tax 0 wrong values post-listener eras (45K orders + 490K products, product table 100% all eras); pairing 0 mispairs/ambiguous since 6/01 (6+7 legacy pre-6/01); arming arithmetic exact (322 = 142 compliant + 180 known cohort + 0 violations, cohort frozen, 0 under-armed, 0 pushes); infra clean (155 triggers 0 wedged, 0 IW* process errors 48h, no churn). **Live proofs during audit:** 12:40 import burst (10 blank, 8 QB-bound) self-healed at the 12:49 fire; **TR-03380 full-chain** — order arrived 12:40 (blank tax→Non at 12:49), 13:04 AutoPair fire paired+acct-stamped+armed at first opportunity → one record exercised every fix; **#77 closed** (AutoPair sweep alive; stale-registration disease was tax-sweep-specific). 77 paired-no-IWAccountId = middleware-paired-at-insert (77/77 single-touch) — not ours, low-sev. **Remedy:** both sweeps' OnAppStart now `AppScheduler.RemoveGroupJobs` + re-schedule (replaces DoesJobExist guard that preserved dead registrations; concurrent-node catch) — verified ACTIVE: compile-restart re-minted BOTH registrations at 14:25 (AutoPair 06-02→06-11), firing on cadence. Deploy traps: tax-sweep schema **"modified locally" locked** (6/9 UI hotfix) → push refuses forever, UI-paste only; post-push **CS0103** from stale package-hierarchy cache after SysPackageDependency rewrite → `clear-redis-db` + recompile. **3100s:** DI141-144GRG/AS125SLF = single clean products, catalog since Aug/Sep 2025, FIRST order ever 6/10, each on 8 invoices/run → invoice-flow create-on-miss collides on invoices 2-8 (Creatio2QBItem flow dead since 3/31 + redundant per Dmytro 4/22 — items created inline by Invoice/PO flows; NO product-before-orders sequencing). ~25 first-time products queued → repeats until Dmytro adds mid-batch item-lookup refresh. Asks: Alex flow restart with fresh QST (just before failed run — NOT old, 5/21 replay lesson) + QB Item-list check + re-run 71296-71304; Dmytro 180-disarm go/no-go + item-cache fix. Follow-up email drafted audit-grade. Full: `SESSION_LOG_20260611.md` + `reference/PAMPABAY_TAXSWEEP_INCIDENT_EVIDENCE_2026-06-10.md`. Memory: [[feedback_creatio_scheduled_sweep_ijobexecutor]], [[feedback_creatio_modifiedonutc_silent_noop]], [[feedback_creatio_internal_invisible_across_packages]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-10 CURRENT STATUS — Transaction→QB arming (BGHasInvoice) disarm-bypass FIX DEPLOYED + VERIFIED on PROD; one-time disarm of 180 stale-armed PENDING Dmytro sign-off.** Andrew directive "all records ready for the middleware" scoped to Transactions/Orders/OrderProducts on three fields (PO→pairing, Sales-Tax→`IWTaxStatus`, `BGHasInvoice`→`IWReady4QB`). Read-only readiness audit (clio SQL) found **arming already complete (0 under-armed** — every paired txn whose Order has `BGHasInvoice=true` is armed); **lookups unused by the middleware** (61/128 *ready* records have no `IWAccountId`; Contact/Opportunity NULL on all 896) → no backfill; and **Creatio has NO reliable invoice signal** (`BGQuickBooksLastExported`=0 across all 896, `BGInvoiceNumber` on only 5/128) → `BGHasInvoice` is the sole, uncorroborated gate (trust per Dmytro 6/1). Middleware **requires invoice to pre-exist** (Andrew-confirmed) so "make ready" ≠ "arm more". **Real finding: 180 txns armed against `BGHasInvoice=false`** — validated 4/4 (all settled, Customer-type, with an `IWPayments` record = the auto-uncheck trigger). **Root cause (code):** `IWPaymentsInsertListener`/`IWOrderInvoiceFlagGuardListener` flip `BGHasInvoice→false` via raw `Terrasoft.Core.DB.Update` (bypasses entity events), so the existing two-way disarm companion `IWOrderReady4QBReevalListener` (OnUpdated) never fires → stale-armed. **Fix deployed:** added `IWTransactionReady4QBListener.ReevaluateForOrder(uc, orderId)` after both raw `BGHasInvoice→false` writes in `IWOrderBGHasInvoiceListener.cs` (IWQBIntegration; cross-pkg call OK, no cycle). Deploy: IDE Save hit the recurring PG 23503 SysSchema.ParentId FK (harmless rollback) → `push-pkg`; caught the `Orders_FormPage.js` −388-line workspace-drift trap AGAIN → re-synced workspace ← PROD pull so only the 1 schema shipped; clean config build (no CS errors) → restart-web-app. Verified: `SysSchema.ModifiedOn` 4/20→6/10; re-pull confirms 2 `ReevaluateForOrder` calls in PROD source. Going forward a paid order auto-disarms its txns. **Consolidated 3-fix email (tax + pairing + arming, 4 `.cs` attached) drafted + staged to Dmytro+Alex (Cc Bruce)** asking sign-off to disarm the 180 — staged in `Downloads\`, NOT sent (M365 read-only; Andrew sends from Outlook). **PENDING (no PROD data write):** disarm the 180 (`UPDATE "IWTransactions" SET "IWReady4QB"=false WHERE "IWReady4QB"=true AND "IWTROrderId" IN (SELECT "Id" FROM "Order" WHERE coalesce("BGHasInvoice",false)=false)` → armed 308→128), held for Dmytro sign-off; harmless to defer (outbound hard-off). Full: `SESSION_LOG_20260610.md`. Memory: [[feedback_creatio_raw_update_skips_invariant_listener]], [[feedback_creatio_pushpkg_regresses_stale_workspace]], [[feedback_creatio_ready4qb_bghasinvoice_gate]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-12 CURRENT STATUS — Old-order re-push KILLS QODBC (~50 errors crashes QRemote → NOTHING processes); Dmytro asked US to build the books-closed guard; forensics prove the trigger is CASCADES, not staff edits; build fully specced (task #79), blocked only on direction confirm.** Incident: ORD-12755 (ship 8/29/25, inv 55248) + ORD-8008 (ship 1/22/25, inv 46731) re-entered the QST window 6/11 → closed-books invoice attempts → error waterfall → QRemote death (also retro-explains the 6/11 failed restart test). **Forensics (no manual edits):** ORD-12755 stamped 16:13:22 — same second as NEW sibling ORD-19867 (Style Shack, created 6/10) Maria was actually working; ORD-8008 stamped 31s after Maria touched the Dazzle ACCOUNT (cascade family `IW Order and Payments Sync`/`Update invoice dates`/`IW Account Check Order For Invoiced` firing under her connection; 0 IWPayments, 0 line edits, 4 live browser sessions, 52-order normal day) → **"don't edit old orders" is unenforceable; Danlyn's "she couldn't have manually" was CORRECT**. **Writer model corrected** ([[feedback_pampabay_bghasinvoice_writer_model]]): `BGHasInvoice` = staff Generate-Invoice + Woo import set it, outbound consumes it (trigger rows 9/11/12), inbound is Balance/Payments-only (row 46) and CANNOT undo an uncheck; metric trap — `BGHasInvoice+ModifiedOn-today` counts staff invoicing activity, NOT QB landings. **Scope verified:** 38,177 Customer Orders ship<1/1/2026 (0 non-customer) + 2,090 NULL-ship via `Order."Date"` fallback (all 2,091 have Date; 1 stays eligible) = 40,267 to lock; 6 armed TRs on old orders; **Danlyn confirmed QB closing date = 12/31/2025** (exactly our cutoff). **Build spec (#79):** new schema `IWOrderBooksClosedSweep` (clone tax-sweep self-healing 15-min pattern; set-based raw Update, NO ModifiedOn bump — else 38K re-enter QST window; boundary = GREATEST(Jan 1 current year, optional `IWBooksClosedDate` SysSetting) — **automated, no manual gate** per Andrew directive) + set-based disarm + ship-date condition added to `IWOrderInvoiceFlagGuardListener` (instant re-flip; current IWPayments guard covers only 1,037/38K — IWPayments starts 3/14/26) + `IWBooksClosedGuardEnabled` kill-switch. Options email SENT (Andrew 11:13 ET: option 1 = uncheck guard, option 2 = `IWQBSyncStatus` reason-coded pre-flight field — Ready/Hold-BooksClosed/Hold-LongPO/Hold-NewItem; 21 long-PO + 25 first-time-item QB-bound errors queued; addresses: 188/188 populated in Creatio → "empty addresses" is middleware mapping, not our data). Dmytro: QST already past the 2 poison orders (2-row uncheck moot), notify-Danlyn-first → Bruce notified her 1:47 PM; her QB-side password lock ≠ Creatio-side protection (Bruce corrected). `IWQBSyncReady` (May field): 45,419 non-null, 0 true — never adopted. Open: Dmytro direction confirm (opt 1 vs 1+2), trigger-config compound/string-match question, Delete/Create mode + "Starting date 2026-01-01" questions, Freshdesk ticket INV-349 assigned to Andrew (separate tenant). Full: `reference/PAMPABAY_BOOKS_CLOSED_GUARD_2026-06-12.md`. Memory: [[feedback_pampabay_bghasinvoice_writer_model]], [[reference_pampabay_staff_actors]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-22 CURRENT STATUS — Period-aware matcher + #79 books-closed guard + L4 re-point LIVE on PROD (since 6/18); Danlyn GO-AHEAD received; 5-agent approach-review done; outbound still OFF (Dmytro Layer-1 gate).** **Shipped 6/18 (live + verified):** btrim/L1/L2/L3/strand matcher, `IWOrderBooksClosedSweep` (#79 — cleared 40,251 closed-order `BGHasInvoice` + disarmed 5 in one fire, NO ModifiedOn bump), L4 re-point, Held-For-Review backend (`IWTRApprovalStatusLookup` value + listener stamping). Gates ON: AutoPair/Ready4QB/BooksClosedGuard/HeldForReview=true, `IWBooksClosedDate`=2026-01-01. **Memo SENT to Danlyn 6/22 8:41 AM** (hedged "in a much better place", NOT "resolved"; Bruce's data-governance close folded in). **Danlyn replied 3:14 PM with the GO-AHEAD:** (1) dup-PO → **SKIP/don't-guess** (overrides the L3 amount-tiebreak); (2) **resume 6/23**; (3) **no bulk load**. **5-agent read-only review (verified live):** armed 348 (84 invoice_true / **264 over-armed** BGHasInvoice=false / 0 no-order), held 0, armed frozen 6/15 — outbound off (confirmed: **NO Creatio outbound SysSetting exists**, it's 100% middleware). **264 over-armed = $56,305, 262 ($55,622) on the single "Website Sales" umbrella, BORN-armed without a real invoice, 0 created on/after 6/23** → HIGH misapplication risk on resume (QB oldest-open auto-apply) → **DISARM-NOW recommended** (reversible, snapshot-first). **Committed to Danlyn (build):** at-a-glance count tile + filtered list on her home dashboard (`IWInterWeaveDashboard`); the list must be a **saved folder on the IWTransactions section** (a Freedom UI home dashboard cannot host a record grid → [[feedback_creatio_freedom_ui_dashboard_no_record_grid]]); she CAN see the dashboard but it's buried at pos-26 in "My applications" → confirm her real landing workplace; **re-sync the package from PROD before any push** (local tree stale on live schemas). **L3 change:** replace `FindMatchingOrder` amount-tiebreak (~lines 368-385) with strand-if->1-open (strand path already stamps Held-For-Review; closed-period drop preserved). **Approach: ship-now bucket** (dashboard tile + folder + L3 + 264 disarm — all Creatio-side, no middleware) **vs gated-on-Dmytro** (outbound resume = Layer-1 `AppliedToTxnRef` + Alex turn-on). **6/22 "Pampa is down" = QB-connection drop** (Alex fixed "14 days"), NOT Creatio (probe UP). **CBC-Psychology #80354 RESOLVED** (separate tenant; Alex synced Peekskill/INV-349). Full: `reference/PAMPABAY_APPROACH_REVIEW_2026-06-22.md` + `SESSION_LOG_20260622.md`. Memory: [[feedback_creatio_transaction_order_matching]], [[feedback_qb_push_target_invoice_required]], [[feedback_creatio_freedom_ui_dashboard_no_record_grid]], [[project_pampabay_qb_export_issues]].
>
> **2026-06-24 CORRECTION (PROD census + deployed-package code; read-only) — field-semantics + outbound status fixed.** (1) **Outbound is NOT cleanly off** — middleware `Creatio2QBCustInvoice` RAN 6/23 13:24 and hit **QODBC 3177** (object `46029E-1782246001` = Order `ORD-44147-46029`, `BGHasInvoice=false`); there is no Creatio outbound SysSetting (100% middleware) so Creatio can't disable it. (2) **`IWQBInvoiceNumber` / `IWQBSyncReady` / `BGLastQBExport` are blank on ALL 45,603 orders and untouched by any Creatio code** (middleware-owned) — NOT discriminators. **`BGNumberInvoice` is a creation-time sequence number** (on 43,834 incl. ALL 264 over-armed) — NOT proof an invoice exists. The **sole** invoice signal is `Order.BGHasInvoice` (true on only 2,099). (3) The **arming gate already requires `BGHasInvoice=true`** (`IWTransactionReady4QBListener.cs:85`, sole writer; comment: must NOT require BGNumberInvoice) and **L3 already strands** (`IWTransactionAutoPairListener.cs:368-385`). (4) **264 over-armed are OPEN-period** (BGShipDate≥2026-01-01, 0 closed) legacy/middleware strays the gate never retroactively cleaned → fix = one-time disarm + a recurring reconcile sweep `IWReady4QB=true ⇒ BGHasInvoice=true`. (5) PO hygiene fine: 0 blank POs; only 3/348 armed on a shared PO. Full: `reference/PAMPABAY_3177_VERIFIED_FINDINGS_2026-06-24.md`. Lesson: [[feedback_verify_field_semantics_before_asserting]].
>
> **2026-06-24 PM — RESUME IN MOTION.** Two reversible PROD disarms: **264 over-armed** (`IWReady4QB=false WHERE BGHasInvoice=false`) → armed 348→84; then **124 pre-cutover** (`IWReady4QB=false WHERE IWTRDateReceived < '2026-06-23'`, incl. **84 older invoice-backed** ones a "created today" filter misses) → **armed = 4**. Current armed = the 4 payments received 6/23 (`TR-03497/98/99/03500`, BGHasInvoice=true, $803) — ready for Dmytro to push. **Inbound feed was OFF 6/15→6/24** (Auth.Net→IWTransactions stopped 6/15; WooCommerce→Order kept importing → payment-feed-specific); Dmytro re-ran it today → back-fill stamps `CreatedOn`=today, so a received-date cutover MUST filter `IWTRDateReceived` not `CreatedOn` → [[feedback_creatio_resume_cutover_by_received_date]]. Inbound restart must stay 6/23 (no 6/16–22 replay). Layer-1 (`AppliedToTxnRef`) still Dmytro's gate. Snapshots in `~/.pampa-monitor/`. Full: `SESSION_LOG_20260624.md`.
>
> **Updated:** 2026-06-24 | **Verified findings:** `reference/PAMPABAY_3177_VERIFIED_FINDINGS_2026-06-24.md` | **Latest Log:** `SESSION_LOG_20260624.md` | **Approach Review:** `reference/PAMPABAY_APPROACH_REVIEW_2026-06-22.md` | **Root Cause Ref:** `~/.claude/projects/-home-magown-creatio-hub/memory/reference_pampabay_qb_outbound_amount_rejection.md`

---

## 🤖 AI Quick Start

**For any AI assistant:** This section enables quick context loading.

### Navigation Documents

| Document | Purpose |
|----------|---------|
| `docs/AI_NAVIGATION.md` | **Scenario → Document mapping** (use this first) |
| `docs/DOCUMENT_INDEX.md` | **Complete document listing** with relationships |
| `docs/SHARED_UNDERSTANDING.md` | **Complete system knowledge** in one place |
| `CLAUDE.md` | Current status, active issues, quick deploy |

### Scenario Quick Lookup

| User Request Type | Start With |
|-------------------|------------|
| V6 Commission Process | `docs/investigation/V6_PROCESS_BUILDER_GUIDE.md` |
| IWQBIntegration / QB Package | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` |
| Reports / Excel issues | `docs/reference/MASTER_CATALOG.md` |
| Deployment | This file → Quick Deploy section |
| Investigation | `docs/investigation/COMPREHENSIVE_INVESTIGATION_SUMMARY.md` |
| What's the status? | This file → Issue Tracker |

### AI Instructions

1. **Always load `CLAUDE.md` first** for current context
2. **Use `docs/AI_NAVIGATION.md`** to find documents by scenario
3. **Use `docs/DOCUMENT_INDEX.md`** for complete document listing
4. **Follow established patterns** in naming and structure
5. **Update documentation** when creating new docs
6. **Cross-reference** new docs in related existing docs

### 🔴 DEPLOY NOW: RPT-005 Backend Fix

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Changed Methods:**
- `QueryCustomerDidNotBuyData()` - Rewritten with correct ESQ relationship columns
- `CreateReportExecution()` - New helper for Type A pattern
- `QueryCustomerDidNotBuyDataDirect()` - New fallback method

**Deploy URL:** https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178

### 📢 BGlobal V7 Architecture Reference (2026-01-30)

**New Documentation:** Complete understanding of how BGlobal designed V7 reports:
- `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` - Full architecture reference
- `docs/investigation/INTEXCELREPORT_COMPLETE_ANALYSIS.md` - All 33 report configurations analyzed
- `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` - Original SQL view definition extracted from PampaBay

---

## 🧠 Workflow (READ THIS FIRST)

**Based on Boris Cherny's Claude Code Method** → Full guide: `docs/reference/CLAUDE_CODE_WORKFLOW.md`

### The Three Pillars

| Pillar | What It Means | How We Do It |
|--------|---------------|--------------|
| **1. Plan First** | Use Plan mode for complex changes. Iterate until plan is solid. | `shift+tab` (x2) to enter Plan mode |
| **2. Verify Always** | Give Claude a way to verify its work = 2-3x quality | Run tests, check browser, use CLI |
| **3. Update CLAUDE.md** | When Claude does something wrong, add correction here | Add to Lessons Learned section |

### Session Start Checklist

1. ✅ Read this CLAUDE.md (you're doing it now)
2. ✅ Check latest session log: `docs/logs/SESSION_LOG_20260203.md`
3. ✅ For deep understanding: Read `docs/SHARED_UNDERSTANDING.md`
4. ✅ Review the pre-deployment checklist: `docs/reference/RISK_CHECKLIST.md`
5. ✅ For complex changes: Enter Plan mode first
6. ✅ Before deploying: Verify with tests

### 🎯 Top Active Tasks (2026-04-07)

| Rank | Task | Priority | Status | Next Action |
|------|------|----------|--------|-------------|
| **1** | **Order Export to QB (718 backlog)** | 🔴 CRITICAL | BROKEN since March 1 | Dmytro must fix Creatio→QB flow. Flagged 4/7. |
| **2** | **Bulk Load Second Pass** | 🔴 HIGH | Proposed, not agreed | Dmytro: TimeModified + RefNum >= 7797 for pre-2/18 invoices |
| **3** | **Commission Report Reconciliation** | 🟡 HIGH | First pass data ready | Danlyn to reconcile PROD report against internal numbers |
| **4** | Product Price Gaps CSV to Danlyn | 🟡 MEDIUM | Ready in Downloads | Attach to next Danlyn email |
| **5** | Alitcha QB Linking | 🟢 LOW | Requested | Dmytro to link BGQuickBooksId |

### Previous Tasks (2026-02-11, mostly superseded)

| Rank | Task | Priority | Status | Next Action |
|------|------|----------|--------|-------------|
| **1** | **V6 Combined Commission Process** | 🟡 | Plan Complete | Build in Process Designer → [Builder Guide](docs/investigation/V6_PROCESS_BUILDER_GUIDE.md) |
| **2** | IWQBIntegration PROD Import | 🔴 | Phase 0 ✅ | Export packages for PROD |
| **3** | QB Go-Live Confirmation | 🟡 | Ready | Monitor stability, confirm with Carlos |
| **4** | SYNC-005 Reset | 🟢 | Pending | Wait for go-live, then SQL reset |

### 🟡 V6 Commission Process (2026-02-11)

**Plan:** Combine 3 broken processes into 1 combined `IWOrderandPaymentsSync`
**Builder Guide:** `docs/investigation/V6_PROCESS_BUILDER_GUIDE.md`
**Test Script:** `scripts/diagnostics/test_v6_process.py`
**Column Verification:** `scripts/diagnostics/verify_v6_columns.py`

| What | Details |
|------|---------|
| **Replaces** | V4 Calculator + Fill V2 Report Fields + Order Recalc V2 |
| **Signals** | 8 (IWPayments + Order + OrderProduct add/modify/delete) |
| **Paths** | A: Payment calculation, B1: Order→Pending, B2: OrderProduct→Pending, C: Order deleted |
| **Elements** | 36 total (8 signals, 7 reads, 6 changes, 4 gateways, 4 formulas, 7 terminators) |
| **Build order** | Path B1 first (tests ChangeData), then B2, C, A |

**Key Risk:** ChangeData may write null columns (known Creatio 8.3 bug). Path B1 is the canary test — if it writes null, switch to Script Task fallback.

**Test command:** `source .env && python3 scripts/diagnostics/test_v6_process.py`

### 🔴 Commission Process Bugs (2026-02-05 Audit)

**Audit:** `docs/investigation/COMMISSION_PROCESS_AUDIT_20260205.md`
**Steps:** `v3_restructure_steps_labeled.md` (Steps 11-12)

| # | Bug | Process | Fix | Status |
|---|-----|---------|-----|--------|
| 1 | V4 100x recursion | V4 | Remove "Payment Modified" signal (Step 11) | TODO |
| 2 | Fill V2 ↔ V4 ping-pong | Fill V2 + V4 | Remove Fill V2's Payment Modified signal (Step 12) | TODO |
| 3 | Fill V2 Order signal unfiltered | Fill V2 | Remove StartSignal4 from Fill V2 (Step 12) | TODO |
| 4 | V3 IsActiveVersion=True in package | V3 | Disable V3 before any PROD import | PENDING |
| 5 | **Order Recalc V2 never Saved in Designer** | Order Recalc V2 | Open in Process Designer → **Save** (not Compile All!) | TODO |
| 6 | Recalculation gap | V4 + Order Recalc V2 | Add Script Task to Order Recalc V2 (Option A) | DESIGN COMPLETE |
| 7 | V3 sets status as TEXT not GUID | V3 | Only matters if V3 activated (keep disabled) | N/A |

**Priority fix order:** 5 → 1 → 2+3 → test → 6

### V4 Commission Process Status (DEV)

| Process | Enabled | Actual | Status | Notes |
|---------|---------|--------|--------|-------|
| **V4** (Payment Calculator) | ✅ | ✅ | 🔴 Recursion bug | Remove "Payment Modified" signal |
| **Fill V2** (Report Fields) | ✅ | ✅ | 🔴 Ping-pong + unfiltered | Remove 2 signals |
| **Order Recalc V2** (Order→Pending) | ✅ | ✅ | 🔴 Never Saved in Designer | Save from Process Designer |
| V2 (Current) | ✅ | ❌ | Replaced by V4 | Won't execute |
| V1 (Original) | ✅ | ❌ | Superseded | Won't execute |

**Phase 0 Checklist (DEV Verification): ✅ COMPLETE**
- [x] Verify V2 commission active ✅ **API-VERIFIED 2026-02-05**
- [x] V1 processes not "Actual version" ✅ (V2 is Actual, V1 won't execute)
- [x] V3/V4 not found in DEV ✅ (V4 created during this session)
- [x] **Order Recalc V2 uses filtered trigger** ✅ **BROWSER-VERIFIED 2026-02-05**
  - Signal: "In any of the selected fields" (NOT "In any field")
  - Fields: Amount, Shipping Charge, Sub Total, Tax Amount, Total
- [x] Payment process triggers on IWPayments ✅ **BROWSER-VERIFIED**
- [ ] **Save Order Recalc V2** in Process Designer (NOT just Compile All!)
- [ ] Test commission in DEV (verify single execution) - Manual
- [ ] Export packages for PROD import - Manual

**📋 Key Documents (2026-02-05):**
- ✅ `docs/investigation/COMMISSION_PROCESS_AUDIT_20260205.md` - **4-agent audit results**
- ✅ `v3_restructure_steps_labeled.md` - **Steps 1-12 implementation guide**
- ✅ `docs/investigation/FILTERED_ORDER_TRIGGER_DESIGN.md` - Already implemented as V2
- ✅ `docs/investigation/COMMISSION_CALCULATION_INVESTIGATION.md` - Gap analysis complete

> **Reports work is HANDED OFF** to BGlobal/Rommel. Focus is now 100% on QB Integration.
> **Exception: COMM-001 Commission View Fix** — DEPLOYED v3 2026-04-03. `CommissionBySalesRepVw` updated:
> - Added `PaymentDate` (IWPayments.IWPaymentDue) and `SalesGroup` (BGSalesGroup.BGSalesGroupName) columns
> - Added system columns (Id, CreatedOn, etc.) for OData/ESQ compatibility
> - `CommissionReportService.cs` now filters by `PaymentDate` instead of `InvoiceDate`
> - Dashboard "Export Sales Commissions" button wired through — no JS changes needed
> - Rommel (e6Solutions) notified of ReportTool package changes
> - Data incomplete (27 Feb records) — Alex Umanets assigned to run QBInvoices2CreatioDRS bulk load (2/18 to today, batch 20)
> - Full investigation: `~/creatio-hub/reference/PAMPABAY_EXPORT_INVESTIGATION_2026-04-01.md`

### Verification Commands

```bash
# API test (primary verification)
source .env && python3 scripts/testing/test_report_service.py

# Specific report test
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser flow test
python3 scripts/investigation/review_report_flow.py --env dev
```

### When to Use Plan Mode

- ✅ Any handler change (v19.x, v20.x, etc.)
- ✅ Backend service modifications
- ✅ SQL view changes
- ✅ Multi-file changes
- ❌ Simple doc updates
- ❌ Single-line fixes

---

## Quick Navigation

| Need | Go To |
|------|-------|
| **What's happening now** | [Active Issues](#active-issues) |
| **Deploy something** | [Quick Deploy](#quick-deploy) |
| **Run tests** | [Verification Commands](#verification-commands) |
| **Understand the system** | `docs/reference/` |
| **Review session history** | `docs/logs/` |
| **Find issue-specific docs** | `docs/issues/` |

---

## 🎯 QB Integration Go-Live Status

### Current State: ✅ READY (pending confirmation)

| Component | Status | Notes |
|-----------|--------|-------|
| **QB Web Connector** | ✅ Online | Was offline, now syncing |
| **Order Sync (PROD)** | ✅ Working | 336 orders synced successfully |
| **QB Customer Order Integration** | ✅ Deployed | Running in PROD |
| **Commission Sync Process** | ✅ Phase 1 deployed | `BGBPGetQuickBooksCommissions` |

### Blockers Cleared

| Issue | Status | Resolution |
|-------|--------|------------|
| SYNC-004 | ✅ Resolved | QB Web Connector back online |
| Connection timeouts | ✅ Resolved | Server responding |

### Remaining Items (Non-Blocking)

| Item | Priority | Notes |
|------|----------|-------|
| SYNC-005: Reset 637 false "Processed" | Low | Can reset after go-live |
| SYNC-003: 20K batch processing | Low | DEV environment only |
| Commission automation | Future | With Rommel later |

### Go-Live Checklist

- [ ] Confirm QB Web Connector stable (monitor 24-48 hours)
- [ ] Verify order sync completing without errors
- [ ] Set go-live date with Carlos
- [ ] Document any manual steps needed

---

## 📦 IWQBIntegration Package Import (2026-02-03)

**Status:** 🔴 **BLOCKED** - DEV verification required + Missing PROD dependency

### Current Blockers

| # | Blocker | Action Required | Status |
|---|---------|-----------------|--------|
| ~~1~~ | ~~DEV process configuration unverified~~ | ~~Verify V2 active, V3 disabled~~ | ✅ RESOLVED — API-verified 2026-02-05 |
| ~~2~~ | ~~System settings missing~~ | ~~Create IWEnableCommissionV3=false~~ | ✅ NOT NEEDED — V3 doesn't exist in DEV |
| 3 | **IWInterWeavePaymentApp not in PROD** | Export from DEV, import first |

### Package Status

| Package | DEV | PROD | Status |
|---------|-----|------|--------|
| PampaBay | ✅ | ✅ | OK |
| PampaBayQuickBooks | ✅ | ✅ | OK |
| **IWInterWeavePaymentApp** | ✅ | ❌ | **MISSING - Must import first!** |
| IWQBIntegration | ✅ | ❌ | Target (after dependency) |

### Required Steps (In Order)

**Phase 0: DEV Verification** ← CURRENT (API-VERIFIED ✅)
1. ✅ V2 commission processes are ACTIVE and set as Actual version
2. ✅ V1 processes enabled but NOT Actual version (won't execute)
3. ✅ V3/V4 NOT FOUND in DEV (no action needed)
4. [ ] Test commission calculation in DEV (verify single execution)
5. [ ] Export packages

**Phase 1-7: PROD Import** (after Phase 0)
1. Export IWInterWeavePaymentApp from DEV
2. Import to PROD, compile
3. Import IWQBIntegration to PROD
4. Verify V2 is Actual version in PROD
5. Compile and test

### Quick Summary (API-Verified 2026-02-05)

| Finding | Impact |
|---------|--------|
| NO breaking conflicts with UsrExcelReportService | ✅ Safe |
| **V3/V4 NOT FOUND in DEV** | No action needed for V3/V4 |
| **V2 is Actual version** | ✅ V1 won't execute (correct config) |
| **Order Recalc V2 EXISTS** | `IWRecalculateCommissionOnOrderChangeV2` already deployed! |
| Invoice race condition confirmed | Multiple processes write same fields |
| 31 entities (10 extended + 21 created) | Order is CRITICAL |

### Documents (Start Here)

| Document | Purpose |
|----------|---------|
| **[Master Catalog](docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md)** | Complete index of everything |
| **[Team Instructions](docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md)** | Step-by-step import procedure |
| [Investigation Log](docs/logs/IWQBINTEGRATION_INVESTIGATION_LOG.md) | Full timeline |
| [Conflict Assessment](docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md) | Risk analysis |
| [Deep Dive Analysis](docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md) | Root cause of 26x |
| [Consolidated Findings](docs/investigation/IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md) | 6 agent results |
| [Next Steps](docs/investigation/IWQBINTEGRATION_NEXT_STEPS.md) | Recommendations |

### Key Configuration (Before Import)

```sql
-- Verify Order.SalesTax exists (user's concern)
SELECT column_name FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';
```

### Process UIds (API-Verified 2026-02-05)

| Process | UId | Actual Ver | Executes |
|---------|-----|------------|----------|
| IWCalculateCommissiononPayment (V1) | c2623b8a-338e-4adb-afbe-cb76b68368d9 | ❌ | No |
| **IWCalculateCommissiononPaymentV2** | 8cdd4845-4b27-45cd-9907-e9cc478bc3c5 | ✅ | **Yes** |
| IWRecalculateCommissionOnOrderChange (V1) | 04e376c2-3452-4786-88d9-faf096c98ec6 | ❌ | No |
| **IWRecalculateCommissionOnOrderChangeV2** | 3c425afe-3ee8-4d38-baf2-a30de552bd94 | ✅ | **Yes** |

**Note:** V1 processes being "Enabled" doesn't matter - only Actual version executes.

| Setting | Required Value |
|---------|----------------|
| Commission Version | V2 is Actual ✅ |
| Order Recalc V2 | V2 is Actual ✅ |
| IWEnableCommissionV3 | Not needed (V3 doesn't exist) |
| IWEnableCommissionV4 | Not needed (V4 doesn't exist) |

---

## Active Issues (Reports - HANDED OFF)

> **Note:** Reports work handed to BGlobal/Rommel for v8 rework. Issues below are for reference only.

### 📋 Handed Off to BGlobal

| ID | Issue | Status |
|----|-------|--------|
| RPT-005 | "Customers did not buy" column mismatch | Handed off |
| RPT-006 | "Items by Customer" DESCRIPCION | Handed off |
| HANDLER-002 | "MainDS_Name" resource string | Handed off |
| IW-001 | IW_Commission columns | Handed off |

### 🔴 QB Integration (Our Focus)

| ID | Issue | Action | Doc |
|----|-------|--------|-----|
| **SYNC-005** | 637 orders falsely marked "Processed" | Reset after go-live confirmed | `docs/qb-sync/` |
| **SYNC-003** | QB Customer Order 20K limit (DEV) | Batch processing if needed | `docs/qb-sync/SYNC_003_BATCH_PROCESSING.md` |

### ✅ Recently Resolved

| ID | Issue | Resolution |
|----|-------|------------|
| **COMM-001** | Commission report all $0.00 (BGTotalMaster dead) | `CommissionBySalesRepVw` v3 deployed 2026-04-03: PaymentDate + SalesGroup columns, service filters by PaymentDate. Pending bulk load for full data. |
| **RPT-009** | "Sales By Item By Type Of Customer" VBA infinite loop | VBA anchor variable fix (v2) |
| **RPT-010** | "Rpt Sales By Item" showing wrong columns | Backend routing order fix |
| RPT-008 | "Items by Customer" VBA Type mismatch | BGItemsByCustomerView routing |
| RPT-007 | "Items by Customer" 26x duplicate rows | SQL Employee JOIN fix |
| RPT-006 | "Items by Customer" DESCRIPCION wrong | BGProductDescription added |
| UI-007 | Customer ID sent as "value" string | v54 flat object fix |
| UI-006 | PROD infinite loading (v50) | v51 deployed |
| RPT-004 | "Items by Customer" not generating | PROD WORKING (8,814 rows) |
| SYNC-004 | QB Web Connector offline | Resolved - syncing |

<details>
<summary>All Resolved Issues</summary>

| ID | Issue | Resolution |
|----|-------|------------|
| CSP-001 | Looker Studio iframes blocked | UsrIframe Shadow DOM |
| UI-003 | Customer filter missing | v19.13 (BGCustomer) |
| UI-004 | Sales Groups not filtered | v19.13 forced reload |
| LOOKER-002 | Looker reports missing URL params | v19.1 deployed |
| UI-002 | Non-Commission reports wrong filters | v19.1 deployed |
| HANDLER-001 | Hybrid handler (Looker + Excel) | Deployed |
| DL-001/002/003/004 | Download issues | All fixed |
| RPT-001/002/003 | Report config issues | All fixed |
| EARNERS-001 | Brandwise missing earners | 263 created |
| SYNC-001 | QB sync automation | Phase 1 deployed |

</details>

---

## Quick Deploy

### Backend (PROD)

**File:** `source-code/UsrExcelReportService_Updated.cs`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178

### Frontend (PROD)

**Current:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2

### Test Commands

```bash
# API tests
source .env && python3 scripts/testing/test_report_service.py
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser test
python3 scripts/investigation/review_report_flow.py --env dev
```

---

## Documentation Structure

```
docs/
├── AI_NAVIGATION.md  ← **AI QUICK LOOKUP** (scenario → document mapping)
├── DOCUMENT_INDEX.md ← **COMPLETE INDEX** (all documents with relationships)
├── SHARED_UNDERSTANDING.md ← **COMPREHENSIVE REFERENCE** (system knowledge)
│
├── logs/           # Session logs, action logs, test logs
│   ├── SESSION_LOG_20260201.md  ← LATEST
│   ├── SESSION_HISTORY.md       ← Overview
│   ├── TEST_LOG.md              ← All test results
│   └── IWQBINTEGRATION_INVESTIGATION_LOG.md ← **Package investigation**
│
├── issues/         # Issue-specific investigation & fixes
│   ├── RPT005_DEPLOYMENT_CHECKLIST.md
│   ├── ITEMS_BY_CUSTOMER_*.md
│   ├── UI002_*.md
│   └── FUTURE_ISSUES_TRACKING.md
│
├── investigation/  # Deep technical analysis
│   ├── COMPREHENSIVE_INVESTIGATION_SUMMARY.md ← START HERE
│   ├── BGLOBAL_V7_ARCHITECTURE_COMPLETE.md ← Full V7 reference
│   ├── RPT005_COMPREHENSIVE_REVIEW.md      ← Customers Did Not Buy fix
│   ├── BGLOBAL_V7_EXECUTION_PATTERN.md
│   ├── OPTION_A_*.md
│   ├── IWQBINTEGRATION_MASTER_CATALOG.md   ← **IWQBIntegration index**
│   ├── IWQBINTEGRATION_TEAM_INSTRUCTIONS.md ← **Import procedure**
│   ├── IWQBINTEGRATION_CONFLICT_ASSESSMENT.md
│   ├── IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md
│   ├── IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md
│   ├── IWQBINTEGRATION_NEXT_STEPS.md
│   └── IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md
│
├── reference/      # System knowledge & catalogs
│   ├── MASTER_CATALOG.md        ← All reports/views/configs
│   ├── HANDLER_VERSION_HISTORY.md
│   ├── REPORT_FILTER_REQUIREMENTS.md
│   ├── CLAUDE_REFERENCE.md      ← Technical reference
│   └── CLAUDE_CODE_WORKFLOW.md  ← How to work
│
├── deployment/     # Deployment guides & checklists
│   ├── V19_DEPLOYMENT_GUIDE.md
│   └── REPORT_TESTING_CHECKLIST.md
│
├── communication/  # Emails, meeting notes, summaries
│   ├── EMAIL_*.md
│   └── TEAM_SUMMARY_*.md
│
├── qb-sync/        # QuickBooks sync documentation
│   ├── QB_SYNC_AUTOMATION.md
│   └── SYNC_003_BATCH_PROCESSING.md
│
└── archive/        # Older/completed docs
```

---

## Key Files

| Purpose | File |
|---------|------|
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Frontend handler | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` |
| **VBA Fix (Sales By Item By Type)** | `vba/PMPSalesbySalesRep_FIXED_v2.bas` |
| All handler versions | `docs/reference/HANDLER_VERSION_HISTORY.md` |
| Report/view catalog | `docs/reference/MASTER_CATALOG.md` |
| Filter requirements | `docs/reference/REPORT_FILTER_REQUIREMENTS.md` |

---

## AI Instructions

### Rules

- Credentials in `.env` only (never in logs/docs/commits)
- Log test results to `docs/logs/TEST_LOG.md`
- Update session log daily in `docs/logs/SESSION_LOG_YYYYMMDD.md`
- Hidden iframe is canonical download approach for reports
- Optimize for v8/Freedom UI-first

### Creatio-Specific Rules

- **WCF date format required:** Backend expects `/Date(milliseconds)/` not ISO 8601
- **Customer MUST be LOOKUP:** Never use text input for customer filter
- **One data source per page:** Creatio Freedom UI limitation
- **UsrIframe (not crt.IFrame):** Use for Looker embedding

### Lessons Learned

<details>
<summary>Click to expand lessons learned</summary>

1. **Layered fixes cause new problems:** v20→v21→v22 each introduced new errors. Simpler is better.
2. **IntGenerateExcelReportUserTask EXISTS** (GUID: 05c5265c-3f51-4114-9862-fc434abe1f6d) - BGlobal's original flow.
3. **"Items by Customer" has 0 BGReportExecution records** - NEVER used execution-based pattern (Type A vs Type B).
4. **Parent-driven approach:** Use parent's `LookupAttribute_bsixu8a` dropdown. Parent business rules handle most filter visibility.
5. **Parent lacks Commission filters:** YearMonth and SalesGroup must be inserted by child handler.
6. **WCF date format required:** Backend expects `/Date(milliseconds)/` not ISO 8601.
7. **UsrIframe component (not crt.IFrame):** Use `UsrIframe` from BGlobalLookerStudio package for Looker embedding.
8. **Customer MUST be LOOKUP:** User explicitly rejected text input.
9. **Creatio only supports ONE data source per page:** embeddedModel and modelConfigDiff dataSources may not be officially supported.
10. **ComboBox CANNOT be programmatically populated:** Freedom UI ComboBox requires proper data source binding.
11. **IntName mismatch discovered (2026-01-29):** MASTER_CATALOG has different IntName values than actual database. Always verify via API.
12. **Route by report name FIRST (2026-01-30):** IntEsq rootSchemaName can be wrong (legacy data). Always check report name before entity schema when routing reports.
13. **VBA anchor variable pattern bug (2026-01-30):** BGlobal's nested While loops reset anchor variables inside the loop, causing infinite loops. Fix: move anchor reset BEFORE the While, remove resets inside loop.
14. **Process "Actual version" vs "Enabled" (2026-02-05):** In Creatio, a process can be Enabled but only the one marked as "Actual version" executes. Multiple versions can be Enabled simultaneously - only Actual version matters.
15. **"Save" in Process Designer ≠ "Compile All" (corrected 2026-03-04):** The Business Process Designer does **NOT** have a "Publish" button — only **"Save"**. Clicking **Save** in Process Designer generates C# code, compiles, and **registers start signals**. "Compile All" from Configuration only recompiles existing generated code — does NOT register new signals. "Generate Source Code" from Configuration compiles the process class but may not register signal subscriptions. A process imported via package but never opened and **Saved** in Process Designer may not have its signals registered.
16. **Unfiltered signals are dangerous (2026-02-05):** A signal with `DZ12=[]` (empty NewEntityChangedColumns) fires on ANY field change. Fill V2's Order signal has no filter — fires on every Order modification. Always verify signal column filters via metadata API.
17. **Creatio formula lookup syntax (2026-02-10):** In Process Designer conditional flow formulas, reference lookup values using `[#Lookup.EntityName.DisplayValue.GUID#]` format, NOT `Guid("...")`. Example: `[#Lookup.IW Commission Status.Pending.930bb1c6-ca67-4ac0-8f96-a5ea4018a366#]`. `Guid.Empty` and `||` are both valid.

</details>

---

## Reference Data

### Status IDs (QB Integration Log)

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

### Data Pipeline

```
ORDER → QB SYNC → QB INVOICE → QB PAYMENT → COMMISSION REPORT
         ↑           ↑            ↑              ↑
     SYNC-004    SYNC-005    QB Accounting    Working
```

Most missing commission data is due to unpaid invoices in QuickBooks.

---

## Scripts

| Purpose | Script |
|---------|--------|
| **V6 process test** | `scripts/diagnostics/test_v6_process.py` |
| **V6 column verify** | `scripts/diagnostics/verify_v6_columns.py` |
| API baseline | `scripts/testing/test_report_service.py` |
| Items by Customer | `scripts/testing/test_items_by_customer.py` |
| Dynamic filters | `scripts/testing/test_commission_dynamic_filters.py` |
| Browser flow | `scripts/investigation/review_report_flow.py` |
| IWQBIntegration | `scripts/investigation/check_iwqb_package.py` |
| QB sync filters | `scripts/investigation/check_qb_sync_process.py` |
