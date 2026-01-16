<!-- Source: page_8 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Mobile application wizard** to customize the Freedom UI page.

## 1\. Make sure the page is converted to Freedom UI [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-1 "Direct link to 1. Make sure the page is converted to Freedom UI")

1. **Open the Mobile application wizard section**. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **Mobile application wizard**.
2. **Create a new or open an existing workplace**. Instructions: [Add new workplaces](https://academy.creatio.com/documents?id=1391&anchor=title-240-1).
3. **Set up the mobile app section page** if needed. Instructions: [Set up mobile application section page](https://academy.creatio.com/documents?id=1394).
4. **Make sure the Freedom UI checkbox is selected**. Otherwise, select the checkbox.
5. **Save the changes**.

## 2\. Add the schemas that configure manifest and page settings of Creatio Mobile section [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-2 "Direct link to 2. Add the schemas that configure manifest and page settings of Creatio Mobile section")

1. **Open the Mobile application wizard section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **Mobile application wizard**.
2. **Open the needed workplace** in the section list.
3. **Open a list of workplace sections**. To do this, click **Actions** → **Set up sections**.
4. **Select the needed section** in the section list.
5. **Click Page setup**.
6. **Save the page**.
7. **Save the settings** of the **Mobile application wizard** section.

## 3\. Set up the page UI [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-3 "Direct link to 3. Set up the page UI")

### 1\. Define the position of the Freedom UI Mobile component [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-4 "Direct link to 1. Define the position of the Freedom UI Mobile component")

If you want to add an arbitrary Freedom UI Mobile component to the Freedom UI page, open the page structure using the emulator. To do this:

1. **Run Creatio Mobile** using the emulator created in Android Studio. Instructions: [Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029).

2. **Synchronize Creatio Mobile** with the main Creatio app.
1. Log in to Creatio Mobile using the same user credentials as the main Creatio app.
2. Open the **Settings** page. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_settings_in_mobile.jpg).
3. Go to the **Synchronization** block.
4. Click **Synchronize**.
3. **Open the emulator file system**. To do this, go to the Android Studio's toolbar → click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_open_menu_button.png) → **View** → **Tool Windows** → **Device Explorer**.


![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomizeFreedomUiPageForMobileCreatio/8.2/scr_device_explorer_tab.png)

4. **Synchronize the emulator file system**. To do this, go to the **Device Explorer** tab → right-click an arbitrary directory → **Synchronize**.

5. **Open the structure of the Freedom UI page** to customize. To do this, click **sdcard** → **Android** → **data** → **com.creatio.mobileapp** → **files** → **creatio** → **AppStructure** → **rev\_0** → **processed** → open the Freedom UI page schema. For example, `MobileFUIContactRecordPageSettingsDefaultWorkplace`.

If the emulator file system includes a **rev** directory whose suffix differs from "0," navigate to this directory. The suffix determines the number of up-to-date mobile app properties.

6. **Process the schema code** using an arbitrary JSON formatter.

7. **Find the needed page structure item** to place the Freedom UI Mobile component.

8. **Copy the item code** from the `name` property. For example, `Contact_PrimaryTab_Body_infoColumnSet_Type`.


### 2\. Configure the Freedom UI Mobile component [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-5 "Direct link to 2. Configure the Freedom UI Mobile component")

Keep in mind the following **requirements for Freedom UI Mobile component code**:

- Creatio lets you use the Freedom UI Mobile component that does not have a Classic UI counterpart on the previously converted Classic UI page. For example, **Contact compact profile**. If you need to do this, use the `merge` type operation in the `viewConfigDiff`, `viewModelConfigDiff`, and `modelConfigDiff` schema sections.
- Add the configuration object as a string.
- Use escaped characters.

To configure the Freedom UI Mobile component:

1. **Create a configuration object** that configures the Freedom UI Mobile component or layout element. Learn more about the available Freedom UI Mobile components and layout elements: [Freedom UI Mobile components and layout elements](https://academy.creatio.com/docs/8.x/mobile/components-references).

We recommend creating the object using an arbitrary text editor or external IDE. Use the copied item code as the `parentName` property value.

View the example that configures the button below.



viewConfigDiff schema section





```js
"viewConfigDiff": [{\
       "operation": "insert",\
       "name": "SomeButton",\
       "parentName": "Contact_PrimaryTab_Body_infoColumnSet_Type",\
       "propertyName": "items",\
       "values": {\
           "type": "crt.Button",\
           "caption": "Button",\
           "clicked":{\
               "request": "crt.CreateRecordRequest"\
           }\
       }\
}]
```

2. **Convert the configuration object** to a string.


1. Open the **Console** tab in browser debugging tools.
2. Enter the `JSON.stringify` JavaScript command.
3. Pass the configuration object as the command value.
4. Press Enter.

View the string-converted configuration object below.

String-converted configuration object

```js
'{"operation":"insert","name":"SomeButton","parentName":"Contact_PrimaryTab_Body_infoColumnSet_Type","propertyName":"items","values":{"type":"crt.Button","caption":"Button","clicked":{"request":"crt.CreateRecordRequest"}}}'
```

3. **Escape characters** of the string-converted configuration object.


1. Copy the string-converted configuration object inside `''`.
2. Paste the string-converted configuration object to an arbitrary text editor or external IDE.
3. Replace `"` characters using `\"` characters.

View the escaped configuration object below.

Escaped configuration object

```js
{\"operation\":\"insert\",\"name\":\"SomeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet_Type\",\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Button\",\"clicked\":{\"request\":\"crt.CreateRecordRequest\"}}}
```

4. **Create a resulting configuration object** that configures the Freedom UI Mobile component.


1. Copy the escaped configuration object.
2. Paste the escaped configuration object to the `viewConfigDiff` schema section in an arbitrary text editor or external IDE.

View the resulting configuration object that configures the Freedom UI Mobile component below.

viewConfigDiff schema section

```js
"viewConfigDiff": "[{\"operation\":\"insert\",\"name\":\"SomeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet_Type\",\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Button\",\"clicked\":{\"request\":\"crt.CreateRecordRequest\"}}}]"
```

### 3\. Add the Freedom UI Mobile component to the Freedom UI page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#title-15087-6 "Direct link to 3. Add the Freedom UI Mobile component to the Freedom UI page")

1. **Open the Freedom UI page schema** to customize. To do this, open the **Configuration** section → select the Freedom UI page schema. For example, `MobileFUIContactRecordPageSettingsDefaultWorkplace`. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. **Add the Freedom UI Mobile component**.


1. Go to the component whose `name` property is set to "settings."
2. Add the resulting configuration object created on the previous step to the `values` configuration object.

View the example that configures the Freedom UI Mobile component below.

Example that configures the Freedom UI Mobile component

```js
[\
    {\
        "operation": "insert",\
        "name": "settings",\
        "values": {\
            "entitySchemaName": "Contacts",\
            "settingsType": "RecordPage",\
            "localizableStrings": {},\
            "columnSets": [],\
            "operation": "insert",\
            "details": [],\
            "viewConfigDiff": "[{\"operation\":\"insert\",\"name\":\"SomeButton\",\"parentName\":\"Contact_PrimaryTab_Body_infoColumnSet_Type\",\"propertyName\":\"items\",\"values\":{\"type\":\"crt.Button\",\"caption\":\"Button\",\"clicked\":{\"request\":\"crt.CreateRecordRequest\"}}}]"\
\
        }\
    }\
]
```

3. **Save the changes**.


**As a result**, the Freedom UI page will be customized. Creatio will merge all schemas and convert them into a resulting JSON object.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile\#see-also "Direct link to See also")

[Set up mobile app workplaces](https://academy.creatio.com/documents?id=1391)

[Set up mobile application section page](https://academy.creatio.com/documents?id=1394)

[Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029)

[Freedom UI Mobile components and layout elements](https://academy.creatio.com/docs/8.x/mobile/components-references)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101)

- [1\. Make sure the page is converted to Freedom UI](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-1)
- [2\. Add the schemas that configure manifest and page settings of Creatio Mobile section](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-2)
- [3\. Set up the page UI](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-3)
  - [1\. Define the position of the Freedom UI Mobile component](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-4)
  - [2\. Configure the Freedom UI Mobile component](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-5)
  - [3\. Add the Freedom UI Mobile component to the Freedom UI page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#title-15087-6)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/customize-page-mobile#see-also)