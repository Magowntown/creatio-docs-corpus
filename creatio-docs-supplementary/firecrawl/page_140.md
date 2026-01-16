<!-- Source: page_140 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-menu#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Setting up the mobile application menu with two groups – the main group and the **Sales** group.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-menu\#title-1505-1 "Direct link to Example implementation")

ModuleGroups schema section

```js
// Mobile application module groups.
"ModuleGroups": {
    // Main menu group setup.
    "main": {
        // Group position in the main menu.
        "Position": 0
    },
    // [Sales] menu group setup.
    "sales": {
        // Group position in the main menu.
        "Position" 1
    }
}
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/examples/set-up-the-menu#title-1505-1)