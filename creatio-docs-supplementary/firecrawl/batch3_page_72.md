<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/secure-access-to-the-portal#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/secure-access-to-the-portal)** (8.3).

Version: 8.2All Creatio products

On this page

To ensure data security, deploy Creatio on-site as a web farm when installing the portal. Learn more about setting up a web farm in a separate article: [Application server web farm](https://academy.creatio.com/documents?id=2110).

Set up the portal access as follows (Fig. 1):

Fig. 1 Typical Creatio installation chart with portal that can be accessed from the external network

![Fig. 1 Typical Creatio installation chart with portal that can be accessed from the external network](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/portal_secure_access/portal_dmz.png)

- **Demilitarized zone (DMZ)**
  - A reverse proxy server must be the only publicly accessible component in your DMZ.
  - The reverse proxy logs the primary network activity. You can also configure the proxy to restrict access to the configuration web services of your application.
  - Authorized portal users only have access to those configuration web services that they are expressly allowed to access on the application level.
  - Configure access permissions for new web services during the development process. Learn more in the developer documentation: [Self-service portal](https://academy.creatio.com/documents?id=15732).
- **Internal network (Intranet)**
  - Deploy a separate set of application nodes on the web farm for servicing portal users. This set must not overlap with application nodes for servicing internal users.

  - To ensure the operation of the portal application and user application, create separate accounts that have different access permissions in the database.

  - Prohibit the login of system users in the portal application settings (disable "AuthProviders" except for portal users). To do this, make sure that the providerNames list in the web.config file of the application loader includes only SSPUserPassword:





    ```xml
    <terrasoft>
        <auth providerNames="SSPUserPassword" ...>
        ...
    </terrasoft>
    ```





    This is required to ensure that only portal users can create sessions from an external network (Extranet).

  - Additionally, you can configure external authentication providers to add a second authorization step.

  - To enhance security, set up unique password for the system user required for portal operation. To do this, set the unique password in the UserMangementSauPassword key and set the same password for the user in Creatio.





    ```xml
    <add key="UserManagementSauPassword" value="SamplePassword" />
    ```

  - Deploy portal application nodes, DBMS, and user applications in separate segments with restricted access.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/secure-access-to-the-portal\#see-also "Direct link to See also")

[Server-side system requirements](https://academy.creatio.com/documents?product=base&ver=7&id=1456)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/secure-access-to-the-portal#see-also)