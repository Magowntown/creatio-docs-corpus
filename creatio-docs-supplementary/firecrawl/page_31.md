<!-- Source: page_31 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/combobox-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Combobox** component to add the `lookup` type field that has extended customization features. For example, create a record directly from the `lookup` type field. Before you use the component, make sure that the `viewModelConfig` schema section includes the attribute bound to the **Combobox** component.

View the example that adds an attribute to the Freedom UI page schema below.

Example that adds an attribute to the Freedom UI page schema

```js
{
    "viewModelConfig": {
        "attributes": {
            "SomeAttribute": {
                "modelConfig": {
                    "path": "PDS.Title"
                },
                "name": "SomeAttribute"
            }
        }
    }
}
```

View the example of a configuration object that lets you add a new contact directly from the `lookup` type field below.

Example of a configuration object that lets you add a new contact directly from the lookup type field

```js
{
    "value": "$Contact",
    "type": "crt.ComboBox",
    "name": "Case_PrimaryTab_Body_primaryColumnSet_Contact",
    "clicked": {
        "request": "crt.OpenLookupPageRequest",
        "params": {
            "entitySchemaName": "Contact",
            "features": {
                "create": {
                    "enabled": true
                }
            },
            "addButtonClicked": {
                "request": "crt.CreateRecordRequest",
                "params": {
                    "entityName": "Contact",
                    "defaultValues": [{\
                        "attributeName": "Name",\
                        "value": "$Number"\
                    }]
                }
            }
        }
    },
    "secondaryDisplayValue": "Account.Phone"
}
```

* * *

```js
string type
```

Component type. `crt.ComboBox` for the **Combobox** component.

* * *

```js
string value
```

The name of attribute from the `viewModelConfig` schema section.

* * *

```js
string name
```

The name of the lookup type field whose functionality is extended.

* * *

```js
object clicked
```

The request fires when a user clicks the button. Creatio lets you bind the sending of a base request or custom request handlers implemented in remote module to the button click event.

* * *

```js
string secondaryDisplayValue
```

Display an additional column that includes contextual information related to the selected records in the **Combobox** component. For example, show relation of a contact to an account.