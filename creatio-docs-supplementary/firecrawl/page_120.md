<!-- Source: page_120 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/list-item-preview-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **List item preview** component to preview a list item.

View the example of a configuration object that previews a list item below.

Example of a configuration object that previews a list item

```js
{
    "type": "crt.ListItem",
    "title": "\$Name",
    "subtitles": ["\$Account"],
    "body": [\
        {\
            "value": "\$JobTitle"\
        },\
        {\
            "value": "\$MobilePhone"\
        }\
    ],
    "action": {
        "type": "crt.Button",
        "caption": "Open",
        "clicked": {...}
    },
    "showEmptyValues": true,
    "icon": "\$Photo"
}
```

* * *

```js
string type
```

Component type. `crt.ListItem` for the **List item preview** component.

* * *

```js
string title
```

The attribute from the `viewModelConfig` schema section. Creatio Mobile displays the title above the content.

* * *

```js
array of strings subtitles
```

The attribute from the `viewModelConfig` schema section. Creatio Mobile displays the subtitle below the list item title on a single line.

* * *

```js
array of strings body
```

The array of attributes from the `viewModelConfig` schema section that are attached to the component. Creatio Mobile displays single column **for mobile phones** and two **for tablets**.

Parameters

| Name | Description |
| --- | --- |
| string value | The attribute from the `viewModelConfig` schema section. |

* * *

```js
object action
```

The Freedom UI Mobile component that is attached to the **List Item preview** component. The component executes an action. For example, button. Creatio Mobile displays the component to the right of the **List Item preview** component. The parameters of attached component depend on the component type.

* * *

```js
boolean showEmptyValues
```

A flag that enables displaying empty values of fields that are specified in the `body` property. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | Display empty values of fields. |
| false | Do not display empty values of fields. |

* * *

```js
string icon
```

List item icon. Creatio Mobile displays the icon of `image` type field. The `icon` property includes the `DataSchemaAttribute.caption` property value. If the value of `image` type field is omitted, Creatio Mobile displays the first two letters of the `image` type field.