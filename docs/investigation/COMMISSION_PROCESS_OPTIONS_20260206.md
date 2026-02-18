# Commission Process Architecture Options — 2026-02-06

> **Context:** All 6 IW commission processes have NEVER been Published. Zero executions in process log ever.
> **Decision needed:** How to restructure before Publishing.
> **Related:** `COMMISSION_PROCESS_AUDIT_20260205.md`, `v3_restructure_steps_labeled.md`

---

## Current State (API-Verified 2026-02-06)

### 6 Processes, 3 Actual

| Process | Full Name | Actual | Signals | Writes To | Metadata |
|---------|-----------|--------|---------|-----------|----------|
| **V4** | IWCalculateCommissiononPaymentV4 | YES | 2 (IWPayments Added, Deleted) | IWPayments (4 tasks) | 207K |
| **Fill V2** | IWFillCommissionReportPaymentsFieldsV2 | YES | 3 (IWPayments Modified, Added, Deleted) | IWPayments (4 tasks) | 286K |
| **Order Recalc V2** | IWRecalculateCommissionOnOrderChangeV2 | YES | 3 (Order Modified[5col], Added, Deleted) | IWPayments (2 tasks) | 143K |
| V1 | IWCalculateCommissiononPayment | no | 3 (IWPayments Mod[2col], Added, Deleted) | IWPayments | 162K |
| Fill V1 | IWFillCommissionReportPaymentsFields | no | 3 (IWPayments Modified, Added, Deleted) | IWPayments | 75K |
| Order Recalc V1 | IWRecalculateCommissionOnOrderChange | no | 3 (Order signals) | none (empty shell) | 15K |

### Architecture Clarification

These are **3 independent business processes**, NOT subprocesses. None calls another. Each listens for its own entity signals and runs autonomously.

```
ORDER entity changes ──→ Order Recalc V2 (sets IWCommissionStatus = Pending)
IWPayments Added     ──→ V4 (calculates commission) + Fill V2 (fills report fields)
IWPayments Deleted   ──→ V4 (handles deletion)      + Fill V2 (handles deletion)
IWPayments Modified  ──→ Fill V2 ONLY (unfiltered!)
```

### Signal Inventory (Confirmed via API)

| Process | Signal | Entity | Type | Filter | FC2 Entity UId |
|---------|--------|--------|------|--------|----------------|
| V4 | StartSignal2 | IWPayments | Added | none | e1169637-8d6e-48d6-a129-0362fbdb7f65 |
| V4 | StartSignal3 | IWPayments | Deleted | none | e1169637-8d6e-48d6-a129-0362fbdb7f65 |
| Fill V2 | StartSignal1 | IWPayments | **Modified** | **NONE (any field!)** | e1169637-8d6e-48d6-a129-0362fbdb7f65 |
| Fill V2 | StartSignal2 | IWPayments | Added | none | e1169637-8d6e-48d6-a129-0362fbdb7f65 |
| Fill V2 | StartSignal3 | IWPayments | Deleted | none | e1169637-8d6e-48d6-a129-0362fbdb7f65 |
| Order Recalc V2 | StartSignal1 | Order | Modified | 5 columns | 80294582-06b5-4faa-a85f-3323e5536b71 |
| Order Recalc V2 | StartSignal2 | Order | Added | none | 80294582-06b5-4faa-a85f-3323e5536b71 |
| Order Recalc V2 | StartSignal3 | Order | Deleted | none | 80294582-06b5-4faa-a85f-3323e5536b71 |

### Write Targets (BK15 EntitySchemaUId Mappings)

| Process | ChangeData Task | Target Entity |
|---------|----------------|---------------|
| Fill V2 | ChangeDataUserTask1 | IWPayments (e1169637...) |
| Fill V2 | ChangeDataUserTask2 | IWPayments (e1169637...) |
| Fill V2 | ChangeDataUserTask3 | IWPayments (e1169637...) |
| Fill V2 | ChangeDataUserTask4 | IWPayments (e1169637...) |
| V4 | ChangeDataUserTask1 | IWPayments |
| V4 | ChangeDataUserTask3 | IWPayments |
| V4 | ChangeDataUserTask4 | IWPayments |
| V4 | ChangeDataUserTask6 | IWPayments |
| Order Recalc V2 | ChangeDataUserTask1 | IWPayments |
| Order Recalc V2 | ChangeDataUserTask2 | IWPayments |

**ALL processes write to IWPayments.** This is the core of every recursion/cascade issue.

### Corrections from Previous Audit

| Previous Finding | Correction |
|-----------------|------------|
| Fill V2 has Order signal (StartSignal4) | **WRONG** — Fill V2 only monitors IWPayments (3 signals) |
| V4 has "Payment Modified" signal | **ALREADY REMOVED** — V4 only has Added + Deleted |
| "Subprocess V2" terminology | **INCORRECT** — Order Recalc V2 is an independent process |

---

## Critical Danger: Fill V2 Self-Recursion

Fill V2 monitors IWPayments Modified (unfiltered) AND writes 4 columns back to IWPayments:

```
ANY write to IWPayments
  → Fill V2 fires (Modified signal, no filter)
  → Fill V2 writes 4 columns to IWPayments
  → IWPayments Modified fires again
  → Fill V2 fires again
  → INFINITE LOOP
```

This also creates cascade from other processes:
- V4 writes IWPayments → triggers Fill V2 → Fill V2 self-recurses
- Order Recalc V2 sets Pending on IWPayments → triggers Fill V2 → Fill V2 self-recurses

**Fill V2 CANNOT be Published as-is.**

---

## Options

### Option A: Minimal Fix (Patch and Publish)

**What:** Remove Fill V2's Modified signal (StartSignal1). Keep Added + Deleted. Publish all 3 processes.

| Pros | Cons |
|------|------|
| Least amount of changes | Fill V2 won't run when V4 updates existing payments |
| Keeps separation of concerns | Report fields only filled on payment creation, not recalculation |
| Quick to implement | Still 3 processes to manage and reason about |
| | When Order Recalc sets Pending + V4 recalculates, Fill V2 won't update report fields |

**Effort:** Low (remove 1 signal, publish 3 processes)

**Gap:** After V4 recalculates an existing payment's commission (e.g., order total changed), Fill V2 won't fire to update report fields like SalesRep, SalesGroup, etc. These fields are typically static per payment, so this may be acceptable.

---

### Option B: Merge Fill V2 into V4 ★ RECOMMENDED

**What:** Add Fill V2's report-field logic (4 ChangeData tasks + supporting reads) into V4's flow, after the calculation step. Delete or disable Fill V2.

| Pros | Cons |
|------|------|
| Eliminates ALL cross-process IWPayments trigger issues | V4 becomes a larger process |
| Down to 2 processes total | Need to recreate Fill V2's read/write logic in V4 |
| Report fields always up-to-date after every calculation | More elements on V4's designer canvas |
| One atomic operation: calculate + fill | |
| Fewer things to Publish and maintain | |

**Effort:** Medium (rebuild ~10 UserTasks + 4 ChangeData tasks in V4)

**Result:** 2 processes:
- V4: Payment Added/Deleted → calculate commission → fill report fields
- Order Recalc V2: Order Modified/Added/Deleted → set Pending → (needs Option A bridge to invoke V4)

---

### Option C: Make Fill V2 a Called Process (No Signals)

**What:** Remove ALL 3 signals from Fill V2. Add a Script Task to V4 that explicitly invokes Fill V2 via `ProcessEngineService` after calculation completes.

| Pros | Cons |
|------|------|
| Clean separation: V4 calculates, Fill V2 fills | Still 3 processes to manage |
| No signal-based triggers between them | Requires Script Task in V4 |
| Fill V2 only runs when intentionally called | Fill V2 still needs Publishing (even signal-less) |
| Keeps process designer canvases simpler | Adds ProcessEngineService dependency |

**Effort:** Medium (remove 3 signals, add Script Task to V4, add input parameter to Fill V2)

**Result:** 3 processes, but Fill V2 is controlled:
- V4: Payment Added/Deleted → calculate → call Fill V2
- Fill V2: No signals, only runs when V4 invokes it
- Order Recalc V2: Order signals → set Pending → (needs bridge to invoke V4)

---

### Option D: Combine Everything into One Process

**What:** Single process handles Order signals + Payment signals + calculation + report filling.

| Pros | Cons |
|------|------|
| Single process, single point of control | Very complex designer canvas |
| No cross-process issues at all | Multiple entity signals in one process is fragile in Creatio |
| Easiest to reason about data flow | Harder to debug individual failures |
| | If one part fails, entire process fails |
| | Creatio may have limitations on mixed-entity signals |

**Effort:** High (rebuild from scratch)

**Result:** 1 process handles everything.

---

### Option E: Delete Everything, Start Fresh

**What:** Disable/delete all 6 existing processes. Build 2 clean processes from scratch with current knowledge.

| Pros | Cons |
|------|------|
| Clean slate, no accumulated design debt | Significant effort |
| Design with full understanding of pitfalls | Risk of introducing new bugs |
| Can use modern patterns from the start | Lose tested V4 calculation logic |
| Document everything from day 1 | |

**Effort:** High

**Result:** 2 clean processes designed correctly from the start.

---

## Comparison Matrix

| Criteria | A: Patch | B: Merge ★ | C: Called | D: Combine | E: Fresh |
|----------|----------|-----------|----------|-----------|---------|
| **Effort** | Low | Medium | Medium | High | High |
| **Risk** | Medium | Low | Low | Medium | Medium |
| **Processes after** | 3 | 2 | 3 | 1 | 2 |
| **Recursion risk** | Low | None | None | None | None |
| **Report fields current** | Partial | Always | Always | Always | Always |
| **Maintainability** | Fair | Good | Good | Poor | Best |
| **Bridge needed** | Yes | Yes | Yes | No | Yes |

("Bridge" = Script Task in Order Recalc V2 to invoke V4 when order changes)

---

## Legacy Processes (V1 Versions)

Regardless of which option is chosen:

| Process | Recommendation | Reason |
|---------|---------------|--------|
| V1 (Payment Calculator) | Disable | Not Actual, superseded by V4 |
| Fill V1 (Report Fields) | Disable | Not Actual, superseded by Fill V2 |
| Order Recalc V1 | Disable | Not Actual, empty shell (0 data tasks) |

These add confusion and could be accidentally activated. Disabling (not deleting) preserves them as reference.

---

## Process UIds (Reference)

| Process | UId |
|---------|-----|
| V4 | dede2ffb-ed56-4a25-b0e1-8d87b43d5448 |
| Fill V2 | 0f3a6403-5d0e-43c0-81a4-45d94b4364b8 |
| Order Recalc V2 | 3c425afe-3ee8-4d38-baf2-a30de552bd94 |
| V1 | c2623b8a-338e-4adb-afbe-cb76b68368d9 |
| Fill V1 | d814f639-4d62-4dad-b954-128fd621f169 |
| Order Recalc V1 | 04e376c2-3452-4786-88d9-faf096c98ec6 |

---

## Decision Log

| Date | Decision | Chosen Option | Rationale |
|------|----------|---------------|-----------|
| 2026-02-06 | Options documented | PENDING | Awaiting team decision |
| 2026-02-10 | **Option B selected** | **B: Merge Fill V2 into V4** | Single writer pattern on IWPayments, atomic calc+fill, 2 processes instead of 3, future-proof against other automations |
