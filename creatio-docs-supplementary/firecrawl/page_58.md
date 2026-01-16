<!-- Source: page_58 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/icons#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

This property is designed to import custom images to the mobile application.

It is set by the configuration objects array, each containing properties from the table.

## Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/icons\#title-1253-2 "Direct link to Configuration object properties")

```js
ImageListId
```

Image list ID.

```js
ImageId
```

Custom image ID from the `ImageListId` list.

Use of custom images

```js
// Custom images import.
"Icons": [\
    {\
        // Image list ID.\
        "ImageListId": "69c7829d-37c2-449b-a24b-bcd7bf38a8be",\
        // Imported image ID.\
        "ImageId": "4c1944db-e686-4a45-8262-df0c7d080658"\
    }\
]
```

- [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/manifest/references/icons#title-1253-2)