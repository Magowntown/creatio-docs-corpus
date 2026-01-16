<!-- Source: page_79 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/area-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Area** element to place the page components into multiple sections. Unlike the **Adaptive layout** element, the **Area** element places components between columns and rows arbitrarily. The **Area** element adapts the content based on the device type. Creatio Mobile displays single column **for mobile phones** and two **for tablets**.

View the example of a configuration object that places page components into multiple sections below.

Example of a configuration object that places page components into multiple sections

```js
{
    "type": "crt.Area",
    "title": "Title",
    "items": [\
        ...\
    ]
}
```

* * *

```js
string type
```

Element type. `crt.Area` for the **Area** element.

* * *

```js
string title
```

Localizable area title.

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