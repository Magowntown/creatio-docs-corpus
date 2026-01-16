<!-- Source: page_139 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 11/03/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with the following **new features** included in Creatio version 8.0.5 Atlas.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-1 "Direct link to No-code platform")

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-2 "Direct link to Business rules")

**New title names**. Automatically generated business rule titles now describe the rule behavior, for example, "Hide elements: Category." The title is added after you save a rule.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-3 "Direct link to Freedom UI Designer")

**Approvals**. You can now manage approvals in Freedom UI quicker and easier using the new components:

- **Approvals**. Approve or deny records in a single click as well as view the number of pending approvals. You can optimize the page space by displaying the component only if the record has a connected approval.
Approvals component

![Approvals component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_approvals_component.png)

- **Approvals list**. View the entire approval process of a specific record as a list to ensure approval transparency.
Approvals list component

![Approvals list component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_approvals_list_component.png)


**Search**. It is now possible to search for records in any Freedom UI list, attachment list, or approval list using the **Search** component. The expanded list and approval list components as well as the list page template include the component by default.

Searching for a record

![Searching for a record](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/gif_search_component.gif)

**Toggle panel**. You can now group elements using the **Toggle panel** element. Compared to the similar **Tabs** element, toggle panel has the following **unique features** that let you create more advanced page functionality:

- Toggle panel is controlled by buttons you can place anywhere on the page.
- You can click the active tab button to hide the panel. Click any tab button to display the panel again. The panel is hidden by default.

The app page template now includes a toggle panel that contains the **Feed** and **Attachments** components.

Using the Toggle panel element

![Using the Toggle panel element](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/gif_toggle_panel_element.gif)

**Email**. You can now manage email addresses using the **Email** field and input. The elements can validate the email address format if needed.

**Web link**. You can now manage URLs using the **Web link** field and input.

**Autonumbering**. It is now possible to number new records in Freedom UI automatically quicker and easier using the **Autonumber** field. You can set the number prefix and change the quantity of digits in the number. Creatio populates the field both when you add a record manually and when a business process or integration add it.

Autonumber field

![Autonumber field](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_autonumber_field.png)

**Gallery view for attachments**. You can now display the attachments in the list as a gallery and specify the gallery item size.

**Flex container alignment**. It is now possible to align elements in flex containers vertically and horizontally.

**New name of the Freedom UI Designer tab**. The browser tab name of the Freedom UI Designer now follows the "Page name – Designer – Creatio" pattern. This lets you discern between main Creatio tabs and Freedom UI Designer tabs more easily, streamlining the Freedom UI Designer workflow.

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-4 "Direct link to Application Hub")

**App transfer between trial environments**. You can now transfer apps between trial Creatio environments in the Application Hub without the need to download apps. For example, this is useful for Creatio partners that need to set up demo websites. To transfer an app, select "Deploy app" in the app context menu and select the destination website.

Transfer an app

![Transfer an app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_deploy_app.png)

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-5 "Direct link to UI and system capabilities")

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-6 "Direct link to Administration")

**Switch from Basic to OAuth authentication**. Microsoft is deprecating Basic (login/password) authentication in favor of OAuth authentication for Office 365 users. The Basic authentication method will be turned off completely on January 1, 2023. This, in turn, will turn off the email and calendar synchronization service for Office 365. Learn more on the Microsoft Tech Community website: [Basic Authentication Deprecation in Exchange Online – September 2022 Update](https://techcommunity.microsoft.com/t5/exchange-team-blog/basic-authentication-deprecation-in-exchange-online-september/ba-p/3609437).

As such, we strongly recommend switching to more secure and modern OAuth authorization method if you are using Basic authentication. This will ensure your email keeps working as intended. Learn more about setting up the OAuth authentication in user documentation: [Set up OAuth authentication for Microsoft Office 365](https://academy.creatio.com/documents?id=2154).

If you experience migration issues or have additional questions, contact [Creatio support](mailto:support@creatio.com).

### Freedom UI Sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-7 "Direct link to Freedom UI Sections")

**Rich text UX**. The user experience in the **Rich text** field and input was greatly improved:

- Images. To add an image, click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/btn_image.png) button on the toolbar, paste the image from buffer, or drag the image to the element.
- Links. To add a link, click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/btn_link.png) button on the toolbar or paste the link from buffer. You can modify the link caption if needed.
- Tables. To add a table, click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/btn_table.png) button on the toolbar to create a table from scratch or paste the table from buffer.

New text formatting options

![New text formatting options](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_rich_text_new_features.png)

**Feed UX**. The user experience in the **Feed** component was greatly improved:

- Rich text. You can now format text using the same features as the **Rich text** field and input, including images.
- User mention. It is now possible to mention a user in the post or comment by typing "@" and entering a user contact name. After the user is mentioned, Creatio notifies them via the notification panel.
- Editing and deletion. The author can now edit or delete feed posts and comments.
- Quick post. You can now press Ctrl + Enter to add a post or comment using the keyboard.

New Feed component options

![New Feed component options](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/scr_feed_new_features.png)

**Email fields**. Emails in the field and list columns use the "mailto:" link format. Click an email to open the email client associated with such links.

**Web link fields**. URLs in the field and list columns use the hyperlink format. Click a URL to open it in a new browser tab.

**Chart data search**. You can now search for records in the drill-down data table of a Freedom UI chart using the new search component.

Searching for records in the drill-down data table

![Searching for records in the drill-down data table](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/gif_drill-down_search.gif)

**Container scrollbars**. Creatio now displays scrollbars only after you hold the pointer over a scrollable component. This improves the UI readability.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-8 "Direct link to Out-of-the-box Creatio solutions")

### Mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-9 "Direct link to Mobile app")

**Data synchronization setup**. You can now use no-code tools to specify the records to synchronize with the offline mode of the mobile app. To do this, set object data filters or turn off synchronization for particular objects on the synchronization setup page of the Mobile Application Wizard.

Setting up a record synchronization filter

![Setting up a record synchronization filter](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/gif_mobile_synchronization_filters.gif)

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-10 "Direct link to Development tools")

**Package install scripts**. You can now customize the app install process using the new install script functionality. Install scripts are schemas of C# source code that can be executed as part of the app installation process.

Unlike SQL scripts, changes to data implemented using install scripts are completely reversible. When you roll the configuration back, Creatio rolls back the data changed by the script to the state prior to the installation as well. This lets you solve problems related to execution of data operations as part of app installation or updates. For example, app preconfiguration, demo data generation, etc.

You can set the script to run before package installation, after package installation, or before package deletion. You can also run multiple install scripts for a single package and drag the scripts to change their execution order.

It is also possible to run the script on the current instance by clicking the "Run as install script" button in the Source Code Designer. This lets you check the outcome of the script execution without transferring the app between environments.

Learn more about the package install scripts in developer documentation: [Customize delivery process](https://academy.creatio.com/documents?id=15009).

Adding package install scripts

![Adding package install scripts](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_5/gif_install_scripts.gif)

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes\#title-2472-11 "Direct link to Beta testing of new features")

Important

The feature below is available for beta testing in Creatio version 8.0.5 Atlas. To evaluate new Creatio capabilities, contact [Creatio support](mailto:support@creatio.com) to receive the setup instructions. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**New service that receives webhooks**. You can now integrate Creatio with landing page designers that send form submissions via webhooks using the new Creatio webhook service. The service lets you add new business logic to Creatio and add object records based on the webhook structure.

Streamlined integration with the Landingi.com service is already available. You can map the fields of landing page forms created using the service to Creatio fields and import the lead to the needed Creatio object. Learn more about the integration on Creatio Marketplace: [Landingi connector for Creatio](https://marketplace.creatio.com/app/landingi-connector-creatio).

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-1)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-3)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-4)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-6)
  - [Freedom UI Sections](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-7)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-8)
  - [Mobile app](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-9)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-10)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/805-atlas-release-notes#title-2472-11)