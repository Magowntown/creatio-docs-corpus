<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/column-permissions)** (8.3).

Version: 8.1

On this page

Configure object permissions on several levels:

- **Operation permissions**. Learn more in a separate article: [Object operation permissions](https://academy.creatio.com/documents?id=262).
- **Record permissions**. Learn more in a separate article: [Record permissions](https://academy.creatio.com/documents?id=1966).
- **Column permissions**. This article explains how to configure permissions to read, edit, and delete **individual columns** of a particular object.

**Object columns** are displayed as fields on pages and section/detail lists. Column permissions let you limit access to read or edit individual object fields for individual users or roles. For example, you can limit permissions to read data in the **Annual revenue** field for the "Secretaries" organizational role and enable all other employees to read the data in that field. The users who do not have permission to read data in the **Annual revenue** field will see the field itself, but not its value (Fig. 1).

Fig. 1 The Annual revenue field with restricted access permissions

![Fig. 1 The Annual revenue field with restricted access permissions](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/chapter_object_permissions_column_permissions_result.png)

For security reasons, system columns ("Created on," "Created by," "Modified on," "Modified by," "Id") are not available for **external users**. If you want to display a system column to external users in the list, set up the list as a system user.

[Operation permissions](https://academy.creatio.com/documents?id=262) override column permissions for particular users or roles. For example, if the user lacks permission to read object data, Creatio does not display the object for the user at all.

If you do not add a column to the detail or do not specify any access permissions for a column on the detail, Creatio grants access to the column according to the operation permissions.

If you add a new column to an object that has column permissions set up, Creatio grants permissions to read the column to all users automatically.

Important

Before you set up object column permissions, make sure that the user or role has access to the corresponding object operations and records. Note that if an object is not managed by operations and records, all users and roles have full access to all operations and all records. Learn more in a separate article: [Object operation permissions](https://academy.creatio.com/documents?id=262).

## Assign column permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions\#title-2264-1 "Direct link to Assign column permissions")

This section covers how to grant or limit access permissions to read and edit data of a particular section record field.

Example

Set up permissions to the **Annual revenue** field on the account page. All company’s employees, apart from its secretaries, must have permissions to read the data in the **Annual revenue** field, while the sales managers must have permissions to read and edit data in that field.

The field value must be hidden for the company’s secretaries.

1. Click the ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/btn_system_designer.png) button to open the System Designer → the " **Object permissions**" section.

2. Select the necessary object in the list or use the search bar. For example, to configure access permissions to the **Annual revenue** field, select the "Sections" filter and choose the "Account" object. Click the name (or title) of the object to open the object permissions settings window.

3. Make sure that the necessary users or roles already have access to object operations or that the object is not administered by operations.

4. Enable the "Use column permissions" toggle (Fig. 2).
Fig. 2 Enable the column permissions

![Fig. 2 Enable the column permissions](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/chapter_object_permissions_section_permissions_administer_by_columns.png)

5. Click **Add** and select the necessary column. For example, to limit access to the **Annual revenue** field, type "Annual revenue" in the search box and click **Select**. The selected column will be displayed in the list on the left. The list on the right lets you select users and roles to configure access permissions (Fig. 3). You can add other columns, if necessary. Select a column in the list to configure its access permissions.

6. Click **Add** in the list on the right, then select users and roles. You can use the search bar or the **Organizational roles**, **Functional roles** and **Users** tabs to quickly find users and roles in the selection box (Fig. 3). In this example, the roles are as follows:


   - the "All employees" role (added automatically)

   - the "Sales managers" organizational role

   - the "Secretaries" organizational role
     Fig. 3 Selecting the Annual revenue column and adding users and roles to configure access permissions

     ![Fig. 3 Selecting the Annual revenue column and adding users and roles to configure access permissions](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/chapter_object_permissions_administer_by_columns_adding_roles_and_users.gif)


By default, each user or role added to the list gets permissions to read, update and delete the object field. Modify permissions to restrict access. For example:

1. Change access permissions for the " **All employees**" role to "Permit reading". As a result, all company’s employees will be able to see the **Annual revenue** field value on the account page without the ability to edit it.
2. Select the "Permit reading and editing" access permission level for the " **Sales managers**" role. As a result, the sales managers will be able to read and edit the value of the **Annual revenue** field.
3. Select the "Deny reading and editing" access permissions level for the " **Secretaries**" role. As a result, the company’s secretaries will not be able to see the value of the **Annual revenue** field.

After you apply the settings, the ![icn_access_rights_priority.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/icn_access_rights_priority.png) icon can appear next to some permissions. This means the permissions are in conflict. Change their priority so that Creatio can apply the permissions correctly.

## Hierarchy of column permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions\#title-2264-2 "Direct link to Hierarchy of column permissions")

Sometimes, different access permissions applied to the same user or role can contradict each other.

For example, the "Sales Managers" and the "Secretaries" roles are included in the "All Employees" role. Sales managers have more permissions than regular employees (Fig. 4).

Fig. 4 Permission levels that contradict each other

![Fig. 4 Permission levels that contradict each other](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/chapter_object_permissions_column_permissions_priority.png)

The higher the permission is in the list, the higher the permission priority. The priority is shown in the **Priority** column, and the highest possible priority is "0". An ![icn_access_rights_priority00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/icn_access_rights_priority00001.png) icon next to some of the rules indicates that they overlap. Lower or raise a rule in the list to ensure other rules work correctly.

**Follow these rules** while configuring access permission priorities:

- Object operation permissions and record permissions have higher priority.

- A user who has several roles will get the access permissions of the highest role in the list.

For example, you can deny editing access for all employees, and grant sales managers the permissions to read and edit this field. To do this, place the "Sales managers" role higher than "All employees" in the list.

- If you want to deny column access for a role that is included in the role that has a higher permission level, place the role to deny access higher than the parent role.

For example, to deny access to read and edit column data for all secretaries, place the "Secretaries" role higher than the "All employees" role that has permissions to read the column data in the list. In this case, Creatio will display the ![icn_access_rights_priority00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/icn_access_rights_priority00002.png) icon next to the "Secretaries" role.



note





In this case, you do not need to change the priority, since the contradiction means the secretaries will be unable to view the column value, which is the intended behavior.

- The access permissions for users or roles that have not been added to the column permissions settings area correspond to the object operation permissions that are configured for them.


Configure access permission priorities for the example above. To change the rule display order, drag the rule to the necessary position in the list (Fig. 5).

1. Place the organizational role that has the highest permission level (in this example, "Sales managers") at the top of the list.
2. Place the "Secretaries" role directly below the "Sales managers" role.
3. Place the "All employees" role at the very bottom of the list.
4. Save the settings.

Fig. 5 Configure the priority of column access permissions

![Fig. 5 Configure the priority of column access permissions](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/column_permissions/chapter_object_permissions_column_permissions_priority_2.png)

As a result:

- Users that are part of the " **Sales managers**" role will be able to read and edit the **Annual revenue** field value.
- All **secretaries** will not be able to see the **Annual revenue** field value on the account page.
- **All company’s employees** will be able to see the **Annual revenue** field value on the account page, without the ability to edit it.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions\#see-also "Direct link to See also")

[Object operation permissions](https://academy.creatio.com/documents?id=262)

[Record permissions](https://academy.creatio.com/documents?id=1966)

* * *

- [Assign column permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions#title-2264-1)
- [Hierarchy of column permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions#title-2264-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/column-permissions#see-also)