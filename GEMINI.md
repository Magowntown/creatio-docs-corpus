# GEMINI.md

## Project Overview

This project aims to fix and enhance report generation functionality within a Creatio v8 (Freedom UI) environment. The core task involves troubleshooting and repairing two types of reports:

1.  **Excel Reports:** Generated via a custom C# backend service (`UsrExcelReportService`). While the main "Commission" report is functional, other Excel-based reports are failing due to template configuration issues.
2.  **Looker Studio Reports:** Accessed via a frontend JavaScript handler. These are currently blocked by a combination of Content Security Policy (CSP) restrictions in the Creatio environment and Google account permission issues.

The system is designed to first check if a report has an associated Looker Studio URL. If so, it attempts to open it in a new tab. If not, it falls back to the backend C# service to generate and download an Excel file.

**Key Technologies:**

*   **Backend:** C# (for `UsrExcelReportService`)
*   **Frontend:** JavaScript (for Creatio Freedom UI client-side handlers)
*   **Database/Environment:** Creatio v8
*   **External Services:** Looker Studio, QuickBooks (for data verification)
*   **Testing/Automation:** Python, Puppeteer

## Building and Running

This project does not have a traditional build process. Instead, it involves deploying individual components (JS handlers, C# services) directly into the Creatio environment.

**Key Commands:**

While there's no central build script, the following commands are relevant for development and testing:

```bash
# Load environment variables (contains Creatio credentials)
source .env

# Run the Python-based API test script
python3 scripts/testing/test_report_service.py

# Run a specific report test
CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py
```

**Deployment:**

Deployment is a manual process of copying and pasting code into the Creatio developer console. The `CLAUDE.md` file provides direct links to the appropriate schemas.

*   **Frontend Handler:**
    *   **File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
    *   **Schema UID:** `873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2`
    *   **URL:** `https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2`
*   **Backend Service:**
    *   **File:** `source-code/UsrExcelReportService_Updated.cs`
    *   **Schema UID:** `ed794ab8-8a59-4c7e-983c-cc039449d178`
    *   **URL:** `https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`

**TODO:** The `package.json` file contains a placeholder test script. This should be updated with a real test command, potentially leveraging the `puppeteer` dependency for automated UI testing.

## Development Conventions

*   **Documentation First:** The `CLAUDE.md` file is the central source of truth for project status, known issues, and session history. It should be consulted before starting work and updated after each session.
*   **Versioned Files:** Both frontend and backend files are versioned by appending suffixes (e.g., `_v2`, `_Updated`). This appears to be the convention for tracking changes. The `README.md` files in `client-module` and `source-code` specify which file is currently deployed.
*   **Modular Structure:** The code is separated by concern:
    *   `client-module/`: Frontend JavaScript handlers.
    *   `source-code/`: Backend C# services.
    *   `scripts/`: Utility and testing scripts.
    *   `docs/`: Project documentation and communication logs.
*   **Credentials:** All sensitive information, such as Creatio API credentials, is stored in a `.env` file and should not be committed to version control.
*   **AI Assistant Workflow:** The `CLAUDE.md` file outlines a specific workflow for AI assistants, which includes:
    1.  Reading `CLAUDE.md` first.
    2.  Using `docs/AI_NAVIGATION.md` to find relevant documents.
    3.  Following established patterns.
    4.  Updating documentation.

### Key Documentation

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | **START HERE** - Main status, active issues, and quick deploy links. |
| `docs/AI_NAVIGATION.md` | A map to find the right document for a given scenario. |
| `docs/DOCUMENT_INDEX.md` | A complete list of all documents in the project. |
| `docs/SHARED_UNDERSTANDING.md` | A comprehensive reference for the system's knowledge. |
| `client-module/README.md` | Index and status of frontend JavaScript handlers. |
| `source-code/README.md` | Index and status of backend C# services. |