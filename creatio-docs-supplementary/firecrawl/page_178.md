<!-- Source: page_178 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/defaultmoduleimageid-and-defaultmoduleimageidv2#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: advanced

Properties are designed to set unique default image IDs for newly created sections or sections that don't contain IDs of the images in the `Icon` or `IconV2` properties of the `Modules` schema section of the configuration object manifest.

Installation of unique image identifiers

```js
// Custom interface V1 default image ID.
"DefaultModuleImageId": "423d3be8-de6b-4f15-a81b-ed454b6d03e3",
// Custom interface V2 default image ID.
"DefaultModuleImageIdV2": "1c92d522-965f-43e0-97ab-2a7b101c03d4"
```