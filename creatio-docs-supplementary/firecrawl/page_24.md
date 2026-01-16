<!-- Source: page_24 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/syncoptions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

`SyncOptions` schema section describes the options for configuring data synchronization.

## Properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/syncoptions\#title-1253-2 "Direct link to Properties")

```js
ImportPageSize
```

The number of pages to synchronize in the same thread.

* * *

```js
PagesInImportTransaction
```

The number of threads to synchronize.

* * *

```js
SysSettingsImportConfig
```

An array of system settings to synchronize.

* * *

```js
SysLookupsImportConfig
```

An array of lookups to cache. Usually, this array includes database tables that are frequently used by users, such as types, categories, and similar items.

* * *

```js
ModelDataImportConfig
```

An array of models whose data to load during synchronization. Specify additional synchronization parameters, the list of available columns and filter conditions for each model. If you need to load a full model during synchronization, specify the object code.

Parameters

|     |     |
| --- | --- |
| Name | Model name from the `Models` schema section. |
| SyncFilter | The filter applied to the model during synchronization. The `SyncFilter` property is used to filter data while the synchronization is performed via the OData protocol.

Parameters

|     |     |
| --- | --- |
| property | Name of model column to filter. Requires the `Terrasoft.FilterTypes.Simple` filter type. |
| modelName | Name of model to filter. Specifies whether the filtering is performed by the columns of the connected model. |
| assocProperty | Connected model column by which the main model is connected. The primary column is a column to connect. |
| operation | Type of filter operation from the `Terrasoft.FilterOperation` enumeration. By default, `Terrasoft.FilterOperation.General`.

Available values

|     |     |
| --- | --- |
| General | Default filtration. |
| Any | Filtration by the `exists` filter. | |
| compareType | Comparison type of filter operation. Takes values from the `Terrasoft.ComparisonType` enumeration. By default, `Terrasoft.ComparisonType.Equal`.

Available values

|     |
| --- |
| Equal |
| LessOrEqual |
| NotEqual |
| Greater |
| GreaterOrEqual |
| Less | |
| funcArgs | An array of parameter values for the method specified in the `functionType` property. The order of the values in the `funcArgs` property must match the order of parameters of the `functionType` method. |
| name | The name of a filter or filter group. |
| valueIsMacros | Defines whether the filtered value is a macro.

Available values

|     |     |
| --- | --- |
| true | The filter uses a macro. |
| false | The filter does not use a macro. | |
| value | Value of the column from the `property` property. Requires the `Terrasoft.FilterTypes.Simple` filter type. Can be set directly by the filter value (including `null`) or a macro. Requires the `"valueIsMacros": true` property if the `value` property value is a macro from the `Terrasoft.ValueMacros` enumeration.

Available values

|     |     |
| --- | --- |
| CurrentUserContactId | ID of current user. |
| CurrentDate | Current date. |
| CurrentDateTime | Current date and time. |
| CurrentDateEnd | End of the current date. |
| CurrentUserContactName | Current contact name. |
| CurrentUserContact | ID and name of current contact. |
| SysSettings | System setting value. Requires the `macrosParams` property. |
| CurrentTime | Current time. |
| CurrentUserAccount | ID and name of current account. |
| GenerateUId | Generated ID. | |
| macrosParams | Macro parameters. Required for the `Terrasoft.ValueMacros.SysSettings` macro. |
| isNot | Specifies whether to use the negation logical operator.

Available values

|     |     |
| --- | --- |
| true | The negation logical operator is used. |
| false | The negation logical operator is not used. | |
| functionType | Function type applied to the model column specified in the `property` property. Takes values from the `Terrasoft.FilterFunctions` enumeration. Use the `funcArgs` property to specify parameter values of the filtration functions. The value to compare the function result is specified in the `value` property.

Available values

|     |     |
| --- | --- |
| SubStringOf | Determines whether the string passed as a parameter is a substring of the `property` property. |
| ToUpper | Changes the column value specified in the `property` property to uppercase. |
| EndsWith | Verifies whether the value specified in the `property` property ends with a value passed as parameter. |
| StartsWith | Verifies whether the value specified in the `property` property starts with a value passed as parameter. |
| Year | Returns year based on the `property` property value. |
| Month | Returns month based on the `property` property value. |
| Day | Returns day based on the `property` property value. |
| In | Verifies if the `property` property value is within the value range passed as the method parameter. |
| NotIn | Verifies if the `property` property value is outside the value range passed as the method parameter. |
| Like | Determines if the `property` property value matches the specified template. | | |
| QueryFilter | Configure data filtering of the specific model when synchronizing data. The `QueryFilter` property is a set of parameters in JSON that are sent in the request to the DataService service. Learn more: [Filters class](https://academy.creatio.com/documents?id=15422).

Parameters

|     |     |
| --- | --- |
| filterType | Filter type from the `Terrasoft.FilterTypes` enumeration. By default, `Terrasoft.FilterTypes.Simple`.

Available values

|     |     |
| --- | --- |
| Simple | Filter that has one condition. |
| Group | Filter that has multiple conditions. | |
| logicalOperation | The logical operation to combine a collection of filters from the `Terrasoft.FilterLogicalOperations` enumeration. Requires the `"filterType": "Terrasoft.FilterTypes.Group"`. By default, `Terrasoft.FilterLogicalOperations.And`.

Available values

|     |     |
| --- | --- |
| Or | Logical operation `OR`. |
| And | Logical operation `AND`. | |
| subfilters | A collection of filters applied to a model. Requires the Obligatory property for the filter type `"filterType": "Terrasoft.FilterTypes.Group"`. The filters are connected by the logical operation specified in the `logicalOperation` property. Each filter is a configuration filter object. | |
| SyncColumns | An array of model columns whose data to synchronize. Except from listed columns, Creatio Mobile synchronizes the system columns (`CreatedOn`, `CreatedBy`, `ModifiedOn`, `ModifiedBy`) and primary displayed columns. |

* * *

```js
SyncRules
```

Synchronization rules. Creatio applies synchronization rules for all operation modes of Creatio Mobile.

Parameters

|     |     |
| --- | --- |
| modelDataImportConfigName | Model name from the `Models` schema section. |
| importOptions | Data to synchronize. When the `modelDataImportConfigName` property is used, the `importOptions` property is ignored.

Parameters

|     |     |
| --- | --- |
| adapterType | Type of data synchronization module. Required for the `importOptions` property.

Available values

|     |     |
| --- | --- |
| Entity | The module to synchronize data from the object specified in the `entityName` property. Requires the `entityName` property. |
| Approval | The module to synchronize approvals. |
| ESN | The module to synchronize feed. | |
| entityName | The object from which to synchronize data. Required for the `Entity` value of the `adapterType` property. |
| columns | An array of model columns whose data to synchronize. If you omit the property, Creatio Mobile synchronizes all the columns. You can specify the column using one of the following templates:

- simple template
- template for column of the `lookup` type

View the examples that add model columns whose data to synchronize using different templates below.

- Simple template
- Template for column of the lookup type

```js
columns: ["Name"]
```

```js
columns: [{\
    "path": "CreatedBy",\
    "expand": true\
}]
```

Parameters (for column of the `lookup` type only)

|     |     |
| --- | --- |
| path | Column code. |
| expand | Defines whether to synchronize primary columns (`PrimaryColumnName`, `PrimaryDisplayColumnName`, `PrimaryImageColumnName`) of the `lookup` type column.

Available values

|     |     |
| --- | --- |
| true | Synchronize primary columns (`PrimaryColumnName`, `PrimaryDisplayColumnName`, `PrimaryImageColumnName`) of the `lookup` type column. |
| false | Do not synchronize primary columns (`PrimaryColumnName`, `PrimaryDisplayColumnName`, `PrimaryImageColumnName`) of the `lookup` type column. | | |
| filters | Configure data filtering of the specific model when synchronizing data. The `filters` property is a set of parameters in JSON that are sent in the request to the DataService service. | |
| related | An array of related synchronization rules. Creatio Mobile uses related synchronization rules automatically when synchronizing data.

Parameters

|     |     |
| --- | --- |
| ruleName | Code of synchronization rule. | |

Creatio lets you **apply synchronization rules in the following ways**:

- when you launch synchronization in the background or log in to the app







View the example that creates `InvoiceModule` synchronization rule for the **Invoice** section below.





Modules schema section





```js
"Modules": {
      "Invoice": {
          "screens": {
              "start": {
                  "schemaName": "MobileInvoiceGridPageSettingsFlutterTest"
              },
              "edit": {
                  "schemaName": "MobileInvoiceRecordPageSettingsFlutterTest"
              }
          },
          "syncRules": ["InvoiceModule"],
          "Group": "main",
          "Model": "Invoice",
          "Position": 5,
          "isStartPage": false,
          "Title": "InvoiceSectionTitle",
          "Hidden": false
      }
},
"SyncOptions": {
      "ModelDataImportConfig": [\
          {\
              "Name": "Invoice",\
              "IsAdministratedByRights": true,\
              "SyncColumns": [\
                  "Contact",\
                  "Account",\
                  "Number",\
                  "StartDate",\
                  "PaymentStatus",\
                  "Owner",\
                  "Currency",\
                  "CurrencyRate"\
              ]\
          }\
      ],
      "SyncRules": {
          "InvoiceModule": {
              "modelDataImportConfigName": "Invoice",
              "related": [{\
                  "ruleName": "InvoiceModule_InvoiceProduct"\
              }]
          },
          "InvoiceModule_InvoiceProduct": {
              "importOptions": {
                  "adapterType": "Entity",
                  "entityName": "InvoiceProduct"
              }
          }
      }
},
```







**As a result**, Creatio Mobile will synchronize data of the **Invoice** section when you log in to the app and in the background.

- when you work with a section







1. Add synchronization rules to the Freedom UI page schema that configures the section.

     View the example that adds synchronization rules to the `MobileInvoiceGridPageSettings` schema that configures the **Invoice** Freedom UI section below.



     viewModelConfig schema section





     ```js
     "viewModelConfig": {
         "attributes": {
             "Items": {
                 "viewModelConfig": {
                     "cacheConfig": {
                         "syncRuleName": "InvoiceModule"
                     },
                 },
                 "name": "Attribute_Items"
             },
             "name": "Attributes"
         },
         "name": "ViewModelConfig"
     }
     ```

2. Add synchronization rules to the Freedom UI page schema that configures the section page.

     View the example that adds synchronization rules to the `MobileInvoiceRecordPageSettings` schema that configures the invoice page of the **Invoice** Freedom UI section below.



     viewModelConfig schema section





     ```js
     "viewModelConfig": {
         "cacheConfig": {
             "syncRuleName": "InvoiceModule_InvoiceProduct"
         },
         "attributes": {...}
         "name": "ViewModelConfig"
     }
     ```


**As a result**, Creatio Mobile will synchronize data of the **Invoice** section automatically when you work with the section.

When you hide the section, bound synchronization rules no longer apply.

* * *

View the example of `SyncOptions` schema section below.

Example of the exists filter

```js
{
    "SyncOptions": {
        /* The number of pages to synchronize in the same thread. */
        "ImportPageSize": 100,
        /* The number of threads to synchronize. */
        "PagesInImportTransaction": 5,
        /* An array of system settings to synchronize. */
        "SysSettingsImportConfig": [\
            "SchedulerDisplayTimingStart", "PrimaryCulture", "PrimaryCurrency", "MobileApplicationMode", "CollectMobileAppUsageStatistics", "CanCollectMobileUsageStatistics", "MobileAppUsageStatisticsEmail", "MobileAppUsageStatisticsStorePeriod", "MobileSectionsWithSearchOnly", "MobileShowMenuOnApplicationStart", "MobileAppCheckUpdatePeriod", "ShowMobileLocalNotifications", "UseMobileUIV2"\
        ],
        /* An array of lookups to cache. Usually, this array includes database tables that are frequently used by users, such as types, categories, and similar items. */
        "SysLookupsImportConfig": [\
            "ActivityCategory", "ActivityPriority", "ActivityResult", "ActivityResultCategory", "ActivityStatus", "ActivityType", "AddressType", "AnniversaryType", "InformationSource", "MobileApplicationMode", "OppContactInfluence", "OppContactLoyality", "OppContactRole", "OpportunityStage", "SupplyPaymentDelay", "SupplyPaymentState", "SupplyPaymentType"\
        ],
        /* An array of models whose data to load during synchronization. */
        "ModelDataImportConfig": [\
            {\
                /* Model name from the "Models" schema section. */\
                "Name": "ActivityParticipant",\
                /* The filter applied to the model during synchronization. */\
                "SyncFilter": {\
                    /* Name of model column to filter. */\
                    "property": "Participant",\
                    /* Name of model to filter. */\
                    "modelName": "ActivityParticipant",\
                    /* Connected model column by which the main model is connected. */\
                    "assocProperty": "Activity",\
                    /* Type of filter operation from the "Terrasoft.FilterOperation" enumeration. */\
                    "operation": "Terrasoft.FilterOperations.Any",\
                    /* Defines whether the filtered value is a macro. */\
                    "valueIsMacros": true,\
                    /* Value of the column from the "property" property. */\
                    "value": "Terrasoft.ValueMacros.CurrentUserContact"\
                },\
                /* Configure data filtering of the specific model when synchronizing data. */\
                "QueryFilter": {\
                    /* The logical operation to combine a collection of filters from the "Terrasoft.FilterLogicalOperations" enumeration. */\
                    "logicalOperation": 0,\
                    /* Filter type from the "Terrasoft.FilterTypes" enumeration. */\
                    "filterType": 6,\
                    /* Root schema name. */\
                    "rootSchemaName": "ActivityParticipant",\
                    "items": {\
                        "ActivityFilter": {\
                            "filterType": 5,\
                            /* Expression of the left side of the filter condition. */\
                            "leftExpression": {\
                                /* "Column" expression type. */\
                                "expressionType": 0,\
                                /* The column to filter. */\
                                "columnPath": "Activity.[ActivityParticipant:Activity].Id"\
                            },\
                            /* A collection of filters applied to a model. */\
                            "subFilters": {\
                                "logicalOperation": 0,\
                                "filterType": 6,\
                                "rootSchemaName": "ActivityParticipant",\
                                "items": {\
                                    "ParticipantFilter": {\
                                        "filterType": 1,\
                                        /* Comparison type of filter operation. */\
                                        "compareType": 3,\
                                        "leftExpression": {\
                                            "expressionType": 0,\
                                            "columnPath": "Participant"\
                                        },\
                                        "rightExpression": {\
                                            "expressionType": 1,\
                                            /* Function type applied to the model column specified in the "property" property. */\
                                            "functionType": 1,\
                                            "macrosType": 2\
                                        }\
                                    }\
                                }\
                            }\
                        }\
                    }\
                },\
                /* An array of model columns whose data to synchronize. */\
                "SyncColumns": [\
                    "Title", "StartDate", "DueDate", "Status", "Result", "DetailedResult", "ActivityCategory", "Priority", "Owner", "Account", "Contact", "ShowInScheduler", "Author", "Type"\
                ]\
            },\
            /* Option to load all model columns. */\
            {\
                "Name": "ActivityType",\
                "SyncColumns": []\
            }\
        ],
        /* Synchronization rules. */
        "SyncRules": {
            "ApprovalModule": {
                "importOptions": {
                    "adapterType": "Approval"
                }
            },
            "ActivityModule": {
                /* Data to synchronize. */
                "importOptions": {
                    /* Type of data synchronization module. */
                    "adapterType": "Entity",
                    /* The object from which to synchronize data. */
                    "entityName": "Activity"
                },
                /* An array of related synchronization rules. */
                "related": [\
                    {\
                        /* Code of synchronization rule. */\
                        "ruleName": "ActivityModule_Participant"\
                    }\
                ]
            }
        }
    }
}
```

- [Properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/syncoptions#title-1253-2)