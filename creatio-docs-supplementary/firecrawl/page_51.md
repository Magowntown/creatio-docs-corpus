<!-- Source: page_51 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 09/06/2022

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are taking it to the next level with the following **new features** included in Creatio version 8.0.4 Atlas.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## No-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-1 "Direct link to No-code platform")

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-2 "Direct link to Business rules")

**Available actions**. Creatio version 8.0.4 Atlas lets you set up business rules that hide and display components, make fields required, and make fields editable.

**Object-level rules**. You can set up business rules that make fields required and editable on the object level. After you set up a rule, Creatio automatically applies it to every Freedom UI page that uses the corresponding object, including editable lists.

Creating a business rule on the object level

![Creating a business rule on the object level](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/gif_creating_an_object-level_business_rule.gif)

**Rule combination**. You can set up multiple Freedom UI business rules that manage a single property, for example, field requirement. Creatio analyzes every business rule that affects the field and performs the corresponding action as a result. For example, you can hide the **Meeting room** field for "To do" type activities or "Meeting" type activities that have the **Online** checkbox selected. If none of the business rule conditions apply, Creatio automatically sets the property to the value specified in the component settings.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-3 "Direct link to Freedom UI Designer")

**Attachments**. It is now possible to manage record attachments in Freedom UI using the **Attachments** component. The files can be attached to the record itself or related objects. You can tag specific attachments to filter them or display multiple attachment lists on a single page, for example, required request files and additional request files.

**Feed**. You can now post and read comments in Freedom UI using the **Feed** component. Feeds have multiple types:

- "Record." For example, discussion of a particular lead.
- "User." For example, the index of posts and comments that mention the current user or those to which the user is subscribed.

Feed component

![Feed component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/scr_feed_component.png)

**Rich text**. You can now manage rich text content in Freedom UI apps using the **Rich text** field and input. For example, this is useful for writing emails or knowledge base articles.

**Color picker**. You can now select a color from the base or extended palette using the **Color picker** field and input. This is particularly useful for a product catalog. The field uses the "Color" data type in the data source.

Color picker component

![Color picker component](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/scr_color_picker_component.png)

**Phone number**. Text fields now include the "Phone number" format type that lets you streamline phone number management. If needed, you can apply the phone number pattern in international format.

Phone number field

![Phone number field](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/scr_phone_number_field.png)

**Component visibility**. The component setup area now lets you specify whether to display the component on page load by default as well as open the Business Rule Designer to set up custom visibility rules.

**Component code**. The component setup area now displays the element's page schema code to streamline advanced page customization.

**Container colors**. You can now set custom colors and transparency levels for container boxes.

**New button action**. Creatio 8.0.4 Atlas lets you manage record access permissions using the new "Set up access rights" button action.

**Button data connection**. The base actions of **Save** and **Cancel** buttons now apply to all page data sources. For example, if you edit fields and editable lists, the **Save** button saves the changes immediately.

**List object creation**. It is now possible to create a new object directly from the setup area of the **List** component.

Creating a list object

![Creating a list object](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/gif_creating_a_list_object.gif)

**Field requirement marks**. Freedom UI Designer now marks required fields on the canvas using the ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/icn_freedomui_field_required.png) character.

### Customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-4 "Direct link to Customization tools")

**Microsoft Word printables**. It is now possible to use images from an external file repository in Microsoft Word printables.

**Vault authentication certificates**. You can now store Vault authentication certificates in Windows Certificate Store. Also, the certificate can now be read both by the name and ThumbPrint.

**Data protection compliance**. You can now mark custom objects’ fields that contain personal data in the **Configuration** section to ensure compliance with GDPR and other regulations on personal data protection. The option is enabled by default for out-of-the-box objects.

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-5 "Direct link to Performance")

**Resource intensive queries**. It is now possible to manage resource intensive queries automatically to ensure they do not affect other Creatio users and infrastructure elements. To do this, set up rules that manage queries, for example, cancel their execution, limit the number of execution threads, or set database timeout, in the **Query handle rule** lookup. You can limit the execution of the following resource intensive queries:

- queries that filter rows using the "CONTAINS" predicate
- queries without filters and pagination
- queries that sort by a non-indexed column
- queries that sort by complex columns that contain subqueries

Creatio tracks queries that trigger the rules in the **Query rule apply log** lookup. The system administrator can use the lookup to view the query, trigger cause, and recommendations on eliminating the negative impact of the query on Creatio.

## UI and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-6 "Direct link to UI and system capabilities")

### Freedom UI Sections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-7 "Direct link to Freedom UI Sections")

**Columns linked via a reverse connection**. You can now add a list column that displays the value of the first record linked via a reverse connection, with or without filter and sorting conditions. For example, this is useful if you need to display the results of the last contact activity.

### Freedom UI [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-8 "Direct link to Freedom UI")

**List UX**. The user experience in the Freedom UI list was greatly improved:

- Column width. The default width of columns added to the list now varies based on the data type.
- Cell editing. You can now edit a selected cell immediately by entering data using the keyboard.
- Phone number fields. Phone numbers in the field and list column use the "tel:" link format. If Creatio is integrated with a phone service, click the field to initiate a call from the communication panel. Otherwise, clicking the field runs the application that handles phone calls.
- Data loss prevention. Creatio now warns you if you have unsaved changes on the page or in the editable list and attempt to take an action that leads to data loss, for example, open a different app, refresh the browser tab, etc.

**List folder management**. New "All" virtual root folder was added to the folder tree. If you activate a filter by clicking on a different folder, click the "All" folder to deactivate the filter. Select the "All" folder and click **Add** to create a new first-level folder.

**Aggregate columns**. You can now set up aggregation for numeric, date, datetime columns and filter the aggregated values. Numeric columns support minimum, maximum, sum, average functions. Date and datetime columns support minimum and maximum functions.

Adding an aggregate column

![Adding an aggregate column](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_4/gif_adding_an_aggregate_column.gif)

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes\#title-3964-9 "Direct link to Development tools")

**Change management**. It is now possible to restore the previous configuration state from package backups completely using the Application Hub, WorkspaceConsole, or Clio utility. For example, this is useful if package installation fails or you find an error after a successful installation. Creatio uses package backups to automatically restore schemas and data changes made using the binding mechanism or backward compatible SQL scripts. Learn more about the backward compatibility requirements in the developer documentation: [Backward compatible SQL scripts](https://academy.creatio.com/documents?id=15109).

**Workspace Console utility**. The utility was improved:

- Package deletion. A command that deletes one or more configuration packages from the environment was added to Workspace Console.
- Configuration updates. A command that lets you update the configuration, including the installation of new packages into the environment and deleting existing packages, was added to WorkspaceConsole. When you run the command, Creatio backs up both packages to update and delete. If you restore the configuration, Creatio both rolls back the installed packages and returns the deleted packages to the configuration.
- Data binding installation. The commands that install packages into the environment and update the configuration can now install only specific data bindings. To do this, pass the path to the file that contains the list of data bindings to install in a command parameter. The commands do not install data bindings not included in the file.

**Custom components**. You can now create handlers and validators directly in the npm package of custom components. This streamlines handler and validator management as opposed to describing them in page schemas, for example, when embedding custom components into Creatio pages. Learn more in the developer documentation: [Custom request handler implemented using remote module](https://academy.creatio.com/documents?id=15037), [Custom validators implemented using remote module](https://academy.creatio.com/documents?id=15040).

- [No-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-1)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-2)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-3)
  - [Customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-4)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-5)
- [UI and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-6)
  - [Freedom UI Sections](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-7)
  - [Freedom UI](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-8)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/804-atlas-release-notes#title-3964-9)