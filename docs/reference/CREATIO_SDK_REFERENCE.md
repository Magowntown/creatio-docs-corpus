# Creatio DevKit SDK Reference

> **SDK Version:** 0.832.0 | **Updated:** 2026-02-05

## Quick Start

```typescript
import {
  CrtModule, CrtViewElement, CrtInput, CrtOutput,
  Model, HttpClientService, DialogService, SysSettingsService
} from '@creatio-devkit/common';
```

---

## 1. Core Decorators

### @CrtModule
Container for registering view elements, handlers, validators, and converters.

```typescript
@CrtModule({
  viewElements: [MyComponent],
  requestHandlers: [MyHandler],
  validators: [MyValidator],
  converters: [MyConverter]
})
@NgModule({...})
export class AppModule implements DoBootstrap {
  constructor(private _injector: Injector) {}

  ngDoBootstrap(): void {
    bootstrapCrtModule('myPackage', AppModule, {
      resolveDependency: (token) => this._injector.get(token)
    });
  }
}
```

### @CrtViewElement
Registers a component as a Freedom UI view element.

```typescript
@CrtViewElement({
  type: 'usr.MyInput',        // Used in viewConfigDiff
  selector: 'usr-my-input',   // DOM selector
  inputs: {
    value: {},                // Input bindings
    label: {}
  },
  outputs: {
    valueChange: {}           // Output events
  },
  validationInputs: {
    valueValidationInfo: {}   // Validation state
  }
})
@Component({
  selector: 'usr-my-input',
  template: `...`,
  encapsulation: ViewEncapsulation.ShadowDom
})
export class MyInputComponent {
  @Input() @CrtInput() value!: string;
  @Input() @CrtInput() label!: string;
  @Output() @CrtOutput() valueChange = new EventEmitter<string>();
  @CrtValidationInput() valueValidationInfo!: CrtValidationInfo;
}
```

### @CrtRequestHandler
Creates custom request handlers for the handler chain.

```typescript
@CrtRequestHandler({
  requestType: 'crt.SomeRequest',
  type: 'usr.SomeRequestHandler'
})
export class SomeRequestHandler extends BaseRequestHandler<SomeRequest> {
  async handle(request: SomeRequest): Promise<unknown> {
    // Custom logic
    return this.next?.handle(request);  // Chain to next handler
  }
}
```

### @CrtValidator
Registers custom validation logic.

```typescript
@CrtValidator({
  type: 'usr.EmailValidator'
})
export class EmailValidator extends BaseValidator {
  protected async = false;

  validate(controlState: CrtControlState): CrtValidationErrors | null {
    const value = controlState.value as string;
    if (!value?.includes('@')) {
      return { email: { message: 'Invalid email format' } };
    }
    return null;
  }
}
```

### @CrtConverter
Creates value converters for binding transformations.

```typescript
@CrtConverter({
  type: 'usr.ToBoolean'
})
export class ToBooleanConverter implements Converter<unknown, boolean> {
  convert(value: unknown): boolean {
    return Boolean(value);
  }
}
```

### @CrtInterfaceDesignerItem
Adds component to Freedom UI Designer toolbox.

```typescript
@CrtInterfaceDesignerItem({
  toolbarConfig: {
    caption: 'usrMyComponentCaption',
    icon: require(`!!raw-loader?{esModule:false}!../assets/icon.svg`),
    hint: 'usrMyComponentHint',
    defaultPropertyValues: {
      value: 'Default value'
    }
  }
})
```

---

## 2. Services

### Model (Data Access)
Primary service for CRUD operations.

```typescript
// Create model instance
const model = await Model.create('Contact');

// Get schema
const schema = await model.getSchema();

// Load records
const contacts = await model.load({
  attributes: ['Name', 'Email', 'Phone'],
  parameters: {
    PrimaryColumnValue: 'some-guid'
  },
  options: {
    pagingConfig: { rowCount: 50 }
  }
});

// Insert record
const result = await model.insert({
  Name: 'John Doe',
  Email: 'john@example.com'
});

// Update record
await model.update({
  Id: 'guid',
  Name: 'Updated Name'
});

// Delete record
await model.delete({ Id: 'guid' });
```

### HttpClientService
HTTP requests with typed responses.

```typescript
const http = new HttpClientService();

// GET request
const response = await http.get<MyData>('/api/endpoint', {
  headers: { 'Custom-Header': 'value' },
  responseType: 'json'
});

// POST request
const result = await http.post('/api/endpoint', { data: 'value' }, {
  responseType: 'json'
});

// Other methods: put(), patch(), delete()
```

### DialogService
Modal dialogs and confirmations.

```typescript
const dialog = new DialogService();

const result = await dialog.open({
  title: 'Confirm Action',
  message: 'Are you sure?',
  buttons: [
    { caption: 'Yes', returnCode: 'yes', color: ButtonColor.Primary },
    { caption: 'No', returnCode: 'no' }
  ]
});

if (result === 'yes') {
  // User confirmed
}
```

### SysSettingsService
System settings access.

```typescript
const sysSettings = new SysSettingsService();

// Get single setting
const setting = await sysSettings.getByCode('IWEnableCommissionV3');
console.log(setting.value);  // false

// Get multiple settings
const settings = await sysSettings.getByCodes([
  'IWEnableCommissionV3',
  'IWEnableCommissionV4'
]);

// Update setting
await sysSettings.update({
  code: 'MySetting',
  value: 'new value'
}, false);  // isPersonal
```

### ProcessEngineService
Business process execution.

```typescript
const processEngine = new ProcessEngineService();

// Execute process by name
const result = await processEngine.executeProcessByName(
  'IWRecalculateCommission',
  { OrderId: 'guid', ForceRecalc: true },  // Parameters
  ['CommissionAmount', 'Status']           // Result parameters
);

// Complete process element
await processEngine.completeExecuting(
  processElementUId,
  { Decision: 'Approved' }
);
```

### FeatureService
Feature flag checking.

```typescript
const features = new FeatureService();

// Check single feature
const isEnabled = await features.getFeatureState('NewCommissionUI');

// Check multiple features
const [feature1, feature2] = await features.getFeaturesState([
  'Feature1', 'Feature2'
]);
```

### RightsService
Permission checking.

```typescript
const rights = new RightsService();

// Check single operation
const canEdit = await rights.getCanExecuteOperation('CanEditOrder');

// Check multiple operations
const [canEdit, canDelete] = await rights.getCanExecuteOperations([
  'CanEditOrder', 'CanDeleteOrder'
]);
```

### MaskService
Loading indicators.

```typescript
const mask = new MaskService();

// Show loading mask
await mask.showBodyMask({ delay: 200 });  // 200ms delay

// Hide mask
await mask.hideBodyMask();
```

### LicenseService
License restrictions.

```typescript
const license = new LicenseService();

// Check license operations
const statuses = await license.getLicenseOperationStatuses([
  'CanExportToExcel',
  'CanUseAdvancedReports'
]);
```

### SysValuesService
System values (current user, culture, etc.).

```typescript
const sysValues = new SysValuesService();
const values = await sysValues.loadSysValues();

console.log(values.currentUser);
console.log(values.currentCulture);
console.log(values.environmentType);
```

### MessageChannelService
WebSocket real-time messaging.

```typescript
const channel = new MessageChannelService();

// Subscribe to messages
const subscription = await channel.subscribe<MyData>(
  'OrderUpdates',
  (event) => console.log('Received:', event.body)
);

// Send message
await channel.sendMessage(
  'OrderUpdates',
  { orderId: 'guid', status: 'Approved' },
  MessageChannelType.WebSocket
);

// Unsubscribe
subscription.unsubscribe();
```

### AiContextService
AI context management (for Copilot integration).

```typescript
const aiContext = AiContextService.instance;

// Add context part
const partId = aiContext.setContextPart(() => ({
  type: 'CreatioPageContextPart',
  pageSchemaName: 'OrderFormPage',
  dataSources: [...]
}));

// Get all context
const context = await aiContext.getContext();

// Remove context
aiContext.removeContextPart(partId);
```

---

## 3. Query Classes

### EntitySchemaQuery (ESQ)
Complex data queries.

```typescript
import { EntitySchemaQuery, FilterGroup, ComparisonType } from '@creatio-devkit/common';

const esq = new EntitySchemaQuery('Order');
esq.addColumn('Number');
esq.addColumn('Amount');
esq.addColumn('Account.Name');  // Join

// Add filter
const filterGroup = new FilterGroup();
filterGroup.addSchemaColumnFilterWithParameter(
  ComparisonType.Equal,
  'Status',
  'Approved'
);
esq.filters = filterGroup;

// Execute
const result = await esq.getEntityCollection();
```

### InsertQuery / UpdateQuery / DeleteQuery
Direct DML operations.

```typescript
import { InsertQuery, UpdateQuery, DeleteQuery } from '@creatio-devkit/common';

// Insert
const insert = new InsertQuery('Contact');
insert.setParameterValue('Name', 'John');
await insert.execute();

// Update
const update = new UpdateQuery('Contact');
update.setParameterValue('Name', 'Updated');
update.filters.addSchemaColumnFilterWithParameter(
  ComparisonType.Equal, 'Id', 'guid'
);
await update.execute();

// Delete
const del = new DeleteQuery('Contact');
del.filters.addSchemaColumnFilterWithParameter(
  ComparisonType.Equal, 'Id', 'guid'
);
await del.execute();
```

---

## 4. Filter System

### FilterGroup
Build complex filter conditions.

```typescript
import { FilterGroup, ComparisonType, LogicalOperatorType } from '@creatio-devkit/common';

const filters = new FilterGroup();
filters.logicalOperation = LogicalOperatorType.And;

// Simple filter
filters.addSchemaColumnFilterWithParameter(
  ComparisonType.Equal,
  'Status',
  'Active'
);

// Between filter
filters.addSchemaColumnBetweenFilterWithParameters(
  'Amount',
  1000,
  5000
);

// In filter (multiple values)
filters.addInFilter('Category', ['A', 'B', 'C']);

// Nested group
const orGroup = new FilterGroup();
orGroup.logicalOperation = LogicalOperatorType.Or;
orGroup.addSchemaColumnFilterWithParameter(ComparisonType.Equal, 'Type', 'Order');
orGroup.addSchemaColumnFilterWithParameter(ComparisonType.Equal, 'Type', 'Quote');
filters.addItem(orGroup);
```

### ComparisonType Enum
```typescript
ComparisonType.Equal
ComparisonType.NotEqual
ComparisonType.Greater
ComparisonType.GreaterOrEqual
ComparisonType.Less
ComparisonType.LessOrEqual
ComparisonType.StartWith
ComparisonType.EndWith
ComparisonType.Contain
ComparisonType.NotContain
ComparisonType.IsNull
ComparisonType.IsNotNull
```

---

## 5. Utility Functions

```typescript
import {
  generateGuid,
  isGuid,
  isEmptyGuid,
  EMPTY_GUID,
  encodeDate,
  toLocalISOString
} from '@creatio-devkit/common';

// GUID utilities
const newGuid = generateGuid();
const valid = isGuid('550e8400-e29b-41d4-a716-446655440000');
const empty = isEmptyGuid('00000000-0000-0000-0000-000000000000');

// Date encoding (for WCF format)
const wcfDate = encodeDate(new Date());  // "/Date(1234567890000)/"
```

---

## 6. Type Definitions

### DataValueType Enum
```typescript
DataValueType.GUID
DataValueType.Text
DataValueType.Integer
DataValueType.Float
DataValueType.Money
DataValueType.DateTime
DataValueType.Date
DataValueType.Time
DataValueType.Boolean
DataValueType.Lookup
DataValueType.Enum
DataValueType.Binary
```

### LookupValue Interface
```typescript
interface LookupValue {
  value: string;      // GUID
  displayValue: string;
}
```

---

## 7. Freedom UI Project Template

**Unzipped Location:** `FreedomUIProjectTemplate_v5/`

### Structure
```
FreedomUIProjectTemplate_v5/
├── angular.json                # Angular CLI config (<%projectName%>, <%vendorPrefix%>)
├── package.json                # Dependencies (Angular 17, SDK)
├── webpack.config.js           # Module Federation setup
├── src/
│   ├── app/
│   │   ├── app.module.ts       # CrtModule + NgModule (COPY THIS PATTERN)
│   │   └── view-elements/      # Custom components go here
│   ├── assets/                 # Icons, images
│   ├── bootstrap.ts            # Angular bootstrap
│   └── main.ts                 # Entry point
└── tsconfig.json               # TypeScript ES2022
```

### Key Dependencies
- Angular 17.3.12
- @creatio-devkit/common ^0.822.0
- @angular-architects/module-federation ^17.0.8
- webpack 5.94

### Setup Steps
1. Replace `<%projectName%>` with actual package name in all files
2. Replace `<%vendorPrefix%>` with `usr` in angular.json
3. Run `npm i` to install dependencies
4. Create components in `src/app/view-elements/`
5. Register in `app.module.ts` @CrtModule decorator
6. Build with `npm run build`
7. Copy `dist/*.js` to Creatio package File Content

### Build Output
The build produces a `remoteEntry.js` that Creatio loads dynamically.

---

## 7.1 Academy Code Examples

**Location:** `creatio-docs-full/code/` (1,496 directories of real examples)

### Find Examples by Topic
```bash
# Remote module examples
find creatio-docs-full/code -path "*remote-module*" -name "*.js"

# Validator examples
find creatio-docs-full/code -path "*validator*" -name "*.js"

# Business logic examples
find creatio-docs-full/code -path "*business-logic*" -name "*.js"

# Data binding examples
find creatio-docs-full/code -path "*bind-data*" -name "*.js"
```

### Key Example Patterns

| Topic | Directory Pattern | Content |
|-------|-------------------|---------|
| Component Creation | `*implement-a-remote-module*` | @CrtViewElement, bootstrapCrtModule |
| Custom Validators | `*custom-validator*` | @CrtValidator, BaseValidator |
| Localization | `*localize-remote-module*` | LocalizeFn integration |
| Business Logic | `*business-logic-of-the-remote*` | Handler chain patterns |
| Validation | `*implement-the-validation*` | @CrtValidationInput |

---

## 8. Common Patterns

### Handler Chain Pattern
```typescript
@CrtRequestHandler({
  requestType: 'crt.OpenPageRequest',
  type: 'usr.CustomOpenPageHandler'
})
export class CustomOpenPageHandler extends BaseRequestHandler {
  async handle(request: OpenPageRequest): Promise<unknown> {
    // Pre-processing
    console.log('Opening page:', request.schemaName);

    // Call next handler in chain
    const result = await this.next?.handle(request);

    // Post-processing
    return result;
  }
}
```

### Attribute Change Handler
```typescript
@CrtRequestHandler({
  requestType: 'crt.HandleViewModelAttributeChangeRequest',
  type: 'usr.AmountChangeHandler'
})
export class AmountChangeHandler extends BaseRequestHandler<HandleViewModelAttributeChangeRequest> {
  async handle(request: HandleViewModelAttributeChangeRequest): Promise<unknown> {
    if (request.attributeName === 'Amount') {
      console.log('Amount changed from', request.oldValue, 'to', request.value);
    }
    return this.next?.handle(request);
  }
}
```

---

## 9. Changelog Highlights (0.832.0)

- **0.832.0**: ViewModelCollectionActionType, ViewModelCollectionChange
- **0.831.0**: TransactionFactoryService
- **0.830.0**: AI Context service types
- **0.823.0**: ProcessEngineService, SysValues.environmentType
- **0.822.0**: ConverterRegistry.find method
- **0.820.0**: MessageChannelService, Subscription class
- **0.814.0**: HandleViewModelAttributeChangeRequest, DialogService
- **0.813.0**: LicenseService
- **0.808.0**: CrtConverter decorator, FilterGroup utilities
- **0.804.0**: CrtInject, CrtRequestHandler, CrtValidator decorators
- **0.803.0**: CrtInterfaceDesignerItem, CrtViewElement decorators

---

## Related Documents

- `CREATIO_ARCHITECTURE_DEEP_DIVE.md` - Platform architecture
- `RESOURCE_INVENTORY.md` - Available resources
- `MASTER_CATALOG.md` - Report configurations
- Creatio Academy: https://academy.creatio.com/documents?id=15017
