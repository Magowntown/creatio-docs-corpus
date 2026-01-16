<!-- Source: page_175 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/positioned-expansion-panel-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Positioned expansion panel** element to place the page components into multiple sections. The element includes the following elements:

- Title
- Container that has Freedom UI Mobile components expanded
- Static container that has Freedom UI Mobile components

The element lets you display specified nested components and at the same time hide other nested components.

View the example of a configuration object that places page components into multiple sections below.

Example of a configuration object that places page components into multiple sections

```js
{
    "type": "crt.PositionedExpansionPanel",
    "title": "Filters",
    "toggleItems": [\
        {\
            "type": "crt.Button",\
            "text": "Show canceled"\
        }\
    ],
    "items": [\
        {\
            "type": "crt.Calendar",\
            "templateValuesMapping": {\
                "startColumn": "StartDate",\
                "endColumn": "DueDate",\
                "titleColumn": "Title",\
                "notesColumn": "Notes"\
            },\
            "highlightedStartDate": "Calendar_highlightedStartDate",\
            "items": "Items"\
        }\
    ],
    "tools": [\
        {\
            "type": "crt.Button",\
            "text": "Days"\
        }\
    ],
    "expanded": true
}
```

* * *

```js
string type
```

Element type. `crt.PositionedExpansionPanel` for the **Positioned expansion panel** element.

* * *

```js
string title
```

Localizable title of the **Positioned expansion panel** element.

* * *

```js
array of objects toggleItems
```

List of nested Freedom UI Mobile components that are added to the container and can be expanded.

Parameters

|     |     |
| --- | --- |
| type | Type of nested component. |
| text | Name of nested component. |

* * *

```js
array of objects items
```

The array of nested Freedom UI Mobile components that are added to the static container. The `items` property of a **Positioned expansion panel** element can include Freedom UI Mobile layout elements and Freedom UI Mobile components. We recommend adding Freedom UI Mobile components that require significant space on the page to a static container. For example, **Calendar**, **List**. If you need to add several components to a static container, specify fixed component width and height. Otherwise, nested components are hidden.

* * *

```js
array of objects tools
```

List of nested Freedom UI Mobile components. For example, buttons. Nested components are displayed in the top right of the **Positioned expansion panel** element.

Parameters

|     |     |
| --- | --- |
| type | Type of nested component. |
| text | Name of nested component. |

* * *

```js
string position
```

The container position. By default, `top`.

Available values

|     |     |
| --- | --- |
| left | Display the container to the left of the element. |
| right | Display the container to the right of the element. |
| top | Display the container above the element. |
| bottom | Display the container below the element. |

* * *

```js
boolean expanded
```

The flag that determines whether to expand element container. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | An element is expanded. |
| false | An element is collapsed. |