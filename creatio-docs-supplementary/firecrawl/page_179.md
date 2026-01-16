<!-- Source: page_179 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 02/20/2024

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are pushing things forward with Creatio version 8.1.2 Quantum, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-10 "Direct link to Creatio composable apps")

### Lead Generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-11 "Direct link to Lead Generation")

You can now manage the initial stages of the customer qualification process using **Lead Generation** app built entirely using Creatio no-code tools. The management process begins with receiving form submissions from integrated landing pages and extends to nurturing contact needs through a variety of marketing automation workflows. These workflows leverage diverse data sets, including valuable insights from Matomo web analytics.

The app is available for all existing Creatio Marketing customers automatically.

Lead Generation app

![Lead Generation app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_lead_generation.png)

### Event Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-14 "Direct link to Event Management")

You can now plan, promote, and manage successful events seamlessly using **Event Management** app built entirely using Creatio no-code tools. Use comprehensive event management features to streamline registration processes, enhance attendee engagement through personalized experiences, and gain valuable insights to measure and optimize event success.

The app is available for all existing Creatio Marketing customers automatically.

Event Management app

![Event Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_event_management.png)

### Knowledge Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-113 "Direct link to Knowledge Management")

**Playbook**. You can now display knowledge base articles to users based on the active stage of a dynamic case using the **Playbook** component. Configure the articles in the **Playbooks** section of the **Knowledge Management** app.

Playbook component

![Playbook component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/gif_playbook.gif)

### Digital Ads [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-114 "Direct link to Digital Ads")

**Select ad accounts to connect**. You can now specify which of all available Facebook or Google ad accounts to connect to Creatio.

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-115 "Direct link to Creatio Marketing")

**Email subscription status**. You can now check whether a contact is subscribed to bulk emails on the contact page.

**Unsubscribe signal**. It is now possible to use contact unsubscribing from a bulk email as a signal in business processes.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-8 "Direct link to End user experience")

**Calls in Freedom UI**. You can now manage calls in the new Freedom UI **Calls** section and form page. The section contains useful filters and lets you find the needed call record easily. The form page contains metrics that provide convenient overview of the most important call timing values.

Call page

![Call page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_call_page.png)

**Summaries UX improvements**.

- Create custom summaries by any object column or directly connected column.
- Save applied summaries for all users. Creatio merges settings saved for all users and settings applied by a particular user and displays them both.
- Reset applied summaries to default.

**Static folders for Classic UI objects**. It is now possible to work with static folders of Classic UI objects in Freedom UI. You can add static folders, bulk add records to or remove them from the folder, and convert dynamic folders to static folders.

**Combined chat messages of the same Creatio contact**. It is now possible to combine messages of the same Creatio contact sent from different contact IDs within the same channel in a single Creatio chat window. For example, if a customer messages support from multiple WhatsApp accounts listed under the same Creatio contact, the chat agent can view the entire communication history in a single place.

**Image format validation**. Content Designer now checks whether the format is supported when you upload an image.

**Email UX improvements**.

- Emails sent from Creatio as part of a thread are now displayed as a single thread in third-party systems as well, for example, Microsoft Outlook.
- Creatio now makes multiple attempts to send an email if the first attempt fails with "Internal server error," for example, due to temporary server issues.
- If Creatio cannot send an email due to an issue with the recipient, for example, incorrect email address, Creatio now shows a notification that contains the description of the issue in the email panel.
- Autofill behavior for **To**, **From**, and **Subject** fields on email page was improved in Microsoft Edge.

**Restrictions to adding new lookup values**. Creatio now displays the **Add new** button in **Dropdown** fields on form pages only if the following conditions are met:

- Lookup has an existing page.
- You have permissions to add new records to the lookup.
- "Enable adding new values" option is turned on for this field.
When adding lookup values from an editable list, only the first two conditions are required.

**Number format change**. It is now possible to change the number format for the user on the user profile page without changing their culture.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-1 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-2 "Direct link to Application Hub")

**Ability to edit your own apps**. You can now edit the contents of apps installed from a \*.zip archive if the maintainer of the environment and maintainer of the app or package match.

**Custom app start page**. No-code developers that own the app can now specify the page that opens when a user clicks the **Run app** button. Learn more: [Change the app start page](https://academy.creatio.com/documents?id=2405&anchor=title-3990-3).

Select the app start page

![Select the app start page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_select_app_page.png)

**App versions**. No-code developers can now specify the app version in the app properties using numbers in X.Y.Z or X.Y format. Creatio uses this field for Marketplace apps to compare the installed app version with the Marketplace version.

**Names of current app packages**. Creatio now generates names of automatically created current app packages based on the app code.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-4 "Direct link to Freedom UI Designer")

**New button actions that enhance the Productivity app**.

- You can now send calendar invitations to meeting participants in Freedom UI using the "Send invite" button action.
- You can now create emails in Freedom UI using the "Create an email" button action. The action lets you define connections to add automatically when an email is sent. For example, link the email activity sent from the case to the account and contact related to the case.

**Default page that adds records**. You can now specify a default page that adds records even when you have typified pages set up.

**Lazy loading in Freedom UI Designer**. Freedom UI Designer now loads only components you can view to ensure you can load even pages that have a lot of content quickly.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-4 "Direct link to Business processes")

**Bulk process launch**. You can now set up bulk actions in the list using no-code tools by launching multiple instances of a process by selected list records.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-6 "Direct link to Integrations")

**OAuth health check**. It is now possible to monitor the health of OAuth functionality in Creatio. To do this, load the `[sitename]/0/api/OAuthHealthCheck` URL. The tool checks whether the required system settings are filled out, the Identity service is available, and the OAuth token is retrievable. You can use the tool manually or as part of integration with automated monitoring systems. Learn more: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513).

**Automatic creation of external users for OpenID**. Creatio can now add an external user automatically when they log in via an OpenID provider for the first time.

**Improvements to the SSO configuration UI**.

- Upload a public SSL certificate for signing and encryption of SAML requests by clicking the **Upload certificate** button.
- Validate the signing of SAML requests by selecting the **Signature validation** checkbox. We strongly recommend not using the SSO login without SAML signing or encryption. This configuration will be insecure and can be used only for development environments.
- Specify where to display the "login via SSO" link: on the main login page, login page for external users, or both. Perform the setup in the **User type** field of the **Additional parameters** section of the SSO provider page.
- Import the SSO configuration from an SSO metadata file. This lets you create a new SSO provider or update an existing provider quickly and easily. Creatio adds all settings automatically, including the SSO certificate for signing and encryption of SAML requests.
- Turn off Single Log Out (SLO) for SSO configuration. If SLO is turned off, the user is logged out only from Creatio upon logout from Creatio. If SLO is turned on, the user is logged out from all services that use SSO upon logout from Creatio.

SSO setup page

![SSO setup page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_sso_setup_page.png)

**Conditional rules in Intune**. You can now set up conditional rules in Intune for the **Mobile Creatio for Intune** app available on iOS and Android.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-16 "Direct link to Advanced customization")

**Package hotfixes**. You can unlock packages in the configuration for hotfixes. Creatio re-locks the packages automatically after a customizable period. The audit log tracks the package unlock/lock action. Learn more: [Package hotfixes](https://academy.creatio.com/documents?id=15091).

**Compilation error indicator**. The system administrator can now see an indicator about compilation errors at the top of the app page. Click the indicator to view the error list in the **Configuration** section. Learn more: [Compile the configuration](https://academy.creatio.com/documents?id=15101&anchor=compilation-errors-and-warnings).

**Compilation error list**. It is now possible to check the list of compilation errors present in your configuration using the **Compilation errors** button in the **Configuration** section. This button is visible only if your configuration has compilation errors. The error list takes into account both full configuration compilation and compilation of separate assembly packages. Learn more: [Compile the configuration](https://academy.creatio.com/documents?id=15101&anchor=compilation-errors-and-warnings).

**System setting values for external users**. It is now possible to read system setting values for external users. This enables developers to create logic that sets unique system setting values for external users.

**Mobile SDK enhancements**.

- Work with multiselection window using custom code.
- Open a customized dialog box using custom code.
- Create an embedded detail that includes custom buttons.

**Conditional rules in Intune**. You can now set up conditional rules in Intune for the **Mobile Creatio for Intune** app available on iOS and Android.

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes\#title-2782-5 "Direct link to Administration")

**Enabled content security policy**. After an update to 8.1.2, Creatio turns on Content Security Policy functionality in logging mode automatically if it was disabled previously.

**Content security policy in the UI**. You can now manage content security policy in the System Designer.

Setup page of content security policy

![Setup page of content security policy](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1_2/scr_content_security_policy.png)

**Streamlined UI management for external users**. The "Use Freedom UI interface for external users" ("UseNewShellForExternalUsers" code) system setting was removed. The "Use Freedom UI interface" ("UseNewShell" code) system setting now controls UI management for external users as well. You can also manage UI preferences for external users as well as other users and roles in the **UI management** section. Freedom UI is turned on for external users on new Creatio instances out of the box.

**Enhanced page permission checks**.

- Creatio now checks whether the section list page is added to any workplace the user can access. If it is not, Creatio opens the desktop instead of the page.

- Creatio now checks whether the Classic UI page belongs to a section added to a workplace the user can access. If it does not, Creatio opens the desktop instead of the page.

**The restrictions above** do not apply to users or roles that have permissions to the "Can use bypass page opening restrictions" ("CanBypassPageOpeningRestrictions" code) system operation. For existing Creatio instances, these roles include "All Employees" and "All External Users."

- You can now set up an allowlist of pages any user can open via direct URL regardless of permissions. To do this, add the relevant pages to the **Whitelist of pages to bypass page opening restrictions** lookup.

- Creatio no longer performs automatic access checks for pages opened as part of a business process.


**Performance improvements**.

- Loading time of lists that have many rows and columns was optimized.
- Classic UI pages are now up to 50% smaller, which speeds up the initial loading of Creatio.
- Creatio now loads pages that include **Timer** components faster.

**Deprecation of old PostgreSQL versions**. PostgreSQL version 11 reached its end of life, thus Creatio will only support version 16 and later since Creatio 8.1.3.

**Deprecation of old Kubernetes versions**. Kubernetes version 1.15 reached its end of life, thus Creatio will only support version 1.25 and later since Creatio 8.1.3.

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-10)
  - [Lead Generation](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-11)
  - [Event Management](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-14)
  - [Knowledge Management](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-113)
  - [Digital Ads](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-114)
- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-115)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-8)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-4)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-6)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-16)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/812-quantum-release-notes#title-2782-5)