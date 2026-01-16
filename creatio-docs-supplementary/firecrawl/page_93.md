<!-- Source: page_93 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 12/26/2024

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code development, and modern CRM. Today we are advancing new forms of innovation with Creatio version 8.2.1 "Energy," featuring the **following new capabilities and enhancements**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio AI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-114 "Direct link to Creatio AI")

**Account data enrichment**. You can now enrich account data using internet-sourced information automatically, including email, phone, website, and address, using the new **Enrich Account Data** AI Skill. This functionality requires Bing Search API key.

**Meeting agenda**. It is now possible to generate a meeting agenda based on your input, including relevant topics, discussion points, and estimated durations, using the new **Prepare meeting agenda** AI Skill.

**Meeting preparation**. It is now possible to gather relevant information and talking points based on the meeting attendees and purpose using the new **Prepare for the meeting** AI Skill.

**Personalize lead call script**. You can now personalize call scripts based on lead profiles and preferences using the new **Generate lead call script** AI Skill.

**Debug information in chat**. You can now view debug information by clicking the **Debug info** button in Creatio AI chat. This lets you see all technical message exchanges in real time, facilitating in-depth analysis and troubleshooting of AI interactions.

**Enhanced actions**. It is now possible to integrate existing business processes and remove any unused actions while editing Creatio AI Skills effortlessly.

**Names in Creatio AI**. Creatio AI actions, action parameters, and skills now have names. This lets you call actions more precisely, making it easier to specify and execute them accurately.

**Creatio AI token balance**. You can now check the balance of your Creatio AI tokens in the **Creatio AI Dashboards** section.

**Search for AI Skill**. You can now search for AI Skills in the **Creatio AI setup** section.

**AI Skill guidelines**. You can now create AI Skills quicker and easier by following tips and best practices directly on the AI Skill page.

**Sample prompts**. You can now create more effective prompts easier using the sample prompt in the AI Skill Designer.

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-1 "Direct link to Creatio composable apps")

### Email Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-119 "Direct link to Email Marketing")

**Email Marketing out of the box**. The Email Marketing app is now available out of the box in all Creatio products or bundles where Creatio Marketing is included.

**Autosave in the Email Designer**. Email Designer now saves all your changes automatically.

**Name updates**. **Category** field is now called **Sending Method**. “Bulk Email” lookup value is now called “Manual at Optimal Time.” “Trigger Email” lookup value is now called “Using a Campaign Flow.” These changes only affect new Creatio instances.

## End user experience [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-18 "Direct link to End user experience")

### UX enhancements [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-8 "Direct link to UX enhancements")

**Element visibility**. Highlighted elements are now better visible when you work with the page using the keyboard. This includes buttons and the navigation menu.

**Improved page UX on keyboard**. When you navigate between Freedom UI pages, the focus automatically goes to the main page.

**UX improvements for navigation panel**. You can now operate the Creatio navigation panel using the keyboard or mouse wheel. Click the middle mouse button to open the section in the new browser tab.

**Browser tab titles**. You can now better distinguish among multiple open Freedom UI Creatio tabs as the browser tab titles now match the page content.

**Email activities in the Next steps component**. When you create an activity that has the “Email” category, the **Next steps** now shows you the email page when you try to complete the activity.

Email window

![Email window](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/gif_email_window.gif)

**Classic UI approvals in the Next steps**. You can now view pending approvals stored in the Classic UI in the **Next Steps** on Freedom UI pages as well.

**Line breaks in plain text emails**. Plain text emails in the **Timeline** component now have line breaks.

**Next Best Offer**. **Next Best Offer** is now available out of the box on contact and account pages for new Creatio instances. For existing Creatio instances, toggle the component using the “Show Next Best Offer component in Contacts form page (freedom UI)” (“ShowNBOInContactPage” code) and “Show Next Best Offer component in Accounts form page (freedom UI)” (“ShowNBOInAccountPage” code) system settings, respectively. The **Next Best Offer** component is now also available in Freedom UI Designer. Learn more: [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-10).

**UX improvements for Hierarchy**.

- The hierarchy now includes virtual scrolling. This lets you navigate through large datasets seamlessly with faster performance.
- The hierarchy now supports lazy loading. 30 items load first and 30 more are loaded later as you scroll through a large dataset.

### WCAG compliance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-15 "Direct link to WCAG compliance")

**Keyboard controls for components**. You can now control **Next Steps**, **Feed**, and **Message composer** significantly better via keyboard. Also, the **Message composer** has a new shortcut. Press Delete on the recipient to remove them.

**Widgets**.

- The charts are now significantly better to control via keyboard. Use Tab to move among the chart elements, up and down arrows for the series, and right and left arrows for the values. Press Enter on a chart legend to view the context menu. Press Esc to hide a chart tooltip. You can also hold the pointer over the entire tooltip area without it disappearing.
Keyboard accessible widget

![Keyboard accessible widget](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/gif_wcag_charts.gif)

- Dividers were added between chart series or values, for example, in areas, stacked bars, doughnuts, and pipelines.

- Widgets now have more accessible colors. More colors were added to the color picker as well.

- The clickable area of line, area, bar, and column charts was increased to make controls easier to activate.


**Accessible desktop color**. It is now possible to set accessible desktop color that displays instead of the background image. You can turn on the accessible color in the user profile settings if it is set up.

Accessible desktop color

![Accessible desktop color](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/scr_accessible_color.png)

**Skip links in Freedom UI**. You can now transition to the navigation or main content area of the page swiftly using skip links.

**List**.

- Focused elements in the list can no longer be obscured because of a pinned column. The list will scroll to show you the focused element.
- Move out of a list on keyboard. When you move focus through the page the list itself will be focused first. Press Enter to start interacting with its elements or just move focus further through the page. When you are interacting with the list press Esc to move focus out of the list.
- Change the column width using a keyboard. Select the width line using Tab and press Right arrow or Left arrow to increase or decrease the width.
- The clickable area of buttons inside the list was increased to make them easier to activate.

**Rich text**. Toolbar button readability in the component was improved.

**Buttons**. Buttons in any configuration now have accessible names.

**Tooltips**. You can now press Esc to hide a tooltip.

**Toggle buttons**. Screen reader or other tools can correctly describe the status of the button toggle group using the new “Pressed” status.

**Menu items**. You can now press Space or Enter to activate a menu item action. If the item does not have an action but has a submenu, a submenu opens. If neither applies, the buttons do nothing.

**Top panel**.

- Top panel titles were corrected for screen readers.
- Changing the focus using Tab is now more intuitive in the top panel.

**Expanded pages**. Expanded pages are now holding the keyboard focus inside the expanded area. This keeps the focused element visible.

**Links**. Most links are now underlined out of the box. They can be underlined only on hover or not underlined at all where they do not violate any of the WCAG criteria.

**Controls inside inputs**. The clickable area of controls inside inputs was increased to make them easier to activate.

**Screen readers**.

- Screen readers are now quiet during loading masks in Freedom UI.

- Screen readers now announce the following:
  - mini page titles
  - message texts in the **Message composer** component
  - message texts in the **Timeline** component
  - message texts in the **Next Steps** component
  - message texts in the **Feed** component
  - image titles in **Contact compact profile** and **Account compact profile** components based on the corresponding field titles of related objects
  - title of the filter setup button in the **Search** component
  - all possible translations in the multilanguage component using the correct language options

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-9 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-2 "Direct link to Application Hub")

**Enhanced app properties**. You can now view dependencies between applications on the new **Dependencies** tab of the application properties window. You can view inherited replacing Freedom UI pages from multiple applications and save the pages into a single app package, which ensures consistency and helps with organization.

App dependencies

![App dependencies](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/scr_app_dependencies.png)

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-3 "Direct link to Business rules")

**Business rule debugging**. You can now debug business rules using messages in the browser console.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-10 "Direct link to Freedom UI Designer")

**Next Best Offer**. You can now tailor product recommendations for an account or contact using the new **Next Best Offer** component. The component is powered by an ML model and displays personalized product or service recommendations based on customer preferences, behaviors, and purchase history. You can apply additional filters by page data or specific criteria like Account or Contact for even more tailored recommendations. The component UX also has special features. Learn more: [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-8)

Next best offer component

![Next best offer component](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/scr_next_best_offers.png)

**Multiselect lookup**. You can now select multiple items from a dropdown list and display them as a chip list using the new **Multiselect lookup** component. This is useful for implementing many-to-many relationships where you need to select and visually manage multiple values as well as for cases where you need to display only one column from the selected object.

Multiselect lookup component

![Multiselect lookup component](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/scr_multi-select.png)

**New button action**. You can now add an Office 365 or Google calendar to synchronize automatically using the new **Add calendar synchronization account** button action.

**Save data on process start**. You can now save page data before starting the business process using the **Run process** button action.

### Business processes​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-11 "Direct link to Business processes​")

**New business process element**. You can now seamlessly integrate Creatio AI Skills into your business process without writing a single line of code using the new **Call Creatio AI** business process element. Learn more: [Handle system-level data using Creatio AI in the business process](https://academy.creatio.com/documents?id=15157&anchor=title-15157-14).

**Loading mask for business processes**. “Run process” action in Freedom UI now gives you information that Creatio is busy by displaying loading mask for processes that do not start in the background and need some time to show the process page.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-12 "Direct link to Integrations")

**Identity Service on .NET 8**. Identity Service that enables Creatio with OAuth authorization functionality is now available on .NET 8 framework. .NET 6 Identity Service is now deprecated.

**OAuth state checkup**. You can now check the state of the OAuth functionality on the **Diagnostics** tab of the OAuth list page. You can check whether all components are configured properly, view detailed error description as well as hints on how to fix issues.

OAuth diagnostics

![OAuth diagnostics](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_2_1/scr_oauth_diagnostics.png)

**Streamlined connection to Identity Service**. You can now set up the connection to Identity Service right from the OAuth list page. To do that, open the **Diagnostics** tab → **Open settings** and fill out the form. Before saving the settings you can check that the values you filled out are correct using the **Test connection** button.

**Enhanced error handling for Telegram chat channels**. You will now receive a notification if a Telegram channel that has webhook integration enabled fails to receive messages. The following updates appear for users that have access to the **Chat settings** section:

- Error notification appears in the notification sidebar.
- Error icon is displayed in the **Chat channels** list
- Notification appears if you attempt to add a new Telegram channel while webhook integration is already enabled.

**New IMAP synchronization policy**. Email Listener microservice now has a lighter load for the IMAP email synchronization.

### Mobile [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-16 "Direct link to Mobile")

**Quick filters in the mobile app**. You can now create your own filters in the mobile app using no-code customization. Configure individual filters for each user to apply on their own or set up predefined filter sets to apply them to all users quickly.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-13 "Direct link to Advanced customization")

**List data source removal**. Creatio now deletes the list data source from the current page schema automatically if the **List** component was deleted in the Freedom UI Designer. Learn more: [List component](https://academy.creatio.com/documents?id=15098&anchor=list-data-source-removal).

**Removal of ViewModel and DataModel attributes**. Creatio now removes `ViewModel` and `DataModel` attributes automatically when you remove an input control in the Freedom UI Designer. During the removal Creatio checks the usage of these attributes in the `handlers` schema section and business rules of the current Freedom UI page. Learn more: [Freedom UI page schema](https://academy.creatio.com/documents?id=15342&anchor=removal-of-attributes).

**Notification mark for toggle panel**. You can now configure notification mark for tab of toggle panel in the Freedom UI page schema. Learn more: [Customize toggle panels](https://academy.creatio.com/documents?id=15175&anchor=display-a-notification-mark).

**Rename code of localizable resource**. Creatio now renames code of localizable resource if the element code was renamed in Freedom UI Designer. Learn more: [Freedom UI page customization basics](https://academy.creatio.com/documents?id=15370&anchor=rename-element-resource).

## Administration​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-14 "Direct link to Administration​")

**.NET 6 deprecation**. Since Microsoft ended official support for .NET 6 in November 2024, starting from version 8.2.1 Creatio no longer supports .NET 6 and switches to .NET 8.

**Optimized large emails in Classic UI cases**. Now you will only see a text preview for emails larger than 50 KB in Classic UI case history. View the full email by opening it directly from case processing.

**Improved logging performance**. Creatio now uses asynchronous log writing approach that enables it to write logs to the database faster and without influencing other Creatio subsystems.

**Improved page loading time**. Page loading time was improved by optimizing how RequireJS loads modules.

**Performance of configuration validation**. Configuration validation is now faster.

**Performance of Next Steps component**. The component now performs faster.

**Performance of Progress bar component**. The component now performs faster, which lets you work with cases on Freedom UI record pages faster.

## Beta testing of new features​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes\#title-2782-17 "Direct link to Beta testing of new features​")

Important

The features below are available for beta testing in Creatio version 8.2.1 Energy. If you have any feedback, contact us at: `beta@creatio.com`. All feedback is appreciated.

**Creatio AI on mobile**. It is now possible to use Creatio AI in the mobile app. You can use your voice to interact with AI, saving time on typing messages.

To turn this functionality on, contact [Creatio support](mailto:support@creatio.com).

**No-code calculations in business rules**. It is now possible to set up calculations in Set Value business rule for actions with numeric fields using a brand new no-code Formula Designer. You can use basic arithmetic operations with attributes of a single page data source. The formula arguments must also be added to conditions.

To activate the functionality, turn on the "BRules-EnableFormulaForSetValueAction" feature. Learn more: [Manage an existing additional feature](https://academy.creatio.com/documents?id=15631).

- [Creatio AI](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-114)
- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-1)
  - [Email Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-119)
- [End user experience](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-18)
  - [UX enhancements](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-8)
  - [WCAG compliance](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-15)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-9)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-10)
  - [Business processes​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-11)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-12)
  - [Mobile](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-16)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-13)
- [Administration​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-14)
- [Beta testing of new features​](https://academy.creatio.com/docs/8.x/resources/release-notes/8-2-1-energy-release-notes#title-2782-17)