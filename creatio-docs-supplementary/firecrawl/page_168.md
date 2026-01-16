<!-- Source: page_168 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/filter-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Filter** component to filter data.

View the example of a configuration object that filters data below.

Example of a configuration object that filters data

```js
{
    "type": "crt.RelatedDetailItem",
    "moduleName": "Activity",
    "relationOptions": {
        "detailColumn": "Opportunity",
        "masterColumn": "Id",
        "parentRecordId": "$Id"
    },
    "filterAttributes": [\
        {\
            "name": "ActivityDetail_Filter"\
        }\
    ],
    "caption": "Attachments",
    "parentModuleName": "Opportunity"
}
```

* * *

```js
string type
```

Component type. `crt.RelatedDetailItem` for the **Filter** component.

* * *

```js
string moduleName
```

The name of module that was customized in the manifest.

* * *

```js
object relationOptions
```

Configuration object to create a related filter based on the parent model.

Parameters

| Name | Description |
| --- | --- |
| string detailColumn | The child object. |
| string masterColumn | The parent object column that is linked to the child object. |
| string parentRecordId | The object column that is linked to the parent object. |

* * *

```js
array of objects filterAttributes
```

Additional filters.

Parameters

| Name | Description |
| --- | --- |
| string name | The attribute that implements the filter from the `viewModelConfig` schema section. |

* * *

```js
string caption
```

Link name.

* * *

```js
string parentModuleName
```

Name of the Classic UI form page.