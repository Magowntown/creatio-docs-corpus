<!-- Source: page_136 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 06/19/2025

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code development, and modern CRM. Today we are advancing new forms of innovation with Creatio version 8.3 "Twin," featuring the **following new capabilities and enhancements**.

A comprehensive overview of technical changes and enhancements can be found in the [8.3 Twin changelog](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-3-twin-changelog).

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio.ai [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-114 "Direct link to Creatio.ai")

**AI Agents**. Creatio.ai now includes AI Agents. These are independent entities that operate within Creatio.ai and help automate complex user tasks. The task performed by an agent depends on its complexity, for example, creating email campaigns, and its area of competence, for example, service or sales support.

Use AI Agent

![Use AI Agent](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_ai_agent.png)

**New AI Agents**.

- Work with all sales skills within a single **Sales AI assistant**.
- Streamline meeting planning and improve communication using the **Productivity agent** that identifies available time slots across participant schedules automatically.
- Summarize cases quickly and receive resolution suggestions using the new **Case resolution agent** in the **Case Management** and **Knowledge Management** apps.
- Summarize information and generate case article using the new **Knowledge agent** in the **Knowledge Management** app, integrated with **Case Management** app.
- Draft, refine, and finalize branded, mobile-ready marketing emails directly in Creatio easier using the **Email generation agent**. It understands your intent, applies brand guidelines, and produces responsive content previews, making professional email creation faster and more efficient.
- Handle non-specific tasks using **Creatio.ai Agent**.

An agent can launch individual skills to complete complex tasks or use actions to validate, check, or edit system data.

You can reference specific agents in the chat when composing messages.

All interaction in the Creatio.ai chat happens directly with agents that make decisions and complete tasks on behalf of the user.

An agent works only with its own skills and actions. However, Creatio can automatically switch to a different agent in the following cases:

- The goal, topic, or user query changes significantly.
- The request falls outside the current agent's scope.
- The current agent cannot technically complete the task.

As a result, all chat interactions in Creatio.ai happen through the most relevant agent that adapts to the context of the user’s task.

If no existing agent can handle the request, Creatio switches to a special Creatio.ai agent designed to answer general questions and help users navigate the system.

Each AI Agent in Creatio consists of the following components:

- **Agent title and description**. Define its purpose and functionality.

- **Status**. Specify whether the agent is active.

- **Prompt name and description**. Include multiple key elements:
  - **Role**. Describes the agent’s functionality, for example, service agent or sales assistant.
  - **Agent instructions**. Define the agent actions, typical tasks it handles, and general usage scenario.
  - **Limitations and restrictions**. Specify what the agent must not do and any limitations in actions or data access.
- **List of available AI Skills**. Each skill solves a specific business task, such as generating a document or analyzing records. If you do not add a skill to any agent, Creatio cannot use it. To activate a skill, add it to the relevant agents.

- **List of available actions**. Low-level operations the agent can perform without calling a skill, such as changing a record, validating data, or reading a value from a lookup.

- **List of available files**.


**AI Agent info**. You can now configure and define the main information for an AI Agent, including name, status, and description, directly in the UI. The procedure is based on a standardized structure similar to AI Skills.

**File support**. Creatio.ai can now work with files, allowing both users and no-code creators to upload and use documents within AI-powered experiences easily. This update enables both design-time and runtime file interactions, supporting a broad range of document-driven use cases.

Work with files in Creatio.ai

![Work with files in Creatio.ai](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_work_with_files.png)

Users can upload text-based files to the Creatio.ai chat panel. These files are instantly accessible to AI features, enabling richer, more flexible interactions from the outset of a session.

For no-code creators, the update introduces the ability to attach documents to AI Skills and agents during setup, allowing more dynamic execution and improved contextual awareness.

**New AI Skill**. It is now possible to extract and update opportunity data automatically based on activity transcriptions, for example, recorded meetings, using the new **Enrich opportunity** AI Skill.

**Data enrichment parameters**. **Enrich Account Data** AI Skill now supports a broader set of parameters, including industry, revenue, business entity type, number of employees, contacts, and more.

**UX improvements for the Creatio.ai chat panel**.

- It is now possible to view and manage multiple ongoing conversations directly in the Creatio.ai chat panel.
- It is now possible to view Creatio.ai conversations sorted by last message date, the most recent chats are on top.
- In-line images are now adapted to fit the size of the message container, ensuring better visual alignment. Click an image to view it in full size.
- It is now possible to initiate new conversations directly from the chat panel using the **New chat** button.
- The chat panel is now resizable, and the chat UI adapts to its width dynamically.
- It is now possible to show or hide the list of chat conversations when the Creatio.ai chat panel is expanded.
- The incoming messages now clearly display the sender name. When an agent responds, their current name appears as the sender label. When no agent is assigned, the label shows "Creatio.ai."
- Chat debug messages now show only file metadata, not file content.
- If an AI Skill or agent is installed without predefined access permissions, Creatio now automatically assigns default permissions if they are configured in the platform.

**Outlook add-in**. You can now use Creatio.ai in the Outlook email client, both web and desktop versions. The add-in supports the following options:

- **Understand full email context**. The add-in can analyze the content of the current email.

- **Use AI skills**. The add-in can use the following skills out of the box:
  - **Identify skills**. Provides useful information about contacts found in the email thread.
  - **Summarize email**. Provides a short summary of the email thread.
  - **Generate email reply**. Assists in preparing a reply based on the analysis of the current email thread.

You can use any other skill available in Creatio in the add-in as well. Learn more: [Creatio.ai add-in for Outlook](http://academy.creatio.com/documents?id=2572).

**Apollo.io connector**. You can now enrich account profiles, for example, industry, revenue, business type, number of employees, country/region, address, communication options, and associated contacts with job titles and communication details, using the [Apollo.io connector for Creatio](https://marketplace.creatio.com/node/31135) Marketplace app. The app is required for the “Enrich account data” AI Skill to work.

## Creatio products and apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-1 "Direct link to Creatio products and apps")

**Preconfigured dashboards**. View KPIs in real time in the **Accounts**, **Calls**, **Cards**, **Cases**, **Chats**, **Contacts**, **Contracts**, **Documents**, **Financial accounts**, **Invoices**, **Leads**, **Opportunities**, **Orders**, and **Tasks** sections using new preconfigured dashboards. If you have customized pages, you can update them to include dashboards as well: [Update list page template to include dashboards](https://academy.creatio.com/documents?id=2595).

Account dashboard

![Account dashboard](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_dashboard.png)

### Email Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-119 "Direct link to Email Marketing")

**Audience selection using folders**. You can now add or exclude bulk email audiences simply by selecting folders without using complex filters.

**Track active contact licenses**. You can now track the usage of active contact licenses directly on the audience page.

Contact licenses

![Contact licenses](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_contact_licenses.png)

### Lead Generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-122 "Direct link to Lead Generation")

**Copy landing pages**. It is now possible to duplicate an existing landing page directly from the **Landing pages** section. The duplicated page retains all elements of the original, including forms, images, text blocks, buttons, ensuring full consistency.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-18 "Direct link to End user experience")

### UX enhancements [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-8 "Direct link to UX enhancements")

**Dashboards**.

This functionality is now available to everyone. Use dashboards to group analytics widgets easier as well as connect them to data source and apply filter by page data.

Dashboard

![Dashboard](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_dashboards.png)

Dashboards have the following UX improvements compared to the beta version:

- You can now add and manage dashboards yourself as well as set up access permissions for dashboards.
- Dashboard list is filtered depending on the access permissions of the current user. Creatio checks license limitations and administrative operation permissions to determine if you can work with a dashboard.
- Dashboard widgets now have preset sizes in rows and columns when you drag them to the canvas. This change applies only to dashboards.
- List dashboards now sort records by name from A to Z.
- Creatio now refreshes a dashboard after you update it in the Freedom UI Designer.

**Browser notifications**. Freedom UI now supports notifications for feed, noteworthy events, business processes, approvals, reminders, and system notifications.

**Variable phone numbers**. You can now enter variable-length phone numbers, for example, Indonesian or Italian numbers. The minimum required digits are displayed out of the box, and you can enter more digits up to the maximum allowed, ensuring both flexibility and format consistency.

**Timeline UX improvements**

- View newly added feed messages and attached files in real time without needing to refresh the page. The functionality requires selecting the **Enable live data update** checkbox for the objects used to store feed messages or files.
- Edit your feed messages directly from the timeline. After you save the message, Creatio updates it immediately in the timeline.
- Multiline plain text fields in the timeline are now easier to read as they preserve and show line breaks.
- Timeline now supports color-coded lookup fields in the timeline so that they are displayed consistently with pages or lists.

Learn more: [Check timelines](https://academy.creatio.com/documents?id=1873).

**Improved page performance**.

- Pages that have a large number of widgets now perform better.
- Live Freedom UI pages opened in background browser tabs now load faster. The update reduces delays caused by inherent tab-throttling mechanisms of web browsers. Actual performance gains might vary depending on the browser’s background loading behavior.

**List sorting performance**. Lists now sort records faster. The more records the list has, the more significant the update is.

**Dropdown field performance**. Interaction with the field is now smoother when the field is handling errors.

### WCAG compliance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-15 "Direct link to WCAG compliance")

**Summary item menu**. You can now press Enter or Space to open the menu of the summary item.

**Widget color palette**. Color palette of widgets was improved for people that have color perception differences.

**Edit button**. Button that edits cells in the editable list is now compliant with WCAG minimum target zone criterion.

**Icons inside inputs**. Icons inside inputs, including tooltip icon, are now compliant with minimum target size criterion.

**Screen reader in editable list**. Screen readers now announce the following:

- record deletion using row action
- record deletion using bulk action
- saving changes
- discarding changes

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-9 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-150 "Direct link to Application Hub")

**Dependency validation**. Creatio now validates dependencies after you upload the file to detect and report missing dependencies before installing an app.

**Inherit elements from packages**. You can now inherit elements directly from packages while configuring dependencies in the app properties.

Package dependency

![Package dependency](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/scr_package_dependency.png)

**Enhanced dependency management**. You can now manage both application and package level dependencies on the **Dependencies** tab of the app properties.

**Icons for item types**. The application installation and update windows now include icons that represent item types, i. e., "package" and "app."

**Maximum compatible version**. You can now specify both minimum and maximum compatible platform versions for apps.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-10 "Direct link to Freedom UI Designer")

**List page updates**. List page underwent a major overhaul in this version. Please be especially vigilant when updating to thie version and review your customizations thoroughly as this update might impact existing implementations. You can update custom Freedom UI pages as well if needed: [Update list page template to include dashboards](https://academy.creatio.com/documents?id=2595).

**Multiple page data sources**. This feature is now available for all users.

**Many-to-one relationships**. You can now add data sources based on objects that are referenced in the lookup columns of the primary data source and use these columns in relations.

**Independent data source**. You can now decouple secondary data sources from the main record. As a result, Creatio loads data based solely on the filters and sorting criteria of the secondary data source.

**Refresh data from multiple data sources**. You can now let users refresh data from multiple data sources using a single "Refresh data" button action.

**Custom quick filters in the timeline**. You can now add the **Quick filter** component to the **Timeline** component to set up custom quick filters. Existing preconfigured filters remain embedded into the timeline. Learn more: [Set up Timeline component](https://academy.creatio.com/documents?id=2597).

Attaching a filter to the timeline

![Attaching a filter to the timeline](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_3/gif_attaching_filter_to_timeline.gif)

**Widget connection**. When you drag a widget to the canvas, Creatio sets widget connections automatically.

**Transfer dashboards**. Creatio now warns users that have permission to the "Can manage configuration elements" (`CanManageSolution` code) system operation when they are editing dashboards in the environment schema. This ensures that changes are implemented without package binding and are stored to the package as an environment schema, not a configuration schema, and reduces confusion for system administrators expecting package-level edits. Learn more: [Dashboards basics](http://academy.creatio.com/documents?id=15196).

**Limited form pages**. If you create more than one Freedom UI section for an object, new sections do not create separate form pages and use the form page from the original section.

**Encrypted field UX**. You can now manage encrypted column and field behavior in both the Object Designer and Freedom UI Designer. Key capabilities include the following:

- Assign operation-level permissions to encrypted fields via a dedicated selector in both Designers. This setting governs who can access or unmask encrypted data.
- Specify whether the "Encrypted string" input type is available using the `EnableSecureTextMasking` feature. When the feature is disabled, the "Encrypted string" input type is hidden, allowing for flexible configuration based on security requirements. The feature is enabled out of the box. Learn more: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631).
- Choose from predefined masking formats in both Designers, including SSN, SIN, Bank card, Hide all characters, and Show only last 4 characters. These options control how encrypted values are represented visually while maintaining data security.

For new encrypted fields, the masking option is enabled by default in the Object Designer, ensuring sensitive data is concealed out-of-the-box. To activate the masking option for existing fields, select the **Mask displayed value** checkbox on the column in the Object Designer.

**Resizable sidebars**. You can now make standalone panel sidebars whose width can be changed by the user.

**Chart series name**. Creatio now renames the chart series when you change the object in the chart settings.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2792-130 "Direct link to Integrations")

**OAuth authorization code**. Creatio now supports the OAuth authorization code grant type. This enables external applications to access Creatio data and APIs on behalf of a specific user who gave consent. To grant external applications access to your account, initiate the authorization flow in the external application, log in to Creatio, and give consent. Manage the integration in the **OAuth integrated applications** section and on the **External applications** tab of the user profile page. Learn more: [Set up authorization code grant](https://academy.creatio.com/documents?id=2576), [Authorize external requests using authorization code grant](https://academy.creatio.com/documents?id=15188), [Manage integrated apps on the user profile page](https://academy.creatio.com/documents?id=2575).

**Parse custom SOAP headers**. It is now possible to parse imported WSDL files that contain custom SOAP headers in the request body of SOAP web services.

**Multi-level SOAP header parameters**. You can now add multi-level SOAP header parameters to SOAP requests using the **Web services** section.

**Webhook warning**. Creatio now alerts you if it has webhooks whose object codes are not listed in the **Webhook entities** lookup. Previously, such webhooks were blocked silently. Out of the box, Creatio supports webhooks for "Contact," "Lead," "Order," and "FormSubmit" objects.

## Creatio Mobile [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-16 "Direct link to Creatio Mobile")

**Context in the Combobox component**. You can now display an additional column that includes contextual information related to the selected records in the **Combobox** component. For example, show relation of a contact to an account. Learn more: [Combobox](https://academy.creatio.com/documents?id=15089&anchor=secondaryDisplayValue).

**Improved sidebar UX**. Creatio Mobile now adjusts sidebar width dynamically based on screen context in the mobile view.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-13 "Direct link to Advanced customization")

**Monitor front-end performance**. You can now collect front-end performance metrics submitted via a new web service endpoint: `/ServiceModel/ClientMetricsService.svc/PublishPerformanceMetrics`. The endpoint is secured by the "Can publish performance metrics" (`CanPublishPerformanceMetrics` code) system operation. To take advantage of this functionality, add and turn on the `EnableClientPerformanceMonitoring` feature. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634).

**jQuery deprecation**. We removed the obsolete version 3.5.1 of the library. From now on, the only available version of jQuery is 3.7.1.

## Administration​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-14 "Direct link to Administration​")

**Skip translation update**. It is now possible to skip automatic translation updates on loading the **Translation** section. To take advantage of this functionality, add and turn on the `SkipActualizeTranslationOnPageLoad` feature. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634).

Regardless of the feature state, manually edited values, i.e., those marked using "isChanged=true," are preserved and not overwritten during any update process, including those started manually.

**Unique translations**. It is no longer possible to create translation records whose keys already exist. This ensures uniqueness in the **Translation** section. Also, Creatio identifies and removes existing duplicates during translation update to correct historical inconsistencies.

## Beta testing of new features​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes\#title-2782-17 "Direct link to Beta testing of new features​")

Important

The features below are available for beta testing in Creatio version 8.3 Twin. If you have any feedback, contact us at: `beta@creatio.com`. All feedback is appreciated.

**Progress bar stage**. Progress bar now displays the previously selected stage correctly if you select from multiple grouped stages and move the case to the next stage. Creatio can store and display the previous stage values beyond 60 days. To activate the functionality, add and enable the `ProcessFeatures.UseDcmExpirationPeriod` and `EnableHistoryDCM` features and set a value in the "DCM log data expiration period (days)" (`DCMLogExpirationPeriod` code) system setting. If the system setting value is "-1," the information is stored indefinitely. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634), [Manage system settings](https://academy.creatio.com/documents?id=269).

**New FileAPI .NET class library**. FileAPI now has an in-house implementation. The updated library maintains full compatibility, replicating the same methods and parameters. Out of the box, the new version is enabled for a closed test group. To take advantage of the functionality, add and turn on the `UseExternalFileApiClientLibrary` feature. Learn more: [Implement a custom additional feature](http://academy.creatio.com/documents?id=15634).

- [Creatio.ai](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-114)
- [Creatio products and apps](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-1)
  - [Email Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-119)
  - [Lead Generation](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-122)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-18)
  - [UX enhancements](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-8)
  - [WCAG compliance](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-15)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-9)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-150)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-10)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2792-130)
- [Creatio Mobile](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-16)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-13)
- [Administration​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-14)
- [Beta testing of new features​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-3-twin-release-notes#title-2782-17)