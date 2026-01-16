<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/change-the-system-user-supervisor#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/change-the-system-user-supervisor)** (8.3).

Version: 8.1

On this page

A dedicated user account called "System user" is required for the correct operation of Creatio. The system user must have the following permissions:

- System administrator (full access) permissions.
- Full license package.
- The user must be specified in the **System operations user** system setting.

By default, each configuration of Creatio has the "Supervisor" user account that is set as the system user.

note

If you do not have a "Supervisor" user in the system, make sure that the user specified in the **System operations user** system setting has a full license package and all access permissions.

Unlike system administrators, there can be only one system user in Creatio.

Important

You can rename or change the system user, but you can not delete the system user account altogether – this may lead to degradation of system performance.

A system user account is needed for both system administration/configuration and to ensure the correct operation of the entire system. For example, a system user account is used to index global search data, save changes in section and detail wizards, sending newsletters. Creatio may not function properly if a system user is deleted or their access rights or licenses have been removed.

1. Transfer the **maximum number of licenses** from the previous user to the new one.
2. Assign the role with **maximum access permissions** to the new system user, e.g. "System administrators".
3. Specify the new system user in the **System operations user** system setting.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/change-the-system-user-supervisor\#see-also "Direct link to See also")

[Functional roles](https://academy.creatio.com/documents?id=1438)

[Add a regular employee user](https://academy.creatio.com/documents?id=1441)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/change-the-system-user-supervisor#see-also)