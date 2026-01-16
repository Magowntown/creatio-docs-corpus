<!-- Source: page_48 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/quick-filter-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Quick filter** component to filter data by custom conditions, date/time, or lookup values. Before you use the component, make sure that the `viewModelConfig` schema section includes the attribute bound to the **Quick filter** component.

View the example that adds an attribute to the Freedom UI page schema below.

Example that adds an attribute to the Freedom UI page schema

```js
{
    "viewModelConfig": {
        "attributes": {
            "My_QuickFilter_Value": {
                "value": null
            },
            "My_Converter_Arg": {
                "value": {
                    "quickFilterType": "lookup",
                    "target": {
                    "viewAttributeName": "Items",
                    "filterColumn": "Category"
                    }
                }
            },
            "My_Filter": {
                "from": "My_QuickFilter_Value",
                "converter": "crt.QuickFilterAttributeConverter : \$My_Converter_Arg"
            },
            "Items": {
                "modelConfig": {
                    "path": "PDS",
                    "filterAttributes": [\
                        {\
                            "loadOnChange": true,\
                            "name": "My_Filter"\
                        }\
                    ]
                }
            }
        }
    }
}
```

View the example of a configuration object that filters the lookup values below.

Example of a configuration object that filters the lookup values

```js
{
    "name": "My_QuickFilter",
    "type": "crt.QuickFilter",
    "filterType": "lookup",
    "config": {
        "caption": "Select category",
        "icon": "person-button-icon",
        "iconPosition": "left-icon",
        "entitySchemaName": "AccountCategory"
    }
}
```

Once you select a filter value, Creatio Mobile stores it to the attribute whose name is `QuickFilterCaption_Value`. For this example, `My_QuickFilter_Value`.

View the example of a configuration object that filters data by custom condition below.

Example of a configuration object that filters data by custom condition

```js
{
    "name": "QuickFilter_Custom",
    "type": "crt.QuickFilter",
    "config": {
        "caption": "Show drafts",
        "defaultValue": true,
        "approachState": true
    },
    "filterType": "custom"
    }
```

* * *

```js
string type
```

Component type. `crt.QuickFilter` for the **Quick filter** component.

* * *

```js
string filterType
```

Type of quick filter.

Available values

|     |     |
| --- | --- |
| lookup | Filter that filters the lookup values. |
| date-range | Filter that filters the date/time values. |
| custom | Filter that filters data by custom conditions. |

* * *

```js
object config
```

Parameters of quick filter.

Parameters

| Name | Type | Description |
| --- | --- | --- |
| string caption | Required | Title of the quick filter. Creatio Mobile displays title if no value is selected. |
| string icon | Required | Icon of the quick filter. The property is supported by the `date-range` and `lookup` quick filter types. You can select any icon that is supported by the `icon` property of **Button** component. |
| string iconPosition | Required | Position of the icon relative to the quick filter caption. By default, `left-icon`. The property is supported by the `date-range` and `lookup` quick filter types.

Available values

|     |     |
| --- | --- |
| only-text | Do not display the icon. Display only the quick filter caption. |
| left-icon | Display the icon to the left of the quick filter caption. |
| right-icon | Display the icon to the right of the quick filter caption. |
| only-icon | Display only the icon. Do not display the quick filter caption. | |
| string defaultValue | Optional | Out-of-the-box value of quick filter.

Parameters of the `date-range` quick filter type

| Name | Type | Description |
| --- | --- | --- |
| string start | Required | Column that stores out-of-the-box start date of quick filter. |
| string end | Required | Column that stores out-of-the-box end date of quick filter. |
| string macros | Required | Macro that determines out-of-the-box time interval of quick filter. For example, `macros: "[#currentWeek#]"`. |

Available values of the `custom` quick filter type

|     |     |
| --- | --- |
| true | Out of the box, quick filter is enabled. Default value. |
| false | Out of the box, quick filter is disabled. | |
| string entitySchemaName | Required | Entity schema whose data is displayed in the quick filter of the `lookup` type. |
| string recordsFilter | Optional | Filter to filter lookup values. |
| string cacheConfig | Optional | Manages caching of lookup values. |
| boolean approachState | Optional | The flag that specifies whether the quick filter of the `custom` type is reversible. For example, quick filter is changed to "Show open cases" when section list displays only closed cases. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The quick filter is not reversible. |
| false | The quick filter is reversible. | |