<!-- Source: page_61 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/pagenavigator#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

The `Terrasoft.PageNavigator` class manages the life cycle of the pages. The class enables opening and closing of the pages, updating of the irrelevant data and storing the page history.

## Methods [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/pagenavigator\#title-1253-2 "Direct link to Methods")

```js
forward(openingPageConfig)
```

Method opens page according to the properties of the `openingPageConfig` configuration parameter object. Main properties of this object are listed in the table.

openingPageConfig object properties

|     |     |
| --- | --- |
| controllerName | name of the controller class |
| viewXType | view type according to xtype |
| type | page type from the `Terrasoft.core.enums.PageType` enumeration |
| modelName | name of the page model |
| pageSchemaName | name of the page schema in configuration |
| isStartPage | flag indicating that the page is a start page. If previously the pages have been opened, they will be closed |
| isStartRecord | flag indicating that the view/edit page should be the first after the list. If there are other opened pages after the list, they will be closed |
| recordId | Id of the record of the page being opened |
| detailConfig | settings of the standard detail |

```js
backward()
```

The method is closing the page.

```js
markPreviousPagesAsDirty(operationConfig)
```

Method marks all previous pages as irrelevant. After returning to previous pages, the `refreshDirtyData()` method is called for each page. The method re-loads the data or updates the data basing on the `operationConfig` object.

```js
refreshPreviousPages(operationConfig, currentPageHistoryItem)
```

Method re-loads data for all previous pages and updates the data basing on the `operationConfig` object. If the value is set for the `currentPageHistoryItem` parameter, the method performs the same actions for the previous pages.

```js
refreshAllPages(operationConfig, excludedPageHistoryItems)
```

Method re-loads data for all pages or updates the data basing on the `operationConfig` object. If the `excludedPageHistoryItems` parameter is set, the method does not update the specified pages.

- [Methods](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/pagenavigator#title-1253-2)