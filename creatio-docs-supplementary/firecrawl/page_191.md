<!-- Source: page_191 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 06/02/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with the following **new features** included in Creatio version 8.0.2 Atlas.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

[![tech_hour](https://academy.creatio.com/sites/en/files/images/Release_notes/tech-hour-rn_bg_small.jpg)](https://www.youtube.com/watch?v=6JiiXjeq-CI)

## Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-2 "Direct link to Freedom UI Designer")

### Freedom UI elements [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-49 "Direct link to Freedom UI elements")

#### Action dashboard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-5 "Direct link to Action dashboard")

- The actions you add to the **Action dashboard** now appear on the canvas in real time.

#### Tabs [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-6 "Direct link to Tabs")

- It is now possible to select the tab style, including the color of the tab panel and tab titles.

- Tab titles now support icons. You can use both text and an icon or replace text with an icon.
Set up a tab title

![Set up a tab title](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_tab_setup.png)

- A setup area, where you can manage tab parameters as well as copy tabs together with their content, was added.


#### Inputs [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-7 "Direct link to Inputs")

- Input fields now support placeholders that contain text and links. If the input has validation set up, the validation message takes priority to the placeholder.

#### Buttons [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-8 "Direct link to Buttons")

- It is now possible to set up menus for action buttons. Menus support multiple levels. A menu item title can contain text, an icon, or both. You can copy existing menu items to accelerate the setup process. You can also copy existing buttons together with their settings.
Set up a button that has a menu

![Set up a button that has a menu](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_button_setup.png)

- If you set up a button that adds records and different record types use different pages, Freedom UI Designer generates the button menu automatically.

- New "Refresh data" button action was added. Use the action to refresh data without refreshing the entire page. The **Expanded list** component and list page template come with this button pre-configured out-of-the-box.

- The icon library for button titles was expanded.

- You can now set different button sizes quickly: S, M, L, XL. For example, this lets you increase the size of icon buttons or reduce the size of text buttons to unify the visual design of the page.

- When you set up a button action that runs business processes, you can select only the latest business process versions.

- If you create a business process when setting up the button, Freedom UI Designer populates the process selection field in the button setup area with the process automatically upon saving.

- Buttons that open pages now let you create and edit the relevant page as part of the button setup. This lets you accelerate the app setup process substantially.


#### Label [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-9 "Direct link to Label")

- The number of **Label** element styles was increased.

### Freedom UI management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-27 "Direct link to Freedom UI management")

#### List management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-28 "Direct link to List management")

- Row numbering was added. This streamlines navigation and data management.
- It is now possible to select individual list cells and move between them using keyboard arrows.
- You can now copy the content of a selected cell using the Ctrl+C keyboard shortcut.
- When you add a record and return to the list, Creatio highlights the new row.
- You can apply list settings to every app user immediately.

#### Data management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-29 "Direct link to Data management")

- Creatio saves data of the folder tree and selected folder settings to the user profile and applies it every time you open the section.
- It is now possible to manage folder access permissions while working in the app. To do this, select the "Set up access rights" action in the folder menu.

Set up folder access permissions

![Set up folder access permissions](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_group_rights_setup.png)

#### Analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-30 "Direct link to Analytics")

- You can now drill down the chart data. You can drill down individual chart points and columns or each chart series. When you drill down the chart data, you can customize the data list similarly to a section list.
Drilling down the chart data

![Drilling down the chart data](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/gif_chart_drilldown_extended.gif)

- When you work in the app, you can change the chart type to analyze data more efficiently.

- The appearance of the **Gauge** component was improved:
  - Sections are now split visually.
  - Captions are shifted so that they do not overlap with the gauge.
  - It is now possible to customize section colors.

#### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-31 "Direct link to Performance")

- Performance of Freedom UI was improved.

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-1 "Direct link to No-code platform")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-53 "Direct link to Application Hub")

#### App export [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-10 "Direct link to App export")

- It is now possible to download an app as an archive to transfer it to different environments. To do this, click "Download" in the app actions menu. This action is available for all apps except base Creatio products.

- When you download an app, Creatio also saves the app properties:


  - icon
  - color
  - name
  - description

Creatio applies the data when you install the app into a different environment.

Download an app

![Download an app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_download_app.png)

#### App installation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-11 "Direct link to App installation")

- The UI of the app installation page was updated.

New UI of the app installation page

![New UI of the app installation page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_install_app_page.png)

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-12 "Direct link to Business processes")

#### Process setup recommendations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-13 "Direct link to Process setup recommendations")

- The accuracy of process setup prediction was improved.
- The recommendation mechanism predicts both the most probable elements and their settings, which lets you accelerate the business process setup substantially.
- Process Designer displays the process step recommendations after you set up an existing element to ensure that prediction corresponds to the element settings.

#### Approvals [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-14 "Direct link to Approvals")

- Creatio now sends approval notifications to a large group of approvers faster.

#### Case setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-15 "Direct link to Case setup")

- Creatio saves cases set up for Freedom UI sections to the same package as the corresponding app. This streamlines the transfer of functionality between environments.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-16 "Direct link to Integrations")

#### Data repository integration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-17 "Direct link to Data repository integration")

- Integration with an external Azure Blow Storage file repository was implemented. After you connect the repository, the files uploaded to the **Attachments** detail or attached to emails are saved to Azure Blob Storage automatically. This lets you reduce the Creatio database size without introducing file restrictions and reduce the time spent on database maintenance.

#### Email Listener setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-18 "Direct link to Email Listener setup")

- It is now possible to open the Email Listener diagnostics page quickly from either the menu in the communication panel or page of configured email services. This requires permission to the "Email providers list setup" ("CanManageMail" servers code) system operation.
- The Email Listener microservice diagnostics page now checks whether the microservice can connect to the Creatio website.

### Email management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-33 "Direct link to Email management")

#### Mailbox setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-34 "Direct link to Mailbox setup")

- If a user who exceeded the daily sent message limit in Gmail tries to send an email from Creatio, they receive a corresponding notification.

- Creatio now handles external issues that block email synchronization. If such a situation occurs, Creatio displays the message that contains the issue description. This lets you resolve the issue without the need to contact support. Creatio handles the following situations:
  - Office365 or Exchange email account does not have a Microsoft license.
  - The account has two-factor authentication enabled in the email service.
  - The account has IMAP support disabled.
- If an authentication error occurs during the email synchronization, Creatio pauses the process and resumes it later without user input.


### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-65 "Direct link to Administration")

#### Containerized components [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-19 "Direct link to Containerized components")

- It is now possible to deploy global search and bulk duplicate search components using Kubernetes orchestrator and Helm package manager. Learn more in separate articles: [Global search](https://academy.creatio.com/documents?id=1712), [Bulk duplicate search](https://academy.creatio.com/documents?id=1959).

#### Oracle [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-20 "Direct link to Oracle")

- Creatio moved to Managed OCAD 12 library, which lets you use newer Oracle versions.

### Security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-21 "Direct link to Security")

#### TLS 1.2 protocol support [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-22 "Direct link to TLS 1.2 protocol support")

- Creatio now supports Redis connection via TLS 1.2 protocol.
- Creatio .NET Core now support LDAP server connection via TLS 1.2 protocol.

#### Information security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-23 "Direct link to Information security")

- You can now configure HTTP response headers. For example, you can use them for browser-side security settings. Perform the setup in the **HTTP response headers** lookup.

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-24 "Direct link to Performance")

#### Performance improvement mechanisms [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-25 "Direct link to Performance improvement mechanisms")

- You can now limit the number of threads required to execute a database query. This lets you reduce the influence of resource intensive operations on user workflow. Set the limit in the "MaxDopQueryHint thread count" ("MaxDopHintThreadsCount" code) system setting.
- A mechanism that prevents external integrations from creating a large number of user sessions was implemented. When an integration creates more than 4 sessions in 1 minute, Creatio caches older sessions and passes their data in a response to a request to create a new session. This increases request sending and execution performance substantially.

#### Mailboxes for case registration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-35 "Direct link to Mailboxes for case registration")

- The **List of mailboxes for case registration** lookup now displays full mailbox addresses, which makes them more informative, for example, if the company uses several domains.

#### OAuth authentication [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-36 "Direct link to OAuth authentication")

- You can now move existing email accounts from login and password authentication to OAuth authentication easier. When the authentication type changes, all users that have active mailboxes receive a communication panel notification that recommends signing in to an external system (Office365 or Google) to continue managing emails.
- If email server issues occur when you add a new mailbox to Creatio or synchronize an existing mailbox, Creatio sends a notification with an error received from the server. This lets you resolve the issue without the need to contact support.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-37 "Direct link to Out-of-the-box Creatio solutions")

### Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-38 "Direct link to Creatio Marketing")

#### Lead generation from social networks [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-39 "Direct link to Lead generation from social networks")

- Creatio .NET Core products now support lead generation from Facebook and LinkedIn.

#### Active contact licenses [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-40 "Direct link to Active contact licenses")

- An indicator that displays the total number of marketing contact licenses and number of available licenses was added to the list page and record page of the **Email**, **Campaigns**, **Events** sections. The color of the indicator depends on the number of available licenses and varies from green (sufficient licenses) to red (no vacant licenses).

License indicator

![License indicator](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_marketing_active_licenses.png)

#### Emails [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-41 "Direct link to Emails")

- ElasticEmail users can now view the reasons for Hard Bounce and Soft Bounce responses. The reasons are specified in the **Response reason** and **Reason details** columns on the **Audience** detail of the bulk email page and **Email - Bulk emails** detail of the contact page.

#### Communication option validity [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-42 "Direct link to Communication option validity")

- The mechanism that selects the "Valid" checkbox for contact communication options was updated. Now Creatio selects the checkbox based on a set of rules that take reasons for receiving the Hard Bounce response into account.

### Phone integration and communication management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-43 "Direct link to Phone integration and communication management")

#### Asterisk PBX [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-44 "Direct link to Asterisk PBX")

- Linux installation files of CMS were updated.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-45 "Direct link to Development tools")

### Change transfer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-46 "Direct link to Change transfer")

- Commands that call backup operations for packages whose new versions to install into the environment as well as commands that restore the configuration from package backup via the Workspace Console utility were added. The mechanism works similarly to the backup and restore functionality available when installing apps or packages by custom means. Learn more in separate article: [Delivery in WorkspaceConsole](https://academy.creatio.com/documents?id=15207&anchor=title-2138-13).

- The mechanism that generates the app's unique code, package name, and name of app schemas was optimized. Creatio generates names based on the app title and "Prefix for schemas and packages name" ("SchemaNamePrefix" code) system setting. For example, if the prefix in the system setting is "Usr", Creatio generates the following values for the "Requests" app:
  - "UsrRequests" code
  - "UsrRequests" package
  - "UsrRequests", "UsrRequestsFormPage" schema code

### Front-end Freedom UI development [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-47 "Direct link to Front-end Freedom UI development")

- You can now use existing elements of classic Creatio pages on Freedom UI pages. To do this, create a web component based on the classic page element. Learn more in separate article: [Implement a custom web component using a 7.X component](https://academy.creatio.com/documents?id=15374).
- It is now possible to use converters on Freedom UI pages when binding query parameters. For example, this lets you pass converted attribute values in the converters without additional intermediate steps.

### Custom web services [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-48 "Direct link to Custom web services")

- You can now develop custom WCF web services using non-standard text encodings for .NET Framework apps. For example, you can use ISO-8859, ISO-2022, etc. encoding families. Learn more in separate article: [Develop a custom web service that uses anonymous authentication and non-standard text encoding](https://academy.creatio.com/documents?id=15270).

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-50 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.0.2 Atlas. To evaluate new Creatio capabilities, enable the feature in a test environment yourself using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request Creatio support to enable the feature. Contact us if you have feedback, we appreciate it: `beta@creatio.com`.

#### Freedom UI business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-3 "Direct link to Freedom UI business rules")

- A business rule that filters fields based on values of other fields was implemented. You can set up the rule at the Creatio object level. In this case, Creatio applies the rule to all pages that contain the affected fields. For example, the rule that filters cities based on countries in contact or account addresses is applied when you use these fields in any new UI. The feature is enabled by default in version 8.0.2.

#### Freedom UI elements [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-4 "Direct link to Freedom UI elements")

- New **Gallery** element can display visual data of any Creatio object on a page. Besides images, the gallery supports record caption and brief description text. To familiarize yourself with new capabilities, enable the "ShowDesignerDemoItems" feature.

Set up a gallery

![Set up a gallery](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_2/scr_gallery.png)

#### Dashboards [​](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes\#title-2359-51 "Direct link to Dashboards")

- You can now view additional data about chart elements (column, area, segment) as another chart. For example, when you analyze a chart that displays employees by departments, you can drill down the R&D department data and visualize the number of department positions. To familiarize yourself with new capabilities, enable the "ChartDrilldown" feature.

- [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-2)
  - [Freedom UI elements](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-49)
  - [Freedom UI management](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-27)
- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-53)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-12)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-16)
  - [Email management](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-33)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-65)
  - [Security](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-21)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-24)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-37)
  - [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-38)
  - [Phone integration and communication management](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-43)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-45)
  - [Change transfer](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-46)
  - [Front-end Freedom UI development](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-47)
  - [Custom web services](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-48)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/802-atlas-release-notes#title-2359-50)