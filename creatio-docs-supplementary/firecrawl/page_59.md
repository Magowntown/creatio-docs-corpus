<!-- Source: page_59 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 06/30/2020

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.16.2.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-1 "Direct link to Creatio Marketing")

- Added integration with the [SendGrid](https://sendgrid.com/) service for sending bulk emails and trigger emails. SendGrid has a delivery rate of 99.99%, as well as analytical dashboards for sales, orders, campaigns and provides real-time analytics. Contact Creatio support to switch your Creatio marketing email provider to SendGrid. You will need to verify your email domain before using SendGrid.

- Improved usability of the campaign diagrams through an array of new cursor modes:


  - ![arrow_tool.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/arrow_tool.png) Arrow – regular mode for selecting separate elements.
  - ![lasso_tool.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/lasso_tool.png) Lasso – selecting multiple elements via a "drag box."
  - ![space_tool.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/space_tool.png) Space – shift multiple elements horizontally or vertically (e.g., to create free space in the middle of a complex diagram).

Similar tools are already available in the Process Designer. For more on working with the diagrams, see " [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-6)."

- You can now start sending bulk emails right after copying, without the need to save the template in the Content Designer.

- Links in templates with the **HTML** blocks now display correctly. Previously, line breaks in the hyperlink code could interfere with link generation in the sent emails.

- Content blocks now properly display after adding a new language to a service notification template and switching to that language tab.


## Financial Services Creatio [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-2 "Direct link to Financial Services Creatio")

- You can now bind products and their subordinate elements automatically to a package. This will be helpful to business analysts and methodologists who work with complex hierarchical product catalogs. You can bind data for specific products or all products. Use the new action in the **Products** section to initiate the data binding.

Binding the product data

![Binding the product data](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/finserv_bind_data.png)

## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-3 "Direct link to Core functions")

- All new queues now have the "Medium" priority and "Planned" status by default.

- Emails with attachments are now marked with ![attachment.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/attachment.png) in the communication panel.

- Quoted previous email is now visually separated on the email page.
Quoted previous email on the email page

![Quoted previous email on the email page](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/quote_letter.png)

- Email attachment now displays correctly in emails that you send from Creatio. Previously, some of the mail clients sometimes did not display all attachments.


### Analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-4 "Direct link to Analytics")

- You can now copy and entire chart series. Use this to accelerate the creation of multi-series charts.
Copying a chart series

![Copying a chart series](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/copying_series.png)

- Improved the navigation in the **Dashboards** section. You can now view dashboard tabs as a menu, filter the tabs, and add them to favorites. The dashboards that you add to favorites will display first in the list.
Adding dashboards to favorites

![Adding dashboards to favorites](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/totals_tabs_filter.gif)

- Added new analytical dashboards for sales, orders, campaigns, and leads.
New lead analysis dashboard

![New lead analysis dashboard](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/new_dashboards.png)


## Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-5 "Direct link to Integrations")

- You can now specify OAuth parameters for Gmail integration via IMAP/SMTP. You can choose between OAuth authentication via GSuite or regular authentication via login/password.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-6 "Direct link to Business processes")

- Business process diagrams with large numbers of elements now load faster in Studio Creatio, free edition.
- Creatio now imports boundary events from \*.BPMN files. Previously, these events were ignored, which could cause errors in the execution of the imported processes. Creatio converts imported boundary events into non-executable elements. You will need to edit the diagram to replicate the logic of the boundary events.

### Process log [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-7 "Direct link to Process log")

- You can now view process instances that were run as multi-instance processes. This information is available on the **Process elements** detail of the process log. Multi-instance processes display as links that open a list of instances.
- Business process instances have a new "Cancelling" status, detailing the state of process instances that are being canceled en mass.

### Process designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-8 "Direct link to Process designer")

- Improved the UX for executable process design by adding several new cursor tools.


  - Use the ![arrow_tool00001.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/arrow_tool00001.png) Arrow tool for typical select and move separate elements on the diagram.

  - Use the ![lasso_tool00002.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/lasso_tool00002.png) Lasso tool to select multiple elements via a "drag box."
    Using the Lasso tool

    ![Using the Lasso tool](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/lasso-tool.gif)

  - Use the ![space_tool00003.png](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/space_tool00003.png) Space tool to shift all elements on the diagram left/right or up/down. This tool applies to all elements to the right or left from the cursor – when shifting elements horizontally. Likewise, when shifting elements vertically, the tool will apply to all elements above the cursor (when shifting upwards) and all elements below the cursor (when shifting the elements downward).


Using the Space tool

![Using the Space tool](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/space_tool.gif)

- Multi-instance processes now execute in parallel. You can run the subprocess instances in parallel or sequentially by changing the setting of the **Subprocess** element. Parallel process instances run independently from one another.
Multi-instance subprocess modes

![Multi-instance subprocess modes](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/type_of_implementation.png)

- Multi-instances subprocesses can now have outbound parameters of the "Collection" type. You can map these parameters as regular collections in the parent process. The collection will include all bi-directional parameters of the multi-instance sub-process.
Resulting collection of a multi-instance sub-process

![Resulting collection of a multi-instance sub-process](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/parametres_in_collection.gif)


## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-9 "Direct link to User customization tools")

- You can now set up MS Word reports on .NET Core Creatio products.

### Section Wizard [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-10 "Direct link to Section Wizard")

- You can now copy a section record page and customize it as a separate page.
Copying a section page

![Copying a section page](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/copying_section_page.png)

- You can now create new sections based on existing Creatio objects.
Creating a new section based on an existing object

![Creating a new section based on an existing object](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/section_wizard.png)

- You can now use business rules to populate or clear fields automatically. For example, a business rule for filtering cities by country can also automatically populate the **Country** field when the user populates the **City** field.
Populating and clearing fields automatically via a business rule

![Populating and clearing fields automatically via a business rule](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.2/BPMonlineHelp/release_notes/business_rule.png)


## Security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-11 "Direct link to Security")

- Creatio now manages permissions and limitations for uploading files. You can create "blacklists" for unwanted file types using the "File extensions DenyList" system setting. By default, the setting already includes a list of potentially unsafe files. You can disable the file extension limitations using the **File Security Mode** system setting.

## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes\#title-140-12 "Direct link to Development tools")

- OData 4 now supports the UPSERT operation and can use data filtering by reverse connections.

- Expanded API for working with data:
  - The QueryColumnExpression now had methods for working with arithmetic and bitwise operations. You can now write DBMS-independent code using  Column.SqlText, for instance. The methods are available in "Column," "Where," "Having," "Set," as well as similar sentences to create "Select," "Delete," "Insert," "InsertSelect," "Update," "UpdateSelect" queries.
  - The DBExecutor class now has a new RefreshMaterializedView() method, which fully updates the contents of the materialized view for Oracle and PostgreSQL.
  - The new HierarchicalOptions property o the Select class enables direct execution of hierarchical queries using the Select class, without the need to obtain SQL text and creating additional DBExecutor instances.
  - The window function API now has ROW\_NUMBER calculation and sorting direction. The new RowNumberQueryFunction function and the OrderDirection enumeration instances can be passed to the WindowQueryFunction window function constructor.

- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-1)
- [Financial Services Creatio](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-2)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-3)
  - [Analytics](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-4)
- [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-5)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-6)
  - [Process log](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-7)
  - [Process designer](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-8)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-9)
  - [Section Wizard](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-10)
- [Security](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-11)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7162-release-notes#title-140-12)