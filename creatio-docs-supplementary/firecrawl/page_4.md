<!-- Source: page_4 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/calendar-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Calendar** component to display calendar events.

View the example of a configuration object that embeds external content into a page below.

Example of a configuration object that embeds external content into a page

```js
{
    "type": "crt.Calendar",
    "templateValuesMapping": {
        "startColumn": "StartDate",
        "endColumn": "DueDate",
        "titleColumn": "Title",
        "notesColumn": "Notes",
        "colorizationColumn": "Status.Color"
    },
    "colorizationType": "byField",
    "items": "ItemsAttribute",
    "dateRange": "CalendarSelectedDate",
    "viewMode": "CalendarViewMode",
    "focusDate": "CalendarPickerFocusDate",
    "createItem": {
        "request": "crt.CreateCalendarRecordRequest",
        "params": {
            "entityName": "Activity",
            "defaultValues": [\
                {\
                    "attributeName": "ShowInScheduler",\
                    "value": "true"\
                }\
            ]
        }
    }
}
```

* * *

```js
string type
```

Component type. `crt.Calendar` for the **Calendar** component.

* * *

```js
object templateValuesMapping
```

Data source columns to bind.

Parameters

| Name | Type | Description |
| --- | --- | --- |
| string startColumn | Required | Column that stores start date of calendar events. |
| string endColumn | Required | Column that stores end date of calendar events. |
| string titleColumn | Required | Column that stores title of calendar events. |
| string notesColumn | Optional | Column that stores additional details of calendar events. |
| string colorizationColumn | Optional | Column that stores custom color of calendar events. |

* * *

```js
string colorizationType
```

The data source attribute that stores calendar colorization modes from the `viewModelConfig` schema section. Requires the `colorizationColumn` property.

Set up calendar colorization

1. Add a column that stores a custom color to data source. Instructions: [Implement the data source](https://academy.creatio.com/documents?id=15088&anchor=title-15088-1) (steps 1-3).

View the configuration object example that implements the data source of the `Activity` object below.



Configuration object example that implements the data source





```js
"modelConfig": {
       "primaryDataSourceName": "PDS",
       "dataSources": {
           "PDS": {
               "config": {
                   "entitySchemaName": "Activity",
                   "attributes": {
                       "Status.Color": {"path": "Status.Color"}
                   }
               }
           }
       }
}
```

2. Register a custom column in the mobile app manifest.


1. Open the mobile app manifest.
2. Go to the `SyncOptions` schema section → `ModelDataImportConfig`.
3. Add a configuration object of a custom column.
4. Save the changes.

View the configuration object example that registers a custom column of the `ActivityStatus` object below.

Configuration object example that registers a custom column

```js
/* Synchronization settings.*/
"SyncOptions": {
    ...,

    /* An array of models that loads data during synchronization. */
    "ModelDataImportConfig": [\
\
        /* "ActivityStatus" model configuration. */\
        {\
            "Name": "ActivityStatus",\
            ...,\
            /* An array of the model columns for which data is imported. */\
            "SyncColumns": [\
                "Color"\
            ]\
        },\
        ...,\
    ]
}
```

* * *

```js
string items
```

The data source attribute from the `viewModelConfig` schema section.

* * *

```js
string dateRange
```

The data source attribute that stores time interval from the `viewModelConfig` schema section.

* * *

```js
string viewMode
```

The data source attribute that stores calendar display modes from the `viewModelConfig` schema section. For example, day, 3 days, week.

* * *

```js
string focusDate
```

The data source attribute that stores date from the `viewModelConfig` schema section. For example, current date.

* * *

```js
object createItem
```

Configuration object that configures parameters of calendar event to create in the **Calendar** component. For example, tasks.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/calendar-mobile\#see-also "Direct link to See also")

[Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/calendar-mobile#see-also)