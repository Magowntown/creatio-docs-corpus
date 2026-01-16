<!-- Source: page_9 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/baseconfigurationpage#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Page controller classes are inherited from the `Terrasoft.controller.BaseConfigurationPage` class that provides methods of handling the life cycle events.

## Methods [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/baseconfigurationpage\#title-1253-2 "Direct link to Methods")

```js
initializeView(view)
```

Method is called after the page view in the DOM is being created (but was not rendered). On this stage you can subscribe to the events of the view classes and perform additional actions with DOM.

```js
pageLoadComplete(isLaunch)
```

Provides extension of the logic that is executed at the page load and return. The `true` value of the `isLaunch` parameter indicates that the page is being loaded for the first time.

```js
launch()
```

Called only when the page is opened. The method initiates the loading of data. If you need to load additional data, use the `launch()` method.

```js
pageUnloadComplete()
```

Provides extension of the logic that is executed at the page unload and closure.

- [Methods](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/baseconfigurationpage#title-1253-2)