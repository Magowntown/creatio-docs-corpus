<!-- Source: page_141 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/models#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

The Models property contains imported application models. Each model in a property is described by a configuration object with a corresponding name. The model configuration object properties are listed in table.

## Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/models\#title-1253-2 "Direct link to Configuration object properties")

```js
Grid
```

Model list page schema name. The page will be generated automatically with the following name: `Mobile[Model_name][Page_type]Page`.

```js
Preview
```

Preview page schema name for model element. The page will be generated automatically with the following name: `Mobile[Model_name][Page_type]Page`.

```js
Edit
```

Edit page schema name for model element. The page will be generated automatically with the following name: `Mobile[Model_name][Page_type]Page`.

```js
RequiredModels
```

Names of the models that the current model depends on. All models, whose columns are added to the current model, as well as columns for which the current model has external keys.

```js
ModelExtensions
```

Model extensions. An array of schemas, where additional model settings are implemented (adding business rules, events, default values, etc.).

```js
PagesExtensions
```

Model page extensions. An array of schemas where additional settings for various page types are implemented (adding details, setting titles, etc.).

- [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/models#title-1253-2)