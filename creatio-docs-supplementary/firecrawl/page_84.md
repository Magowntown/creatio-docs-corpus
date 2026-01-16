<!-- Source: page_84 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 08/10/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.0.10, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-1 "Direct link to No-code platform")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-2 "Direct link to Application Hub")

**AI app generation**. It is now possible to accelerate app development drastically using AI. Simply describe the purpose of the app in plain text and the AI will generate data model, sections, pages, and fields automatically.

Generate an app using AI

![Generate an app using AI](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/scr_generate_an_app.png)

**Package deletion**. You can now delete editable packages in the No-Code Designer.

**Update notes for Marketplace apps**. The installation window for Marketplace apps now includes the **What’s new** section that contains update notes.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-3 "Direct link to Business rules")

**Disable element**. You can now make fields or inputs read only as well as disable buttons, menu items, and other page components using the "Make elements read-only" business rule.

**Static filter**. You can now create static filters using business rules. For example, display only customers in the **Contact** dropdown field.

**Dropdown field clearing and population**. You can now set up automatic clearing and population of dropdown fields while setting up business rules that contain dynamic filters.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-4 "Direct link to Freedom UI Designer")

**Quick filter improvements**.

- You can now set up the Date/Time quick filter by two columns, for example, activity start and due dates.
- You can now set up the Lookup quick filter via reverse connections, for example, filter activities by participant.

**List improvements**.

- It is now possible to turn list row numbering on and off in the component settings.
- It is now possible to turn bulk record selection on and off in the component settings.

**Streamlined configuration of Freedom UI pages**. Whether the users are working with preconfigured Freedom UI pages in a business process or using the "Open specific page" button action to load the Freedom UI page, the "Save" and "Cancel" button actions are readily available without the need for custom code.

**New button actions**.

- Delete data. Deletes selected records from the **List** component.
- Continue in other page. Opens the default form page for the data source without saving the record yet. This is particularly useful for mini pages.

**Enhanced mini page templates**. Mini page templates now have the **Continue in other page** button.

**Attachment restrictions for message composer**. The **Message composer** component now restricts the upload of email attachments based on the values of "Attachment max size" ("MaxFileSize" code), "File Security Mode" ("FileSecurityMode" code), and "MaxAttachmentSize" system settings.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-5 "Direct link to Business processes")

**Pre-configured mini pages**. You can now use Freedom UI mini pages in the **Pre-configured page** process element. For example, this lets you create an info box as part of the business process.

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-6 "Direct link to Administration")

**New user licenses**.

- External user. The license enables users to work with an unlimited number of sections and data quantity but can be issued only to users that are a part of external organization. For example, the license works great for partner company representatives.
- Data input restricted user. The license enables users to work in one or more sections only with data the user adds themselves, such as support cases. You can issue this license for both employees and external users. Some sections, such as **Knowledge base**, can prohibit data entry but display data added by other users instead. For example, this license works great for members of a large customer service portal.
- Mobile only user. The license enables users to access Creatio only via the mobile app. For example, this license works great for field sales or service teams.

Learn more: [Creatio Composable Pricing](https://www.creatio.com/products/pricing).

**Improved lookup selection UX in Freedom UI**. It is now possible to streamline the value selection process in Freedom UI lookup fields by excluding inactive (archived) reference records from the selection list.

**Global search update**. Global search functionality was updated to version 4.0. The main component of the service, Elastic Search, was updated to version 8.2.2. Now, bulk actions, for example, data import, do not affect individual queries and are indexed faster.

**Freedom UI in .NET 6**. Freedom UI is now turned on for new .NET 6 Creatio instances out of the box.

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-7 "Direct link to Performance")

**Improved loading time**. Freedom UI pages that contain many elements now load up to 30% faster.

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-8 "Direct link to UI and system capabilities")

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-9 "Direct link to Freedom UI sections")

**List UX improvements**.

- Bulk record deletion. You can now select multiple records in lists and bulk delete the selected records.
- Column settings for external users. Saving the list column settings for all users now saves them for external users as well.

**Filtered list column selection**. The column selection window now displays only columns to which you have the corresponding permissions. The functionality is turned on for new Creatio instances out of the box. Turn on the "UseColumnReadPermissionsForStructureExplorer" feature by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) to take advantage of this functionality in existing Creatio instances.

**Page UX improvements**.

- Maximized pages. You can now get even more workspace by maximizing pages to the entirety of the browser tab.
Maximizing a page

![Maximizing a page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/gif_expanding_the_list.gif)

- Saved component states. Creatio now saves the following changes made to components on live pages:
  - expansion panel state (expanded/collapsed)
  - tab selection

**Feed UX improvements**.

Profile photo in a mention

![Profile photo in a mention](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/scr_feed_mention.png)

- Photos in mentions. The component now displays the profile photo of the user when you mention them.
- Messages for external users. You can now create feed messages available for external users as well as mention external users.
- Attachment deletion. You can now delete uploaded files when you edit a post or comment.
- Improved layout. The component is now more readable when placed in narrow containers.
- Faster likes. The like action now takes less time to complete.

**New keyboard shortcuts for mini pages**.

- Esc: closes the page
- Ctrl + S: saves data

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-10 "Direct link to Out-of-the-box Creatio solutions")

### Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-111 "Direct link to Creatio Sales")

**Improved stage logging mechanism for dynamic cases**. Creatio now logs case stages to **History** detail in **Leads** and **Opportunities** sections according to DCM settings.

### External user management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-11 "Direct link to External user management")

**Password reset emails**. External users can now reset their password using the user email instead of login email. If the user login does not have an email address, Creatio sends the email to the address specified in the **Email** field of the user page.

**Streamlined access permission setup**. You can now set up access permissions for external users in the **Object permissions** section without using the "List of objects available for external users" and "List of schema fields for external access" lookups. Objects must have operation permissions set up to be available for external users.

**Object permission warning**. Creatio now warns you if you have not set up permissions to dropdown fields of an object on a page available for external users or the permissions you have set up are not secure.

Permission warning

![Permission warning](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/scr_permission_warning.png)

**Organization profile in Freedom UI**. External users that have the "Administrator for external organization" role can now open the organization profile in Freedom UI.

### Mobile App [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-12 "Direct link to Mobile App")

**Activity search** You can now search for data in activity details.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-13 "Direct link to Development tools")

**Automatically activated packages**. It is now possible to create packages that get activated or deactivated automatically based on the availability of required dependencies in an environment. This lets you create an ecosystem of composable apps that work both as individual apps and enhancements to functionality of other apps. Learn more: [Smart activation package](https://academy.creatio.com/documents?id=15071).

**Compilation logs**. The "CompilationHistory" object now saves the results of configuration, OData, or assembly package compilation that was run manually or automatically. If errors and warning occur as part of the compilation, the object saves them as well. To view the "CompilationHistory" object data, register the object in the **Lookups** section. Learn more: [Compile the configuration](https://academy.creatio.com/documents?id=15101&anchor=compilation-errors-and-warnings).

**TypeScript code in Freedom UI**. You can now add custom TypeScript code to Freedom UI pages.

**App package deletion**. You can now delete packages that are a part of apps in the **Configuration** section.

**Configuration section UX**. You can now use the Ctrl+S keyboard shortcut to save changes in Designers of the **Configuration** section.

**Custom layouts for mobile**. You can now have more control over the layout of mobile Freedom UI pages by setting up custom layouts in page properties. For example, you can specify the order of **Area** layout elements.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes\#title-2782-14 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.0.10 Atlas. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Lead and Opportunity Management app**. You can now manage opportunities and leads in Freedom UI easily. Apply effective lead capturing tools, segment leads to focus on the best opportunities, and monitor the lead pipeline that follows industry standard lead lifecycle stages to detect and eliminate bottlenecks as early as possible.

Lead and Opportunity Management app

![Lead and Opportunity Management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/scr_leads_and_opportunities.png)

**Beta apps**. You can now view beta versions of composable apps in the app creation window. For example, this is useful if you want to test beta versions on a development or test environment. To evaluate this functionality, turn on the "AppsFeatures.CanInstallPrereleaseComposableApps" feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature.

You can test the following apps:

- Lead and opportunity management. Lets you manage the sales pipeline.
- Digital Ads. Lets you analyze the efficiency of ads on popular platforms.
- Engagement Tools. Lets you generate leads and collect web analytics.
- Email Marketing. Lets you conduct email marketing campaigns.
- Event Marketing. Lets you manage and automate events.
- Knowledge Management. Lets you set up the knowledge base.
- Productivity. Lets you manage activities using a calendar.

**Update notifications for Marketplace apps**. Creatio administrators now receive update notifications for Marketplace apps in the communication panel and Application Hub. To evaluate this functionality, turn on the "AppsFeatures.CheckApplicationUpdates" feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature.

**Improved UX of feed mentions**. You can now improve the search speed and accuracy when mentioning users in posts or comments of the **Feed** component by utilizing the global search service. To evaluate this functionality, turn on the "ESMention feature" in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature.

Update the global search service before turning on the feature in Creatio on-site. If you need additional information, contact support.

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-6)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-7)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-8)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-9)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-10)
  - [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-111)
  - [External user management](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-11)
  - [Mobile App](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-12)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-13)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/8010-atlas-release-notes#title-2782-14)