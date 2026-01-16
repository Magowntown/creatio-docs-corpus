<!-- Source: page_42 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/router#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Routing is used for managing visual components: pages, pickers, etc. The route has 3 states:

1. `Load` – opens a current route.
2. `Unload` – closes current route on return.
3. `Reload` – restores the previous route on return.

The `Terrasoft.Router` class is used for routing and it’s main methods are `add()`, `route()`, `back()`.

## Methods [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/router\#title-1253-2 "Direct link to Methods")

```js
add(name, config)
```

Adds a route.

Parameters

|     |     |
| --- | --- |
| name | unique name of the route. In case of re-adding, the latest route will override the previous one |
| config | describes names of the functions that handle route states. Handlers of the route states are set in the `handlers` property |

Example of method use

```js
Terrasoft.Router.add("record", {
  handlers: {
     load: "loadPage",
     reload: "reloadPage",
     unload: "unloadLastPage"
  }
});
```

```js
route(name, scope, args, config)
```

Starts the route.

Parameters

|     |     |
| --- | --- |
| name | name of the route |
| scope | context of the function of the state handlers |
| args | parameters of the functions of the state handlers |
| config | additional route parameters |

Example of method use

```js
var mainPageController = Terrasoft.util.getMainController();
Terrasoft.Router.route("record", mainPageController, [{pageSchemaName: "MobileActivityGridPage"}]);
```

```js
back()
```

Closes current route and restores previous.

- [Methods](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/router#title-1253-2)