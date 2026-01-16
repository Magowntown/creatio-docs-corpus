<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/functional-roles)** (8.3).

Version: 8.1

On this page

**Functional roles** reflect employee job titles, e. g., "Sales associates".

To manage functional roles, click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_system_designer.png) → **Functional roles**.

The **Functional roles** section contains the structure of functional roles (represented in the form of a folder tree) and the information about each functional role.

note

By default, only system administrators have access to this section. Users need to have permission to the "Manage user list" ("CanManageUsers" code) system operation to work with this section.

Use functional roles to set up identical access permissions for all employees with certain job positions, regardless of the company division. For example, you can create a functional role for managers in both main and regional offices. To do this:

1. **Create a functional role**. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#title-295-1)
2. **Connect the functional role** to needed organizational roles. [Read more >>>](https://academy.creatio.comtitle-295-2/)
3. **Configure access permissions** for a functional role. Learn more about access permissions in separate articles: [Object operation permissions](https://academy.creatio.com/documents?id=262), [Record permissions](https://academy.creatio.com/documents?id=1966), [Column permissions](https://academy.creatio.com/documents?id=264), [System operation permissions](https://academy.creatio.com/documents?id=258)

## Add a functional role [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles\#title-295-1 "Direct link to Add a functional role")

To create a functional role:

1. Click ![btn_system_designer00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_system_designer00001.png) → **Functional roles**.

2. Click **Add**. Specify the name of the role in the window that opens.



note





The name of a functional role must be unique.

3. Click **Save**.

4. Click ![btn_marketing_plans_detail_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_marketing_plans_detail_menu.png) → **Update roles** for changes to take effect (Fig. 1).
Fig. 1 Adding a functional role

![Fig. 1 Adding a functional role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/gif_section_users_add_functional_role.gif)


As a result, Creatio will add a new functional role.

## Connect functional and organizational roles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles\#title-295-2 "Direct link to Connect functional and organizational roles")

A functional role can be connected to one or more organizational roles. For example, you can connect the "Managers" functional role to the "Main office. Managers group" and "Regional office. Managers group" organizational roles.

To connect a functional role to an organizational role:

1. Click ![btn_system_designer00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_system_designer00002.png) → **Functional roles**.

2. **Select the corresponding functional role** in the list of functional roles. This opens the functional role page on the right.

3. Click ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_com_add_tab.png) on the **Organizational roles** tab and **add organizational roles** to include the functional role. For example, connect the "Managers" functional role to the "Main office. Managers group" and "Regional office. Managers group" organizational roles.

4. Click ![btn_marketing_plans_detail_menu00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_marketing_plans_detail_menu00003.png) → **Update roles** for changes to take effect (Fig. 2).
Fig. 2 Connecting functional and organizational roles

![Fig. 2 Connecting functional and organizational roles](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/gif_section_users_add_functional_role2.gif)


As a result, the "Managers" functional role will be connected to the "Main office. Managers group" and "Regional office. Managers group" organizational roles. This will grant all permissions of the "Managers" functional role to the users included in the "Main office. Managers group" and "Regional office. Managers group" organizational roles.

## Add users to a functional role [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles\#title-295-3 "Direct link to Add users to a functional role")

You can add users to the functional role in any of the following ways:

- Add an existing user (select a user from the list).
- Add a new user via a new user page.
- Import LDAP users. Learn more in a separate article: [Import new users and roles from Active Directory](https://academy.creatio.com/documents?id=1996).

Important

You can import LDAP users only if the LDAP user integration has been set up. Learn more in a separate article: [Set up LDAP synchronization](https://academy.creatio.com/documents?id=513).

To add users to a functional role:

1. Click ![btn_system_designer00004.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_system_designer00004.png) → **Functional roles**.

2. **Select the corresponding organization and/or division** in the list of functional roles.

3. Take the following steps on the **Users** tab:
1. Click ![btn_com_add_tab00005.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_com_add_tab00005.png) and select **Add existing** to **add an existing user**. Select the corresponding user in the pop-up window (Fig. 3).

2. Click ![btn_com_add_tab00006.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/btn_com_add_tab00006.png) and select **Add new** to **add a new user** assigned to this role. You will need to fill out the new user page.
      Fig. 3 Adding existing users to a functional role

      ![Fig. 3 Adding existing users to a functional role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/functional_roles/gif_section_users_add_users_to_functional_role.gif)

As a result, Creatio will add new or existing users to a functional role. Additionally, they will inherit any access permissions configured for this role.

note

Learn more about access permissions in separate articles: [Object operation permissions](https://academy.creatio.com/documents?id=262), [Record permissions](https://academy.creatio.com/documents?id=1966), [Column permissions](https://academy.creatio.com/documents?id=264), [System operation permissions](https://academy.creatio.com/documents?id=258).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles\#see-also "Direct link to See also")

[Add users](https://academy.creatio.com/documents?id=1441)

[Organizational roles](https://academy.creatio.com/documents?id=1434)

[Object operation permissions](https://academy.creatio.com/documents?id=262)

[Record permissions](https://academy.creatio.com/documents?id=1966)

[Column permissions](ihttps://academy.creatio.com/documents?id=264)

[System operation permissions](https://academy.creatio.com/documents?id=2000)

- [Add a functional role](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#title-295-1)
- [Connect functional and organizational roles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#title-295-2)
- [Add users to a functional role](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#title-295-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/functional-roles#see-also)