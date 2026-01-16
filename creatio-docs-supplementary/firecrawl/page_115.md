<!-- Source: page_115 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/data-grid-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Data grid** component to add and edit table data.

View the example of a configuration object that adds table data below.

Example of a configuration object that adds table data

```js
{
    "type": "crt.DataGrid",
    "features": {
        "editable": {
            "enable": true
        },
        "rows": {
            "toolbar": true
        }
    },
    "rowTitle": "\$Account",
    "columns": [\
        {\
            "code": "Name",\
            "width": 200,\
            "sticky": true,\
            "cellView": {\
                "type": "crt.ViewField",\
                "value": "\$Name",\
                "maxLines": 3,\
                "label": {\
                    "visible": false\
                }\
            },\
            "readonly": true\
        },\
        {\
            "code": "CreatedOn"\
        },\
        {\
            "code": "DoNotUseEmail"\
        },\
        {\
            "code": "Age"\
        }\
    ],
    "sorting": [\
        {\
            "columnCode": "Name",\
            "direction": "asc"\
        }\
    ],
    verticalScroll: true
}
```

* * *

```js
string type
```

Component type. `crt.DataGrid` for the **Data grid** component.

* * *

```js
string features
```

Additional component features.

Parameters

| Name | Description |
| --- | --- |
| object editable | Manages the editing of data.

Parameters

| Name | Description |
| --- | --- |
| boolean enable | The flag that determines whether to edit component data. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The component data is editable. |
| false | The component data is not editable. | | |
| object rows | Additional features of component rows.

Parameters

| Name | Description |
| --- | --- |
| boolean toolbar | The flag that determines whether to display available actions. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | Available actions are displayed. |
| false | Available actions are not displayed. | | |

* * *

```js
string rowTitle
```

Pre-configured and non-editable column name. When you set the `rowTitle` property, Creatio Mobile ignores the `sticky` property value.

* * *

```js
array of objects columns
```

Array of columns to load.

Parameters

| Name | Description |
| --- | --- |
| number id | Unique column identifier. If you omit a value, Creatio Mobile uses the `code` property value as an identifier. |
| string code | Column name. |
| string caption | Column caption. If you omit a value, Creatio Mobile receives the `caption` property value from data source. |
| number dataValueType | Column data type. |
| number width | Column width. If you omit a value, Creatio Mobile uses out-of-the-box column width (120px). |
| boolean hidden | The flag that determines whether to hide a column. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | A column is hidden. |
| false | A column is shown. | |
| boolean sticky | The flag that determines whether to freeze a column. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | A column is frozen. |
| false | A column is not frozen. | |
| boolean readonly | The flag that sets the column to read-only. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The column is editable. |
| false | The column is not editable. | |
| object cellView | Parameters that determine conditions to view and edit column. List of parameters depends on column type. |

* * *

```js
array of objects sorting
```

Sort component data.

Parameters

| Name | Description |
| --- | --- |
| string columnCode | Column name. |
| string direction | The sorting order.

Available values

|     |     |
| --- | --- |
| asc | Ascending. |
| desc | Descending. |
| none | The sorting order is not defined. | |

* * *

```js
boolean verticalScroll
```

The flag that determines whether to scroll component data. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | Scrolling is enabled. |
| false | Scrolling is disabled. |