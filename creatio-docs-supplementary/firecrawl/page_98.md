<!-- Source: page_98 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 12/07/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.1.1 Quantum, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-10 "Direct link to Creatio composable apps")

### Order And Contract Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-11 "Direct link to Order And Contract Management")

You can now manage the product catalog, orders, invoices, contracts, and other documents in Freedom UI using the **Order And Contract Management** app built entirely using Creatio no-code tools.

Order And Contract Management app

![Order And Contract Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/scr_order_page.png)

### Knowledge Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-111 "Direct link to Knowledge Management")

All new instances of Sales, Marketing, Service, and Financial Services Creatio products now include the app out of the box. The app section replaces the classic UI **Knowledge base** section.

### Case Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-14 "Direct link to Case Management")

Contact and account timelines now display linked cases.

Cases in the Timeline component

![Cases in the Timeline component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/scr_cases_in_timeline.png)

### Customer 360 [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-13 "Direct link to Customer 360")

Contact and account pages in the mobile app now include the **Timeline** component.

### Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-113 "Direct link to Creatio Marketing")

It is now possible to add campaign participants automatically from landing pages integrated via webhooks using the new **Add from web page** campaign element. The element is triggered when a user submits a web form on the landing page.

Add from web page campaign element

![Add from web page campaign element](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/scr_add_from_web_page.png)

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-8 "Direct link to End user experience")

**Calendar UX improvements**

- You can now add online meeting links to activity descriptions and click the **Join** button to join the meeting quickly. Creatio shows the button on the mini page and full page of the activity within 15 minutes from the beginning of the meeting and during the entire duration of the meeting. Learn more about configuring the functionality: [Add a service to connect to online meetings](https://academy.creatio.com/documents?id=2392).
- You can now create meetings for a selected period. To do this, select a period, type the name, and press Enter.
- You can now customize the time scale. Available values are 5 minutes, 10 minutes, 15 minutes, 30 minutes, and 1 hour.
- The component saves all changes, for example, resizing an activity, immediately. You no longer need to click the **Save** button to apply changes.
- The current time indicator now uses the time zone specified in the user profile.
- The secondary fields of activity tiles now utilize all available tile space.
- To ensure stable performance, the component automatically switches to the lightweight mode and hides the secondary tile fields if you load a significant number of meetings for a period.

Calendar setup was also enhanced. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-4).

**Improved rich text UX**

- Rich text fields, feed messages, and emails in the **Timeline** component now scale images you insert into the text box to fit it if they are wider than it.
- You can now click images to view their full version in rich text fields, feed messages, and emails in the **Timeline** component.

**Bulk add tags**. You can now bulk add or remove tags if you select multiple records in a Freedom UI list.

Tag setup was also enhanced. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-4).

**Streamlined connection of WordPress landing pages**. You can now connect landing pages created using WordPress via Elementor to Creatio much easier. You only need to specify where to send webhook data in Elementor settings.

**Attachment search**. You can now search for attachments in the Freedom UI component by name using global search. Creatio indexes attachment names automatically.

**Live list updates**. Creatio now updates Freedom UI lists in addition to Freedom UI fields automatically without the need to refresh pages if you turn on the **Enable live data update** property of the object.

**Live feed updates**. Comments and messages in the feed are now updated in real time without the need to refresh the page.

**New activity completion flow in the Next steps component**. To ensure the correct operation of background logic, the mini page that completes activities no longer contains the status field. To complete an activity, click the result of the activity instead.

New activity completion flow

![New activity completion flow](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/gif_complete_an_activity.gif)

**Improved performance when editing records**. If a single record is updated multiple times in a short period, Creatio now applies each update more smoothly.

**Protection of system field data**. To ensure Freedom UI apps operate as intended, system fields, for example, "Created by," "Modified by," "Created On," "Modified On," are now marked as read-only automatically. You no longer need to set up the editability manually.

**Localization update for the mobile app**. The mobile app now supports Polish and Italian languages.

**Improved loading time of Freedom UI pages**. Creatio now loads Freedom UI pages you previously had open significantly faster. For example, if you open a list page, then open the record page and go back to the list page, the list page loads faster than the first time.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-1 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-2 "Direct link to Application Hub")

**Improved package management UX**.

- You can now create app packages from the No-Code Designer. If the app does not contain an editable current package, Creatio sets the new package as the current app package automatically.

- You can now add existing packages to apps in the No-Code Designer. The package must meet the following requirements:


  - available for editing
  - not a primary package of any other app
  - not included in the current app

If the app does not contain an editable current package, Creatio sets the added package as the current app package automatically.

- No-Code Designer now creates a current app package only when you save changes to schemas.

- You can now set any editable package as the current app package from the package action menu in the No-Code Designer.

- No-Code Designer now marks the current package in the list of app packages using ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/icn_current_package.png).

- You can now open package properties from the package action menu in No-Code Designer.


### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-4 "Direct link to Freedom UI Designer")

**Email connection to specific records**. You can now link emails sent via **Message Composer** and **Next steps** components to records besides the current record using no-code tools. For example, link the email sent from the case page to the account and contact related to the case.

**Independent setup of similar inputs**. You can now set up inputs connected to the same page field differently. This includes settings in the element setup area and conditional properties defined by business rules.

**Summaries**. You can now manage summaries of list records in Freedom UI using the new **Summaries** component.

Summaries component

![Summaries component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/scr_summaries.png)

**Color coded activities in the calendar**. New modes that color code tiles in the **Calendar** component are available:

- Automatic. Color codes tiles based on a lookup value. For example, activity status. If the lookup has no colors associated with columns, the component assigns colors randomly.
- By user. Color codes tiles based on the activity participant. For example, this is useful if you want to find common free time slots to schedule a meeting. Available if you build the calendar by "Activity" object.

Calendar activities color coded by participant

![Calendar activities color coded by participant](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/scr_color_coded_calendar.png)

Calendar UX was also improved. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-8).

**Timeline component improvements**

- You can now set custom codes for objects of the **Timeline** component, for example, "Activity." Creatio also generates codes automatically based on the "TimelineTile\_\[#ObjectName\]\_\[#RandomSuffix\]" pattern.
- You can now specify which filters to display in the **Timeline** component.

**Tag setup improvements**

- The component now supports tags set up in Classic UI. If the object has Classic UI tags set up, Creatio selects the Classic UI tag model automatically. Otherwise, Freedom UI tag model is used. You can switch between Classic and Freedom UI tag models at any moment.
- You can now set permissions to specific actions with tags, for example, create or edit, in the "Access to tag grantee" lookup.

Tag UX was also improved. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-8).

**New button action**. You can now print reports by any object in Freedom UI using the **Print report** button action.

**Improved UX of data model attributes**

- Creatio now marks data model attributes that are already present on the page with ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/icn_existing_attribute.png).
- Creatio now marks required data model attributes with ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_1/icn_required_attribute.png).

**New page template**. New "Tabbed page with Progress bar" template was added. The template includes the newest **Progress bar** and **Next steps** components and replaces the "Tabbed page with Action dashboard" template.

**Improved object search**. Object search algorithm in the Freedom UI Designer is now more precise.

**Editable codes of data model attributes**. You can now change codes of data model attributes after creating them.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-4 "Direct link to Business processes")

**Freedom UI pages in Classic UI**. You can now open Freedom UI pages when working with business processes even if you use Classic UI.

**Performance improvements**

- You can now cancel any number of business processes without an impact on Creatio performance.
- Creatio now executes loops within business processes faster.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-6 "Direct link to Integrations")

**Microsoft Intune compatible mobile app**. You can now ensure maximum security of your resources across various devices by using a mobile app version that is compatible with Microsoft Intune and Mobile Application Management restrictions. To receive the app files, contact [Creatio support](mailto:support@creatio.com).

If you enable Intune integration, Creatio server no longer becomes accessible via the base mobile app version.

**Streamlined Cisco Finesse integration**. It is now possible to set up the Cisco Finesse integration for Finesse version 11.6 and later without enabling websocket in the server settings. Select the Cisco Finesse 11.6 BOSH connector in the "Default messages exchange library" ("SysMsgLib" code) system setting to take advantage of this feature.

**Integration performance**. Creatio now performs more efficient permission checks for integration requests that perform login operations frequently. For example, out-of-the-box Microsoft Exchange integration.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-16 "Direct link to Advanced customization")

**Code outside of Creatio zone**. You can now run custom code outside of Creatio zone, similarly to runOutsideAngular in the Angular framework. This lets you optimize the execution of code that does not affect navigation between pages, for example, logging events in the background. Learn more: [Creatio zone](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/creatio-zone).

**Custom filters**. It is now possible to use custom filters in page schema handlers during development.

**Compilation UX improvements**

- You can now check the user who ran compilation in the **Started by** column of the "Compilation history" object.
- You can now check how much time compilation took in the **Duration** column of the "Compilation history" object. For example, this is useful if you want to estimate how long new compilation will take.

Learn more: [Compile the configuration](https://academy.creatio.com/documents?id=15101&anchor=compilation-errors-and-warnings).

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-5 "Direct link to Administration")

**New user licenses**. "Data input restricted" user license was replaced with the following licenses: "External B2C," "Limited internal," "Self-service."

"External B2C" license works best for customers that interact with your company. For example, patients who schedule visits and view test results, subscribers who review services and pay bills or students who view timetables and submit homework. Users that have this license can work with any number of Creatio sections. You can issue this license only to external users. This license has the following user restrictions:

- Users cannot be a part of an organization available for external users.
- Users cannot interact with other external users.
- Users cannot view data created by other external users. However, they can view data created by company employees based on object permissions.
- Users cannot use communication features, for example, chat, telephony, and email.
- Users cannot set up columns, create folders and tags, or build dashboards.

"Limited internal" license works best for company employees who require Creatio only for a single use case. For example, approve invoices, send requests, etc. You can issue this license only to company employees. This license has the following user restrictions:

- Users can work with only a single Creatio section specified by the system administrator. They can also access **Knowledge base** section in read-only mode.
- Users cannot use communication features, for example, chat, telephony, and email.

"Self-service" license works best for users that only require a support portal. You can issue this license to both company employees and external users. This license has the following user restrictions:

- Users can access only **Cases** and **Knowledge base** sections.
- Users can only register cases, not process them.
- Users cannot use communication features, for example, chat, telephony, and email.
- Users cannot set up columns, create folders and tags, or build dashboards.

Learn more: [Creatio composable pricing](https://www.creatio.com/products/pricing).

**New workplace types**. Creatio now includes **Limited internal** and **Self-service** workplace types. Users that have the corresponding licenses can view them. The workplace types apply section restrictions automatically. For example, if you add **Cases**, **Knowledge base**, and **Accounts** sections to a workplace of **Self-service** type, users that have the corresponding license can view only **Cases** and **Knowledge base** sections.

If you add more than one workplace of the same type, users that have the corresponding licenses can view only the first workplace as per the sorting order.

**Attachment deletion**. Creatio now deletes the record attachments from the "Uploaded file" table automatically when a section record is deleted. Out of the box, the attachments are deleted 2 days after the record is deleted. You can customize the delay in the "File deletion delay period, days" ("FileDeletionDelayPeriod" code) system setting.

**Multiple form pages for a single object available for external users**. You can now set one or more of the form pages created for a single object to be available for external users.

**Page permissions enforced for direct URLs**. Users that lack permissions to an object can no longer access pages whose data source is that object directly via URLs. If they open the URL, Creatio loads the desktop instead. This restriction does not apply to users or roles that have permissions to the "Can use bypass page opening restrictions" ("CanBypassPageOpeningRestrictions" code) system operation.

**RestSharp library deletion**. RestSharp library was deleted from all Creatio products due to security vulnerabilities. The library was required to generate REST requests to external services. If you have a custom solution that inherits from RestSharp directly or uses "RestClientFactory," "RestSharpExt," or "RestSharpJsonConverter" classes, we recommend switching to IHttpRequestClient instead. If you want to ensure backward compatibility, contact [Creatio support](mailto:support@creatio.com).

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes\#title-2782-17 "Direct link to Beta testing of new features")

Important

The feature below is available for beta testing in Creatio version 8.1.1 Quantum. To learn more about the feature, contact [Creatio support](mailto:support@creatio.com). You can also contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Online meeting rooms for Microsoft Teams**. Creatio can now add online meeting rooms for Microsoft Teams. A room is added when a meeting organizer sends invitations to participants. The participants receive email notifications that contain the call details.

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-10)
  - [Order And Contract Management](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-11)
  - [Knowledge Management](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-111)
  - [Case Management](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-14)
  - [Customer 360](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-13)
  - [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-113)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-8)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-4)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-6)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-16)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-5)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/811-quantum-release-notes#title-2782-17)