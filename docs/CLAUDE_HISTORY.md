# CLAUDE_HISTORY.md - Change Log & Archived Context

> Historical record. For current status, see `CLAUDE.md`.

---

## Change Log

| Date | Change | AI |
|------|--------|-----|
| 2026-01-08 | Initial investigation, root cause documented | Claude |
| 2026-01-09 | Commission & IW filters fixed via FiltersConfig | Claude |
| 2026-01-09 | Handler updated to window.open() approach | Claude |
| 2026-01-09 | Handler updated to hidden iframe approach | Claude |
| 2026-01-09 | TDD methodology added, TEST_LOG.md created | Claude |
| 2026-01-09 | Documentation restructured for AI workflow | Claude |
| 2026-01-09 | **Gate A PASSED** - API baseline verified | Claude Code |
| 2026-01-09 | **Gate B PASSED** - Runtime verification | Claude Code |
| 2026-01-09 | **Gate C PASSED** - DL-001 browser download | Claude Code |
| 2026-01-09 | Added Boris Cherny's Claude Code best practices | Claude Code |
| 2026-01-10 | **Gate D PASSED** - Dynamic filter sweep (3 combos) | Claude Code |
| 2026-01-12 | **Gate C2 PASSED** - DL-003 fix (.xlsm downloads) | Claude Code |
| 2026-01-12 | **FUT-001 documented** - Pre-calculated .xlsx requirement | Claude Code |
| 2026-01-12 | **FLT-004 identified** - Empty data root cause | Claude Code |
| 2026-01-12 | **FLT-004 BLOCKED** - Workspace compile errors | Claude Code |
| 2026-01-12 | Mandatory documentation update requirement added | Claude Code |
| 2026-01-13 | **ENV-001 NOT REPRODUCIBLE** - Re-tested | Warp |
| 2026-01-13 | **FLT-004 re-tested** - GUID detection fix needed | Warp |
| 2026-01-13 | Documentation reconciled - Section 8 fixed | Claude Code |
| 2026-01-13 | **CLAUDE.md restructured** - Split into slim core + reference files | Claude Code |
| 2026-01-14 | **IWQBIntegration package** recreated in DEV | User |
| 2026-01-14 | **FLT-002 RESOLVED** - IW_Commission filters working | Claude Code |
| 2026-01-14 | **V4 process error** identified - gateway type mismatch | Claude Code |
| 2026-01-15 | **PROD view missing** - BGCommissionReportDataView not created | Claude Code |
| 2026-01-15 | **DATA-001 identified** - PaymentStatusId=Planned blocks QB sync | Claude Code |
| 2026-01-15 | **SYNC-001 CRITICAL** - QB sync stuck since Aug 2025 | Claude Code |
| 2026-01-15 | **Root cause found** - Process waiting for manual date input | Claude Code |
| 2026-01-15 | DataService vs OData discovery - DataService more reliable | Claude Code |
| 2026-01-15 | Full documentation update - all docs synchronized | Claude Code |
| 2026-01-15 | **SYNC-001 RESOLVED** - Manual sync completed (8,428 records) | User + Claude Code |
| 2026-01-15 | **QB_SYNC_AUTOMATION.md** created - Process automation guide | Claude Code |
| 2026-01-15 | **Phase 1 automation deployed** - Simplified 30-day script working | Claude Code |
| 2026-01-15 | **Verification complete** - 2 records synced via automated process | Claude Code |
| 2026-01-15 | **Dec 2025 data analyzed** - 0 Sales, 39 Credit Memos only | Claude Code |
| 2026-01-15 | **DATA-002 identified** - QB data entry issue (no Dec Sales) | Claude Code |
| 2026-01-15 | **Client correlation confirmed** - "Returns but not Sales" matches data | Claude Code |
| 2026-01-15 | Full documentation update - all docs synchronized | Claude Code |
| 2026-01-15 | **Data flow investigation** - Traced Orders → QB Invoices → ReceivePayments | Claude Code |
| 2026-01-15 | **Dec 2025 orders found** - 20+ orders exist with BGQuickBooksId (synced to QB) | Claude Code |
| 2026-01-15 | **BGQuickBooksService.cs analyzed** - Confirmed ReceivePayment vs Invoice query logic | Claude Code |
| 2026-01-15 | **DATA-002 root cause confirmed** - Dec invoices in QB awaiting payment processing | Claude Code |
| 2026-01-15 | **API discovery** - OData more reliable than DataService for large tables | Claude Code |
| 2026-01-15 | Full documentation update - TEST_LOG, CLAUDE_REFERENCE, CLAUDE_HISTORY | Claude Code |

---

## Archived Context

### Multi-AI Collaboration (Reference)

| Task | Claude Code | ChatGPT | Gemini |
|------|-------------|---------|--------|
| Code editing | ✅ Primary | ❌ | ❌ |
| API testing | ✅ Primary | ❌ | ❌ |
| Long browser waits | ❌ Timeout | ✅ Primary | ❌ |
| Code review | ✅ Good | ✅ Good | ✅ Best |

### Gate Definitions (Full)

1. **Gate A** - API baseline: `test_report_service.py` passes
2. **Gate B** - Runtime verification: `reportDownloadFrame` marker found
3. **Gate C** - DL-001 browser download: .xlsx downloads successfully
4. **Gate C2** - DL-003 durability: .xlsm served for macro-enabled files
5. **Gate D** - Dynamic filter sweep: 3 combos validated
6. **Gate E** - Regression testing: other reports work
7. **Gate F** - Hardening: edge cases, error messages
8. **Gate G** - PROD upgrade checklist

### FUT-001: Pre-calculated .xlsx (Future)

**Goal:** Execute VBA macros server-side, serve plain .xlsx.

**Approaches:**
1. Headless Excel automation (LibreOffice, Excel Interop)
2. Convert VBA logic to C#
3. Rebuild workbook with EPPlus/ClosedXML

---

## Claude Code Best Practices (Boris Cherny)

> Archived from original CLAUDE.md Section 0

### Key Points

1. **Run multiple Claudes in parallel** - Local tabs + web sessions
2. **Start in Plan mode** (Shift+Tab twice)
3. **Use Opus 4.5 with thinking**
4. **Create slash commands** for repeated workflows
5. **Use hooks** for automation (PostToolUse, Stop)
6. **Give Claude verification tools** - This 2-3x quality

### Verification for This Project

```bash
# API Level
python3 scripts/testing/test_report_service.py

# Browser Level
python3 scripts/investigation/review_report_flow.py --env dev

# Handler Deployment
# Search for 'reportDownloadFrame' in compiled JS
```

---

## TDD Cycle (Reference)

```
1. ISSUE → 2. TEST PLAN → 3. SOLUTION → 4. VERIFY → 5. LOG → 6. UPDATE DOCS
```

Before any code change:
1. What test proves this is broken?
2. What test proves this is fixed?
3. How will I verify?
4. Where will I log results? (`docs/TEST_LOG.md`)
