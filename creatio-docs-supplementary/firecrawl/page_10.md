<!-- Source: page_10 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 06/05/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.0.9, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-1 "Direct link to No-code platform")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-2 "Direct link to Application Hub")

**Streamlined app update mechanism**. If Creatio finds an update, the app in the Application Hub displays the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/icn_update.png) icon. Click it to update the app.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-3 "Direct link to Business rules")

**Filters for dropdown fields**. It is now possible to filter available values of a dropdown field by selected value of another dropdown field in Freedom UI using business rules. For example, filter cities by selected country.

Setting up the filter for a dropdown field

![Setting up the filter for a dropdown field](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/gif_filtering_business_rule.gif)

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-4 "Direct link to Freedom UI Designer")

**Retirement of Action dashboard component**. The component was retired as it was replaced with **Progress bar** and **Next steps** components that let you set up user workflow much more flexibly. Action dashboards are still available on existing pages, but you cannot add them to new pages.

**Next steps**. You can now view activities and tasks generated automatically or added manually as tiles in Freedom UI using the **Next steps** component. The component completes activities and displays new activities based on the stage in the **Progress bar** component. The new component also lets you do the following:

- add a task or email
- complete an activity manually
- approve a record
- view the task owner and open their contact page

Next steps component

![Next steps component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_next_steps.png)

**Communication options**. You can now manage the record communication options in Freedom UI using the **Communication options** component. The component is available if you have the Customer 360 app installed.

Communication options component

![Communication options component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_communication_options.png)

**Improvements to the Quick filter component**.

- It is now possible to filter the connected component by one or more values of any lookup. For example, display only cases that have a particular status.

You can specify the lookup values available for selection using advanced filters. For example, display only active case statuses.
Filtering a list using the quick lookup filter

![Filtering a list using the quick lookup filter](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/gif_quick_lookup_filter.gif)

- The dropdown list of the lookup filter lets you select all records visible in the filter list and bulk clear all selected records.

- The lookup filter displays selected values at the top of the list when you open the filter again. This lets you deselect the required records quicker and easier.

- You can now filter charts except for "Sales pipeline" and "Full pipeline" using the component.


Filtering charts using the quick lookup filter

![Filtering charts using the quick lookup filter](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/gif_chart_lookup_filter.gif)

**Dedicated pages that add records**. It is now possible to set up dedicated pages that enable users to add records in Freedom UI. For example, this lets you enable users to add records using a mini page and view or edit records using a full page.

**Buttons that open mini pages**. The "Open specific page" button action now supports mini pages.

**Connect lists to other components**. You can now connect list, approval lists, and attachment lists to other page components that work with data. This includes lists or dashboards except "Sales pipeline" and "Full pipeline." The connected components filter their data by records displayed in the list. For example, this lets you filter case chart data by currently open cases.

You can link components via direct connection, for example, the city of a contact. If you connect a list to another list, you can also filter data by the record selected in the list.

Charts connected to a list

![Charts connected to a list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/gif_charts_connected_to_list.gif)

**Classic folders in Freedom UI**. If you create a Freedom UI app that uses an object that has a Classic UI section, you can reuse folders of the Classic UI section in the Freedom UI **Folders** component. This streamlines the migration of Classic UI sections to Freedom UI

**Streamlined configuration of email and phone fields**. Creatio no longer generates email and phone links based on field code ( **Code** parameter in the Freedom UI Designer). This streamlines the setup of **Email** and **Phone** fields. If you still have email or phone fields set up via field code, make sure they have **Email** or **Phone** type, respectively.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-5 "Direct link to Business processes")

**Process parameters in Freedom UI**. Business processes now support parameters in Freedom UI pages. Create, view, edit, and delete the parameters in the Freedom UI Designer. Initialize and retrieve the resulting parameter values in business processes.

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-6 "Direct link to Administration")

**FileApi for chat attachments**. Chat attachments now support Creatiowide file storage rules.

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-7 "Direct link to UI and system capabilities")

**Page link UX**. The browser no longer refreshes the page if the target page URL leads to the same page but has a letter in a different case or "/" after the "#" character. This greatly improves the UX if you have custom pages that use such links.

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-8 "Direct link to Freedom UI sections")

**Case stage in the list**. Freedom UI lists now visualize the stage of a dynamic case. You can also transfer a case to a different stage if the list is editable.

Case stage in the list

![Case stage in the list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_case_stage_in_the_list.png)

### Communication panel in Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-9 "Direct link to Communication panel in Freedom UI")

**Chat attachment storage**. You can now save chat attachments to the database or an external repository.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-10 "Direct link to Out-of-the-box Creatio solutions")

### Customer 360 [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-11 "Direct link to Customer 360")

**Mini pages**. The app now uses a mini page to add contact or account records.

Mini page that adds records

![Mini page that adds records](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_mini_page.png)

**Communication options**. Contact and account pages now display communication options.

### Mobile App [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-13 "Direct link to Mobile App")

**Tablet UI**. Lists and pages in the Creatio mobile app are now optimized for tablets.

Tablet UI in the mobile app

![Tablet UI in the mobile app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_tablet_ui.png)

**Freedom UI links**. The mobile app now supports the new format of links to Freedom UI pages.

**Dynamic folders**. The mobile app can now use dynamic folders in Freedom UI pages regardless of whether the web Creatio instance uses Freedom UI or Classic UI pages.

**Background synchronization**. The app now supports background synchronization on mobile devices that have Android 12 and later.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-14 "Direct link to Development tools")

**Changes to app properties**.

- Apps can now contain more than one property file. Creatio marks every package that contains properties as Primary. You can delete the property file or transfer it to another package only if the package is unlocked.
- The mechanism that generates properties was changed. Now, if Creatio stores the property file in a locked package, you cannot modify the file or transfer it to a different package. If you are improving an installed app and properties are stored in a locked package, Creatio adds a new package that contains properties and marks the package as Primary.
- If you install an archive that does not contain app properties, Creatio no longer creates the property file automatically.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes\#title-2732-15 "Direct link to Beta testing of new features")

Important

The feature below is available for beta testing in Creatio version 8.0.8 Atlas and might not work as intended in Safari browser. To evaluate new Creatio capabilities, disable the "DisableRedirectToShell" feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Automatic redirection to Freedom UI**. Creatio now redirects links to Classic UI form pages to their Freedom UI counterparts if the following conditions are met:

- You have both a Classic UI and Freedom UI section.
- You set up Creatio to open Freedom UI form pages. Learn more in the user documentation: [Manage the form pages in the Freedom UI and Classic UI](https://academy.creatio.com/documents?id=2413).

Creatio also redirects links to any page in the Classic UI format to Freedom UI automatically if you have Freedom UI turned on. This redirect type lets you exclude links that lead to pages that are incompatible with Freedom UI from redirection in the "Blacklist of redirects from Classic UI" lookup.

Both redirect types let you use the "ClassicUI" query parameter to force open a link in Classic UI without setting up the lookup. In this case, the links must look as follows:

- **[https://yoursite.creatio.com/0/Nui/ViewModule.aspx?ClassicUI#CardModuleV2/ContactPageV2/edit/{some](https://yoursite.creatio.com/0/Nui/ViewModule.aspx?ClassicUI#CardModuleV2/ContactPageV2/edit/%7Bsome) contact Id}** for Classic UI links
- **[https://yoursite.creatio.com/0/Shell/?ClassicUI#Card/Contacts\\\_FormPage/edit/{some](https://yoursite.creatio.com/0/Shell/?ClassicUI#Card/Contacts%5C_FormPage/edit/%7Bsome) contact ID}** for Freedom UI links

Important

The features below are available for beta testing in Creatio version 8.0.9 Atlas. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Portal user overhaul**.

- Portal users are now called external users. "Portal user" user type and "All portal users" root role were renamed to "External user" and "All external users," respectively.

- Freedom UI is turned on for external users in new Creatio instances out of the box. You can turn it off for external users in the "Use Freedom UI interface for external users" ("UseNewShellForExternalUsers" code) system setting. Turning off Freedom UI Creatiowide turns it off for external users as well.

- You can create Freedom UI sections and form pages available for external users. To do this, specify the pages on the **Pages** tab of the Object Designer, configure object permissions for external users, and add the section to a workplace accessible by external users.

Application Hub marks sections and pages available for external users using the "External" label.
Pages that have the External label

![Pages that have the External label](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_9/scr_pages_for_external_users.png)

- External users can view the right panel that contains the **Feed** section as well as notifications regarding activities, processes, and approvals.


- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-6)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-7)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-8)
  - [Communication panel in Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-9)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-10)
  - [Customer 360](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-11)
  - [Mobile App](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-13)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-14)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/809-atlas-release-notes#title-2732-15)