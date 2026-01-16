<!-- Source: page_30 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 07/11/2024

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are pushing things forward with Creatio version 8.1.4 Quantum, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-1 "Direct link to Creatio composable apps")

### Order and Contract Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-2 "Direct link to Order and Contract Management")

**Product features**. Enhanced Freedom UI product catalog empowers you to manage and showcase your products with unmatched clarity and efficiency. This update, currently exclusive to Creatio Sales, empowers you to:

- Clearly define product features. Specify details like CPU speed or supported memory for each product, giving customers a clear understanding of capabilities.
- Easy no-code configuration. Leverage the Freedom UI designer to configure the product catalog to perfectly match your business needs.
- Seamless feature-based search. Search the product catalog by specific features, allowing users to quickly find products that perfectly match their needs.

Product features

![Product features](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_product_features_0.png)

**Summaries in product cart**. When you change products in the cart, the Summaries component updates count, quantity, and total price automatically.

### Lead and Opportunity Management​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-3 "Direct link to Lead and Opportunity Management​")

**Playbook on the opportunity page**. You can now use the playbook on the opportunity page. The component displays hints and instructions that let you access information from the knowledge base by specific dynamic case stages.

Opportunity playbook

![Opportunity playbook](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_opportunity_playbook.png)

### Productivity​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-4 "Direct link to Productivity​")

**Display the task in the calendar**. You can now better organize your calendar by hiding some meetings from it or by displaying there some tasks that were initially visible only in the task list.

### Knowledge Management​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-5 "Direct link to Knowledge Management​")

**Plain text conversion for articles**. Creatio now converts and stores the plain text version of each article in the **NotHtmlField** field. For example, this is useful for integrations that export data from Creatio.

## Creatio Marketplace​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-6 "Direct link to Creatio Marketplace​")

**Ada AI Chatbot integration**. You can now use the new **Ada AI Chatbot** composable app to integrate Creatio chats with the Ada AI-powered bots and communicate with customers via multiple social channels. It is also possible to export knowledge base articles to Ada to use them for better answers. System administrator can add Ada channel in the Chat settings section out of the box. If Ada bot hands over unresolved conversation to Creatio agents, a new chat is added and distributed to the chat queue for the most preferable agent. Agents can proceed with chats in the communication panel. Creatio saves both dialogs completed in Ada with no handover and dialogs handed over to agents to Chats section to preserve the communication history. Learn more: [Integrate an Ada chat channel](https://academy.creatio.com/documents?id=15624&anchor=title-15624-1).

## Creatio Marketing​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-7 "Direct link to Creatio Marketing​")

**One-click unsubscription headers**. Due to new requirements for a one-click unsubscribe link in emails sent to Google and Yahoo mailboxes, Creatio adds the necessary headers for one-click unsubscription to marketing emails. As such, you need not worry about being blacklisted by Google or Yahoo servers.

## End user experience​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-8 "Direct link to End user experience​")

**Product filters by feature**. You can now use the hierarchy on the product selection page to set up dynamic filters by product features. The **Hierarchy** component is now also available in Freedom UI Designer. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-10).

Product filters

![Product filters](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_product_filter.png)

**Editable summaries**. You can now edit existing summaries live. To do this, click the summary → **Edit**.

Editing a summary

![Editing a summary](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/gif_editing_a_summary.gif)

**Duplicate search as part of Excel import**. Duplicate search mechanism as part of Excel import was updated:

- If all values of fields required to search for duplicates are empty, Creatio does not consider this record a duplicate and adds a new record.
- If the import procedure is unable to parse values from the Excel file, the record is excluded from import and specified in the import log.

**Icon only navigation panel**. It is now possible to collapse the navigation panel to icon only mode. This mode lets you take the following actions:

- switch between sections
- switch between workplaces
- view the name of the section by holding the pointer over the section icon

Icon only navigation panel

![Icon only navigation panel](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_icon_only_navigation_panel.png)

**Bulgarian and Croatian localization**. You can now use Creatio in Bulgarian and Croatian.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-9 "Direct link to No-code tools")

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-10 "Direct link to Freedom UI Designer")

**Widget setup improvements**.

- Hide the border of widgets that have "Plain white" style.
- View and set up which filtering element is connected to the **chart**, **metric**, or **gauge** in the widget settings. For example, this lets you connect a folder tree directly to the widget without using a list as a proxy.

**Metric setup improvements**.

- Metrics added to pages that have data source now display the count for that object immediately after you add the metric to the canvas. If the page has no data source, metrics are not pre-configured.

- Set "Transparent" style to metrics that removes their background. For example, this is useful if you want to create metrics that look like fields.
Transparent metric

![Transparent metric](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_transparent_metric.png)

- Add icons to metrics and change icon colors if needed.
Metrics that have icons

![Metrics that have icons](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_metric_icons.png)

- Set up metrics without titles.


**Sidebar setup improvements**.

- Specify users and roles who can access a custom sidebar based on operation permissions. Specify the permission in the "Access by operation permission" field of the sidebar parameters.
- Create a custom sidebar as a standalone panel at the top of the working area using Freedom UI Designer.
- Disable the sidebar if needed.
- Hide the notification mark when the user opens the sidebar or code custom behavior.

**Hierarchy**. You can now build hierarchical lists based on data of any object using the new Hierarchy component. For example, create a seamless hierarchy of products by organizing them based on category and type. The component UX also has special features. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-8).

### Business processes​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-11 "Direct link to Business processes​")

**Permission-aware execution**. By leveraging user context for **Read data** process element, Creatio gains increased flexibility for working with sensitive information. This approach enforces least privilege, granting users access only to the specific data their permissions allow. This simplifies workflows and reduces the risk of unauthorized data exposure while maintaining compliance with security regulations. Turn on this functionality in the "Use user permissions for elements" process setting.

Use user permissions for elements process setting

![Use user permissions for elements process setting](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_4/scr_user_permissions.png)

**Automatic expiration of business process traces**. You can now specify default period for trace collection for business processes. Traces expire automatically after this period. This optimizes data storage and system performance.

**Pass records to the process in bulk**. It is now possible to run a single process and pass multiple selected records to a collection parameter.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-12 "Direct link to Integrations")

**Chat settings in Freedom UI**. It is now possible to configure chat settings in Freedom UI.

**Delete chat channels**. You can now delete channels that have related chats or other records on the Chat settings page.

**RAM limit for OData requests**. You can now limit RAM size dedicated to handling OData API requests for data selection. For example, this lets you protect users who are doing everyday Creatio activities from the performance issue caused by inefficient integration. Set the limit in the "RAM limit for data selection via OData" ("MaxMemoryUsageToGetDataViaEntityCollection" code) system setting. Learn more: [Limit RAM size dedicated to handling OData requests](https://academy.creatio.com/documents?id=15135).

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-13 "Direct link to Advanced customization")

**Connection settings for external file storage**. You can now use `SetFileStorageConnectionString` WorkspaceConsole command to change connection settings for external file storage, for example, S3 or Azure Blob. For example, this is useful to arrange automation, such as rotating credentials regularly. Learn more: [WorkspaceConsole utility parameters](https://academy.creatio.com/documents?id=15211).

**Customization improvements for sidebars implemented using remote module**.

- Developers can now open or close sidebar via requests.
- Developers can now add notification marks (red dots) to custom sidebars.
- Creatio now hides the notification mark if the sidebar is open. Developers can customize this behavior using code.

Learn more: [Manage sidebar events implemented using remote module](https://academy.creatio.com/documents?id=15102&anchor=title-15102-4).

**Custom handlers with business rules**. It is now possible to control whether to execute the business rules for the new records added to collections via custom handlers. Learn more: [Auto-apply business rules to records that are added by a custom request handler](https://academy.creatio.com/documents?id=15136).

## Administration​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-14 "Direct link to Administration​")

**Deprecation of old Microsoft SQL versions**. Microsoft SQL Server version 2016 reached its end of life, therefore Creatio 8.2 and later will only support Microsoft SQL version 2022 and later.

**License distribution improvements**.

- It is now possible to provide different licenses to different user groups automatically. System administrators can issue licenses for user roles using **Licenses** tab in **Roles** section. After that, every time users are included or excluded from the role, Creatio automatically provides users with licenses assigned to their roles. To use this functionality, turn on "Turn on role-based license distribution after manual changes to user roles" ("RedistributeLicensesOnRoleChanges" code) system setting.
- When system administrator changes the list of licenses that are issued for the role, Creatio updates the list of licenses for users included in the role automatically. To use this functionality, turn on "Turn on role-based license distribution after manual changes to user roles" ("RedistributeLicensesOnRoleChanges" code) system setting.
- Creatio now distributes licenses based on user role automatically during the invite to the external organization. If some of the roles the user receives during the invitation contain licenses, Creatio distributes them to the user automatically.
- When an external user registers on their own, Creatio distributes licenses bound to the "All external user" role to them automatically.

**Workplace setup**. You can now go to the workplace setup page from the workplace list in the navigation menu. The button is available for users that have permission to the "Access to workplace setup" ("CanManageWorkplaceSettings" code) system operation.

**Performance and stability of Excel import**. Performance and stability of Excel import were improved. As part of the optimization effort, a limitation was introduced. You can now use only 10 columns of the same type for identifying duplicates in Creatio. For example, you can search for duplicates by 10 lookup columns, 10 text columns, and 10 boolean columns, but not by 11 text columns. This change affects only fields required for duplicate search and introduces no new limitations to the overall number of columns, records, etc. that can be imported.

**Calendar performance**. Calendars that have a significant number of meetings now have better performance.

## Beta testing of new features​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes\#title-2782-17 "Direct link to Beta testing of new features​")

Important

The features below are available for beta testing in Creatio version 8.1.4 Quantum. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Google Analytics**. It is now possible to receive Google web analytics data for Creatio contacts after a form submission on a landing page integrated via webhooks. To access this functionality, contact support.

**Synchronization of Office 365 calendar**. It is now possible to import meetings that have "Creatio sync" category from Office 365 calendar to Creatio. To access this functionality, contact [Creatio support](mailto:support@creatio.com).

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-1)
  - [Order and Contract Management](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-2)
  - [Lead and Opportunity Management​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-3)
  - [Productivity​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-4)
  - [Knowledge Management​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-5)
- [Creatio Marketplace​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-6)
- [Creatio Marketing​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-7)
- [End user experience​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-8)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-9)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-10)
  - [Business processes​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-11)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-12)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-13)
- [Administration​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-14)
- [Beta testing of new features​](https://academy.creatio.com/docs/8.x/resources/release-notes/814-quantum-release-notes#title-2782-17)