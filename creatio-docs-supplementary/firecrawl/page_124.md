<!-- Source: page_124 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/attachment-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Attachment** component to work with files. The component lets you display, add, and delete files. Before you use the component, make sure that the Freedom UI page schema includes the data source. Learn more: [Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088).

View the example of a configuration object that works with files below.

Example of a configuration object that works with files

```js
{
    "type": "crt.Attachments",
    "items": "AttachmentItems"
}
```

* * *

```js
string type
```

Component type. `crt.Attachments` for the **Attachment** component.

* * *

```js
string items
```

The attribute from the `viewModelConfig` schema section.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/attachment-mobile\#see-also "Direct link to See also")

[Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/attachment-mobile#see-also)