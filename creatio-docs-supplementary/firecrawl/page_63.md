<!-- Source: page_63 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/tabs-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Tabs** element to add a tab area. The tab area lets you display content grouped by multiple criteria. That way, you can publish more required information without overcrowding the page. Creatio Mobile lets you reorder tabs.

View the example of a configuration object that adds tab areas below.

Example of a configuration object that adds tab areas

```js
{
    "type": "crt.Tabs",
    "isScrollable": true,
    "items": [\
        {\
            "position": 1,\
            "text": "Tab 1",\
            "body": {\
                ...\
            }\
        },\
        {\
            "position": 2,\
            "text": "Tab 2",\
            "body": {\
                ...\
            }\
        }\
    ]
}
```

* * *

```js
string type
```

Element type. `crt.Tabs` for the **Tabs** element.

* * *

```js
boolean isScrollable
```

The flag that determines whether to scroll element data. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | Scrolling is enabled. |
| false | Scrolling is disabled. |

* * *

```js
array of objects items
```

The array of tabs.

Parameters

|     |     |
| --- | --- |
| position | Tab order. |
| text | Tab name. |
| body | The array of nested Freedom UI Mobile components. |
| isTransparent | The flag that determines whether the tab has a background. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The tab has background. |
| false | The tab has no background. | |