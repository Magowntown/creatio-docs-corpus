<!-- Source: page_122 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 02/27/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.0.7, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-1 "Direct link to No-code platform")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-2 "Direct link to Application Hub")

**Localizable section names**. You can now localize names of new and the existing Freedom UI sections in the Application Hub.

**New character limit for section names**. Section names can now contain up to 50 characters.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-3 "Direct link to Business rules")

**Advanced business rule conditions**. It is now possible to set up more advanced business rules using system settings and system variables in business rule conditions. For example, you can set up a rule that displays the **Results** field if the current user is the record owner.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-4 "Direct link to Freedom UI Designer")

**Improved UX of the expanded list**. You can now set up the **Expanded list** component more quickly and easily. All you have to do is select a list object, and the Freedom UI Designer automatically links every relevant component to the object. The title of the expansion panel is updated automatically as well provided that you have not changed the title manually.

**Editable element code**. You can now edit the code in the **Element code** field of the element setup area to make the code more informative.

**Duplicate search action**. Creatio 8.0.7 Atlas lets you set up search for duplicate records in Freedom UI using the new **Open duplicates page** button action. You can connect the button to any section that supports the duplicate search functionality.

**Chart values**. You can now specify whether to display values of individual bars and columns on "Bar" and "Column" chart types, respectively.

### Customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-5 "Direct link to Customization tools")

**Improved accuracy of machine learning models**. You can now increase the accuracy of machine learning models trained on string fields by specifying words to exclude from the training. For example, customer signature, greeting, etc.

**Search by phone number**. You can now improve the accuracy of search queries that contain phone numbers by indexing **Phone number** fields in the global search service.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-6 "Direct link to Integrations")

**Increased security requirements for email server connection**. Support for email server connections using an invalid (self-signed, expired) SSL certificate will be retired in Creatio 8.0.8. This is an unsafe connection option that is prone to various SSL attacks. If you are using an invalid SSL certificate, we strongly recommend switching to a valid certificate to ensure uninterrupted operation of the email service.

**Improved webhook management**. Multiple stages of the webhook management workflow in Creatio were improved:

- API key generation. You can now generate an API key for Landingi.com service automatically on the web form setup page in Creatio. The web form setup page is available in the Freedom UI **Contacts** section as well as in the apps that use the "Records and business processes" template.
Generating an API key for Landingi.com

![Generating an API key for Landingi.com](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/gif_generating_api_key.gif)

- Webhook URL generation. You can also generate a URL to receive webhooks from a landing page created in a different service on the web form setup page.
Generating a webhook URL

![Generating a webhook URL](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/gif_generating_webhook_url.gif)

- Contact search or creation. Creatio now searches for or adds contacts by records that were based on webhooks. This mechanism works with the **Submitted form** object, but you can also extend it to work with any other Creatio object in the "Define search options and create contact from webhook" business process.

- Matomo data import. Creatio can now import site events recorded by the Matomo tracking service as part of processing form submissions from landing pages integrated via webhooks.

- Checkbox fields. Creatio can now import data from checkbox fields via webhooks received from Landingi.com.


Learn more about webhook integration in the user documentation: [Webhook service integration](https://academy.creatio.com/docs/user/crm_tools/landing_pages_and_web_forms/webhook_service_integration).

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-7 "Direct link to Performance")

**Improved loading time**. The Freedom UI pages now load up to 70% faster. The Freedom UI lists now load data significantly faster as well.

**Basic visual mode**. You can now disable advanced visual effects of the Freedom UI by turning on the "Disable advanced visual effects" ("DisableAdvancedVisualEffects" code) system setting. Currently, the setting disables the blur in the semi-transparent "Glass effect" chart style.

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-1 "Direct link to UI and system capabilities")

As part of transition to new architecture, the application UI was revamped in Creatio version 8.0.6. The Freedom UI encompasses the latest and greatest UX best practices to streamline the user workflow all while providing extensive personalization capabilities. Learn more in a separate article: [Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445).

The Freedom UI is turned on for new Creatio instances by default. Learn how to turn on the Freedom UI for existing instances: [Turn on the Freedom UI](https://academy.creatio.com/documents?id=2446).

### Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-8 "Direct link to Freedom UI")

**Global process start button**. The button now displays only the processes that have the **Display in run process button list** checkbox selected in the properties. This streamlines the button UX.

### Communication panel in the Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-10 "Direct link to Communication panel in the Freedom UI")

**Active call indicator**. The Freedom UI now displays the call indicator if you go to a different communication panel tab or minimize the panel while on a call. The indicator displays the contact's full name or the phone number if the number is not linked to the contact. Click the indicator to reopen the call tab.

Active call indicator

![Active call indicator](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/gif_active_call_indicator.gif)

### Appearance customization of the Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-11 "Direct link to Appearance customization of the Freedom UI")

**Custom backgrounds**. You can now add a personal touch to your Creatio application by uploading your own background image or setting the background color.

Custom background

![Custom background](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/scr_custom_background.png)

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-12 "Direct link to Freedom UI sections")

**Automatic field updates**. Creatio can now update fields on open form pages automatically without the need to refresh the page. This functionality is available for the following field types:

- Record fields. For example, the **Assign to me** button on a request page runs a business process that sets the current user as the request owner. If you click the button, Creatio populates the **Owner** field on the request page with your contact, and the result is visible immediately. Turn on this functionality manually for the object whose data is to be updated. To do this, select the **Enable live data update** checkbox in the **Behavior** group of the Object Designer.
- Fields of directly linked records. For example, a contact record has the **Account** and **No. of employees** ("Contact.Account.No. of employees") fields. If you fill out the **Account** field, Creatio populates the **No. of employees** field automatically. This functionality is available for every object by default.

Learn more in separate articles: [Update form page fields automatically](https://academy.creatio.com/documents?id=15379&anchor=title-2397-1), [Update form page fields automatically](https://academy.creatio.com/documents?id=15107&anchor=title-2314-1).

**Preserved scroll position**. Creatio now keeps your scroll position on a Freedom UI page when you return to it.

### Mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-13 "Direct link to Mobile app")

**User info on the settings page**. You can now see which user is logged in to the mobile app on the app settings page.

### Emails [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2549-14 "Direct link to Emails")

**Email participant list**. You can now view the email sender and recipients in the **Participants** detail on the **General information** tab of the email page. Creatio records the participants when you send or receive an email.

Participants detail

![Participants detail](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/scr_participants_detail.png)

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2472-8 "Direct link to Out-of-the-box Creatio solutions")

### Customer 360 [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2472-15 "Direct link to Customer 360")

Important

The feature below is available by default for all Creatio products except Studio. To use this feature in Studio, request the Creatio support to enable it. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Relationships of account records**. You can now manage relationships of account records in Freedom UI **Accounts** section. To do this, click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/btn_relationships.png) button in the top right.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes\#title-2472-16 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.0.7 Atlas. To evaluate new capabilities of the Freedom UI Designer, enable the "ShowDesignerDemoItems" feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Quick filters**. It is now possible to apply custom filters to one or more Freedom UI lists on a page using the **Quick filter** component. For example, you can display only contacts whose type is "Customer."

Using a Quick filter component

![Using a Quick filter component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/gif_quick_filter.gif)

**Message composer**. It is now possible to send emails and post feed messages from any Freedom UI page using the **Message composer** component. You can specify the mailbox sender and delete one of the communication channels if needed. Both communication channels support rich text, including images. The email channel includes the following features as well:

- attachments
- templates
- drafts
- email forwarding
- email thread expansion

Message composercomponent

![Message composercomponent](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_7/scr_message_composer.png)

**Message composer in the timeline**. The **Timeline** component now includes the message composer functionality. This lets you use the component for customer cases.

**Freedom UI in Financial Services Creatio**. You can now turn on the Freedom UI in Financial Services Creatio. The communication panel in the Freedom UI includes the consultation panel.

**.NET 6.** You can use Studio Compatibility Edition (Studio CE) in the classic UI on .NET 6. .NET 6 is a cross-platform framework that lets you run Creatio on both Linux and Windows. Similarly to other Creatio products, configuration source code in Creatio .NET 6 is compiled into code that is compatible with the .NET Standard 2.0. As such, the existing apps are compatible with Creatio .NET 6. To receive the build, contact the Creatio support.

Learn more about Studio CE in the developer documentation: [Package architecture in Studio Creatio 8.1](https://academy.creatio.com/documents?id=15028).

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-4)
  - [Customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-5)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-6)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-7)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-1)
  - [Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-8)
  - [Communication panel in the Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-10)
  - [Appearance customization of the Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-11)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-12)
  - [Mobile app](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-13)
  - [Emails](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2549-14)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2472-8)
  - [Customer 360](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2472-15)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/807-atlas-release-notes#title-2472-16)