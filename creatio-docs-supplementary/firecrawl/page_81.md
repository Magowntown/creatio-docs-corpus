<!-- Source: page_81 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 02/01/2021

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.17.2.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-1 "Direct link to Creatio Marketing")

-  Import of the event audience has been improved: you can add several records manually from a folder or using a custom filter.
Event audience import

![Event audience import](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/gif_add_audience_to_event_ENU.gif)


### Campaigns [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-2 "Direct link to Campaigns")

- Updated the logic of adding participants to campaigns.
  - Participants are added from landings and events by signal, and not at the start of a new campaign execution period.
  - The **Add from landing** and **Add from event** elements can only be used as start events.
  - All the elements that enable adding participants by signal allow the participants to re-enter a campaign.
- You can now use a new element to populate the event audience from campaign.
Updated campaign elements

![Updated campaign elements](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/new_campaign_element_example_ENU.png)

- You can now view the total number of participants on every campaign step. To do this, use the new "History" counter that was added to campaign diagrams.


### Email marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-3 "Direct link to Email marketing")

- You can now use the "-" symbol in utm-marks.
- Bulk emails scheduled for sending in several minutes cannot be sent manually any more.

## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-4 "Direct link to Creatio Sales")

- You can now drill down the data used to receive the calculated forecast metrics. Click a forecast record to display a window with the list of source data. You can set up columns for the list, and export data to Excel.
Source data of a calculated forecast metric column

![Source data of a calculated forecast metric column](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/gif_forecast_details_ENU.gif)

- You can now open section records used to calculate the forecast from the drill down list. This feature is only available for beta-testing in Creatio 7.17.2. If you are interested in testing out this feature, you need to contact Creatio support. The new feature will be available in the upcoming Creatio releases.


## Creatio Service [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-5 "Direct link to Creatio Service")

- Implemented AI search for similar cases, which increases the support team efficiency. If you have more than 100 processed cases in Creatio, the out-of-the-box recommendation model will be automatically trained and will predict siimlar case recommendations for all new cases. The search results will display on the **Similar cases** detail. If either the case description or subject has been changed, you can run additional similar case search.

Additional search for similar cases

![Additional search for similar cases](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/search_for_cases_again_ENU.png)

## Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-6 "Direct link to Base interface and system capabilities")

### Chats [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-7 "Direct link to Chats")

- Paste an image in a chat from the clipboard using the Ctrl + V hotkey command.

- Utilize templates for quick replies.

  - Use the ![](https://academy.creatio.com/docs/sites/default/files/images/Release_notes/release_notes_7_17_2/btn_chat_templates.png) button to select the template in a chat window. You can edit the text before sending your reply.
  - You can personalize the templates using macros to add the agent or customer data.
  - The "//" command enables an agent to find the necessary template easily. To search for a template, use the template name or template text.
  - Use the "Message templates" section to add new or edit existing templates.
  - Implemented multilingual chat templates. In the chat channel, specify the language to be used in reply templates that will be available for the agent. If on the contact’s page the preferred language is selected, then reply templates will be available in that language. If the preferred language is not specified on the contact page, nor is set for the channel, the template available will be in the language specified in the "Default language for messages" system setting.
- You can now change the agent status in the communication panel.
Agent status in the communication panel

![Agent status in the communication panel](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/change_chat_operator_status_ENU.png)


## Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-8 "Direct link to Mobile application")

- You can now work with approvals in the hybrid mode. The list of approvals and approval processing is available regardless of the connection to the main application. All the changes will be passed to the main application when connection is established.

## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-9 "Direct link to Integrations")

- Implemented low-code integration with SOAP services. To set up the integration, upload the WDSL file received on the service side in Creatio. Working with SOAP services is similar to working with the REST services.
- Enabled synchronization with LDAP for Creatio applications deployed on Linux.
- In Net Framework Creatio applications deployed on Windows, LDAP synchronization is based on the secure SSL protocol.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-10 "Direct link to Business processes")

- You can now use the **Process file** business process element to generate custom MS Word reports or Fast Reports. You can add the generated reports to the **Attachments and notes** detail of any record or use it further in the business process, e.g., send it as an email attachment.
- When using lookup values as element or process parameters, the record Id is added to the record macro. This helps to avoid ambiguity if lookups contain several records with the same names.

## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-11 "Direct link to User customization tools")

### Reports [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-12 "Direct link to Reports")

- You can now copy the MS Word reports in Creatio. This allows to save time when setting up similar reports. The report copy will contain the columns, macros, tables, filters and template of the original report. You can also copy just report tables when setting up a new report, which saves time when creating reports with similar tables.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-13 "Direct link to Business rules")

-  Implemented the "CurrentDateTime" function in the "Set field value" business rule. It is used when you need to set a future date based on the current date, e.g., the planned task completion time, the date of next opportunity verification, etc.

### Section Wizard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-14 "Direct link to Section Wizard")

- You can now add tips to fields in the Page Designer.
  - Tips are localized, so you can use any Creatio language for creating them.
  - HTML formatting is also available for tips. To use it, apply HTML markup when entering the tip text.
- For pages created or edited using the developer tools, you can now apply changes of the date formats, precision, string length, etc. when working in the Section Wizard.

- You can now add details for new Creatio objects in the Detail Wizard directly.

- You can set up details with editable lists when creating details using the Detail Wizard.


## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-15 "Direct link to Administration")

- Added notifications about expiring licenses. System administrators will see a notification in their communication panel if the application licenses are not available or not sufficient for the new period. By default, the notifications appear one day in advance before the current licenses expire. You can set up a custom notification alert period using the "ExpireLicenseNotificationTerm" system setting.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-16 "Direct link to Development tools")

- We have added API for working with files, enabling Creatio integration with third-party file storages, e.g., file systems, cloud repositories, etc.
- DataService implemented a restriction that blocks delete requests without filters. This protects Creatio from deleting all table data by mistake.

### Advanced settings [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes\#title-3081-17 "Direct link to Advanced settings")

- In the **Advanced settings** section, you can now manage blocking packages and SVN elements. Additional action added for this purpose.

- You can edit the incorrect metadata in the updated **Advanced settings** section.

In the schema list, you can now use the function of multiple selection. The following actions for multiple records are available:
  - delete;
  - export;
  - generate source codes;
  - migrate elements;
  - update database structure;
  - install data;
  - install SQL scripts.
- You can now view the source code of business processes, "User actions" elements and objects. To view the source code, select the necessary option of the element actions in the **Advanced settings** section.
View a source code

![View a source code](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes%207_17_2/gif_open_bp_source_code_ENU.gif)

- You can manage the client module parameters in the **Advanced settings** section.

- You can check the available conflicts by dependencies that may appear after you migrate elements between packages. Use the **Validate dependencies between elements** action in the **Advanced settings** section.

- In the data binding designer, you can now search for elements by ID, and by all fields of the GUID type.

- You can migrate schemas between packages. The migration is available for the selected elements, as well as for the whole package content.

- Implemented verification of the unique schema names within a package when performing development in the file system.


- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-1)
  - [Campaigns](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-2)
  - [Email marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-3)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-4)
- [Creatio Service](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-5)
- [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-6)
  - [Chats](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-7)
- [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-8)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-9)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-10)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-11)
  - [Reports](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-12)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-13)
  - [Section Wizard](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-14)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-15)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-16)
  - [Advanced settings](https://academy.creatio.com/docs/8.x/resources/release-notes/7172-release-notes#title-3081-17)