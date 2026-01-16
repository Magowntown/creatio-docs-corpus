<!-- Source: page_157 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/use-the-substring-search-function-for-data-search#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Use the substring search function for data search.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/use-the-substring-search-function-for-data-search\#title-1503-1 "Direct link to Example implementation")

PreferedFilterFuncType schema section

```js
// Substring search function is used to search for data.
"PreferedFilterFuncType": "Terrasoft.FilterFunctions.SubStringOf"
```

Important

If the function specified as the data filtering function in the `PreferedFilterFuncType` schema section is not `Terrasoft.FilterFunctions.StartWith`, then indexes will not be used while searching database records.

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/use-the-substring-search-function-for-data-search#title-1503-1)