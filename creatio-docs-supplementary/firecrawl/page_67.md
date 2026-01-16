<!-- Source: page_67 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

To implement the example:

1. Create a TypeScript project. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-1)
2. Create a custom request. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-2)
3. Create a custom request handler. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-3)
4. Add the custom request handler to the Freedom UI page. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-4)

Example

Add a **Change to supplier** button to the contact page in Creatio Mobile. The button must send the custom request handler and change the **Type** field value to "Supplier."

Implement a request handler using a remote module created in TypeScript project.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ImplementRequestHandlerUsingRemoteModule/8.2/scr_result.gif)

## 1\. Create a TypeScript project [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-1 "Direct link to 1. Create a TypeScript project")

1. **Install or update Node.js® and npm package manager** if needed. [Download the file](https://nodejs.org/en/).

Learn more: [Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) (official npm Docs documentation).

2. **Download and unpack the \*.zip archive**. [Download](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/RequestHandlerMobileCreatio/8.2/ts_sdk_template_module.zip).

3. **Change the directory name** of the TypeScript project to the name of the package to transfer the remote module.

For this example, change the directory name of the TypeScript project to the `handler_in_remote_module_mobile`.

4. **Open the project** in Microsoft Visual Studio Code.

5. **Install the**`npm` **modules**. To do this, run the `npm install` command at the command line terminal of Microsoft Visual Studio Code.

6. **Update the**`@creatio/mobile-common` **library**. To do this, run the `npm update @creatio/mobile-common` command at the command line terminal of Microsoft Visual Studio Code.


**As a result**, Microsoft Visual Studio Code will create a TypeScript project to develop a custom request handler using remote module.

## 2\. Create a custom request [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-2 "Direct link to 2. Create a custom request")

1. **Open the**`index.ts` **file**.
2. **Inherit the**`BaseRequest` **class** from the `@creatio/mobile-common` library.
3. **Import the required functionality** from the libraries into the class.
4. **Save the file**.

index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequest,
    CrtRequest
} from "@creatio/mobile-common";

/* Add the "CrtRequest" decorator to the "ChangeContactTypeToSupplierRequest" class. */
@CrtRequest({
    type: 'usr.ChangeContactTypeToSupplierRequest'
})

export class ChangeContactTypeToSupplierRequest extends BaseRequest {}
```

## 3\. Create a custom request handler [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-3 "Direct link to 3. Create a custom request handler")

1. **Implement a custom request handler** that changes the **Type** field value on a contact page in Creatio Mobile to "Supplier."


1. Open the `index.ts` file.

2. Add the configuration object that declares the request handler.
      - Set `type` property to `usr.ChangeContactTypeToSupplierRequestHandler`. The `type` property is the type of handler.
      - Set `requestType` property to `usr.ChangeContactTypeToSupplierRequest`. The `type` property is the type of request to execute the handler specified in the `type` property.
3. Flag the `ChangeContactTypeToSupplierRequestHandler` class using the `CrtRequestHandler` decorator.

4. Inherit the `BaseRequestHandler` class from the `@creatio-devkit/common` library.

5. Find the ID of the "Supplier" value in the **Contact type** lookup. For this example, the ID is "ac278ef3-e63f-48d9-ba34-7c52e92fecfe."

6. Generate the value to display on the Freedom UI page.

7. Import the required functionality from the libraries into the class.

8. Save the file.


index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequestHandler,
    CrtRequestHandler
} from "@creatio/mobile-common";

/* Add the "CrtRequestHandler" decorator to the "ChangeContactTypeToSupplierRequestHandler" class. */
@CrtRequestHandler({
    requestType: 'usr.ChangeContactTypeToSupplierRequest',
    type: 'usr.ChangeContactTypeToSupplierRequestHandler'
})

export class ChangeContactTypeToSupplierRequestHandler extends BaseRequestHandler<ChangeContactTypeToSupplierRequest> {

    public async handle(request: ChangeContactTypeToSupplierRequest): Promise<unknown> {

        /* Generate the value to display on the Freedom UI page. */
        request.$context['Type'] = 'ac278ef3-e63f-48d9-ba34-7c52e92fecfe';
        return this.next?.handle(request);

    }
}
```

2. **Register the request handler**.


1. Open the `index.ts` file.
2. Add the `ChangeContactTypeToSupplierRequestHandler` handler to the `requestHandlers` section in the `CrtModule` decorator.
3. Import the required functionality from the libraries into the class.
4. Save the file.

index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    CrtModule,
    bootstrapCrtModule,
    DoBootstrap
} from '@creatio/mobile-common';
...

@CrtModule({
    ...,
    /* Specify that "ChangeContactTypeToSupplierRequestHandler" is request handler. */
    requestHandlers: [\
        ChangeContactTypeToSupplierRequestHandler\
    ],
})

export class SdkRemoteModuleInMobileApp implements DoBootstrap {
    bootstrap(): void {
        bootstrapCrtModule('SdkRemoteModuleInMobileApp', SdkRemoteModuleInMobileApp);
    }
}
```

3. **Build the project**.
1. Run the `npm run build` command at the command line terminal of Microsoft Visual Studio Code.
2. Open the `package.json` file.
3. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/RequestHandlerMobileCreatio/8.2/scr_Debug_button.png) → `build` command.

**As a result**, Microsoft Visual Studio Code will add the `main.js` build file to the TypeScript project's directory that is specified in the `webpack.config.js` file → `baseConfig` configuration object → `output` configuration object → `path` property. Out of the box, Microsoft Visual Studio Code adds the build files to the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` project directory.

## 4\. Add the custom request handler to the Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-4 "Direct link to 4. Add the custom request handler to the Freedom UI page")

01. **Ensure the**`EnableMobileSDK` **additional feature is enabled**. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3).

02. **Open the Customer 360 app** in the No-Code Designer.

03. **Open the Package settings tab** in the No-Code Designer. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → "Application management" → "Application Hub" → **Customer 360** app → "Package settings."

04. **Create a user-made package** to add the schema. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreateConfigurationWebService/8.1/btn_create_a_package.png) → **Create new package** → fill out the package properties → **Save**.

    For this example, create the `sdkChangeContactTypeMobile` user-made package.

05. **Change the current package**. Instructions: [Change the current package](https://academy.creatio.com/documents?id=15072&anchor=change-the-current-package).

    For this example, change the current package to `sdkChangeContactTypeMobile` user-made package.

06. **Enable the file system development mode**. Instructions: [Set up Creatio to work with the file system](https://academy.creatio.com/documents?id=15111&anchor=title-2098-4).

07. **Download packages to the file system** using Creatio IDE.
    1. Open the **Configuration** section. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).
    2. Click **Actions** → **File system development mode** group → **Download packages to file system**.
    3. Go to the `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/sdkChangeContactTypeMobile/Files` file system directory.
    4. Create a `/src/mobile/SdkRemoteModuleInMobileApp` directory.
    5. Copy the `main.js` build file from the `../ts_sdk_template_module/out/mobile/SdkRemoteModuleInMobileApp` project directory to the `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/sdkChangeContactTypeMobile/Files/src/mobile/SdkRemoteModuleInMobileApp` directory.
    6. Click **Actions** → **File system development mode** group → **Update packages from file system**.
    7. Compile the configuration. Instructions: [Compile the configuration](https://academy.creatio.com/documents?id=15339&anchor=title-2093-8).
08. **Add the schemas that configure manifest and page settings** of Creatio Mobile section to the user-made package. Instructions: [Add the schemas that configure manifest and page settings of Creatio Mobile section](https://academy.creatio.com/documents?id=15087&anchor=title-15087-2).

    For this example, select the **Contacts** section in the section list.

    As a result, the `MobileApplicationManifestDefaultWorkplace` and `MobileFUIContactRecordPageSettingsDefaultWorkplace` schemas will be added to the `sdkChangeContactTypeMobile` user-made package.

09. **Define the position of the button**. Instructions: [Define the position of the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-4).

    For this example, the button will be added to the structure item whose `name` property is set to `Contact_PrimaryTab_Body_infoColumnSet`.

10. **Configure the button**. Instructions: [Configure the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-5).

    For this example, the resulting configuration object that configures the button is as follows.



    viewConfigDiff schema section





    ```js
    "viewConfigDiff": "[{\"operation\":\"insert\",\"name\":\"UsrChangeContactTypeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet\",\"index\":1,\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Change to supplier\",\"size\":\"medium\",\"clicked\":{\"request\":\"usr.ChangeContactTypeToSupplierRequest\"}}}]"
    ```

11. **Add the button** to the Freedom UI page. Instructions: [Add the Freedom UI Mobile component to the Freedom UI page](https://academy.creatio.com/documents?id=15087&anchor=title-15087-6).

    For this example, add the button to the `MobileFUIContactRecordPageSettingsDefaultWorkplace` Freedom UI page schema.



    MobileFUIContactRecordPageSettingsDefaultWorkplace schema





    ```js
    [\
        {\
            "operation": "merge",\
            "name": "settings",\
            "values": {\
                "localizableStrings": {\
                    "primaryColumnSetContact_caption": "Primary column set",\
                    "profileColumnSetContact_caption": "Profile",\
                    "infoColumnSetContact_caption": "Contact info",\
                    "ContactCareerDetailV2EmbeddedDetailContact_caption": "Job experience",\
                    "ContactAddressDetailV2EmbeddedDetailContact_caption": "Addresses",\
                    "ContactCommunicationDetailEmbeddedDetailContact_caption": "Communication options",\
                    "ContactTimelineTab_caption": "Timeline",\
                    "TabFeed_caption": "Feed",\
                    "TabAttachments_caption": "Attachments"\
                },\
                "viewConfigDiff": "[{\"operation\":\"insert\",\"name\":\"UsrChangeContactTypeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet\",\"index\":1,\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Change to supplier\",\"size\":\"medium\",\"clicked\":{\"request\":\"usr.ChangeContactTypeToSupplierRequest\"}}}]"\
            }\
        }\
    ]
    ```

12. **Save the changes**.


**As a result**, the **Change to supplier** button will be added to the contact page.

## View the result [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-5 "Direct link to View the result")

1. **Synchronize Creatio Mobile** with the main Creatio app.
1. Run Creatio Mobile using the emulator created in Android Studio.
2. Log in to Creatio Mobile using the same user credentials as the main Creatio app.
3. Open the **Settings** page. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_settings_in_mobile.jpg).
4. Go to the **Synchronization** block.
5. Click **Synchronize**.
2. **Synchronize the emulator file system** if needed. To do this, go to the **Device Explorer** tab → right-click an arbitrary directory → **Synchronize**.

3. **Open the Contacts section**.

4. **Open a contact** whose **Type** field value differs from the "Supplier." For example, "Alexander Wilson."

5. **Click Change to supplier**.


**As a result**, the **Change to supplier** button on the contact page in Creatio Mobile will send the custom request handler and change the **Type** field value to "Supplier." [View the result >>>](https://academy.creatio.com/documents?id=15178&anchor=view-result)

The handler is implemented using the remote module created in TypeScript project.

## Source code [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#title-15178-6 "Direct link to Source code")

- index.ts file
- MobileFUIContactRecordPageSettingsDefaultWorkplace

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequestHandler,
    CrtModule,
    CrtRequestHandler,
    BaseRequest,
    bootstrapCrtModule,
    DoBootstrap,
    CrtRequest
} from '@creatio/mobile-common';

/* Add the "CrtRequest" decorator to the "ChangeContactTypeToSupplierRequest" class. */
@CrtRequest({
    type: 'usr.ChangeContactTypeToSupplierRequest'
})
export class ChangeContactTypeToSupplierRequest extends BaseRequest {}

/* Add the "CrtRequestHandler" decorator to the "ChangeContactTypeToSupplierRequestHandler" class. */
@CrtRequestHandler({
    requestType: 'usr.ChangeContactTypeToSupplierRequest',
    type: 'usr.ChangeContactTypeToSupplierRequestHandler'
})

export class ChangeContactTypeToSupplierRequestHandler extends BaseRequestHandler<ChangeContactTypeToSupplierRequest> {

    public async handle(request: ChangeContactTypeToSupplierRequest): Promise<unknown> {

        /* Generate the value to display on the Freedom UI page. */
        request.$context['Type'] = 'ac278ef3-e63f-48d9-ba34-7c52e92fecfe';
        return this.next?.handle(request);
    }
}

@CrtModule({
    /* Specify that "ChangeContactTypeToSupplierRequestHandler" is request handler. */
    requestHandlers: [\
        ChangeContactTypeToSupplierRequestHandler\
    ],
})
export class SdkRemoteModuleInMobileApp implements DoBootstrap {
    bootstrap(): void {
        bootstrapCrtModule('SdkRemoteModuleInMobileApp', SdkRemoteModuleInMobileApp);
    }
}
```

```js
[\
    {\
        "operation": "merge",\
        "name": "settings",\
        "values": {\
            "localizableStrings": {\
                "primaryColumnSetContact_caption": "Primary column set",\
                "profileColumnSetContact_caption": "Profile",\
                "infoColumnSetContact_caption": "Contact info",\
                "ContactCareerDetailV2EmbeddedDetailContact_caption": "Job experience",\
                "ContactAddressDetailV2EmbeddedDetailContact_caption": "Addresses",\
                "ContactCommunicationDetailEmbeddedDetailContact_caption": "Communication options",\
                "ContactTimelineTab_caption": "Timeline",\
                "TabFeed_caption": "Feed",\
                "TabAttachments_caption": "Attachments"\
            },\
            "viewConfigDiff": "[{\"operation\":\"insert\",\"name\":\"UsrChangeContactTypeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet\",\"index\":1,\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Change to supplier\",\"size\":\"medium\",\"clicked\":{\"request\":\"usr.ChangeContactTypeToSupplierRequest\"}}}]"\
        }\
    }\
]
```

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module\#resources "Direct link to Resources")

[\*.zip archive that contains the implemented Freedom UI app for Creatio Mobile](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/ImplementRequestHandlerUsingRemoteModule/8.2/sdkChangeContactTypeMobile_2025-03-13_08.14.28.zip)

[TypeScript project that contains the implemented example](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/ImplementRequestHandlerUsingRemoteModule/8.2/handler_in_remote_module_mobile.zip)

- [1\. Create a TypeScript project](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-1)
- [2\. Create a custom request](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-2)
- [3\. Create a custom request handler](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-3)
- [4\. Add the custom request handler to the Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-4)
- [View the result](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-5)
- [Source code](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#title-15178-6)
- [Resources](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/examples/implement-a-custom-request-handler-using-remote-module#resources)