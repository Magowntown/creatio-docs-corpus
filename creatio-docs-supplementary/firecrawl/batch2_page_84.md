<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/technical-user#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/technical-user)** (8.3).

Version: 8.1

On this page

note

The feature below is available for beta testing in Creatio version 8.1.5 Quantum. If you have any feedback, contact us at: `beta@creatio.com`. All feedback is appreciated.

To access the technical user functionality, contact Creatio support.

Technical users are a special type of Creatio users designed for system integration purposes. They let you connect Creatio to external systems without consuming additional licenses and compromising your Creatio environment's security. However, technical users have certain limitations:

- **Access restrictions**. Technical users cannot log in to the Creatio web or mobile application using their credentials. They can only interact with Creatio via the API.
- **Authentication method**. Technical users can only authenticate in Creatio using OAuth authentication. Other authentication methods are not supported.
- **Privilege management**. Technical users have no access to Creatio objects or operations out of the box. You must grant them privileges explicitly to perform specific tasks. Technical users cannot inherit role permissions through the hierarchy. Users will receive privileges from direct roles only.
- **Subscription limit**. The number of technical users you can add is determined by your subscription plan.

Important

To enhance security, we strongly recommend creating a unique technical user for each OAuth integration you add. Assign only the minimum necessary permissions to each user, ensuring they have access only to data and actions required for that specific integration.

To **add a technical user**:

1. Click ![btn_system_designer.png](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/add_users/8_1/btn_system_designer_8_shell.png) → **Import and integration** → **Technical users**.
2. Click **New**. This opens the new technical user page.
3. Fill out the **Name** field. When creating a name for a technical user, consider its purpose. Use a clear and descriptive name that indicates the specific external system or functionality it will interact with. This will help with organization and troubleshooting.
4. Fill out **Language** and **Time zone** fields to manage language and time of data the technical user receives by interacting with Creatio API.
5. **Save changes**.

Newly created technical users in Creatio have no object and operation permissions. To utilize these users for OAuth integrations or other purposes, you must **assign the necessary permissions**. Learn more: [Object operation permissions](https://academy.creatio.com/documents?id=250), [System operation permissions](https://academy.creatio.com/documents?id=258). All permissions granted to the technical user are viewable in a read-only format on their page.

Fig. 1 Technical user's page

![Fig. 1 Technical user's page](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/technical_users/scr_technical_user_page.png)

To streamline permission assignment, consider grouping technical users who need to access the same data into specific functional roles. Learn more: [Assign a user role](https://academy.creatio.com/documents?id=2005). Technical users have the following **restrictions regarding role membership**:

- **Indirect membership**. They can only be included in child roles within the "All employees" role, not directly in the root role.
- **Initial rolelessness**. New technical users are not automatically assigned to any roles.
- **Limited inheritance**. They cannot inherit permissions from parent roles in the hierarchy. Permissions are granted directly from the roles to which they belong. For instance, a technical user in the "Integrations" role, which is a child of "All employees," will only have the permissions explicitly assigned to "Integrations," not those of "All employees."

You can **monitor the activity** of the technical user on their page. The **User sessions** tab displays a dashboard showing the current technical user's session activity over the past 10 days. You can also view a detailed list of all sessions for any specific date by using the list view at the bottom of the page.

To temporarily **disable** a technical user's access to Creatio data through integrations, clear the **Active** checkbox on their user page. This will prevent them from interacting with the system. Deactivation is helpful when you need to block a user's activity or want to preserve existing integration settings while troubleshooting or making changes.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/technical-user\#see-also "Direct link to See also")

[Object operation permissions](https://academy.creatio.com/documents?id=250)

[System operation permissions](https://academy.creatio.com/documents?id=258)

[Assign a user role](https://academy.creatio.com/documents?id=2005)

[Functional roles](https://academy.creatio.com/documents?id=1438)

[Add a regular employee user](https://academy.creatio.com/documents?id=1441)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/technical-user#see-also)