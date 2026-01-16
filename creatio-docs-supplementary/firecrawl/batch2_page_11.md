<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/licensing/manage-user-licenses)** (8.3).

Version: 8.1

On this page

Licenses must be issued for each new Creatio user. Only licensed users can log in to Creatio and access the corresponding functionality. For example, users who were not issued a "marketing creatio product cloud" license, will not be able to use functions that are specific to Creatio Marketing, such as the **Bulk emails** and the **Campaigns** sections.

Before distributing licenses, ensure that the user role has permission to the "Manage user licenses" (`CanManageLicUsers` code) system operation. Out of the box, only users that have the "Creatio Maintenance," "Developer," "Administrator," "System administrators" role can execute the action. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=2000).

Important

To enable licensing a user account, Creatio must have available licenses that were not distributed among other users.

Set up licensing in the **License manager** section (Fig. 1).

Fig. 1 License manager section

![Fig. 1 License manager section](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing.png)

If the licenses expire, the license manager page opens for a user that has the "System administrators" role automatically when they log in to Creatio.

**General procedure to license Creatio**:

1. Add licenses to Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-1)
2. Distribute the available licenses among the users. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-230-2)

When working with Creatio, it can be necessary to manage user licenses, e.g., to distribute licenses to a new employee or recall licenses from a resigned employee. You can use the **Users** section as well as **License manager** section for this purpose.

## Add licenses to Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-229-1 "Direct link to Add licenses to Creatio")

The licensing process is similar for all types of licenses used in Creatio.

When purchasing licenses, extending available licenses, and updating Creatio on-site:

1. Generate a license request file and send it to [Creatio support](mailto:support@creatio.com).
2. The support team sends a file for you to upload to Creatio.

This procedure is also **required when updating Creatio on-site**.

### Generate a license request [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-229-2 "Direct link to Generate a license request")

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **License manager**.

2. **Click Actions** → **Request**.

3. **Enter the company ID** for licensing. Creatio provides the ID after the purchase. Alternatively, request it from [Creatio support](mailto:support@creatio.com).

4. **Click Generate a license request file** (Fig. 2). This generates a \*.tlr license request file.
Fig. 2 Generate a license request

![Fig. 2 Generate a license request](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_wnd_license_request.gif)

5. **Fill out the License version field** using the Creatio version to which you are going to update.

6. **Send the license request file to** [Creatio support](mailto:support@creatio.com). In response, the support team sends you a file that contains the information about purchased licenses.


You can also request licenses from the **Users** section by clicking **Request licenses** in the **Actions** menu (Fig. 3).

Fig. 3 Generate a license request

![Fig. 3 Generate a license request](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/8.3/scr_user_license_request.png)

**As a result**, the license request will be sent to Creatio support.

### Upload licenses to Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-229-3 "Direct link to Upload licenses to Creatio")

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **License manager**.

2. **Click Actions** → **Upload** (Fig. 4).
Fig. 4 Upload a license file to Creatio

![Fig. 4 Upload a license file to Creatio](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing00002.png)

3. **Specify the path to the license file** you saved earlier.


You can also upload licenses from the **Users** section by clicking **Upload licenses** in the **Actions** menu (Fig. 5).

Fig. 5 Upload a license file to Creatio

![Fig. 5 Upload a license file to Creatio](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing00002_user.png)

**As a result**, the new licenses will be uploaded to Creatio. The total license number might increase, and the available licenses will be extended.

## Ways to redistribute licenses [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-1472-5 "Direct link to Ways to redistribute licenses")

Creatio supports multiple ways to redistribute licenses. All ways use the same license redistribution rules.

Choose the appropriate way based on the business goals listed in the table below.

| Business goal | Way of license redistribution | Use cases |
| --- | --- | --- |
| Manually grant or revoke licenses for specific users without automation | Manual redistribution | - One-time or occasional adjustments<br>- Limited number of users<br>- Administrator needs full manual control<br>- No automation required |
| Automatically grant or revoke licenses according to license sets assigned to user roles | Role-based redistribution | - Recurring or large-scale redistribution tasks<br>- Medium or large number of users<br>- Administrator needs automation with predictable outcomes<br>- No manual intervention required during redistribution |

Creatio supports manual and role-based license redistribution and provides tools to automate role-based redistribution. Learn more: [Automate role-based license redistribution](https://academy.creatio.com/documents?id=15388) (developer documentation).

## Redistribute licenses manually [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-1472-1 "Direct link to Redistribute licenses manually")

To enable new employees to log in or use specific functions, their user accounts must be licensed. A system administrator can redistribute the available licenses at any time. Use this way when manual redistribution is required, for example, when you need to grant or recall licenses for specific users without involving any automation. The number of active and available licenses is displayed on the product licensing page and depends on the license type.

**Redistribute licenses manually** in the **License manager** or **Users** sections.

### Redistribute licenses manually for multiple users [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-230-2 "Direct link to Redistribute licenses manually for multiple users")

To redistribute licenses to multiple user accounts at once:

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Users**.
2. **Click Actions** → **Select multiple records**.
3. **Select the needed users** in the list.
4. **Click Actions** → **select Grant licenses** or **Recall licenses** depending on your business goals. This opens the **Select: Licensed configuration** window.
5. **Select the required records**.
6. **Click Select**.

**As a result**, the selected licenses will be redistributed for the selected user accounts.

### Redistribute licenses manually for a single user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-230-1 "Direct link to Redistribute licenses manually for a single user")

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Users**.

2. **Select the user** to whom the license must be redistributed.

3. **Go to the Licenses tab**.

4. **Select licenses** (Fig. 6).
Fig. 6 Select products for licensing

![Fig. 6 Select products for licensing](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/8.3/scr_chapter_licensing_user_page_select.png)


Similarly, you can recall the licenses.

5. **Click Save**.


**As a result**, the selected licenses will be redistributed for the user account.

## Redistribute licenses based on user roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-1472-2 "Direct link to Redistribute licenses based on user roles")

note

This functionality is available for Creatio 8.1.3 and later.

Creatio supports a role-based license redistribution to speed up the issuance of licenses to users. Out of the box, role-based license redistribution works for Creatio instances during **LDAP synchronization** or **Single Sign-On provisioning**. You can also configure it to trigger when user roles change.

Roles inherit licenses through the full hierarchy in the company's organizational structure. For example, if you have a "Support" organizational role that has "1st-line support", "2nd-line support" and "3rd-line support" child roles, then all users who do not belong directly to the "Support" role but are included in one of the child roles are provided with licenses from the "Support" and "All employees" organizational roles.

Before triggering role-based license redistribution, ensure that:

- The role of the user on whose behalf to redistribute the licenses has permission to the "Manage user licenses" (`CanManageLicUsers` code) system operation. Out of the box, only users that have the "Creatio Maintenance," "Developer," "Administrator," "System administrators" role can execute the action. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=2000).

- The `UseRoleBasedLicenseDistribution` additional feature is enabled. Out of the box, registered and enabled.

- The "Turn on role-based license redistribution after manual changes to user roles" (`RedistributeLicensesOnRoleChanges` code) system setting is set to "true." When "true," Creatio automatically recalculates user licenses after role changes or updates to role-bound licenses. Out of the box, "false." For LDAP or SSO–based role updates, this setting is not required.

- Licenses are distributed to the user roles. Otherwise, **distribute licenses to the user roles** manually. To do this:
1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Organizational roles** or **Functional roles**.
2. **Select the user role** for which licenses must be redistributed.
3. **Open the Licenses tab**.
4. **Click**![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_add_tab.png) on the **Licenses to distribute with roles** expansion panel.
5. **Select licenses** to be distributed to user role.
6. **Click Select**.

**As a result**, selected licenses will be bound to the role and automatically redistributed for all users included in the role during the LDAP synchronization process or JIT provisioning via SSO. If the **user is excluded from the role** in LDAP or SSO, the licenses will be removed accordingly.

Similarly, you can recall the licenses.

### Redistribute licenses for all active users based on assigned roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-1472-3 "Direct link to Redistribute licenses for all active users based on assigned roles")

To trigger role-based license redistribution without waiting for users to re-login via LDAP or SSO:

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Organizational roles** or **Functional roles**.

2. **Click**![icn_actions_in_roles.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/icn_actions_in_roles.png) → **Redistribute licenses for all roles** (Fig. 7).
Fig. 7 Redistribute licenses for all roles

![Fig. 7 Redistribute licenses for all roles](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/8.3/scr_redistribute_licenses_for_all_roles.png)

3. **Specify whether to keep or remove manually granted licenses**.

4. **Click OK**.


**As a result**, the selected licenses will be redistributed for all active users, and Creatio will display a system message in the **System messages** sidebar on the notification panel. If you do not recall user licenses that provide access to the product as part of redistribution, the redistribution process does not affect users in Creatio.

### Redistribute licenses for users based on assigned roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-229-6 "Direct link to Redistribute licenses for users based on assigned roles")

To trigger role-based license redistribution without waiting for users to re-login via LDAP or SSO:

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Organizational roles** or **Functional roles**.

2. **Select the user role** to whom the license must be redistributed.

3. **Click Actions** → **Redistribute licenses for the role** (Fig. 8).
Fig. 8 Redistribute licenses for the role

![Fig. 8 Redistribute licenses for the role](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/8.3/scr_chapter_licensing_redistribute.png)

4. **Specify whether to keep or remove manually granted licenses**.

5. **Click OK**.

6. **Repeat steps 2-5** for all the roles to redistribute licenses.


**As a result**, the selected licenses will be redistributed for all the users within selected roles, and Creatio will display a system message in the **System messages** sidebar on the notification panel. If you do not recall user licenses that provide access to the product as part of redistribution, the redistribution process does not affect users in Creatio.

### Redistribute licenses for a single user based on assigned roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-1472-4 "Direct link to Redistribute licenses for a single user based on assigned roles")

To trigger role-based license redistribution without waiting for users to re-login via LDAP or SSO:

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **Users**.

2. **Select the user** to whom the license must be redistributed.

3. **Open the Licenses tab**.

4. **Click**![scr_open_properties.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/PopulateDeliveryType/8.1/scr_open_properties.png) → **Redistribute licenses based on roles** (Fig. 9).
Fig. 9 Redistribute licenses based on roles

![Fig. 9 Redistribute licenses based on roles](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/8.3/scr_redistribute_licenses_based_on_roles.png)

5. **Specify whether to keep or remove manually granted licenses**.

6. **Click OK**.

7. **Repeat steps 2-6** for other users to redistribute licenses.


**As a result**, the licenses will be redistributed for the selected Creatio user. If you do not recall user licenses that provide access to the product as part of redistribution, the redistribution process does not affect users in Creatio.

## Delete licenses from Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#title-229-5 "Direct link to Delete licenses from Creatio")

Sometimes, deleting licenses is required. For example, if you need to switch Creatio to the demo mode.

To delete licenses from Creatio:

1. **Click**![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) in the top right → **Users and administration** → **License manager**.

2. **Click Actions** → **Delete** (Fig. 10).
Fig. 10 Deleting licenses

![Fig. 10 Deleting licenses](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_delete_license.gif)


**As a result**, Creatio will delete all licenses.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses\#see-also "Direct link to See also")

[Creatio licenses overview](https://academy.creatio.com/documents?id=1264)

[Automate role-based license redistribution](https://academy.creatio.com/documents?id=15388) (developer documentation)

[Workflow of role-based license redistribution](https://academy.creatio.com/documents?id=15390) (developer documentation)

- [Add licenses to Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-1)
  - [Generate a license request](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-2)
  - [Upload licenses to Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-3)
- [Ways to redistribute licenses](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-1472-5)
- [Redistribute licenses manually](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-1472-1)
  - [Redistribute licenses manually for multiple users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-230-2)
  - [Redistribute licenses manually for a single user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-230-1)
- [Redistribute licenses based on user roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-1472-2)
  - [Redistribute licenses for all active users based on assigned roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-1472-3)
  - [Redistribute licenses for users based on assigned roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-6)
  - [Redistribute licenses for a single user based on assigned roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-1472-4)
- [Delete licenses from Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#title-229-5)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses#see-also)