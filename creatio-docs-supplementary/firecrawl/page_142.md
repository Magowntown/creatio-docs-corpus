<!-- Source: page_142 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/read-only-field-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Read-only field** component to display the component data. Before you use the component, make sure that the `viewModelConfig` schema section includes the attribute bound to the **Read-only field** component.

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

Creatio Mobile lets you display the `text`, `lookup`, `double`, `integer`, `date`, `boolean`, `phone`, `email`, `web`, `rich text`, and `color` **Read-only field** component types.

View the example of a configuration object that displays data below.

Example of a configuration object that displays data

```js
{
    "type": "crt.ViewField",
    "value": "$SomeAttribute",
    "maxLines": 2,
    "label": {
        "visible": true,
        "value": "Title",
        "position": "left"
    },
    "launchConfig": {
        "name": "ConfigurationOptionalName",
        "type": "phone",
        "bindingColumn": "CommunicationType",
        "binding": {
            ...
        },
    }
}
```

* * *

```js
string type
```

Component type. `crt.ViewField` for the **Read-only field** component.

* * *

```js
string value
```

The name of attribute from the `viewModelConfig` schema section.

* * *

```js
number maxLines
```

Maximum number of lines in the component to display.

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

* * *

```js
object launchConfig
```

Add link to the component. If you omit the `type` property, Creatio analyzes the values of the `binding` and `bindingColumn` properties. The `bindingColumn` property configures the content provider launched based on the value set in the `binding` property.

Parameters

| Name | Description |
| --- | --- |
| string name | Link name. |
| string type | Link type.

Available values

|     |     |
| --- | --- |
| phone | Creatio Mobile opens the dialer app. |
| email | Creatio Mobile opens the email client. |
| map | Creatio Mobile opens the map app. |
| uri | Creatio Mobile opens an arbitrary link. | |
| string bindingColumn | Name of the column that determines the type of opened link. |
| object binding | Record ID that determines the type of opened link. |