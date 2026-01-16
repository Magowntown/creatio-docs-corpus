<!-- Source: page_125 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/flex-container-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Flex container** element to lay out its nested components vertically or horizontally.

View the example of a configuration object that adds Freedom UI Mobile components to the **Flex container** element below.

Example of a configuration object that adds Freedom UI Mobile components to the Flex container element

```js
{
    "type": "crt.FlexContainer",
    "items": [\
        {\
            "type": "crt.Link",\
            "caption": "Some link caption"\
        },\
        {\
            "type": "crt.Button",\
            "caption": "Some button caption"\
        }\
    ],
    "gap": 16,
    "padding": {
        "left": "medium",
        "right": "medium"
    },
    "direction": "row",
    "justifyContent": "center",
    "wrap": "nowrap"
}
```

* * *

```js
string type
```

Element type. `crt.FlexContainer` for the **Flex container** element.

* * *

```js
array of objects items
```

The array of nested Freedom UI Mobile components. The `items` property of an **Flex container** component can include Freedom UI Mobile layout elements and Freedom UI Mobile components.

Parameters

|     |     |
| --- | --- |
| type | Type of nested component. |
| caption | Caption of nested component. |

* * *

```js
number gap
```

The column and row spacing between the nested components in the `flex` container. The property applies a single value to both vertical and horizontal gaps and is able to accept numbers only.

* * *

```js
object padding
```

The `flex` container padding settings. The property can apply a single value to all sides or provide a specific value for each side of nested components. The property can accept numbers, strings, and the available values listed below.

Available values

|     |     |
| --- | --- |
| none | Zero padding. |
| small | Small padding. |
| medium | Medium padding. |
| large | Large padding. |

* * *

```js
string direction
```

The orientation and direction of the `flex` container’s main axis to which `flex` components align. By default, `row`.

Available values

|     |     |     |
| --- | --- | --- |
| row | The nested components of the `flex` container align horizontally. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_flex_direction_row.png) |
| column | The nested components of the `flex` container align vertically. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_flex_direction_column.png) |
| row-reverse | The nested components of the `flex` container align horizontally in reverse. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_flex_direction_row_reverse.png) |
| column-reverse | The nested components of the `flex` container align vertically in reverse. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_flex_direction_column_reverse.png) |

* * *

```js
string justifyContent
```

Space distribution along the main axis. Defines how the Creatio Mobile distributes space between and around nested components along the main axis of the `flex` container. By default, `start`.

Available values

|     |     |     |
| --- | --- | --- |
| start | Pack nested components from the start of the main `flex` container axis. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_justify_content_flex_start.png) |
| end | Pack nested components from the end of the main `flex` container axis. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_justify_content_flex_end.png) |
| center | Pack nested components around the center of the main `flex` container axis. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_justify_content_center.png) |
| space-between | The blocks of the `flex` container are distributed evenly. The first nested component is flush from the start of the main axis, the other is flush from the end. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/FlexContainer/8.0/scr_justify_content_flex_space_between.png) |

* * *

```js
string wrap
```

Sets whether the nested components are forced onto one line or can wrap onto multiple lines in the `flex` container. By default, `nowrap`.

Available values

|     |     |     |
| --- | --- | --- |
| nowrap | The nested components are forced onto one line in the `flex` container. | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/FreedomUiLayoutComponents/8.2/scr_wrap_nowrap.png) |
| wrap | The nested components are forced onto multiple lines in the `flex` container. | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/FreedomUiLayoutComponents/8.2/scr_wrap_wrap.png) |
| wrap-reverse | The nested components are forced onto multiple lines in the `flex` container in reverse. | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/FreedomUiLayoutComponents/8.2/scr_wrap_wrap_reverse.png) |