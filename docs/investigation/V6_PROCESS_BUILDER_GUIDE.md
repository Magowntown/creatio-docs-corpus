# V6 Commission Process — Step-by-Step Builder Guide

> **Process Name:** `IWOrderandPaymentsSync`
> **Package:** PampaBay (or preferred package)
> **Created:** 2026-02-11
> **Replaces:** V4 Calculator + Fill V2 Report Fields + Order Recalc V2

This guide walks through building the combined commission process in Creatio's visual Process Designer. Follow each step exactly — element names, filter configurations, and column mappings are all verified against OData metadata.

---

## Table of Contents

1. [Create Process Shell](#step-1-create-process-shell)
2. [Add Process Parameters](#step-2-add-process-parameters)
3. [Add All 8 Signals](#step-3-add-all-8-signals)
4. [Build Path B1 — Order Change](#step-4-build-path-b1--order-change-simplest-test-first)
5. [Build Path B2 — OrderProduct Change](#step-5-build-path-b2--orderproduct-change)
6. [Build Path C — Order Deleted](#step-6-build-path-c--order-deleted)
7. [Build Path A — Payment Processing](#step-7-build-path-a--payment-processing-main-flow)
8. [Publish](#step-8-publish)
9. [Testing Sequence](#step-9-testing-sequence)
10. [Disable Old Processes](#step-10-disable-old-processes)
11. [Troubleshooting](#troubleshooting)

---

## Step 1: Create Process Shell

1. Open **Process Designer** in Creatio
   - Configuration → Process Library → **Add Process**
2. Set properties:
   - **Title:** `IW Order and Payments Sync`
   - **Code (Name):** `IWOrderandPaymentsSync`
   - **Package:** PampaBay
   - **Tag:** Commission
   - **Description:** `Combined commission calculator. Replaces V4 Calculator, Fill V2 Report Fields, and Order Recalc V2. Triggers on Order, OrderProduct, and Payment changes.`
3. **Save** (not Publish yet)

---

## Step 2: Add Process Parameters

Open the process properties panel (click the canvas background). Add these 4 parameters:

| # | Name | Caption | Type | Default |
|---|------|---------|------|---------|
| 1 | `CalculatedSalesAmount` | Calculated Sales Amount | Decimal (Money) | 0 |
| 2 | `CommissionAmount` | Commission Amount | Decimal (Money) | 0 |
| 3 | `CommissionRate` | Commission Rate | Decimal | 0 |
| 4 | `PaymentYearMonthName` | Payment Year Month Name | Text (50) | *(empty)* |

**Save** after adding parameters.

---

## Step 3: Add All 8 Signals

Drag 8 **Signal** start events onto the canvas. Configure each one:

### Signal 1: PaymentAdded

| Property | Value |
|----------|-------|
| **Name** | `PaymentAdded` |
| **Which event?** | Record Added |
| **In which object?** | IWPayments |
| **Expected record changes** | *(none — fires on any new record)* |

### Signal 2: PaymentStatusChanged

| Property | Value |
|----------|-------|
| **Name** | `PaymentStatusChanged` |
| **Which event?** | Record Modified |
| **In which object?** | IWPayments |
| **Expected record changes** | **In any of the selected fields** |
| **Selected fields** | `IWCommissionStatus` only |

> **CRITICAL:** This column filter prevents recursion. When V6 writes IWCommissionAmount, IWSalesAmount, etc., this signal does NOT fire. It only fires when IWCommissionStatus changes.

### Signal 3: OrderAdded

| Property | Value |
|----------|-------|
| **Name** | `OrderAdded` |
| **Which event?** | Record Added |
| **In which object?** | Order |

### Signal 4: OrderModified

| Property | Value |
|----------|-------|
| **Name** | `OrderModified` |
| **Which event?** | Record Modified |
| **In which object?** | Order |
| **Expected record changes** | **In any of the selected fields** |
| **Selected fields** | `Amount`, `BGTaxAmount`, `BGSubTotal`, `BGShippingCharge`, `BGSalesRepLookup`, `BGSalesGroup` |

### Signal 5: OrderDeleted

| Property | Value |
|----------|-------|
| **Name** | `OrderDeleted` |
| **Which event?** | Record Deleted |
| **In which object?** | Order |

### Signal 6: OrderProductAdded

| Property | Value |
|----------|-------|
| **Name** | `OrderProductAdded` |
| **Which event?** | Record Added |
| **In which object?** | OrderProduct |

### Signal 7: OrderProductModified

| Property | Value |
|----------|-------|
| **Name** | `OrderProductModified` |
| **Which event?** | Record Modified |
| **In which object?** | OrderProduct |
| **Expected record changes** | **In any of the selected fields** |
| **Selected fields** | `Amount`, `Quantity`, `Price`, `TaxAmount` |

### Signal 8: OrderProductDeleted

| Property | Value |
|----------|-------|
| **Name** | `OrderProductDeleted` |
| **Which event?** | Record Deleted |
| **In which object?** | OrderProduct |

**Save** after adding all 8 signals. The canvas should now show 8 green circle start events.

---

## Step 4: Build Path B1 — Order Change (Simplest, Test First)

> **Why B1 first?** This is the simplest path with only 1 column write. It tests whether ChangeData works correctly before building complex multi-column writes.

### Elements to Add

```
OrderAdded ────────┐
                    ├──→ ChangeData_SetPending ──→ Terminate_B1
OrderModified ─────┘
```

### 4.1: ChangeData_SetPending

Drag a **Modify data** element onto the canvas.

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_SetPending` |
| **Caption** | Set Payments to Pending |
| **Which object to modify records?** | IWPayments |
| **How to filter records?** | Filter by column value |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `IWPaymentsInvoice` | = | Signal → `RecordId` |

> **How to set the filter value to Signal RecordId:**
> 1. Click "Add condition"
> 2. Select column: `IWPaymentsInvoice` (this is the lookup to Order)
> 3. Condition: equals
> 4. Value source: **Process parameter**
> 5. For OrderAdded connection: Select `OrderAdded` → `Record ID`
> 6. For OrderModified connection: Select `OrderModified` → `Record ID`
>
> **Note:** Since both signals connect to this same element, the RecordId will come from whichever signal fired. In the Process Designer, you may need to use a **Parallel Gateway** or simply connect both signals to the same element — the "RecordId" of the firing signal is automatically the active one.

**Column Values to Set:**

| Column | Value Type | Value |
|--------|-----------|-------|
| `IWCommissionStatus` | Lookup value | **Pending** (`930bb1c6-ca67-4ac0-8f96-a5ea4018a366`) |

### 4.2: Terminate_B1

Drag a **Terminate** event after ChangeData_SetPending.

| Property | Value |
|----------|-------|
| **Name** | `Terminate_B1` |

### 4.3: Connect the Elements

1. Draw a connector from **OrderAdded** → **ChangeData_SetPending**
2. Draw a connector from **OrderModified** → **ChangeData_SetPending**
3. Draw a connector from **ChangeData_SetPending** → **Terminate_B1**

### 4.4: SAVE AND TEST

**Save** the process. Click **Publish**.

**Test procedure:**
1. Open any Order in Creatio that has IWPayments records
2. Change the Order's Amount field slightly (e.g., add $0.01)
3. Save the Order
4. Wait 5-10 seconds
5. Check the IWPayments records for that order — `IWCommissionStatus` should now be "Pending"

```bash
# Run the test script to verify
source .env && python3 scripts/diagnostics/test_v6_process.py --check-only
```

**If ChangeData writes null instead of "Pending":** STOP. Switch to Script Task fallback (see [Troubleshooting](#troubleshooting)).

**If it works:** Continue to Phase 5.

---

## Step 5: Build Path B2 — OrderProduct Change

```
OrderProductAdded ────────┐
OrderProductModified ─────┤
OrderProductDeleted ──────┴──→ ReadOrderProduct ──→ ChangeData_SetPending2 ──→ Terminate_B2
```

### 5.1: ReadOrderProduct

Drag a **Read data** element onto the canvas.

| Property | Value |
|----------|-------|
| **Name** | `ReadOrderProduct` |
| **Caption** | Read Order Product |
| **Which data read mode?** | Read the first record matching the conditions |
| **Which object to read data from?** | OrderProduct |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | Signal → `RecordId` (from whichever OrderProduct signal fired) |

**Columns to read:**
- `OrderId` (the FK to the parent Order)

### 5.2: ChangeData_SetPending2

Drag a **Modify data** element.

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_SetPending2` |
| **Caption** | Set Payments to Pending (OrderProduct) |
| **Which object to modify records?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `IWPaymentsInvoice` | = | **ReadOrderProduct** → `OrderId` |

**Column Values to Set:**
| Column | Value Type | Value |
|--------|-----------|-------|
| `IWCommissionStatus` | Lookup value | **Pending** (`930bb1c6-ca67-4ac0-8f96-a5ea4018a366`) |

### 5.3: Terminate_B2

| Property | Value |
|----------|-------|
| **Name** | `Terminate_B2` |

### 5.4: Connect

1. **OrderProductAdded** → **ReadOrderProduct**
2. **OrderProductModified** → **ReadOrderProduct**
3. **OrderProductDeleted** → **ReadOrderProduct**
4. **ReadOrderProduct** → **ChangeData_SetPending2**
5. **ChangeData_SetPending2** → **Terminate_B2**

> **Note on OrderProductDeleted:** The record may already be gone when ReadData executes. If ReadOrderProduct returns no results, the process terminates gracefully (ChangeData with no matching filter just does nothing). The Order total also auto-recalculates, which triggers Path B1 as a backup.

---

## Step 6: Build Path C — Order Deleted

```
OrderDeleted ──→ ChangeData_SetOrderDeleted ──→ Terminate_C
```

### 6.1: ChangeData_SetOrderDeleted

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_SetOrderDeleted` |
| **Caption** | Set Payments to Order Deleted |
| **Which object to modify records?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `IWPaymentsInvoice` | = | **OrderDeleted** → `Record ID` |

**Column Values to Set:**
| Column | Value Type | Value |
|--------|-----------|-------|
| `IWCommissionStatus` | Lookup value | **Order Deleted** (`8c2313f4-7e27-4781-afef-d16deb90cc6d`) |

### 6.2: Terminate_C

| Property | Value |
|----------|-------|
| **Name** | `Terminate_C` |

### 6.3: Connect

1. **OrderDeleted** → **ChangeData_SetOrderDeleted**
2. **ChangeData_SetOrderDeleted** → **Terminate_C**

---

## Step 7: Build Path A — Payment Processing (Main Flow)

This is the complex path with commission calculation. Build it element by element.

```
PaymentAdded ─────────┐
                       ├──→ ReadPayment ──→ BounceCheck ──→ ReadOrder ──→ OrderTotalCheck
PaymentStatusChanged ──┘         │              │                              │
                            (read payment)  (final? terminate)           (<=0? error)
                                                                               │
                                                                               ↓
                               ReadEmployee ← ReadSalesGroup ← Formula_YearMonth ← ...
                                     ↓
                               ReadYearMonth → ReadCommissionRate → HasRate?
                                                                      │
                                                              (no rate → error)
                                                                      │
                                                                      ↓
                                                    Formula_CalcSalesAmount → Formula_CalcCommission
                                                                                      │
                                                                                 CheckSign?
                                                                              >=0 │    │ <0
                                                                                  ↓    ↓
                                                                         WriteDone  WriteReturned
                                                                              ↓        ↓
                                                                          Terminate  Terminate
```

### 7.1: ReadPayment

Drag a **Read data** element.

| Property | Value |
|----------|-------|
| **Name** | `ReadPayment` |
| **Caption** | Read Payment |
| **Which data read mode?** | Read the first record matching the conditions |
| **Which object to read data from?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | Signal → `RecordId` |

**Columns to read (important!):**
- `Id`
- `IWAmount`
- `IWPaymentDue`
- `IWPaymentsInvoiceId` (the Order FK)
- `IWCommissionStatusId`

### 7.2: BounceCheck Gateway

Drag an **Exclusive Gateway (OR)**.

| Property | Value |
|----------|-------|
| **Name** | `BounceCheck` |
| **Caption** | Already Processed? |

Connect **ReadPayment** → **BounceCheck**.

Add a **conditional flow** from BounceCheck to a new Terminate element:

**Condition (Bounce — terminate if already final):**

Using the Creatio formula syntax:
```
[#ReadPayment.IWCommissionStatusId#] == [#Lookup.IWCommissionStatus.Done.deb80242-b56a-4b94-967a-0e170e2198d8#]
|| [#ReadPayment.IWCommissionStatusId#] == [#Lookup.IWCommissionStatus.Returned.ee14b2ce-163a-4fb2-abea-e739636794ed#]
|| [#ReadPayment.IWCommissionStatusId#] == [#Lookup.IWCommissionStatus.Error.26c1b9de-75c9-46c7-8963-e02b8a63f261#]
|| [#ReadPayment.IWCommissionStatusId#] == [#Lookup.IWCommissionStatus.Order Deleted.8c2313f4-7e27-4781-afef-d16deb90cc6d#]
```

> **Alternative simpler approach:** If the formula editor doesn't support multi-OR with lookups, use a **different pattern**:
> - Make the **default flow** go to the Terminate (bounce)
> - Make a **conditional flow** for "Pending or New" that continues processing:
>   ```
>   [#ReadPayment.IWCommissionStatusId#] == [#Lookup.IWCommissionStatus.Pending.930bb1c6-ca67-4ac0-8f96-a5ea4018a366#]
>   || [#ReadPayment.IWCommissionStatusId#] == Guid.Empty
>   ```
> - This way: Pending/New → continue processing, everything else → terminate

Connect:
- BounceCheck → **Terminate_Bounce** (conditional: status is final) or (default: if using the inverted approach)
- BounceCheck → **ReadOrder** (default flow, or conditional: status is Pending/Empty)

### 7.3: Terminate_Bounce

| Property | Value |
|----------|-------|
| **Name** | `Terminate_Bounce` |
| **Caption** | Already Processed - Skip |

### 7.4: ReadOrder

| Property | Value |
|----------|-------|
| **Name** | `ReadOrder` |
| **Caption** | Read Parent Order |
| **Which object to read data from?** | Order |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadPayment** → `IWPaymentsInvoice` |

**Columns to read:**
- `Id`
- `Amount`
- `BGTaxAmount`
- `BGSubTotal`
- `BGShippingCharge`
- `BGSalesRepLookupId`
- `BGSalesGroupId`
- `OwnerId`
- `BGOrderDescription`

### 7.5: OrderTotalCheck Gateway

Drag an **Exclusive Gateway (OR)**.

| Property | Value |
|----------|-------|
| **Name** | `OrderTotalCheck` |
| **Caption** | Order Total > 0? |

**Conditional flow → ChangeData_SetError:**
```
[#ReadOrder.Amount#] <= 0
```

**Default flow → ReadEmployee** (continues processing)

### 7.6: ChangeData_SetError

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_SetError` |
| **Caption** | Set Payment to Error |
| **Which object to modify records?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadPayment** → `Id` |

**Column Values to Set:**
| Column | Value Type | Value |
|--------|-----------|-------|
| `IWCommissionStatus` | Lookup value | **Error** (`26c1b9de-75c9-46c7-8963-e02b8a63f261`) |
| `IWCommissionCalculated` | Boolean constant | `false` |

Connect: **ChangeData_SetError** → **Terminate_Error**

### 7.7: Terminate_Error

| Property | Value |
|----------|-------|
| **Name** | `Terminate_Error` |

### 7.8: ReadEmployee

| Property | Value |
|----------|-------|
| **Name** | `ReadEmployee` |
| **Caption** | Read Sales Rep Employee |
| **Which object to read data from?** | Employee |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadOrder** → `BGSalesRepLookup` |

**Columns to read:**
- `Id`
- `Name`

### 7.9: ReadSalesGroup

| Property | Value |
|----------|-------|
| **Name** | `ReadSalesGroup` |
| **Caption** | Read Sales Group |
| **Which object to read data from?** | BGSalesGroup |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadOrder** → `BGSalesGroup` |

**Columns to read:**
- `Id`
- `Name`

### 7.10: Formula_YearMonth

Drag a **Formula** element (or **Set parameter value** — in some Creatio versions this is under "System actions").

| Property | Value |
|----------|-------|
| **Name** | `Formula_YearMonth` |
| **Caption** | Calculate Year-Month String |
| **Which parameter to set?** | `PaymentYearMonthName` (process parameter) |
| **Formula value:** | `[#ReadPayment.IWPaymentDue#].ToString("yyyy-MM")` |

> **If Formula element is unavailable:** Use a Script Task with:
> ```csharp
> Set("PaymentYearMonthName",
>     Get<DateTime>("ReadPayment.IWPaymentDue").ToString("yyyy-MM"));
> return true;
> ```

### 7.11: ReadYearMonth

| Property | Value |
|----------|-------|
| **Name** | `ReadYearMonth` |
| **Caption** | Read Year Month Lookup |
| **Which object to read data from?** | BGYearMonth |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Name` | = | Process parameter → `PaymentYearMonthName` |

**Columns to read:**
- `Id`
- `Name`

### 7.12: ReadCommissionRate

| Property | Value |
|----------|-------|
| **Name** | `ReadCommissionRate` |
| **Caption** | Read Commission Earner |
| **Which object to read data from?** | BGCommissionEarner |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `BGOrder` | = | **ReadOrder** → `Id` |

**Columns to read:**
- `Id`
- `BGCommissionRate`

**After reading:** You need to map BGCommissionRate to the process parameter. Add a **Formula** or **Set parameter value** element:

### 7.12b: SetCommissionRate

| Property | Value |
|----------|-------|
| **Name** | `SetCommissionRate` |
| **Caption** | Copy Commission Rate to Parameter |
| **Which parameter to set?** | `CommissionRate` (process parameter) |
| **Formula value:** | `[#ReadCommissionRate.BGCommissionRate#]` |

### 7.13: HasRate Gateway

Drag an **Exclusive Gateway (OR)**.

| Property | Value |
|----------|-------|
| **Name** | `HasRateCheck` |
| **Caption** | Has Commission Rate? |

**Conditional flow → ChangeData_SetError:**
```
[#CommissionRate#] == 0
```

**Default flow → Formula_CalcSalesAmount** (continues)

> **Note:** Reuse the same ChangeData_SetError element from step 7.6 — just draw a second connector into it. Or create a duplicate `ChangeData_SetError2` with identical configuration if the designer doesn't support multiple inputs.

### 7.14: Formula_CalcSalesAmount

| Property | Value |
|----------|-------|
| **Name** | `Formula_CalcSalesAmount` |
| **Caption** | Calculate Sales Amount |
| **Which parameter to set?** | `CalculatedSalesAmount` (process parameter) |
| **Formula value:** | |

```
[#ReadPayment.IWAmount#] - ([#ReadOrder.BGTaxAmount#] * [#ReadPayment.IWAmount#] / [#ReadOrder.Amount#])
```

> This formula deducts the proportional tax from the payment. For a $100 payment on a $500 order with $25 tax: SalesAmount = 100 - (25 * 100 / 500) = 100 - 5 = 95.

### 7.15: Formula_CalcCommission

| Property | Value |
|----------|-------|
| **Name** | `Formula_CalcCommission` |
| **Caption** | Calculate Commission Amount |
| **Which parameter to set?** | `CommissionAmount` (process parameter) |
| **Formula value:** | |

```
[#CalculatedSalesAmount#] * ([#CommissionRate#] / 100)
```

### 7.16: CheckSign Gateway

Drag an **Exclusive Gateway (OR)**.

| Property | Value |
|----------|-------|
| **Name** | `CheckSign` |
| **Caption** | Positive or Negative Sales? |

**Conditional flow → ChangeData_WriteReturned:**
```
[#CalculatedSalesAmount#] < 0
```

**Default flow → ChangeData_WriteDone** (positive sales)

### 7.17: ChangeData_WriteDone

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_WriteDone` |
| **Caption** | Write Commission - Done |
| **Which object to modify records?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadPayment** → `Id` |

**Column Values to Set (11 columns):**

| # | Column | Value Source | Value |
|---|--------|-------------|-------|
| 1 | `IWCommissionStatus` | Lookup value | **Done** (`deb80242-b56a-4b94-967a-0e170e2198d8`) |
| 2 | `IWCommissionAmount` | Process parameter | `CommissionAmount` |
| 3 | `IWSalesAmount` | Process parameter | `CalculatedSalesAmount` |
| 4 | `IWCommissionCalculated` | Boolean constant | `true` |
| 5 | `IWIsReturn` | Boolean constant | `false` |
| 6 | `IWOwner` | Element reference | **ReadOrder** → `OwnerId` |
| 7 | `IWBGTransactionType` | Lookup value | **Sale** (`b4494f26-26c2-4aa6-951c-658d0828d0d0`) |
| 8 | `IWSalesGroup` | Element reference | **ReadSalesGroup** → `Id` |
| 9 | `IWBGSalesRep` | Element reference | **ReadOrder** → `BGSalesRepLookup` |
| 10 | `IWBGYearMonth` | Element reference | **ReadYearMonth** → `Id` |
| 11 | `IWDescription` | Element reference | **ReadOrder** → `BGOrderDescription` |

Connect: **ChangeData_WriteDone** → **Terminate_Done**

### 7.18: Terminate_Done

| Property | Value |
|----------|-------|
| **Name** | `Terminate_Done` |

### 7.19: ChangeData_WriteReturned

| Property | Value |
|----------|-------|
| **Name** | `ChangeData_WriteReturned` |
| **Caption** | Write Commission - Returned |
| **Which object to modify records?** | IWPayments |

**Filter Configuration:**
| Column | Condition | Value |
|--------|-----------|-------|
| `Id` | = | **ReadPayment** → `Id` |

**Column Values to Set (11 columns):**

| # | Column | Value Source | Value |
|---|--------|-------------|-------|
| 1 | `IWCommissionStatus` | Lookup value | **Returned** (`ee14b2ce-163a-4fb2-abea-e739636794ed`) |
| 2 | `IWCommissionAmount` | Process parameter | `CommissionAmount` |
| 3 | `IWSalesAmount` | Process parameter | `CalculatedSalesAmount` |
| 4 | `IWCommissionCalculated` | Boolean constant | `true` |
| 5 | `IWIsReturn` | Boolean constant | `true` |
| 6 | `IWOwner` | Element reference | **ReadOrder** → `OwnerId` |
| 7 | `IWBGTransactionType` | Lookup value | **Credit Memo** (`c26d3478-7ac1-49e9-97f9-1c0809552f1f`) |
| 8 | `IWSalesGroup` | Element reference | **ReadSalesGroup** → `Id` |
| 9 | `IWBGSalesRep` | Element reference | **ReadOrder** → `BGSalesRepLookup` |
| 10 | `IWBGYearMonth` | Element reference | **ReadYearMonth** → `Id` |
| 11 | `IWDescription` | Element reference | **ReadOrder** → `BGOrderDescription` |

Connect: **ChangeData_WriteReturned** → **Terminate_Returned**

### 7.20: Terminate_Returned

| Property | Value |
|----------|-------|
| **Name** | `Terminate_Returned` |

### 7.21: Connect Path A (Full Chain)

Summary of all Path A connections:

```
PaymentAdded ──────────→ ReadPayment
PaymentStatusChanged ──→ ReadPayment
ReadPayment ──────────→ BounceCheck
BounceCheck ──(final status)──→ Terminate_Bounce
BounceCheck ──(default/pending)──→ ReadOrder
ReadOrder ────────────→ OrderTotalCheck
OrderTotalCheck ──(<=0)──→ ChangeData_SetError → Terminate_Error
OrderTotalCheck ──(default)──→ ReadEmployee
ReadEmployee ─────────→ ReadSalesGroup
ReadSalesGroup ───────→ Formula_YearMonth
Formula_YearMonth ────→ ReadYearMonth
ReadYearMonth ────────→ ReadCommissionRate
ReadCommissionRate ───→ SetCommissionRate
SetCommissionRate ────→ HasRateCheck
HasRateCheck ──(rate=0)──→ ChangeData_SetError → Terminate_Error
HasRateCheck ──(default)──→ Formula_CalcSalesAmount
Formula_CalcSalesAmount → Formula_CalcCommission
Formula_CalcCommission → CheckSign
CheckSign ──(negative)──→ ChangeData_WriteReturned → Terminate_Returned
CheckSign ──(default/positive)──→ ChangeData_WriteDone → Terminate_Done
```

---

## Step 8: Publish

1. **Save** the process
2. Click **Publish** in the Process Designer toolbar

> **CRITICAL:** You MUST use **Publish** (not "Compile All" from Configuration).
> - **Publish** generates C# code, compiles it, AND registers all 8 signal start events
> - **Compile All** only recompiles existing code — it does NOT register new signals
> - If you only Compile All, the 8 signals will never fire

After publishing, verify:
```bash
source .env && python3 scripts/diagnostics/test_v6_process.py --check-only
```

---

## Step 9: Testing Sequence

Test in this exact order. Each test builds on the previous.

### Test 1: Path B1 — Order Modification (ChangeData Validation)

**Purpose:** Confirm ChangeData writes correctly (not null).

1. Find an Order in Creatio that has at least 1 IWPayments record
2. Note the current IWCommissionStatus of those payments
3. Edit the Order — change Amount by $0.01
4. Save the Order
5. Wait 10 seconds
6. Check IWPayments for that order:
   - **Expected:** IWCommissionStatus = "Pending" (`930bb1c6...`)
   - **If null:** ChangeData bug confirmed — switch to Script Task fallback

```bash
source .env && python3 scripts/diagnostics/test_v6_process.py --verify-order <ORDER_GUID>
```

### Test 2: Path A — New Payment (Full Calculation)

**Purpose:** Confirm full commission calculation pipeline.

**Prerequisites:**
- An Order with Amount > 0
- A BGCommissionEarner record linked to that Order
- A BGYearMonth record matching the payment date

1. Create a new IWPayments record linked to the test Order
2. Set IWAmount to a known value (e.g., $100)
3. Set IWPaymentDue to a date with a matching BGYearMonth
4. Wait 10-30 seconds for process execution
5. Verify payment record:
   - **IWCommissionStatus** = Done (or Returned if negative)
   - **IWSalesAmount** = Payment - proportional tax
   - **IWCommissionAmount** = SalesAmount × Rate / 100
   - **IWCommissionCalculated** = true
   - **IWBGSalesRep** = Order's BGSalesRepLookup
   - **IWSalesGroup** = Order's BGSalesGroup
   - **IWBGYearMonth** = Matching year-month record
   - **IWBGTransactionType** = Sale (or Credit Memo)
   - **IWOwner** = Order's Owner

### Test 3: Path B Cascade — Order Change Triggers Recalculation

1. Using the same Order from Test 2
2. Change the Order's Amount (e.g., add $50)
3. Save the Order
4. Wait 10-30 seconds
5. Check:
   - First, Path B1 fires → sets payments to "Pending"
   - Then, Signal #2 fires for each payment → Path A recalculates
   - Payment should end up with updated SalesAmount and Commission

### Test 4: Path B2 — OrderProduct Change

1. Add or modify an OrderProduct for the test Order
2. Wait 10-30 seconds
3. Verify payments recalculated (same checks as Test 3)

### Test 5: Path C — Order Deleted

**WARNING:** This deletes an Order. Use a test order.

1. Delete the test Order
2. Check IWPayments records:
   - **IWCommissionStatus** should = "Order Deleted"

### Test 6: Bounce Check

1. Check SysProcessLog for V6 executions
2. After Test 2 (which writes "Done"), Signal #2 fires again
3. V6 starts → BounceCheck sees "Done" → Terminate immediately
4. This second execution should be very fast (<1 second)
5. Verify no infinite recursion in the process log

```bash
source .env && python3 scripts/diagnostics/test_v6_process.py
```

---

## Step 10: Disable Old Processes

**Only after ALL tests pass:**

1. Open Process Library
2. Find each old process and set **"Actual version"** = No:
   - `IWCalculateCommissiononPaymentV4` (or V5)
   - `IWFillCommissionReportPaymentsFieldsV2`
   - `IWRecalculateCommissionOnOrderChangeV2`
3. Optionally disable V1 processes too:
   - `IWCalculateCommissiononPayment` (V1)
   - `IWRecalculateCommissionOnOrderChange` (V1)

> **Do NOT delete** the old processes — just remove "Actual version" status. This allows rollback.

---

## Troubleshooting

### ChangeData Writes Null Values

**Symptom:** After ChangeData executes, columns are null instead of the expected values.

**Known Issue:** Creatio 8.3.2.4199 has a bug where ChangeData visual elements produce null for some column types.

**Fix:** Replace the ChangeData element with a **Script Task** that writes via EntitySchemaQuery:

```csharp
// Example Script Task replacement for ChangeData_WriteDone
var esq = new EntitySchemaQuery(UserConnection.EntitySchemaManager, "IWPayments");
esq.PrimaryQueryColumn.IsAlwaysSelect = true;
var entity = esq.GetEntity(UserConnection, Get<Guid>("ReadPayment.Id"));
if (entity != null) {
    entity.SetColumnValue("IWCommissionStatusId", new Guid("deb80242-b56a-4b94-967a-0e170e2198d8"));
    entity.SetColumnValue("IWCommissionAmount", Get<decimal>("CommissionAmount"));
    entity.SetColumnValue("IWSalesAmount", Get<decimal>("CalculatedSalesAmount"));
    entity.SetColumnValue("IWCommissionCalculated", true);
    entity.SetColumnValue("IWIsReturn", false);
    entity.SetColumnValue("IWOwnerId", Get<Guid>("ReadOrder.OwnerId"));
    entity.SetColumnValue("IWBGTransactionTypeId", new Guid("b4494f26-26c2-4aa6-951c-658d0828d0d0"));
    entity.SetColumnValue("IWSalesGroupId", Get<Guid>("ReadSalesGroup.Id"));
    entity.SetColumnValue("IWBGSalesRepId", Get<Guid>("ReadOrder.BGSalesRepLookupId"));
    entity.SetColumnValue("IWBGYearMonthId", Get<Guid>("ReadYearMonth.Id"));
    entity.SetColumnValue("IWDescription", Get<string>("ReadOrder.BGOrderDescription"));
    entity.Save();
}
return true;
```

### Signals Not Firing

**Symptom:** Process never executes after data changes.

**Checks:**
1. Did you **Publish** (not just Compile All)?
2. Is the process set as **Actual version**?
3. Is the process **Enabled**?
4. Check `VwSysProcess` for `NeedUpdateSourceCode` = false

```bash
source .env && python3 scripts/diagnostics/test_v6_process.py --check-only
```

### Formula Errors

**Symptom:** Process errors at a Formula element.

**Common causes:**
- Division by zero: `ReadOrder.Amount` is 0 → add the OrderTotalCheck gateway before formulas
- Null reference: `ReadPayment.IWPaymentDue` is null → add a null check or ensure payments always have a due date
- DateTime format: `ToString("yyyy-MM")` may not work in all formula contexts → use Script Task fallback

### Recursion / Excessive Executions

**Symptom:** Process log shows hundreds of V6 executions for one change.

**Checks:**
1. Signal #2 (PaymentStatusChanged) must filter on `IWCommissionStatus` ONLY
2. BounceCheck gateway must terminate on all final statuses (Done, Returned, Error, Order Deleted)
3. V6 must NOT write to Order or OrderProduct entities

### Process Takes Too Long

**Symptom:** Commission calculation takes >30 seconds.

**Likely cause:** Multiple payments for one order each trigger separate Path A executions. This is by design — each payment is calculated independently.

If performance is an issue, consider batching with a Script Task that processes all payments for an order in a single execution.

---

## Element Count Summary

| Category | Elements | Count |
|----------|----------|-------|
| Signals | PaymentAdded, PaymentStatusChanged, OrderAdded, OrderModified, OrderDeleted, OrderProductAdded, OrderProductModified, OrderProductDeleted | 8 |
| ReadData | ReadPayment, ReadOrder, ReadEmployee, ReadSalesGroup, ReadYearMonth, ReadCommissionRate, ReadOrderProduct | 7 |
| ChangeData | ChangeData_SetPending, ChangeData_SetPending2, ChangeData_SetOrderDeleted, ChangeData_SetError, ChangeData_WriteDone, ChangeData_WriteReturned | 6 |
| Gateways | BounceCheck, OrderTotalCheck, HasRateCheck, CheckSign | 4 |
| Formulas | Formula_YearMonth, SetCommissionRate, Formula_CalcSalesAmount, Formula_CalcCommission | 4 |
| Terminators | Terminate_B1, Terminate_B2, Terminate_C, Terminate_Bounce, Terminate_Error, Terminate_Done, Terminate_Returned | 7 |
| **Total** | | **36** |

---

## Rollback Plan

If V6 has issues after deployment:

1. **Disable V6:** Open Process Designer → set Active = No
2. **Re-enable old processes:**
   - Set `IWCalculateCommissiononPaymentV4` (or V5) as Actual version
   - Set `IWFillCommissionReportPaymentsFieldsV2` as Actual version
   - Set `IWRecalculateCommissionOnOrderChangeV2` as Actual version
3. **Publish** each re-enabled process to re-register their signals

---

## Quick Reference Card

### Lookup GUIDs (Copy-Paste Ready)

```
Commission Status:
  Pending:       930bb1c6-ca67-4ac0-8f96-a5ea4018a366
  Done:          deb80242-b56a-4b94-967a-0e170e2198d8
  Returned:      ee14b2ce-163a-4fb2-abea-e739636794ed
  Error:         26c1b9de-75c9-46c7-8963-e02b8a63f261
  Order Deleted: 8c2313f4-7e27-4781-afef-d16deb90cc6d

Transaction Type:
  Sale:          b4494f26-26c2-4aa6-951c-658d0828d0d0
  Credit Memo:   c26d3478-7ac1-49e9-97f9-1c0809552f1f
```

### Key Column Names

```
IWPayments WRITE columns:
  IWCommissionAmount, IWSalesAmount, IWCommissionCalculated,
  IWCommissionStatusId, IWOwnerId, IWIsReturn, IWDescription,
  IWSalesGroupId, IWBGSalesRepId, IWBGTransactionTypeId, IWBGYearMonthId

IWPayments READ columns:
  IWAmount, IWPaymentDue, IWPaymentsInvoiceId, IWCommissionStatusId

Order READ columns:
  Amount, BGTaxAmount, BGSubTotal, BGShippingCharge,
  BGSalesRepLookupId, BGSalesGroupId, OwnerId, BGOrderDescription
```
