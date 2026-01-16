<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/delegate-permissions)** (8.3).

Version: 8.1

On this page

The functionality of delegating permissions enables granting all access permissions of a user to another user for a limited time. This is useful when, for example, an employee is out of the office or otherwise unavailable and someone should take over their duties. You can delegate permissions of individual users or roles to any number of other users or roles.

To delegate permissions, a user must have access to the " **Manage user list**" (CanManageUsers) and " **Change delegated permissions**" (CanChangeAdminUnitGrantedRight) system operations.

## Delegate permissions of a user to other users and roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions\#title-292-1 "Direct link to Delegate permissions of a user to other users and roles")

To delegate user permissions to another employee or employee group:

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/btn_system_designer.png) → **System users**.

2. Open the user page, **whose permissions you want to delegate**.

3. Click **Rights delegation** → **Delegate permissions**.

4. In the opened window, select the user or employee group that **will receive the delegated permissions**, e.g., the "Accounting department" organizational role.

5. Click **Select**. Click **Close** on the user page.

6. Click **Actions** → **Update roles** to apply the changes.

As a result, the users and roles who received the permissions will be displayed in the **Who receives permissions** column, and the user/role, whose permissions were delegated, will be displayed in the **Who grants permissions** column on the **Access rights delegation** detail ( [Fig. 1](https://academy.creatio.com/#XREF_77385_Fig_493_Delegating)).
Fig. 1 Delegating permissions of a user to another user/employee group

![Fig. 1 Delegating permissions of a user to another user/employee group](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/gif_section_users_delegate_permissions.gif)


## Delegate permissions of other users and roles to a user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions\#title-292-2 "Direct link to Delegate permissions of other users and roles to a user")

To delegate permissions of other users and roles to a user:

1. Click ![btn_system_designer00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/btn_system_designer00001.png) → **System users**.

2. Open the page of a user, who **will receive the delegated permissions**.

3. Click **Rights delegation** → **Get permissions**.

4. In the opened window, select the user or role whose **permissions must be delegated** to the current user, e.g., the "Accounting department" organizational role.

5. Click **Select**. Click **Close** on the user page.

6. Click **Actions** → **Update roles** to apply the changes.

As a result, the user who received the permissions will be displayed in the **Who receives permissions** column, and the user/role, whose permissions were delegated, will be displayed in the **Who grants permissions** column on the **Access rights delegation** detail ( [Fig. 1](https://academy.creatio.com/#XREF_18194_Fig_494_Delegating)).
Fig. 1 Delegating permissions of an alternative user/employee group to the current user

![Fig. 1 Delegating permissions of an alternative user/employee group to the current user](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/gif_section_users_delegate_permissions2.gif)


## Remove the delegated user permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions\#title-292-3 "Direct link to Remove the delegated user permissions")

1. Click ![btn_system_designer00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/btn_system_designer00002.png) → **System users**.

2. Open the page of the user, whose **delegated permissions you want to remove**.

3. Open the **Rights delegation** tab, **click the record** you want to delete.

4. Click ![btn_marketing_plans_detail_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/btn_marketing_plans_detail_menu.png) → "Delete" ( [Fig. 1](https://academy.creatio.com/#XREF_22971_Fig_495_Removing)). **Close the user page**.

5. Click **Actions** → **Update roles** to apply the changes.
Fig. 1 Removing the delegated permissions

![Fig. 1 Removing the delegated permissions](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/delegating_permissions/gif_section_users_deleting_delegated_rights.gif)


As a result, the delegated permissions will be deleted. The user will only have the initially assigned permissions.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions\#see-also "Direct link to See also")

[Issue a license to a user](https://academy.creatio.com/documents?id=2309)

[Change the "system" user (Supervisor)](https://academy.creatio.com/documents?id=1756)

- [Delegate permissions of a user to other users and roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions#title-292-1)
- [Delegate permissions of other users and roles to a user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions#title-292-2)
- [Remove the delegated user permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions#title-292-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/delegate-permissions#see-also)