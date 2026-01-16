<!-- Source: page_32 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/menu-item-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Menu item** component to add additional actions to a button menu item.

View the example of a configuration object that implements the button menu item below.

Example of a configuration object that implements the button menu item

```js
{
    "type": "crt.MenuItem",
    "caption": "Menu item",
    "clicked": {
        "request": "crt.SetViewModelAttributeRequest",
        "params": {
            "attributeName": "CalendarViewMode",
            "value": "day"
        }
    },
}
```

* * *

```js
string type
```

Component type. `crt.MenuItem` for the **Menu item** component.

* * *

```js
string caption
```

Localizable caption of button menu item.

* * *

```js
object clicked
```

The request fires when a user clicks the button menu item. Creatio lets you bind the sending of a base request or custom request handlers implemented in remote module to the button click event.