# Freedom UI Project Template (v5)

> Official Angular 17 template for creating Creatio Freedom UI components using remote modules.

## Quick Start

### 1. Configure Project Name

Replace placeholders in all files:
- `<%projectName%>` → Your package name (e.g., `my_custom_component`)
- `<%vendorPrefix%>` → `usr`

**Files to update:**
- `angular.json`
- `package.json`
- `webpack.config.js`
- `src/app/app.module.ts`

### 2. Install Dependencies

```bash
npm install
```

### 3. Create a Component

```bash
ng g c view-elements/my-input --view-encapsulation=ShadowDom
```

### 4. Register Component

**src/app/view-elements/my-input/my-input.component.ts:**
```typescript
import { Component, Input, Output, EventEmitter, ViewEncapsulation } from '@angular/core';
import { CrtViewElement, CrtInput, CrtOutput } from '@creatio-devkit/common';

@Component({
  selector: 'usr-my-input',
  template: `<input [value]="value" (input)="onInput($event)">`,
  encapsulation: ViewEncapsulation.ShadowDom
})
@CrtViewElement({
  selector: 'usr-my-input',
  type: 'usr.MyInput'
})
export class MyInputComponent {
  @Input() @CrtInput() value: string = '';
  @Output() @CrtOutput() valueChange = new EventEmitter<string>();

  onInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.valueChange.emit(value);
  }
}
```

**src/app/app.module.ts:**
```typescript
import { DoBootstrap, Injector, NgModule, ProviderToken } from '@angular/core';
import { createCustomElement } from '@angular/elements';
import { BrowserModule } from '@angular/platform-browser';
import { bootstrapCrtModule, CrtModule } from '@creatio-devkit/common';
import { MyInputComponent } from './view-elements/my-input/my-input.component';

@CrtModule({
  viewElements: [MyInputComponent]
})
@NgModule({
  declarations: [MyInputComponent],
  imports: [BrowserModule],
  providers: [],
})
export class AppModule implements DoBootstrap {
  constructor(private _injector: Injector) {}

  ngDoBootstrap(): void {
    const element = createCustomElement(MyInputComponent, {
      injector: this._injector,
    });
    customElements.define('usr-my-input', element);

    bootstrapCrtModule('my_custom_component', AppModule, {
      resolveDependency: (token) => this._injector.get(<ProviderToken<unknown>>token)
    });
  }
}
```

### 5. Build

```bash
npm run build
```

### 6. Deploy to Creatio

1. Copy `dist/*.js` files to Creatio package **File Content**
2. Reference in schema or use in Freedom UI Designer

## Directory Structure

```
FreedomUIProjectTemplate_v5/
├── angular.json              # Angular CLI config
├── package.json              # Dependencies
├── webpack.config.js         # Module Federation config
├── webpack.prod.config.js    # Production webpack
├── tsconfig.json             # TypeScript config
├── tsconfig.app.json         # App-specific TS config
├── tsconfig.spec.json        # Test TS config
├── jest.config.ts            # Jest test config
├── src/
│   ├── app/
│   │   ├── app.module.ts     # Main module (CrtModule + NgModule)
│   │   └── view-elements/    # Your components go here
│   ├── assets/               # Static assets
│   ├── bootstrap.ts          # Angular bootstrap
│   ├── main.ts               # Entry point
│   ├── index.html            # HTML template
│   └── styles.scss           # Global styles
└── README.md                 # This file
```

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| @angular/core | 17.3.12 | Angular framework |
| @angular/elements | 17.3.12 | Custom Elements support |
| @creatio-devkit/common | ^0.822.0 | Creatio SDK |
| @angular-architects/module-federation | ^17.0.8 | Module Federation |

## Webpack Module Federation

The template uses Module Federation to expose components as a remote entry:

```javascript
// webpack.config.js
new ModuleFederationPlugin({
  name: "<%projectName%>",
  filename: "remoteEntry.js",
  exposes: {
    './RemoteEntry': './/src/main.ts',
  },
  shared: share({...})
})
```

## Testing

```bash
npm run test
```

## Related Resources

- `docs/reference/CREATIO_SDK_REFERENCE.md` - Complete SDK reference
- `creatio-docs-full/code/*remote-module*` - Academy code examples
- `node_modules/@creatio-devkit/common/index.d.ts` - Type definitions
- https://academy.creatio.com/documents?id=15017 - Official documentation
