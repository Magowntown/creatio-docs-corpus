<!-- Source: page_112 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/barcodescanner-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **BarcodeScanner** component to embed scanner into a page if you need to scan multiple QR or bar codes. The component calls the request handler implemented using remote module, launches the camera on your device and displays a bar code scanning window. Unlike the `BarcodeScanService` service, the **BarcodeScanner** component provides abilities to customize a bar code scanning window based on your business goals. For example, you can control the flash when scanning bar codes. Learn more: [Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177), [Scan QR and bar codes in Creatio Mobile](https://academy.creatio.com/documents?id=15174).

View the example of a configuration object that enables bar code scanning functionality on a page below.

Example of a configuration object that enables bar code scanning functionality on a page

```js
{
    "type": "crt.BarcodeScanner",
    "name": "InventoryScanner",
    "size": "medium",
    "scanTimeout": 2000,
    "features": {
        "flashToggle": true
    },
    "enabled": true,
    "scanned": {
        "request": "SomeRequest",
        "params": {
            "result": "@event"
        }
    }
}
```

* * *

```js
string type
```

Component type. `crt.BarcodeScanner` for the **BarcodeScanner** component.

* * *

```js
string name
```

Unique identifier for the **BarcodeScanner** component.

* * *

```js
string size
```

Size of a bar code scanning window. By default, `medium`. Real sizes can vary based on the screen size or other conditions. We recommend selecting a bar code scanning window size that fits your layout consistently and provides convenient bar code scanning.

Available values

|     |     |
| --- | --- |
| small | 200x200 pt |
| medium | 350x350 pt |
| large | 500x500 pt |
| max | A bar code scanning window takes up all screen space. We recommend using `max` value together with the non-scrollable containers. |

* * *

```js
number scanTimeout
```

Timeout in milliseconds before scanning the next bar code. By default, `2000`. We recommend configuring a scan timeout based on your business goals. Use short timeout to scan multiple bar codes quickly. Use long timeout to reduce the number of accidental duplicates.

* * *

```js
object features
```

Configuration object that configures additional functionality for the bar code scanning window.

Parameters

| Name | Description |
| --- | --- |
| boolean flashToggle | The flag that determines whether to display the button that controls the flash when scanning bar codes. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | The flash button is shown. |
| false | The flash button is hidden. | |

* * *

```js
boolean enabled
```

Available values

|     |     |
| --- | --- |
| true | The bar code scanner is enabled. |
| false | The bar code scanner is disabled. |

* * *

```js
object scanned
```

The request fires when a bar code is scanned successfully. Creatio lets you bind the sending of a custom request handlers implemented in remote module to the scan event. We recommend implementing request handlers that process scan results quickly to provide immediate feedback.

The `result` property includes the `@event` placeholder and is replaced by the `BarcodeScanResult` object that corresponds to the list of the `scan()` method output parameters. Learn more: [BarcodeScanService service](https://academy.creatio.com/documents?id=15184).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/barcodescanner-mobile\#see-also "Direct link to See also")

[BarcodeScanService service](https://academy.creatio.com/documents?id=15184)

[Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177)

[Scan QR and bar codes in Creatio Mobile](https://academy.creatio.com/documents?id=15174)

- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/barcodescanner-mobile#see-also)