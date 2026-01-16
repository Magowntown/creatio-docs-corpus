<!-- Source: page_21 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 04/21/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with the following **new features** included in Creatio version 8.0.1 Atlas.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

[![tech_hour](https://academy.creatio.com/sites/en/files/images/Release_notes/tech-hour-rn_bg_small.jpg)](https://www.youtube.com/watch?v=6JiiXjeq-CI)

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-1 "Direct link to No-code platform")

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-4 "Direct link to Freedom UI Designer")

#### Dashboards [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-6 "Direct link to Dashboards")

- It is now possible to add "Gauge" type charts to pages.
- You can filter chart and metric data by the parameters of the dashboard location page. This lets you display only the data relevant to the current record on the chart. For example, the partner page can include a histogram that displays the sales dynamics of the partner or top 5 open deals. The value filtering is available for all chart types except pipelines.

#### Slider [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-7 "Direct link to Slider")

- New "Slider" element was added. Use the element to display a number within a range and slide it up and down with a preset step value. For example, below is the slide for a product that can be ordered in the quantity from 10 to 100 and increment of 5. You can set the minimum and maximum data values as well as the step value in the slider settings.

Set up a slider

![Set up a slider](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_1/scr_slider_setup.png)

#### Tabs and expansion panels [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-27 "Direct link to Tabs and expansion panels")

- Inner layout management options were added to tabs and expansion panels: column number, background color, margins, etc.

#### Action dashboard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-28 "Direct link to Action dashboard")

- It is now possible to specify all available user actions in the action dashboard settings: call, email, feed message, or task.

Set up an action dashboard

![Set up an action dashboard](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_1/scr_actions_dashboard_settings.png)

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-27 "Direct link to Business processes")

#### Process step prediction [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-11 "Direct link to Process step prediction")

- An innovative AI suggestion mechanism was added to the Process Designer. The mechanism speeds up the setup of the process diagram for experienced users and improves the learning curve for new users. It works by displaying a menu with potential further process steps as you add elements to the working area of the Designer. The suggestion mechanism generates recommendations for each user individually based on their previous decisions as well as best practices for business process setup in Creatio. The AI prediction model for process step prediction comes pre-trained and ready for use out-of-the-box.

Process step suggestions

![Process step suggestions](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_1/scr_future_elements_prediction.png)

#### Sub-process execution [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-12 "Direct link to Sub-process execution")

- **Sub-process** element can now be run in the background. This lets you keep working on the case or business process without the need to wait until Creatio runs the needed actions.

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-13 "Direct link to Integrations")

#### Integration with REST services [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-14 "Direct link to Integration with REST services")

- You can now use the XML request body when setting up REST protocol integrations. The new mechanism lets you pass the XML request body to the REST request body as well as receive and process the XML response.

#### Email Listener setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-16 "Direct link to Email Listener setup")

- The Exchange Listener service that synchronizes Creatio with email providers was renamed to Email Listener.
- You can check the health of mailboxes that use OAuth authentication on the diagnostics page of the Email Listener microservice.

## Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-9 "Direct link to Base interface and system capabilities")

### Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-39 "Direct link to Freedom UI")

#### List setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-5 "Direct link to List setup")

- You can customize list columns while working in an app.
- Creatio saves the list settings in the user profile, therefore the settings are applied every time you open an app.
- You can restore the default settings in a single click via the **Reset to default settings** button.

Set up a list

![Set up a list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_1/gif_list_settings.gif)

#### Favorite folders [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-41 "Direct link to Favorite folders")

- It is now possible to add folders to favorites. Creatio displays the index of favorite elements in the folder tree.

#### Data management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-28 "Direct link to Data management")

- The button that adds bound records displays the selection menu if different record types use different pages.
A button that displays the menu

![A button that displays the menu](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_1/scr_add_record_menu.png)

- The loading time of Freedom UI pages, including the navigation between tabs and folders, was improved.


### Meeting and task synchronization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-42 "Direct link to Meeting and task synchronization")

#### Exchange calendars [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-44 "Direct link to Exchange calendars")

- Fault tolerance of the mechanism that synchronizes calendars with Microsoft Exchange was ensured. If Creatio fails to import meetings, the import is restarted automatically.
- Creatio uses only the main Exchange calendar (default calendar) for synchronization. The records of additional calendars are not imported. Learn more about setting up the default calendar in [Microsoft documentation](https://support.microsoft.com/en-us/office/set-default-calendar-7c546486-0c7c-4870-964a-0d6eb4de83e0).

### Email setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-18 "Direct link to Email setup")

#### OAuth authentication [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-46 "Direct link to OAuth authentication")

- If the Access token for Creatio must be updated, the users receive a notification that lists the required steps.

#### Azure security policy [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-47 "Direct link to Azure security policy")

- If your company uses Azure security policy, you can set up the email synchronization after the Azure administrator approves it.

## Out-of-the-box Creatio solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-48 "Direct link to Out-of-the-box Creatio solutions")

### Mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-24 "Direct link to Mobile app")

#### File upload [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-27 "Direct link to File upload")

- It is now possible to upload multiple files from a mobile device simultaneously.

#### Mobile app administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-25 "Direct link to Mobile app administration")

- You can now disable the synchronization on app start.

#### Mobile app development [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-26 "Direct link to Mobile app development")

- The index of error message calls for the functionality implemented using Flutter was expanded.
- Firebase for Android was updated.

### Phone integration and communication management [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-43 "Direct link to Phone integration and communication management")

#### Asterisk PBX [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-20 "Direct link to Asterisk PBX")

note

This functionality is available for beta testing in Creatio version 8.0.1. You can request early access to the new connector features by contacting Creatio support. We appreciate your feedback.

New connector for Asterisk PBX was created.

- Support for Asterisk 16 and 18 LTS versions was implemented.
- The number of Asterisk events required to process calls was reduced, which improves the connector reliability.
- Attended and blind call transfers can be used simultaneously.
- Daily logging that streamlines connector bottleneck tracking was set up. The records are stored in a single directory and sorted by date. This lets you find the needed record quickly, as well as send data only for the period when the connector had issues to tech support.
- Automatic signal reception by the user device was implemented on callback. This lets you start talking to the subscriber immediately after the call.
- The number of permissions the Asterisk integration (AMI User) account requires to manage the Asterisk connector was reduced.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-21 "Direct link to Development tools")

### Change transfer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes\#title-2328-22 "Direct link to Change transfer")

- The automatic addition of package dependencies when you bind data in the **Configuration** section and advanced settings mode of the **Application Hub** was implemented. You can select any objects and their columns regardless of the current dependencies. Creatio adds the needed dependencies automatically after you save the changes.
- The mechanism that adds package dependencies automatically was optimized. Creatio takes the entire package dependency hierarchy into account when you add dependencies. That way, Creatio adds significantly fewer dependencies.

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-1)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-4)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-27)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-13)
- [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-9)
  - [Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-39)
  - [Meeting and task synchronization](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-42)
  - [Email setup](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-18)
- [Out-of-the-box Creatio solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-48)
  - [Mobile app](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-24)
  - [Phone integration and communication management](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-43)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-21)
  - [Change transfer](https://academy.creatio.com/docs/8.x/resources/release-notes/801-atlas-release-notes#title-2328-22)