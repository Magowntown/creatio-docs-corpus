<!-- Source: page_187 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 07/29/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with the following **new features** included in Creatio version 8.0.3 Atlas.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

[![tech_hour](https://academy.creatio.com/sites/en/files/images/Release_notes/tech-hour-rn_bg_small.jpg)](https://www.youtube.com/watch?v=6JiiXjeq-CI)

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-1 "Direct link to No-code platform")

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-2 "Direct link to Freedom UI Designer")

**Set up Freedom UI record pages for any Creatio object**. You can now set up Freedom UI record pages for any Creatio object regardless of its origin, for example, out-of-the-box sections or lookups. You can start configuring the page from the Freedom UI Designer in a few clicks. Creatio adds the new page to the app where you created it. After you set up the page, it will open from any part of Creatio that uses the corresponding object. Learn more in user documentation: [Create a custom Freedom UI page for a Creatio object](https://academy.creatio.com/documents?id=2406).

**Field tooltips**. It is now possible to set up tooltips for fields of all the main types:

- text
- number
- checkbox
- dropdown
- date/time

Creatio displays a tooltip when you hold the pointer over the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/icn_info.png) icon to the right of the field.

**Buttons that add and open records**. New setup options were added to buttons that add and open records:

- Sections that have multiple pages, for example, **Activities**, now can receive default values from the button that adds new records.
- It is now possible to create or edit a Freedom UI record page for any Creatio object quickly from the button setup area. These objects include out-of-the-box sections, details, and lookups as well as objects created using the Section Wizard or development tools.

**New button actions**. Creatio 8.0.3 Atlas lets you set up buttons that import and export data. Button actions have the required logic preconfigured, for example, the selection and handling of the file that contains the data to import.

**Editable list**. Freedom UI now supports editable lists. The editability is enabled by default in the **List** element settings. You can disable the editability in a single click if needed

Set up a List component

![Set up a List component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/scr_admin_list_settings.png)

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-3 "Direct link to Application Hub")

**App title validation**. App title requirements were simplified:

- Character restrictions were removed. Now, the app name can contain alphanumeric and special characters.
- The minimum required number of characters is 3.
- The maximum number of characters is 100.

**Unique app code generation**. The automatic generation of the app code was optimized:

- Creatio generates the unique app code based on its title, which streamlines configuration management and app transfer. We recommend using at least one Latin word in the title since the code can contain only digits and Latin characters.
- To generate the code, Creatio requires at least 3 characters suitable for the package code and name generation. If the app title contains multiple spaces, Creatio removes them from the code and formats the code in camelcase. For example, the code of the "Document Management" app is "UsrDocumentManagement."
- If the app title contains fewer than 3 characters suitable for code generation, Creatio generates the code in the format of "AppUsr\_gfgvd08j."
- If you change the app title, Creatio updates the code accordingly.
- If you change the unique app code manually, Creatio does not update the code on further changes to the app title.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-4 "Direct link to Business processes")

**Process log archival**. You can disable the process log archival if you do not need to store the archived data. In this case, Creatio deletes the process execution records that are older than 30 days. This helps to avoid the accumulation of unneeded data and improves the performance of logging. You can manage the record archival using the "Archive data on deletion from log" ("ArchiveProcessLogOnDeletion" code) system setting. The archival is disabled by default for new Creatio environments. The settings of existing environments remain unchanged.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-5 "Direct link to Integrations")

**Fault-tolerant Email Listener configuration**. Fault-tolerant Email Listener configuration was adapted to work without Kubernetes Statefullset. This lets you deploy the microservice using alternative orchestrators to Kubernetes.

**Fault-tolerant email synchronization**. The stability of the email synchronization process was improved. If the QRTZ trigger required to start the email synchronization is missing, Creatio recreates it automatically. You can also initiate the trigger recreation manually using the "Recreate Listener Service Fail Job" business process.

**Avaya Aura phone integration**. The libraries were updated to support the Avaya 8.0.x, 8.1.x, 10.1.x connector.

**Cisco Finesse phone integration**. New connector for Cisco Finesse version 11.5 and later that supports WebSocket connection was released. Also, you no longer have to set up ARR in IIS to set up the phone integration.

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-6 "Direct link to Administration")

**SSO authentication**. SSO parameter setup was updated:

- It is now possible to set up the base SSO login from Creatio UI without the need to edit the configuration files.
- You no longer need to restart Creatio after you add a new provider.
- Presets were added for common providers: Azure, AD FS, Okta.
- You can test the applied settings in the **Single Sign On configuration** section.
- If you have already set up an authentication provider, Creatio displays the link to log in using SSO on the login page of your website. You no longer need to specify the default login page.
- Creatio database stores the SSO provider settings. You no longer need to restart Creatio after you add a new provider.
- If you have multiple providers set up, the login page displays multiple authentication links.
- Backward compatibility was preserved. The providers you have previously set up using the configuration files will keep working without the need for an additional setup.
- If you need to set up a non-standard configuration, you can always contact the Creatio support.

Set up SSO parameters

![Set up SSO parameters](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/scr_sso_setup_page.png)

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-7 "Direct link to UI and system capabilities")

### Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-8 "Direct link to Freedom UI")

**Management of an editable list**. You can now edit data of Freedom UI lists without opening record pages.

- Select a list cell to check its editability status represented by the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/icn_freedomui_list_editable.png) or ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/icn_freedomui_list_uneditable.png) icon.

- Creatio marks edited yet unsaved data using the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/icn_freedomui_list_edited.png) icon. The font of the edited text is also bold.

- If Creatio is unable to validate the edited data, the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/icn_error.png) icon appears to the right of the cell. Hold the pointer over the icon to view the error description. The same icon appears at the beginning of the row.

- After you edit one or more cells, the control panel ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/scr_actions.png) appears at the bottom. Use the panel to save or cancel the changes made on the page. You can drag the panel around the page. To do this, hold the left mouse button while holding the pointer over the left border of the panel.

- You can cancel changes made to a single row using the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/btn_freedomui_list_undo.png) button. The button appears to the left of the row after you edit one or more cells.

- Currently, you cannot edit a cell if any of the following conditions are met:
  - You lack permissions to edit the selected record.
  - You lack permissions to edit the selected column.
  - You selected a system column, for example, **Created on**.
  - You selected an aggregate column.
  - You selected a column of the linked object.
- If you prefer to manage a list using a keyboard, a wide variety of actions is available:
  - Use the cursor keys to move between cells.
  - Press Enter to edit the selected cell.
  - Press Tab or Enter once again to apply changes.
  - Press Space to switch the checkbox value.
  - Press Ctrl + S to save the changes.

Managing an editable list

![Managing an editable list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/gif_editable_list_short.gif)

**Frozen list columns**. You can now unfreeze a frozen column by clicking the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/btn_pin.png) button to the right of the column title.

**Chart data export**. You can export chart and pivot table data to Excel to process data easier. To do this, expand the dashboard and select **Export to Excel** in the context menu. The browser will download the data file to your computer.

Exporting dashboard data

![Exporting dashboard data](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/gif_export_dashboard.gif)

**Chart data drill-down**. You can now drill down the data of "Gauge" and "Metric" charts and metrics.

**Favorite folders**. Since Creatio version 8.0.3 Atlas, you can add Freedom UI folders to favorites. Favorite folders are available in the folder management menu, which lets you select and apply the filter quickly without opening the folder tree.

### Chats [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-9 "Direct link to Chats")

**View messages of incomplete chats**. You can now view the messages of incomplete chats in the **Chats** section. This enables managers to understand the context without additional actions, for example, chat escalation, and make quick decisions.

**Automatic chat completion**. The mechanism that automatically completes chats was improved. Now Creatio applies the chat completion timeout mechanism both to incoming and outgoing messages. Chats processed by agents are completed if either the agent or the customer is not responding within the specified period.

**Telegram chat setup**. You no longer need to fill out the "Website URL" ("SiteUrl" code) system setting to set up the Telegram channel integration.

### Email setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-10 "Direct link to Email setup")

**Secure Office365 setup**. Microsoft is deprecating the login and password authentication (Basic Authentication) method since it is obsolete and insecure. We recommend setting up secure OAuth authentication in the near future so that you do not lose access to your mailboxes from Creatio. Learn more in user documentation: [Set up OAuth authentication for Microsoft Office 365](https://academy.creatio.com/documents?id=2154).

**Shared mailbox setup**. You can now add shared mailboxes that use OAuth authentication to Creatio.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-11 "Direct link to Out-of-the-box Creatio solutions")

### Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-12 "Direct link to Creatio Marketing")

**Email deliverability monitoring**. To help you analyze the reasons for an email delivery failure, the Creatio Marketing homepage now includes a dashboard that shows the detailed reasons for a delivery failure of emails that received the "Hard Bounce," "Soft Bounce," "Delivery error" responses. Also, the **Contacts** section now includes folders that let you quickly view the index of contacts who did not receive the emails. To streamline the workflow, the data is grouped by the reasons for a delivery failure. The email deliverability monitoring lets you maintain the relevance of the contact base and increase the efficiency of emails.

Dashboard to analyze the reasons for email delivery failure

![Dashboard to analyze the reasons for email delivery failure](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/scr_bounce_monitor_dashboard.png)

**UTM marks in lead management**. It is now possible to save the UTM mark data (utm\_source, utm\_medium, utm\_campaign, utm\_content, utm\_term) for leads created using a landing page or social network integration. The **Lead** object now includes the corresponding fields. You can display them on the record page if needed. You can use the fields to set up custom logic connected to the marks: filters, dashboards, business processes, etc.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-13 "Direct link to Development tools")

**Front-end Freedom UI development**. You can add components that classic Creatio pages do not use to the Freedom UI Designer. You can create such components from scratch or upload them from external resources. We recommend using components created with the Angular framework. The component must be developed in an npm package. You can transfer components between Creatio environments similarly to packages and apps. You can display the new components in the Freedom UI Designer library to facilitate their use in no-code development. In this case, they will be available in the "Custom components" group.

**Change transfer**. To ensure safe transfer of changes between environments, it is now possible to mark SQL scripts in your apps as backward compatible. Backward compatible scripts are those whose execution does not make irreversible changes to the database, which lets you roll the configuration back completely. The developer of the SQL script must monitor its backward compatibility. Learn more in the developer documentation: [Backward compatible SQL scripts](https://academy.creatio.com/documents?id=15109).

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes\#title-3964-14 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.0.3 Atlas. To evaluate new Creatio capabilities, enable the feature in a test environment yourself using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Business Rule Designer**. A visual business rule editor was implemented for Freedom UI pages. In version 8.0.3 Atlas, you can set up display rules for page elements.

- To set up business rules, click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/btn_open_business_rules_designer.png) button in the Freedom UI Designer.
- You can set up a condition that triggers the rule upon comparing an attribute (field) to another attribute or a constant.
- When you set up the "Show element" or "Hide elements" actions, you can select multiple elements to show or hide when the rule is triggered. For your convenience, Creatio groups the elements in the index by type: inputs, charts, layout elements, etc. You can search for an element by type, title, or code. At the moment we recommend using the "Hide elements" action since Creatio displays every element and component that you add to the canvas by default.
- You can delete both an individual element in the action block and the action itself.
- Creatio can execute several actions as part of a single rule.

To familiarize yourself with the new capabilities, enable the "SetupBusinessRuleAddonEnabled" feature.

Business Rule Designer for Freedom UI

![Business Rule Designer for Freedom UI](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_3/scr_business_rules_designer.png)

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-1)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-2)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-3)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-4)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-6)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-7)
  - [Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-8)
  - [Chats](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-9)
  - [Email setup](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-10)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-11)
  - [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-12)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-13)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/803-atlas-release-notes#title-3964-14)