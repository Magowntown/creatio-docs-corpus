<!-- Source: page_27 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 12/13/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.0.6, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## Composable architecture [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-7 "Direct link to Composable architecture")

Creatio 8.0.6 offers a composable architecture that empowers you to accelerate the app design process and maximize the component reusability. Creatio platform delivers a library of composable elements that no-code creators can use to assemble functionality blocks, applications, and full-scale products using no-code. The composable no-code architecture brings agility to a new level. Since all the components are pluggable, replaceable, and reusable, the significant amount of configuration, customization, and development work is now replaced by assembling your apps from available blocks and components.

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-8 "Direct link to Application Hub")

Enjoy **Customer 360**, the very first out-of-the-box Freedom UI app developed using the composable approach and only no-code tools. The app lets you manage contacts and accounts in Freedom UI. New Creatio instances replace the classic **Contacts** and **Accounts** section in existing workplaces with their **Customer 360** counterparts.

**Apps based on existing objects**. It is now possible to create Freedom UI sections and apps that use the "Records and business processes" template based on existing Creatio objects. You can specify which section to display in the workspace settings.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-9 "Direct link to Freedom UI Designer")

**Account and contact compact profiles**. You can now display the main contact or account data—for example, account name and location or contact name, birth date, and country - using the **Account compact profile** and **Contact compact profile** components. The components are available if you have the **Customer 360** app installed.

Contact compact profile

![Contact compact profile](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_contact_compact_profile.png)

**Local time**. You can now display the current time within a time zone using the **Local time** component. The component takes data from any time zone field.

**Timer**. You can now count down to or up from specific date and time using the **Timer** component. For example, this is useful if you want to display the case response deadline. The component supports custom captions and macros, e. g.: " **#timer#** spent on the Nurturing stage."

Timer component

![Timer component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_timer.png)

**Image**. You can now add images to Freedom UI pages using the **Image** component. The component can display images from different sources, for example, Creatio database or CDN.

**Timeline**. You can now display the communication history and linked records of a specific record in chronological order using the **Timeline** component. Users can like and comment feed records in the timeline.

The component sets the objects to display in the timeline automatically. To display additional objects, select the "Show in Timeline component by default" checkbox in the Object Designer. The primary display value and creation date of the records are displayed on the timeline. You can customize the columns to display using low-code tools.

Timeline component

![Timeline component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_timeline.png)

**Label macros**. You can now use macros in the **Label** component. They must follow the **#CurrentUser.<Fields>#** pattern, where **<Fields>** are fields of the current user contact. For example, "Your business phone is **#CurrentUser.Business Phone#**."

**Chart backgrounds**. It is now possible to add semi-transparent backgrounds that have various colors using the "Glass effect" style, available for all charts and metrics except "Sales pipeline" and "Full pipeline."

Metric that has the Glass effect style

![Metric that has the Glass effect style](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_glass_effect_metric.png)

**Container wrapping**. You can now specify whether to wrap elements within flex containers. If you turn off wrapping for a container that has multiple elements placed in a single row, Creatio adds a horizontal scroll bar instead of wrapping the elements when container becomes narrower. For example, this is useful if you want to place a folder tree and list on a single row.

**Page templates**. Freedom UI page templates were updated. Now, the page header is editable as well.

Editable page header

![Editable page header](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_new_page_template.png)

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-1 "Direct link to UI and system capabilities")

### Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-2 "Direct link to Freedom UI")

As part of the new architecture, the recent update features a revamped shell. The Freedom UI encompasses the latest and greatest UX best practices to streamline the app design process and user adoption, all while providing a high level of personalization. Learn more in a separate article: [Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445).

The Freedom UI is turned on for new Creatio instances by default. Learn how to turn on the Freedom UI for existing instances: [Turn on the Freedom UI](https://academy.creatio.com/documents?id=2446).

Freedom UI

![Freedom UI](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_freedom_ui_shell.png)

### Desktops in the Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-3 "Direct link to Desktops in the Freedom UI")

**Desktop**. You can now add widgets that display to stunning Creatio desktops. Users can switch between the available desktops and select the desktop to display by default. System administrators can add or customize desktops as well as grant desktop permissions to users. You can open the desktop by clicking the logo in the top left.

Creatio desktop

![Creatio desktop](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/gif_set_up_desktop.gif)

**Section icons**. The icons of base Creatio sections were redrawn to fit the Freedom UI design code exactly.

**Responsive design**. You can now use Creatio more comfortably on screens and windows of various sizes, including mobile.

**All apps**. You can now view every available section in the **All apps** workplace.

**Side panel minimization**. You can now minimize the side panel to free up even more workspace.

Minimizing the side panel

![Minimizing the side panel](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/gif_minimize_side_panel.gif)

**Section search**. You can now search for sections within the active workspace using the search bar.

Searching for a section

![Searching for a section](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/gif_section_search.gif)

**Search bar in the top panel**. The command line functionality is no longer included in the Creatio search bar.

**System Designer button**. Creatio now displays the button only for users that have permissions to open the System Designer.

### Communication panel in the Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-4 "Direct link to Communication panel in the Freedom UI")

**Panel redesign**. The communication panel was moved to the top bar. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/icn_communication_panel.png) communication panel button to manage feed, calls, emails, and chats. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/icn_notification_panel.png) notification panel button to view reminders, feed notifications, approvals, noteworthy events, system messages, and business process tasks.

**UX improvements on the Calls tab**.

- Agent status. You can now click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/btn_agent_status.png) button to change the status of the call center agent.
- Telephony setup. You can now click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/btn_set_up_telephony.png) button to open the telephony setup page.

### Appearance customization of the Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-5 "Direct link to Appearance customization of the Freedom UI")

**Turn on the shell**. The Freedom UI is turned on for new Creatio instances by default. Existing customers can turn the Freedom UI on using the "Use Freedom UI interface" ("UseNewShell" code) system setting. You can set different setting values for different users, for example, to roll the Freedom UI out gradually.

The Freedom UI is fully compatible with out-of-the-box pages that use the previous version of the UI. They continue to operate as intended regardless of the UI type. Most pages customized using code are compatible as well.

We recommend turning on the Freedom UI for all users only after you check whether the existing customizations are compatible with the new UI.

**Logo**. The default logo and logo background can now be changed using the "Logo in Freedom UI panel" ("CrtAppToolbarLogo" code) and "Background color for the logo in Freedom UI" ("CrtAppToolbarLogoUnderlayColor" code) system settings. We have already migrated logos of existing customers to the new system settings, and set the background of these logos to white.

**Color coded sections**. It is now possible to color code backgrounds of section icons in the side panel.

Color coded sections

![Color coded sections](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_color_coded_sections.png)

**Applying changes**. You no longer need to log out of and log back in to Creatio to apply changes to workplaces and sections. For example, add a section to a workplace, change the section icon.

**Hidden workplaces**. You can now hide workplaces from the classic UI. To do this, select the **Use only in shell** checkbox in the workplace settings.

**Quick record add menu**. You can now populate the menu using the "Quick add records menu" lookup and add different menu items for different user roles.

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-6 "Direct link to Freedom UI sections")

**Color coded lookup values**. You can now color code lookup values in the lists. To do this, open the lookup and specify the hex color code in the **Color** column.

Color coded lookup values

![Color coded lookup values](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_color_coded_lookup_values.png)

**Search UX improvements**. The user experience in the **Search** Freedom UI component was improved:

- Search by columns. You can now specify the columns to search.
- Icon-only mode. You can now enable the icon-only mode so that the component loads minimized to an icon.

**Partial scrolling**. It is now possible to scroll down the selected page area or container instead of the entire page.

### Mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-13 "Direct link to Mobile app")

**Freedom UI**. The app was migrated to the Freedom UI, including the **Customer 360** app.

Freedom UI in the mobile app

![Freedom UI in the mobile app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/gif_mobile_app.gif)

**Bottom bar**. You can now open the app list, notification panel, and settings from the bottom navigation bar.

**Notifications**. You can now manage notifications in the mobile app as well as open records linked to notifications.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-10 "Direct link to Business processes")

**Freedom UI pages**. You can now use Freedom UI pages in business processes and cases if you have the Freedom UI turned on.

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-11 "Direct link to No-code platform")

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-11 "Direct link to Administration")

**User profile**. The user profile page was rebuilt using Freedom UI.

- Now, the users can change more settings related to their Creatio profile, for example, name and photo. The changes are applied on saving without the need to relogin to Creatio.
- Users can open the old profile page by clicking "Additional settings."
- System administrators can restrict user permissions to edit certain profile columns, for example, login and email.
- System administrators can customize the page in the Freedom UI Designer. New fields can be added using custom code.

New user profile page

![New user profile page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_6/scr_user_profile_page.png)

**Form pages to open in classic sections**. You can now specify whether to open a Freedom UI or classic form page in classic sections if the object has both form pages. **Freedom UI sections** always open Freedom UI form pages when you add, view, edit, or copy a record. In other cases, Creatio determines the page to open using the mechanism specified below.

To specify the form page to open, use the following system settings:

- "Default edit pages in new UI" ("EditPagesUITypeForFreedomHost" code) for the Freedom UI
- "Default edit pages in old UI" ("EditPagesUITypeForEXTHost" code) for the classic UI

Alternatively, add exceptions for specific objects to the "Edit pages in UIs by object" lookup.

**Personalized greeting macro**. It is now possible to personalize greetings in emails or labels using the **#Recipient Name#** macro. Creatio takes the macro value from the "GivenName (First Name)" column. If the column is empty, the value from the "Name (Full name)" column is taken instead.

**Demo mode in the calls panel**. Creatio now displays the input field, setup button, agent status, and call records (if available) even if you do not have the telephony set up. This streamlines the workflow of Creatio partners that set up demo environments.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes\#title-2502-14 "Direct link to Development tools")

**Freedom UI pages created in the Object Designer**. If you use Object Designer to add a Freedom UI page for an object that only has a classic UI section, add the new page to the "Edit pages in UIs by object" lookup. The existing pages created by customers have already been added to the lookup.

Alternatively, set the following system settings to "8x pages":

- "Default edit pages in new UI" ("EditPagesUITypeForFreedomHost" code) for the Freedom UI
- "Default edit pages in old UI" ("EditPagesUITypeForEXTHost" code) for the classic UI

**Hidden objects**. You can now hide rarely used objects in Studio Creatio. To do this, select the **Show in advanced mode only** checkbox in the Object Designer. To view hidden objects, turn off the "IsAdvancedObjectDisplayModeDisabled" feature.

- [Composable architecture](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-7)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-8)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-9)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-1)
  - [Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-2)
  - [Desktops in the Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-3)
  - [Communication panel in the Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-4)
  - [Appearance customization of the Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-5)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-6)
  - [Mobile app](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-13)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-10)
- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-11)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-11)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/806-atlas-release-notes#title-2502-14)