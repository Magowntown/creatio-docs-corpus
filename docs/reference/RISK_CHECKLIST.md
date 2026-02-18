# Risk & Edge-Case Checklist

This checklist is designed to be used before committing or deploying changes to the Creatio reports project. It covers the most common and high-impact failure points discovered during the project's history.

---

### Frontend & UI (Highest Risk)

-   **[ ] State & Caching:**
    -   Does the change involve a filter that depends on another filter's selection (e.g., cascade)?
    -   Verify that changing a parent filter correctly clears and reloads the child filter's options, even when switching between different report types.
    -   Test for race conditions: open dropdowns quickly after a selection to see if stale data is shown before async queries complete.

-   **[ ] Attribute Binding:**
    -   Are all new UI attributes for visibility or data binding declared as empty objects (e.g., `UsrMyAttribute: {}`) to ensure reactivity?
    -   Are you accessing data from parent schema controls (like date pickers) using `await context.AttributeName`, not `context.attributes.AttributeName`?

-   **[ ] Lookups & Data Sources:**
    -   Does a new lookup/ComboBox bind to an entity (`Account`) or a plain text `VARCHAR` column in a view? This is a critical distinction that has caused many bugs.
    -   If using an `embeddedModel` for a data source, is the syntax *exactly* matching the Creatio Academy pattern (`modelConfigDiff`, etc.)?

---

### Backend & Data Generation

-   **[ ] VBA Macro Dependency (High Risk):**
    -   If the backend data source for an Excel report is modified, have you confirmed the **exact column order, data types, and header names** match what the `.xlsm` template's VBA macro expects?
    -   Check for the "anchor variable" infinite loop bug in any new or modified VBA that uses nested `While` loops.

-   **[ ] Report Routing & Configuration:**
    -   Is the report routing logic in the C# service checking the report's **Name** (`IntName`) *before* falling back to the entity schema name? Relying on `rootSchemaName` from the configuration is a known source of errors.
    -   Does the report's `UsrCode` in the `UsrReportesPampa` menu match the `IntName` in the `IntExcelReport` table? Check for subtle differences like prefixes ("Rpt ") or spacing.

---

### General System

-   **[ ] Filter Combination Logic:**
    -   Test reports that use a combination of filters (e.g., "Items by Customer" which uses Customer, Dates, and Status).
    -   Test edge cases with filters: no filters selected, all filters selected, and unusual date ranges (e.g., a single day).

-   **[ ] Empty & Null Data:**
    -   How does the report behave when a filter returns no results? (e.g., a customer with no items, a month with no sales). Does it show an empty state gracefully or throw an error?
    -   Verify that `null` or `undefined` values from the database or API calls are handled correctly in both frontend and backend logic.
