<!-- Source: page_92 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 04/17/2023

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with Creatio version 8.0.8, featuring the following **new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-1 "Direct link to No-code platform")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-2 "Direct link to Application Hub")

**App bundles**. You can now install app bundles, i. e., archives that contain multiple apps.

**App code**. You can now set a custom app code to use for generating objects and section schemas when you create an app. The code also serves as a unique app ID.

**Section code**. You can now set a custom section code to use for generating object and schema names when adding Freedom UI sections.

**Random icons and colors**. Creatio now sets a random icon and color when you create an app or section. This helps you differentiate among test apps and sections. You can set different icon and color upon creation or change them later if needed.

**Marketplace app compatibility**. Now, when you select a Marketplace app to install, your Creatio instance passes Creatio version to Marketplace and Marketplace automatically downloads the compatible published app.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-3 "Direct link to Business rules")

**Tab visibility**. You can now manage the visibility of individual tabs in the **Tabs** component using business rules. For example, display the "Approvals" tab only for requesters and request owners.

**Constant values in fields**. You can now populate fields with constants using business rules. For example, populate the request description based on the category selected by the user.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-4 "Direct link to Freedom UI Designer")

**Mini pages**. You can now create mini pages in Freedom UI to enable users to add or edit records without opening the form page. Mini page templates support all Freedom UI components and can be set as default form pages.

Set up a mini page

![Set up a mini page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/scr_mini_page.png)

**Progress bar**. You can now track and change case stages on any Freedom UI page using the **Progress bar** component. The component works with existing cases seamlessly. The component layout is fully responsive and supports color coding.

Progress bar component

![Progress bar component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/scr_progress_bar.png)

**Date/time filters in Freedom UI**. You can now set up a filter by date/time on any Freedom UI page using the **Quick filter** component. The filter can have a default period applied for any users that load the relevant page for the first time. If the user changes the default period manually on the page, Creatio no longer applies the period for the user.

Using a date/time filter in Freedom UI

![Using a date/time filter in Freedom UI](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/gif_using_a_datetime_filter.gif)

**Web link icons**. You can now select from 24 more icons to display in a **Web link** field in place of the default ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/icn_web_link_default.png) icon.

Icons available in the Web link field

![Icons available in the Web link field](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/scr_web_link_icons.png)

**List filters**. You can now set up filters by page data in lists easier:

- If the page only has a single data source available, Creatio adds the data source to the filter automatically.
- If you select a list or data source column and only a single column can be selected in the corresponding data source or list, Creatio selects that column automatically as well.

**Timeline enhancements**.

- The component now updates the content automatically without the need to refresh the entire page as long as the **Enable live data update** checkbox is selected for the corresponding object in the Object Designer.
- The component now displays the date by which to sort records of an object live. If the sorting value is empty, the component sorts records by modification date.

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-5 "Direct link to Business processes")

**Improvements to edit pages**. Creatio now finishes the execution of the **Open edit page** process element and closes the page only when a user clicks the button that saves the record. This enables users to continue working with the edit page when Creatio saves the page implicitly, for example, after adding a detail record or changing the case stage.

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-6 "Direct link to Administration")

**Password security requirements**. New password security policies are available:

- Password must differ from login regardless of case, for example, Supervisor/supervisor, test/tesT, etc. Turn on the policy in the "Password complexity: not equal to user login" ("PasswordNotEqualToUserLogin"code) system setting.
- Password must differ from commonly used weak passwords, for example, qwerty, 12345678, password, etc. Specify weak passwords in the **Weak password list** lookup. Turn on the policy in the "Password complexity: deny weak passwords from list" ("PasswordNotFromWeakList" code) system setting.

**.NET 6 support**. Studio Creatio as well as Sales Enterprise, Marketing, Service Enterprise bundle in Freedom UI are now available on .NET 6. This framework let you deploy Creatio both on Windows and Linux. Creatio .NET Core 3.1 products are still available, but we are going to replace them with .NET 6 product lineup in upcoming releases.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-7 "Direct link to Integrations")

**UTM marks in webhooks**. You can now use webhooks to track lead channel, source, campaign, and bulk email passed via UTM marks for records of the "Lead" and "Submitted forms" objects.

**OpenID support**. You can now use the OpenID provider to integrate Creatio with your company infrastructure and set up a unified entry point for all platforms.

**OAuth authentication for email providers**. You can now integrate as many email providers that use OAuth authentication with a single Creatio instance as needed.

**IdentityService on .NET 6**. IdentityService application that enables OAuth integrations in Creatio was migrated to .NET 6.

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-8 "Direct link to Performance")

**Page loading time**. Page loading time was improved even more, especially when moving from pages that have a large amount of content. For example, when you open a record page from a list page that contains many records and columns.

**New sections**. Creatio now adds Freedom UI sections to existing apps twice as fast.

**Management of advanced visual effects**. Users can now disable the blur in the semi-transparent "Glass effect" chart style for themselves on the user profile page. This setting has a higher priority than the "Disable advanced visual effects" ("DisableAdvancedVisualEffects" code) system setting.

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-9 "Direct link to UI and system capabilities")

As part of transition to new architecture, the application UI was revamped in Creatio version 8.0.6. The Freedom UI encompasses the latest and greatest UX best practices to streamline the user workflow all while providing extensive personalization capabilities. Learn more in a separate article: [Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445).

The Freedom UI is turned on for new Creatio instances by default. Learn how to turn on the Freedom UI for existing instances: [Turn on the Freedom UI](https://academy.creatio.com/documents?id=2446).

### Freedom UI sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-10 "Direct link to Freedom UI sections")

**List UX improvements**.

- It is now possible to add records to editable lists directly. You can do this in multiple ways:


  - Press the **New** button below the list. This adds the record last in the list.
  - Select a cell and press Shift + Enter. This adds the record below the selected row.
  - Point to the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/btn_row_control_panel.png) row control panel and click the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/btn_add_record_round.png) button. This adds the record below the row.

Adding a record from the list

![Adding a record from the list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/gif_adding_a_record_from_the_list.gif)

- It is now possible to delete cell data from the editable list by pressing Delete or Backspace.

- It is now possible to delete a record whose column you selected in the editable list by pressing Shift + Delete.


**Feed UX improvements**.

- You can now attach files to posts or comments.
- The component saves message drafts automatically when you close the tab or open a different page.

**Timeline UX improvements**.

- Timeline records now display placeholder initials if the contact does not have a photo. This makes the communication history more personalized.
- The component now displays activities for all contacts included in the participant list.
- You can now view the number of email recipients as well as recipient details in the **Timeline** component.

**Message composer UX improvements**. The **Message composer** component now saves drafts automatically when you close the tab or open a different page.

**Column population**. Creatio now populates system columns, columns that have default values, and linking columns automatically when you add records.

### Communication panel in Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-11 "Direct link to Communication panel in Freedom UI")

**UX improvements to the active call indicator**. The active call indicator that appears when the phone panel is minimized now displays the call length.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-12 "Direct link to Out-of-the-box Creatio solutions")

### Case management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-13 "Direct link to Case management")

**New app**. New **Case management** composable app was released. It provides intelligent, full-cycle service management capabilities that enhance processes related to service delivery, customer interaction, feedback tracking and analysis, agent performance monitoring, and more in Freedom UI.

Use the app to manage cases, services, and service agreements. The classic **Cases**, **Service**, and **Service agreements** sections in existing workplaces are replaced with their **Case management** app counterparts in new Creatio instances out of the box. The app is included in Service enterprise and Customer Center products.

Case management app

![Case management app](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_8/scr_case_management.png)

### Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-14 "Direct link to Creatio Marketing")

**UTM marks**. You can now use UTM marks to track lead channel, source, campaign, and bulk email for records of the "Submitted forms" object.

### Financial services Creatio [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-15 "Direct link to Financial services Creatio")

**Freedom UI**. Freedom UI is now available in the entire product lineup of Financial services Creatio.

**Active consultation indicator**. The Freedom UI shell now displays the consultation indicator if you go to a different communication panel tab or minimize the panel while performing a consultation. The indicator displays the contact name as well as duration of the consultation. Click the indicator to reopen the consultation panel.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-16 "Direct link to Development tools")

**Changes of the app primary package**. You can now change the primary package that stores the app properties in the app-descriptor.json file for apps that comprise multiple packages. To do this, create a lookup for the "Package in installed application" object, filter the app packages, and select the "Primary" checkbox for the needed package.

Apps can only have a single primary package. You can set only unlocked packages as primary or secondary. Learn more in a separate article: [Primary app package](https://academy.creatio.com/documents?id=2419&anchor=title-3990-3).

**Streamlined development of custom Freedom UI components**. You can now create converters within the remote module. This lets you use these converters in business logic defined within the remote module. Previously, you could only create converters in schemas. Learn more in a separate article: [Custom converter implemented using remote module](https://academy.creatio.com/documents?id=15035).

### Mobile App [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-18 "Direct link to Mobile App")

**Object-level business rules support**. Creatio mobile app now supports the operation of object-level business rules both online and offline.

## Beta testing of new features [​](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes\#title-2610-17 "Direct link to Beta testing of new features")

Important

The features below are available for beta testing in Creatio version 8.0.8 Atlas. To evaluate new capabilities of the Freedom UI Designer, enable the corresponding feature in a test environment yourself by using [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or request the Creatio support to enable the feature. Contact us if you have any feedback, we appreciate it: `beta@creatio.com`.

**Limits to primary communication options**. Creatio now sets only the first communication option added to contact or account as primary automatically. The value of the primary communication option is synchronized with the value of the corresponding object field if available. Communication options of the same type that are added later are not set as primary. Enable the "CommonCommunicationsBehavior" feature to take advantage of this mechanism.

**Improved feedback collection mechanism**. To ensure the case feedback you collect is left by customers instead of spam filters, the feedback collection mechanism was overhauled using the new **#@Invoke.EstimateLinkGenerator#** macro. The macro adds a link to the feedback collection page that includes the grading scale and comment field. The new mechanism works for both classic Creatio Service products and **Case management** app. Enable the "EstimationWithNoSubmitting" feature to take advantage of this mechanism.

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-1)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-6)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-7)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-8)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-9)
  - [Freedom UI sections](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-10)
  - [Communication panel in Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-11)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-12)
  - [Case management](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-13)
  - [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-14)
  - [Financial services Creatio](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-15)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-16)
  - [Mobile App](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-18)
- [Beta testing of new features](https://academy.creatio.com/docs/8.x/resources/release-notes/808-atlas-release-notes#title-2610-17)