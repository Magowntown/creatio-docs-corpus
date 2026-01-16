<!-- Source: page_38 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 09/14/2020

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.16.4.

The "Update guide" for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-1 "Direct link to Creatio Marketing")

### Website event tracking [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-2 "Direct link to Website event tracking")

We have completely revamped the website tracking functionality. A new **Event tracking service settings** section is now available in the System Designer.

- You can now track user activity on multiple websites. Use the **Tracking resources** detail to set up the list of tracked websites. The tracking resources are grouped as "projects."
New website tracking project settings

![New website tracking project settings](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/tracking_project_example.png)

- Information about the tracked website events has been moved to a separate tab.

- You can now set up and use an extended list of event types. For example, adding a product to the wish list, downloading a file, adding or removing a product to the shopping cart, adding payment details, etc. You can get additional information on each event, including the page from which the user transitioned to the site, user’s web browser, language, and screen resolution.

- Creatio records the website events for incomplete user sessions, e.g., if the user interrupts the connection before the page finishes loading.

- We have increased the website event tracking bandwidth, enabling the registration of an unlimited number of actions per website.


### Marketing emails [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-3 "Direct link to Marketing emails")

- We have changed the email address and sender domain verification logic for the UniOne provider. We have added a new verification parameter: unione-verification-record. The parameter is required in the DNS zone of your domain along with DKIM and SPF records. After the verification, all email addresses within the verified domain will be able to send emails, there is no need to verify each email address separately.

- The email setup page now displays only the fields required by the chosen email provider.

- Emails sent through UniOne no longer have extra spaces in Outlook, Outlook web, and Gmail.

- We have implemented additional audience management features for bulk emails.
  - You can now create audiences from different Creatio objects, such as "Lead," "Account," "Order," "Event participant," and more. Set up the object list for audience import using the **Object management** command in the **Audience** action menu.
  - We have implemented filtering bulk email recipients using the fields of a connected object. For example, you can configure an email audience to include only leads with a specific need. To set up the filters, click **Audience management** in the detail menu.
  - Users can now delete all records from the **Audience** detail by clicking **Clear the audience**. When the number of the contacts is significant, the deletion is run in the background.
  - You can now view individual dynamic content emails sent to specific recipients. The templates are available in the **Audience** detail after sending the emails.

### Content Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-4 "Direct link to Content Designer")

- Creatio now validates custom HTML code. Validation errors in an **HTML** (Smart block) element will stop the template from being saved. The details of the validation errors will be available on the validation panel.
- We have implemented selecting a lookup object for the macros values when sending a test email.
- Creatio now caches the email addresses of test recipients to accelerate sending test emails.  The addresses will populate the **Test email(s) will be sent to email addresses** field automatically when preparing the next test email for sending.

## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-5 "Direct link to Creatio Sales")

- You can now set up the periodicity for updating the actual values in the **Forecasts** section. Select the **Automatic calculation** checkbox to enable this function.

Setting up the period for automatic calculation of a forecast

![Setting up the period for automatic calculation of a forecast](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/forecasts_calculation_period.png)

## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-6 "Direct link to Core functions")

- Creatio 7.17 stops supporting Internet Explorer 11. For Windows, Microsoft recommends using the Microsoft Edge browser. For more information, please see the [Microsoft Tech Community](https://techcommunity.microsoft.com/t5/windows-it-pro-blog/the-perils-of-using-internet-explorer-as-your-default-browser/ba-p/331732) article. We recommend using Google Chrome and Mozilla Firefox for working with Creatio on Windows-based devices.

- Now you can use voice typing in multi-line fields. The functionality is available when working with Creatio in the latest version of Google Chrome.
Example of voice typing in Creatio

![Example of voice typing in Creatio](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/voice_typing.gif)


### Predictive data analysis [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-7 "Direct link to Predictive data analysis")

- We have implemented "recommendation" predictive models for Creatio Sales. The models train automatically, using the data from at least 100 opportunities. As a result, Creatio will produce a personalized list of products that each customer is most likely to purchase. The list of recommended products displays on the **Recommended products** detail of the opportunity page. Learn more in the " [Recommendation prediction](https://academy.creatio.com/documents/administration/7-16/recommendation-prediction)" article.

## Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-8 "Direct link to Mobile application")

- When working with approvals, you can now browse the feed messages and the files on the **Attachments** detail.

## Phone integration and managing communications [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-9 "Direct link to Phone integration and managing communications")

- Terrasoft Messaging Service now supports TLS 1.2 due to the changes in Google security policies and the termination of support for outdated TLS encryption protocols in the new version of Google Chrome.

- Emails imported from Creatio are now marked with a separate category. This function is available on MS Exchange.
Creatio in the list of email categories

![Creatio in the list of email categories](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/ms_outlook_categories.png)


## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-10 "Direct link to Integrations")

- You can now authenticate integrate third-party applications using the OAuth 2.0 protocol using the "client credentials" authentication type. The settings are available in **OAuth 2.0 integration setup** section of the System Designer.

Accessing the OAuth 2.0 integration setup section

![Accessing the OAuth 2.0 integration setup section](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/OAuth_2.0_integrations.png)

Important

This functionality is in the beta-testing mode in version 7.16.4. We appreciate your feedback! Please contact Creatio support to enable this function.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-11 "Direct link to Business processes")

- You can now trace parameter values of multi-instance sub-processes. The tracing data is available for separate elements, as well as for separate instances of a sub-process.

- The diagram of a completed multi-instance sub-process now shows the number of successful instances (the green marker) and the number of instances that have stopped due to an error or were canceled (the red marker).
An execution diagram for a multi-instance sub-process

![An execution diagram for a multi-instance sub-process](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/mi_bp_execution_diagram.png)

- You can now run business processes by multiple section records in bulk. To do so, select multiple records then click **Actions** → **Run process**.
Running a business process by several contacts in bulk

![Running a business process by several contacts in bulk](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/run_bp_for_multiple_records.gif)

- You can now create process parameters of the "Collection of records" type. Add nested parameters to configure the collection structure. "Collection" parameters are useful in the following cases:


  - If a **Script task** element returns a collection of records, you can pass it to the process parameter of the "collection" type and process the collection using no-code means.
  - When running a business process from C# or JS code, you can pass a collection of records to an incoming parameter of the business process.
  - This type of parameter is also useful any time you need to pass a collection of records between different business processes.

Setting up the structure of a Collection of records parameter

![Setting up the structure of a Collection of records parameter](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/mi_subprocess_parameters.png)

## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-12 "Direct link to User customization tools")

### Section Wizard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-13 "Direct link to Section Wizard")

- The no-code tools for designing section pages and "pre-configured pages" in business processes have been expanded with the following new features:


  - Choose the format for displaying the "Date/Time" fields. The fields can display as "Date/Time," "Date only," or "Time only."
  - Limit the number of characters in a text field. You can set the maximum number of characters to 50, 250, and 500 characters, or remove the character limit entirely.
  - You can specify a field title in several languages.

Entering a field title in multiple languages

![Entering a field title in multiple languages](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.4/BPMonlineHelp/release_notes/multilanguage_column_name.gif)

- We have implemented a new type of business rules: "Set field value." The rule will populate a specific field whenever its conditions are fulfilled. Examples of business logic that involves this rule include:
  - Populating the contact details automatically once a case contact has been specified.
  - Display financial details of a linked opportunity or contract on the project page.
  - Create a custom profile of linked records using no-code tools.

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-14 "Direct link to Administration")

- Starting with version 7.17 Creatio will stop supporting legacy UI elements that were used in the previous versions for the **Configuration** section. The following functionality will be available in the new UI only:


  - License manager
  - Change log
  - Object permissions
  - Report setup
  - Email provider setup

The outdated UI elements will be completely removed from the Creatio core.

- You can now set up domain authentication for .NET Core-based Creatio applications.


## Security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-15 "Direct link to Security")

- Security restrictions for the formats of uploaded files now apply to all web services, including those added as part of customization or installed from Creatio Marketplace. You can now disable the limitations for a specific web service. To disable file format restrictions, add the web service to the **List of file security excluded Uris** lookup.
- Creatio .NET Core applications now support security restrictions for the formats of uploaded files.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes\#title-138-16 "Direct link to Development tools")

- The following deprecated API methods will be removed in version 7.17.3:


  - QueryColumnExpression.SqlText
  - Column.SqlText
  - DBExecutor.ExecuteReader
  - DBExecutor.ExecuteScalar
  - DBExecutor.Execute
  - DBExecutor.ExecuteBatches

Instead, use DBMS-independent server classes Select, Delete, Insert, InsertSelect, Update, UpdateSelect. Learn more in the " [Class description](https://academy.creatio.com/documents/technic-sdk/7-16/class-description)" article. Starting with version 7.16.4, Creatio will display warnings if deprecated classes are used during the compilation. The source code of Oracle-based products needs to be re-generated before compiling.

- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-1)
  - [Website event tracking](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-2)
  - [Marketing emails](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-3)
  - [Content Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-4)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-5)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-6)
  - [Predictive data analysis](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-7)
- [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-8)
- [Phone integration and managing communications](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-9)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-10)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-11)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-12)
  - [Section Wizard](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-13)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-14)
- [Security](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-15)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7164-release-notes#title-138-16)