<!-- Source: page_52 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/customschemas#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: advanced

The `CustomSchemas` schema section is designed for connecting additional schemas to the mobile app (custom schemas with source code in JavaScript) that expand the functionality. This can be additional classes implemented by developers as part of a project, or utility classes that implement functions to simplify development, etc.

The value of the property is an array with the names of connected custom schemas.

Connect additional custom schemas for registering actions and utilities

```js
// Connect additional custom schemas.
"CustomSchemas": [\
    // Custom action registration schema.\
    "MobileActionCheckIn",\
    // Custom utility schema.\
    "CustomMobileUtilities"\
]
```