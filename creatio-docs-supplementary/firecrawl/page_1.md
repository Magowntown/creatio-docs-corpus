<!-- Source: page_1 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 01/11/2021

At Creatio we are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.17.1.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-1650-1 "Direct link to Creatio Marketing")

### Campaigns [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-13 "Direct link to Campaigns")

- Campaign participants can now be added from various Creatio objects, e.g. leads, cases, accounts.
Adding campaign audience from a lead

![Adding campaign audience from a lead](https://academy.creatio.com/docs/sites/en/files/2020-12/add_audience.png)

- Campaign participant data can be used in macros in email templates, as well as in filters in conditional flows.


### Email marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-2 "Direct link to Email marketing")

- A new "Sending progress" dashboard tab has been added to the **Email** section. It is used to display data for all emails sent within the past 72 hours: email start time and total number of recipients, whose emails were prepared or processed.

- The **Sending progress** tab has been added to the email page. It displays the current email status, the bottlenecks and the sending duration, initial provider responses and issues that occur during sending.
The Sending progress tab on an email page

![The Sending progress tab on an email page](https://academy.creatio.com/docs/sites/en/files/2020-12/sending_progress_on_page.png)

- You can now successfully start the trigger emails that were sent more than 6 hours ago.


## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-3 "Direct link to Creatio Sales")

- When working with one forecasting time period on a forecasting tab, the "Total" block on the right handside of the tab is hidden. When working with two or more time periods, the "Total" block is visible again.

- Improved forecast setup UI. General and automation forecast settings are located under separate tabs.
The updated UI for the forecast setup

![The updated UI for the forecast setup](https://academy.creatio.com/docs/sites/en/files/2020-12/edit_forecast_automation.png)

- Forecast tab versions have been improved. When viewing different versions of the forecast, you can only see the rows that were relevant at the time when the version was saved. The rows that were added later are not displayed. The rows that are not included in the last forecast version are grayed out.
Example of a forecasting tab version

![Example of a forecasting tab version](https://academy.creatio.com/docs/sites/en/files/2020-12/forecast_period.png)


## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-4 "Direct link to Core functions")

- You can do formula calculations in date type columns in pivot tables. This will allow a user to calculate e.g., the planned date of closing a case or the actual time of processing a case in days.

- Users will now receive notifications when a new feed message has been added to section records that they are following.

- You can now set up AI models to search for similar objects. The models can search for similar Creatio objects using unstructured text data. Use this functionality to search for similar cases, automatically select the knowledge base articles or most relevant answers, etc.
Example of setting up a recommendation model

![Example of setting up a recommendation model](https://academy.creatio.com/docs/sites/en/files/2020-12/similar_case_model.png)

- Added Telegram customer communication channel. All messages sent to the Telegram channel configured in Creatio will be available for processing by agents in the communication panel. Use "Chats settings" available in the System Designer to add and set up the new channel.
Processing Telegram chat messages in the communication panel

![Processing Telegram chat messages in the communication panel](https://academy.creatio.com/docs/sites/en/files/2020-12/telegram_chat_enu2.png)


## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-5 "Direct link to Integrations")

- When synchronizing activities, Creatio now processes private meetings from Exchange and Google calendars. The captions of the corresponding activities will be set to "Private meeting." Names and descriptions of the private meetings are not imported to Creatio.
- We have changed the redirection address for registering Creatio in GSuite to synchronize with Google calendars and contacts. To ensure the correct synchronization, create a new OAuth 2.0 client ID and perform the setup. Read more in the [Register Creatio application in Gsuite](https://academy.creatio.com/node/191) article.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-6 "Direct link to Business processes")

- You can now work with files using a new business process element. Use newly added **Process file** business process element to read and copy files available on any **Attachments and notes** detail. The system creates a collection that can be later used in the process. For example, these files can be added as attachments when using **Send email** process element.

This element can only work with files stored in the application database. If you store your files in a third-party repository (a file system or the cloud), the element will not process them. We will provide an API to work with files from the third-party repositories in the upcoming releases.
Example of using the \[Process file\] element

![Example of using the [Process file] element](https://academy.creatio.com/docs/sites/en/files/2020-12/process_file_element.png)

- A new "File" process parameter has been added. This parameter stores information about the file and enables passing this information between process elements and between business processes.

- The **Send email** element can now add attachments to outgoing emails. To use this, add the parameter to the element and specify the needed files as the data source. Use the **Process file** element to receive the list of files.

- You can now receive one or more resulting parameters when starting interpreted business processes from the client JS module or a C# code.


## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-7 "Direct link to User customization tools")

- You can now create custom lookup fields based on database views using no-code tools. Examples of views include company structure and business process library.

- The following features are now available in the Section Wizard to accelerate and simplify the detail setup:
  - Create an object for a new detail and register the detail for the created object.
  - Create a detail based on the existing Creatio object.
  - Create a lookup column that would connect the new detail to the configured page.
  - Open the Detail Wizard from a detail property window to set up the detail. If you do not close the property window that you used to open the Detail Wizard, the detail name and the columns will display right away after you save the changes in the Detail Wizard.
  - When specifying the connection fields for the columns, the available values are now filtered by lookups linked to these fields. If the connection exists between the page and the detail, Creatio will suggest establishing such connection automatically.
- When setting up page tabs in the Section Wizard and the Pre-configured Page Designer, you can edit the tab code while creating it.

- You can now specify the UI element captions in different localizations in the Section Wizard and the Pre-configured Page Designer. This option is available for the tab captions, detail captions and the connection lookup columns. In the Pre-configured Page Designer, this option is also available for buttons.

- In the "Set field value" business rule, you can now use formulas with date fields. Use this to calculate the task completion time, next invoice payment date, etc.
Example of setting up a business rule for calculating a time period

![Example of setting up a business rule for calculating a time period](https://academy.creatio.com/docs/sites/en/files/2020-12/gif_bus_rule_set_field_value%20%28002%29.gif)


## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-8 "Direct link to Administration")

- When managing objects by records is disabled, the change log settings remain unaffected.
- For the .Net Core applications, we have enabled installing a Marketplace app using the standard download UI without downloading a file.

### License manager [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-9 "Direct link to License manager")

- You can now work with server licenses in the License Manager.
Example of displaying server licenses

![Example of displaying server licenses](https://academy.creatio.com/docs/sites/en/files/2020-12/license_manager_enu.png)

- You can now delete all licenses.

- To make licensing more convenient, we have added license request and upload buttons to the action menu.


## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-10 "Direct link to Development tools")

- When working with SelectQuery in Data Service, you can now filter records by current user inclusion in a role: direct membership, delegation, manager inheritance, hierarchy inheritance, etc.

### Advanced settings [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes\#title-3011-11 "Direct link to Advanced settings")

- Package Dependency diagram is now available in the Configuration section under "Actions."
- Enabled working with metadata in the updated **Configuration** section. You can open the metadata from the element action menu or the schema action menu.

- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-1650-1)
  - [Campaigns](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-13)
  - [Email marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-2)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-3)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-4)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-5)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-6)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-7)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-8)
  - [License manager](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-9)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-10)
  - [Advanced settings](https://academy.creatio.com/docs/8.x/resources/release-notes/7171-release-notes#title-3011-11)