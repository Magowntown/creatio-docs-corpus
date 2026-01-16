<!-- Source: page_66 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

The mobile application includes the following detail types:

- **Embedded details** display all their records on the section record page regardless of the amount of data on the detail (Fig. 1).
Fig. 1 Job experience embedded detail on the section page

![Fig. 1 Job experience embedded detail on the section page](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_embedded_detail.png)

- **Standard details** do not display their records on the section page (Fig. 2). Tap a standard detail to view its records on a separate page.
Fig. 2 Activities and Invoices standard details

![Fig. 2 Activities and Invoices standard details](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_standard_detail.png)


You can add new details and configure the existing details in the Mobile Application Wizard.

## Add detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-1 "Direct link to Add detail")

### Add an embedded detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-2 "Direct link to Add an embedded detail")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/btn_system_designer.png) to **open the System Designer**.

2. **Go to** the **System setup** block → **Mobile Application Wizard**.

3. **Select the workplace** to edit → **Open**.

4. **Click** **Set up sections**.

5. **Select a section** in the list → **Page setup**.

6. **Click** **New** in the bottom → **Embedded detail** (Fig. 3). This opens a window.
Fig. 3 Add an embedded detail

![Fig. 3 Add an embedded detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_new_embedded_detail.png)

7. **Set the detail parameters** (Fig. 4):
Fig. 4 Set up an embedded detail

![Fig. 4 Set up an embedded detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_embedded_detail_parameters.png)



|     |     |
| --- | --- |
| **Parameter** | **Parameter value** |
| Detail | Select a detail to add. Required. Some of the existing details are designed for specific sections. Be sure to select the version of a detail whose name specifically indicates that the detail was designed for this particular section. For example, when adding the **Attachments** detail to the **Accounts** section page, select the “Account attachments” detail. |
| Title | Specify the detail title. |
| Detail column | Select the column that connects detail records to the current record in the section. Required. For example, records on the **Account addresses** detail in the **Accounts** section are connected to the **Accounts** section by the **Account** column. |
| Object column | Specify the column that contains the section ID. Required. Out of the box, it is “Id.” |

8. **Click** **Save**. As a result, a new detail will be added to the section page. For some details, the default columns might not be configured. In this case, you must add the displayed columns manually. Adding columns to a detail is similar to adding columns a section page. Learn more: [Set up mobile application section page](https://academy.creatio.com/documents?id=1394)

9. **Save the page**.


### Add a standard detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-3 "Direct link to Add a standard detail")

To ensure data on the standard detail is displayed correctly, add the corresponding section to the mobile application. For example, to display data on the **Documents** detail of the contact page, add the **Documents** section to the mobile application.

To add a standard detail:

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/btn_system_designer.png) to **open the System Designer**.

2. **Go to** the **System setup** block → **Mobile Application Wizard**.

3. **Select the workplace** to edit → **Open**.

4. **Click** **Set up details**. This opens a page

5. **Click** **New detail** (Fig. 5).
Fig. 5 Settings page of the section detail

![Fig. 5 Settings page of the section detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_standard_details.png)

6. **Set the detail parameters**:


|     |     |
| --- | --- |
| **Parameter** | **Parameter value** |
| Detail | Select a detail to add. Required. Some of the existing details are designed for specific sections. Be sure to select the version of a detail whose name specifically indicates that the detail was designed for this particular section. |
| Title | Specify the detail title. |
| Detail column | Select the column that connects detail records to the current record in the section. Required. For example, records on the **Documents** detail in the **Contacts** section are connected to the **Contacts** section by the **Owner** column. |
| Object column | Specify the column that contains the section ID. Required. Out of the box, it is “Id.” |

7. **Click** **Save**.

8. **Save the changes**.

9. Add the corresponding section to mobile application and configure it for the correct operation and display of details. For example, add the **Documents** section to the Mobile Application Wizard to display additional fields on the **Documents** detail page and set up fields on the edit page. Learn more: [Set up mobile application section page](https://academy.creatio.com/documents?id=1394).


The display order of standard details is determined by the order in which the details are added.

## Edit detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-4 "Direct link to Edit detail")

### Edit an embedded detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-5 "Direct link to Edit an embedded detail")

To edit embedded details, use the buttons next to the detail name (Fig. 6).

Fig. 6 Edit buttons for embedded detail

![Fig. 6 Edit buttons for embedded detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_edit_embedded_detail.png)

Click **Set** to edit the detail. Make your changes in the **Detail setting** window and click **Save**.

Use the ![btn_move_down_detail.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app_setup/BPMonlineHelp/mobile_app_setup_detail/btn_move_down_detail.png) and ![btn_move_up_detail.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/mobile_app_setup/BPMonlineHelp/mobile_app_setup_detail/btn_move_up_detail.png) buttons to modify the location of the detail on the section page.

To delete the embedded detail from the section page, click **Delete**.

### Edit standard detail [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#title-237-6 "Direct link to Edit standard detail")

To do this, open the detail configuration page (Fig. 7).

Fig. 7 Settings page of standard details

![Fig. 7 Settings page of standard details](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_standard_details.png)

To delete a standard detail from a section page, click the **Delete** button next to the detail name.

To modify the parameters of existing standard details, click the **Set** button next to the detail name. Setting up parameters of the standard detail is identical to setting up parameters of the embedded detail. Learn more: [Add an embedded detail](https://academy.creatio.com/documents?id=1395#title-237-2).

Fig. 8 Set up a standard detail

![Fig. 8 Set up a standard detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/mobile_detail_setup/scr_standard_detail_parameters.png)

You can specify a column of a connected object detail and configure data filtering by this object. For example, on the activity page, you can display the contacts connected to the account that is specified in the activity. To do this, add the **Contacts** detail to the activity record page and specify “Account” in both the **Detail column** and **Object column** fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail\#see-also "Direct link to See also")

[Set up mobile app workplaces](https://academy.creatio.com/documents?id=1391)

[Set up mobile application section list](https://academy.creatio.com/documents?id=1393)

[Set up mobile application section page](https://academy.creatio.com/documents?id=1394)

- [Add detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-1)
  - [Add an embedded detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-2)
  - [Add a standard detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-3)
- [Edit detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-4)
  - [Edit an embedded detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-5)
  - [Edit standard detail](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#title-237-6)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-app-setup/set-up-mobile-application-detail#see-also)