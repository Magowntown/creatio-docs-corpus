<!-- Source: page_163 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-start-page-and-menu-sections#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Set up the application sections:

1. Main menu sections: **Contacts**, **Accounts**.
2. The application starting page: the **Contacts** section.

Strings containing the section titles should be created in the **LocalizableStrings** manifest schema block:

- `ContactSectionTitle` with the "Contacts" value.
- `AccountSectionTitle` with the "Accounts" value.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-start-page-and-menu-sections\#title-1506-1 "Direct link to Example implementation")

Modules schema section

```js
// Mobile application modules.
"Modules": {
    // "Contact" section.
    "Contact": {
        // The application menu group that contains the section.
        "Group": "main",
        // Model name that contains the section data.
        "Model": "Contact",
        // Section position in the main menu group.
        "Position": 0,
        // Section title.
        "Title": "ContactSectionTitle",
        // Custom image import to section.
        "Icon": {
            // Unique image ID.
            "ImageId": "4c1944db-e686-4a45-8262-df0c7d080658"
        },
        // Custom image import to section.
        "IconV2": {
            // Unique image ID.
            "ImageId": "9672301c-e937-4f01-9b0a-0d17e7a2855c"
        },
        // Menu display checkbox.
        "Hidden": false
    },
    // "Account" section.
    "Account": {
        // The application menu group that contains the section.
        "Group": "main",
        // Model name that contains the section data.
        "Model": "Account",
        // Section position in the main menu group.
        "Position": 1,
        // Section title.
        "Title": "AccountSectionTitle",
        // Custom image import to section.
        "Icon": {
            // Unique image ID.
            "ImageId": "c046aa1a-d618-4a65-a226-d53968d9cb3d"
        },
        // Custom image import to section.
        "IconV2": {
            // Unique image ID.
            "ImageId": "876320ef-c6ac-44ff-9415-953de17225e0"
        },
        // Menu display checkbox.
        "Hidden": false
    }
}
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-start-page-and-menu-sections#title-1506-1)