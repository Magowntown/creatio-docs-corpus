<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/import-users-from-excel)** (8.3).

Version: 8.1

On this page

You can quickly add multiple users to Creatio by importing them from Excel. Learn more: [Excel data import](https://academy.creatio.com/documents?id=1252).

Import data into the "System administration object" that corresponds to the "SysAdminUnit" table in the database. This object contains the company's organizational structure: users, organizational and functional roles.

To import users from Excel:

1. **Prepare the file for import** and fill out the needed columns. Learn more: [Prepare an Excel file for importing users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-1).
2. Download the file and **import users** to the system. Learn more: [Run the import process](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-2).
3. **Set up user records**: assign roles, specify passwords and available licenses. Learn more: [Set password, role, and grant licenses to the imported users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-3).

## Prepare an Excel file for importing users [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel\#title-296-1 "Direct link to Prepare an Excel file for importing users")

Create an \*.xlsx document. The document should contain the "Name" and "Type" fields, where you specify the login and type values. You can optionally populate the rest of the columns.

| Column name | Column value in the imported Excel file |
| --- | --- |
| Name | User’s login name. This column is required. |
| Type | Specify "4" to import records as users. This column determines the type of administration unit that is imported – either a role or a user. These types are stored in the "Object Permission Types (SysAdminUnitType)" object. You can find the possible values of this table below. This column is required. |
| Contact | Specify the name of the user’s contact. The names that you specify in the "Contact" column of your user import file must match the names of corresponding contacts in Creatio, otherwise Creatio will create new contacts. This column is optional. If you do not populate it, Creatio create new contacts using username as the contact’s name. |
| Active | The following values can be used:<br>- "0" for deactivated users<br>- "1" for active users<br>This column is optional. By default, all users are active. |
| Culture | Specify the user language code (e. g., the "en-US" for English UI). Learn more about Creatio cultures: [Manage UI languages](https://academy.creatio.com/documents?id=1844). This column is optional. By default, the users will use English localization. |
| Connection type | The connection type determines the access permissions inherited by the user.<br>- "0" for company employees<br>- "1" for portal users<br>This column is optional. By default, all users are imported as employees. |

View the values of "Object Permission Types" (SysAdminUnitType) object in the table below.

| System administration unit type | "Type" column value | "Connection type" column value |
| --- | --- | --- |
| Organization | 0 | 0 |
| Organizational unit | 1 | 0 |
| Manager | 2 | 0 |
| User | 4 | 0 |
| Portal user | 4 | 1 |
| Functional role | 6 | 0 |

Learn more about general requirements for the imported Excel file: [Prepare a file](https://academy.creatio.com/documents?id=1252&anchor=title-764-1).

## Run the import process [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel\#title-296-2 "Direct link to Run the import process")

To import users from Excel:

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/import_users_from_excel/btn_system_designer.png) System Designer → **Data import** (Fig. 1).
Fig. 1 The link to the Data import functionality in the Import and integration block

![Fig. 1 The link to the Data import functionality in the Import and integration block](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/import_users_from_excel/section_users_data_import_link.png)

2. **Add your user import Excel file**: drag it to the Data Import page that opens, or click **Select file** and locate your Excel file.

3. Click **Other** and select " **System administration object**" as the object for importing file records (Fig. 2). Click **Next**.
Fig. 2 Select an object for the import on the Data Import page

![Fig. 2 Select an object for the import on the Data Import page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/import_users_from_excel/scr_section_users_add_excel_file_users.png)

4. Specify the **column mapping** by connecting the columns from the Excel file to the fields in the Creatio import object (Fig. 3). Click **Next**.
Fig. 3 Map the columns

![Fig. 3 Map the columns](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/import_users_from_excel/scr_section_users_map_columns.png)

5. **Specify the conditions to identify duplicate records**. The data of these columns must be unique for each of the imported records (Fig. 4).

If the value of a column in the imported file coincides with the database value, Creatio will update the existing record. If the value is not available in the database, Creatio will create a new record.

For example, when importing users, use the "Contact" column to determine whether the imported record already exists. If contact with such a name does not exist, Creatio creates a new record.
Fig. 4 Manage duplicates

![Fig. 4 Manage duplicates](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/import_users_from_excel/scr_section_users_duplicate_management.png)

6. Click **Start data import**.



note





Learn more about how to set up columns and duplicate parameters: [Import a customer database](https://academy.creatio.com/documents?id=1252&anchor=title-764-2).





When the import process completes, Creatio will inform you accordingly.

As a result, the imported records will be displayed in Creatio user record list. Note that the imported users will not have roles, licenses or passwords. You will need to assign those manually.


## Set password, role, and grant licenses to the imported users [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel\#title-296-3 "Direct link to Set password, role, and grant licenses to the imported users")

After you complete the import, you need to perform the following steps manually for each imported user:

1. On the **General information** tab of the user page, **set a password** to enable the user to log in to Creatio.



note





Users can change their password when logging in to Creatio for the first time. Learn more: [Create a user](https://academy.creatio.com/documents?id=1441&anchor=title-287-6).

2. **Select the necessary role** (e. g., "All employees") on the **Roles** tab. Learn more: [Assign a user role](https://academy.creatio.com/documents?id=2005).

3. **Distribute licenses** on the **Licenses** tab. Learn more: [Issue a license to a user](https://academy.creatio.com/documents?id=2309).


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel\#see-also "Direct link to See also")

[How to prepare an Excel file for import](https://academy.creatio.com/documents?id=1587)

[How to import customer database](https://academy.creatio.com/documents?id=1588)

- [Prepare an Excel file for importing users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-1)
- [Run the import process](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-2)
- [Set password, role, and grant licenses to the imported users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#title-296-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/import-users-from-excel#see-also)