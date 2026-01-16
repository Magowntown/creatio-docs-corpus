<!-- Source: page_129 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/expansion-panel-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Expansion panel** element to place the page components into multiple sections. Unlike the **Area** element, the **Expansion panel** element can be expanded. The **Expansion panel** element adapts the content based on the device type. Creatio Mobile displays single column **for mobile phones** and two **for tablets**.

View the example of a configuration object that places page components into multiple sections below.

Example of a configuration object that places page components into multiple sections

```js
{
    "type": "crt.ExpansionPanel",
    "title": "Job experience",
    "items": [\
        {\
            "type": "crt.DataGrid",\
            "items": "ContactCareerDetailV2EmbeddedDetail",\
            "verticalScroll": false,\
            "columns": [\
                {\
                    "code": "Job",\
                    "sticky": true,\
                },\
                {\
                    "code": "Account",\
                    "caption": "My account",\
                    "width": 200,\
                }\
            ]\
        }\
    ],
    "tools": [\
        {\
            "type": "crt.Button",\
            "icon": "add-button-icon",\
            "iconPosition": "only-icon",\
            "color": "default",\
            "size": "medium",\
            "clicked": {\
                "request": "crt.CreateRecordRequest",\
                "params": {\
                    "entityName": "ContactCareer",\
                    "defaultValues": [\
                        {\
                            "attributeName": "Contact",\
                            "value": "\$Id"\
                        }\
                    ]\
                }\
            },\
            "visible": true,\
            "clickMode": "default"\
        }\
    ],
    "name": "ContactCareerDetailV2EmbeddedDetail"
}
```

* * *

```js
string type
```

Element type. `crt.ExpansionPanel` for the **Expansion panel** element.

* * *

```js
string title
```

Localizable title of the **Expansion panel** element.

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
array of objects tools
```

List of nested Freedom UI Mobile components. For example, buttons. Nested components are displayed in the top right of the **Expansion panel** element.

Parameters

|     |     |
| --- | --- |
| type | Type of nested component. |
| text | Name of nested component. |

* * *

```js
boolean expanded
```

The flag that determines whether to expand an element. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | An element is expanded. |
| false | An element is collapsed. |