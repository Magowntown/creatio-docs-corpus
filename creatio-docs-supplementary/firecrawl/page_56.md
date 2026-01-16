<!-- Source: page_56 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/list-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **List** component to add lists. Creatio Mobile displays data received from a data source as a scrolling list on the full screen.

View the example of a configuration object that adds the list below.

Example of a configuration object that adds the list

```js
{
    "type": "crt.List",
    "items": "$Items",
    "itemLayout": {
        "type": "crt.ListItem",
        "title": "$PDS_Name"
    }
}
```

* * *

```js
string type
```

Component type. `crt.List` for the **List** component.

* * *

```js
string items
```

The attribute from the `viewModelConfig` schema section.

* * *

```js
object itemLayout
```

Configuration object that configures parameters of a list item to display in the **List** component.

Parameters

| Name | Description |
| --- | --- |
| string type | The component type to display in the **List** component. In most cases, `crt.ListItem`. |
| string title | The data source attribute from the `viewModelConfig` schema section. |