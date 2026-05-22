# Session Log: 2026-05-21 — graphify setup + paused extract

**Topic:** Install [safishamsi/graphify](https://github.com/safishamsi/graphify) knowledge-graph tool across `~/creatio-hub/` (WSL) + `C:\Creatio` (Windows).
**Outcome:** Tooling installed and configured. Hub extract paused mid-semantic-phase before significant token spend. Windows extract not started.

## What got done

| Item | Status |
|------|--------|
| `graphifyy 0.8.14` installed via `uv tool install` (Python 3.12, extras: pdf/office/sql/video/gemini/mcp/svg) | ✅ |
| `graphify` skill registered at `~/.claude/skills/graphify/SKILL.md` | ✅ |
| `.graphifyignore` curated for `~/creatio-hub/` (excludes 5+ vendor doc dirs, IDE plugins, `runtime/` symlink, package zips, `client-module/` BGApp experiments, `media/` Academy icons — 12,222 noise images) | ✅ |
| `.graphifyignore` curated for `/mnt/c/Creatio/` (excludes IIS runtime dirs `D1/D2/D3`, installer drop, `_orphaned`, venvs) | ✅ |
| Backend decision: **`claude-cli`** (routes through local Claude Code Pro/Max — `$0` cost per `graphify/llm.py:108-117`) | ✅ |
| Hub extract started, AST phase completed (cache preserved at `graphify-out/cache/`), semantic phase running | ⏸️ PAUSED |
| Windows `/mnt/c/Creatio` extract | ⏳ Not started |
| `graphify claude install` to wire graph into Claude Code | ⏳ After extract completes |
| Vendor corpus run (11,755 Academy pages, etc.) | ⏳ Deferred (covered by 211K Gemini embeddings) |

## Key decisions

1. **Backend = `claude-cli`, not gemini or claude API.** First scan with Gemini produced 21,065 semantic chunks → cost estimate $60-200. User: *"ensure gemini does not make us spend money."* Discovered `claude-cli` backend in source has explicit `{"input": 0.0, "output": 0.0}` pricing — uses the existing subscription.
2. **Curated scope first, vendor corpus later.** User: *"go with 1. but keep in mind we still want the full vendor corpus which we will aim to do later."* Vendor docs already vector-searchable via existing ChromaDB embeddings — graphify's structural value is low for isolated doc pages with no cross-document architecture.
3. **Paused before the spend hit.** User: *"pause for now we are about to spend our tokens."* Killed graphify main process (PID 31873), lingering `claude -p` subprocess (PID 56965), monitor tail processes. AST cache preserved → resume is a single command.

## Resume command

```bash
graphify extract ~/creatio-hub \
  --backend claude-cli \
  --global --as creatio-hub \
  --max-concurrency 2
# AST cache reused; only semantic phase re-runs.
```

## Lesson codified

Don't `cat` full log files in diagnostics — at the AST-progress scale, the `graphify-hub.log` dump was ~15K characters of repeated "AST extraction: N/M files" lines and contributed materially to the 680k-token context spike that prompted the pause. Use `head/tail/wc -l + sample` instead. Saved as feedback memory.

## Context spike root-cause notes

Diagnosed the 680k-token session size when user asked. Top contributors:
- System-reminder skill-catalog re-injections (~120k cumulative across turns)
- Conversation history (~150-200k)
- One `cat graphify-hub.log` diagnostic (~10k, avoidable)
- Tool schemas loaded via ToolSearch (Monitor/TaskCreate/etc., ~12k)
- MCP server instructions block at session start (~20k)
- CLAUDE.md files + MEMORY.md + cited memory files (~25k)

## Related
- Memory: `~/.claude/projects/-home-magown-creatio-hub/memory/project_graphify_setup.md`
- Memory: `~/.claude/projects/-home-magown-creatio-hub/memory/feedback_diagnostic_log_dump_cost.md`

---

# Session Log: 2026-05-21 (PM) — Pampa Bay IWReady4QB race fix + bulk-load morning

**Topic:** Ship the Ready4QB race fix to `pampabay` PROD, backfill the stranded TRs, respond to Alex's bulk-load progress, audit catch-up scope.

**Outcome:** Race fix deployed. 174 stranded TRs flipped to Ready4QB=true with ModifiedOn bumped. Alex executed a manual file-based bulk load (213 invoices, 16 POs) into QB **outside the integration flow**. Outbound integration flow `Creatio2QBCustInvoice` auto-throttled to 1-4hr intervals after Noella exclusive-mode interruption — **race fix is still untested under real outbound load**.

## Timeline (ET)

| Time | Event | Source |
|---|---|---|
| **06:21** | Scheduled `Creatio2QBCustInvoice` flow tried to fire; immediately got `XmlSql.go Connection Failed` (Initial == Final query time, zero records processed) | `iwn_alert22@interweave.biz` alert |
| **08:19** | Connection Failed alert auto-fired to Danlyn | Alert |
| **08:20** | Andrew sent interim email "There should be around 174 Transactions now" | Sent Items |
| **08:24** | Dmytro reply: "174 with IWReady4QB checked? Or total loaded since 05/02?" | Inbox |
| **08:33** | Dmytro to Alex: "Check with Danlyn if we need to load Payments from Creatio to QB first or just start scheduled flows and load payments tonight." | Inbox |
| **10:48** | Alex emailed "Server - Data errors" (HIGH) — recurring data errors including `CreatioObj2QBPON` (>11-char PO numbers, QODBC 3070) | Inbox |
| **11:22** | Alex emailed "Server - Bulk loads" — **213 invoices loaded** (#68503-69422), **16 POs loaded**, asking about Payment Receipts | Inbox |
| **11:27** | Alex forwarded Connection Error to Danlyn + CC (Andrew, Dmytro, Bruce) — root cause "QB user Noella switched QB file into exclusive use mode mid-flow" | Inbox |

## Code shipped today (`IWInterWeavePaymentApp` package)

### 1. `IWTransactionReady4QBListener.cs` — refactored to DB-read pattern
- Replaced `txn.GetTypedColumnValue<Guid>("IWTROrderId")` with `new Select(uc).Column("IWTROrderId").From("IWTransactions")...`
- Added contract comment: any raw `Update().Execute()` writer must call `EvaluateById` after.
- New `internal static EvaluateById(UserConnection, Guid)` exposes the gate for AutoPair to call.

### 2. `IWTransactionAutoPairListener.cs` — explicit Ready4QB.EvaluateById call
- After `new Update("IWTransactions").Set("IWTROrderId", ...).Execute()`, now calls `IWTransactionReady4QBListener.EvaluateById(txn.UserConnection, txnId)`.
- Updated doc-comment: removed stale "Amount verification" wording; now reflects PO-only strict-single-match policy from 2026-05-06 Dmytro directive.

### 3. Descriptor bumps (avoids push-pkg silent no-op per feedback memory)
All three `ModifiedOnUtc` bumped to `1779364161768`:
- `IWInterWeavePaymentApp/descriptor.json`
- `IWInterWeavePaymentApp/Schemas/IWTransactionReady4QBListener/descriptor.json`
- `IWInterWeavePaymentApp/Schemas/IWTransactionAutoPairListener/descriptor.json`

### Deploy sequence
1. `clio push-pkg IWInterWeavePaymentApp -e dev-pampabay` → smoke-tested
2. `clio push-pkg IWInterWeavePaymentApp -e pampabay` → PROD
3. Backfill UPDATE on the 174 stranded TRs (settled + paired + Order.BGHasInvoice=true + IWReady4QB=false)
4. Second UPDATE bumping ModifiedOn=NOW on the same 174 rows (raw SQL doesn't auto-bump; outbound flow needs ModifiedOn > watermark)

## PROD verification queries

### Backfill audit
- `still_stranded = 0`
- `total_ready = 174`

### Catch-up audit since 2026-05-02
- **Total: 366** IWTransactions
- 283 settled / 83 non-settled
- **164** ready + paired + Order.BGHasInvoice=true → push-eligible (covered by backfill)
- **18** paired + Order.BGHasInvoice=false → architectural-sequel bucket
- **101** settled but unpaired → strict single-match + data issues
- **0** already pushed (`IWQBLastModified > '2026-01-01'`)
- Reconciles: 283 settled = 164 + 18 + 101 + 0 ✓

### Today's push-back validation
- `IWQBLastModified > '2026-05-21 00:00:00'` count = **0** (MIN, MAX = NULL)
- **Interpretation:** Alex's "213 invoices loaded" did NOT touch IWQBLastModified because it was a manual file-based load directly into QB, not an integration flow retry. Race fix is **unverified** under real outbound load.

## Alex's bulk-load mechanics (clarified)
Alex's email phrasing — "All 213 invoices have been loaded into QB **per the file you sent**" — confirms QODBC-direct write from a CSV Danlyn sent. This path:
- ✅ Updates QB-side data
- ❌ Does NOT call the InterWeave middleware
- ❌ Does NOT touch Creatio columns (IWQBLastModified, IWQBPayment, etc.)
- ❌ Does NOT create IWPayment writeback records in Creatio

So QB has 213 net-new invoices; Creatio has 174 TRs ready to push; next scheduled outbound run (throttled ~4hr) is the moment of truth.

## Connection Error / Noella incident (operational reference)
- Alert format `iwn_alert22@interweave.biz` documented as canonical telemetry.
- Auto-throttle window: **1 to 4 hours** if current interval is shorter.
- Saved as new reference memory: `reference_pampabay_qb_flow_autothrottle.md`.

## Outstanding from today
1. **Verify race fix under real load** — when throttled outbound flow next fires (~4hr cadence), check `IWQBLastModified > 2026-05-21` count.
2. **Send refined reply to Dmytro** — acknowledge 174 vs 213 distinction (Creatio flag vs QB file-load).
3. **Reply Bruce with curated >11-char PO list** — extract from Alex's "Server - Data errors" email today.
4. **Architectural sequel** — Order.BGHasInvoice → IWTransactions.Ready4QB re-evaluation listener (closes 18-record bucket).
5. **IWQBSyncReady rules table** — still owed to Dmytro from 5/12 20:17 ET (9-day silence).

## Memory updates this session
- **Project**: `project_pampabay_qb_export_issues.md` — prepended 2026-05-21 section.
- **Feedback (extended)**: `feedback_creatio_iwqblastmodified_filter_pitfall.md` — added writeback-signal addendum.
- **Reference (new)**: `reference_pampabay_qb_flow_autothrottle.md`.
- **MEMORY.md index** — updated project line + added new reference.

## Files touched
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWInterWeavePaymentApp/Schemas/IWTransactionReady4QBListener/IWTransactionReady4QBListener.cs`
- `/mnt/c/Creatio/creatio-dev-agent/packages/IWInterWeavePaymentApp/Schemas/IWTransactionAutoPairListener/IWTransactionAutoPairListener.cs`
- 3 × `descriptor.json` (parent package + 2 schemas)
- `/mnt/c/Creatio/creatio-dev-agent/agent-query-todays-pushes.bat` (new query helper)
- `/mnt/c/Creatio/creatio-dev-agent/agent-query-todays-totals.bat` (new query helper)
