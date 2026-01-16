<!-- Source: page_101 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/modules#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

A mobile application module is an application section. Each module in the `Modules` configuration object manifest describes a configuration object with properties given in table. The name of the configuration section object must match the name of the model that provides section data.

## Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/modules\#title-1253-2 "Direct link to Configuration object properties")

```js
Group
```

The application menu group that contains the section. Set by the string containing the menu section name from the `ModuleGroups` schema section of the manifest configuration object.

```js
Model
```

Model name that contains the section data. Set by the string containing the name of one of the models included in the `Models` schema section of the manifest configuration object.

```js
Position
```

Section position in the main menu group. Set by a numeric value starting with 0.

```js
Title
```

Section title. String with the section title localized value name. Section title localized value name should be added to the **LocalizableStrings** manifest schema block.

```js
Icon
```

This property designed to import custom images to the version 1 user interface menu section.

```js
IconV2
```

This property designed to import custom images to the version 2 user interface menu section.

```js
Hidden
```

Checkbox that defines a section is displayed in the menu (`true` – hidden, `false` – displayed). Optional property. By default – `false`.

- [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/modules#title-1253-2)