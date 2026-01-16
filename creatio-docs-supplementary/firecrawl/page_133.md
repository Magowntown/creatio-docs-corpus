<!-- Source: page_133 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-model-configuration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Add the following model configurations to the manifest:

1. `Contact`. Specify list page, view and edit page schema names, required models, model extension modules and model pages.
2. `Contact address`. Specify only the model extension module.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-model-configuration\#title-1504-1 "Direct link to Example implementation")

Models schema section

```js
// Importing models.
"Models": {
    // "Contact" model.
    "Contact": {
        // List page schema.
        "Grid": "MobileContactGridPage",
        // Display page schema.
        "Preview": "MobileContactPreviewPage",
        // Edit page schema.
        "Edit": "MobileContactEditPage",
        // The names of the models the "Contact" model depends on.
        "RequiredModels": [\
            "Account", "Contact", "ContactCommunication", "CommunicationType", "Department",\
            "ContactAddress", "AddressType", "Country", "Region", "City", "ContactAnniversary",\
            "AnniversaryType", "Activity", "SysImage", "FileType", "ActivityPriority",\
            "ActivityType", "ActivityCategory", "ActivityStatus"\
        ],
        // Model extensions..
        "ModelExtensions": [\
            "MobileContactModelConfig"\
        ],
        // Model page extensions.
        "PagesExtensions": [\
            "MobileContactRecordPageSettingsDefaultWorkplace",\
            "MobileContactGridPageSettingsDefaultWorkplace",\
            "MobileContactActionsSettingsDefaultWorkplace",\
            "MobileContactModuleConfig"\
        ]
    },
    // "Contact addresses" model.
    "ContactAddress": {
        // List, display and edit pages were generated automatically.
        // Model extensions..
        "ModelExtensions": [\
            "MobileContactAddressModelConfig"\
        ]
    }
}
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-model-configuration#title-1504-1)