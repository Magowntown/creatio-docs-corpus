<!-- Source: page_3 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

All Creatio products

On this page

**Creatio Mobile** is a modern business solution that brings the Creatio platform to your mobile device. Built on the composable no-code architecture of Creatio, Creatio Mobile provides a maximum degree of freedom to automate your unique business processes and customize the user experience with no-code.

Use Creatio Mobile to execute the following actions:

- Synchronize contacts, accounts, leads, activities, sales, etc., among all your devices.
- View, add, modify, and delete records.
- Call contacts directly from within the app.
- Access customer information in offline mode.
- View the latest work updates from your team.

Before you install and use the Creatio Mobile:

1. Make sure the Creatio Mobile version corresponds to the version of the main Creatio app.
2. Make sure your mobile device meets the system requirements.

## System requirements for mobile devices [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-1 "Direct link to System requirements for mobile devices")

To install and use the Creatio Mobile, ensure that your mobile device meets the system requirements listed in the table below.

| Characteristic | Mobile platform |
| --- | --- |
| iOS | Android |
| Supported version (minimal) | 13 | 8 |
| Recommended version | Latest version available | Latest version available |
| Recommended devices | iPhone 13<br>iPhone 13 Pro and later<br>iPad 8 (2020)<br>iPad Air 4 (2020) and later | Google Pixel 2 / 2 XL (2017)<br>Google Pixel 3 / 3a / 3 XL (2018)<br>Samsung Galaxy S8 / S8+ (2017)<br>Samsung Galaxy S9 / S9+ (2018) |

## Install the Creatio Mobile [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-2 "Direct link to Install the Creatio Mobile")

1. **Download the Creatio Mobile**. This is a one-time procedure. Creatio Mobile is available for download on the [App Store](https://itunes.apple.com/us/app/creatio-mobile-7/id708432450?mt=8) and [Google Play](https://play.google.com/store/apps/details?id=com.creatio.mobileapp).

2. **Log in to Creatio Mobile** (Fig. 1).
Fig. 1 Log in to Creatio Mobile

![Fig. 1 Log in to Creatio Mobile](https://academy.creatio.com/docs/sites/academy_en/files/images/NoCodePlatform/SetUpMobileCreatio/8.1/scr_group_mobile_app.png)


Creatio applies the HTTPS connection protocol automatically.

Creatio Mobile lets you log in using the Single Sign-On technology. Instructions: [Authentication](https://academy.creatio.com/docs/8.x/setup-and-administration/category/authentication).

To **explore the Creatio Mobile functionality**, tap the **Demo login** button on the app login page. This accesses the demo version without user credentials. The app login page displays the **Demo login** button automatically if your Creatio Mobile is not synchronized with a main Creatio app.

3. **Synchronize the mobile app** with a main Creatio app. Creatio Mobile launches the synchronization automatically. The synchronization procedure might differ depending on the operation mode.



Important





A certificate signed by a certification authority is required to synchronize with **Creatio on-site**. Creatio Mobile security policies do not support connections to websites that use self-signed certificates.





During the synchronization of the mobile app with a main Creatio app after login, Creatio Mobile executes the following actions:


1. load system data
2. load structure
3. update structure
4. load system settings
5. check if the main app contains data to import
6. import data if needed

When the synchronization is finished, the app opens.

**As a result**, Creatio Mobile will be opened automatically after the synchronization is done. You will be able to start working with the app.

## Creatio Mobile settings page [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-9 "Direct link to Creatio Mobile settings page")

To **open the settings page** (Fig. 2), tap the **Settings** button.

Fig. 2 Creatio Mobile settings page

![Fig. 2 Creatio Mobile settings page](https://academy.creatio.com/docs/sites/academy_en/files/images/NoCodePlatform/SetUpMobileCreatio/8.1/scr_group_mobile_app_settings.png)

Use the settings page of Creatio Mobile to execute the following actions:

- Switch workplaces
- Synchronize the app
- Send feedback
- Log out of the app

### Switch workplaces [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-8 "Direct link to Switch workplaces")

Configure the list of workplaces and sections that are available for Creatio Mobile using the **Mobile Application Wizard** in the main Creatio app. To reduce the synchronization time between the mobile and main Creatio apps, we recommend setting up only the sections you will use.

To switch workplaces:

1. **Open the settings page**. Instructions: [Creatio Mobile settings page](https://academy.creatio.com/documents?id=1920&anchor=title-773-9).
2. **Open the list of available workspaces**. To do this, tap the **Workplace** field.
3. **Select the workplace**.
4. **Change workspace**.

**As a result**, the workspace will be switched and Creatio Mobile will launch synchronization.

### Synchronize the app [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-6 "Direct link to Synchronize the app")

Creatio Mobile synchronizes data **automatically** in the following cases:

- A user works in online mode. Creatio Mobile synchronizes data in the background.
- A user switches the workplace. Instructions: [Switch workplaces](https://academy.creatio.com/documents?id=1920&anchor=title-773-8). Creatio Mobile synchronizes data and restarts the app.

To synchronize the app **manually**:

1. **Open the settings page**. Instructions: [Creatio Mobile settings page](https://academy.creatio.com/documents?id=1920&anchor=title-773-9).
2. **Tap the Synchronize button**.

**As a result**, data from the Creatio Mobile will be synchronized with data from the main Creatio app and vice versa.

### Log out of the app [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-10 "Direct link to Log out of the app")

To log out of the app:

1. **Open the settings page**. Instructions: [Creatio Mobile settings page](https://academy.creatio.com/documents?id=1920&anchor=title-773-9).
2. **Tap the Log out button**.

**As a result**, you will be logged out of the app. Logout clears the cache. If you have changes that are not synchronized with the main Creatio app, launch synchronization before logging out. Otherwise, the changes will be lost.

## Mobile operation modes [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-3 "Direct link to Mobile operation modes")

The following modes are available for Creatio Mobile:

- Online
- Hybrid
- Offline

To **change the operation mode**, use the "Mobile application operation mode" ("MobileApplicationMode" code) system setting in the main Creatio app.

note

Regardless of the selected operation mode, mobile devices only display data that users can access.

### Online mode [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-4 "Direct link to Online mode")

Online mode requires an Internet connection. In this mode, the user works directly with the main Creatio app that works as a Creatio server. Configuration changes are synchronized automatically in real time.

If you select the online operation mode, manual synchronization is not required. The online mode supports real-time synchronization with the Creatio server. For example, when you create a record using the Creatio Mobile, the main Creatio app displays the record automatically and vice versa.

The **difference between online and offline modes** is as follows. For example, the opportunity is moved to the next stage and the business process creates a new activity. When this happens, Creatio Mobile synchronizes with the main Creatio app. The main Creatio app creates the activity, and Creatio Mobile displays the created activity. A user who works online does not notice this business logic because the Creatio Mobile app works directly with the server. Creatio Mobile displays the new activity as soon as the corresponding business process is completed. Manual synchronization is not required. A user who works offline only sees the activity after manual synchronization.

### Hybrid mode [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-14 "Direct link to Hybrid mode")

Hybrid mode is a type of online mode. Hybrid mode is designed for working with data and is activated automatically if a stable connection to the Creatio server is unavailable. This mode lets you create new records and work with schedules. It is also possible to manage 10 section records with which you have interacted recently.

After restoring the connection, the Creatio Mobile resumes real-time synchronization with the main Creatio app. If the same record (for example, the duration of the activity) was changed for both Creatio Mobile and main Creatio app, Creatio saves the changes based on the execution order.

note

The hybrid mode is unavailable for the [Field sales for Creatio](https://marketplace.creatio.com/app/field-sales-creatio) and [Pharma Creatio](https://marketplace.creatio.com/app/pharma-creatio) Marketplace apps.

### Offline mode [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#title-773-5 "Direct link to Offline mode")

For offline mode, an Internet connection is only required for the preliminary import and synchronization. When you use this mode, the app saves data locally to the mobile device. You must manually synchronize data with the Creatio server to receive configuration changes and data updates. Creatio Mobile synchronizes data with the main Creatio app using the DataService service and saves all synchronization conflicts to the synchronization log. The synchronization log is available only in offline mode.

To **view information about the last synchronization**, tap the **Synchronization log** field (Fig. 3). This opens the **Synchronization log** page.

Fig. 3 Open the synchronization log

![Fig. 3 Open the synchronization log](https://academy.creatio.com/docs/sites/academy_en/files/images/NoCodePlatform/SetUpMobileCreatio/8.1/scr_synchronization_log.png)

View the tabs of the **Synchronization log** page in the table below.

| Tab | Tab description |
| --- | --- |
| Log | The tab includes the last synchronization date and a list of all conflicts that occurred during synchronization with the main Creatio app. Conflict details are specified for each record individually. |
| Pending changes | The tab includes the entirety of data that still needed to be exported to the main Creatio app during the last synchronization attempt. |

To **solve the conflict**, click the record on the **Synchronization log** page and select the action. The action depends on the conflict. View the available actions in the table below.

| Action | Action description |
| --- | --- |
| Revert changes | The action reverts all changes and deletes the record from the synchronization log. If you select the action, the record in the Creatio Mobile will be overwritten with the corresponding record from the main Creatio app. For example, a system administrator removed user rights to edit an account type. A conflict occurs when you edit the **Type** field and try to synchronize with the main Creatio app. To solve the conflict, decline the changes and re-synchronize the Creatio Mobile data. Learn more about solving synchronization conflicts: [Creatio Mobile FAQ](https://academy.creatio.com/documents?id=1668&anchor=title-771-2). |
| Go to record | The action opens the record page. For example, an empty field is required. When you create a record whose required field is empty, a conflict occurs. To solve the conflict, open the record page, populate the required field, and re-synchronize Creatio Mobile data. |
| Request access | The action opens a default mobile mail client and creates a request template to provide the permissions required for synchronization. |

Creatio Mobile lets you **send logs** to system administrators. To do this:

1. Make sure the "Email for sending permission requests" ("MobileEmailForPermissionRequests" code) system setting **includes the correct email address**.
2. **Open the settings page**. Instructions: [Creatio Mobile settings page](https://academy.creatio.com/documents?id=1920&anchor=title-773-9).
3. **Tap the Send logs button**.

**As a result**, the logs will be sent to system administrators.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install\#see-also "Direct link to See also")

[Creatio Mobile FAQ](https://academy.creatio.com/documents?id=1668)

[Get started with the Creatio Mobile UI](https://academy.creatio.com/documents?id=1955)

- [System requirements for mobile devices](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-1)
- [Install the Creatio Mobile](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-2)
- [Creatio Mobile settings page](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-9)
  - [Switch workplaces](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-8)
  - [Synchronize the app](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-6)
  - [Log out of the app](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-10)
- [Mobile operation modes](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-3)
  - [Online mode](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-4)
  - [Hybrid mode](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-14)
  - [Offline mode](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#title-773-5)
- [See also](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-install#see-also)