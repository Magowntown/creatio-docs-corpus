<!-- Source: page_11 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/sort-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Sort** component to sort list data.

View the example of a configuration object that sorts list data below.

Example of a configuration object that sorts list data

```js
{
    "type": "crt.Sort",
    "value": "\$ItemsSorting",
    "sortItems": [\
        {\
            "attributeName": "Name",\
            "caption": "Name"\
        }\
    ],
    "valueChange": {
        "request": "crt.SortChangeRequest"
    }
}
```

* * *

```js
string type
```

Component type. `crt.Sort` for the **Sort** component.

* * *

```js
string value
```

The attribute from the `viewModelConfig` schema section.

* * *

```js
array of objects sortItems
```

Array of parameters to sort.

Parameters

| Name | Description |
| --- | --- |
| string attributeName | The attribute from the `viewModelConfig` schema section. |
| string caption | Column caption. |

* * *

```js
object valueChange
```

The `crt.SortChangeRequest` base request that opens a list of available sorting options.