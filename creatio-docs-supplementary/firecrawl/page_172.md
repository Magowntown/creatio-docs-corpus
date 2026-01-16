<!-- Source: page_172 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

The general procedure to debug Creatio Mobile differs in Freedom UI and Classic UI.

## Debug Creatio Mobile in Freedom UI [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure\#title-15904-1 "Direct link to Debug Creatio Mobile in Freedom UI")

Creatio Mobile lets you customize Freedom UI pages by adding components and implement the business logic of the Freedom UI page using request handlers. You can implement a custom request handler in Creatio Mobile using remote module and debug the implemented business logic if needed.

To debug Creatio Mobile in Freedom UI:

01. **Perform preliminary setup** if needed.
    1. Receive an `app-debug.apk` file of the Creatio Mobile app to debug. To do this, contact [Creatio support](mailto:support@creatio.com).

    2. Install Google Chrome on your PC.

    3. Install and set up Android Studio. Learn more: [Android Studio](https://developer.android.com/studio) (official Android Studio website), [Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029).

    4. Install and set up Android command-line tool. Learn more: [Command-line tools](https://developer.android.com/tools) (official Android Studio documentation).

    5. Configure the behavior of Android Studio and the Android command-line tools. To do this, set the following environment variables.



       | Variable name | Variable description | Variable value |
       | --- | --- | --- |
       | PATH | The path to the `adb.exe` installation file. | `C:\Users\SomeUserName\AppData\Local\Android\Sdk\platform-tools`, where `SomeUserName` is the username of your Windows user account. |


       Learn more: [Environment variables](https://developer.android.com/tools/variables) (official Android Studio documentation).

    6. Ensure the business logic of the remote module is implemented in the TypeScript project created via the \*.zip archive. Otherwise, copy your customizations to a new TypeScript project created via a \*.zip archive.
02. **Specify the class** that implements the `DoBootstrap` interface.


    1. Open the project in Microsoft Visual Studio Code.
    2. Open the `creatio-mobile-config.json` file.
    3. Set the class name to the `moduleName` property.
    4. Save the file.

creatio-mobile-config.json file

```js
{
    "moduleName": "SdkRemoteModuleInMobileApp",
    ...
}
```

03. **Run Creatio Mobile** to debug using Android Studio in one of the following ways:


    - Android mobile device that has debug mode enabled. Enabling debug mode depends on the model of your mobile device.
    - Mobile app emulator. Instructions: [Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029).

We recommend simultaneously running only a single emulator or mobile device using Android Studio.

04. **Upload your customization** to the Creatio Mobile to debug. Repeat the step once you create a new emulator or delete data, even if you do not modify the code.
    1. Open the project in Microsoft Visual Studio Code.

    2. Open the `package.json` file.

    3. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/RequestHandlerMobileCreatio/8.2/scr_Debug_button.png) → `build:inject-on-device` command. This builds the project and automatically replaces the remote module's code with the remote module's code implemented in the project on the Creatio Mobile launched using Android Studio. Out of the box, the command replaces the code of the `main.js` and `main.release.js` files, but you can **modify the list of replaced files**:
       1. Open the project in Microsoft Visual Studio Code.
       2. Open the `tools` directory → `common.js` file.
       3. Specify the list of replaced files using the `updateExcludedModules()` method.
05. **Apply the changes**. To do this, restart the Creatio Mobile using Android Studio.

06. **Open Google Chrome** on the PC.

07. **Open the Inspect with Chrome Developer Tools tab**. To do this, enter the `chrome://inspect/#devices` URL in the browser address bar. This opens the **Devices** tab that includes the list of connected devices. The link to Creatio Mobile is `com.creatio.mobileapp`.


    ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_devices_tab.png)


    If the browser displays several devices that have the `com.creatio.mobileapp` link, select the first device.

08. **Click the**`inspect` **link** under the link to Creatio Mobile. This opens the **Sources** tab of an app debugging window.


    ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_sources_tab_freedom.png)

09. **Find remote module** to debug. Most of the classes are in the `dev_module` directory.


    ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_dev_module.png)

10. **Debug Creatio Mobile**.

11. **Repeat steps 4-10** to apply the changes.


## Debug Creatio Mobile in Classic UI [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure\#title-15904-2 "Direct link to Debug Creatio Mobile in Classic UI")

1. **Run Creatio Mobile** to debug using one of the following ways:
Mobile device







1. Receive an `app-debug.apk` file of the Creatio Mobile app to debug. To do this, contact [Creatio support](mailto:support@creatio.com).
2. Install the Creatio Mobile on your mobile device.
3. Run the app on the mobile device.
4. Connect the mobile device to your PC via USB.

Mobile app emulator

Set up the mobile app emulator. Instructions: [Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029).

2. **Open Google Chrome** on the PC.

3. **Open the Inspect with Chrome Developer Tools tab**. To do this, enter the `chrome://inspect/#devices` URL in the browser address bar. This opens the **Devices** tab that includes the list of connected devices. The link to Creatio Mobile is `com.creatio.mobileapp`.


![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/DebugMobileApp/8.0/scr_ConnectedDevices.png)

4. **Display the connected device** (optional).

If the connected device is missing from the **Devices** tab, check the device authorization. To do this:
1. Download Android Debug Bridge (adb). [Download](https://developer.android.com/studio/releases/platform-tools).

2. Open the command line.

3. Go to the directory that contains the `adb.exe` file. To do this, run the command below.





      ```cli
      cd [Path to the directory that contains the adb.exe file]
      ```

4. Open the list of connected devices. To do this, run the command below.





      ```cli
      adb.exe devices
      ```

5. If you see `unauthorized` status for the mobile device, authorize the device.
      1. Disconnect the USB cable.
      2. Revoke USB debugging permissions on your device.
      3. Reconnect the USB cable.
      4. Set **Trust this computer?** to "Yes."
5. **Click the inspect link** under the link to Creatio Mobile. This opens an app debugging window.

6. **Open the Sources tab**.

7. **Find functionality** to debug. Most of the classes are in the `android_asset/www/js/terrasoft-all-combined.js` file.


![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/scr_sources_tab.png)

8. **Debug Creatio Mobile**.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure\#see-also "Direct link to See also")

[Set up the mobile app emulator](https://academy.creatio.com/documents?id=15029)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure\#resources "Direct link to Resources")

[Official Android Studio website](https://developer.android.com/studio)

[Command-line tools](https://developer.android.com/tools) (official Android Studio documentation)

[Environment variables](https://developer.android.com/tools/variables) (official Android Studio documentation)

- [Debug Creatio Mobile in Freedom UI](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure#title-15904-1)
- [Debug Creatio Mobile in Classic UI](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure#title-15904-2)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/mobile/mobile-development/debugging-mobile-app/general-procedure#resources)