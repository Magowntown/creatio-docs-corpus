<!-- Source: page_23 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 10/28/2020

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.17.0.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-1 "Direct link to Creatio Marketing")

### Lead generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-2 "Direct link to Lead generation")

- Added integration with Facebook lead generation forms. All you need to do is link a landing page record in Creatio with a Facebook business page and select one of the lead registration forms on it. As a result, each submission of the corresponding Facebook form will generate a new lead in Creatio.

Setting up integration with a Facebook landing page

![Setting up integration with a Facebook landing page](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/facebook_lead_generation_integration.png)

### Email marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-3 "Direct link to Email marketing")

- Creatio now sends bulk emails 8 times faster. Added a new type of bulk email response: "Canceled (unsubscribed by email type)." This response indicates that a contact was not sent any emails because they unsubscribed from this type of bulk email. In this case, Creatio does not send the emails.

## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-4 "Direct link to Creatio Sales")

- Forecasting tabs now have versions. Functions:
  - Select a specific version of the forecast.
  - Set up daily autosaving of a forecast tab.
  - Compare the volumes of a specific version with the current version of the forecast. The values that are higher in the current version of the forecast are highlighted in green, while the values that are lower than in the compared version are highlighted in red. The highlighted cells have tooltips displaying the values from the current version of the forecast, as well as the difference with the compared version.
- Creatio now enables specifying the time zone when setting up automatic forecast calculation and autosaving.


Comparing data in the versions of a forecasting tab

![Comparing data in the versions of a forecasting tab](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/planning_versions.png)

## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-5 "Direct link to Core functions")

- You can now use mathematical formulas to calculate the values of numeric fields in pivot tables.
- Improved the searching for contacts when mentioning them in the feed: you can choose the search criteria between "Contains ..." or "Starts with ...." Managing the search is implemented via the "String columns filter" (StringColumnSearchComparisonType) system setting.

### Chats [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-6 "Direct link to Chats")

Chats are now available in Creatio as a new communication channel.

Important

The following Creatio functionality is only available for beta-testing. To evaluate the chat feature, use a trial version of any Creatio product or request early access for beta-testing by contacting Creatio support. We appreciate your feedback!

The new feature will be available in the upcoming Creatio releases.

- Customers can write private messages to your company page in Facebook or using the Facebook Messenger plug-in available on your website. You will be able to process all the messages in Creatio, they will be saved on a customer page.
- The agents can process the incoming chats in the communication panel, provide consultations in real time, as well as send instructions and additional materials.
- When working with chats, agents can create cases based on customer requests or run their own business processes.
- The completed conversations are available for review in the new **Chats** section and the **Timeline** tab of the contact page.
- Use the new **Chat settings** section in the System Designer to enable and set up the chat functionality.

Creating a case based on a chat

![Creating a case based on a chat](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/omnichat_create_case.png)

## Customer database management tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-7 "Direct link to Customer database management tools")

We have updated the "connected to" diagram in the **Contacts** and **Accounts** sections.

Important

This functionality is only available for beta-testing in Creatio version 7.17.0. To evaluate the new "connected to" diagram, use a trial version of any Creatio product or request early access for beta-testing by contacting Creatio support. We appreciate your feedback!

The new feature will be available in the upcoming Creatio releases.

- With the new diagram, you can:
  - set up the connections between contacts and accounts in a couple of clicks;
  - see all the internal and external contact connections, both professional and personal;
  - group contacts within and outside an organization.

The “connected to” diagram for contacts and accounts

![The “connected to” diagram for contacts and accounts](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/Connected_to.png)

## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-8 "Direct link to Integrations")

- Enabled uploading emails that have been copied from one mailbox to the other on a mail service.
- For Creatio .Net Core applications, supported authorization via the OAuth 2.0 protocol.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-9 "Direct link to Business processes")

- You can now save a modified business process as a new version regardless of whether any of its instances have been run. This enables tracking change history details and returning to any of the previous versions if needed.
Saving the process

![Saving the process](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/save_process_version.png)

- Dynamic cases now have versions. If you change a case, you can save it in a new version. Note that the cases that were run earlier will be executed in their current version. You can change the version of such cases for a new one. This will cancel the current instance of the case and will run a new instance in the new version.


## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-10 "Direct link to User customization tools")

### Section Wizard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-11 "Direct link to Section Wizard")

- You can now copy a page together with the **Timeline** tab settings.

- Creatio now saves sections created based on existing objects if you do not specify the default display column in the object.

- The following features are now available in the Section Wizard and the pre-configured page designer to accelerate and simplify the setup:
  - Specifying the value precision when setting up numeric fields. You can select an integer or a fractional number with precision up to eight decimal digits.
  - Adding translations of field groups, boolean and lookup fields and new lookup names when setting up the page.
  - Editing the field group code when adding it.
  - Changing the name and code of the lookup that has been created for a new lookup field but not yet saved in the Section Wizard.
- You can set up the value calculation logic in numeric fields using formulas in the "Set field value" business rule. Examples of business logic that involves this rule include:
  - Calculating the product cost based on its price and the stock volume.
  - Calculating the order sum in the base currency based on the current exchange rate and the order sum in the local currency.

## Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-12 "Direct link to Performance")

- Creatio now updates roles faster. For applications with large number of users and multidivisional organizational structure, the role update now performs 10 times faster as compared to previous versions.
- For applications deployed on Oracle, we have improved generating static content in the file system.

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-13 "Direct link to Administration")

- You can check the validity of version for the installed Creatio Marketplace applications. When a new version of the Creatio Marketplace application appears, system administrators receive a corresponding notification in the communication panel.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-14 "Direct link to Development tools")

- We have updated the interface of working with SVN. The setup in new interface is simpler and more flexible.

- You can now log in when adding an SVN repository to Creatio, which accelerates the setup process.
Adding a new repository

![Adding a new repository](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/svn_storage.png)


### Advanced settings [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-15 "Direct link to Advanced settings")

- The **Configuration** section and the configuration designers have been updated.

- The section displays the list of configuration items with their statuses.

- We have added a form to view the configuration item properties.

- You can filter items in the section by:
  - type;
  - available errors;
  - needed actualization;
  - available locks.
- You can perform search separately by packages or by items.

- The locked and editable packages are not highlighted in different colors.

- The packages that are connected to SVN have a repository icon displayed. When you hover over the icon, it provides information about the revision number and the repository.

- The package properties contain all information about the repository that it is connected to.

- You can now create a web service in the **Configuration** section.


The updated Configuration section

![The updated Configuration section](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.17.0/BPMonlineHelp/release_notes/configuration.png)

### Configuration item designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes\#title-1650-16 "Direct link to Configuration item designer")

- All configuration item designers now have search by structure.

- Implemented "hotkeys" for the designer functions.

- The pre-configured filters have been removed from the page of adding data – you can now select the needed data manually.

- Made several improvements to the object adding page:
  - Added grouping by column type.
  - By default, Creatio displays the expanded mode of working with object and only the relevant properties for each type of column.
  - The column properties have been regrouped and now correspond to the Section Wizard.
  - Added a block with the list of all available triggers for events.
  - The new **Edit process** button enables opening the Process Designer for the object.
- Implemented a code validation function in the source code controls. If a code contains errors or warnings, a corresponding icon will mark the faulty string. If a code contains errors or warnings, the string will have a corresponding icon. When you hover over the icon, you will see a tool tip with the message of error or warning.

- When adding localizable strings, Creatio displays only the active cultures. To display the full list of languages, click **Show all languages**.


- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-1)
  - [Lead generation](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-2)
  - [Email marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-3)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-4)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-5)
  - [Chats](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-6)
- [Customer database management tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-7)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-8)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-9)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-10)
  - [Section Wizard](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-11)
- [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-12)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-13)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-14)
  - [Advanced settings](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-15)
  - [Configuration item designer](https://academy.creatio.com/docs/8.x/resources/release-notes/7170-release-notes#title-1650-16)