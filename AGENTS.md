# Repository Guidelines

## Project Structure & Module Organization
This repo is a working archive for Creatio report fixes, with versioned artifacts and supporting docs.
- `client-module/` Freedom UI client handlers (JS). See `client-module/README.md` for the deployed file list.
- `source-code/` Backend services (C#). See `source-code/README.md` for the deployed service and endpoints.
- `docs/` Investigation notes, logs, and reference docs.
- `scripts/` Python/SQL utilities for testing, investigation, and deployment helpers.
- `sql/` and `vba/` Database queries and Excel macro sources.
- `creatio-docs-*` Crawled Creatio documentation snapshots.
- `test-artifacts/` Downloads and verification outputs.
- `*.zip` Exported Creatio packages (historical snapshots).

## Build, Test, and Development Commands
There is no single build step; work is script-driven and typically targets a Creatio environment.
- `source .env` loads credentials and base URLs for scripts.
- `python3 scripts/testing/test_report_service.py` runs an end-to-end report generation + download check and writes to `test-artifacts/`.
- `python3 scripts/investigation/review_report_flow.py --env dev` summarizes the current report flow in DEV.
- Additional scripts follow the same pattern under `scripts/testing/` and `scripts/investigation/`.

## Coding Style & Naming Conventions
- Indentation: 4 spaces, matching existing JS/C# files.
- Client handler files follow package + schema prefixes, e.g. `BGApp_eykaguu_UsrPage_ebkv9e8_*` (child schema) and `BGlobalLookerStudio_*` (parent schema).
- Backend services are versioned as `UsrExcelReportService_*.cs`.
- Preserve existing file naming and version suffixes instead of renaming in place.

## Testing Guidelines
- Primary checks are Python scripts in `scripts/testing/` named `test_*.py`.
- Most scripts require `requests`; some optionally use `openpyxl` for workbook inspection.
- Use DEV by default unless a script explicitly targets PROD.
- Record meaningful results in `docs/TEST_LOG.md` when validation affects status.

## Commit & Pull Request Guidelines
- History uses short, descriptive summaries (e.g., “New handler…”, “Add … investigation”). Keep messages concise and scoped.
- PRs should include: summary of changes, environment tested (DEV/PROD), and references to updated docs/logs.
- If status changes, update `CLAUDE.md` and relevant docs under `docs/`.

## Security & Configuration Tips
- Credentials live in `.env` and must not be committed.
- Prefer DEV endpoints for testing unless explicitly instructed.
- Redact customer data in logs or screenshots before sharing.

## Agent Notes
- Start with `CLAUDE.md` for current status and navigation.
- Use `docs/AI_NAVIGATION.md` and `docs/DOCUMENT_INDEX.md` to locate related materials.
