<!-- Source: page_15 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use QR and bar code scanning in Creatio Mobile to retrieve, validate, or populate data from physical labels quickly. This streamlines operations like product identification, document tracking, and service access directly from a mobile device.

To scan QR and bar codes in Creatio Mobile, implement a custom request handler using remote module. Learn more: [Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177). To call the request handler, use one of the following components added to the Freedom UI page in the Creatio Mobile:

- **Button** component. Since the scanner is closed immediately after scanning, use the component if you need to scan a single QR or bar code. Requires using the `BarcodeScanService` service that initiates the scanner in fullscreen mode and returns scanning result using the `scan()` method while implementing a request handler. Learn more: [Button component](https://academy.creatio.com/documents?id=15089), [BarcodeScanService service](https://academy.creatio.com/documents?id=15184).
- **BarcodeScanner** component. Use the component if you need to scan multiple QR or bar codes. The component lets you embed scanner into page as well as other Freedom UI Mobile components and provides abilities to customize a bar code scanning window based on your business goals. Learn more: [BarcodeScanner component](https://academy.creatio.com/documents?id=15296).

QR and bar code scanning functionality provides the following advantages:

- Instant code scanning saves time compared to manual data entry.
- Automatic recognition of QR and bar codes minimizes the risk of error occurrence.
- Support for a wide range of code formats commonly used in product labeling, digital services, and other apps.
- Instant access to information.

## General procedure [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-2 "Direct link to General procedure")

### 1\. Create a TypeScript project [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-3 "Direct link to 1. Create a TypeScript project")

Instructions: [Create a TypeScript project](https://academy.creatio.com/documents?id=15177&anchor=title-15177-1).

### 2\. Create a custom request [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-4 "Direct link to 2. Create a custom request")

Instructions: [Create a custom request](https://academy.creatio.com/documents?id=15177&anchor=title-15177-2).

### 3\. Create a custom request handler [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-5 "Direct link to 3. Create a custom request handler")

Instructions: [Create a custom request handler](https://academy.creatio.com/documents?id=15177&anchor=title-15177-3).

View the example that uses the `BarcodeScanService` service while implementing a request handler below.

index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequest,
    CrtRequest,
    BaseRequestHandler,
    CrtRequestHandler,
    CrtModule,
    bootstrapCrtModule,
    DoBootstrap,
    BarcodeScanService,
    BarcodeScanResult
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
    scopes: ['MobileFUIContactRecordPageSettingsDefaultWorkplace'],
})

export class SomeRequestNameHandler extends BaseRequestHandler<SomeRequestNameRequest> {

    public async handle(request: SomeRequestNameRequest): Promise<unknown> {

        /* Implement a custom business logic to process scanned data.
        For example, save scanned data to the contact page in Creatio Mobile.*/
        const res: BarcodeScanResult = await new BarcodeScanService().scan();
        request.$context['Name'] = 'Scanned text: ' + res.rawContent;

        ...;

        return res;

    }
}

/* Required for this module to function correctly as a JS source in package file content. */
@CrtModule({
    ...,
    /* Specify that "SomeRequestNameHandler" is request handler. */
    requestHandlers: [\
        SomeRequestNameHandler\
    ],
})

export class SomeMainAppClass implements DoBootstrap {
    bootstrap(): void {
        bootstrapCrtModule('SomeMainAppClass', SomeMainAppClass);
    }
}
```

### 4\. Add the custom request handler to the Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-6 "Direct link to 4. Add the custom request handler to the Freedom UI page")

1. **Repeat steps 1-9** of the procedure to [add the custom request handler to the Freedom UI page](https://academy.creatio.com/documents?id=15177&anchor=title-15177-4).

2. **Configure the Freedom UI Mobile component**.
   - Configure the **Button** component that calls the request handler implemented using remote module if you need to scan a single QR or bar code. Instructions: [Configure the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-5).
   - Configure the **BarcodeScanner** component that calls the request handler implemented using remote module if you need to scan multiple QR or bar codes. Instructions: [Configure the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-5).
3. **Repeat steps 10-15** of the procedure to [add the custom request handler to the Freedom UI page](https://academy.creatio.com/documents?id=15177&anchor=title-15177-4).


**As a result**, Creatio Mobile will be able to scan the following:

- a single QR or bar code if you use the **Button** component
- multiple QR or bar codes if you use the **BarcodeScanner** component

When you process scan results, we recommend following these recommendations:

- To **display and modify scanned values**, use the **Field** component. Learn more: [Field component](https://academy.creatio.com/documents?id=15216).
- To **trigger actions** based on scanned data, use the **Button** component. Learn more: [Button component](https://academy.creatio.com/documents?id=15089).

## Supported QR and bar code types [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#title-15174-1 "Direct link to Supported QR and bar code types")

Creatio Mobile supports the QR and bar code types listed in the table below.

| Name | Description | Example | ISO/IEC certification | Common usage |
| --- | --- | --- | --- | --- |
| One-dimensional (1D) bar codes / linear bar codes |
| Code 39 | Lines that have two different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_code_39.png) | ISO/IEC 16388 | Industrial |
| Code 93 | Lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_code_93.png) | ISO/IEC 15417 | Industrial |
| EAN (European Article Number) | Lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_ean.png) | ISO/IEC 15420 | Retail |
| Code 128 | Lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_code_128.png) | ISO/IEC 15417 | All industries |
| ITF (Interleaved 2 of 5) | Lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_itf.png) | ISO/IEC 16390 | Industrial,<br>Distribution |
| UPC-E | Lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_upc_e.png) | ISO/IEC 15420 | Retail,<br>Warehousing,<br>Distribution |
| Two-dimensional (2D) bar codes / matrix codes |
| Aztec code | Pixel matrix that has a marker in the center | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_aztec_code.png) | ISO/IEC 24778 | Transportation,<br>Healthcare |
| Data Matrix | Pixel matrix that has an L-shaped border as a marker | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_data_matrix.png) | ISO/IEC 16022 | Aerospace,<br>Automotive,<br>Electronics |
| QR code | Pixel matrix that has markers in the corners | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_qr_code.png) | ISO/IEC 18004 | Marketing,<br>Public transport,<br>Package delivery |
| PDF417 | Stacked lines that have different widths | ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ScanQrAndBarCodes/8.2/scr_pdf417.png) | ISO/IEC 15438 | Transportation,<br>Ticketing,<br>Driver's licenses,<br>Visas,<br>ID cards |

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview\#see-also "Direct link to See also")

[Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177)

[Freedom UI Mobile components and layout elements](https://academy.creatio.com/docs/8.x/mobile/components-references)

[Customize Freedom UI page for Creatio Mobile](https://academy.creatio.com/documents?id=15087)

- [General procedure](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-2)
  - [1\. Create a TypeScript project](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-3)
  - [2\. Create a custom request](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-4)
  - [3\. Create a custom request handler](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-5)
  - [4\. Add the custom request handler to the Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-6)
- [Supported QR and bar code types](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#title-15174-1)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/scan-bar-codes/overview#see-also)