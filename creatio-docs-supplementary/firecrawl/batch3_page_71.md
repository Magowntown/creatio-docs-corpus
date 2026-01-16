<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/organizational-roles)** (8.3).

Version: 8.2

On this page

**Organizational roles** are user groups that represent company units, departments or subdivisions in the organizational structure, for example, the "Boston Office Sales Department" or the "Washington Office HR Department." Each organizational role can be assigned access permissions that apply to all of its users. Organizational roles also automatically inherit access permissions from their parent organizational roles.

To manage organizational roles, click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_system_designer.png) → **Organizational roles**.

The **Organizational roles** section contains the company’s organizational structure (represented in the form of a folder tree) and the information about individual organizational roles.

note

By default, only system administrators have access to this section. Users need to have permission to the "Manage user list" ("CanManageUsers" code) system operation to work with this section.

### Add an organizational role [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles\#title-2266-1 "Direct link to Add an organizational role")

1. Click ![btn_system_designer00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_system_designer00001.png) → **Organizational roles**.

2. In the list of organizational roles, **select the corresponding parent role**. For example, an organizational role for the regional office.

3. Click **Add** and **select the role type**: "Organization" or "Division." For example, create a "Marketing department" division for the regional office.

4. Enter the **name** of the role. The name of each organizational role must be unique.

5. Open the **Functional roles** tab and add functional roles. For example, "Marketing Manager," "Copywriter," etc. All users in these functional roles will obtain all permissions of the organizational role.

This step is optional.



note





Alternatively, you can connect a functional role to an organizational role on the functional role page. Read more: [Connect functional and organizational roles](https://academy.creatio.com/documents?id=1438&anchor=title-295-2).

6. Click ![btn_marketing_plans_detail_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_marketing_plans_detail_menu.png) → **Update roles** for changes to take effect (Fig. 1).
Fig. 1 Adding an organizational role

![Fig. 1 Adding an organizational role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/gif_section_users_add_organization_role.gif)


As a result, a new organizational role will be added to Creatio. It will automatically obtain the same access permissions as its parent organizational role.

## Add a management role [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles\#title-2266-2 "Direct link to Add a management role")

Set up special access permissions for management staff by adding a **management role** to an organizational role. The management role exists as a standalone organizational role in Creatio and may have its own access permissions, but it is not visible in the list of organizational roles.

Management role inherits the subordinate role's and users access permissions automatically.

To add a management role:

1. Click ![btn_system_designer00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_system_designer00002.png) → **Organizational roles**.

2. Select the corresponding organization and/or division to assign a management role in the list of organizational roles. For example, to assign a manager to the HR Department, select the "HR Department" role.

3. Select the **Management role exists** checkbox on the **Managers** tab.

4. Specify the name of the management role (Fig. 2) in the **Management role** field.
Fig. 2 Creating a management role for the HR Department organizational role

![Fig. 2 Creating a management role for the HR Department organizational role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/gif_section_users_add_manager_role.gif)

5. Take the following steps on the **Managers** tab:
1. Click ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_com_add_tab.png) and select **Add existing** to **add an existing user**. Select the corresponding user in the pop-up box (Fig. 3).

2. Click ![btn_com_add_tab00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_com_add_tab00003.png) and select **Add new** to **add a new user** assigned to this role. You will need to fill out the new user page.
      Fig. 3 Adding users to the HR Department management role

      ![Fig. 3 Adding users to the HR Department management role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/gif_section_users_add_managers_to_role.gif)

As a result, the management role will be added to the organizational role. The users that have the management role will obtain all access permissions of the role, including permissions inherited from the subordinate role (e. g., "HR Department").

Sometimes, managers can inherit unnecessary permissions. For example, if an employee was granted extended permissions to accomplish tasks. You can restrict the automatic delegation of permissions for specific roles to ensure the managers do not inherit unneeded permissions.

To do this, add the needed organizational or functional roles to the "User roles not inherited by managers" [lookup](https://academy.creatio.com/documents?id=1899). By default, the lookup includes the "System administrators" role.

Learn more in separate articles: \[Object operation permissions\](a href= [https://academy.creatio.com/documents?id=262](https://academy.creatio.com/documents?id=262)), [Record permissions](https://academy.creatio.com/documents?id=1966), [Column permissions](https://academy.creatio.com/documents?id=264), [System operation permissions](https://academy.creatio.com/documents?id=258).

## Add users to an organizational role [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles\#title-2266-3 "Direct link to Add users to an organizational role")

You can create a list of users in an organizational role in any of the following ways:

- add an existing user (selecting a user from the list)
- add a new user via a new user page
- import LDAP users

Important

You can import LDAP users only if the LDAP user integration has been set up. Learn more: [Set up LDAP synchronization](https://academy.creatio.com/documents?id=513).

All users added to the organizational role will inherit any access permissions configured for it.

To add users to an organizational role:

1. Click ![btn_system_designer00004.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_system_designer00004.png) → **Organizational roles**.

2. **Select the corresponding organization and/or division** in the list of functional roles represented as a folder tree.

3. Take the following steps on the **Users** tab:
1. Click ![btn_com_add_tab00005.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_com_add_tab00005.png) and select **Add existing** to **add an existing user**. Select the corresponding user in the pop-up box (Fig. 4).

2. Click ![btn_com_add_tab00006.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/btn_com_add_tab00006.png) and select **Add new** to **add a new user** assigned to this role (you will need to populate the new user page).
      Fig. 4 Adding existing users to an organizational role

      ![Fig. 4 Adding existing users to an organizational role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/organizational_roles/gif_section_users_add_users_to_organizational_role.gif)

As a result, selected users will be added to the organizational role. The users will inherit any access permissions configured for the organizational role.

note

Learn more about access permissions in separate articles: [Object operation permissions](https://academy.creatio.com/documents?id=262), [Record permissions](https://academy.creatio.com/documents?id=1966), [Column permissions](https://academy.creatio.com/documents?id=264), [System operation permissions](https://academy.creatio.com/documents?id=258).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles\#see-also "Direct link to See also")

[Functional roles](https://academy.creatio.com/documents?id=1438)

[Object operation permissions](inthttps://academy.creatio.com/documents?id=262)

[Record permissions](https://academy.creatio.com/documents?id=1966)

[Column permissions](https://academy.creatio.com/documents?id=264)

[System operation permissions](https://academy.creatio.com/documents?id=2000)

- [Add an organizational role](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles#title-2266-1)
- [Add a management role](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles#title-2266-2)
- [Add users to an organizational role](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles#title-2266-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/user-management/organizational-roles#see-also)