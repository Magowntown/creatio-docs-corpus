<!-- Source: page_29 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/account-compact-profile-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

The component is available if you have the **Customer 360** app installed.

Use the **Account compact profile** component to display main data of an account:

- logo
- name
- local time
- country

The component behavior is pre-configured and non-editable.

View the example of a configuration object that displays main account data below.

Example of a configuration object that displays main account data

```js
{
    "type": "crt.AccountCompactProfile"
}
```

* * *

```js
string type
```

Component type. `crt.AccountCompactProfile` for the **Account compact profile** component.