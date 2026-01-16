<!-- Source: page_83 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/contact-compact-profile-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

The component is available if you have the **Customer 360** app installed.

Use the **Contact compact profile** component to display main data of a contact:

- photo
- full name
- birth date
- age
- local time
- country

The component behavior is pre-configured and non-editable.

View the example of a configuration object that displays main contact data below.

Example of a configuration object that displays main contact data

```js
{
    "type": "crt.ContactCompactProfile"
}
```

* * *

```js
string type
```

Component type. `crt.ContactCompactProfile` for the **Contact compact profile** component.