<!-- Source: page_91 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/references/barcodescanservice#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

`BarcodeScanService` service initiates the bar code scanner in fullscreen mode and returns bar code scanning result using the `scan()` method. Since the scanner is closed immediately after scanning, use the `BarcodeScanService` service while implementing a request handler if you need to scan a single QR or bar code. Learn more: [Scan QR and bar codes in Creatio Mobile](https://academy.creatio.com/documents?id=15174).

```js
scan()
```

Returns the result of bar code scanning.

Output parameters

|     |     |
| --- | --- |
| type | Type of bar code scanning result.

Available values

|     |     |
| --- | --- |
| barcode | Bar code. |
| error | Bar code scanning ended in an error. |
| cancelled | Bar code scanning is cancelled. | |
| rawContent | Content of scanned bar code when the `type` parameter is equal to `barcode`. Otherwise, `null`. |
| errorMessage | Error message when the `type` parameter is equal to `error`. Otherwise, `null`. |

View the example of the `scan()` method usage below.

Example of the scan() method usage

```js
import {
    BaseRequest,
    CrtRequest,
    BaseRequestHandler,
    CrtRequestHandler
} from "@creatio/mobile-common";

/* Add the "CrtRequest" decorator to the "SomeRequestNameRequest" class. */
@CrtRequest({
    type: 'usr.SomeRequestNameRequest'
})

export class SomeRequestNameRequest extends BaseRequest {}

/* Add the "CrtRequestHandler" decorator to the "SomeRequestNameHandler" class. */
@CrtRequestHandler({
    requestType: 'usr.SomeRequestNameRequest',
    type: 'usr.SomeRequestNameHandler',
})

export class SomeRequestNameHandler extends BaseRequestHandler<SomeRequestNameRequest> {

    public async handle(request: SomeRequestNameRequest): Promise<unknown> {

        const res: BarcodeScanResult = await new BarcodeScanService().scan();
        Logger.console('___ Result type: ' + res.type);
        Logger.console('___ Content: ' + res.rawContent);
        Logger.console('___ Error: ' + res.errorMessage);
        return res;
    }
}
```