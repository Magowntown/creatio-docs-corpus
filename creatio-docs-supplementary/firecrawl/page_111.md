<!-- Source: page_111 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 05/10/2024

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are pushing things forward with Creatio version 8.1.3 Quantum, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-10 "Direct link to Creatio composable apps")

### Order and Contract Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-11 "Direct link to Order and Contract Management")

**Product catalog page**. You can now access the product catalog directly from the order page. The page includes a hierarchical set of product categories. The page also lets you add products to cart, remove them from cart, and edit records in the cart.

Opening the product catalog

![Opening the product catalog](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/gif_opening_the_product_catalog.gif)

### Lead Generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-113 "Direct link to Lead Generation")

**LinkedIn permission updates**. On May 15, 2024, LinkedIn will implement critical updates to its API. To maintain seamless integration and ensure continuous lead generation, it is essential to update permissions for all active LinkedIn integrations before this date.

**Additional languages in LinkedIn forms**. You can now use LinkedIn forms in languages besides English to register leads.

**Web forms and pages**. Lead Generation app now includes the **Web forms and pages** section that lets you integrate your landing page with Creatio. The section functionality is identical to the functionality of the import page in the **Contacts** section.

Web forms and pages section

![Web forms and pages section](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_web_forms_and_pages_section.png)

### Productivity [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-114 "Direct link to Productivity")

**Available activity results**. It is now possible to specify available activity results in the conditional flow of a business process. Creatio displays only those results in the drop-down list on the **Tasks** form page.

### Case Management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-14 "Direct link to Case Management")

**Notification for external messages**. Out-of-the-box, Creatio now sends an email notification to the case contact when the case assignee posts an external message.

## Financial Services Creatio [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-200 "Direct link to Financial Services Creatio")

**Freedom UI**. You can now take full advantage of Freedom UI in **Financial accounts**, **Cards**, **Products**, and **Documents** sections.

Cards section

![Cards section](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_cards_section.png)

## Creatio Service [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-115 "Direct link to Creatio Service")

**More items in the Agent desktop queue**. To improve the user experience, Creatio now displays more items in the Agent desktop queue out of the box. You can edit the value in the "Maximum number of unprocessed items in queue" ("MaximumQueueItemsInQueue" code) system setting.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-8 "Direct link to End user experience")

**Calendar UX improvements**.

- The component now populates the linking field automatically when you create a new calendar record that filters content by page data. For example, if you link a calendar to an account, Creatio automatically links the new activity to the account.
- You can now view more items in the monthly view.

**List settings for specific folder**. It is now possible to customize the list for a specific folder and save the settings for all users that can view the folder.

List that has different columns for different folders

![List that has different columns for different folders](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/gif_list_settings_for_folders.gif)

**Inline files in Rich text fields**. You can now add various types of files to **Rich text** fields. Creatio adds the files to record attachments automatically as well. Click the file to download it. Configure the available file types and maximum file size in the "File extensions DenyList" ("FileExtensionsDenyList" code) and "Attachment max size" ("MaxFileSize" code) system settings, respectively.

Inline file

![Inline file](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_inline_file.png)

Field setup was also updated. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-2).

**Lookup selection window in the Message Composer**. It is now possible to select email templates using the standard lookup selection window.

**Metric UX improvements**.

- If you have a metric on a list page that displays the value of a list object and update the list values, Creatio updates metric values in real time without the need for you to refresh the page. This works for changes made by the current user.
- Metric widgets are now smaller out of the box.

Metric setup was also updated. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-2).

**Call titles in the timeline**. Creatio now generates the call title in the timeline based on the call direction. For example, "John Best called Alexander Wilson" for outgoing calls, or "Alexander Wilson called John Best" for incoming calls.

**Release notes in Creatio**. You can now open release notes section of the Creatio Academy from the **Help** menu.

View release notes

![View release notes](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_release_notes.png)

**Hungarian localization**. You can now use Creatio in Hungarian.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-1 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-2 "Direct link to Application Hub")

**Deactivated packages**. You can now deactivate packages. This preserves information about package existence and package contents, but makes the contents inaccessible. You can reactivate or delete deactivated packages. It is possible to view all deactivated packages in the No-Code Designer and the **Configuration** section.

Deactivated package

![Deactivated package](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_deactivated_package.png)

**New default app versions**. Versions of new Freedom UI apps now start from 1.0.0.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-4 "Direct link to Freedom UI Designer")

**Lookup descriptions**. You can now display a value inside a lookup under the field that uses the lookup. For example, this is useful if you want to elaborate on the values for users.
To take advantage of this functionality, turn on the "EnableComboboxValueDetails" feature. Learn more: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631).

Lookup description

![Lookup description](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_lookup_description.png)

**New properties of Freedom UI pages**. Freedom UI Designer now displays the parent page and whether the page replaced the parent page in the page settings.

New page properties

![New page properties](https://academy.creatio.com/docs/sites/academy_en/files/images/Release_notes/release_notes_8_1_3/scr_new_page_properties.png)

**Improvements to Metric widget**.

- Customize the metric size.
- Specify where to display the metric text relative to the value.

Metric UX was also improved. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-8).

**Improvements to Rich text field**.

- Specify where to store files uploaded to the field.
- Specify the record to attach files uploaded to the field.

Field UX was also improved. Learn more [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-8).

**New button action**. It is now possible to move records or specific record columns between two lists, for example, product catalog and cart, using the new "Move selected records" button action.

**Parameters in the "Open specific page" button action**. It is now possible to use parameters in the "Open specific page" button action. For example, if the page includes parameter inputs that have specific values, you can pass the values to a different page that includes similar parameter inputs while using the button action.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-4 "Direct link to Business processes")

**Record collections for a single process instance**. You can now run a single instance of a business process by multiple records selected in the list.

**Iteration limit for a single process**. To ensure optimal Creatio performance and stability, processes can now trigger themselves a finite number of times, directly or indirectly.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-6 "Direct link to Integrations")

**Email preservation on Creatio restart**. The email synchronization service now preserves and queues messages if you restart the Creatio website. This ensures no data is lost when a restart is required.
To use this functionality in Creatio on-site, upgrade the Email Listener microservice and turn on the "UseEmailSyncQueue" feature. Learn more: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631).

**SSO configuration security**. Newly created SSO configurations that do not have SAML request signing or SAML encryptions turned on are now disabled automatically. Creatio shows the configuration in the UI, but users cannot log in. To enable the configuration, the Creatio administrator must upload the SSL certificate and turn on SAML request signing.

**Error logging for Cisco Finesse and Webitel connectors**. If you are experiencing an issue related to the connector license, Creatio now posts a message to the browser console that helps you identify the issue quickly.

**Management of just-in-time provisioning for external users**. It is now possible to turn JIT on or off for either system or external users separately.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-16 "Direct link to Advanced customization")

**API for Freedom UI selection window**. You can now use custom code to work with the Freedom UI selection window using the API. It is also possible to create custom data selection windows. Learn more: [Customize selection windows](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/selection-window).

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-5 "Direct link to Administration")

**Automatic license distribution**. It is now possible to distribute licenses among specific user groups automatically. Every time a user is included in or excluded from a role during LDAP synchronization or role provisioning via SSO, Creatio distributes the licenses that correspond to their roles. You can check whether the license was distributed automatically or manually on the user page or in the **License manager** section. Learn more: [Redistribute licenses based on user roles](https://academy.creatio.com/documents?id=1472&anchor=title-1472-2), [Role-based license redistribution](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/role-based-license-redistribution).

**License restrictions for navigation menu**. Users that have **Self-service** license can now view the **Main page** section if they use Classic UI, but not Freedom UI.

**User email deactivation**. If you deactivate a user, Creatio now deactivates their email automatically in the synchronization service as well.

**Password recovery**. It is now possible to use the password recovery mechanism for both external and internal users.

**Enhanced page permission check**. Creatio now checks whether the user role is permitted to view the page in the object settings when a user opens a page directly via URL. If the page is assigned to a different role, Creatio opens the desktop instead. This restriction does not apply to users or roles that have permissions to the "Can use bypass page opening restrictions" ("CanBypassPageOpeningRestrictions" code) system operation. For existing Creatio instances, these roles include "All Employees" and "All External Users."

**Enhanced security for external users**. It is no longer possible to delete or modify data of the **SysPortalConnection** user. This ensures the correct self-registration of external users, password recovery, and case feedback collection.

**Performance improvements**.

- When you load a Freedom UI page for the first time, Creatio uses up to 20-25% less traffic.
- When you load a Classic UI page in the **Forecast** section and pivot tables, Creatio uses less traffic.
- RAM usage while working with Freedom UI pages for a long time was optimized.
- Creatio loading time in a new browser tab is now faster.
- **List** component now uses virtual scroll, i. e., loads only the visible records and loads other records as you scroll.
- The **Calendar** component now loads particularly large (300+) numbers of meetings faster.
- Performance of **Message Composer**, **Next steps**, and **Feed** components was improved.
- Freedom UI Designer now loads widgets and tabs that have a large number of components faster.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes\#title-2782-17 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.1.3 Quantum. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Synchronization of Office 365 calendar**. It is now possible to import meetings that have "Creatio sync" category from Office 365 calendar to Creatio. To access this functionality, contact [Creatio support](mailto:support@creatio.com).

**Sidebars**. It is now possible to create new sidebars (bars in Notification and Communication panels) in Freedom UI using no-code tools and adapt sidebars from the previous generation using development tools. All Freedom UI sidebars developed for Creatio versions 8.0.6 to 8.1.2 were moved to a dedicated Additions panel. To access the new sidebar development functionality, turn on the "SidePanelExtensions" feature. Learn more: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631), [Customize sidebars](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/sidebar).

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-10)
  - [Order and Contract Management](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-11)
  - [Lead Generation](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-113)
  - [Productivity](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-114)
  - [Case Management](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-14)
- [Financial Services Creatio](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-200)
- [Creatio Service](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-115)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-8)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-4)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-6)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-16)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-5)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/813-quantum-release-notes#title-2782-17)