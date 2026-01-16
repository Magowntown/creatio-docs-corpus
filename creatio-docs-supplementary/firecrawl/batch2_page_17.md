<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory)** (8.3).

Version: 8.1

On this page

If you use the Active Directory service, you can import users from your directories to Creatio via LDAP synchronization. This will let you copy users and roles from Active Directory to Creatio.

## Prepare the directory for integration [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory\#title-2019-18 "Direct link to Prepare the directory for integration")

Prepare the directory for integration before you start adding users via LDAP synchronization:

1. Make sure that the users are assigned to the AD user groups you are going to synchronize with Creatio. Creatio will not import Active Directory (AD) users that do not belong to any AD user group. Creatio only imports the organizational structure represented by the AD user groups.
2. [Set up LDAP integration](https://academy.creatio.com/documents?id=513). After you click **Save** on the LDAP integration setup page, Creatio will run a business process that imports users and roles from LDAP in the background and send you a corresponding notification.

## Import new users from LDAP [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory\#title-2019-19 "Direct link to Import new users from LDAP")

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/LDAP/btn_system_designer.png) button to open the System Designer.

2. Navigate to the "Users and administration" block and click "Organizational roles" or "Functional roles" depending on what user groups you would like to synchronize.

You can also create a new role for the AD user group in your Creatio organizational structure. To do this:
1. Select a parent role. For example, "All employees" to add regular users or "All portal users" to add portal users → **New** → **Organization**.
2. Specify the name for your new role. You can use the name of your Active Directory user group or specify a different name.
3. Select the element where Creatio will import the LDAP users in the role tree.

4. Select the **Synchronize with LDAP** checkbox in the **Users** tab. Select the Active Directory group that corresponds to this Creatio role in the **LDAP element** field.

5. Click **Save**.

6. Run the **Synchronize with LDAP** action in the section menu. Once the synchronization is complete, all users from the LDAP server group will be imported to the selected Creatio organizational or functional group.


note

Should LDAP synchronization result in an error, review the "Synchronize user data with LDAP" process in the **Process log** section to find out the reason.

As a result, Creatio will add contacts and user accounts that correspond to the selected LDAP users. Creatio will automatically add new user accounts to the selected organizational structure element. Creatio populates the contact page fields with values of LDAP element attributes specified during the synchronization setup.

Important

The LDAP user list displays all users regardless of whether they are included in the LDAP element connected to the organizational structure element.

Creatio will only synchronize the users included in the LDAP element that is connected to the organizational structure.

note

Creatio will license the user account connected to the LDAP user automatically if you select the corresponding checkbox. Read more: [Set up the connection to server](https://academy.creatio.com/documents?id=2142&anchor=title-2021-3).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory\#see-also "Direct link to See also")

[Set up LDAP synchronization](https://academy.creatio.com/documents?id=513)

[Set up Active Directory filters](https://academy.creatio.com/documents?id=1868)

[Set up LDAP authentication](https://academy.creatio.com/documents?id=2367)

- [Prepare the directory for integration](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory#title-2019-18)
- [Import new users from LDAP](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory#title-2019-19)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/import-new-users-and-roles-from-active-directory#see-also)