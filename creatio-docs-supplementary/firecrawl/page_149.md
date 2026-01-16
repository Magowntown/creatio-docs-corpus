<!-- Source: page_149 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/feed-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Feed** component to add a feed. You can enable internal and external users to post and read comments that support rich text and user mention via "@." Authors can edit or delete their posts or attachments. Before you use the component, make sure that the Freedom UI page schema includes the data source. Learn more: [Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088).

View the example of a configuration object that adds a feed below.

Example of a configuration object that adds a feed

```js
{
    "type": "crt.Messaging",
    "items": "ContactFeed"
}
```

* * *

```js
string type
```

Component type. `crt.Messaging` for the **Feed** component.

* * *

```js
string items
```

The attribute from the `viewModelConfig` schema section.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/feed-mobile\#see-also "Direct link to See also")

[Operations with data for Creatio Mobile](https://academy.creatio.com/documents?id=15088)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/feed-mobile#see-also)