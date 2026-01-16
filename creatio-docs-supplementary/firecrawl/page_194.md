<!-- Source: page_194 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/logging-tools/change-log/view-the-change-log)** (8.3).

Version: 8.0All Creatio products

On this page

When working with Creatio, you may need to view the changes made to your data and see who made these changes and when. For example, you can check which contact records were changed last month.

The data change history is available in the **Change log** section (Fig. 1).

Fig. 1 The Change log section view

![Fig. 1 The Change log section view](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_crd_example.png)

The change log contains information about adding, modifying, and deleting records (entries) in the database tables for Creatio objects. This includes sections, details, lookups, as well as other objects.

There are two ways you can open a change log for viewing its records:

- Open the **Change log** section from the System Designer and select an object to view its logs.
- Open the change log of a specific record directly from the **record page**.

## Method 1. View the record changes from the change log [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log\#title-236-1 "Direct link to Method 1. View the record changes from the change log")

Example

View the contact records that were changed last month.

1. Open the System Designer, e.g., by clicking ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/btn_system_designer.png).

2. Under **Users and administration**, click **Change log**.



note





To view the changes, make sure you have the **Access to "Change log" section** (CanManageChangeLog) system operation permission.



Learn more about using system operations in the " [System operation permissions](https://academy.creatio.com/documents?product=base&ver=7&id=258)" article.

3. Set the filter - for our example, select "Sections".

4. Find the needed object using the search bar or manually. In our example, we use the "Contact" object.   Click the object title to open the change log page.

5. Click the **Log data** tab and set the date filter (Fig. 1). In our example, it is the time period from February 2nd to March 2nd, 2020.
Fig. 1 Filtering changes by date for the Contact object

![Fig. 1 Filtering changes by date for the Contact object](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_wnd_filter_date.png)


As a result, the list of records that were changed within the specified period will be displayed (Fig. 2). The icons next to dates display the type of the performed operations: deleting, adding or editing.
Fig. 2 Viewing the change log

![Fig. 2 Viewing the change log](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_crd_view_section.png)

6. Use the **search bar** to quickly find the needed record by title. In our case - by the contact’s full name (Fig. 3). To learn the details of the performed changes, click the name in the **Record** column.
Fig. 3 Quick search by record name

![Fig. 3 Quick search by record name](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_crd_find.png)


## Method 2. View logs of a specific record directly from the record page [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log\#title-236-2 "Direct link to Method 2. View logs of a specific record directly from the record page")

Example

See the change log of the field values on the page of a specific contact for the last month.

1. Open the page of the needed record.

2. Click **Actions** → **View change log** (Fig. 1).
Fig. 1 The View change log action

![Fig. 1 The View change log action](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_crd_view_record.png)




note





If you cannot see the **View change log** command in the **Actions** menu, make sure you have permission to the **View change log** (CanViewChangeLog) system operation.



Learn more about using system operations in the " [System operation permissions](https://academy.creatio.com/documents?product=base&ver=7&id=258)" article.

3. The page that opens will display information about the selected record:
1. dates of the changes
2. authors of the changes
3. record name
4. list of the changed columns
5. values before the change
6. values after the change
4. Set the date filter to display only the changes for the last month. (Fig. 2). In our example, it is the time period from February 2nd to March 2nd, 2020.
Fig. 2 Filtering changes by date for the log of a specific record

![Fig. 2 Filtering changes by date for the log of a specific record](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_wnd_contact_filter_date.png)


As a result, you will see the changes that were made in the logged fields within the specified period (Fig. 3).

Fig. 3 Record logs

![Fig. 3 Record logs](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/view_change_log/scr_section_change_log_view_column_record.png)

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log\#see-also "Direct link to See also")

[Clear the change log](https://academy.creatio.com/documents?id=1455)

- [Method 1. View the record changes from the change log](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log#title-236-1)
- [Method 2. View logs of a specific record directly from the record page](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log#title-236-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/logging-tools/change-log/view-the-change-log#see-also)