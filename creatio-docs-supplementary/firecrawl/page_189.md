<!-- Source: page_189 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

The **mobile app manifest** describes the structure of the mobile app, its objects and connections between them. The base version of the Creatio Mobile app is described in the manifest located in the `MobileApplicationManifestDefaultWorkplace` schema of the `Mobile` package.

## Structure of mobile app manifest [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview\#title-1515-1 "Direct link to Structure of mobile app manifest")

The mobile app manifest is a `JSON` configuration object whose schema sections describe the structure of the mobile app. The users can add new sections and pages. All of them must be registered in the manifest for the app to be able to work with new functionality. Since third-party developers have no ability to make changes to the manifest of the base app, the system automatically creates a new updated manifest each time a new section or page is added from the Mobile application wizard.

note

When you register new sections and pages in the mobile app manifest, make sure the last properties of arrays and objects that determine schema sections have no extra commas. Otherwise, it leads to business logic errors.

Template for the manifest schema name: `MobileApplicationManifest[SomeWorkplaceName]Workplace`. For example, if the **Field sales** workplace is added to the mobile app, the system generates a new manifest schema that has the name `MobileApplicationManifestFieldSalesWorkplace`.

View schema sections of the mobile app manifest in the table below.

| Schema section | Description |
| --- | --- |
| ModuleGroups | Describes the properties of the mobile app module groups. |
| Modules | Describes the properties of the mobile app modules. |
| SyncOptions | Describes data synchronization parameters. |
| Models | Contains configuration of the imported app models. |
| PreferedFilterFuncType | Determines the operation to search and filter data. |
| CustomSchemas | Connects additional schemas to the mobile app. |
| Icons | Enables adding custom images to the app. |
| DefaultModuleImageId | Sets default image for UI V1. |
| DefaultModuleImageIdV2 | Sets default image for UI V2. |

All properties of a configuration object in the manifest can be divided into general groups. View detailed description in the table below.

| Group | Property | Description |
| --- | --- | --- |
| App interface properties | ModuleGroups<br>Modules<br>Icons<br>DefaultModuleImageId<br>DefaultModuleImageIdV2 | Contains properties that form the mobile app UI. For example, app sections, main menu, custom images, etc. |
| Data and business logic properties | Models<br>CustomSchemas<br>PreferedFilterFuncType | Contains properties that describe imported data as well as custom business logic for processing data in the mobile app. |
| App synchronization properties | SyncOptions | Contains a single property to synchronize data with the main Creatio app. |

## Access modifiers of a page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview\#title-1515-3 "Direct link to Access modifiers of a page")

`Terrasoft.ChangeModes` enumeration contains access modifiers.

The mobile app lets you configure **access modifiers** of section or expanded list. For example, you can disable modifying, adding and deleting records for all users in the section.

To **set up the access to section** in the read-only mode, add the section code to the schema that has the `ModuleConfig` suffix:

Set up the access to section

```js
Terrasoft.sdk.Module.setChangeModes("UsrCodeOfSomeCustomSection", [Terrasoft.ChangeModes.Read]);
```

To **set up the access to expanded list** in the read-only mode

1. **Open the schema** that has the `ModuleConfig` suffix.
2. **Add the section code**.
3. **Add the code of expanded list**.

Set up the access to expanded list

```js
Terrasoft.sdk.Details.setChangeModes("UsrCodeOfSomeCustomSection", "UsrCodeOfSomeCustomExpandedList", [Terrasoft.ChangeModes.Read]);
```

**As a result**, Creatio will forbid to add and modify corresponding section and expanded list.

Creatio lets you use several access modifiers. View the example that enables adding and modifying records and disables deleting records.

Combine access modifiers

```js
Terrasoft.sdk.Module.setChangeModes("UsrCodeOfSomeCustomSection", [Terrasoft.ChangeModes.Create, Terrasoft.ChangeModes.Update]);
```

## Controls [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview\#title-1515-4 "Direct link to Controls")

You can add the following controls to the section page:

- `Terrasoft.ColumnSet` column groups
- `Terrasoft.EmbeddedDetail` expanded lists
- standard expanded lists
- inheritor components of the `Terrasoft.RecordPanelItem` class

Use the **Mobile application wizard** to add the `Terrasoft.ColumnSet` column group, `Terrasoft.EmbeddedDetail` expanded list, standard expanded list types of controls.

To **add an inheritor component of the**`Terrasoft.RecordPanelItem` **class** to the section page:

1. **Create a class** that inherits from the `Terrasoft.RecordPanelItem` class.
2. **Define the component configuration object**.
3. **Define the class methods**.
4. **Create a section settings schema** whose code template is `Mobile[NameOfSomeCustomSection]ModuleConfig`.
5. **Implement adding the custom component** to the section page using the `addPanelItem()` method of the `Terrasoft.sdk.RecordPage` class.
6. **Add the custom schema to the mobile app manifest**.

- [Structure of mobile app manifest](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview#title-1515-1)
- [Access modifiers of a page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview#title-1515-3)
- [Controls](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/overview#title-1515-4)