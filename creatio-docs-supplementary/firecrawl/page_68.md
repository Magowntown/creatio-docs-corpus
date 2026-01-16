<!-- Source: page_68 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 05/25/2020

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.16.1.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-1 "Direct link to Creatio Marketing")

- We have fixed the issue that caused the tasks added on the **Activities** detail of a marketing activity page to display on the **Email** detail as well.

## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-2 "Direct link to Creatio Sales")

- We have improved the UX of field visit planning in the Field sales and Field module for Creatio applications. You can now plan visits directly in the activity list or the calendar view without having to open the **Visit scheduling** view.

### Forecasts [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-3 "Direct link to Forecasts")

- You can now add multiple records to a forecast using the **Select all** action.
- You can now "pin" the **Total** column of a forecast. To pin the column, click ![forecasts_pin_totals.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/forecasts_pin_totals.png) next to the column name.
- Forecast strings can now be deleted.
- You can edit the forecast name and hierarchy after you save the forecast.

Editing the forecast hierarchy

![Editing the forecast hierarchy](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/modifying_forcast_hierarchy.gif)

## Creatio Service [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-4 "Direct link to Creatio Service")

### Cases [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-5 "Direct link to Cases")

- We have improved the UX of case messaging on the **Processing** tab by making internal and external communications visually different. Internal communications, such as feed messages, mailing between employees, and messages that are not available on the portal are highlighted in blue.
Internal and external case messages on the Processing tab

![Internal and external case messages on the Processing tab](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/case_processing_messages_view.png)

- You can now view sender and recipient addresses by clicking **Details** in emails displayed on the **Processing** tab of a case page.
Viewing the email addresses of senders and recipients in a case message

![Viewing the email addresses of senders and recipients in a case message](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/case_processing_email_addresses_view.gif)

- Working with large images in the email body is now more convenient. Click an image to expand it to its full size.

- Dividers in emails now display as dotted lines.

- If an email sender does not have a contact profile photo, the message thumbnail will display the contact’s initials.


## Financial Services Creatio [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-6 "Direct link to Financial Services Creatio")

- You can now copy products along with data on the **General info** tab of the product page, as well as the product conditions. The copied record will use all product details of the initial record, as long as those details are currently valid. Any conditions whose validity date has expired will not be copied. This will speed up the process of populating multiple products with similar parameters.
- You can also copy separate conditions from the **Product details** to a new record.

## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-7 "Direct link to Core functions")

- Searching for values in drop-down lists on record pages, quick filters, etc. has become more convenient. Entering the searched text in a lookup field will first display the values that start with the searched text, then – the values that contain the searched text.
- We have fixed the issue that could sometimes damage large files during the upload to the **Attachments** detail in .Net Core applications.
- We have updated the **Queue object** lookup interface. This lookup is used to set up the list of queue objects and sorting queue records. The lookup is now available in products on the .Net Core platform.
- You can now delete a message draft from the email page. In previous versions of Creatio, you could do it exclusively from the **Email** tab of the communication panel. You can only delete a draft that is not connected to any business process.
- We have fixed an error with opening the **HTML** element property setup area when working with emails.

### Predictive analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-8 "Direct link to Predictive analytics")

- We have implemented a low-code tool for setting up "recommendation" – a new type of machine learning models. No coding is required for setting up the model parameters, saving the prediction results, and implementing the model via the **Predict data** BPMN process element.
Product recommendation model in a Predict data business process element

![Product recommendation model in a Predict data business process element](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/product_recommendation.png)

- We have added several additional options for machine learning model setup:
  - limit the maximum and the minimum number of records used for model training
  - set an algorithm of selecting values for the classification
  - set possible options for selecting parameters of the recommendation prediction models

### Analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-9 "Direct link to Analytics")

- You can now set up pivot table dashboards. You can group and consolidate data to make your analysis more convenient. New functions for working with data in the pivot tables include calculating the number of unique records and the median. You can convert any "List" dashboard into a pivot table.

Example of a pivot table dashboard

![Example of a pivot table dashboard](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/opportunities.png)

## Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-10 "Direct link to Mobile application")

- You can now work with approvals in the Creatio mobile app. You can now approve or reject records. You can enable section approvals in the Mobile Wizard. Internet connection is required for working with approvals on mobile.

Important

This functionality is only available for beta-testing in Creatio version 7.16.1. You can request early access to the functionality by contacting [Creatio support](mailto:support@creatio.com). We appreciate your feedback! The new feature will be available in the upcoming Creatio releases.

Approval of invoices in the mobile app

![Approval of invoices in the mobile app](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/mobile_application_approving.png)

## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-11 "Direct link to Integrations")

- You can now enable automatic licensing of users when synchronizing with LDAP. To do this, select the **Grant licenses** checkbox on the LDAP integration setup page.
The Grant licenses checkbox on the LDAP integration setup page

![The Grant licenses checkbox on the LDAP integration setup page](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/licensing.png)

- You can synchronize LDAP users by groups. The setting enables you to automatically deactivate users in Creatio, if they were excluded from the corresponding synchronized groups in the LDAP catalog.

- We have implemented synchronizing emails from the shared MS Exchange mailboxes.


## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-12 "Direct link to Business processes")

- You can now no-code tools to handle data collections in Creatio business processes. A collection parameter is passed to a **Sub-process** element, which runs a separate instance of the sub-process per each collection instance.

note

This functionality is only available for beta-testing in Creatio version 7.16.1. We appreciate your feedback! We will finalize the development of the feature in the upcoming releases and it will become fully available for users.

- The direction of process parameters is now visually identified in the setup area: output ![icn_outgoing_process_parameter.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/icn_outgoing_process_parameter.png), input ![icn_incoming_process_parameter.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/icn_incoming_process_parameter.png), bidirectional ![icn_bidirectional_process_parameter.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/icn_bidirectional_process_parameter.png). Displaying the parameter direction makes it easier to map the **Sub-process** element parameters and enables you to see at once which parameters require incoming values, and which are populated after the sub-process instance completes.
Displaying the parameter directions in the sub-process setup area

![Displaying the parameter directions in the sub-process setup area](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/param_direction.png)

- Working with flows in business process diagrams has become more convenient. If you click a flow and drag it to any edge of the element in the process diagram, the flow will draw the optimal path.
Connecting elements using the flows

![Connecting elements using the flows](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/flows_positioning.gif)

- If you import a BPMN process diagram from Studio Creatio, free edition, the imported process will include a link to its description in Studio free, providing additional information for post-import setup. You can also edit the process description link in the setup area in the Process Designer.


## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-13 "Direct link to User customization tools")

- We have updated the UI in the **Report setup** section. You can open the section from the System Designer or the **Printables** lookup.

- The following new features are now available in the UI of the **Report setup** section:
  - A quick search for the report template by name.
  - Updated UI for downloading report templates for editing, as well as uploading the configured templates to Creatio. You can import and export report templates by clicking **Download file** or **Upload file** on the report page.
  - Added several hints on populating the report setup page, as well as quick access to the " [The MS Word printables setup](https://academy.creatio.com/documents/administration/7-15/ms-word-printables-setup)" guide.

A report page in the new UI

![A report page in the new UI](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.1/BPMonlineHelp/release_notes/download_file.png)

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-14 "Direct link to Administration")

- Creatio Marketing now supports .NET Core. You can learn more about Creatio support of the .NET Core platform in the " [Creatio on the .NET Core platform](https://academy.creatio.com/documents/creatio-net-core-platform)" article.
- Fixed several issues with the SQL Azure database deployed on the Microsoft Azure cloud platform. The error was caused by the change of Azure access policy to the DBMS system information.
- Users authenticated via LDAP or Single Sign-On can log in to the application while the "Password validity term, days" system setting is populated.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes\#title-141-15 "Direct link to Development tools")

- We have added a "Noteworthy events for contact" sample report that you can use as a template when setting up custom FastReport reports.
- When synchronizing your mailbox via the IMAP/SMTP protocol, Creatio now uses the MailKit library.

- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-1)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-2)
  - [Forecasts](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-3)
- [Creatio Service](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-4)
  - [Cases](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-5)
- [Financial Services Creatio](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-6)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-7)
  - [Predictive analytics](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-8)
  - [Analytics](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-9)
- [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-10)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-11)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-12)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-13)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-14)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7161-release-notes#title-141-15)