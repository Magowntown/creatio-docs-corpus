<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/object-operation-permissions)** (8.3).

Version: 8.2

On this page

This article covers the setup of **business data access permissions**. Access to business data involves CRUD data operations: create, read, update, and delete. To grant access to business data, configure access permissions to corresponding Creatio objects.

Configure object permissions on several levels:

- **Operation permissions**. This article covers the setup of data operation permissions for different Creatio objects: section and detail.
- **Record permissions**. Learn more in a separate article: [Record permissions](https://academy.creatio.com/documents?id=1966).
- **Column permissions**. Learn more in a separate article: [Column permissions](https://academy.creatio.com/documents?id=264).

**Access to functions** can be granted through system operations. Object operations are different from system operations. Set up system operation permissions in the **Operation permissions** section of the System Designer. Learn more in a separate article: [System operation permissions](https://academy.creatio.com/documents?id=258).

note

Certain system operations cancel any other object permission settings, namely: "View any data" ("CanSelectEverything" code), "Add any data" ("CanInsertEverything" code), "Edit any data" ("CanUpdateEverything" code), and "Delete any data" ("CanDeleteEverything" code). The user that has access to these operations receives permissions regardless of the settings in the **Object permissions** section.

Creatio includes the following object permissions out-of-the-box:

- "All employees" organizational role has permissions to create, read, update and delete any record in any object. Creatio also grants these permissions to "All employees" role for objects with "Use operation permissions" switch disabled.
- "All external users" organizational role has no operation permissions for Creatio records. To enable the users with this role to see their records and their organization's data in external sections, set up operation permissions for each section available for external users.
- "System administrators" organizational role has system operation permissions to add, view, edit and delete any data. These permissions have higher priority than object operation permissions.
- Technical users have no operation permissions for Creatio records. To enable the users of this type to interact with records, you need to set up operation permissions for each section separately.

## Configure access to operations in section objects [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions\#title-2265-1 "Direct link to Configure access to operations in section objects")

Example

Set up the following permissions to the **Opportunities** section:

Sales managers must have all permissions to section records except for the "Delete" permission.

Their managers must have full access to records.

One of the employees with the "Secretaries" role must have a permission to view the section records, while all other secretaries should not be able to view the **Opportunities** section at all.

1. Go to the System Designer (![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/btn_system_designer.png) button) and open the **Object permissions** section.

2. Select the necessary object in the list or use the search box. For example, to configure access permissions to the **Opportunities** section, select the "Sections" filter and choose the "Opportunity" object. Click the name (or title) of the object to open the object permission settings window (Fig. 1).
Fig. 1 Choosing the section object and opening the permissions settings window

![Fig. 1 Choosing the section object and opening the permissions settings window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_obgect_permissions_administer_by_operations_section.gif)

3. Enable the "Use operation permissions" switch (Fig. 2).
Fig. 2 Enable the Use operation permissions switch

![Fig. 2 Enable the Use operation permissions switch](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_objects_permissions_section_permissions_administer_by_operations.png)




Important





If you remove the "All employees" role from the settings area, and then disable the "Use operation permissions" switch and apply the changes, users will not be able to see the object records.

4. Click **Add** and select the necessary users and roles. You can use the search box or the **Organizational roles**, **Functional roles** and **Users** tabs to quickly find users and roles. In this case:
1. The "All employees" role (added automatically).

2. The "Sales managers" organizational role.

3. The "Sales managers. Managers group" organizational role.

4. The "Secretaries" organizational role.

5. An individual user from the "Secretaries" organizational role (Fig. 3), e. g., V. Murphy.
      Fig. 3 Adding users and roles to grant access permissions to the section

      ![Fig. 3 Adding users and roles to grant access permissions to the section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_obgect_permissions_administer_by_operations_adding_roles_and_users.gif)
5. By default, each user or role that you add is granted access to read, create, update and delete object data. Edit these permissions according to your requirements, for example:
1. Leave the **Read** checkbox selected and clear the **Create**, **Edit** and **Delete** checkboxes for the " **All employees**" role. As a result, all company employees can read section records but cannot create, edit or delete them.

2. Leave the **Read**, **Create**, **Edit** checkboxes selected and clear the **Delete** checkbox for the " **Sales managers**" role. As a result, sales managers will be able to read, create and edit section records without the ability to delete them.

3. Leave the **Read**, **Create**, **Edit** and **Delete** checkboxes selected for the " **Sales managers. Managers group**" role. As a result, sales department managers will have permission to read, create, edit or delete records in the **Opportunities** section.

4. Clear the **Read**, **Create**, **Edit** and **Delete** checkboxes for the " **Secretaries**" role. As a result, the **Opportunities** section will be hidden from the company’s secretaries.

5. Leave the **Read** checkbox selected for the **specific user in the "Secretaries" role**. As a result, the user can read records in the **Opportunities** section.

      ![icn_access_rights_priority.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/icn_access_rights_priority.png) icon might appear next to some permissions. This means that some settings contradict each other, and it is necessary to adjust their priorities.

## Create the hierarchy of object operation permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions\#title-2265-2 "Direct link to Create the hierarchy of object operation permissions")

Sometimes the access permissions that apply to the same user or role might contradict each other, since a user might be included in several roles. Also, organizational roles might inherit permissions from one another, for example, the "Sales managers," "Sales managers. Managers group," and "Secretaries" roles are a part of the "All employees" role. Additionally, permissions granted to an individual user might conflict with permissions that the user might have as a member of their role. These conflicts are indicated by the ![icn_access_rights_priority00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/icn_access_rights_priority00001.png) icon next to the conflicting access permission.

In case of a conflict, the permission that is the highest in the list will have a higher priority. The priority is shown in the **Priority** column and the highest possible priority is "0." An ![icn_access_rights_priority00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/icn_access_rights_priority00002.png) icon next to an access permission rule indicates such a conflict. You can drag a rule to change its position in the list (Fig. 4).

Fig. 4 The need to adjust priorities in the list of permission rules

![Fig. 4 The need to adjust priorities in the list of permission rules](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_objects_permissions_section_permissions_permission_priority.png)

**Please take the following into account** while configuring access permission priorities:

- A user who is a part of several roles will get the access permissions of the **highest** role in the list.

For example, all users should not access the **Opportunities** section records, but sales managers (who also belong to the "All users" role) should be given all permissions except those that enable them to delete records. To do this, place the "Sales managers" role higher than "All employees" in the list.

- To deny access permissions to an operation for a role while permitting the operation for some of its users, place this role **lower** in the list than the users who need to be granted access.

Thus, if you deny access to the **Opportunities** section for the "Secretaries" role, but grant permission to read data to one of the secretaries, make sure that you move the "Secretaries" below the secretary employee who is supposed to access to the section.

- Users or roles that are **not added** to the object operations settings area do not get access to operations and are not included in priority settings.


Configure access permission priorities. To change the rule display order, drag the rule to the necessary position in the list (Fig. 5).

1. Place the organizational role with the highest level of permissions (in our case, "Sales managers. Managers group") at the top of the list.

2. Place the "Sales managers" role directly below.

3. The "All employees" role and the "V. Murphy" user (who belongs to the "Secretaries" role) have the same access permissions. Thus, you can place them directly below the "Sales managers" role in any order.

4. The "Secretaries" role should be placed at the very bottom of the list since they do not have access to the **Opportunities** section.

5. Save the changes by clicking "Apply" in the upper left corner of the page.
Fig. 5 Set up the access permission priorities

![Fig. 5 Set up the access permission priorities](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_objects_permissions_section_permissions_result.png)


As a result:

- Users in the " **Sales managers**" role have access to the **Opportunities** section with the ability to create and edit section records. Sales managers do not have permission to delete records.
- Their **managers** should have full access to these records, including the permissions to delete them.
- **All company employees** can read section records but cannot create, edit or delete them.
- All **secretaries**, apart from V. Murphy, cannot view the **Opportunities** section records.
- **V. Murphy** can read the records in the section.

## Configure access to operations in detail objects [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions\#title-2265-3 "Direct link to Configure access to operations in detail objects")

Example

Configure access permissions to the **Attachments** detail in the **Contracts** section. Users in the "Sales managers" organizational role should have full access to detail records.

All other users can only view the files in the detail and cannot edit or delete them.

1. Go to the System Designer (![btn_system_designer00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/btn_system_designer00003.png) button) and open the **Object permissions** section.

2. Select the "All objects" filter.

3. Find the "Attachments" object via the search box.

4. Click the name or the title of the object to open the access permissions configuration window.

5. Enable the "Use operation permissions" switch (Fig. 6).
Fig. 6 Enable the Use operation permissions switch

![Fig. 6 Enable the Use operation permissions switch](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/chapter_objects_permissions_section_permissions_administer_by_operations_2.png)

6. Click **Add** and select the necessary users and roles. Use the search box to quickly find the necessary users and roles. In this case:
1. The "All employees" role (added automatically).
2. The "Sales managers" role.
7. By default, each user or role in the list is granted access to read, create, update and delete object data. Edit these permissions to fit the example requirements:
1. Leave the **Read**, **Create**, **Edit** and **Delete** checkboxes selected for the " **Sales managers**" role. As a result, sales managers can read, create, edit and delete data in the **Attachments** detail.
2. Leave the **Read** checkbox selected and clear the **Create**, **Edit** and **Delete** checkboxes for the " **All employees**" role. As a result, all employee users can view the data on the **Attachments** detail without the ability to add, edit or delete anything.
8. If necessary, configure access priorities for the selected roles. Adjustments might be necessary if access levels conflict with each other (roles might overlap). For example, the "Sales Managers" role is included in the "All Employees" role. These conflicts are indicated by the ![icn_access_rights_priority00004.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/operation_permissions/icn_access_rights_priority00004.png) icon next to the conflicting access permission. Learn more about priorities: [Create the hierarchy of object operation permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#title-2265-2).


As a result:

- Users in the " **Sales managers**" role have full access to the **Attachments** detail.
- **All company’s employees** can view the data on the **Attachments** detail without the ability to create, edit or delete anything.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions\#see-also "Direct link to See also")

[Record permissions](https://academy.creatio.com/documents?id=1966)

[Column permissions](https://academy.creatio.com/documents?id=2142&anchor=264)

[Object permissions by system operations](https://academy.creatio.com/documents?id=2553)

- [Configure access to operations in section objects](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#title-2265-1)
- [Create the hierarchy of object operation permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#title-2265-2)
- [Configure access to operations in detail objects](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#title-2265-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/object-operation-permissions#see-also)