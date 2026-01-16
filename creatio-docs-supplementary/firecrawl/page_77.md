<!-- Source: page_77 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

Creatio Mobile lets you implement the business logic of the Freedom UI page using **request handlers**. You can implement a custom request handler in Creatio Mobile using remote module.

Creatio Mobile executes request handlers when an event is triggered on a visual element of a Freedom UI page. For example, bind a custom request handler implemented using remote module to the `clicked` button event. You can use base request handlers or implement a new request handler. Base handlers are executed at different life cycle stages. Both main Creatio app and Creatio Mobile have the same request handlers. Learn more: [Generic request handlers](https://academy.creatio.com/documents?id=15368&anchor=title-3832-1).

You can modify the business logic of a request handler based on the type of related request. View the request type in the component documentation or source code of the schema that implements the request logic.

## General procedure [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-5 "Direct link to General procedure")

### 1\. Create a TypeScript project [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-1 "Direct link to 1. Create a TypeScript project")

Develop a custom request handler in a dedicated `npm` package using an external IDE. This example covers the request handler development in Microsoft Visual Studio Code. We recommend utilizing request handlers created in the TypeScript project. You can develop a custom request handler using remote module in Creatio Mobile via a \*.zip archive of the TypeScript project that contains the template of a remote module.

To create a TypeScript project to develop a custom request handler using remote module:

1. **Install or update Node.js® and npm package manager** if needed. [Download the file](https://nodejs.org/en/).

Learn more: [Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) (official npm Docs documentation).

2. **Download and unpack the \*.zip archive**. [Download](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/RequestHandlerMobileCreatio/8.2/ts_sdk_template_module.zip).

3. **Change the directory name** of the TypeScript project to the name of the package to transfer the remote module. Enter the directory name in `snake case`, for example, "process\_designer."

4. **Open the project** in Microsoft Visual Studio Code.

5. **Install the**`npm` **modules**. To do this, run the `npm install` command at the command line terminal of Microsoft Visual Studio Code. The installation might take some time.

6. **Install or update the**`@creatio/mobile-common` **library** (optional).
   - Run the `npm install @creatio/mobile-common` command at the command line terminal of Microsoft Visual Studio Code to **install the release version of the library**.
   - Run the `npm update @creatio/mobile-common` command at the command line terminal of Microsoft Visual Studio Code to **update the library version**.

**As a result**, Microsoft Visual Studio Code will create a TypeScript project to develop a custom request handler using remote module.

### 2\. Create a custom request [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-2 "Direct link to 2. Create a custom request")

1. **Open the**`index.ts` **file**.
2. **Inherit the**`BaseRequest` **class** from the `@creatio/mobile-common` library.
3. **Add the type and parameter** of the request if needed.
4. **Import the required functionality** from the libraries into the class.
5. **Save the file**.

index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequest,
    CrtRequest
} from "@creatio/mobile-common";

/* Add the "CrtRequest" decorator to the "SomeRequestNameRequest" class. */
@CrtRequest({
    type: 'usr.SomeRequestNameRequest'
})

export class SomeRequestNameRequest extends BaseRequest {
    /* The type and parameter of the request (optional). */
    public someParameterName?: someParameterType;
}
```

### 3\. Create a custom request handler [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-3 "Direct link to 3. Create a custom request handler")

1. **Implement a request handler** that displays data on the Freedom UI page. Creatio Mobile lets you implement both custom and base request handlers.
   - Implement a base request handler that is executed when the value of any attribute on a Freedom UI page changes.


     1. Open the `index.ts` file.

     2. Add the configuration object that declares the request handler.
        - Set `type` property to `usr.SomeRequestNameHandler`.
        - Set `requestType` property to `crt.HandleFUIActivityViewModelAttributeChangeHandler`.
        - Set `scopes` property to `MobileFUIActivityRecordPageSettingsDefaultWorkplace` code of Freedom UI page. The request handler is executed when Creatio initializes the Freedom UI page that has the specified code. If the property is empty or missing, it is a global handler that Creatio executes on all Freedom UI pages.
     3. Flag the `SomeRequestNameHandler` class using the `CrtRequestHandler` decorator.

     4. Inherit the `BaseRequestHandler<HandleViewModelAttributeChangeRequest>` class from the `@creatio/mobile-common` library.

     5. Implement the update of data received from the external web service when Creatio initializes the Freedom UI page. Based on your business goals, the business logic of the request handler lets you implement different operations. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-6)

     6. Import the required functionality from the libraries into the class.

     7. Save the file.


index.ts file

```js
/* Import the required functionality from the libraries. */
import {
    BaseRequestHandler,
    CrtRequestHandler,
    HandlerChainService,
    HandleViewModelAttributeChangeRequest
} from "@creatio/mobile-common";

/* Add the "CrtRequestHandler" decorator to the "SomeRequestNameHandler" class. */
@CrtRequestHandler({
    type: 'usr.SomeRequestNameHandler',
    requestType: 'crt.HandleViewModelAttributeChangeRequest',
    scopes: ['MobileFUIActivityRecordPageSettingsDefaultWorkplace'],
})

export class SomeRequestNameHandler extends BaseRequestHandler<HandleViewModelAttributeChangeRequest> {
    public async handle(request: HandleViewModelAttributeChangeRequest): Promise<unknown> {

        /* Execute a request handler when the value of any attribute on a Freedom UI page changes. */
        await HandlerChainService.instance.process({
            type: 'crt.SomeRequestNameRequest',
            someParameterName: 'someParameterValue',
            $context: request.$context
        } as SomeRequestNameRequest);

        return this.next?.handle(request);
    }
}
```

   - Implement a custom request handler that displays data on the Freedom UI page.


     1. Open the `index.ts` file.

     2. Add the configuration object that declares the request handler.
        - Set `type` property to `usr.SomeRequestNameHandler`. The `type` property is the type of handler.
        - Set `requestType` property to `usr.SomeRequestNameRequest`. The `type` property is the type of request to execute the handler specified in the `type` property.
     3. Flag the `SomeRequestNameHandler` class using the `CrtRequestHandler` decorator.

     4. Inherit the `BaseRequestHandler` class from the `@creatio-devkit/common` library.

     5. Implement the handling of the request result. Based on your business goals, the business logic of the request handler lets you implement different operations. [Read more >>>](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-6)

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

/* Add the "CrtRequestHandler" decorator to the "SomeRequestNameHandler" class. */
@CrtRequestHandler({
    requestType: 'usr.SomeRequestNameRequest',
    type: 'usr.SomeRequestNameHandler',
})

export class SomeRequestNameHandler extends BaseRequestHandler<SomeRequestNameRequest> {

    public async handle(request: SomeRequestNameRequest): Promise<unknown> {

        /* Generate the value to display on the Freedom UI page. */
        ...;

        return this.next?.handle(request);

    }
}
```
2. **Register the request handler**.


1. Open the `index.ts` file.
2. Add the `SomeRequestNameHandler` handler to the `requestHandlers` section in the `CrtModule` decorator.
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

3. **Build the project**.
1. Run the `npm run build` command at the command line terminal of Microsoft Visual Studio Code.
2. Open the `package.json` file.
3. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/RequestHandlerMobileCreatio/8.2/scr_Debug_button.png) → `build` command.

**As a result**, Microsoft Visual Studio Code will add the `main.js` build file to the TypeScript project's directory that is specified in the `webpack.config.js` file → `baseConfig` configuration object → `output` configuration object → `path` property. Out of the box, Microsoft Visual Studio Code adds the build files to the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` project directory.

### 4\. Add the custom request handler to the Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-4 "Direct link to 4. Add the custom request handler to the Freedom UI page")

01. **Ensure the**`EnableMobileSDK` **additional feature is enabled**. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3).

02. **Create a new Freedom UI app or open an existing app**. Instructions: [Create an app manually](https://academy.creatio.com/documents?id=2377&anchor=title-2232-6).

03. **Open the Package settings tab** in the No-Code Designer. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → "Application management" → "Application Hub" → select the app → "Package settings."

04. **Create a user-made package** to add the schema. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreateConfigurationWebService/8.1/btn_create_a_package.png) → **Create new package** → fill out the package properties → **Save**.

05. **Change the current package**. Instructions: [Change the current package](https://academy.creatio.com/documents?id=15072&anchor=change-the-current-package).

06. **Enable the file system development mode**. Instructions: [Set up Creatio to work with the file system](https://academy.creatio.com/documents?id=15111&anchor=title-2098-4).

07. **Download packages to the file system**.
    Using Creatio IDE







    1. Open the **Configuration** section. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

    2. Click **Actions** → **File system development mode** group → **Download packages to file system**.

    3. Go to the `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files` file system directory.

    4. Create a `/src/mobile/SomeMainAppClass` directory.

    5. Specify the directory to add the build files automatically if needed.


       1. Open the `webpack.config.js` file.

       2. Go to the `output` configuration object.

       3. Set the `path` property to the full path to the directory to add the build files. Path template: `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files/src/mobile/SomeMainAppClass` directory, where:
          - `SomePackage` is a directory of a Freedom UI app package in the file system.
          - `SomeMainAppClass` is a unique class name in the TypeScript project.

webpack.config.js file

```js
const baseConfig = {
    ...,
    output: {
        path: '../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files/src/mobile/SomeMainAppClass',
        ...
    },
    ...
};
```

Otherwise, Microsoft Visual Studio Code adds the build files to the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` project directory.

    6. Copy the `main.js` build file from the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` project directory to the `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/sdkChangeContactTypeMobile/Files/src/mobile/SomeMainAppClass` directory. If you specify the directory to add the build files automatically, omit the step for further development.

    7. Click **Actions** → **File system development mode** group → **Update packages from file system**.

    8. Compile the configuration. Instructions: [Compile the configuration](https://academy.creatio.com/documents?id=15339&anchor=title-2093-8).


Using Clio utility

    09. Install the Clio utility. This is a one-time procedure. To do this, run the `dotnet tool install clio -g` command at the terminal of Microsoft Visual Studio Code.

    10. Register an existing Creatio instance in Clio. To do this, run the `clio reg-web-app some_application_name -u https://mycreatio.com/ -l SomeLogin -p SomePassword` command at the Microsoft Visual Studio Code terminal, where:
        - `some_application_name` is the Creatio instance name.
        - `https://mycreatio.com/` is the Creatio instance URL.
        - `SomeLogin` is the user login to the Creatio instance.
        - `SomePassword` is the user password to the Creatio instance.
    11. Ensure that Clio is connected to the Creatio instance. To do this, run the `clio ping -e some_application_name` command at the Microsoft Visual Studio Code terminal.

    12. Install the `cliogate` system package into your development environment. To do this, run the `clio install-gate some_application_name` command at the Microsoft Visual Studio Code terminal.

    13. Register an existing Freedom UI app package in Clio. To do this, run the following commands at the Microsoft Visual Studio Code terminal.





        ```cli
        clio pull-pkg SomePackage -e some_application_name
        clio extract-pkg-zip SomePackage.zip -e some_application_name
        ```

    14. Go to the `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files` file system directory.

    15. Create a `../Files/src/mobile/SomeMainAppClass` directory.

    16. Specify the directory to add the build files automatically if needed.


        1. Open the `webpack.config.js` file.

        2. Go to the `output` configuration object.

        3. Set the `path` property to the full path to the directory to add the build files. Path template: `../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files/src/mobile/SomeMainAppClass` directory, where:
           - `SomePackage` is a directory of a Freedom UI app package in the file system.
           - `SomeMainAppClass` is a unique class name in the TypeScript project.

webpack.config.js file

```js
const baseConfig = {
    ...,
    output: {
        path: '../Terrasoft.WebApp/Terrasoft.Configuration/Pkg/SomePackage/Files/src/mobile/SomeMainAppClass',
        ...
    },
    ...
};
```

Otherwise, Microsoft Visual Studio Code adds the build files to the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` directory of the TypeScript project.

    17. Copy the `main.js` build file from the `../ts_sdk_template_module/out/mobile/SomeMainAppClass` project directory to the .`./Terrasoft.WebApp/Terrasoft.Configuration/Pkg/sdkChangeContactTypeMobile/Files/src/mobile/SomeMainAppClass` directory. If you specify the directory to add the build files automatically, omit the step for further development.

    18. Update the packages from file system. To do this, run the `clio push-pkg SomePackage -e some_application_name` command at the Microsoft Visual Studio Code terminal.


08. **Add the schemas that configure manifest and page settings** of Creatio Mobile section to the user-made package. Instructions: [Add the schemas that configure manifest and page settings of Creatio Mobile section](https://academy.creatio.com/documents?id=15087&anchor=title-15087-2).

09. **Define the position of the button**. Instructions: [Define the position of the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-4).

10. **Configure the Freedom UI Mobile component**. Instructions: [Configure the Freedom UI Mobile component](https://academy.creatio.com/documents?id=15087&anchor=title-15087-5).

11. **Add the Freedom UI Mobile component** to the Freedom UI page. Instructions: [Add the Freedom UI Mobile component to the Freedom UI page](https://academy.creatio.com/documents?id=15087&anchor=title-15087-6).

12. **Save the changes**.

13. **Synchronize Creatio Mobile** with the main Creatio app.
    1. Run Creatio Mobile using the emulator created in Android Studio.
    2. Log in to Creatio Mobile using the same user credentials as the main Creatio app.
    3. Open the **Settings** page. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_settings_in_mobile.jpg).
    4. Go to the **Synchronization** block.
    5. Click **Synchronize**.
14. **Synchronize the emulator file system** if needed. To do this, go to the **Device Explorer** tab → right-click an arbitrary directory → **Synchronize**.

15. **Debug the implemented business logic** if needed. Instructions: [Debug Creatio Mobile in Freedom UI](https://academy.creatio.com/documents?id=15904&anchor=title-15904-1).


**As a result**, the request handler implemented using remote module will be added to the Freedom UI page and displayed in the Creatio Mobile.

## Operations with data of Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#title-15177-6 "Direct link to Operations with data of Freedom UI page")

Based on your business goals, the business logic of the request handler lets you implement the following operations:

- **Operations with column values**.

View the examples that execute different operations with column values below.



  - Column value of a string type
  - Column value of a lookup type
  - Column value of a date type

```js
/* Receive the "Name" column value of a "string" type and save it to the "name" variable. */
let name = await request.$context['Name'];

/* Change the "Name" column value of a "string" type to the "Some new column value." */
request.$context['Name'] = 'Some new column value';
```

```js
/* Receive the "OpportunityType" column value of a "lookup" type and save it to the "type" variable. When you work with the "lookup" type field, use the "value" and "displayValue" properties of the "LookupValue" instance. */
let type = await request.$context["OpportunityType"];
let isVisible = type != null && (type as LookupValue).value === "19127009-20ae-4003-8eb8-7bb7764663d4";
```

```js
/* Receive the "RegisteredOn" column value of a "date" type and save it to the "registeredOnString" variable. The column value corresponds to the ISO 8601 standard. */
let registeredOnString = await request.$context["RegisteredOn"];

/* Create a "date" object instance from the "registeredOnString" variable. */
let registeredOnDate = new Date(registeredOnString);

/* Change the "RegisteredOn" column value to the current date and time */
request.$context["RegisteredOn"] = new Date();

/* Change the "RegisteredOn" column value to the "2024-07-19T12:13:42.394Z." */
request.$context["RegisteredOn"] = '2024-07-19T12:13:42.394Z';
```

- **Operations with attribute values**.

View the examples that execute different operations with attribute values below.



Examples that execute different operations with attribute values





```js
/* Specify the "Contact_PrimaryTab_Body_profileColumnSet_Account" attribute value as required. */
await request.$context.setAttributePropertyValue('Contact_PrimaryTab_Body_profileColumnSet_Account', 'required', true);

/* Receive the "Contact_PrimaryTab_Body_profileColumnSet_Account" attribute value and display it in the console. */
let widgetAttr = await request.$context.getAttributePropertyValue('Contact_PrimaryTab_Body_profileColumnSet_Account', 'visible');
console.log(widgetAttr);
```





Out of the box, an attribute is bound to the Freedom UI Mobile component whose name is specified as an attribute value.

- **Filter data**.

View the examples that filter data below.



  - Filter values of lookup type column
  - Filter columns of the embedded list

```js
/* Filter values of the "Account" "lookup" type column. */
let result = await this.next?.handle(request);
await request.$context.setAttributePropertyValue('Account', 'filter', {
    "filterType": 4,
    "comparisonType": 3,
    "isEnabled": true,
    "trimDateTimeParameterToDate": false,
    "leftExpression": {
        "expressionType": 0,
        "columnPath": "PrimaryContact"
    },
    "rightExpressions": [\
        {\
            "expressionType": 2,\
            "parameter": {\
                "dataValueType": 10,\
                "value": "410006e1-ca4e-4502-a9ec-e54d922d2c00"\
            }\
        }\
    ],
    "isAggregative": false,
    "key": "63871ecc-40a1-4f00-a7e5-9c5099a76ea4",
    "dataValueType": 10,
    "referenceSchemaName": "Contact"
});
return result;
```

```js
/* Filter columns of the "OpportunityContactDetailV2EmbeddedDetail" embedded list. */
"viewModelConfig": {
    "attributes": {
        ...,
        "OpportunityContactDetailV2EmbeddedDetail": {
            "modelConfig": {
                ...,
                "filterAttributes": [{\
                    "name": "OpportunityContactDetailV2EmbeddedDetail_Filter"\
                }],
            },
        }
    }
}

/* Apply the filter before the "crt.LoadDataRequest" request handler. */
request.$context['OpportunityContactDetailV2EmbeddedDetail_Filter'] = {
    "filterType": 4,
    "comparisonType": 4,
    "isEnabled": true,
    "trimDateTimeParameterToDate": false,
    "leftExpression": {"expressionType": 0, "columnPath": "Contact"},
    "isAggregative": false,
    "key": "63871ecc-40a1-4f00-a7e5-9c5099a76ea4",
    "dataValueType": 10,
    "leftExpressionCaption": "Contact",
    "referenceSchemaName": "Contact",
    "rightExpressions": [\
        {\
            "expressionType": 2,\
            "parameter": {"dataValueType": 10, "value": "410006e1-ca4e-4502-a9ec-e54d922d2c00"}\
        }\
    ]
};
return await this.next?.handle(request);
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#see-also "Direct link to See also")

[handlers schema section](https://academy.creatio.com/documents?id=15368)

[Manage an existing additional feature](https://academy.creatio.com/documents?id=15631)

[Manage apps](https://academy.creatio.com/documents?id=2377)

[Simple package](https://academy.creatio.com/documents?id=15072)

[External IDEs basics](https://academy.creatio.com/documents?id=15111)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101)

[Operations with schemas in Creatio IDE](https://academy.creatio.com/documents?id=15339)

[Customize Freedom UI page for Creatio Mobile](https://academy.creatio.com/documents?id=15087)

[Debug Creatio Mobile](https://academy.creatio.com/documents?id=15904)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview\#resources "Direct link to Resources")

[Node.js installation file](https://nodejs.org/en/)

[Official vendor documentation](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) (npm Docs)

[Template of remote module in Creatio Mobile](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/RequestHandlerMobileCreatio/8.2/ts_sdk_template_module.zip)

- [General procedure](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-5)
  - [1\. Create a TypeScript project](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-1)
  - [2\. Create a custom request](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-2)
  - [3\. Create a custom request handler](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-3)
  - [4\. Add the custom request handler to the Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-4)
- [Operations with data of Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#title-15177-6)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/custom-request-handler/overview#resources)