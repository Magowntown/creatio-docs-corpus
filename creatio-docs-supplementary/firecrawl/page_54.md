<!-- Source: page_54 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

Use GPS functionality in Creatio Mobile to retrieve real-time latitude and longitude data directly from the mobile app as well as gain deeper insights using additional GPS-related information, for example, accuracy, permissions, and mock location detection.

To work with GPS data in Creatio Mobile, implement a custom request handler using remote module. Learn more: [Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177). Requires using the `GeolocationService` service that returns current location using the `getCurrentCoordinates()` method. Learn more: [GeolocationService service](https://academy.creatio.com/documents?id=15087).

To call the request handler, use the **Button** component added to the Freedom UI page in the Creatio Mobile. Learn more: [Button component](https://academy.creatio.com/documents?id=15089).

## 1\. Create a TypeScript project [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview\#title-15173-1 "Direct link to 1. Create a TypeScript project")

Instructions: [Create a TypeScript project](https://academy.creatio.com/documents?id=15177&anchor=title-15177-1).

## 2\. Create a custom request [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview\#title-15173-2 "Direct link to 2. Create a custom request")

Instructions: [Create a custom request](https://academy.creatio.com/documents?id=15177&anchor=title-15177-2).

## 3\. Create a custom request handler [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview\#title-15173-3 "Direct link to 3. Create a custom request handler")

Instructions: [Create a custom request handler](https://academy.creatio.com/documents?id=15177&anchor=title-15177-3).

View the example that uses the `GeolocationService` service while implementing a request handler below.

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
    GeolocationService,
    GeolocationServicePosition,
    GeolocationAccuracy
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

        /* Implement a custom business logic to get and save GPS data.
        For example, save GPS data to the contact page in Creatio Mobile. */
        const coords: GeolocationServicePosition = await new GeolocationService()
            .getCurrentCoordinates(GeolocationAccuracy.low);
        request.$context['Name'] = "GPS coords: Lat:" + coords.latitude + ", Long:" + coords.longitude;
        ...;

        return this.next?.handle(request);

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

## 4\. Add the custom request handler to the Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview\#title-15173-4 "Direct link to 4. Add the custom request handler to the Freedom UI page")

Instructions: [Add the custom request handler to the Freedom UI page](https://academy.creatio.com/documents?id=15177&anchor=title-15177-4).

**As a result**, Creatio Mobile will return current location data when you click the button.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview\#see-also "Direct link to See also")

[Custom request handler implemented using remote module in Creatio Mobile](https://academy.creatio.com/documents?id=15177)

[GeolocationService service](https://academy.creatio.com/documents?id=15087)

[Button component](https://academy.creatio.com/documents?id=15089)

[Customize Freedom UI page for Creatio Mobile](https://academy.creatio.com/documents?id=15087)

- [1\. Create a TypeScript project](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#title-15173-1)
- [2\. Create a custom request](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#title-15173-2)
- [3\. Create a custom request handler](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#title-15173-3)
- [4\. Add the custom request handler to the Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#title-15173-4)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/overview#see-also)