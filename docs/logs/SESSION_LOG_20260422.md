# Session Log — 2026-04-22 (early AM, continuation of 2026-04-21)

**Context:** Continuation from `SESSION_LOG_20260421.md` evening reframe. Late-night ultrathink pass validating the Option B (IWInvoiceLineRate) fix design. Picking up tomorrow morning.

---

## What we resolved overnight

### Pivot from Row 15 config change to Option B (derived column)

Previous plan: change middleware Row 15 from empty to `BGCustomerPrice` or `PrimaryPrice`.

**Both would have been wrong:**
- `BGCustomerPrice`, `BGFinalPrice`, `BGBuyerPrice`, `BGAmountWithDiscount` — all 0.0 on every OrderProduct row sampled. Never populated.
- `PrimaryPrice` globally would fix ~15 orders but break 328+ clean Customer orders (where Price = PrimaryPrice and line math currently works) plus all 1,124 Factory orders (where Price is correctly wholesale).

Correct solution: **add a computed column `IWInvoiceLineRate` = GREATEST(Price, PrimaryPrice)**, point Row 15 there. Handles every pattern observed in PROD.

Blueprint: `reference/OPTION_B_IWINVOICELINERATE_BLUEPRINT.md`.

### Verified with PROD (not packages, not theory)

| Check | Result |
|---|---|
| Divergent orders | **22** (Danlyn flagged 14; missed 8: 64482, 64483, 64486, 64488, 64489, 64492, 64621, 64623) |
| WCId range | 38808-38858 (tight, not 38812-38858 as first thought) |
| WC-side creation window | 2026-03-31T09:31 UTC → 2026-04-01T14:01 UTC (~28 hours) |
| Per-line ratio uniformity | **100% at exactly 0.400** — 62/62 lines, zero variance |
| Recurrence outside window | **None** — no other WC orders show the divergence |
| All affected orders are BGOrderType=Customer | ✅ |
| Factory orders (1,124) unaffected | ✅ all p_match, Price=PrimaryPrice |
| Brandwise/MarketTime orders | ✅ 9/10 P=PP, 1/10 P>PP, 0/10 P<PP — GREATEST handles all |
| Auth.Net confirms customers paid retail | ✅ 12 of 22 have matching IWTransactions |
| OrderProduct total row count | **480,508** (backfill scope) |
| Column name `IWInvoiceLineRate` available | ✅ doesn't exist |
| BP interaction safety | ✅ Explore agent confirmed no collision |
| Option B also fixes 64625-29 + 64493 via Delete/Create | ✅ re-push simulation exact |

### Option B coverage

| Category | Count | Fix path |
|---|---|---|
| Divergent orders (data-corrupted Price) | 22 | Option B + Delete/Create re-push |
| Late-batch mystery (stale QB values) | 5 (64625-64629) | Delete/Create re-push (destroys old, recreates correct) |
| Extreme outlier | 1 (64493, QB=$3260.88 → Creatio $242.25) | Delete/Create re-push |
| Manual flag flip needed | 1 (64623 — BGHasInvoice=false) | One-off SQL or UI flip, then re-push |
| Refund reconciliation (intentional) | 1 (64484, TR-00130 $7.44) | Leave alone, documented edge |

**Net: 29 orders fixed automatically, 1 needs one-click manual flag flip first.**

---

## State of work streams going into 4/22 morning

| Stream | Status | Blocker |
|---|---|---|
| Ready4QB checkbox | Ready to build, 3 spec questions sent | Dmytro's answers |
| Option B (IWInvoiceLineRate) | Blueprint complete, code drafted, verifications done | Dmytro's approval |
| BGHasInvoice listener | Deployed 4/20, working | — |
| IWTransactionAutoPairSweep | Deployed 4/20, working | — |
| Payments flow turn-on | Not started | Ready4QB |
| Bulk load (4/18+) | Not started | Payments flow + Danlyn confirmation |
| Creatio2QBItem failing since 3/31 | Dmytro-owned | His schedule |
| Edit-prevention listener (was proposed) | **Dropped** — Danlyn rejected the rule | — |
| Price-anomaly detector (future) | Deferred | Option B gives us IWInvoiceLineRate to build it cheaply later |

---

## Unsent communications

- **Dmytro email with Option B proposal** — drafted but NOT SENT. See `docs-corpus/docs/communication/DMYTRO_EMAIL_DRAFT_OPTION_B_UNSENT.md`. Ready to send after morning review.

---

## Morning pickup checklist

### Priority 1 — check inboxes and context first (before doing anything)
1. Check Danlyn's response on Payments flow test (Dmytro was starting the scheduled flow overnight; she was to confirm AM)
2. Check Dmytro's response on Ready4QB 3 questions (field name, insert+update vs insert-only, backfill yes/no)
3. Check for any unexpected email/slack traffic overnight
4. Re-read `OPTION_B_IWINVOICELINERATE_BLUEPRINT.md` with fresh eyes — catch anything missed

### Priority 2 — send the Option B email to Dmytro
- Pull up `DMYTRO_EMAIL_DRAFT_OPTION_B_UNSENT.md`
- Verify the draft still matches current understanding
- Send

### Priority 3 — while waiting on Dmytro, pre-build the package
- Generate fresh GUID for `IWInvoiceLineRate` column UId
- Update `packages/IWQBIntegration/extracted/Schemas/OrderProduct/metadata.json` with new column block
- Update `packages/IWQBIntegration/extracted/Resources/OrderProduct.Entity/resource.en-US.xml` with caption
- Create new schema dir `packages/IWQBIntegration/extracted/Schemas/IWOrderProductInvoiceLineRateListener/` with descriptor, metadata, properties, and `.cs` listener file
- Build package locally, validate metadata diff
- **Do NOT push to PROD until Dmytro approves Option B**

### Priority 4 — prep for Ready4QB checkbox (second package to ship, independent of Option B)
- Same pattern as BGHasInvoice listener: column + listener in `IWQBIntegration` (or `IWInterWeavePaymentApp` if preferred)
- Code is trivial once Dmytro's questions are answered
- Can ship same-day once unblocked

### Priority 5 — support Danlyn proactively
- Surface the 8 orders she missed: 64482, 64483, 64486, 64488, 64489, 64492, 64621, 64623
- Ask her to re-verify QB totals on 64625-29 (0.46 ratio pattern) and 64493 ($3,260.88 outlier) — these don't fit any line-math pattern; may be her in-progress manual edits or separate QB-side issues
- Confirm bulk load window is 4/18+ per her "manually applied up through 4/17"

---

## Open questions (not blocking but worth resolving)

1. Why is INV 64623 BGHasInvoice=false? No IWPayments, no cancel date, no QB export log, no PO. Probably manual uncheck — ask Danlyn or Pamela if they recall.
2. Why do 64625-29 show 0.46 ratio in QB when current Creatio state is clean (Price=PrimaryPrice)? Three theories: (a) Danlyn partial manual updates, (b) stale from original wholesale push that was corrected in Creatio but not re-synced, (c) something else. Delete/Create re-push resolves regardless of cause.
3. Why did 64493 get $3,260.88 in QB for a $242.25 order? 13.46× ratio is not any known pricing multiplier. Likely QB-side data entry error or duplicate posting. Delete/Create re-push overwrites.
4. What exactly changed on WooCommerce side during 2026-03-31 09:31 → 2026-04-01 14:01? Someone (BGlobal, WC admin, a plugin) briefly activated a wholesale pricing rule. Worth asking BGlobal/Rommel if they know.

---

## Key files (all persist across sessions)

- **Blueprint:** `reference/OPTION_B_IWINVOICELINERATE_BLUEPRINT.md`
- **Email draft (unsent):** `docs-corpus/docs/communication/DMYTRO_EMAIL_DRAFT_OPTION_B_UNSENT.md`
- **Project memory:** `~/.claude/projects/-home-magown-creatio-hub/memory/project_pampabay_qb_export_issues.md`
- **Middleware config memory:** `~/.claude/projects/-home-magown-creatio-hub/memory/reference_interweave_middleware_config.md`
- **Edit-pattern feedback:** `~/.claude/projects/-home-magown-creatio-hub/memory/feedback_pampabay_edit_after_push_refund.md`
- **Yesterday's log:** `docs-corpus/docs/logs/SESSION_LOG_20260421.md`
- **Data pull:** `/tmp/iwtransactions_2026-04-02.csv` (317 Auth.Net txns — may be cleaned up by /tmp rotation; re-pull if needed)

---

## What nothing has yet touched

- **The WooCommerce webhook itself.** We have no code access, no logs. If it regresses, Option B's GREATEST formula protects us, but we haven't diagnosed the source.
- **Middleware platform credentials.** Andrew got them from Alex on 4/21 but hasn't logged in yet. Could inspect Row 15 directly instead of relying on screenshots.
- **BGlobal / Rommel** on the WC-side window question.

---

## Final status

✅ Option B blueprint complete and verified.
✅ Memory updated with all findings.
✅ Unsent email draft preserved for morning send.
⏸ Waiting on Dmytro's approval + Danlyn's payments confirmation before any new deployment.

**Nothing was pushed to PROD overnight. All work is planning + verification only.**

---

## Dmytro's 02:00 UTC follow-up email (received AFTER blueprint was written)

Dmytro sent a pre-emptive pushback at 2026-04-22T02:00:17 UTC on the Invoice Errors thread. Must be addressed before the Option B email goes out — sending Option B cold would re-trigger the same skepticism.

### Exact quotes

> Creatio2QBItem flow needs to be revisited but it is actually just a redundant part of the integration. It can be stopped and nothing will happen because all items are created by the Invoice flow if that flow cannot find the item in QB. PO flow is doing the same. Description is missing probably for Items without proper description.

> Regarding Price column. We use Cost in the Item as Price - as it was requested by Danlyn. This is controlled by the command %PURCHASE_TO_SALES% in the line %58 of the item page. It is also reversing purchase description to sales description (requested by customer as well). We cannot use BG fields for invoices because they never contain any useful information for most of the invoices we created. This entire analysis is very weird. It presumes that all hundreds of invoices we loaded have incorrect data. According to it we had no single invoice created correctly. Really?

> Conclusion. We must not use BG fields for all the invoices because many of them (actually, most of them) will be failing. I'm looking into my logs. In all our previous tests BGCustomrPrice and BGFinalPrice are 0. BGAmountWithDiscount is an Amount, not a Rate and cannot be sent to QB. I see several examples where Price is 16, Quantity is 2 and BGAmountWithDiscount=32. Was that field recommended by AI?

> The only way to fix is to make sure that Orders in question have Price populated not from the Wholesale Price field in the Item, but from MSRP field. Not sure what would be the correct conditions here. Say, if Order came from WooCommerce. Or if MSRP is not empty.

> If no such rule can be applied, we may need two company profiles. One for Orders using Price field and another using some other field. That is more complicated solution because two triggers will be required (one per each profile).

> What to do. I think we need a meeting with Danlyn. She has to provide business rules to use. Based on those we can propose either Creatio automation or Additional integration profile. Charges will apply.

### What he's right about (confirms our analysis)

- **BGCustomerPrice and BGFinalPrice are 0** on every order — we confirmed this independently.
- **BGAmountWithDiscount is line amount, not per-unit rate** — pointing Row 15 at it would have double-counted. Correct warning.
- **Creatio2QBItem redundancy** — closes Danlyn's "no descriptions" concern as a Product data issue, not a flow issue.
- **`%PURCHASE_TO_SALES%`** directive at Item page line 58 is the mechanism sending wholesale cost as Item Sales Price. **This is intentional for Items** — Danlyn explicitly requested it. Does not affect invoice line rate (that's Row 15 on a different page).

### What he's wrong about (scope of the issue)

- **It is NOT "hundreds of invoices" wrong.** Only **22 orders** in WCId 38808-38858 (a 28-hour WC-side window). 62 lines, 100% at exactly 0.400 ratio. Clean, tight, auditable.
- **Most invoices ARE correct today.** 328 of 500 clean Customer orders + 1,124 Factory orders + hundreds of Brandwise orders all work correctly. Row 15 = empty → middleware reads Price → Price = retail for these → QB total = correct.
- **Option B doesn't touch those working orders.** The GREATEST(Price, PrimaryPrice) formula returns Price unchanged when Price ≥ PrimaryPrice (i.e., all working orders). Only returns PrimaryPrice for the 22 where Price < PrimaryPrice.

### His proposed alternative

"Populate Price from MSRP not Wholesale, conditional on order source" — this is the **upstream-fix counterpart to Option B**. Same outcome, different layer:
- **His approach:** fix the process that COPIES Price from Product → OrderProduct so it picks MSRP for WC orders
- **Option B:** leave Price as-is (audit trail preserved) and add a derived column for middleware to read

Both arrive at "middleware reads retail". His preserves middleware behavior but requires finding/changing the order creation logic. Mine adds a new column without touching existing paths.

### Implications for morning work

1. **Option B email as drafted will escalate, not resolve.** Dmytro is already in "your analysis is wrong" mode. Sending a long proposal will trigger more pushback. Need a shorter, more diagnostic message first.
2. **Start with evidence, not proposal.** Lead the morning email with: (a) the specific 22 orders with WCId range, (b) the exact 0.4 ratio on 62 lines, (c) Auth.Net proof customers paid retail, (d) explicit acknowledgement that every OTHER invoice is fine. THEN offer options as a menu.
3. **Include his %PURCHASE_TO_SALES% confirmation.** Show we heard him: Items use wholesale (intentional); Invoices is a separate question with a narrower scope.
4. **Meeting with Danlyn is reasonable.** Offer to set one up, but don't make Option B contingent on it.
5. **Address "Was that field recommended by AI?" directly.** That line is a trust signal — he's wondering if I'm being led astray. Need to own it, walk back BGAmountWithDiscount explicitly, and show the PROD-verified narrow column choice (PrimaryPrice, with GREATEST to keep working orders untouched).
6. **Ready4QB still blocked** — he didn't answer the 3 questions. Surface them again separately; don't bury them in the Option B thread.

### Revised morning email strategy

Split into TWO emails:

**Email 1 — Ready4QB (short, unblocks payments flow):**
- "Three quick answers and I can ship Ready4QB today."
- Repeat the 3 questions (column name, insert+update vs insert-only, backfill y/n, AND-filter confirmation)
- No mention of invoice issue

**Email 2 — Invoice analysis correction + narrowed proposal (longer but structured):**
- "You're right that my earlier framing was too broad. Here's the exact scope."
- Concrete numbers: 22 orders, 38808-38858, 2026-03-31 09:31 → 04-01 14:01 UTC, 0.400 exact
- Evidence: Auth.Net charged retail (12 of 22 verified), Price/PrimaryPrice diverge only in that window, every other WC order is clean
- Walk back: "BGAmountWithDiscount was in an earlier draft. You're correct — it's amount not rate. I narrowed to PrimaryPrice after PROD verification."
- Show his %PURCHASE_TO_SALES% understanding is aligned with ours: Items use wholesale intentionally; Invoice line rate is a separate mapping (Row 15) that defaults to Price
- Propose Option B as a narrow, reversible fix that doesn't change behavior for the 478 working orders
- Alternative mentioned: his upstream fix (change order creation logic to use MSRP for WC). Note it requires finding the logic location and has wider surface area
- Offer Danlyn meeting if he prefers business-rule first
- DO NOT send until morning Andrew reviews

### Morning pickup additions

Priority 1 (before any action):
- Read Dmytro's 02:00 UTC email in full (this log has the key excerpts but the HTML has more context)
- Read the unsent Option B email draft — it needs substantial rework given Dmytro's posture
- Reconcile Option B vs his "fix Price at source" approach

Priority 2:
- Send the Ready4QB-only email (short, unblocks payments)
- Draft the corrected invoice-scope email (don't send until Andrew reviews)

Priority 3:
- Look for the Order creation logic that copies BGWholesalePrice → OrderProduct.Price — this is Dmytro's preferred fix point. If we can find it, we can offer both options. Look in:
  - `PampaBayVer2_latest/Schemas/BGProcess_*` (the 4 BP schemas) — likely contains the Order creation flow
  - `IWQBIntegration/Schemas/IWOrderandPaymentsSync`
  - Any SQL triggers on OrderProduct insert (Explore agent found none in packages, but it's worth a second check across PROD via `pg_trigger`)

### Points to validate with Dmytro in the next exchange

1. Confirm `%PURCHASE_TO_SALES%` applies ONLY to Item sync (Products page, line 58), NOT to Invoice line rate (Row 15 on Invoice page). Dmytro's email conflates them slightly — worth getting explicit.
2. Ask where the OrderProduct.Price population happens — is it WC webhook direct, or a Creatio process? If Creatio, we can modify it (his preferred direction). If WC plugin, we can't.
3. Confirm he's OK with Option B as a "safety net" even if we pursue his upstream fix first — GREATEST is a free insurance policy.
4. Confirm the dual-profile approach is genuinely more work than Option B (it is — two triggers, two configs).
