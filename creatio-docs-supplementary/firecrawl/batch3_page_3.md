<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/add-users)** (8.3).

Version: 8.2

On this page

Each Creatio user has a unique name and password to log in to the system. A user account is linked to a corresponding contact record and each contact record can only be linked to one user account. You can add users to Creatio in multiple ways:

- Create users manually in the **System users** section. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-4)
- Import users from Excel. [Read more >>>](https://academy.creatio.com/documents?id=2001)
- Import users and roles from LDAP. [Read more >>>](https://academy.creatio.com/documents?id=1996)
- Create users automatically during their first login via SSO. [Read more >>>](https://academy.creatio.com/documents?id=1759)

Manage Creatio users in the **System users** section. User settings determine what operations users can perform, what data they can see and how they can work with this data.

note

By default, only system administrators have access to the **System users** section.

Click ![btn_system_designer.png](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/btn_system_designer_8_shell.png) → **System users** to access the **System users** section.

## Add a regular employee user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-4 "Direct link to Add a regular employee user")

To create a new user account for a regular employee:

1. **Create a contact** for the new user in the **Contacts** section or make sure that the relevant contact already exists. If you use Studio Creatio without other Creatio apps, you can skip this step. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-5).
2. **Create a new user** in the **System users** section and specify the contact in the user profile. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-6).
3. **Assign the user a role**, if applicable. [Read more >>>](https://academy.creatio.com/documents?id=2005).
4. **Distribute licenses** to the user. [Read more >>>](https://academy.creatio.com/documents?id=2309).

### Add a new contact [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-5 "Direct link to Add a new contact")

1. **Go to the Contacts** section → **Create contact**.

2. **Fill out the required fields** on the contact mini-page and click **Save** (Fig. 3).
Fig. 1 Adding a new contact

![Fig. 1 Adding a new contact](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/gif_section_users_add_contact.gif)


**As a result**, a new contact will be added to Creatio, and you will be able to create a user for this contact.

note

You can also add a new contact directly from the contact lookup page when filling out the **Contact** field on the user page. Click ![btn_com_lookup.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_lookup.png) in the **Contact** field, then click **New** in the lookup box that pops up. Fill out the contact page that opens. After you save the contact page, you will return to the new user page, with the **Contact** field populated with the newly created contact.

### Create a user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-6 "Direct link to Create a user")

1. Click ![btn_system_designer.png](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/btn_system_designer_8_shell.png) → **System users**.

2. Click **New** → **Company employee** (Fig. 4). This opens the new page.
Fig. 2 Select a user type

![Fig. 2 Select a user type](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/scr_section_users_add_user.png)




note





You can change the type of the user ("Company employee" or External user") once you save the new user record and reopen the user page.

3. **Fill out the fields**:



| Field | Field value |
| --- | --- |
| Contact | Select the user’s contact in the **Contacts** section. |
| Type | Creatio populates the field automatically when you select the user type at step 2. Available values are "External user" or "Company employee". |
| Active | A status checkbox selected automatically for active users. Clear the checkbox to deactivate a user. |
| Culture | The UI language for the current user. Creatio populates the value automatically, the user can change the UI language in the user profile. The field displays active languages. To select other languages, activate them in the **Languages** section of the System Designer. Learn more about Creatio cultures: [Manage UI languages](https://academy.creatio.com/documents?id=1624). |
| Home page | Select a section page that will open by default when the user logs in to Creatio. If you leave the field empty, the user will be redirected to the Main Menu, and upon subsequent logins – to the last opened page during the previous session. |
| Date and time format | Specify the format that will be used to display dates for the user. You can leave the field empty, the user will be able to specify the format later in the user profile. |

4. **Fill out the Authentication detail**:



| Field | Field value |
| --- | --- |
| Username | Enter the Creatio user login. This is a required field. |
| Email | Enter the Creatio user login email. If you fill out this field, the user will be able to log in with either the username or the email. |
| Password, Password confirmation | Enter the password the user will use to log in to Creatio. These are required fields. |
| Password expiration date | The field is non-editable and displays the date when the password expires. The date is calculated based on the **Default value** field of the "Password validity term, days" ("MaxPasswordAge" code) system setting. The value is set to "0" out of the box, in which case the password has no expiration date, and the **Password expiration date** field on the user page remains blank and locked. |
| Reset password | Select this checkbox if you want to force the user to change their password when logging in for the next time. If the checkbox is selected on the user page, Creatio will notify the user that their password has expired and request changing it at the next login attempt. |




note





If you use the LDAP authentication, select the **LDAP authentication** checkbox and specify the username from the LDAP lookup in the **Username** field. The lookup in this field contains the list of LDAP users that have not been synchronized with Creatio yet. Learn more: [Set up LDAP synchronization](https://academy.creatio.com/documents?id=513).

5. **Save the page**.


**As a result**, a new user for a company employee will be added to Creatio.

## Add a system administrator user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-1 "Direct link to Add a system administrator user")

Out-of-the-box Creatio has a "System administrators" organizational role whose members have full access to all data in Creatio. This is achieved through access to the following system operations:

- "Add any data" ("CanInsertEverything" code)
- "Delete any data" ("CanDeleteEverything" code)
- "Edit any data" ("CanUpdateEverything" code)
- "View any data" ("CanSelectEverything" code)

Learn more: [Description of system settings](https://academy.creatio.com/documents?id=1259).

To **add a new system administrator user** in Creatio:

1. **Create a contact** for the new user or make sure that the relevant contact already exists in the **Contacts** section. Learn more: [Add a new contact](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-5).

2. **Create a new user** in the **System users** section and specify the contact in the user profile. Learn more: [Create a user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-6).

3. **Add the user to the "System administrators" role**.



Important





Access to these operations overrides any object permissions a user might have. For example, a user that has permission to the "View any data" system operation can view all records in objects, even if you try to deny the "Read" permission for that user in the object permission UI.


You can assign the system administrator role to a user in multiple ways:

- from the user page
- from the role page

### Method 1. Assign a system administrator role to a user from the user’s page [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-2 "Direct link to Method 1. Assign a system administrator role to a user from the user’s page")

1. Click ![btn_system_designer.png](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/btn_system_designer_8_shell.png) → **System Designer** → **System users**.

2. **Open the user page** → the **Roles** tab.

3. Click ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_add_tab.png) in the **Organizational roles** detail and **specify the "System administrators" role** (Fig. 1).
Fig. 3 Assigning a system administrator role to a user from the user’s page

![Fig. 3 Assigning a system administrator role to a user from the user’s page](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/gif_section_users_add_sys_admin1.gif)


**As a result**, the user will be added to the "System administrators" role and will receive full access to all Creatio data.

### Method 2. Assign a system administrator role to a user from the role page [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#title-2067-3 "Direct link to Method 2. Assign a system administrator role to a user from the role page")

1. Click ![btn_system_designer.png](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/btn_system_designer_8_shell.png) → **Organizational roles**.

2. **Select the "System administrators" role** in the list of organizational roles represented in the form of a folder tree. The area to the right of the roles tree will show the page of the selected role.

3. On the **Users** tab:
1. Click ![btn_com_add_tab00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_add_tab00003.png) and select **Add existing** to **add an existing user**. This opens a window.

2. Select the corresponding user (Fig. 2).

3. Click ![btn_com_add_tab00004.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_add_tab00004.png) and select **Add new** to **add a new user** assigned to this role. You will need to fill out the new user page.
      Fig. 4 Assigning a system administrator role to a user via the Organizational roles section

      ![Fig. 4 Assigning a system administrator role to a user via the Organizational roles section](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/gif_section_users_add_sys_admin2.gif)

**As a result**, the user will be added to the "System administrators" role and will receive full access to all data in Creatio.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users\#see-also "Direct link to See also")

[Assign a user role](https://academy.creatio.com/documents?id=2005)

[Issue a license to a user](https://academy.creatio.com/documents?id=2309)

- [Add a regular employee user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-4)
  - [Add a new contact](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-5)
  - [Create a user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-6)
- [Add a system administrator user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-1)
  - [Method 1. Assign a system administrator role to a user from the user’s page](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-2)
  - [Method 2. Assign a system administrator role to a user from the role page](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#title-2067-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/add-users#see-also)