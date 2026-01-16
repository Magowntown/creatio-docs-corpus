<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/logging-tools/change-log/view-the-change-log)** (8.3).

Version: 8.2

On this page

When working with Creatio, you might need to view the changes made to your data and see who made these changes and when. For example, you can check which contact records were changed last month.

The data change history is available in the **Change log** section (Fig. 1).

Fig. 1 The Change log section view

![Fig. 1 The Change log section view](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_crd_example.png)

The change log contains information about adding, modifying, and deleting records (entries) in the database tables for Creatio objects. This includes sections, Classic UI details, lookups, as well as other objects.

note

To view the changes, make sure you have the "Access to "Change log" section" (`CanManageChangeLog` code) or "View change log" (`CanViewChangeLog` code) system operation permission.

Learn more about using system operations: [System operation permissions](https://academy.creatio.com/documents?id=258).

You can open a change log for viewing its records in the following ways:

- Open the **Change log** section from the System Designer and select an object to view its logs. [Read more >>>](https://academy.creatio.com/documents?id=1454#title-236-1)
- Open the change log of a specific record directly from the **record page** that has the relevant button. [Read more >>>](https://academy.creatio.com/documents?id=1454#title-236-2)

## Method 1. View the record changes from the change log [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log\#title-236-1 "Direct link to Method 1. View the record changes from the change log")

Example

View the contact records that were changed on specific dates.

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/btn_system_designer.png) to **open the System Designer**.

2. **Go to** the **Users and administration** block → **Change log**.

3. **Set the filter**. For this example, select "Sections".

4. **Find the needed object** using the search bar or manually. For this example, use the "Contact" object. Click the object title to open the change log page.

5. Click the **Log data** tab and **set the date filter** (Fig. 2). For this example, it is the time period from October 25th to November 3rd, 2025.
Fig. 2 Filter changes by date for the Contact object

![Fig. 2 Filter changes by date for the Contact object](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/scr_filter_date_object.png)


**As a result**, the list of records that were changed within the specified period will be displayed (Fig. 3). The icons next to dates display the type of the performed operations: deleting, adding or editing.

Fig. 3 View the change log

![Fig. 3 View the change log](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/scr_change_log.png)

Use the **search bar** to quickly find the needed record by title. For this example, use the contact’s full name (Fig. 4). To learn the details of the performed changes, click the name in the **Record** column.

Fig. 4 Quick search by record name

![Fig. 4 Quick search by record name](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/scr_change_log_search.png)

## Method 2. View logs directly from the record page [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log\#title-236-2 "Direct link to Method 2. View logs directly from the record page")

You can view the change log for a specific record or object if the record page contains a button that has the **Open change log** action set up.

Example

View the change log of the field values on the contact page that were changed on specific dates.

1. **Open the page** of the needed record.

2. **Click the change log button**. This opens the page that contains the following information about the selected record:
1. dates of the changes
2. authors of the changes
3. record name
4. list of the changed columns
5. values before the change
6. values after the change
3. **Set the date filter** to display only the changes for the last month. (Fig. 5). For this example, it is the time period from October 25th to November 3rd, 2025.
Fig. 5 Filter changes by date for the log of a specific record

![Fig. 5 Filter changes by date for the log of a specific record](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/scr_filter_date_record.png)


**As a result**, you will see the changes that were made in the logged fields within the specified period (Fig. 6).

Fig. 6 Record logs

![Fig. 6 Record logs](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/view_the_change_log/scr_record_change_log.png)

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log\#see-also "Direct link to See also")

[Clear the change log](https://academy.creatio.com/documents?id=1455)

[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?id=2376)

- [Method 1. View the record changes from the change log](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log#title-236-1)
- [Method 2. View logs directly from the record page](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log#title-236-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/logging-tools/change-log/view-the-change-log#see-also)