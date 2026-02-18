# V4 Process Restructuring — Step-by-Step Guide (WITH DESIGNER LABELS)
## Based on V3 Metadata, Implemented as V4 (2026-02-05)

---

## IMPLEMENTATION STATUS

| Step | Description | Status |
|------|-------------|--------|
| 1 | Delete 7 flows | ✅ DONE |
| 2 | Delete 3 orphaned elements | ✅ DONE |
| 3 | Wire "Calculate Sales Amount" → "Has Commission Rate?" | ✅ DONE |
| 4 | Add "Set Error - No Total" | ✅ DONE |
| 5 | Wire "Order Total > 0?" default → Error → Terminate | ✅ DONE |
| 6 | Add "Set Error - No Rate" | ✅ DONE |
| 7 | Wire "Has Commission Rate?" default → Error → Terminate | ✅ DONE |
| 8 | Modify "Check Commission Status" condition | ✅ DONE |
| 9 | Add CommRate + SalesRep to "Update Payment 'Done'" | ⏭️ SKIPPED |
| 10 | Add CommRate + SalesRep to "Update Payment 'Returned'" | ⏭️ SKIPPED |
| **11** | **Remove "Payment Modified" signal from V4** | 🔴 TODO |
| **12** | **Remove StartSignal4 from Fill V2** | 🔴 TODO |

**Process Version:** Implemented as **V4** (new version created from V3)
**⚠️ RECURSION BUG FOUND** — V4 triggers itself 100x via "Payment Modified" signal. Steps 11-12 fix this.

### Why Steps 9-10 Were Skipped

| Column | Decision | Rationale |
|--------|----------|-----------|
| **IWBGSalesRep** | **Not needed in V4** | Fill V2 already populates this from BGCommissionEarner → BGSalesRep |
| **IWCommissionRate** | **Deferred** | No process currently writes this. Gap exists but no report or page currently reads IWCommissionRate from the payment record. Can be added later if needed. |

---

## COMPLETE ELEMENT LABEL REFERENCE

Use this table to find elements in the Creatio Process Designer:

| # | Internal Name | Designer Label (what you see) | UId |
|---|---|---|---|
| 1 | StartSignal2 | **"Payment Added"** | `11f8fdef` |
| 2 | StartSignal1 | **"Payment Modified"** | `d8adeedf` |
| 3 | StartSignal3 | **"Payment Deleted"** | `5e2f23f8` |
| 4 | ReadDataUserTask1 | **"Read Payments Record"** | `e14048b0` |
| 5 | ReadDataUserTask2 | **"Read Order Record"** | `6ad6e5ff` |
| 6 | ReadDataUserTask4 | **"Read Commission Rate"** | `0f3eb9a6` |
| 7 | ExclusiveGateway3 | **"Order Total > 0?"** | `0017199f` |
| 8 | FormulaTask1 | **"Calculate Sales Amount"** | `e739b215` |
| 9 | FormulaTask2 | **"Set Sales Amount"** | `b5908e55` |
| 10 | ExclusiveGateway2 | **"Payment Return?"** | `b089222e` |
| 11 | ChangeDataUserTask2 | **"Payment is Returned"** | `52baca83` |
| 12 | ExclusiveGateway1 | **"Does Order Commission Earner have Commission Rate?"** | `a0e575c7` |
| 13 | FormulaTask3 | **"Calculate Commission Amount"** | `83f29aeb` |
| 14 | ExclusiveGateway4 | **"Check Commission Status"** | `4150f8b0` |
| 15 | ChangeDataUserTask1 | **"Update Payment "Done""** | `b7dc7a54` |
| 16 | ChangeDataUserTask3 | **"Update Payment "Returned""** | `d4cd2bf8` |
| 17 | TerminateEvent1 | **Terminate** (red circle) | `67461fd9` |

## COMPLETE FLOW LABEL REFERENCE

| # | Internal Name | Designer Label | From → To |
|---|---|---|---|
| 1 | SequenceFlow2 | *(unlabeled)* | "Payment Added" → "Read Payments Record" |
| 2 | SequenceFlow7 | *(unlabeled)* | "Payment Modified" → "Read Payments Record" |
| 3 | SequenceFlow12 | *(unlabeled)* | "Payment Deleted" → "Read Payments Record" |
| 4 | SequenceFlow10 | *(unlabeled)* | "Read Payments Record" → "Read Order Record" |
| 5 | SequenceFlow13 | *(unlabeled)* | "Read Order Record" → "Read Commission Rate" |
| 6 | SequenceFlow3 | *(unlabeled)* | "Read Commission Rate" → "Order Total > 0?" |
| 7 | ConditionalFlow2 | **"Has Total"** | "Order Total > 0?" → "Calculate Sales Amount" |
| 8 | DefaultFlow3 | **"Has no Total or 0"** | "Order Total > 0?" → "Set Sales Amount" |
| 9 | SequenceFlow8 | *(unlabeled)* | "Calculate Sales Amount" → "Payment Return?" |
| 10 | SequenceFlow16 | *(unlabeled)* | "Set Sales Amount" → "Payment Return?" |
| 11 | ConditionalFlow3 | **"SalesAmount < 0"** | "Payment Return?" → "Payment is Returned" |
| 12 | DefaultFlow2 | **"Not Returned"** | "Payment Return?" → "Does Order Commission Earner have Commission Rate?" |
| 13 | SequenceFlow9 | *(unlabeled)* | "Payment is Returned" → "Does Order Commission Earner have Commission Rate?" |
| 14 | ConditionalFlow1 | **"Has Commission Rate"** | "Does Order Commission Earner have Commission Rate?" → "Calculate Commission Amount" |
| 15 | DefaultFlow1 | **"No Commission Rate"** | "Does Order Commission Earner have Commission Rate?" → "Check Commission Status" |
| 16 | SequenceFlow11 | *(unlabeled)* | "Calculate Commission Amount" → "Check Commission Status" |
| 17 | ConditionalFlow4 | **"Status = "Returned""** | "Check Commission Status" → "Update Payment "Returned"" |
| 18 | DefaultFlow4 | **"Status ≠ "Returned""** | "Check Commission Status" → "Update Payment "Done"" |
| 19 | SequenceFlow1 | *(unlabeled)* | "Update Payment "Returned"" → Terminate |
| 20 | SequenceFlow15 | *(unlabeled)* | "Update Payment "Done"" → Terminate |

---

## CORRECTED FINDINGS (vs previous audit)

| Item | Previous Audit Said | Metadata Shows | Impact |
|------|---------------------|----------------|--------|
| IWIsReturn on "Update Payment "Done"" | ❌ NOT SET | ✅ Already set (False) | No edit needed |
| IWIsReturn on "Payment is Returned"/"Update Payment "Returned"" | ❌ NOT SET | ✅ Already set (True on both) | No edit needed |
| ~~ChangeDataUserTask4~~ | Exists (sets UnappliedAmt) | Does NOT exist in V3 | N/A |
| "Read Commission Rate" order | After "Does Order Commission Earner have Commission Rate?" | BEFORE "Order Total > 0?" | Changes flow restructuring |
| "Order Total > 0?" default path | Terminates | Goes to "Set Sales Amount" (continues) | Must add Error element |
| "Does Order Commission Earner have Commission Rate?" default path | Terminates | Goes to "Check Commission Status" (continues) | Must add Error element |
| "Check Commission Status" | Doesn't exist / unknown | Checks ORIGINAL status for Done vs Returned | Must change condition |

---

## CURRENT FLOW (Before Changes — V3)

```
"Payment Added"     ─┐
"Payment Modified"   ─┤→ "Read Payments    → "Read Order    → "Read Commission
"Payment Deleted"    ─┘    Record"              Record"           Rate"
                                                                    │
                                                                    ↓
                                                        "Order Total > 0?"
                                                        ┌──────┴──────┐
                                               "Has Total"      "Has no Total or 0"
                                                   ↓                    ↓
                                          "Calculate Sales       "Set Sales
                                            Amount"               Amount"
                                                   ↓                    ↓
                                                   └─────┬─────────────┘
                                                         ↓
                                                 "Payment Return?"
                                                 ┌──────┴──────┐
                                          "SalesAmount < 0"   "Not Returned"
                                                 ↓                   ↓
                                          "Payment is              │
                                           Returned"              │
                                                 ↓                   ↓
                                                 └─────┬─────────────┘
                                                       ↓
                                    "Does Order Commission Earner
                                     have Commission Rate?"
                                       ┌──────┴──────┐
                                "Has Commission    "No Commission
                                  Rate"              Rate"
                                       ↓                   ↓
                                "Calculate                 │
                                 Commission               │
                                 Amount"                  │
                                       ↓                   ↓
                                       └─────┬─────────────┘
                                             ↓
                                    "Check Commission Status"
                                     ┌──────┴──────┐
                              "Status =           "Status ≠
                              'Returned'"         'Returned'"
                                     ↓                   ↓
                              "Update Payment      "Update Payment
                               'Returned'"          'Done'"
                                     ↓                   ↓
                                     └─────┬─────────────┘
                                           ↓
                                       Terminate
```

### 3 BUGS IN CURRENT FLOW

**Bug 1 — IWIsReturn Overwrite:**
"Payment is Returned" (mid-flow) sets IWIsReturn = True.
But BOTH paths converge into "Does Order Commission Earner have Commission Rate?", and eventually reach "Check Commission Status". The **"Status ≠ 'Returned'"** default path always goes to "Update Payment 'Done'", which sets IWIsReturn = **False** — overwriting the True that was just set.

**Bug 2 — Stale Status Perpetuation:**
"Check Commission Status" checks the ORIGINAL IWCommissionStatus value read from the database by "Read Payments Record" (not anything calculated). So if a payment was previously "Returned" but the order total changed, the gateway still routes to "Update Payment 'Returned'" based on the old status — perpetuating stale data.

**Bug 3 — Silent Continuation on Missing Data:**
- "Order Total > 0?" default path ("Has no Total or 0") goes to "Set Sales Amount" which just stores the raw amount — then continues through the full flow and writes "Done" status. Should terminate with Error.
- "Does Order Commission Earner have Commission Rate?" default path ("No Commission Rate") goes directly to "Check Commission Status" — skipping commission calculation but still writing "Done" or "Returned" status. Should terminate with Error.

---

## V4 FLOW (After Steps 1-8, BEFORE recursion fix)

```
"Payment Added"     ─┐
"Payment Modified"   ─┤→ "Read Payments    → "Read Order    → "Read Commission
"Payment Deleted"    ─┘    Record"              Record"           Rate"
                                                                    │
                                                                    ↓
                                                        "Order Total > 0?"
                                                        ┌──────┴──────┐
                                                 "Has Total"       Default
                                                   ↓            (No Total)
                                          "Calculate Sales         ↓
                                            Amount"          "Set Error -
                                                   ↓           No Total"
                                                   │         [Status=Error,
                                                   │          Calc=False]
                                                   │               ↓
                                                   │           Terminate
                                                   ↓
                                    "Does Order Commission Earner
                                     have Commission Rate?"
                                       ┌──────┴──────┐
                                "Has Commission       Default
                                  Rate"              (No Rate)
                                       ↓                   ↓
                                "Calculate           "Set Error -
                                 Commission           No Rate"
                                 Amount"             [Status=Error,
                                       ↓              Calc=False]
                                       │                   ↓
                                       │              Terminate
                                       ↓
                              "Check Commission Status"
                                 ┌──────┴──────┐
                          Condition            Default
                          (SalesAmt < 0)       (Not Return)
                                 ↓                   ↓
                          "Update Payment      "Update Payment
                           'Returned'"          'Done'"
                          [EXISTING 6 cols]    [EXISTING 6 cols]
                                 ↓                   ↓
                                 └─────┬─────────────┘
                                       ↓
                                   Terminate
```

**What V4 changed (Steps 1-8):**
1. **DELETED:** "Set Sales Amount", "Payment Return?", "Payment is Returned" (and all their flows)
2. **ADDED:** Two new "Set Error" elements with terminate paths
3. **REWIRED:** "Calculate Sales Amount" now goes directly to "Does Order Commission Earner have Commission Rate?"
4. **MODIFIED:** "Check Commission Status" condition changed from status lookup to calculated SalesAmount < 0

**What V4 did NOT change (Steps 9-10 skipped):**
- "Update Payment 'Done'" — still has original 6 columns (no CommRate/SalesRep added)
- "Update Payment 'Returned'" — still has original 6 columns (no CommRate/SalesRep added)
- **IWBGSalesRep** — covered by Fill V2 (no gap)
- **IWCommissionRate** — not written by any process (gap exists, but no current consumer)

---

## V4 TARGET FLOW (After Steps 11-12 — recursion fix)

```
"Payment Added"     ─┐
                      ├→ "Read Payments    → "Read Order    → "Read Commission
"Payment Deleted"    ─┘    Record"              Record"           Rate"
                                                                   │
                                                                   ↓
                                                       "Order Total > 0?"
                                                       ┌──────┴──────┐
                                                "Has Total"       Default
                                                  ↓            (No Total)
                                         "Calculate Sales         ↓
                                           Amount"          "Set Error -
                                                  ↓           No Total"
                                                  │         [Status=Error,
                                                  │          Calc=False]
                                                  │               ↓
                                                  │           Terminate
                                                  ↓
                                   "Does Order Commission Earner
                                    have Commission Rate?"
                                      ┌──────┴──────┐
                               "Has Commission       Default
                                 Rate"              (No Rate)
                                      ↓                   ↓
                               "Calculate           "Set Error -
                                Commission           No Rate"
                                Amount"             [Status=Error,
                                      ↓              Calc=False]
                                      │                   ↓
                                      │              Terminate
                                      ↓
                             "Check Commission Status"
                                ┌──────┴──────┐
                         Condition            Default
                         (SalesAmt < 0)       (Not Return)
                                ↓                   ↓
                         "Update Payment      "Update Payment
                          'Returned'"          'Done'"
                         [EXISTING 6 cols]    [EXISTING 6 cols]
                                ↓                   ↓
                                └─────┬─────────────┘
                                      ↓
                                  Terminate
```

**KEY CHANGE:** "Payment Modified" signal is GONE. Only 2 triggers remain: Added + Deleted.
No more self-recursion. No more V4 ↔ Fill V2 ping-pong.

---

## 10 STEPS IN PROCESS DESIGNER

### STEP 1: Delete flows connected to "Payment Return?" and "Payment is Returned" ✅ DONE

**Delete these 7 flow arrows (click each → Delete):**

| # | Flow Label | From → To | Why |
|---|---|---|---|
| 1 | **"Has no Total or 0"** | "Order Total > 0?" → "Set Sales Amount" | Replacing with Error path |
| 2 | *(unlabeled)* | "Set Sales Amount" → "Payment Return?" | Removing FormulaTask2 |
| 3 | *(unlabeled)* | "Calculate Sales Amount" → "Payment Return?" | Rewiring to skip "Payment Return?" |
| 4 | **"SalesAmount < 0"** | "Payment Return?" → "Payment is Returned" | Removing entire mid-flow check |
| 5 | **"Not Returned"** | "Payment Return?" → "Does Order Commission Earner have Commission Rate?" | Rewiring directly |
| 6 | *(unlabeled)* | "Payment is Returned" → "Does Order Commission Earner have Commission Rate?" | Removing mid-flow element |
| 7 | **"No Commission Rate"** | "Does Order Commission Earner have Commission Rate?" → "Check Commission Status" | Replacing with Error path |

**In Process Designer:** Click each flow arrow → Delete. Do ALL of these before adding new flows.

---

### STEP 2: Delete orphaned elements ✅ DONE

**Delete these 3 elements (click each → Delete):**

| # | Designer Label | Why |
|---|---|---|
| 1 | **"Set Sales Amount"** | The "no total" raw-amount formula — no longer needed |
| 2 | **"Payment Return?"** | The mid-flow return check gateway — replaced by "Check Commission Status" |
| 3 | **"Payment is Returned"** | The mid-flow IWIsReturn=True setter — no longer needed |

**In Process Designer:** Click each element → Delete.

---

### STEP 3: Wire "Calculate Sales Amount" → "Does Order Commission Earner have Commission Rate?" ✅ DONE

**New flow:** Draw arrow from **"Calculate Sales Amount"** output → **"Does Order Commission Earner have Commission Rate?"** input

**Type:** Regular Sequence Flow (no condition, no label needed)

**In Process Designer:** Drag connector from "Calculate Sales Amount" output → "Does Order Commission Earner have Commission Rate?" input.

**Why:** Previously, "Calculate Sales Amount" went to "Payment Return?" which we deleted. Now it goes directly to the commission rate check, skipping the deleted mid-flow return check entirely.

---

### STEP 4: Add NEW element — "Set Error - No Total" ✅ DONE

**New element:** Modify Data (ChangeData type)
**Position:** Where "Set Sales Amount" used to be, or near "Order Total > 0?"

**Configuration:**

| Setting | Value |
|---------|-------|
| **Name/Caption** | Set Error - No Total |
| **Entity** | IWPayments |
| **Filter** | Id = `[#Read Payments Record.First item.Id#]` |

**Columns to set:**

| Column | Value |
|--------|-------|
| IWCommissionStatus | **Error** (`26c1b9de-...`) — Lookup GUID |
| IWCommissionCalculated | **False** |

---

### STEP 5: Wire "Order Total > 0?" default → "Set Error - No Total" → Terminate ✅ DONE

**New flows:**

| # | From → To | Type |
|---|---|---|
| 1 | **"Order Total > 0?"** → **"Set Error - No Total"** | **Set as Default flow** on the gateway |
| 2 | **"Set Error - No Total"** → **Terminate** (red circle) | Regular Sequence Flow |

**In Process Designer:**
- Click "Order Total > 0?" gateway
- The existing conditional flow **"Has Total"** (→ "Calculate Sales Amount") stays unchanged
- Set the new flow to "Set Error - No Total" as the **Default flow**

**Why:** Previously, the default path went to "Set Sales Amount" which stored a raw amount and continued — allowing records with no order total to reach "Done" status. Now they get "Error" and terminate.

---

### STEP 6: Add NEW element — "Set Error - No Rate" ✅ DONE

**New element:** Modify Data (ChangeData type)
**Position:** Between "Does Order Commission Earner have Commission Rate?" and the Terminate area

**Configuration:**

| Setting | Value |
|---------|-------|
| **Name/Caption** | Set Error - No Rate |
| **Entity** | IWPayments |
| **Filter** | Id = `[#Read Payments Record.First item.Id#]` |

**Columns to set:**

| Column | Value |
|--------|-------|
| IWCommissionStatus | **Error** (`26c1b9de-...`) — Lookup GUID |
| IWCommissionCalculated | **False** |

---

### STEP 7: Wire "Does Order Commission Earner have Commission Rate?" default → "Set Error - No Rate" → Terminate ✅ DONE

**New flows:**

| # | From → To | Type |
|---|---|---|
| 1 | **"Does Order Commission Earner have Commission Rate?"** → **"Set Error - No Rate"** | **Set as Default flow** on the gateway |
| 2 | **"Set Error - No Rate"** → **Terminate** (red circle) | Regular Sequence Flow |

**In Process Designer:**
- Click "Does Order Commission Earner have Commission Rate?" gateway
- The existing conditional flow **"Has Commission Rate"** (→ "Calculate Commission Amount") stays unchanged
- Set the new flow to "Set Error - No Rate" as the **Default flow**

**Why:** Previously, the default path ("No Commission Rate") went to "Check Commission Status" — skipping commission calculation but still writing "Done" or "Returned". Now it gets "Error" and terminates.

---

### STEP 8: Modify "Check Commission Status" gateway condition ✅ DONE

**Current condition on the conditional flow (labeled "Status = 'Returned'"):**
```
ReadPayments.IWCommissionStatus == Returned (ee14b2ce)
```
**This checks the ORIGINAL status from the database — causes Bug 1 and Bug 2!**

**Change to:**
```
[#Calculated Sales Amount#] < 0
```
Which is the process parameter `CalculatedSalesAmount` (UId `eab9b2d5-4600-4a94-840d-4243c218cd28`)

**In Process Designer:**
1. Click the conditional flow arrow from **"Check Commission Status"** → **"Update Payment 'Returned'"**
   (This is the flow currently labeled **"Status = 'Returned'"**)
2. Edit condition formula
3. Change from "Read Payments Record.IWCommissionStatus == Returned"
   to: **"Calculated Sales Amount < 0"**
4. This is the **process parameter** `CalculatedSalesAmount`, NOT a read-from-entity value
5. Optionally rename the flow label to **"SalesAmount < 0"** for clarity

**Why:** The calculated sales amount is freshly computed by "Calculate Sales Amount" (FormulaTask1). Negative values indicate a payment return. This is reliable because:
- It uses the CALCULATED value, not stale database data
- It runs AFTER the amount is computed, so the decision is based on current data
- It eliminates the mid-flow "Payment Return?" check and its overwrite bug

---

### STEP 9: Add 2 columns to "Update Payment 'Done'" ⏭️ SKIPPED

> **Decision:** These columns were not added to V4.
> - **IWBGSalesRep** — Already populated by Fill V2 process (no gap)
> - **IWCommissionRate** — No process writes this, but no report/page currently reads it either (deferred)

<details>
<summary>Original instructions (for future reference if IWCommissionRate is needed)</summary>

**Open "Update Payment 'Done'"** (the Modify Data element that writes status = Done)

**ADD 2 new columns to the existing 6 (don't change the existing ones):**

| # | Column | Value | Expression |
|---|--------|-------|------------|
| 7 | **IWCommissionRate** | From Commission Earner | `[#Read Commission Rate.First item.Commission Rate#]` |
| 8 | **IWBGSalesRep** | From Commission Earner | `[#Read Commission Rate.First item.Sales Rep#]` |

</details>

**Current 6 columns on "Update Payment 'Done'" (unchanged):**

| # | Column | Current Value |
|---|--------|---------------|
| 1 | IWCommissionAmount | `[#Commission Amount#]` (process parameter) |
| 2 | IWCommissionCalculated | True |
| 3 | IWSalesAmount | `[#Calculated Sales Amount#]` (process parameter) |
| 4 | IWCommissionStatus | **Done** (GUID `deb80242-...`) |
| 5 | IWOwner | `[#Read Order Record.First item.Owner#]` |
| 6 | IWIsReturn | **False** |

---

### STEP 10: Add 2 columns to "Update Payment 'Returned'" ⏭️ SKIPPED

> **Decision:** Same as Step 9 — columns not added to V4.
> - **IWBGSalesRep** — Covered by Fill V2
> - **IWCommissionRate** — Deferred (no current consumer)

<details>
<summary>Original instructions (for future reference if IWCommissionRate is needed)</summary>

**Open "Update Payment 'Returned'"** (the Modify Data element that writes status = Returned)

**ADD 2 new columns to the existing 6 (don't change the existing ones):**

| # | Column | Value | Expression |
|---|--------|-------|------------|
| 7 | **IWCommissionRate** | From Commission Earner | `[#Read Commission Rate.First item.Commission Rate#]` |
| 8 | **IWBGSalesRep** | From Commission Earner | `[#Read Commission Rate.First item.Sales Rep#]` |

</details>

**Current 6 columns on "Update Payment 'Returned'" (unchanged):**

| # | Column | Current Value |
|---|--------|---------------|
| 1 | IWCommissionAmount | `[#Commission Amount#]` (process parameter) |
| 2 | IWCommissionCalculated | True |
| 3 | IWSalesAmount | `[#Calculated Sales Amount#]` (process parameter) |
| 4 | IWCommissionStatus | **Returned** (GUID `ee14b2ce-...`) |
| 5 | IWOwner | `[#Read Order Record.First item.Owner#]` |
| 6 | IWIsReturn | **True** |

---

## VERIFICATION CHECKLIST

After Steps 1-8 (V4):

- [x] **No orphaned elements** — "Set Sales Amount", "Payment Return?", "Payment is Returned" are gone
- [x] **"Order Total > 0?"** has exactly 2 paths:
  - Conditional: **"Has Total"** → "Calculate Sales Amount"
  - Default: → "Set Error - No Total" → Terminate
- [x] **"Calculate Sales Amount"** outputs to **"Does Order Commission Earner have Commission Rate?"** (NOT to deleted "Payment Return?")
- [x] **"Does Order Commission Earner have Commission Rate?"** has exactly 2 paths:
  - Conditional: **"Has Commission Rate"** → "Calculate Commission Amount"
  - Default: → "Set Error - No Rate" → Terminate
- [x] **"Calculate Commission Amount"** still outputs to **"Check Commission Status"**
- [x] **"Check Commission Status"** condition changed to `CalculatedSalesAmount < 0`
  - Conditional: SalesAmt < 0 → "Update Payment 'Returned'"
  - Default: → "Update Payment 'Done'"
- [x] **"Update Payment 'Done'"** has 6 columns (unchanged — Steps 9-10 skipped)
- [x] **"Update Payment 'Returned'"** has 6 columns (unchanged — Steps 9-10 skipped)
- [x] **Both error elements** set IWCommissionStatus = Error GUID + IWCommissionCalculated = False
- [ ] ~~**All 3 signals** still point to "Read Payments Record"~~ → **CHANGED: Remove "Payment Modified" (Step 11)**
- [x] **Save and compile** — no validation errors
- [ ] ~~**No errors thrown** after V4 activation~~ → **BLOCKED: 100x recursion until Step 11 is done**

---

## WHAT THESE CHANGES FIX

| Bug | Before | After |
|-----|--------|-------|
| **IWIsReturn overwrite** | "Payment is Returned" (mid-flow) sets True, then "Update Payment 'Done'" overwrites to False | "Payment Return?" and "Payment is Returned" deleted — return check moved to "Check Commission Status" using calculated value |
| **Stale status perpetuation** | "Check Commission Status" checks ORIGINAL IWCommissionStatus from database | Now checks freshly calculated SalesAmount < 0 |
| **No rate → false "Done"** | "No Commission Rate" path skips calc but still reaches "Update Payment 'Done'" | "No Commission Rate" → "Set Error - No Rate" → Terminate |
| **No total → silent continue** | "Has no Total or 0" path uses raw amount, continues through full flow | "Has no Total or 0" → "Set Error - No Total" → Terminate |
| **Missing CommissionRate** | Not written to payment record | ⏭️ Still not written (deferred — no current consumer) |
| **Missing SalesRep** | Not written by V3/V4 | ✅ Covered by Fill V2 process (no change needed in V4) |

---

## ELEMENTS UNCHANGED (for reference)

These elements require NO modification:

| Designer Label | Why Unchanged |
|----------------|---------------|
| **"Payment Added"** | Signal correctly points to "Read Payments Record" |
| ~~**"Payment Modified"**~~ | **REMOVING in Step 11** — causes 100x recursion |
| **"Payment Deleted"** | Signal correctly points to "Read Payments Record" |
| **"Read Payments Record"** | Correctly reads IWPayments by signal record ID |
| **"Read Order Record"** | Correctly reads Order via Payment.Invoice |
| **"Read Commission Rate"** | Correctly reads BGCommissionEarner via Order.Id |
| **"Calculate Sales Amount"** | Correctly calculates SalesAmount with tax proration |
| **"Calculate Commission Amount"** | Correctly calculates Commission = SalesAmt × Rate% |
| **Terminate** (red circle) | Just terminates — no configuration |
| **"Has Total"** flow | Total > 0 condition stays the same |
| **"Has Commission Rate"** flow | Rate > 0 condition stays the same |
| All signal→read and read→read flows | Internal connections that don't change |

---

## 🔴 RECURSION BUG FIX (Steps 11-12)

### Bug Report

**Symptom:** After saving V4, creating or modifying any IWPayments record triggers V4 ~100 times, then errors with:
> *"Operation interrupted to prevent recursive execution. The maximum allowed background recursion depth: '100' has been exceeded"*

**Root Cause:**
V4's **"Payment Modified"** signal has `NewEntityChangedColumns: []` — meaning it fires on **ANY** field change to IWPayments. V4 itself writes 6 columns to IWPayments (via "Update Payment 'Done'" or "Update Payment 'Returned'"), which triggers its own signal, creating an infinite loop:

```
V4 fires → reads data → calculates → writes 6 cols to IWPayments
   ↓
"Payment Modified" signal fires (because IWPayments was updated)
   ↓
V4 fires AGAIN → reads data → calculates → writes 6 cols to IWPayments
   ↓
"Payment Modified" signal fires AGAIN
   ↓
... repeats 100 times → Creatio kills it
```

**Secondary cascade:** Fill V2 (IW Fill Commission Report Payment Fields) also has a signal on IWPayments Modified. V4's writes trigger Fill V2, and Fill V2's writes trigger V4 back — creating a **ping-pong chain** on top of V4's self-recursion.

**Confirmed by error trace:**
- V4 Schema: `dede2ffb-ed56-4a25-b0e1-8d87b43d5448`
- V4 "Payment Modified" Signal: `522b0a0f-2cb7-4fbb-9a9b-172c42e68634`
- Fill V2 Schema: `0f3a6403-5d0e-43c0-81a4-45d94b4364b8`
- Fill V2 Signal: `138245da-2819-4b47-944f-6e1b909ebfe0`
- Payment Record: `74cf6bce-c64f-4674-8d99-aee5157aefb0`

**V4 IS calculating correctly** — SalesAmount=175.53, CommissionAmount=26.33, CommissionRate=15%, Status=Done. The bug is purely about the signal triggering, not the calculation logic.

---

### Why Filtering Won't Work

We considered filtering "Payment Modified" to specific columns instead of removing it, but this creates a dilemma:

| Filter Option | Problem |
|---------------|---------|
| Filter to IWAmount only | V4 wouldn't recalculate when the subprocess sets IWCommissionStatus = Pending |
| Filter to IWCommissionStatus | V4 writes IWCommissionStatus = Done → triggers itself → still recursive |
| Filter to multiple columns | V4 writes 6 columns — any overlap causes recursion |

**The only clean fix is removing "Payment Modified" entirely from V4.**

---

### STEP 11: Remove "Payment Modified" signal and its flow from V4 — 🔴 TODO

**What to delete:**

| # | Element/Flow | Designer Label | Why |
|---|---|---|---|
| 1 | **Flow** | *(unlabeled)* from "Payment Modified" → "Read Payments Record" | Disconnecting the signal |
| 2 | **Signal element** | **"Payment Modified"** | Removing the recursive trigger |

**In Process Designer:**

1. **Delete the flow first:** Click the arrow from **"Payment Modified"** → **"Read Payments Record"** → Delete
2. **Delete the signal element:** Click the **"Payment Modified"** element (the orange signal icon) → Delete

**After deletion, V4 should have exactly 2 start signals:**
- ✅ **"Payment Added"** → "Read Payments Record"
- ✅ **"Payment Deleted"** → "Read Payments Record"

**What this means:**
- V4 triggers when a new payment is **created** (correct — calculate commission for new payment)
- V4 triggers when a payment is **deleted** (correct — clean up/recalculate)
- V4 does **NOT** trigger when payment fields change (prevents recursion)
- For **order recalculation** (when order products change), the subprocess will need to directly invoke V4 — see "Recalculation Design" section below

---

### STEP 12: Remove StartSignal4 from Fill V2 (IW Fill Commission Report Payment Fields) — 🔴 TODO

> **Decision D3 from original restructuring** — this was already planned but not yet done.

Fill V2 also has a signal that fires on IWPayments Modified, which gets caught in V4's recursion chain. This signal (StartSignal4, ID `138245da`) should be removed.

**In Process Designer:**

1. Open **"IW Fill Commission Report Payment Fields"** process (Fill V2)
2. Find the signal element that triggers on IWPayments Modified
3. Delete the flow from that signal → the next element
4. Delete the signal element itself

**After deletion, Fill V2 should only trigger via its remaining signals** (not on generic IWPayments modification).

---

### Recalculation Design (After Steps 11-12)

With "Payment Modified" removed from V4, we need a way to recalculate commission when order totals change. The current design:

```
Order product added/deleted
    ↓
IWRecalculateCommissionOnOrderChangeV2 (standalone process)
    ↓
Sets IWCommissionStatus = Pending on linked payments
    ↓
??? V4 no longer fires on Modified ???
```

**Two options to close this gap:**

#### Option A: Add "Start Process" element to the subprocess (Recommended)

Add a **Start Process** element at the end of `IWRecalculateCommissionOnOrderChangeV2` that explicitly launches V4 for each affected payment. This is direct invocation, not signal-based — no recursion possible.

**Steps:**
1. Open **IWRecalculateCommissionOnOrderChangeV2** in Process Designer
2. After the element that sets IWCommissionStatus = Pending, add a **"Start Process"** element
3. Configure it to start **"IW Calculate Commission on Payment V4"**
4. Pass the payment record ID as a parameter

#### Option B: Add a filtered "Payment Modified" signal back to V4

Add a new signal that ONLY fires when `IWCommissionStatus` changes to `Pending` specifically. This requires:
- The signal filtered to `IWCommissionStatus` column only
- An **Exclusive Gateway** at the start of V4 that checks: "If IWCommissionStatus is already Done or Error, skip (terminate)"
- This prevents the loop: V4 sets Done → signal fires → V4 checks "already Done" → terminates

**Option A is simpler and more reliable.** Option B has edge cases (what if Fill V2 writes to the same record between the status check and the calculation?).

---

### VERIFICATION CHECKLIST (After Steps 11-12)

- [ ] **V4 has exactly 2 start signals:** "Payment Added" and "Payment Deleted" (NO "Payment Modified")
- [ ] **"Payment Modified" element is GONE** from V4 designer canvas
- [ ] **Fill V2 no longer has IWPayments Modified signal** (StartSignal4 removed)
- [ ] **Save and compile V4** — no validation errors
- [ ] **Save and compile Fill V2** — no validation errors
- [ ] **Test: Create new payment** → V4 fires ONCE, calculates correctly, status = Done
- [ ] **Test: No recursion** — process log shows exactly 1 V4 + 1 Fill V2 execution (not 40+)
- [ ] **Test: Modify payment amount manually** → V4 does NOT fire (expected — we removed that signal)
- [ ] **Test: Delete payment** → V4 fires, handles deletion
- [ ] **Decide on recalculation approach** (Option A or B above) — implement after recursion is confirmed fixed
