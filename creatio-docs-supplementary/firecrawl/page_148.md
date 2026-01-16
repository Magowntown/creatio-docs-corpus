<!-- Source: page_148 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/field-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Field** component to modify the component data. Before you use the component, make sure that the `viewModelConfig` schema section includes the attribute bound to the **Field** component.

View the example that adds an attribute to the Freedom UI page schema below.

Example that adds an attribute to the Freedom UI page schema

```js
{
    "viewModelConfig": {
        "attributes": {
            "SomeAttribute": {
                "modelConfig": {
                    "path": "PDS.Title"
                },
                "name": "SomeAttribute"
            }
        }
    }
}
```

Creatio Mobile lets you modify the `text`, `lookup`, `double`, `integer`, `date`, `boolean`, `phone`, `email`, `web`, `rich text`, and `color` **Field** component types.

View the example of a configuration object that modifies data below.

Example of a configuration object that modifies data

```js
{
    "type": "crt.EditField",
    "value": "$SomeAttribute",
    "minLines": 2,
    "maxLines": 5,
    "hint": "Enter title",
    "readOnly": false,
    "label": {
        "visible": true,
        "value": "Title",
        "position": "left"
    }
}
```

* * *

```js
string type
```

Component type. `crt.EditField` for the **Field** component.

* * *

```js
string value
```

The name of attribute from the `viewModelConfig` schema section.

* * *

```js
number minLines
```

Minimum number of lines in the component. Available for the `text`, `email`, `web` **Field** component types.

* * *

```js
number maxLines
```

Maximum number of lines in the component. Available for the `text`, `email`, `web` **Field** component types.

* * *

```js
string hint
```

The hint that Creatio Mobile displays in the component when you omit the component value.

* * *

```js
boolean readOnly
```

The flag that sets the component to read-only. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The component is editable. |
| false | The component is not editable. |

* * *

```js
object label
```

The component title. If you omit a value, Creatio Mobile displays the `DataSchemaAttribute.caption` property value.

Parameters

| Name | Description |
| --- | --- |
| boolean visible | The flag that makes the component label visible. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | The component label is visible. |
| false | The component label is not visible. | |
| string value | The label value. By default, the title is the same as the title of the corresponding model field. |
| string position | The label position. By default, `top`.

Available values

|     |     |
| --- | --- |
| left | Display the label to the left of the component. |
| right | Display the label to the right of the component. |
| top | Display the label above the component. |
| bottom | Display the label below the component. | |