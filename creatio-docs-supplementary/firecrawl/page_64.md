<!-- Source: page_64 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/timeline-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Timeline** component to enable users to view the history of communication regarding the record as well as records linked to it in chronological order. You can specify the sorting column for most objects in the timeline except for "Feed" and "File" that are always sorted by creation date. Users can like and comment feed records in the timeline. The component also includes the message composer functionality.

Use the **Timeline** component to display the linked records of the following objects:

- Attachments
- Activities
- Emails
- Calls
- Feed messages

The timeline displays the primary display value and creation date of linked records. You can customize the columns to display in the timeline addon of the relevant object using no-code tools. Learn more: [Customize an object column to display in the Timeline component](https://academy.creatio.com/documents?id=15046&anchor=title-15046-1).

View the example of a configuration object that implements the timeline below.

Example of a configuration object that implements the timeline

```js
{
    "type": "crt.Timeline",
    "masterSchemaId": "$Id",
    "items": [\
        {\
            "type": "crt.TimelineTile",\
            "linkedColumn": "Contact",\
            "sortedByColumn": "CreatedOn",\
            "data": {\
                "schemaName": "Activity",\
                "schemaType": "Email",\
                "columns": [\
                    {\
                        "columnName": "Status"\
                    }\
                ],\
                "filter": {\
                    "columnName":"Type",\
                    "columnValue":"e2831dec-cfc0-df11-b00f-001d60e938c6"\
                }\
            }\
        }\
    ]
}
```

* * *

```js
string type
```

Component type. `crt.Timeline` for the **Timeline** component.

* * *

```js
string masterSchemaId
```

Parent object column to create a filter in the timeline tile.

* * *

```js
array of objects items
```

The array of timeline tiles.

Parameters

| Name | Description |
| --- | --- |
| string type | Tile type. By default, `crt.TimelineTile`. |
| string linkedColumn | The tile object column that is linked to the parent object. |
| string sortedByColumn | The tile object column to sort timeline data. |
| object data | Configuration object of timeline data.

Parameters

| Name | Description |
| --- | --- |
| string schemaName | Name of the tile schema. |
| string schemaType | The tile type.

Available values

|     |
| --- |
| Email |
| Call |
| Feed |
| SysFile | |
| array of objects columns | The list of tile columns to load. |
| object filter | Additional filter. | |

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/timeline-mobile\#see-also "Direct link to See also")

[Customize the Timeline component](https://academy.creatio.com/documents?id=15046)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/timeline-mobile#see-also)