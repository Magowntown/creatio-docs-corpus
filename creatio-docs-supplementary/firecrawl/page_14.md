<!-- Source: page_14 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 03/14/2025

This document details the technical changes and enhancements introduced in Creatio 8.2.2 Energy. It is intended for developers, system administrators, and DevOps engineers responsible for maintaining and extending Creatio customizations.

For a comprehensive overview of the new features, refer to the [8.2.2 Energy release notes](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-2-energy-release-notes).

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Platform [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-platform "Direct link to Platform")

- WCAG support is implemented for the following:
  - Inactive menu items. The screen reader now announces when a menu item is inactive. Creatio displays the full title in a tooltip when a menu item title is cut.
  - Widgets. Additionally, contrast for widget elements highlighted by keyboard focus indicator is added.
  - Breadcrumbs in widgets. Additionally, the focus frame is added.
  - The **Summaries** component. The screen reader now announces when a summary item is added, changed, or deleted.
  - The **Multiselect lookup** component.
  - The **Tag** component.
  - The **Folder management menu** component.
  - The **Quick filter** component of the "Lookup" type.
  - Buttons in the **List** component headers.
  - Selected rows in the **List** component. The screen reader now specifies the number of currently selected records.
  - Fields to display in list selected using the keyboard. Additionally, the focus frame is added.
  - Selected button in the top panel. Additionally, the border is added.
  - User profile button in the top panel. Additionally, contrast is added and the keyboard focus indicator is now more readable.
  - Buttons in the notification panel. Additionally, contrast and border are added.
- WCAG support is implemented for the keyboard focus indicator:
  - Improved compliance for editable list panel and bulk action panel. When you move focus through the page the panel itself is focused first. Press Enter to start interacting with its elements or move focus further through the page. When you are interacting with the panel elements, press Esc to move focus out to the level of panel itself.
  - Widgets.
  - Dialog windows. Keyboard focus indicator is no longer overlapped by dialog window.
  - Selection windows.
  - **Summaries** component.
  - **List** component.
  - The "Checkbox," "Dropdown," "Web link," "Color picker" field types. When you open the "Dropdown" field types using keyboard, focus frame is moved on the first item in the list.
- Multi-language support for the screen reader is implemented.

- Creatio now displays a message when a session will end soon and lets you continue it.

- New wallpaper that makes the page elements more visible is added.

- Support for bulk actions and multi-select in the **Gallery** component is implemented.

- Additional option for sorting section records from column menu is added. As before, you can sort column data in ascending and descending order by clicking the column title. When sorting is enabled, the corresponding menu item changes to **Clear sorting** that cancels the sorting.

- Activity files and links can now be made available in the timeline for external users. To enable the functionality, grant access to the **File and link of activity** (`ActivityFile` code) object for the "All external users" group. Out of the box, disabled.

- Ability to open the app from the app menu within the Application Hub is added.

- Information about application dependencies in the app-descriptor.json file is added.

- Ability to collapse and expand the element library of the Freedom UI Designer is added.

- Ability to search for elements in the element library of the Freedom UI Designer is added.

- Ability to disable the input mask for a "Phone" field type that has no data source using the `"displayAsPhone": false;` value in the `viewConfigDiff` schema section is added.

- Ability to set up synchronization options for Google or Outlook calendar using the new "Set up calendar synchronization account" button action is added.

- Ability to save a new record without closing the page is added. The **Stay on page after record is created** checkbox is added for the button whose **Action** property value in the Freedom UI Designer is "Save data." The functionality is available for full-sized form pages.

- Additional warning messages are added in the **Configuration** section to alert users about actions that could potentially degrade environment performance. Those messages are enabled only for production environments.
More details







Actions where new messages are added or replace existing warnings:



  - Generate for modified schemas ( **Source code** action group)
  - Import ( **Add** drop-down list)
  - Move to another package ( **Multi-actions** drop-down list and **Configuration** element menu)
  - Validate configuration ( **Configuration** action group)
  - **Compile** button (section toolbar)
  - **Compile all** button (section toolbar)
  - Update DB structure where it is needed ( **Actualize items** actions group)

Additional features that manage the status of warning messages:

  - DisableDetailedConfirmForConfActions
  - DisableDetailedConfirmForConfItemActions
  - EnableDetailedConfirmForConfPackageActions
  - DisableDetailedConfirmForConfImportItemActions

- Ability to update translations using background business process is added. To do this, run the "Actualize translations" business process from the Process library.

- Ability to force apply translations even if `isChange = false`. This is useful if you want to make data between runtime and translation sections consistent. To do this, run the "Apply translations" business process, specify the language, and select the **Force apply all translations** checkbox.

- Ability to apply translations only for a specific language is added. This is useful if you want to apply translations faster or do not want to apply some languages because translations are not verified. To do this, run the "Apply translations" business process, select the **Apply translations for specified language** checkbox, and specify the language in the lookup field.

- Ability to manage user permissions for Microsoft Word printable reports is added. To add, edit, and delete records of the `SysModuleReport` and `SysModuleReportTable` objects, users require permissions to the "Access to "Report setup" section" (`CanManageReports` code) system operation.

- Ability to use browser scroll bar in Creatio using the "Use default browser scrollbar styles" (`UseDefaultBrowserScrollbarStyles` code) system setting is added. Out of the box, disabled. The system setting value can be changed by the administrator in the **System settings** section and by the user in the user profile on the **Accessibility settings** tab. The browser scrolling setting in the user profile has a higher priority than in the **System settings** section.

- Ability to log extended package installations and simplify the identification and debugging of schemas that block successful package installation using the `Terrasoft.Core.Packages.PackageStorage` logger is added. The default logging level is "Debug."

- Ability to log the `ReadDataUserTask` schema using the `ReadDataUserTask:Process_Name` logger is added. Requests are logged if `"IsTraceEnabled = true"`.

- Ability to track attempts to read deleted columns and simplify monitoring and debugging using the `BusinessProcess.log` logger is added.

- Support for relative paths for the `-backupPath` and `-sourcePath` parameters of the WorkspaceConsole utility is implemented.

- Automatic recovery of the SQLite database that stores object schema properties in runtime mode is implemented. If SQLite is deleted or corrupted, Creatio will remain fully operable and re-generate the file automatically within several minutes.

- Size limit of email message previews in the message history for Freedom UI is added. To change the maximum size of email message previews in the timeline in Freedom UI, add and then set the value of the new "LargeSizeEmailValueInFreedomUI" (`LargeSizeEmailValueInFreedomUI` code) system setting that improves page performance. Default value of the system setting is "50," in KB.

- Ability to manage access rights to AI Skills for users and user groups in both "Chat" and "API" usage modes is added. Using AI Skill access rights enhances system security and controls LLM usage costs.
More details







  - Added the `GenAIFeatures.UseSkillSchemaOperationRights` additional feature. Out of the box, disabled. The feature is under beta testing.
  - Added default access rights for newly created AI Skills. Default access is automatically applied to the "All employees" group. This enhances security, standardizes Creatio.ai behavior, and simplifies access management.

- Ability to display selected records without the counter in the **Multiselect lookup** component is added. To do this, a new **Wrapping items to the next line** checkbox is added in the Freedom UI Designer. The checkbox is under beta testing. To display the checkbox on the Freedom UI Designer setup area, add and then enable the `EnableWrapInMultiSelect` additional feature.

- The communication option is now deleted when the associated contact or account field is cleared.

- UI of the **Business process** tab in the No-Code Designer is improved.
More details







  - Current version is displayed on the business process tile.
  - Status of the business process is displayed on the business process tile. For non-active business processes, the tile has gray tile and the corresponding label is displayed.
  - When you click the "Version" field, the window that contains all available business process versions opens.

- The object replacement is streamlined. When you configure dependencies between apps using the **Dependencies** tab of the **App properties** window in the No-Code Designer, the **Data models** tab now displays inherited data models. To replace data model objects quickly and easily, open the inherited object, change an object schema and click **Save** or **Save and publish**.

- Modification of inherited sections is streamlined. When you configure dependencies between apps using the **Dependencies** tab of the **App properties** window in the No-Code Designer, the **Navigation and sections** tab now displays inherited sections. To modify the UI of an inherited section from other apps quickly and easily, open the inherited section, change section properties and click **Save**. "Data" type schema will be created in a custom app automatically.

- Modification of inherited business processes is streamlined. The business logic of working with inherited business processes in the No-Code Designer was updated. When you configure dependencies between apps using the **Dependencies** tab of the **App properties** window in the No-Code Designer, the **Business processes** tab now displays inherited business processes. To modify a business process from other apps quickly and easily, open the inherited business process, implement needed changes and click **Save**. The modified business process will be saved as a new version. You can also copy inherited business processes to a custom app.

- **Multiselect lookup** component in Freedom UI Designer is improved.
More details







  - Ability to add new records in both "Dropdown" and "Selection window" lookup views.
  - Ability to select the displayed column of the object chosen in the **Multiselect value storage** property if the object includes multiple "Lookup" type columns. Otherwise, the **Column to display** property is populated automatically.
  - Ability to toggle between "Dropdown" and "Selection window" lookup views. The selection window also enables users to select multiple records in a single session.

- Google SSO and Ping Identity configuration is streamlined by ability to import their metadata files into Creatio.

- The package maintainer is now displayed in the package tooltip in the **Configuration** section.

- The performance of the "Apply translations" business process is improved. Translations are now applied up to 5 times faster using new parallelism implementation and optimization of localization resource processing algorithm. You can manage the number of parallel threads allocated for the "Apply translations" business process execution using a new "Apply translation concurrency limit" (`ApplyTranslationConcurrencyLimit` code) system setting. Default value of the system setting is "3." If the translation application process is interrupted, it will resume during the next run.

- The performance of the "Actualize translations" business process is improved. Translations are now actualized up to 13 times faster using parallelism implementation algorithm. You can manage the number of parallel threads allocated for the "Actualize translations" business process execution using a new "Translation update task concurrency limit" (`TranslationUpdateTaskConcurrencyLimit` code) system setting.

- The performance of the Freedom UI Designer is improved. Freedom UI Designer now opens and saves pages up to 2.5 times faster using a new resource comparison algorithm when calculating the schema hierarchy.

- Permissions for "Creatio ALM integration" technical user are enhanced. This is done by adding a right to the new "Can install applications" (`CanInstallApplication` code) system operation that enables users to install apps without access rights to the "Can manage configuration elements" (`CanManageSolution` code) system operation.

- Database performance for environments that have 2FA enabled is optimized. To do this, the `UseStaticCacheInLoader2FA` additional feature that manages caching of both the "The number of attempts to verify the second factor" (`SecondFactorAttemptCount` code) and "User locking time" (`UserLockoutDuration` code) system settings in the loader is added. Out of the box, disabled. If enabled, IIS restart is required to apply new system setting values.

- Navigation panel loading is optimized. To do this, a new `getOpenSchemaNavigationUrl()` method that generates a link by taking the schema code as an input parameter is added.

- The **Call Creatio AI** business process element is enhanced to display and update AI Skill parameters dynamically.
More details







  - When an AI Skill is selected in the **Call Creatio AI** element, its parameters are displayed automatically.
  - Creating new AI Skill parameters, renaming, and deleting existing AI Skill parameters are reflected in real time, without requiring a page refresh.

- Title and focus state of the **Navigation panel** button in the top panel is changed from dynamic to static.

- The filtering of objects available for selection when creating custom system settings is changed. Virtual objects are now excluded from the list, ensuring data consistency and preventing potential app errors.

- The `aria-expanded` and `aria-haspopup="menu"` properties in the DOM for the `menu-buttons` property of the **List** component are changed to comply with WCAG.

- Keyboard focus placement to the first menu item when menu items load after opening is changed to comply with WCAG.

- Now specific values on the line, spline, area, and scatter widgets are displayed as different shapes instead of circles.

- Desktop behavior is adjusted to be responsive on both small and large screen sizes, for example, 317-1080 px and 1080-1920 px.

- Localization resources of titles for chat-related objects are updated.

- The description of the **Depends on applications** heading on the **Dependencies** tab of the **App properties** window in the No-Code Designer is changed from "The "Some Name" application depends on the following applications:" to "Configure dependencies to extend the application using elements inherited from other applications and store them in the current application. The "Some Name" application depends on the following applications:".

- The **Advanced settings** tab in the No-Code Designer is renamed to **Package settings**.

- The states of the Freedom UI Designer element library and setup area in the user profile are now stored for the Freedom UI Designer as a whole, rather than for a specific page as before. For example, when you modify a specific page using Freedom UI Designer and collapse element library, element library is collapsed for other pages until you expand it.

- Now, when you save changes to the "Addon" type schema of another package at the same hierarchy level, the dependency on that package is automatically added to the current package.

- The UX of the dialog window that tells about unsaved data on the page is changed.
More details







  - Added the **Don't save** button to proceed with user's action without saving changes.
  - Added the **Cancel** button to continue working on the page without saving.
  - Added the **Save** button to save changes and proceed with user's action.

- Now the "Update split test audience" business process is no longer hidden in the Process library.

- The "Can bypass page opening restrictions" (`CanBypassPageOpeningRestrictions` code) system operation is disabled out of the box for external users.

- The custom tooltip of the **Remove** button in the **Configuration** section is changed to the default browser tooltip.

- Working with many records in the editable cell of the "Chat actions" expanded list on the "Chat settings" page is simplified. To do this, the default value of the `Lookup view` property for the "BusinessProcess" column in the `OmniChatAction` object schema is changed from the "List" property value to "Selection window."

- Task performance when working with modified data structures is improved. Deleted columns are no longer read when using the `FetchOnlyUsedColumnValues()` method of the `ReadDataUserTask` schema. This reduces unnecessary data retrieval and prevents issues.

- An optimization to request handler completion is implemented. Request handler completion is no longer impacted by binding of handler output events that involves parameter analysis using asynchronous potentially long-running operations.

- Speed optimization for login page loading is implemented when 2FA functionality is disabled. 2FA functionality is not loaded when the "Enable 2FA" (`Enable2FA` code) system setting is disabled.

- An optimization for the creation of the default resource for OAuth authentication is implemented. If the default resource is already created, Creatio does not attempt to create it again after the OAuth authentication system settings are filled out.

- An optimization for memory consumption when using system-reserved names in schema or business process parameters is implemented. Memory consumption no longer causes slowdowns and failures during high-load requests.

- Creatio now only parses webhooks explicitly specified in the **Webhook entities lookup** into objects. Out of the box, Creatio parses webhooks of "Contact," "Lead," "Order," and "Submitted form" objects. Webhooks that reference object codes not included in the lookup are blocked and logged for future reference. To retrieve blocked webhooks, contact [Creatio support](mailto:support@creatio.com). This enhances system security.

- Saving the **Multiselect lookup** component is improved.
More details







  - Selecting and removing records in the **Multiselect lookup** component now triggers displaying of the **Save** button. Otherwise, the button is not displayed on the page.
  - Component changes are not saved until the **Save** button is clicked.
  - Changes are reverted when the **Cancel** button is clicked.

- Adding records using the **Add data** business process element is changed. The `MaxEntityRowCount` setting in the ..\\Terrasoft.WebApp\\Web.config file no longer limits the maximum number of records added, as the "Add data" element processes records iteratively. This lets you copy data between objects efficiently, enhancing system efficiency.

- Size limit of email message previews in the message history for Classic UI is changed to 1 MB. To change the maximum size of email message previews in the timeline in Classic UI, set the value of the "LargeSizeEmailValue" (`LargeSizeEmailValue` code) system setting.

- The names of the "Webhook Service user," technical user, and related data bindings are changed to "Creatio Webhook Service" that better reflects the purpose and lets you unambiguously identify out-of-the-box data.

- The names of the "ALM integration," technical user, and related data bindings are changed to "Creatio ALM integration" that better reflects the purpose and lets you unambiguously identify out-of-the-box data.

- Empty messages generated due to client-side errors are no longer sent via WebSocket.

- Cumulative layout no longer shift when filters are applied on the page that includes a timeline. A loading mask is added when applying filters.

- The **Call Creatio AI** business process element now does not reference deactivated or deleted AI Skills during development and testing. This helps avoid potential configuration errors.
More details







  - A "Skill is not available" error message is displayed if the AI Skill cannot be accessed.
  - The entire business process is now invalidated since an AI Skill is mandatory for the **Call Creatio AI** element.
  - Deleting a selected AI Skill in the "API" mode no longer alters the element title, preserving the original naming structure.

- You can no longer change properties when the primary app package is locked.

- Dates in the "Modified on" column for schemas automatically created together with the template-based app now correspond to app creation date.

- Business rules from packages at the same hierarchy level are now displayed correctly in Freedom UI Designer that is opened directly from the page.

- Creating and updating the app-descriptor.json or app-descriptor-extension.json file for apps installed from SVN now works correctly.

- Column name duplication causing `ProductBase` package installation errors is fixed.

- Now, when a Windows authentication login attempt fails due to incorrect NTLM settings, a message with a detailed description of the problem is displayed instead of a link to a problem with technical user limitations.

- Now, when you click the **Apply translations** button, the package is determined even if the package lacks localization resources for the primary language culture.

- The "System.ServiceModel.ServiceActivationException: Set AspNetCompatibilityEnabled true" error that sometimes occurred during automatic creation of a default resource for OAuth authentication is fixed.

- Invalid pagination in Classic UI timeline for emails that have participants is fixed.

- Accidental marketing campaign splits ("Cannot execute INSERT in a read-only transaction" error) in PostgreSQL instances are fixed. This improves app performance and reliability.

- Image upload via `ImageApi` service is fixed. The service now enforces the file size specified in the "Image max size" (`MaxImageSize` code) system setting.

- Now feed messages are loaded in the timeline without duplication.

- Regardless of the feed message length in the timeline, the loading mask no longer appears.

- Text value of stacked bars no longer changes the color on mouse hover.

- A static content generation error that occurred when the `Body` property in the `BaseRelationshipDetailV2` schema metadata included a value is fixed.

- The **Next steps** component located in a toggle panel now automatically updates and displays the list of steps when the status changes in the progress bar.

- The **Read more** button no longer overlaps email attachments in the timeline.

- Shift+Tab hotkey in Safari browser now correctly moves keyboard focus within the **List** component.

- The error of populating a "Phone" field type that has an input mask from a related record is fixed. The phone number is now displayed as valid.

- The **Formatting options** button for the "Rich text" field type no longer flicks when focused using the Tab key.

- The toolbar for the "Rich text" field type no longer overlaps the **Message composer** text after saving a link.

- The loading of inline images for the "Rich text" field type on multi-domain Creatio websites is fixed.

- The display of the rewrite text icon for the "Rich text" field in the dialog window is fixed.

- User access rights caching for details in Classic UI no longer affect system administrators' access to detail settings.

- The update of contact fields based on the SAML response during the initial user login using JIT via SSO to Creatio deployed on .NET Core is fixed.

- An error with the service provider during SSO login to Creatio deployed on .NET Core is fixed.

- The addition of a WhatsApp chat channel when a custom channel for another chat exists for the specified phone number is fixed.

- External users can now view calendar records in read-only mode.

- Automatic mailbox selection in the **Message composer** component is fixed. Now, when case categorization is disabled using the `CategoryFromMailBox` additional feature or the "Enable the relationship between support mailboxes and the categories of processed cases" (`DefineCaseCategoryFromMailBox` code) system setting, the default mailbox is determined using the "Customer service email" (`SupportServiceEmail` code) system setting.

- A loading mask no longer appears in Classic UI when reopening a section from the navigation panel after closing any record page within that section.

- Loading of navigation panel content ("A generic error occurred in GDI+" error) during resource processing is fixed. The defective resource is now logged and no longer interrupts the loading of navigation panel content.

- Regardless of the number of pages opened, the loading mask ("Cannot read properties of null (reading '\_lView')" error) no longer appears when sequentially opening Creatio pages in the same browser tab.

- The display of pages that include elements linked to incorrect data in DCM database tables is fixed. Page elements directly related to incorrect DCM data now load partially and do not affect the loading of other page elements. The `DisableFastDcmSchemaManagerRequest` additional feature that temporarily addressed this is no longer needed.

- A configuration corruption error ("Default workspace assembly is not initialized" message) after deleting a package that contains a \*.dll file is fixed.

- Invalid cache error after app deletion is fixed.

- The `System.Text.Json` library is updated. The current version is 8.0.5.

- The `Telegram.Bot` library is updated. The current version is 22.1.3.

- The `DomPurify` library is updated. The current version is 3.2.3.

- The `Secure` attribute to the `UserType` cookie in .NET 8.

- The `LinkPreview` additional feature is temporarily disabled to improve external source interactions.

- `jQuery` 1.11.3 library on Android will be deprecated in the upcoming Mobile Creatio releases. Learn more about the library vulnerabilities: [jquery vulnerabilities](https://security.snyk.io/package/npm/jquery) (Snyk Vulnerability Database).
More details







  - `jQuery` library will be removed from the core of the Mobile Creatio.
  - Users dependent on `jQuery` will be able to install it as a separate package for continued compatibility. This change strengthens app security without affecting compatibility.

- The `WebitelCore` and `WebitelCollaborations` packages from the app are removed. These packages are still available in the [Webitel call manager for Creatio](https://marketplace.creatio.com/node/9892) and [Webitel telemarketing for Creatio](https://marketplace.creatio.com/node/10132) Marketplace apps.

- The `UserService.svc` service and the corresponding `ClientConnection` class that enables third-party apps and services to interact with custom Creatio web services are removed. This can affect the operation of the unsupported "DevExpress" Report Designer.

- The unused `region` role in the DOM for the **Expansion panel** layout element in Freedom UI is removed.

- The foreign key constraint in the `EntryPoint` database table is removed. This no longer causes locks when deleting business process element data and improves app stability.


## Products and Apps [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-products-and-apps "Direct link to Products and Apps")

### Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-sales-creatio "Direct link to Creatio Sales")

- Forecast periods up to 2035 to the **Periods** lookup are added.

### Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-marketing-creatio "Direct link to Creatio Marketing")

- A loader while waiting for domain verification is added.
- The content display on the **Approvals** tab in the **Notification panel** is fixed.

### Digital Ads [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-digital-ads "Direct link to Digital Ads")

- Digital Ads now supports Google Ads API v18 and Facebook Marketing API v22 for enhanced compatibility and performance improvements.

### Email marketing [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-email-marketing "Direct link to Email marketing")

- A notification now appears in the Email Designer once when clicking **Copy email** and provides users with essential recommendations and terms.
- Files uploaded to the S3 file storage in the Email Designer are now displayed immediately.

### Case Management [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-case-management "Direct link to Case Management")

- The **Assignee** field is no longer cleared automatically when an external user saves changes on the case page.
- Demo data from the **Case Management** app is removed to ensure custom data consistency after installing the app from Creatio Marketplace.
- The **Add new** button from the dropdown list in the "Member/team" column of the "Responsible service team" expanded list on the service page is removed.

## Mobile Creatio [​](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog\#title-mobile-creatio "Direct link to Mobile Creatio")

- A notification about lacking access rights to view a page is added to the Mobile Creatio.

- Mobile Creatio now natively supports `MERGE` and `DELETE` request types for OData 4 in Classic UI when the `UseMobileDataService` additional feature is disabled.

- The default app colors in the Mobile Creatio are changed to comply with WCAG, resulting in updated widget colors to better align with the app design.

- Creatio AI in Mobile Creatio is enabled out of the box. Now, you can use all AI Skills available for the platform and **Customer 360** app of the main Creatio app. The functionality is managed by the `Mobile.EnableCreatioAI` additional feature.

- If the folder is selected, the folder tree opens in full-screen mode. Otherwise, the folder tree opens to 75%.

- UX of the 2FA, login, password reset page in the Mobile Creatio is improved.

- Approval process speed in the Mobile Creatio is improved.
More details







  - Sending push notifications no longer blocks other tasks.
  - Since version 8.1.4, Creatio deletes the push notification token if the token is invalid.

- iOS mobile app stability is improved by fixing an error that caused freezing and crashing in offline mode.

- Display error of decimal separator in "Number" type field in the Mobile Creatio is fixed.

- Display of related objects in Mobile Creatio is fixed by modifying the `AddQueryColumns()` method of the `DashboardGridDataSelectBuilder` schema (PostgreSQL only).

- The `MobileData` schema is removed.


- [Platform](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-platform)
- [Products and Apps](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-products-and-apps)
  - [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-sales-creatio)
  - [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-marketing-creatio)
  - [Digital Ads](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-digital-ads)
  - [Email marketing](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-email-marketing)
  - [Case Management](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-case-management)
- [Mobile Creatio](https://academy.creatio.com/docs/8.x/resources/releases/changelog/8-2-2-energy-changelog#title-mobile-creatio)