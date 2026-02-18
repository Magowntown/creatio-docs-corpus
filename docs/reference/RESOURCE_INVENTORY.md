# Complete Resource Inventory

> **Last Updated:** 2026-02-05 | **Total Resources:** ~17GB across locations

## Quick Reference

| Location | Size | Key Contents |
|----------|------|--------------|
| C:\Creatio (Windows) | 16GB | 3 Creatio versions, 2 DEV instances, 396 packages |
| creatio-report-fix (WSL) | ~500MB | Project docs, source, scripts, investigation |
| creatio-docs-full (WSL) | ~200MB | 5,000 Creatio Academy pages |

---

## 1. Windows Resources - `/mnt/c/Creatio/` (16GB)

### Creatio Installations

| File | Size | Version | Date | Notes |
|------|------|---------|------|-------|
| 8.1.2.3842_Studio_Softkey_MSSQL_ENU.zip | 960MB | 8.1.2 | Mar 2024 | Studio edition |
| 8.1.3.6789_...PostgreSQL_ENU.zip | 954MB | 8.1.3 | Jun 2024 | PostgreSQL variant |
| **8.3.0.3031_...MSSQL_ENU/** | ~2GB | **8.3.0** | Jul 2025 | **Latest - Extracted** |
| 8.3.0.3031_...MSSQL_ENU.zip | 2GB | 8.3.0 | Jul 2025 | MSSQL variant |
| 8.3.0.3031_...PostgreSQL_ENU.zip | 992MB | 8.3.0 | Jul 2025 | PostgreSQL variant |

### Deployed Development Instances

| Directory | Purpose | Date | Key Contents |
|-----------|---------|------|--------------|
| **D1_mkpdev-interweave/** | DEV Environment | Aug 2025 | IWQBIntegration deployed, 396 package backups |
| D2_mkpdev-2153/ | Older DEV | Jun 2024 | Legacy reference |

### D1_mkpdev-interweave Key Files

| File | Size | Purpose |
|------|------|---------|
| CREATIO_DEVELOPMENT_COMPLETE_REFERENCE_GUIDE.md | 17KB | Complete IDE development guide |
| CREATIO_SAFE_DEVELOPMENT_PRACTICES_GUIDE.md | 9KB | DO's/DON'Ts, pitfalls, solutions |
| CREATIO_QUICK_REFERENCE_ARCHITECTURE.md | 9KB | Package structure, components |
| CREATIO_OPTIMAL_PROMPTS_COLLECTION.md | 13KB | AI prompt templates for Creatio tasks |
| Creatio_Technical_Analysis_Report.md | 10KB | Technical analysis of platform |
| Packages/ | 396 files | Complete package backup from DEV |
| Terrasoft.WebApp/.../IWQBIntegration/ | 57 schemas | Deployed IWQBIntegration (Jul 2025 version) |

### Other Windows Resources

| File | Purpose |
|------|---------|
| clio/appsettings.json | Clio CLI configuration |
| documentation/WINDOWS_SETUP.md | Windows clio setup guide |
| ConnectionStringsBackup.config | Database connection backup |
| 8.3.0.../db/BPMonline830...bak | 1.4GB SQL Server backup |

---

## 2. Project Directory - `/home/magown/creatio-report-fix/`

### Documentation Structure

```
docs/
├── AI_NAVIGATION.md          # Scenario → Document mapping
├── DOCUMENT_INDEX.md         # Complete document listing
├── SHARED_UNDERSTANDING.md   # Consolidated system knowledge
│
├── investigation/            # 30+ technical analysis docs
│   ├── IWQBINTEGRATION_MASTER_CATALOG.md
│   ├── IWQBINTEGRATION_TEAM_INSTRUCTIONS.md
│   ├── COMMISSION_CALCULATION_INVESTIGATION.md
│   └── ...
│
├── reference/                # 15+ reference documents
│   ├── MASTER_CATALOG.md
│   ├── RISK_CHECKLIST.md
│   ├── RESOURCE_INVENTORY.md (this file)
│   └── ...
│
├── logs/                     # Session logs
│   └── SESSION_LOG_202601*.md (7 logs)
│
└── qb-sync/                  # QB integration docs
```

### Source Code

| Directory | Count | Key Files |
|-----------|-------|-----------|
| source-code/ | 2 | UsrExcelReportService_Updated.cs |
| client-module/ | 99 | Handler versions v1-v54 |
| vba/ | 2 | PMPSalesbySalesRep_FIXED_v2.bas |
| sql/ | 12 | View definitions and fixes |

### Scripts

| Directory | Count | Purpose |
|-----------|-------|---------|
| scripts/testing/ | 10+ | API tests, report tests |
| scripts/investigation/ | 20+ | Analysis and debugging |
| scripts/deployment/ | 5+ | Deployment automation |
| scripts/crawling/ | 10+ | Documentation scraping |

### IWQBIntegration Package Analysis

| File | Size | Content |
|------|------|---------|
| investigation/IWQBIntegration/full_content.txt | 4.4MB | 90,255 lines extracted JSON |
| investigation/IWQBIntegration/file_list.txt | 43KB | Package manifest |
| investigation/IWQBIntegration/IWQBIntegration.gz | 637KB | Compressed package |
| investigation/IWQBIntegration/IWQBIntegration | 5MB | Raw binary |

---

## 3. Creatio Academy Documentation - `creatio-docs-full/`

| Resource | Count | Coverage |
|----------|-------|----------|
| Markdown files | 4,985 | Complete Academy mirror |
| Code examples | 1,496 dirs | SDK, API, customization |
| Process elements | 30+ docs | Signal, Read, Modify, Gateway |
| Platform version | 8.x | Current production |

### Key Process Element Docs

| Document | Location | Content |
|----------|----------|---------|
| signal-start-event.md | markdown/ | Signal triggers, "In any of selected fields" |
| read-data-process-element.md | markdown/ | 4 read modes, efficient queries |
| modify-data-process-element.md | markdown/ | Batch updates, filter operations |
| exclusive-gateway-or-process-element.md | markdown/ | Conditional branching |
| conditional-flow.md | markdown/ | Flow conditions |

---

## 4. Version Comparison

### IWQBIntegration Package Versions

| Source | Version Date | Dependencies | Schemas | Notes |
|--------|--------------|--------------|---------|-------|
| D1 (deployed) | Jul 14, 2025 | 13 | 57 | Missing V3/V4 processes |
| PROD package | Sep 10, 2025 | **19** | ~80+ | Has V3/V4, needs IWInterWeavePaymentApp |

### Missing PROD Dependency

| Package | Status | Required By |
|---------|--------|-------------|
| IWInterWeavePaymentApp | In DEV only | IWQBIntegration PROD import |
| UId: a60336cf-5bda-440e-bc45-419a93b9b332 | Must export from DEV | Phase 1 of import |

---

## 5. Environment Configuration

### Clio CLI (Windows)

```json
// C:\Creatio\clio\appsettings.json
{
  "Environment": "mkpdev-interweave",
  "URL": "https://mkpdev-interweave.creatio.com/",
  "Username": "Supervisor"
}
```

### Test Commands

```bash
# From Windows PowerShell
clio ping mkpdev-interweave
clio get-pkg-list -e mkpdev-interweave
clio pull-pkg IWQBIntegration -e mkpdev-interweave
```

---

## 6. Critical Findings Summary

1. **D1's IWQBIntegration is OLDER** than package needed for PROD
2. **IWInterWeavePaymentApp must be imported first** to PROD
3. **V3 process 26x cascade risk** - verify IWEnableCommissionV3=false
4. **Complete Creatio Academy offline** - all process elements documented
5. **396 package backups available** from DEV for reference
6. **5 custom development guides** specifically for IWQBIntegration

---

## 7. Usage Recommendations

### For IWQBIntegration Import
1. Use `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` for procedure
2. Reference `investigation/IWQBIntegration/full_content.txt` for package details
3. Check D1 deployed version for working reference

### For Process Development
1. Use `creatio-docs-full/markdown/signal-start-event.md` for trigger patterns
2. Reference `CREATIO_DEVELOPMENT_COMPLETE_REFERENCE_GUIDE.md` from D1
3. Follow patterns in `CREATIO_SAFE_DEVELOPMENT_PRACTICES_GUIDE.md`

### For Freedom UI Development
1. Use `CREATIO_OPTIMAL_PROMPTS_COLLECTION.md` for task templates
2. Reference `CREATIO_QUICK_REFERENCE_ARCHITECTURE.md` for components
3. Check D1's deployed IWQBIntegration schemas for examples
4. **Use `docs/reference/CREATIO_SDK_REFERENCE.md`** for TypeScript SDK patterns

---

## 8. Freedom UI Project Template (Unzipped)

**Location:** `/home/magown/creatio-report-fix/FreedomUIProjectTemplate_v5/`

### Directory Structure

```
FreedomUIProjectTemplate_v5/
├── angular.json              # Angular CLI config
│   └── <%projectName%>       # Replace with actual package name
│   └── <%vendorPrefix%>      # Replace with 'usr' prefix
├── package.json              # Dependencies
│   └── Angular 17.3.12
│   └── @creatio-devkit/common ^0.822.0
│   └── @angular-architects/module-federation ^17.0.8
├── webpack.config.js         # Module Federation setup
│   └── exposes: ./RemoteEntry → src/main.ts
│   └── output: remoteEntry.js
├── tsconfig.json             # TypeScript ES2022
├── jest.config.ts            # Jest testing
├── src/
│   ├── app/
│   │   ├── app.module.ts     # @CrtModule + @NgModule
│   │   └── view-elements/    # Custom components go here
│   ├── assets/               # Icons, images
│   ├── bootstrap.ts          # platformBrowserDynamic()
│   ├── main.ts               # Entry point
│   └── styles.scss
└── README.md                 # Build instructions
```

### Key Files with Content

**app.module.ts** (Template Pattern):
```typescript
@CrtModule({
  viewElements: [],  // Add your components here
})
@NgModule({
  declarations: [],
  imports: [BrowserModule],
  providers: [],
})
export class AppModule implements DoBootstrap {
  constructor(private _injector: Injector) {}

  ngDoBootstrap(): void {
    bootstrapCrtModule('<%projectName%>', AppModule, {
      resolveDependency: (token) => this._injector.get(token)
    });
  }
}
```

**webpack.config.js** (Module Federation):
```javascript
new ModuleFederationPlugin({
  name: "<%projectName%>",
  filename: "remoteEntry.js",
  exposes: {
    './RemoteEntry': './/src/main.ts',
  },
  shared: share({...})
})
```

### Usage Steps

1. Replace `<%projectName%>` with actual package name (e.g., `sdk_remote_module_package`)
2. Replace `<%vendorPrefix%>` with `usr`
3. Run `npm i` to install dependencies
4. Create components in `src/app/view-elements/`
5. Register in `app.module.ts` CrtModule decorator
6. Build with `npm run build`
7. Copy `dist/` JS files to Creatio package File Content

---

## 9. NPM Packages (creatio-report-fix)

### Installed Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **@creatio-devkit/common** | 0.832.0 | Official Creatio Freedom UI SDK |
| **@creatio/base** | 0.832.0 | Base classes and query builders |
| class-transformer | 0.5.1 | Object transformation |
| lodash | 4.17.23 | Utility functions |
| puppeteer | 24.35.0 | Browser automation testing |
| reflect-metadata | 0.2.2 | Decorator metadata |
| shortid-extend | 0.0.3 | Short ID generation |
| tslib | 2.8.1 | TypeScript helpers |

### @creatio-devkit/common Key Exports

**Decorators:**
- `@CrtModule` - Container for view elements, handlers, validators
- `@CrtViewElement` - Register Freedom UI components
- `@CrtInput` / `@CrtOutput` - Component I/O bindings
- `@CrtRequestHandler` - Custom request handlers
- `@CrtValidator` - Custom validators
- `@CrtConverter` - Value converters
- `@CrtInterfaceDesignerItem` - Designer toolbox items
- `@CrtInject` - Dependency injection

**Services:**
- `Model` - CRUD data access
- `HttpClientService` - HTTP requests
- `DialogService` - Modal dialogs
- `SysSettingsService` - System settings
- `ProcessEngineService` - Business process execution
- `FeatureService` - Feature flags
- `RightsService` - Permission checking
- `MaskService` - Loading indicators
- `LicenseService` - License restrictions
- `SysValuesService` - System values
- `MessageChannelService` - WebSocket messaging
- `AiContextService` - AI/Copilot context

**Query Classes:**
- `EntitySchemaQuery` - Complex data queries
- `InsertQuery` / `UpdateQuery` / `DeleteQuery` - DML operations
- `FilterGroup` - Query filters
- `ComparisonType` - Filter comparison operators

**Utilities:**
- `generateGuid()`, `isGuid()`, `isEmptyGuid()`, `EMPTY_GUID`
- `encodeDate()` - WCF date format encoding
- `DataValueType` - Column type enumeration

### Freedom UI Project Template

**File:** `FreedomUIProjectTemplate_v5.zip` (10KB)

| Component | Technology |
|-----------|------------|
| Framework | Angular 17.3.12 |
| Build | Webpack 5.94 + Module Federation |
| SDK | @creatio-devkit/common 0.822.0 |
| Testing | Jest 29.7 |
| Node | >=16.17.0 |

**Structure:**
```
├── angular.json                # Angular CLI config
├── webpack.config.js           # Module Federation (remoteEntry.js)
├── src/app/
│   ├── app.module.ts           # @CrtModule + @NgModule
│   └── view-elements/          # Custom components
└── src/bootstrap.ts            # platformBrowserDynamic()
```

**Key Pattern (app.module.ts):**
```typescript
@CrtModule({
  viewElements: [MyComponent]
})
@NgModule({...})
export class AppModule implements DoBootstrap {
  ngDoBootstrap(): void {
    bootstrapCrtModule('packageName', AppModule, {
      resolveDependency: (token) => this._injector.get(token)
    });
  }
}
```

---

## 9. SDK Documentation Reference

| Document | Location | Content |
|----------|----------|---------|
| **SDK Reference** | `docs/reference/CREATIO_SDK_REFERENCE.md` | Complete TypeScript SDK guide |
| SDK README | `node_modules/@creatio-devkit/common/README.md` | Installation |
| SDK Changelog | `node_modules/@creatio-devkit/common/CHANGELOG.md` | Version history |
| SDK Types | `node_modules/@creatio-devkit/common/index.d.ts` | 99KB TypeScript definitions |
| Academy | https://academy.creatio.com/documents?id=15017 | Official documentation |

---

## 11. Crawled Documentation Code Examples

**Location:** `creatio-docs-full/code/` (1,496 directories)

### Key Code Example Categories

| Pattern | Example Directory | Content |
|---------|-------------------|---------|
| Remote Module | `*implement-a-remote-module*` | @CrtViewElement, bootstrapCrtModule |
| Validators | `*custom-validator*` | @CrtValidator, BaseValidator |
| Localization | `*localize-remote-module*` | LocalizeFn patterns |
| Business Logic | `*implement-the-business-logic*` | Handler chains |
| Data Binding | `*bind-data*` | @CrtInput, @CrtOutput |
| OData API | `*odata*` | EntitySchemaQuery alternatives |
| Web Services | `*web-service*` | HttpClientService patterns |
| Mobile | `*mobile*` | Mobile-specific patterns |

### Example: Complete Remote Module (from Academy)

**Component (input.component.ts):**
```typescript
import { Component, ViewEncapsulation } from '@angular/core';
import { CrtViewElement } from '@creatio-devkit/common';

@Component({
  selector: 'usr-input',
  templateUrl: './input.component.html',
  encapsulation: ViewEncapsulation.ShadowDom
})
@CrtViewElement({
  selector: 'usr-input',
  type: 'usr.Input'
})
export class InputComponent { }
```

**Module (app.module.ts):**
```typescript
import { createCustomElement } from '@angular/elements';
import { bootstrapCrtModule, CrtModule } from '@creatio-devkit/common';

@CrtModule({ viewElements: [InputComponent] })
@NgModule({ declarations: [InputComponent], imports: [BrowserModule] })
export class AppModule implements DoBootstrap {
  constructor(private _injector: Injector) {}

  ngDoBootstrap(): void {
    const element = createCustomElement(InputComponent, { injector: this._injector });
    customElements.define('usr-input', element);
    bootstrapCrtModule('package_name', AppModule, {
      resolveDependency: (token) => this._injector.get(token)
    });
  }
}
```

### Finding Examples by Topic

```bash
# Find Freedom UI examples
find creatio-docs-full/code -name "*.js" -path "*freedom*" | head -20

# Find validator examples
find creatio-docs-full/code -name "*.js" -path "*validator*"

# Find remote module examples
find creatio-docs-full/code -name "*.js" -path "*remote-module*"
```

---

## 12. D1 Development Guides (Windows)

**Location:** `/mnt/c/Creatio/D1_mkpdev-interweave/`

| Document | Size | Purpose |
|----------|------|---------|
| `CREATIO_DEVELOPMENT_COMPLETE_REFERENCE_GUIDE.md` | 17KB | Complete IDE development guide |
| `CREATIO_SAFE_DEVELOPMENT_PRACTICES_GUIDE.md` | 9KB | DO's/DON'Ts, pitfalls, solutions |
| `CREATIO_QUICK_REFERENCE_ARCHITECTURE.md` | 9KB | Package structure, components |
| `CREATIO_OPTIMAL_PROMPTS_COLLECTION.md` | 13KB | AI prompt templates for Creatio |
| `Creatio_Technical_Analysis_Report.md` | 10KB | Platform technical analysis |

### Access from WSL

```bash
# Read D1 guides
cat /mnt/c/Creatio/D1_mkpdev-interweave/CREATIO_DEVELOPMENT_COMPLETE_REFERENCE_GUIDE.md

# Copy to local project if needed
cp /mnt/c/Creatio/D1_mkpdev-interweave/*.md docs/reference/d1-guides/
```

---

## 13. Python Automation Scripts

**Location:** `scripts/investigation/creatio_*.py`

| Script | Size | Purpose |
|--------|------|---------|
| `creatio_api_schema.py` | 8KB | REST API schema fetching via Playwright |
| `creatio_apply_handler.py` | 12KB | Apply handler changes |
| `creatio_browser_test.py` | 12KB | Browser automation testing |
| `creatio_code_edit_test.py` | 4KB | Code editing validation |
| `creatio_dom_extract.py` | 8KB | DOM extraction for debugging |
| `creatio_extract_schema.py` | 10KB | Schema extraction |
| `creatio_find_handlers.py` | 5KB | Find handler definitions |
| `creatio_find_schema.py` | 7KB | Schema search |
| `creatio_inspect.py` | 3KB | Page inspection |
| `creatio_interaction_test.py` | 13KB | UI interaction testing |
| `creatio_open_schema.py` | 11KB | Open schema in designer |
| `creatio_report_button_fix.py` | 11KB | Report button fixes |
| `creatio_source_code_test.py` | 6KB | Source code validation |
| `creatio_ui_schema.py` | 9KB | UI schema extraction |

### Environment Requirements

```bash
# Set credentials
export CREATIO_URL="https://pampabay.creatio.com"
export CREATIO_USERNAME="..."
export CREATIO_PASSWORD="..."

# Run script
python3 scripts/investigation/creatio_api_schema.py
```

---

## 14. Quick Reference Summary

### For New AI Sessions

| Task | Start With |
|------|------------|
| **Freedom UI Component** | `CREATIO_SDK_REFERENCE.md` → `FreedomUIProjectTemplate_v5/` |
| **Report Fix** | `MASTER_CATALOG.md` → `HANDLER_VERSION_HISTORY.md` |
| **IWQBIntegration** | `IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` |
| **Commission Process** | `COMMISSION_CALCULATION_INVESTIGATION.md` |
| **Platform Understanding** | `CREATIO_ARCHITECTURE_DEEP_DIVE.md` |
| **TypeScript SDK** | `CREATIO_SDK_REFERENCE.md` |
| **Code Examples** | `creatio-docs-full/code/` (1,496 dirs) |
| **Academy Docs** | `creatio-docs-full/markdown/` (5,000 pages) |

### Key Paths

| Resource | Path |
|----------|------|
| SDK Types | `node_modules/@creatio-devkit/common/index.d.ts` |
| Template | `FreedomUIProjectTemplate_v5/` |
| Code Examples | `creatio-docs-full/code/` |
| Documentation | `creatio-docs-full/markdown/` |
| Scripts | `scripts/investigation/` |
| D1 Guides | `/mnt/c/Creatio/D1_mkpdev-interweave/` |
