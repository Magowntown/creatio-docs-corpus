<!-- Source: page_171 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/column-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Column** element to arrange page content vertically.

View the example of a configuration object that arranges page content vertically below.

Example of a configuration object that arranges page content vertically

```js
{
    "type": "crt.Column",
    "scrollable": true,
    "items": [\
        ...\
    ],
    "padding": {
        "left": "medium"
    }
}
```

* * *

```js
string type
```

Element type. `crt.Column` for the **Column** element.

* * *

```js
boolean scrollable
```

A flag that determines whether to scroll element data. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | Scrolling is enabled. Creatio Mobile lets applies scrolling when the **Column** element has nested Freedom UI Mobile components. |
| false | Scrolling is disabled. |

* * *

```js
array of objects items
```

The array of nested Freedom UI Mobile components.

Parameters

|     |     |
| --- | --- |
| value | The name of attribute from the `viewModelConfig` schema section. |
| type | Type of nested component. |

* * *

```js
object padding
```

The container padding settings. The property can apply a single value to all sides or provide a specific value for each side of nested components.

Available values

|     |     |
| --- | --- |
| none | Zero padding. |
| small | Small padding. |
| medium | Medium padding. |
| large | Large padding. |