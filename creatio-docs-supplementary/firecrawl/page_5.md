<!-- Source: page_5 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

All Creatio products

On this page

After synchronizing with the Creatio server you can start working with the mobile application (Fig. 1).

Fig. 1 Mobile application workplace

![Fig. 1 Mobile application workplace](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_main_wizard.png)

Tap ![btn_group_mobile_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/btn_group_mobile_menu.png) to access the main page (Fig. 2) and move between sections of the mobile application.

Fig. 2Mobile application main page

![Fig. 2Mobile application main page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_main_menu.png)

The main page of the mobile application contains a list of sections configured in the Mobile Application Wizard, as well as the [Approvals](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-23) section and the [Settings](https://academy.creatio.com/documents?id=1920#title-773-9) menu.

The mobile application list (Fig. 3) contains a list of section records. The list and display method are configured in the main application

Fig. 3 Accounts section list of mobile application

![Fig. 3 Accounts section list of mobile application](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_list.png)

To open the record, tap it in the list.

## Search records [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-2 "Direct link to Search records")

To search for a record in a section, enter the search parameters (for example, a fragment of a company name) in the **Search** field (Fig. 4). The search is performed in the current section and by the primary displayed column (the first column configured in the mobile application wizard).

For example, enter a fragment of an account name in the **Accounts** section, and in a couple of seconds, the result corresponding to the search parameters will be displayed. A search by primary account won't return any search results.

Fig. 4 Search in the section list

![Fig. 4 Search in the section list](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_search.png)

To display all the records of a section, clear the search field.

## Add records [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-3 "Direct link to Add records")

To create a new record, tap the ![btn_add_from_list.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/btn_add_from_list.png) button in the section list. Fill in the page and save the changes.

## Filter records [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-4 "Direct link to Filter records")

You can filter records in Creatio mobile app sections and details by the values specified in one or more columns. For example, using the filters you can quickly find an account by a name fragment or tasks by a specific customer.

To access the filter, tap the ![icn_Funnel.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/icn_Funnel.png) button to the right of the search field (Fig. 5) of the section or detail list. The filter page will open (Fig. 6).

Fig. 5 The filter button in a section

![Fig. 5 The filter button in a section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_filter_button.png)

note

In the **Activities** section, the filter is available in the section list view only.

Tap a column that you want to filter records by and specify the filter value.

Fig. 6 The filter page

![Fig. 6 The filter page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_filter_page.png)

When opened, the filter page displays the same columns as the corresponding section page. If the application is in the online mode, tap **Show more** to display all section columns. In the offline mode, only preliminary configured columns will be displayed.

note

Use the **Search** field at the top of the filter page to quickly locate the needed columns.

note

The columns in the section record page can be configured in the **Mobile application wizard** in the System designer of the desktop application.

After selecting the filter values, tap ![icn_apply.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/icn_apply.png) to apply the filter. Filtered records will be displayed in the section or detail list (Fig. 7).

Fig. 7 Applying filters in a section

![Fig. 7 Applying filters in a section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_filtered_section.png)

The number at the top right of the “funnel” icon represents the number of columns used in the currently applied filter.

note

If a filter uses several columns, then only the values that match all filter conditions will be displayed after applying the filter (similar to using the "AND" logical operator to group filter conditions in the desktop application).

To change the filter conditions, tap ![icn_Funnel1.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/icn_Funnel1.png).

Tap ![icn_cross.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/icn_cross.png) to remove the filter.

note

The filter settings will persist after updating the page or switching sections. The filters will reset upon logout.

You can filter data by string, lookup, numeric, and date columns. For example, if you need to filter data by an account name, tap a text column on the filter page and enter the full or partial filter value using the keyboard (Fig. 8).

Fig. 8 Filtering by a text column

![Fig. 8 Filtering by a text column](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_text_column_filter.png)

By default, all text column filters use the “starts with” condition. For example, if you enter the “Alpha” value in the **Name** column of the **Account** section and apply the filter, all companies with the name starting with “Alpha” will be displayed.

Use the “%” character to set “wildcard” filter values. For example, in the Accounts section, enter the "%Global" as the value of a **Name** column filter to display all companies that contain **Global** in their names (Fig. 9).

Fig. 9 Using the “%” character to specify text filter values

![Fig. 9 Using the “%” character to specify text filter values](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_special_character_filter.png)

## Edit records [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-16 "Direct link to Edit records")

You can edit data either in edit mode or in normal mode (when viewing data).

In view mode, you can make changes to the page's fields and embedded columns. You can also make changes to the page using the actions menu. In section page edit mode all columns are available for editing.

### Quick edit [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-28 "Direct link to Quick edit")

In normal mode (view mode), column values containing main information and communication options are available for editing.

For example, to change the name of the company where the contact works:

1. **Open** the **Contacts** section of the mobile application.

2. **Tap and hold** the **Account** column and drag it through the column to the left (Fig. 10).
Fig. 10 Editing a contact's Account column

![Fig. 10 Editing a contact's Account column](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_swap.png)

3. **Tap** the **Change** button.

4. **Select a value** from the lookup.

Communication options are edited in the same way in view mode.



note





To change, for example, the name of a contact, tap on the column and enter the value.


### Edit mode [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-18 "Direct link to Edit mode")

In the edit mode, you can edit a record:

1. **Tap** the **Edit** button in the upper right corner of the mobile application (Fig. 11)
Fig. 11 Editing records in mobile application

![Fig. 11 Editing records in mobile application](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_edit_page_choose.png)

2. **Enter the required values** on the edit page (Fig. 12).
Fig. 12 Editing mobile application section page

![Fig. 12 Editing mobile application section page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_edit_page_edit.png)

3. **Tap** **Save**.


## Run actions [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-22 "Direct link to Run actions")

Tap ![](https://academy.creatio.com/docs/sites/default/files/images/2020-12/btn_mobile_card_menu.png) in the lower part of the record to access the section actions menu.

The list of actions available in the actions menu depends on the opened section (Fig. 13).

Fig. 13 Contacts section actions menu

![Fig. 13 Contacts section actions menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app/BPMonlineHelp/chapter_mobile_overview/scr_mobile_overview_section_menu.png)

## Approve records [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#title-772-23 "Direct link to Approve records")

The approval functionality of Creatio desktop applications is available in the mobile app as well. After a record is submitted for approval in the main Creatio application, the assignee can approve or reject the record in the mobile app. To do this, use the **Approvals** section.

The **Approvals** section lists all records submitted for approval, including records from sections normally unavailable in the mobile app (Fig. 14). For example, you can approve a contract and an order using your mobile app, even if the app is not configured to display the **Contracts** and **Orders** sections. Read more about setting up mobile app sections in the [Mobile application wizard](https://academy.creatio.com/docs/user/no_code_customization/mobile_app_setup) article.

Fig. 14 Records submitted for approval in the mobile Approvals section

![Fig. 14 Records submitted for approval in the mobile Approvals section](https://academy.creatio.com/docs/sites/en/files/images/Platform_basics/Mobile_UI/scr_mobile_overview_visas_list.PNG)

Approvals require an active Internet connection.

To process an approval:

1. Open the **Approvals** section of the mobile application.

2. Swipe the record **left** to **approve a record**.

3. Swipe the record **right** to **reject a record**.

A few seconds after the swipe, you can **cancel** your approval or rejection using the cancel button in the notification at the bottom of the app.

As a result, the record will be approved or rejected. The app will display a notification about a successful approval processing to the approver. The approval status will be changed to “Positive” or “Negative”. The record will be no longer listed in the **Approvals** section.



note





Instead of swiping, you can tap a record in the **Approvals** section to open the approval page, then tap **Approve** or **Reject**. In that case, canceling the approval or rejection will not be available.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface\#see-also "Direct link to See also")

[Mobile application FAQ](https://academy.creatio.com/documents?id=1668)

[Get started with the mobile app setup](https://academy.creatio.com/documents?id=1945)

- [Search records](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-2)
- [Add records](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-3)
- [Filter records](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-4)
- [Edit records](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-16)
  - [Quick edit](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-28)
  - [Edit mode](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-18)
- [Run actions](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-22)
- [Approve records](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#title-772-23)
- [See also](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-interface#see-also)