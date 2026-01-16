<!-- Source: page_46 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 10/06/2025

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code development, and modern CRM. Today we are advancing new forms of innovation with Creatio version 8.3.1 "Twin," featuring the **following new capabilities and enhancements**.

A comprehensive overview of technical changes and enhancements can be found in the [8.3.1 Twin changelog](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-3-1-twin-changelog).

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio.ai [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-114 "Direct link to Creatio.ai")

**Select AI model**. You can now fine-tune performance of AI Agents and AI Skills by selecting which large language model (LLM) they use to process requests. The Creatio-hosted models have the following advantages:

- **GPT-5**: best for complex, high-stakes tasks that need deep reasoning and strict instruction following. Use for multi-step planning, policy or legal summarization, advanced data extraction that uses constraints, long-context analysis.
- **GPT-4.1**: strong general-purpose choice when you want a balance of quality, speed, and cost. Use for most skills and agents, content drafting, and accurate structured outputs.
- **GPT-4o**: optimized for multimodal and real-time interactions. Use when you need fast, natural, and responsive conversations.
- **GPT-4.1 mini**: fastest and most cost-effective. Use for intent detection, routing, short summaries, simple transformations, classification, template filling, and high-throughput batch tasks.

**AI data model**. You can now ask natural-language questions about the Creatio data structure. AI Agents / AI Skills use that knowledge reliably to explain the model and automate tasks. For example, you can ask where the customer’s risk score is stored or how the order is related to the product.

**AI dashboard creation**. It is now possible to describe your analytical needs in natural language to generate fully configured widgets that contain appropriate data, filters, and visualization. Creatio.ai supports combinations of filters and aggregation functions, for example, count, sum, average, min, and max. You can use related table data in prompts using forward and backward references for filters and aggregated functions. All widget types except gauge, pipeline, and list widgets are supported.

Create a dashboard using AI

![Create a dashboard using AI](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3_1/scr_dashboard_ai.png)

**Access rights for AI Agents**. It is now possible to control which users can view or invoke particular AI Agents, ensuring secure and targeted use. Access rights for agents work the same way as for skills. If a user has access to an agent, they automatically receive access to all skills assigned to that agent if they also have rights to those skills. If a user does not have access, the agent and its skills will not be visible or available in chats. Out of the box, all employees have access to existing agents. Learn more: [Creatio.ai skill and agent permissions](https://academy.creatio.com/documents?id=2625)

**Creatio.ai on-site**. You can deploy Creatio.ai on-site by running your own instance of the AI microservice and integrating it with LLMs deployed in various cloud providers or hosted locally in your own infrastructure.

**Work with existing files**. You can now work with existing Creatio files, for example, documents related to records or mentioned in prompts, directly in Creatio.ai chat. This enhances document handling workflow and file-based AI interactions.

Work with record attachments

![Work with record attachments](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3_1/scr_work_with_attachments.png)

**File handling in business processes**. You can now automate document management and file-based operations by using files as part of business process logic in Creatio.ai. Simply pass files to API Skills directly within business process elements.

**Chat UX enhancements**.

- Find conversations quickly by searching in the Creatio.ai chat panel. The search works by chat name and the first 500 characters of chat messages and highlights the matched text. When you open a searched chat, the conversation scrolls directly to the relevant message, making navigation faster and easier.
- View the time and date of the previous conversations with Creatio.ai. If the last message in chat was sent today, only the time is shown. For earlier chats, the full date is displayed.
- Rename chats to organize your workflow better.
- Creatio.ai now makes navigation smoother by remembering where you left off in each conversation. When switching between chats, reopening the panel, or refreshing the page, the scroll position is preserved, allowing you to continue from where you left off seamlessly.

**Creatio.ai in Microsoft Teams**. You can now increase efficiency of your Microsoft Teams workflow using Creatio.ai directly in Microsoft Teams via a Creatio.ai add-in. For example, use it to identify contacts from meeting participants, prepare for meetings with CRM insights, or check open support cases before customer calls. You can continue the AI conversation in desktop Creatio.

When you open the app from an event, Creatio.ai opens the conversation related to that meeting. If no previous conversation exists, a new conversation is created. If multiple conversations exist, the app restores the last conversation with which you interacted.

**UX of Creatio.ai add-in for Outlook**. The add-in now keeps you signed in longer. If your Microsoft session is still valid, you will not see the login screen again when reopening the add-in. It also automatically opens the last website you used. Only if your session expires will you need to log in and select a website again. The same behavior applies to Microsoft Teams add-in.

## Creatio products and apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-1 "Direct link to Creatio products and apps")

**Classic UI Shell deprecation**. Starting with Creatio version 8.3.2, support for Classic UI shell will be discontinued officially. Classic UI sections will continue to work as before. In other words, all existing functionalities will remain unaffected, and the changes apply exclusively to the panels, navigation, communication areas, and related elements. All environments still using the Classic UI shell will be automatically switched to the Freedom UI shell during the upgrade to version 8.3.2. No additional configuration will be required on your side. The switch will take place seamlessly during the upgrade.

Creatio Freedom UI

![Creatio Freedom UI](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3_1/scr_freedom_ui.png)

Freedom UI is the next-generation interface designed to deliver a more modern user experience, improved performance, and enhanced customization options. It provides a consistent look and feel across all devices and ensures better support for Creatio’s future product innovations.

You do not have to wait for the update to start working with the new UI. We strongly recommend and encourage all users to prepare for this change in advance. Switch your interface to Freedom UI, verify that everything works as expected, and reach out to our support team if you encounter any issues. Administrators can enable the Freedom UI in advance for selected users, user roles, or even the entire organization. This lets you adopt the new UI gradually, run internal testing, and collect feedback from your teams before the automatic switch with version 8.3.2.

For your convenience, we recommend exploring the following articles:

- [Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445): learn more about its capabilities, benefits, and differences from Classic UI.
- [Turn on Freedom UI](https://academy.creatio.com/documents?id=2446): step-by-step instructions on how to configure the UI settings for users, roles, and organizations.

### Email marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-119 "Direct link to Email marketing")

**Dynamic content**. It is now possible to personalize emails using conditions based on contact-related data, such as location, purchase history, gender, age, and website behavior. This improves email relevance for different audiences, increasing engagement and loyalty while reducing costs associated with untargeted email campaigns.

**Google Analytics in email campaigns**. You can now track and analyze user interactions seamlessly from your bulk email campaigns in Creatio using Google Analytics. First, connect your Google Analytics account to Creatio. Then either connect analytics to your Creatio landing page or add the tracking script to your webhook-integrated landing page. Once set up, Creatio automatically synchronizes web session and action data linked to contacts who follow the bulk email link leading to the connected page and engage with the latter.

### Lead Generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-122 "Direct link to Lead Generation")

**Google Analytics on landing pages**. You can now seamlessly monitor and evaluate landing page performance using Google Analytics insights on pages created in the Landing Page Designer. Simply connect your Google Analytics account, select a stream name, and have the Google Analytics tracking script embedded into the HTML code of the published landing page automatically. Alternatively, the script is included in the downloaded HTML for external publishing. After a successful connection, Creatio automatically initiates a daily sync of Google Analytics data for the landing page, including active user dynamics by channel, source, device, and events. Additionally, Creatio syncs Google Analytics data daily for contacts created via the landing page form or those who clicked a bulk email link leading to the landing page.

**Google Analytics data**. You can now evaluate and compare landing page performance directly within Creatio. View Google Analytics data on the **Visitors** tab of the **Web Analytics** section and **Analyze performance** tab of each landing page.

Google Analytics data

![Google Analytics data](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3_1/scr_google_analytics.png)

**Restricted fields in Landing Page Designer**. To enhance security and performance, certain fields, for example, **Contacts**, **Accounts**, **Orders**, can no longer be selected in the web forms in Landing Page Designer. Manage available fields using the **Web form field deny list** lookup to ensure data security and prevent errors when working with large datasets.

**Automation for form registration**. Creatio now sets the registration method to "Facebook" for submissions received from Facebook and "Landing page" for submissions received from landing pages.

**Streamlined naming**. For better consistency and clarity, **Submitted forms** section and the corresponding objects are now called **Submissions**.

### Case Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-14 "Direct link to Case Management")

**AI Skill updates**. "Summarize case" AI Skill was updated to enhance both skill selection and output quality. The skill now better recognizes user requests in different languages by expanding the description and keyword mapping. Additionally, the summary output was redesigned to provide more actionable, role-specific information. It now highlights the root cause, current ownership, blockers, and next steps, ensuring better alignment with the needs of support agents and stakeholders.

### Knowledge Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-200 "Direct link to Knowledge Management")

**Playbook article filtering**. If an object has multiple dynamic cases, Creatio now recommends only the playbook articles relevant to the current case and stage.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-18 "Direct link to End user experience")

### UX enhancements [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-8 "Direct link to UX enhancements")

**Warning for file uploads**. Creatio Classic UI now warns you if you try to close the window or tab while file upload is still in progress. This prevents issues with corrupted or not fully transferred files.

**Merge records**. Section lists, list widgets, and galleries now have "Merge" as a bulk action. You can also use the new button action to merge records. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-10).

**View encrypted field values**. You can now view the values of encrypted fields to which you have sufficient permissions even if they are read-only. The element setup also has special features. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-10).

**Page loading time**.

- The loading of live Creatio Freedom UI pages opened in background browser tabs was enhanced to reduce delays caused by browsers’ inherent tab-throttling mechanisms. This change aims to improve speed even when the page is opened in a new background tab. Actual performance gains might vary depending on the browser’s background loading behavior.
- Freedom UI pages that have complex structure now load faster.

### WCAG compliance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-15 "Direct link to WCAG compliance")

**Accessibility-optimized mode**. You can now activate a mode that simplifies navigation via keyboard and improves screen reader performance for **Feed** and **Message composer** components in the user profile.

**Creatio.ai chat**.

- Screen readers now automatically announce key chat updates, including new incoming messages, typing indicators, message sent confirmations, chat renames, and newly created chats.
- Screen readers now announce interactive elements, for example, chat lists, messages, input fields, and action buttons accurately.

**Feed**.

- The focus indicator for entries when user mentions somebody via "@" was adjusted.
- The keyboard focus indicator for the links in the feed messages now meets the standard focus indicator across Creatio.

**Timer**. Default color of negative values was changed.

**Message composer**. Icon margins for the **Insert template**, **Select attachments**, and **Formatting options** buttons were increased.

**Calendar**. Screen reader now announces when you move the meeting, modify it, or add a new meeting.

**Next steps**. Screen reader now announces when you complete a task.

**Email field**. The email icon in the "Email" type field now has increased contrast ratio.

**Web and email fields**. The keyboard focus indicator for "Web" and "Email" type fields now meets the standard focus indicator across Creatio.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-9 "Direct link to No-code tools")

**Classic UI deprecation**. Starting from Creatio 8.3.1 Section and Detail Wizards for Classic UI are no longer displayed in the System Designer. We recommend using the modern Freedom UI tools that provide a more flexible and future-ready experience.

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-150 "Direct link to Application Hub")

**App version check**. Creatio now checks if all dependent applications have compatible versions and blocks the installation if they do not meet the criteria.

**Required version for dependencies**. You can now enforce version-level compatibility when declaring dependencies between apps. To do this, define specific versions or compatible version ranges for app dependencies in the app properties window, under the **Dependencies** tab.

**Application Hub URLs**. You can now use shorter `/hub` and `/apps` links to open the Application Hub directly.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-10 "Direct link to Freedom UI Designer")

**Angular updates**. We continue migrating from deprecated Angular Material elements to supported elements. In this release, multiple elements were updated. Review the Technical changelog for the full list of changes: [8.3.1 Twin changelog](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-3-1-twin-changelog).

**Improved saving logic**. Data saving behavior now ensures data consistency between the records of different objects used as data sources of a single page. This is done by checking for backend-level validation errors while saving pages that have multiple dependent data sources. If errors are found, Freedom UI Designer prevents saving data to all page data sources.

**List widget**. You can now use lists in your analytics with visual consistency using the new **List** widget component. It combines a fully functional list with a customizable colored frame.

List widget

![List widget](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3_1/scr_list_widget.png)

**List enhancements**.

- Create focused list views, for example, top five lists, by setting a maximum number of records displayed in lists and list widgets.
- Specify whether the users can view list headers as well as drag, resize, and sort columns in lists and list widgets.

**Filters for Multiselect lookup**. You can now define item selection constraints directly as part of the **Multiselect lookup** component setup.

**Sorting in the Dropdown field**. It is now possible to specify the column by which to sort values of a "Dropdown" type field as well as sorting direction. This improves data discoverability in long lists, supports multilingual catalogs with proper collation, and reduces manual scanning.

**Default tab in the toggle panel**. You can now have more control over the initial display behavior of the **Toggle panel** component by specifying a default tab.

**Follow feed**. You can now follow or unfollow feed updates on the page using the new **Follow/Unfollow Feed** button action.

**Reload data on save**. If you have a save button whose logic is configured to let the user remain on a page upon saving, it is now possible to have the button reload page data. For example, this is useful to reflect server-side changes incompatible with new Freedom UI approaches.

**Encrypted string enhancements**.

- Use the "Encrypted string" type field in forward references. This ensures the field functions correctly across relational structures.
- Make "Encrypted string" type field read only, similarly to other fields.

The component UX also has special features. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-8).

**Rearrange tabs**. You can now rearrange toggle and tab containers without deleting and re-adding items.

**Merge records**. You can now enable users to merge records easily using the new "Merge data" button action. The action works with section lists, list widgets, and galleries. Record merge is available to end users in other components as well. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-8).

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-3 "Direct link to Business rules")

**Visibility rules for tabs of the Toggle panel component**. You can now set up more dynamic and personalized UX using visibility business rules for individual tab layout elements in the **Toggle panel** component.

**Comparison operators**. You can now use comparison operators for numeric and date/time attributes in business rules conditions.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2792-130 "Direct link to Integrations")

**Encryption of Creatio Messaging Service**. CMS now uses an improved encryption algorithm. All customers who use Avaya and Cisco Enterprise (CTIOS) connectors must update CMS to the latest version when their Creatio instance is updated to 8.3.1. Contact [Creatio support](mailto:support@creatio.com) to get the latest version of the CMS installer.

**Calendar synchronization improvements**. You can now run Office365/Exchange calendar synchronization in a separate Quartz thread to improve performance and stability for high-loaded websites.

**Track sessions of external applications**. You can now improve auditability, strengthen security monitoring, and simplify troubleshooting of integration activity by tracking sessions initiated by external applications in Creatio. You can distinguish between standard user sessions and those created by OAuth integrations on behalf of a user, ensuring better visibility and control. A new monitoring list on the page of of Authorization Code grant type OAuth integrations displays session details, for example, user, client name, IP address, and timeframes, while the user page in the **Users** section now includes an **External application** column.

**Role-based permissions for OAuth integrations**. You can now improve efficiency, ensure consistency, and lower the risk of access errors in integration management by assigning access not by user but to entire roles while setting up authorization code grant type of OAuth authorization.

**Azure Blob storage authorization**. To enhance security, improve auditability, and align with Microsoft’s recommended best practices for cloud storage access, it is now possible to authorize Azure Blob storage via Client ID and Secret. Instead of using account keys, Creatio can now authenticate with service principal credentials ( **Client ID**, **Client secret**, and **Tenant ID**), enabling precise and role-based permission management.

**Stricter authentication**. You can now enhance security by disabling login with username and password for company employees. This can be configured via the "Manage login with username and password for company employees" (`DisableInternalUserPasswordAuth` code) system setting. Out of the box, disabled. If this option is enabled, employees must use an alternative authentication method, for example, SSO. System administrators can still log in with username and password, including two-factor authentication.

## Creatio Mobile [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-16 "Direct link to Creatio Mobile")

**Sliders on mobile**. You can now use **Slider** component in Creatio Mobile. Learn more: [Slider component](http://academy.creatio.com/documents?id=15320).

**Search Creatio.ai**. It is now possible to search in Creatio.ai chats.

**Business rule updates**. You can now use Current User Roles macros in business rules in Creatio Mobile.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-13 "Direct link to Advanced customization")

**Installation checks**. `InstallApp` operations in the WorkspaceConsole utility now also check for compatibility with Creatio version, missing dependencies, and minimum required versions of dependent apps. `InstallZipPackage` operations in the WorkspaceConsole utility now also check for missing dependencies. Learn more: [WorkspaceConsole utility parameters](https://academy.creatio.com/documents?id=15211).

**Current package protection**. To prevent system errors, it is no longer possible to deactivate or delete a package or its dependencies if the package is specified in the "Current package" (`CurrentPackageId` code) system setting.

**Environment schemas**. It is now possible to work with environment schemas in the **Configuration** section using new **Environment schemas** group. Environment schemas are schemas not associated with any package and stored directly in the database. They support only some of the operations available for configuration schemas, with the following limitations:

- They cannot be created manually in the **Configuration** section.
- They cannot be imported or exported until you convert the environment schema to a configuration schema.

Learn more: [Schemas overview](https://academy.creatio.com/documents?id=15347), [Operations with schemas in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15339).

## Administration​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-14 "Direct link to Administration​")

**Translation enhancements**.

- Speed up the application of translations by skipping validations. This is especially useful when applying only a small number of updates where manual review is sufficient and full validation would be unnecessarily time-consuming.
- Update translations quicker and easier by running the "Update translations" business process directly from the **Translation** section. Creatio runs the process in the background, you will receive a notification when it is completed. In previous releases, this operation was launched automatically when you opened the section.
- Creatio now helps you keep the **Translation** section up-to-date by deleting outdated translation records automatically during translation update process.
- The "Apply Translations" action now runs as a background business process instead of a direct blocking operation. Creatio executes the process asynchronously, leaving the UI responsive and allowing you to track progress in the **Process log** section. The logic and results remain the same, but the update enhances user experience, transparency, and control, especially when working with large translation datasets.

**Localization-aware indexing in global search**. You can now manage localization for global search quicker and easier without effect on Creatio performance or required user interaction. To do this, specify the culture in the "Global Search localization for indexing" (`GlobalSearchIndexationLocalization` code) system setting. If you leave the setting empty, Creatio uses the default language of the Supervisor system user.

**Turn off JIT when using OpenID SSO**. You can now have more control over user data updates and prevent unintended overwrites by turning off JIT provisioning when using OpenID-based SSO. The same checkbox previously used for SAML SSO in the Single Sign-On settings section now also controls whether user data is synchronized during login via OpenID SSO. When the checkbox is cleared, Creatio no longer updates user data from the Identity Provider.

**Log export to Excel**. You can now track export to Excel operations in the audit log. Enable logging in the "Log export to Excel events" (`UseExportToExcelLog` code) system setting.

## Beta testing of new features​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes\#title-2782-17 "Direct link to Beta testing of new features​")

Important

The features below are available for beta testing in Creatio version 8.3.1 Twin. If you have any feedback, contact us at: `beta@creatio.com`. All feedback is appreciated.

**Validation for installed files**. Creatio now can streamline the app or package installation by validating apps or packages for missing dependencies and compatibility issues before installation. If missing dependencies are detected and they exist in the Creatio Marketplace, the Application installer microservice automatically enriches the initial file by adding the required apps. If compatibility issues or conflicting dependencies are found, the installation is blocked. To take advantage of these capabilities, add and enable the `AppsFeatures.UseAutoInstallDependencies` additional feature. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634).

**Workplace type setup**. It is now possible to specify whether a workplace is used in web Creatio or Creatio Mobile. Sections also have the option to be set as web/mobile, so only sections of compatible type can be added to the workplace. To take advantage of the functionality, add and enable the `UseMobilePageDesigner` additional feature. By default, Creatio adds all mobile pages to the automatically created "My applications" workspace whose type is "Mobile." To restrict creating separate workspaces for Creatio Mobile, add and enable the `DisableSetupMobileWorkplaces` additional feature. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634).

**Translation enhancement**. You can now tailor the localized values across the platform and deliver a more consistent UX by applying custom translations to core platform UI elements in Creatio. This applies to system components that were previously not translatable, for example, profile menu labels.

- [Creatio.ai](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-114)
- [Creatio products and apps](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-1)
  - [Email marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-119)
  - [Lead Generation](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-122)
  - [Case Management](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-14)
  - [Knowledge Management](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-200)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-18)
  - [UX enhancements](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-8)
  - [WCAG compliance](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-15)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-9)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-150)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-10)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-3)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2792-130)
- [Creatio Mobile](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-16)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-13)
- [Administration​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-14)
- [Beta testing of new features​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-1-twin-release-notes#title-2782-17)