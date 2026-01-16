<!-- Source: page_183 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/client-schema-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

As part of transition to new architecture, the app UI was revamped in Creatio. Freedom UI shell encompasses the latest and greatest UX best practices to streamline the user workflow all while providing extensive personalization capabilities. Learn more: [Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445).

The **client module schema** is used to implement the front-end part of Creatio. The **Freedom UI page type** of the client module schema represents the front-end part of Creatio in Freedom UI. The schema structure of Freedom UI pages is the same for Creatio and Creatio Mobile. Learn more: [Freedom UI page schema](https://academy.creatio.com/documents?id=15342).

Unlike the main app, the Freedom UI page schema of the mobile app has the following differences:

- It includes only source code in JSON format.
- You cannot access it to implement business logic using custom source code.

View the Freedom UI page schema sections of the mobile app in the table below.

| Schema section | Description |
| --- | --- |
| DesignTime | RunTime |
| viewConfigDiff | viewConfig | Tree of Freedom UI Mobile components |
| viewModelConfigDiff | viewModelConfig | Simple type attribute (`string`, `number`, `boolean`), an attribute that contains nested `view model` instance (i. e., attribute that is configured using the `HandlerChain` mechanism), a custom attribute, resource attribute |
| modelConfigDiff | modelConfig | Data sources and their dependencies |

Each schema section is a JSON configuration object that distinguishes the Freedom UI page schema from the parent schema. This lets you customize Freedom UI page schemas using schema inheritance.

View the example that demonstrates the schema structure of Freedom UI pages of the mobile app in the `DesignTime` mode below.

Example that demonstrates Freedom UI page schema of the mobile app (DesignTime mode)

```js
{
    "viewConfigDiff": [{"operation":"insert","name":"ViewConfig","values":{"type":"crt.EditScreen","body":{},"actions":[],"floatActions":[]}}, ...],
    "viewModelConfigDiff": [{"operation":"insert","name":"ViewModelConfig","values":{"attributes":{}}}, ...],
    "modelConfigDiff": [{"operation":"insert","name":"ModelConfig","values":{"primaryDataSourceName":"PDS","dataSources":{},"dependencies":{}}}, ...]
}
```

Creatio merges all schemas and converts them into a resulting JSON object in the `RunTime` mode. You can see the `RunTime` mode schema sections only in the integrated developer tools provided by all supported browsers. View the example that demonstrates the resulting JSON object in the `RunTime` mode below.

Example that demonstrates result JSON object (RunTime mode)

```js
{
    "viewConfig": {
        "body": {
            "type": "crt.Tabs",
            "items": [\
                {\
                    "body": {\
                        "type": "crt.AdaptiveLayout",\
                        "items": [\
                            {\
                                "type": "crt.Area",\
                                "visible": true,\
                                "items": [\
                                    {\
                                        "value": "$Account",\
                                        "type": "crt.EditField"\
                                    }\
                                ],\
                                "title": "Profile"\
                            },\
                            {\
                                "type": "crt.Detail",\
                                "items": "ContactCareerDetailV2EmbeddedDetail",\
                                "title": "Job experience",\
                                "itemLayout": {\
                                    "type": "crt.DetailItem",\
                                    "fields": [\
                                        {\
                                            "value": "$Account",\
                                            "type": "crt.ListItemBodyField"\
                                        },\
                                        {\
                                            "value": "$Job",\
                                            "type": "crt.ListItemBodyField"\
                                        }\
                                    ]\
                                },\
                                "editColumns": [\
                                    {"columnName": "Account"},\
                                    {"columnName": "Job"}\
                                ]\
                            }\
                        ],\
                        "scrollable": true,\
                        "columns": {"tabletLandscape": [3, 7]},\
                        "padding": {"bottom": "floatingActionBottomPadding"}\
                    },\
                    "position": 0,\
                    "text": "#ResourceSystemString(Screen.DefaultTab)",\
                    "isTransparent": true\
                }\
            ]
        },
        "actions": [],
        "floatActions": [\
            {\
                "title": "#ResourceSystemString(Button.Copy)",\
                "clicked": {"request": "crt.CopyRecordRequest"}\
            },\
            {\
                "title": "#ResourceSystemString(Button.Delete)",\
                "clicked": {"request": "crt.DeleteRecordRequest"}\
            }\
        ],
        "header": {"type": "ContactCompactProfile"}
    },
    "viewModelConfig": {
        "attributes": {
            "Id": {"modelConfig": {"path": "PDS.Id"}},
            "Account": {"modelConfig": {"path": "PDS.Account"}},
            "ContactCareerDetailV2EmbeddedDetail": {
                "modelConfig": {
                    "path": "ContactCareerDetailV2EmbeddedDetailDS",
                    "cacheConfig": {},
                    "sortingConfig": {
                        "default": [{"columnName": "CreatedOn", "direction": "asc"}]
                    }
                }
            },
            "Name": {"modelConfig": {"path": "PDS.Name"}},
        }
    },
    "modelConfig": {
        "primaryDataSourceName": "PDS",
        "dataSources": {
            "PDS": {"config": {"entitySchemaName": "Contact"}},
            "ContactCareerDetailV2EmbeddedDetailDS": {
                "config": {
                    "entitySchemaName": "ContactCareer",
                    "attributes": {
                        "CreatedOn": {"path": "CreatedOn"},
                        "Account": {"path": "Account"},
                        "Job": {"path": "Job"}
                    }
                }
            }
        },
        "dependencies": {
            "ContactCareerDetailV2EmbeddedDetailDS": [\
                {"attributePath": "Contact", "relationPath": "PDS.Id"}\
            ],
            "FileDetailV2EmbeddedDetailDS": [\
                {"attributePath": "Contact", "relationPath": "PDS.Id"}\
            ]
        }
    }
}
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/client-schema-mobile\#see-also "Direct link to See also")

[Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445)

[Freedom UI page schema](https://academy.creatio.com/documents?id=15342)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/client-schema-mobile#see-also)