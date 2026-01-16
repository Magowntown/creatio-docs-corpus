<!-- Source: page_174 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 09/20/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.1 Quantum, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-10 "Direct link to Creatio composable apps")

**Composable architecture milestone**. Creatio 8.1 Quantum is the next stage in the transition to composable architecture. This release includes multiple composable apps that both include all-new features and let you use existing features while taking full advantage of Freedom UI capabilities. More composable apps are going to follow soon.

### Productivity [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-11 "Direct link to Productivity")

You can now organize your working hours, view and plan activities of your subordinates, track interconnections between activities and other Creatio sections, and keep records of completed tasks in Freedom UI using the **Productivity** app built entirely using Creatio no-code tools.

You can also use the **Calendar** component from the app in your own customizations. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-4).

Productivity app

![Productivity app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_productivity_app.png)

### Digital Ads [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-12 "Direct link to Digital Ads")

You can now evaluate the effectiveness of advertising in Freedom UI using the **Digital Ads** app built entirely using Creatio no-code tools. The app offers seamless integration with both Facebook Ads and Google Ads. You can calculate how many contacts each advertising campaign attracted as well as check the cost of their attraction effortlessly. Learn more: [Overview of Digital Ads app](https://academy.creatio.com/documents?id=2461).

Digital Ads app

![Digital Ads app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_ad_campaigns_section.png)

### Lead And Opportunity Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-13 "Direct link to Lead And Opportunity Management")

You can now manage opportunities and leads in Freedom UI easily using the **Lead And Opportunity Management** app built entirely using Creatio no-code tools. Apply effective lead capturing tools, segment leads to focus on the best opportunities, and monitor the lead pipeline that follows industry standard lead lifecycle stages to detect and eliminate bottlenecks as early as possible.

Lead And Opportunity Management app

![Lead And Opportunity Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_lead_and_opportunity_management_app.png)

### Knowledge Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-111 "Direct link to Knowledge Management")

You can now create and maintain a knowledge base in Freedom UI using the **Knowledge Management** app built entirely using Creatio no-code tools. Enrich the knowledge base with internal company policies, answers to the frequently asked questions, equipment specs, and other valuable information.

Knowledge Management app

![Knowledge Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_knowledge_management_app.png)

### Case Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-14 "Direct link to Case Management")

**Streamlined migration to Case Management app**. It is now possible to convert portal messages in the case history to feed messages available for external users and visible in the **Case Management** app. To do this, run the Convert portal messages to Freedom UI external feed messages business process.

**Functionality for external users in Freedom UI**. External users can now create cases and track their statuses, post comments, and grade the provided solution in Freedom UI.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-8 "Direct link to End user experience")

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-9 "Direct link to Freedom UI sections")

**Communication options on mobile**. It is now possible to use the new **Communication options** mobile component to manage the communication options.

Communication options component on mobile

![Communication options component on mobile](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_mobile_communication_options.png)

**Timeline UX improvements**.

- The component now displays chats and their entire content.
- The component now displays the **External** label next to emails that external users can view.
- It is now possible to filter component record by type, for example, activity, call, etc.
- It is now possible to filter component records by date. Specify the column to use in the filter in the in the **Sort by** component parameter.
- It is now possible to filter component records by owner. Specify the column to use in the filter in the **Column for owner filtering** component parameter. The component uses the **Created by** column out of the box.
- It is now possible to hide automated emails from the timeline, for example, case registration and status change notifications.
- You can now search for component records by text, number, and lookup columns using the built-in search bar.
- It is now possible to sort component records by date.
- The component now groups records by months to improve readability.

Timeline setup was also enhanced. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-4).

Improved Timeline component

![Improved Timeline component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_timeline.png)

**List UX improvements**.

- It is now possible to filter data of a different list by active row even if you bulk select records.
- It is now possible to use the Ctrl + LMB (Cmd + LMB) keyboard shortcut to select multiple list records.
- It is now possible to select every record currently filtered in the component.

Selecting every list record

![Selecting every list record](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/gif_select_all.gif)

List setup was also enhanced. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-4).

**Opened pages preserved on relogin**. If you relogin to Creatio after the user session ends by timeout, Creatio opens the page you previously had open.

**Saved toggle panel states**. Creatio now saves the changes to toggle panel state made on live pages.

**Chart UX improvements**.

- Stacked chart series no longer display 0 values.
- Large numbers on X and Y axes are now shortened. For example, Creatio displays 450k instead of 450 000.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-1 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-2 "Direct link to Application Hub")

**Improved app generation using AI**. It is now possible to generate an even better app using text prompts.

- Generated apps now contain demo data.
- Generated apps now include dynamic cases and **Progress bar** components on form pages.
- Generated apps now contain a customizable mini page for adding lookup and expanded list records.
- Error descriptions during app generations are now more elaborate and user-friendly.

**App update notifications**. Development and test environments of Creatio in the cloud now notify system administrators about Marketplace app updates in the following ways:

- message in the notification panel
- icon on the app tiles in the Application Hub
- update button in the No-Code Designer

**Package exclusion from apps**. You can now exclude an unlocked package from an app without deleting the package from the environment. Learn more: [Exclude a package from an app](https://academy.creatio.com/documents?id=2419&anchor=title-2419-1), [Add an existing package to an app](https://academy.creatio.com/documents?id=2419&anchor=title-2419-2).

**Limited app content displayed in the Freedom UI Designer**. You can now check how your app looks like both on its own and when enhanced by other composable apps. Open Freedom UI Designer from the Application Hub to view the content only within the app package dependencies. Open Freedom UI Designer from the app section to view all dependencies that affect the app.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-4 "Direct link to Freedom UI Designer")

**Multiple form pages for a single object**. It is now possible to create multiple form pages for a single object in the Object Designer as well as in the settings of both **List** and **Button** components. The app determines the page to open based on a field value. For example, this lets you have completely different pages for different request types.

Creatio opens the default form page when the **Continue in other page** button action is executed.

**Tags**. You can now add and manage tags of any entity in Freedom UI using the **Tags** component. Tags can have different permission types and custom colors. New apps include the component on form pages out of the box.

Tags component

![Tags component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_tag_component.png)

**Tag filters**. It is now possible to filter tags using the lookup quick filter.

**Calendar**. You can now view and manage records that have start and end dates as tiles in a **Calendar** component. This is particularly useful for any kind of tasks and activities.

The component includes the following features:

- You can select the primary and secondary fields to display on tiles
- You can filter tiles by period or participants using the **Quick filter** component.
- The component supports static filters.
- The component includes different display modes based on selection period: day, week, month, multi-month.
- You can configure working hours to display in the component.
- The component includes the current time indicator.
- You can drag the tiles to move them.

The new **Productivity** composable app also includes the component out of the box. Learn more: [Productivity](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-11).

Set up the Calendar component

![Set up the Calendar component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_calendar_setup.png)

**Timeline improvements**.

- Unique data sources. You can now set a timeline data source that is different from the default page data source. For example, this is useful if you want to display the account timeline on a case or opportunity page. Select the data source based on the lookup fields of the current or related objects.
- Automatic content update. When you set the **Show in Timeline component by default** property in an object, Creatio adds object content to every existing **Timeline** component automatically. For example, this is useful when you install an app that is connected to existing Creatio sections.

Timeline UX was also improved. Learn more: [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-9).

**Selection window for Dropdown fields**. It is now possible to specify whether to use a drop-down value selector or a full-scale selection window with **Dropdown** fields. This feature streamlines the selection process for large lookup values, for example, products. The selection window is a fully customizable Freedom UI page.

**Bulk action setup in lists**. You can now specify which bulk actions the users can execute in the **List** component. Currently, you can select from **Delete data** and **Export to Excel** actions.

List UX was also improved. Learn more: [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-9).

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-6 "Direct link to Integrations")

**Webhook management in the UI**. You can now use the **Webhooks** section of the **Studio** workplace to analyze incoming webhooks as well as view parsed results and errors in parsing. We recommend using the section in Freedom UI. Learn more about webhooks: [Webhook service integration](https://academy.creatio.com/docs/8.x/no-code-customization/category/webhook-service-integration).

Webhooks section

![Webhooks section](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_webhooks_section.png)

**New email page**. It is now possible to write and send emails using a new Freedom UI page.

New email page

![New email page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_new_email_page.png)

**TAPI UX improvement**. It is now possible to resume held calls while they are in the Attendant transfer mode.

**Deprecation of old Oracle versions**. Oracle ended support for Oracle DBMS versions 11 and 12, thus Creatio no longer supports these versions. We strongly recommend updating your Oracle DBMS to the most recent version.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-16 "Direct link to Advanced customization")

**Updates to Freedom UI page metadata**. It is now possible to store attributes in page metadata in ways that let you overwrite or update array items entirely and prevent issues with non-removable filter items from predefined filters or any other object properties. The specific changes are as follows:

- viewModelConfig property was replaced with the new viewModelConfigDiff property.
- modelConfig property was replaced with the new modelConfigDiff property.

The changes are compatible with existing pages.

**Detailed descriptions of OData 3 and OData 4 errors**. The issue that disabled detailed descriptions of these errors was fixed. The services now return a detailed response that contains the error cause description if an error occurs.

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-5 "Direct link to Administration")

**Streamlined UI management**. It is now possible to manage the type of Creatio UI for users or user groups as well as specify what type of form pages to open in Freedom UI and Classic UI quickly and easily. Perform the setup in the new **UI management** section of the **Studio** workplace.

UI management section

![UI management section](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_ui_management_section.png)

**Filtered list column selection for external users in Classic UI and Freedom UI**. To ensure the security of internal data, the column selection window now displays only columns specified in the "List of schema fields for external access" lookup to external users if the object does not have column permissions set up. Once you set up column permissions, the window displays only columns to which the external users have the corresponding permissions instead.

**Filtered list column selection for all users in Classic UI**. The column selection window in Classic UI can now display only columns to which all users have the corresponding permissions. Turn on the "UseColumnReadPermissionsForStructureExplorer7x" feature to take advantage of this functionality. Instructions: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631) (developer documentation).

**Automatic distribution of server licenses**. Creatio now distributes server licenses among users automatically.

**Improved License Manager UX**. The License Manager now includes a filter by license type.

**Amazon ElastiCache**. Creatio now lets you use Amazon ElastiCache with Redis. This is particularly useful if you host Creatio on your own AWS subscription.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes\#title-2782-17 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.1 Quantum. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Subscription details in the Application Hub**. It is now possible to view the current subscription plan of your organization as well as track the usage of plan limits in the new **Subscriptions** section of the Application Hub. This functionality is available only for organizations that bought a subscription and received a customer ID. Contact your CSM to take advantage of the functionality.

Viewing the subscription details

![Viewing the subscription details](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/gif_subscription_details.gif)

Important

To evaluate the features below, turn on the "AppsFeatures.CanInstallPrereleaseComposableApps" feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the [Creatio support](mailto:support@creatio.com) to enable the feature, then install the beta versions of the apps from Creatio Marketplace.

**Order And Contract Management**. You can now maintain a product catalog as well as create orders and invoices in Freedom UI using the **Order And Contract Management** app built entirely using Creatio no-code tools.

Order And Contract Management app

![Order And Contract Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_1/scr_order_and_contract_management_app.png)

**Updates to Email Marketing app**. Mechanisms that let you send marketing emails both manually and using an automated marketing campaign were added.

**Updates to Engagement Tools app**. The following features were added:

- Contact-to-lead functionality that lets you create leads from well-nurtured contacts that have high level of interest.
- Generation of prospects from Facebook.

**Updates to Event Marketing app**. Audience management workflow was improved.

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-10)
  - [Productivity](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-11)
  - [Digital Ads](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-12)
  - [Lead And Opportunity Management](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-13)
  - [Knowledge Management](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-111)
  - [Case Management](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-14)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-8)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-9)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-4)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-6)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-16)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-5)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/81-quantum-release-notes#title-2782-17)