<!-- Source: page_12 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/adaptive-layout-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Adaptive layout** element to place the page components into multiple sections. Freedom UI page has the **Adaptive layout** element out of the box. Unlike the **Area** element, the **Adaptive layout** element places components between columns and rows based on a configured layout. The **Adaptive layout** element adapts the content based on the device type and screen orientation.

Creatio Mobile displays the Freedom UI page content as follows:

- A **smartphone** displays content in a single column.
- A **tablet in portrait mode** displays 2 columns that have the same width.
- A **tablet in landscape mode** displays 2 columns. The first column has 30% width, and the second column has 70% width.

View the example of a configuration object that places page components into multiple columns below.

Example of a configuration object that places page components into multiple columns

```js
{
    "scrollable": true,
    "columns": {
        "phonePortrait": 1,
        "phoneLandscape": 1,
        "tabletPortrait": [1, 1],
        "tabletLandscape": [3, 7]
    },
    "items": [\
        {\
            "value": "$Title",\
            "type": "crt.EditField",\
            "layoutConfig": {\
                "column": 2,\
                "row": 1\
            }\
        },\
        {\
            "value": "$LeadType",\
            "type": "crt.EditField",\
            "layoutConfig": {\
                "column": 1,\
                "row": 1\
            }\
        },\
        {\
            "value": "$Type",\
            "type": "crt.EditField",\
            "layoutConfig": {\
                "column": 1,\
                "row": 2\
            }\
        },\
    ]
}
```

* * *

```js
string type
```

Element type. `crt.AdaptiveLayout` for the **Adaptive layout** element.

* * *

```js
boolean scrollable
```

A flag that determines whether to scroll element data. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | Scrolling is enabled. Creatio Mobile applies scrolling when the **Adaptive layout** element has nested Freedom UI Mobile components. |
| false | Scrolling is disabled. |

* * *

```js
object columns
```

A set of fixed-width columns that include other components. Column number and size based on the device type and screen orientation.

Parameters

|     |     |
| --- | --- |
| phonePortrait | Column settings in mobile device portrait mode. |
| phoneLandscape | Column settings in mobile device landscape mode. |
| tabletPortrait | Column settings in tablet portrait mode. |
| tabletLandscape | Column settings in tablet landscape mode. |

* * *

```js
array of objects items
```

The array of nested Freedom UI Mobile components. The `items` property of an **Adaptive layout** element can include Freedom UI Mobile layout elements and Freedom UI Mobile components.

Parameters

|     |     |
| --- | --- |
| value | The name of attribute from the `viewModelConfig` schema section. |
| type | Type of nested component. |
| layoutConfig | The number of columns and rows for nested component.

Parameters

|     |     |
| --- | --- |
| column | Number of columns for nested component. |
| row | Number of rows for nested component. |

Creatio Mobile handles nested Freedom UI Mobile components as follows:

1. Creatio adds components **without the**`layoutConfig` **property** to every column step-by-step.
2. Creatio adds components that **include the**`layoutConfig` **property** to the corresponding column and row. Column and row numbering starts from 1.
3. Creatio adds components that **do not have the column number** specified in the source code to every column step-by-step. |

* * *

```js
object padding
```

The container padding settings. The property can apply a single value to all sides or provide a specific value for each side of nested components. The property can accept numbers, strings, and the available values listed below.

Available values

|     |     |
| --- | --- |
| none | Zero padding. |
| small | Small padding. |
| medium | Medium padding. |
| large | Large padding. |