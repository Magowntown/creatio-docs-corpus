<!-- Source: page_131 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/iframe-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **IFrame** component to embed external content into a page.

View the example of a configuration object that embeds external content into a page below.

Example of a configuration object that embeds external content into a page

```js
{
    "type": "crt.IFrame",
    "name": "Link name",
    "urlContent": "https://creatio.com/",
}
```

* * *

```js
string type
```

Component type. `crt.IFrame` for the **IFrame** component.

* * *

```js
string name
```

The name of the URL to receive the external content.

* * *

```js
string urlContent
```

The URL to receive the external content.