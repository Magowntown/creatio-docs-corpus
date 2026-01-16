<!-- Source: page_109 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Some Freedom UI Mobile components use data sources to load and display data. For example, **List item preview**, **Embedded lists**. The data source configuration object is a part of the Freedom UI page schema and lets you customize the data loading.

## Implement the data source [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#title-15088-1 "Direct link to Implement the data source")

1. **Convert the existing page to Freedom UI** if needed. Instructions: [Configure the Freedom UI page](https://academy.creatio.com/documents?id=15087&anchor=title-15087-1) (step 1).

2. **Open the Freedom UI page schema**.

3. **Create the data source configuration object**.

View the configuration object example that implements the data source of the `Opportunity` object below.



Configuration object example that implements the data source





```js
"modelConfig": {
       "primaryDataSourceName": "PDS",
       "dataSources": {
           "PDS": {
               "type": "crt.EntityDataSource",
               "config": {
                   "entitySchemaName": "Opportunity",
                   "attributes": {
                       "Title": {"path": "Title", "name": "PDS_Attribute_Title"}
                   }
               }
           }
       }
}
```









View the common parameters of the data source configuration object in the table below.



| Parameter | Parameter description |
| --- | --- |
| primaryDataSourceName | The data source name |
| type | Data source type. If you omit the value, Creatio will use the `crt.EntityDataSource` type. |
| entitySchemaName | The name of the entity schema. Parameter of the data source type. |
| attributes | The list of attributes to load. Parameter of the data source type. |

4. **Add an attribute** that includes the data source.


1. Create an attribute in the `attributes` property.
2. Add the data source name to the `path` property.

View the example that adds the `CustomAttribute` attribute below. The `CustomAttribute` attribute stores the data source of the `Opportunity` object.

Example that adds an attribute

```js
"viewModelConfig": {
    "attributes": {
        "CustomAttribute": {
            "modelConfig": {
                "path": "PDS"
            }
        }
    }
}
```

5. **Bind the data source** to the Freedom UI Mobile component. To do this, add the attribute that stores data source data to the `items` property.

View the example that binds the `CustomAttribute` attribute to the Freedom UI Mobile component below.



Example that binds the data source to the Freedom UI Mobile component





```js
"viewConfig": {
       "type": "crt.List",
       "items": "CustomAttribute",
       ...
}
```









For this example, the Freedom UI page loads data from the `Opportunity` object and displays it in the **List** component.

6. **Configure the Freedom UI page**.


1. Go to the component whose `name` property is set to `settings`.
2. Add configuration objects as string.

View the example that configures the Freedom UI page below.

Example that configures the Freedom UI page

```js
[\
    {\
        "operation": "insert",\
        "name": "settings",\
        "values": {\
            "entitySchemaName": "UsrSection",\
            "settingsType": "RecordPage",\
            "localizableStrings": {},\
            "columnSets": [],\
            "operation": "insert",\
            "details": [],\
            "viewConfigDiff": "[{\"operation\":\"merge\",\"type\":\"crt.ListScreen\",\"items\":\"CustomAttribute\",...}]",\
            "viewModelConfigDiff": "[{\"operation\":\"merge\",\"attributes\":{\"CustomAttribute\":{\"modelConfig\":{\"path\":\"PDS\"}}}]",\
            "modelConfigDiff": "[{\"operation\":\"merge\",\"primaryDataSourceName\":\"PDS\",\"dataSources\":{\"PDS\":{\"type\":\"crt.EntityDataSource\",\"config\":{\"entitySchemaName\":\"Opportunity\",\"attributes\":{\"Title\":{\"path\":\"Title\",\"name\":\"PDS_Attribute_Title\"}}}}}}]"\
\
        }\
    }\
]
```

7. **Save the changes**.


**As a result**, you will be able to use data sources to customize a Freedom UI page based on your business goals. For example, filtering or sorting data.

## Filter data [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#title-15088-2 "Direct link to Filter data")

Creatio lets you use the following filtering types:

- Simple data filtering. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-3)
- Data filtering based on data from another data source. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-4)

### Simple data filtering [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#title-15088-3 "Direct link to Simple data filtering")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-1).

2. **Set up filtering**.


1. Create an attribute that implements the filter in the `attributes` property.
2. Add the attribute name to the `filterAttributes` property.

View the example that sets up the filtering below. The `CustomFilter` attribute implements the filtering of records from the `Opportunity` object.

Example that sets up the filtering

```js
"viewModelConfig": {
    "attributes": {
        "Items": {
            "modelConfig": {
                "path": "PDS",
                "filterAttributes": [\
                    {"name": "CustomFilter"}\
                ]
            }
        },
        "CustomFilter": {
            "value": {
                "items": {
                    "63871ecc-40a1-4f00-a7e5-9c5099a76ea4": {
                        "filterType": 4,
                        "comparisonType": 3,
                        "isEnabled": true,
                        "trimDateTimeParameterToDate": false,
                        "leftExpression": {"expressionType": 0, "columnPath": "Owner"},
                        "isAggregative": false,
                        "key": "63871ecc-40a1-4f00-a7e5-9c5099a76ea4",
                        "dataValueType": 10,
                        "leftExpressionCaption": "Owner",
                        "referenceSchemaName": "Contact",
                        "rightExpressions": [\
                            {\
                                "expressionType": 2,\
                                "parameter": {"dataValueType": 10, "value": "410006e1-ca4e-4502-a9ec-e54d922d2c00"}\
                            }\
                        ]
                    }
                },
                "logicalOperation": 0,
                "isEnabled": true,
                "filterType": 6,
                "rootSchemaName": "Opportunity"
            }
        }
    }
}
```

3. **Configure the Freedom UI page**.


1. Go to the component whose `name` property is set to `settings`.
2. Add configuration objects as string.

View the example that configures the Freedom UI page below.

Example that configures the Freedom UI page

```js
[\
    {\
        "operation": "insert",\
        "name": "settings",\
        "values": {\
            "entitySchemaName": "UsrSection",\
            "settingsType": "RecordPage",\
            "localizableStrings": {},\
            "columnSets": [],\
            "operation": "insert",\
            "details": [],\
            "viewConfigDiff": "[{\"operation\":\"merge\",...}]",\
            "vieModelConfigDiff": "[{\"operation\":\"merge\",\"attributes\":{\"Items\":{\"modelConfig\":{\"path\":\"PDS\",\"filterAttributes\":[{\"name\":\"CustomFilter\"}]}},\"CustomFilter\":{\"value\":{\"items\":{\"63871ecc-40a1-4f00-a7e5-9c5099a76ea4\":{\"filterType\":4,\"comparisonType\":3,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{\"expressionType\":0,\"columnPath\":\"Owner\"},\"isAggregative\":false,\"key\":\"63871ecc-40a1-4f00-a7e5-9c5099a76ea4\",\"dataValueType\":10,\"leftExpressionCaption\":\"Owner\",\"referenceSchemaName\":\"Contact\",\"rightExpressions\":[{\"expressionType\":2,\"parameter\":{\"dataValueType\":10,\"value\":\"410006e1-ca4e-4502-a9ec-e54d922d2c00\"}}]}},\"logicalOperation\":0,\"isEnabled\":true,\"filterType\":6,\"rootSchemaName\":\"Opportunity\"}}}}]",\
            "modelConfigDiff": "[{\"operation\":\"merge\",...}]"\
\
        }\
    }\
]
```

4. **Save the changes**.


**As a result**, the received data will be filtered.

Creatio lets you **use multiple filters**. To do this, combine the attributes that implement the filters using the `And` operator.

### Data filtering based on data from another data source [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#title-15088-4 "Direct link to Data filtering based on data from another data source")

Creatio lets you filter data from one data source based on data from another data source. For example, you can filter data from the **Expanded list**, **Attachment**, **Feed** components based on data from another data source. To do this, bind the data sources using **dependencies**.

To bind the data sources:

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-1).

2. **Implement the data source of component**. To do this, create an attribute that implements the component data source.

View the example that implements the data source of the `ContactCareerDetailDS` expanded list below.



Example that implements the data source





```js
"modelConfig": {
       "primaryDataSourceName": "PDS",
       "dataSources": {
           ...,
           "ContactCareerDetailDS": {
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
       ...,
}
```

3. **Set up dependencies**. To do this, bind the root schema to the parent root schema.

View the example that binds the `ContactCareer` root schema to the parent `Contact` root schema below. The `ContactCareer` root schema contains a Contact column that is bound to the `Id` column of the parent `Contact` root schema.



Example that sets up dependencies





```js
"modelConfig": {
       "primaryDataSourceName": "PDS",
       "dataSources": {
           ...,
       },
       "dependencies": {
           "ContactCareerDetailDS": [\
               {"attributePath": "Contact", "relationPath": "PDS.Id"}\
           ],
           ...,
       }
}
```









View the common properties of the `dependencies` property in the table below.



| Property | Property description |
| --- | --- |
| attributePath | The root schema column that connects the root schema to parent root schema. The `relationPath` property contains the parent root schema column. |
| relationPath | The parent root schema column that connects the parent root schema to the root schema. The `attributePath` property contains the root schema column. |

4. **Configure the Freedom UI page**.


1. Go to the component whose `name` property is set to `settings`.
2. Add configuration objects as string.

View the example that configures the Freedom UI page below.

Example that configures the Freedom UI page

```js
[\
    {\
        "operation": "insert",\
        "name": "settings",\
        "values": {\
            "entitySchemaName": "UsrSection",\
            "settingsType": "RecordPage",\
            "localizableStrings": {},\
            "columnSets": [],\
            "operation": "insert",\
            "details": [],\
            "viewConfigDiff": "[{\"operation\":\"merge\",...}]",\
            "viewModelConfigDiff": "[{\"operation\":\"merge\",...}]",\
            "modelConfigDiff": "[{\"operation\":\"merge\",\"primaryDataSourceName\":\"PDS\",\"dataSources\":{...,\"ContactCareerDetailDS\":{\"config\":{\"entitySchemaName\":\"ContactCareer\",\"attributes\":{\"CreatedOn\":{\"path\":\"CreatedOn\"},\"Account\":{\"path\":\"Account\"},\"Job\":{\"path\":\"Job\"}}}}},\"dependencies\":{\"ContactCareerDetailDS\":[{\"attributePath\":\"Contact\",\"relationPath\":\"PDS.Id\"}],...,}}]"\
\
        }\
    }\
]
```

5. **Save the changes**.


**As a result**, the `ContactCareerDetailDS` expanded list will display filtered data based on data from the `Contact` data source.

## Sort data [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#title-15088-5 "Direct link to Sort data")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-1).

2. **Set up sorting**. To do this, configure the sorting conditions in the `sortingConfig` property.

View the example that sets up the sorting below. The `Opportunity` object records are sorted by `CreatedOn` column in ascending order.



Example that adds an attribute





```js
"viewModelConfig": {
       "attributes": {
           "Items": {
               "modelConfig": {
                   "path": "PDS",
                   "sortingConfig": {
                       "default": [\
                           {"columnName": "CreatedOn", "direction": "asc"}\
                       ]
                   }
               }
           }
       },
       ...
}
```









View the common properties of the `sortingConfig` property in the table below.



| Property | Property description |
| --- | --- |
| columnName | Name of the column by which to sort data. |
| direction | Sorting order. Available values: `asc` (ascending), `desc` (descending). |

3. **Configure the Freedom UI page**.


1. Go to the component whose `name` property is set to `settings`.
2. Add configuration objects as string.

View the example that configures the Freedom UI page below.

Example that configures the Freedom UI page

```js
[\
    {\
        "operation": "insert",\
        "name": "settings",\
        "values": {\
            "entitySchemaName": "UsrSection",\
            "settingsType": "RecordPage",\
            "localizableStrings": {},\
            "columnSets": [],\
            "operation": "insert",\
            "details": [],\
            "viewConfigDiff": "[{\"operation\":\"merge\",...}]",\
            "viewModelConfigDiff": "[{\"operation\":\"merge\",\"attributes\":{\"Items\":{\"modelConfig\":{\"path\":\"PDS\",\"sortingConfig\":{\"default\":[{\"columnName\":\"CreatedOn\",\"direction\":\"asc\"}]}}}},...}]",\
            "modelConfigDiff": "[{\"operation\":\"merge\",...,}}]"\
\
        }\
    }\
]
```

4. **Save the changes**.


**As a result**, the received data will be sorted.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile\#see-also "Direct link to See also")

[Set up mobile app workplaces](https://academy.creatio.com/documents?id=1391)

[Set up mobile application section page](https://academy.creatio.com/documents?id=1394)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101)

[Customize Freedom UI page for Creatio Mobile](https://academy.creatio.com/documents?id=15087)

- [Implement the data source](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-1)
- [Filter data](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-2)
  - [Simple data filtering](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-3)
  - [Data filtering based on data from another data source](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-4)
- [Sort data](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#title-15088-5)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/data-operations-mobile#see-also)