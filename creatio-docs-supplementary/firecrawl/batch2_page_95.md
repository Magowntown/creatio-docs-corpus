<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/system-operation-permissions)** (8.3).

Version: 8.2

On this page

Access to a number of Creatio functions cannot be managed via permissions to add, view, edit and delete data in objects. Examples of such functions are import and export operations, creating business processes, configuring workplaces, system configuration, etc. Use **system operations** to manage access to these functions. A system operation can have one of the two access levels: a user or role either have access to perform the operation, or they do not. For example, if you grant the "All employees" role permission to perform the "Export list records" system operation, all users will be able to export section list data as Excel files.

The **Operation permissions** section of the System Designer is designed for managing access to system operations. Although standard folders are not available in the list of system operations, you can use either a [standard](https://academy.bpmonline.com/documents?product=base&ver=7&id=1233) or an [advanced filter](https://academy.bpmonline.com/documents?product=base&ver=7&id=1234) to find the needed operation.

Please note that system operation permissions work in conjunction with other access permissions. For example, users can only export data, which they can access according to object permissions.

By default, only system administrators have access to key system operations. You can configure access permissions to system operations for individual users or user groups.

Example

Set up access to the **Export to Excel** system operation for the sales supervisors.

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_system_designer.png) → System Designer → **Operation permissions**

2. Apply the "Name = Export list records" (or "Code = CanExportGrid") filter. **Click the name of the operation** to open it.

3. Click ![btn_mobile_add_product.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_mobile_add_product.png) and specify the necessary **user/role** on the **Operation permission** detail. For example the "Sales managers. Managers group" organizational role. The user/role will show up on the **Operation permission** detail with the "Yes" value in the "Access level" column. As a result, the "Sales managers.Managers group" role will be able to export section data to Excel (Fig. 1).
Fig. 1 Granting access permissions to a system operation

![Fig. 1 Granting access permissions to a system operation](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/gif_section_operations_permissions_add_permission.gif)


note

To deny access permissions, click a record on the **Operation permission** detail and change the value in the "Access level" column to "No". To do this, select the user or role in the list. The "Access level" column value will be displayed as a checkbox. Clear it to deny access permissions for the selected user/role. Please do not forget to save.

Sometimes a user may be assigned conflicting permissions to system operations. This may happen if the user is a member of several roles, some of which have permission to a system operation, and some are denied that permission. In order for access permissions to work correctly, make sure you properly configure their priority. Use ![btn_move_down_detail.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_move_down_detail.png) or ![btn_move_up_detail.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_move_up_detail.png) on the **Operation permissions** detail to change the priority of assigned operation permissions. The role that is the highest in the list will determine the actual access permissions of a user. For example, if you need to deny permission to export list records for all users except sales managers, place the "All Employees" role lower than the "Sales managers" role in the list.

note

Users or roles that were not added to the **Operation permission** detail will not have access to perform the corresponding system operation. In addition, they will not affect the permission priorities.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-permissions\#see-also "Direct link to See also")

[System operation reference](https://academy.creatio.com/documents?id=2386)

[Object permissions by system operations](https://academy.creatio.com/documents?id=2553)

[Object operation permissions](https://academy.creatio.com/documents?id=262)

[Add users](https://academy.creatio.com/documents?id=1441)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-permissions#see-also)