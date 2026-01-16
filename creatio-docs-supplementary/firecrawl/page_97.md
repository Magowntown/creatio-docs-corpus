<!-- Source: page_97 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/preferedfilterfunctype#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

The property defines the operation used for searching and filtering data in the section, detail and lookup lists. The value for the property is specified in the `Terrasoft.FilterFunctions` enumeration. The list of filtering functions is available in table.

## Filtering functions (Terrasoft.FilterFunctions) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/preferedfilterfunctype\#title-1253-2 "Direct link to Filtering functions (Terrasoft.FilterFunctions)")

```js
SubStringOf
```

Determines whether a string passed as an argument, is a substring of the `property` string.

```js
ToUpper
```

Returns values of the column specified in the `property` in relation to upper list.

```js
EndsWith
```

Verifies if the `property` column value ends with a value passed as argument.

```js
StartsWith
```

Verifies if the `property` column value starts with a value passed as argument.

```js
Year
```

Returns year based on the `property` column value.

```js
Month
```

Returns month based on the `property` column value.

```js
Day
```

Returns day based on the `property` column value.

```js
In
```

Checks if the `property` column value is within the value range passed as the function argument.

```js
NotIn
```

Checks in the `property` column value is outside the value range passed as the function argument.

```js
Like
```

Determines if the `property` column value matches the specified template.

If the current property is not explicitly initialized on the manifest, then by default the `Terrasoft.FilterFunctions.StartWith` function is used for search and filtering, as this ensures the proper indexes are used in the SQLite database tables.

- [Filtering functions (Terrasoft.FilterFunctions)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/preferedfilterfunctype#title-1253-2)