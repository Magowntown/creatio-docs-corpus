# Repository Guidelines

## Project Structure & Module Organization
Working archive for Creatio report fixes with versioned artifacts.
- `client-module/` Freedom UI handlers (JS); deployed file list in `client-module/README.md`.
- `source-code/` Backend services (C#); deployed service + endpoints in `source-code/README.md`.
- `docs/` Investigation notes, logs, and reference docs.
- `scripts/` Python/SQL utilities for testing, investigation, deployment.
- `sql/`, `vba/`, `test-artifacts/` assets and outputs.
- `creatio-docs-*` documentation snapshots; `*.zip` package exports.

## Build, Test, and Development Commands
No single build step; work is script-driven against Creatio.
- `source .env` loads credentials and base URLs.
- `python3 scripts/testing/test_report_service.py` end-to-end report generation + download.
- `python3 scripts/investigation/review_report_flow.py --env dev` summarizes DEV report flow.

## Coding Style & Naming Conventions
- Indentation: 4 spaces, matching existing JS/C# files.
- Client handler files follow package + schema prefixes, e.g. `BGApp_eykaguu_UsrPage_ebkv9e8_*` (child schema) and `BGlobalLookerStudio_*` (parent schema).
- Backend services are versioned as `UsrExcelReportService_*.cs`.
- Preserve existing file naming and version suffixes instead of renaming in place.

## Testing Guidelines
- Primary checks are `scripts/testing/test_*.py`; most use `requests` and some use `openpyxl`.
- Use DEV by default unless a script explicitly targets PROD.
- Record meaningful results in `docs/TEST_LOG.md` when status changes.

## Commit & Pull Request Guidelines
- Use short, descriptive summaries (e.g., “New handler…”, “Add … investigation”).
- PRs should include summary, environment tested (DEV/PROD), and doc/log references.
- If status changes, update `CLAUDE.md` and relevant `docs/`.

## Security & Configuration Tips
- Credentials live in `.env` and must not be committed.
- Prefer DEV endpoints for testing unless explicitly instructed.
- Redact customer data in logs or screenshots before sharing.

## Parallel Orchestration
All three CLIs may edit in parallel; avoid conflicts via coordination, not lockfiles.
- Default split: Claude Opus (investigation + planning), Codex (implementation + tests), Gemini (review + regression analysis).
- Preflight before edits: check `git status`, scan `docs/logs/SESSION_LOG_*.md`, and call out target files in chat.
- Handoff format (post in chat): “Changed: `<file>`… Verified: `<how>`… Next: `<action>`.”

## Readiness & Blockers
- Only current local change should be `AGENTS.md`; keep worktrees clean before edits.
- `client-module/` and `source-code/` contain many legacy files; confirm the deployed target in their respective `README.md` files before editing.
- `scripts/testing/` is ready for use; most scripts expect `.env` and `requests` (some optional `openpyxl`).

## Agent Notes
- Start with `CLAUDE.md` for current status and navigation.
- Use `docs/AI_NAVIGATION.md` and `docs/DOCUMENT_INDEX.md` to locate related materials.
