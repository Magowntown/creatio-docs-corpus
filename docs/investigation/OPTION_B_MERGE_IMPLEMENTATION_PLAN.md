# Option B Revised: Complete Commission Process Redesign

> **Decision:** 2026-02-10 | **Status:** IMPLEMENTED — VERIFICATION TESTING
> **Supersedes:** Original Option B plan (same date, earlier version)
> **Goal:** Two processes that handle ALL real business scenarios with zero recursion risk

---

## Design Philosophy

**Single writer pattern:** Only V4 writes commission + report data to IWPayments.
**Event-driven bridge:** Order Recalc V2 sets "Pending" status → V4 detects and recalculates.
**Bounce protection:** V4 checks for final status at the start, terminating immediately on bounces.

---

## Complete IWCommissionStatus Lookup (API-Verified)

| Status | GUID | Set By | Meaning |
|--------|------|--------|---------|
| *(empty)* | 00000000-0000-0000-0000-000000000000 | Default | New payment, never calculated |
| **Pending** | 930bb1c6-ca67-4ac0-8f96-a5ea4018a366 | Order Recalc V2 | Awaiting recalculation |
| **Done** | deb80242-b56a-4b94-967a-0e170e2198d8 | V4 | Commission calculated successfully |
| **Returned** | ee14b2ce-163a-4fb2-abea-e739636794ed | V4 | Refund/negative amount |
| **Error** | 26c1b9de-75c9-46c7-8963-e02b8a63f261 | V4 | No earner found or zero commission |
| **Order Deleted** | 8c2313f4-7e27-4781-afef-d16deb90cc6d | Order Recalc V2 | Parent order was deleted |

**Lookup Entity UId:** 94c61392-ccde-4274-88c6-7ffe7660250f

---

## Business Scenarios Covered

| # | Scenario | Trigger | Process | Action |
|---|----------|---------|---------|--------|
| 1 | QB payment arrives | IWPayments **Added** | V4 | Calculate commission + fill report fields |
| 2 | Manual payment created | IWPayments **Added** | V4 | Same as above |
| 3 | Product added/removed from Order | Order **Modified** | Order Recalc V2 → V4 | Set Pending → V4 recalculates + re-fills |
| 4 | Sales tax added/removed | Order **Modified** | Order Recalc V2 → V4 | Same as above |
| 5 | Order amount manually adjusted | Order **Modified** | Order Recalc V2 → V4 | Same as above |
| 6 | Sales rep changed on Order | Order **Modified** | Order Recalc V2 → V4 | Set Pending → V4 re-reads Order → updates SalesRep, SalesGroup |
| 7 | Order deleted | Order **Deleted** | Order Recalc V2 | Sets status to "Order Deleted" on related IWPayments |
| 8 | Payment deleted | IWPayments **Deleted** | *(none)* | No action needed — record is gone |

---

## Architecture: Two Processes

### Process 1: V4 — IWCalculateCommissiononPaymentV4

**Role:** Single authority on IWPayments commission data. Handles calculation AND report field filling for ONE payment per execution.

**Signals:**
| Signal | Entity | Type | Filter |
|--------|--------|------|--------|
| StartSignal2 | IWPayments | **Added** | none |
| StartSignal_Modified (**NEW**) | IWPayments | **Modified** | **IWCommissionStatus column only** |
| ~~StartSignal3~~ | ~~IWPayments~~ | ~~Deleted~~ | **REMOVE** (writing to a deleted record is wasted work) |

**Flow:**
```
StartSignal (Added) ──────────┐
                               ├→ ReadPayment
StartSignal (Modified/Status) ─┘       │
                                        ▼
                              ┌─ Gateway_BounceCheck: Is status a FINAL state? ─┐
                              │  (Done, Returned, Error, Order Deleted)          │
                              │                                                  │
                              YES                                                NO
                              ↓                                                  ↓
                         Terminate_Bounce                              ReadOrder
                         (harmless, instant)                              │
                                                                          ▼
                                                              ReadEmployeeForFill (NEW)
                                                                          │
                                                                          ▼
                                                              ReadSalesGroupForFill (NEW)
                                                                          │
                                                                          ▼
                                                              ReadYearMonthForFill (NEW)
                                                                          │
                                                                          ▼
                                                                    ReadEarner
                                                                          │
                                                                          ▼
                                                              Gateway3: Earner found?
                                                              ├─ NO → ChangeData4 (Error + partial fill)
                                                              └─ YES → Formula1 (calc commission)
                                                                          │
                                                                          ▼
                                                              Gateway1: Commission > 0?
                                                              ├─ NO → ChangeData6 (Error)
                                                              └─ YES → Formula3 (calc sale amount)
                                                                          │
                                                                          ▼
                                                              Gateway4: Amount >= 0?
                                                              ├─ YES → ChangeData1 (Done + calc + fill)
                                                              │         TransType = Sale
                                                              └─ NO  → ChangeData3 (Returned + calc + fill)
                                                                        TransType = Credit Memo
```

### Process 2: Order Recalc V2 — IWRecalculateCommissionOnOrderChangeV2

**Role:** Detects Order changes and triggers V4 recalculation by setting IWPayments status to Pending.

**Signals (StartSignal1 updated 2026-02-10):**
| Signal | Entity | Type | Filter |
|--------|--------|------|--------|
| StartSignal1 | Order | Modified | **6 columns** (Amount, Shipping, SubTotal, Tax, Total, **Sales Rep**) |
| StartSignal2 | Order | Added | none |
| StartSignal3 | Order | Deleted | none |

**Flow (existing, no changes needed):**
```
StartSignal1 (Modified) ─┐
StartSignal2 (Added) ────├→ Gateway1 → ReadOrder → ReadIWPayments → Gateway2:
StartSignal3 (Deleted) ──┘                                           │
                                                              ├─ Order has invoice + payments → ChangeData1 (set Pending)
                                                              ├─ Order has payments only → ChangeData1 (set Pending)
                                                              ├─ Order deleted → ChangeData2 (set "Order Deleted")
                                                              └─ No payments → Terminate
```

**Bridge mechanism:** ChangeData1 sets `IWCommissionStatus = Pending` on all IWPayments for the order. This modification fires V4's new Modified signal → V4 recalculates each payment automatically.

---

## The Bounce — Why It's Safe

When V4 processes a payment and sets status to Done/Returned/Error, the Modified signal fires again (because IWCommissionStatus changed). Here's what happens:

```
1. Order Recalc V2 sets IWPayments.Status = Pending
2. V4 fires (Modified signal) → reads payment → status = Pending → NOT final → proceeds
3. V4 calculates + fills → writes Status = Done (and other columns)
4. Modified signal fires again (IWCommissionStatus changed to Done)
5. V4 fires again → reads payment → status = Done → IS final → Terminate immediately
6. No more signals. Chain complete.
```

**Per payment:** 2 V4 executions (1 useful + 1 instant bounce). The bounce reads one record, hits the gateway, and terminates. No data writes, no cascading.

**Per Order with N payments:** 1 Order Recalc V2 + N useful V4 executions + N instant bounces = 2N+1 total process instances. All bounces are read-only and terminate instantly.

---

## Implementation Steps

### Phase 1: Modify V4 Signals

#### Step 1.1: Add Modified Signal

1. Open V4 in Process Designer
2. Drag a **Signal Start Event** onto the canvas
3. Name it: **StartSignal_RecalcTrigger**
4. Configure:
   - **Object:** IWPayments
   - **When record:** Modified
   - **In which of the selected fields:** Select **IW Commission Status** only
   - This ensures V4 ONLY fires when the status field changes, not on any other IWPayments modification

#### Step 1.2: Remove Deleted Signal

1. Select **StartSignal3** (IWPayments Deleted)
2. Delete it and its outgoing flow arrow
3. This eliminates wasted work on deleted payments

#### Step 1.3: Connect New Signal

1. Draw a flow arrow from **StartSignal_RecalcTrigger** to **ReadPayment** (ReadDataUserTask1)
   - This joins the existing Added signal path

### Phase 2: Add Bounce Protection Gateway

#### Step 2.1: Insert Gateway After ReadPayment

1. **Delete** the flow arrow from ReadPayment → ReadOrder
2. Drag an **Exclusive Gateway** onto the canvas between ReadPayment and ReadOrder
3. Name it: **Gateway_BounceCheck**
4. Connect: ReadPayment → Gateway_BounceCheck

#### Step 2.2: Add Terminate for Bounces

1. Drag a **Terminate** event onto the canvas
2. Name it: **Terminate_Bounce**

#### Step 2.3: Configure Gateway Conditions

**Conditional flow → Terminate_Bounce:**
```
[#ReadPayment.First item.IWCommissionStatus.Id#] == Guid("deb80242-b56a-4b94-967a-0e170e2198d8")
```
Caption: "Status is Done — bounce"

**Conditional flow → Terminate_Bounce (second):**
```
[#ReadPayment.First item.IWCommissionStatus.Id#] == Guid("ee14b2ce-163a-4fb2-abea-e739636794ed")
```
Caption: "Status is Returned — bounce"

**Conditional flow → Terminate_Bounce (third):**
```
[#ReadPayment.First item.IWCommissionStatus.Id#] == Guid("26c1b9de-75c9-46c7-8963-e02b8a63f261")
```
Caption: "Status is Error — bounce"

**Conditional flow → Terminate_Bounce (fourth):**
```
[#ReadPayment.First item.IWCommissionStatus.Id#] == Guid("8c2313f4-7e27-4781-afef-d16deb90cc6d")
```
Caption: "Status is Order Deleted — bounce"

**Default flow → ReadOrder:**
Proceeds with calculation. Handles both:
- New payments (status = empty/null) ✅
- Pending recalculations (status = Pending) ✅

> **Note:** If Creatio's Exclusive Gateway doesn't support 4 separate conditional flows to the same target, combine into a single expression:
> `Status != Empty AND Status != Pending` → Terminate_Bounce
> Or use a Formula task to compute a boolean flag, then a single conditional on the flag.

**Alternative (simpler):** Use ONE conditional flow:
```
Conditional → ReadOrder: [#ReadPayment.First item.IWCommissionStatus.Id#] == Guid.Empty
  OR [#ReadPayment.First item.IWCommissionStatus.Id#] == Guid("930bb1c6-ca67-4ac0-8f96-a5ea4018a366")
```
Caption: "New or Pending — proceed"
**Default → Terminate_Bounce** (everything else is a final state)

### Phase 3: Add Fill V2 ReadData Tasks

(Same as original plan)

#### Step 3.1: Add "Read Employee" ReadData Task

1. Drag a **Read Data** element onto the canvas
2. Name it: **ReadEmployeeForFill**
3. Configure:
   - **Entity:** Employee
   - **Read first record matching conditions**
   - **Filter:** Id = `[#Read Order Record.First item of resulting collection.Sales Rep#]`
   - **Columns to read:** Sales Group (at minimum)

#### Step 3.2: Add "Read Sales Group" ReadData Task

1. Drag a **Read Data** element
2. Name it: **ReadSalesGroupForFill**
3. Configure:
   - **Entity:** BGSalesGroup
   - **Filter:** Id = `[#ReadEmployeeForFill.First item of resulting collection.Sales Group#]`

#### Step 3.3: Add "Read Year-Month" ReadData Task

1. Drag a **Read Data** element
2. Name it: **ReadYearMonthForFill**
3. Configure:
   - **Entity:** BGYearMonth
   - **Filter:** Name = `[#Read IW Payment Record.First item of resulting collection.IWPaymentDue#].ToString("yyyy-MM")`

### Phase 4: Wire New ReadData Tasks Into Flow

**Current flow (after Phase 2):** Gateway_BounceCheck → ReadOrder → ReadEarner
**New flow:** Gateway_BounceCheck → ReadOrder → **ReadEmployeeForFill** → **ReadSalesGroupForFill** → **ReadYearMonthForFill** → ReadEarner

1. Delete the flow arrow from ReadOrder to ReadEarner
2. Connect: ReadOrder → ReadEmployeeForFill → ReadSalesGroupForFill → ReadYearMonthForFill → ReadEarner

### Phase 5: Add Fill Columns to ChangeData Tasks

#### Step 5.1: Update ChangeDataUserTask1 (Success — Status=Done)

Add 5 new columns to existing "Set column values":

| Column | Value |
|--------|-------|
| Description | `[#Read Order Record.First item.Description#]` |
| Sales Rep | `[#Read Order Record.First item.Sales Rep#]` |
| Sales Group | `[#ReadSalesGroupForFill.First item.Id#]` |
| Year-Month | `[#ReadYearMonthForFill.First item.Id#]` |
| QB Transaction Type | Lookup → QuickBooks Transaction Type → **Sale** (`b4494f26-26c2-4aa6-951c-658d0828d0d0`) |

#### Step 5.2: Update ChangeDataUserTask3 (Refund — Status=Returned)

Add same 5 columns, **except TransType:**

| Column | Value |
|--------|-------|
| Description | `[#Read Order Record.First item.Description#]` |
| Sales Rep | `[#Read Order Record.First item.Sales Rep#]` |
| Sales Group | `[#ReadSalesGroupForFill.First item.Id#]` |
| Year-Month | `[#ReadYearMonthForFill.First item.Id#]` |
| QB Transaction Type | Lookup → QuickBooks Transaction Type → **Credit Memo** (`c26d3478-7ac1-49e9-97f9-1c0809552f1f`) |

#### Step 5.3: Update ChangeDataUserTask4 and ChangeDataUserTask6 (Error paths)

Add partial fill (available data only):

| Column | Value |
|--------|-------|
| Description | `[#Read Order Record.First item.Description#]` |
| Sales Rep | `[#Read Order Record.First item.Sales Rep#]` |

### Phase 6: Disable Fill V2

1. Open **IWFillCommissionReportPaymentsFieldsV2** in Process Designer
2. Set **Active** to No
3. Save (do NOT Publish)

### Phase 7: Publish V4

1. Open V4 in Process Designer
2. Click **Publish** (NOT Compile All!)
3. This generates C# code, registers ALL signals (including the new Modified signal), and clears NeedUpdate flags

### Phase 8: Publish Order Recalc V2

1. Open **IWRecalculateCommissionOnOrderChangeV2** in Process Designer
2. Click **Publish**
3. This registers its Order signals (never been registered before)

### Phase 9: Disable Legacy Processes

1. Disable **IWCalculateCommissiononPayment** (V1)
2. Disable **IWFillCommissionReportPaymentsFields** (Fill V1)
3. Disable **IWRecalculateCommissionOnOrderChange** (Order Recalc V1)

---

## Verification Checklist

### Test 1: New Payment (Added Signal)

- [ ] Create a new IWPayment record linked to an Order
- [ ] Verify V4 fires in SysProcessLog
- [ ] Verify IWPayment has: Commission Amount, Status=Done, Description, SalesRep, SalesGroup, YearMonth, TransType=Sale, Owner
- [ ] Verify Fill V2 does NOT fire
- [ ] Verify only 1 V4 execution (no bounce for Added)

### Test 2: Order Modified (Recalculation Chain)

- [ ] Modify an existing Order's Amount field
- [ ] Verify Order Recalc V2 fires in SysProcessLog
- [ ] Verify related IWPayments status changes to Pending
- [ ] Verify V4 fires for each related IWPayment
- [ ] Verify IWPayments are recalculated with updated commission amounts
- [ ] Verify report fields (Description, SalesRep, etc.) are refreshed
- [ ] Verify bounce executions appear but terminate immediately (no errors)

### Test 3: Order Deleted

- [ ] Delete an Order that has IWPayments
- [ ] Verify Order Recalc V2 fires
- [ ] Verify IWPayments status set to "Order Deleted"
- [ ] Verify V4 fires (bounce) but terminates immediately (Order Deleted is a final state)

### Test 4: No Infinite Loops

- [ ] After each test, check SysProcessLog
- [ ] Count V4 executions: should be exactly N (useful) + N (bounces) for N payments
- [ ] No executions beyond the bounce
- [ ] No errors in process log

---

## Reference Data

### IWCommissionStatus Lookup (Complete)

| Status | GUID | Final State? |
|--------|------|-------------|
| *(empty)* | 00000000-0000-0000-0000-000000000000 | No → V4 proceeds |
| Pending | 930bb1c6-ca67-4ac0-8f96-a5ea4018a366 | No → V4 proceeds |
| Done | deb80242-b56a-4b94-967a-0e170e2198d8 | **Yes → V4 terminates** |
| Returned | ee14b2ce-163a-4fb2-abea-e739636794ed | **Yes → V4 terminates** |
| Error | 26c1b9de-75c9-46c7-8963-e02b8a63f261 | **Yes → V4 terminates** |
| Order Deleted | 8c2313f4-7e27-4781-afef-d16deb90cc6d | **Yes → V4 terminates** |

### TransType Lookup

| Name | GUID |
|------|------|
| Sale | b4494f26-26c2-4aa6-951c-658d0828d0d0 |
| Credit Memo | c26d3478-7ac1-49e9-97f9-1c0809552f1f |

### IWCommissionStatus Lookup Entity UId

`94c61392-ccde-4274-88c6-7ffe7660250f`

### Process UIds

| Process | UId | Action |
|---------|-----|--------|
| V4 | dede2ffb-ed56-4a25-b0e1-8d87b43d5448 | MODIFY + PUBLISH |
| Fill V2 | 0f3a6403-5d0e-43c0-81a4-45d94b4364b8 | DISABLE |
| Order Recalc V2 | 3c425afe-3ee8-4d38-baf2-a30de552bd94 | PUBLISH (Sales Rep added to signal filter) |
| V1 | c2623b8a-338e-4adb-afbe-cb76b68368d9 | DISABLE |
| Fill V1 | d814f639-4d62-4dad-b954-128fd621f169 | DISABLE |
| Order Recalc V1 | 04e376c2-3452-4786-88d9-faf096c98ec6 | DISABLE |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Bounce doubles V4 execution count | Bounces terminate instantly (read + gateway only). Acceptable overhead. |
| Creatio fires Modified per-UPDATE not per-value-change | Bounce check handles this — final states always terminate |
| Many payments per Order = many process instances | Each runs independently. Creatio handles concurrent process instances. |
| SalesGroup null reference | Creatio leaves column null if ReadData finds no records. Acceptable. |
| Order Recalc V2 sets "Order Deleted" → V4 fires bounce | V4 recognizes "Order Deleted" as final state → terminates |
| Fill V2 accidentally re-enabled | Disabled + documented. Delete after 2 weeks validation. |
| V4 and Order Recalc V2 run simultaneously on same payment | Both write different columns. V4 wins on commission data (last writer). |

---

## Rollback Plan

1. Disable V4 (set Active=No)
2. Re-enable Fill V2 (with Modified signal REMOVED — Option A fallback)
3. Publish Fill V2 with only Added + Deleted signals
4. Re-publish V4 without the Modified signal and fill columns

---

## Future Considerations

| Item | When | Description |
|------|------|-------------|
| Payment BGOrder changed | If needed | Add BGOrder column to V4's Modified signal filter |
| Manual payment amount edit | If needed | Add IWAmount column to V4's Modified signal filter |
| Commission report accuracy | Ongoing | V4 now refreshes ALL report fields on every recalculation |
| Delete Fill V2 permanently | After 2 weeks stable | Remove dead code |
| Delete V1 processes permanently | After 2 weeks stable | Remove dead code |
