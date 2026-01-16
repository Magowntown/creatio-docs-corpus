<!-- Source: page_134 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/embedded-list-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Embedded list** component to add embedded list. Before you use the component, make sure that the Freedom UI page schema includes the data source. Learn more: [Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088).

View the example of a configuration object that adds embedded list below.

Example of a configuration object that adds embedded list

```js
{
    "type": "crt.Detail",
    "items": "ItemAttribute",
    "title": "Contact in opportunity",
    "itemLayout": {
        "type": "crt.ListItem",
        "body": [\
            {\
                "value": "\$Contact"\
            }\
        ]
    },
    "editColumns": [\
        {\
            "columnName": "Contact"\
        }\
    ],
    "tools": [\
        {\
            "type": "crt.Button",\
            "text": "Add",\
            "menuTitle": "Select",\
            "menuItems": [\
                {\
                    "type": "crt.MenuItem",\
                    "caption": "By filter",\
                    "clicked": [\
                        {\
                            "request": "crt.CreateActivityParticipantDetailRequest",\
                            "params": {\
                                "attributeName": "ActivityParticipantDetailV2EmbeddedDetail",\
                                "filtersConfig": {\
                                    "filterAttributes": [\
                                        {\
                                            "loadOnChange": true,\
                                            "name": "ParticipantFilterAttribute",\
                                        }\
                                    ],\
                                }\
                            }\
                        }\
                    ]\
                },\
                {\
                    "type": "crt.MenuItem",\
                    "caption": "All",\
                    "clicked": [\
                        {\
                            "request": "crt.CreateActivityParticipantDetailRequest",\
                            "params": {\
                                "attributeName": "ActivityParticipantDetailV2EmbeddedDetail",\
                            }\
                        }\
                    ]\
                },\
            ]\
        }\
    ]
}
```

* * *

```js
string type
```

Component type. `crt.Detail` for the **Embedded list** component.

* * *

```js
string items
```

The attribute from the `viewModelConfig` schema section.

* * *

```js
string title
```

The component title.

* * *

```js
object itemLayout
```

Configuration object that configures parameters of component to display in the **Embedded list** component.

Parameters

| Name | Description |
| --- | --- |
| string type | The component type to display in the **Embedded list** component. In most cases, `crt.ListItem`. |
| array of objects body | Parameters of the `crt.ListItem` component type. |

* * *

```js
array of objects editColumns
```

List of editable columns.

* * *

```js
array of objects tools
```

List of embedded Freedom UI Mobile components. For example, buttons. Embedded components are displayed in the top right of the **Embedded list** component.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/embedded-list-mobile\#see-also "Direct link to See also")

[Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/embedded-list-mobile#see-also)