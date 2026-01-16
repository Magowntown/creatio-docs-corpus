<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/logging-tools/change-log/set-up-the-change-log)** (8.3).

Version: 8.1

On this page

The **change log** records changes to business data. You can use it for things like tracking product price or account balance changes.

The **audit log** records system events, system settings, and system data. Learn more in a separate article: [Set up the audit log](https://academy.creatio.com/documents?id=1260).

The change log is disabled by default. Follow the steps in this article to enable this feature.

To set up logging, you can use either the **Change log** section or a Classic UI Creatio section, lookup, or detail.

Example

Set up logging of changes in contact phone numbers and emails.

Emails, mobile and work phones are available in the contact profile, so you need to enable logging in the **Contacts** section on the column level.

If you use a load balancer to ensure fault tolerance of your Creatio application, perform the setup on one Creatio instance, then transfer settings to other instances. The setup process applies to Marketplace apps, custom packages, and other settings that require compilation. Learn more in a separate article: [Compile an app on a web farm](https://academy.creatio.com/documents?id=2410).

## Method 1. Set up logging in the \[Change log\] section [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log\#title-234-1 "Direct link to Method 1. Set up logging in the [Change log] section")

We recommend setting up logging only for columns whose values you need to track. With large databases, logging a significant number of objects and columns might reduce Creatio’s performance.

You must have permission to the “Access to "Change log" section” (the “CanManageChangeLog” code) system operation to manage the **Change Log** section. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_the_change_log/btn_system_designer.png) to **open the System Designer**.

2. **Go to** the **Users and administration** block → **Change log**.

3. **Find the needed section object**, detail, or lookup in the object list. For example, set the “Sections” filter (Fig. 1).
Fig. 1 Object filter in the change log

![Fig. 1 Object filter in the change log](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_change_log/scr_section_change_log_choosing_object.png)

4. **Select the section** from the list or find it using the search bar (Fig. 2). Click the title of the needed object. For example, the “Contact” object. This opens a page.
Fig. 2 Search bar in the change log

![Fig. 2 Search bar in the change log](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_change_log/scr_section_change_log_wnd_find_object.png)

5. Toggle on the **Enable logging** switch to **enable logging on the object level**. If you save the changes on this step, Creatio will log only the delete operations.

6. **Set up the list of columns** to log. For example, use the **Email**, **Mobile phone**, and **Business phone** columns (Fig. 3).

Click **Add** to add a new column. Hold the pointer over the column title and click ![btn_delete.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_change_log/btn_delete.png) to delete an added column.
Fig. 3 Column logging setup

![Fig. 3 Column logging setup](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_change_log/scr_section_change_log_choosing_column.png)

7. **Click** **Apply** to save the changes.


As a result, Creatio will start monitoring the record create, update, and delete events and recording them to the change log.

## Method 2. Set up logging in a Classic UI section, lookup or detail [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log\#title-234-2 "Direct link to Method 2. Set up logging in a Classic UI section, lookup or detail")

1. **Open the needed Classic UI section**, lookup, or detail. For example, the **Contacts** section.

2. **Click** **Actions** → **Change log setup** (Fig. 4).
Fig. 4 Set up the change log in the Contacts section

![Fig. 4 Set up the change log in the Contacts section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_change_log/scr_section_change_log_wnd_set_section.png)


note

If you cannot see **Change log setup** in the action list, make sure you have permission to the “Access to "Change log" section” (the “CanManageChangeLog” code) system operation. Learn more in a separate article: [System operation permissions](https://academy.creatio.com/documents?id=258).

As a result, the change log setup page of the **Contacts** section will open. Follow **steps 5 through 7** from the **Method 1** to complete the setup.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log\#see-also "Direct link to See also")

[View the change log](https://academy.creatio.com/documents?id=1454)

[Clear the change log](https://academy.creatio.com/documents?id=1455)

- [Method 1. Set up logging in the \[Change log\] section](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log#title-234-1)
- [Method 2. Set up logging in a Classic UI section, lookup or detail](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log#title-234-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/set-up-the-change-log#see-also)