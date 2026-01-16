<!-- Source: page_128 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/link-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Link** component to add clickable URLs. Additionally, you can display a label above the URL text.

View the example of a configuration object that adds the clickable URL below.

Example of a configuration object that adds the clickable URL

```js
{
    "type": "crt.Link",
    "caption": "\$MyActivityCaptionAttribute",
    "label": "Label",
    "clicked": {
        "request": "crt.UpdateRecordRequest",
        "params": {
            "entityName": "Activity",
            "recordId": "\$MyActivityIdAttribute",
        }
    }
}
```

* * *

```js
string type
```

Component type. `crt.Link` for the **Link** component.

* * *

```js
string caption
```

Link name.

* * *

```js
string label
```

Link title.

* * *

```js
object clicked
```

The request fires when a user clicks the link.