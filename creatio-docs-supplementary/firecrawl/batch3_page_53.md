<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service)** (8.3).

Version: 8.2On-site

On this page

Identity Service implements OAuth 2.0 in Creatio. Before you connect the Identity Service to Creatio **on-site**, deploy the Identity Service. Instructions: [Deploy the Identity Service](https://academy.creatio.com/documents?id=2396).

If you use Creatio **in the cloud**, the Identity Service is connected out of the box. Proceed to getting OAuth 2.0 credentials. Instructions: [Generate OAuth 2.0 client credentials](https://academy.creatio.com/documents?id=2508&anchor=title-2508-1).

To connect the Identity Service to Creatio **on-site**:

1. **Enable the OAuth 2.0 integration** in Creatio. To do this, change the status of the "OAuth20Integration" additional feature. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3) (developer documentation).

As a result, the **OAuth 2.0 integrated applications** will be displayed in the **Import and integration** block of the System Designer (Fig. 1).
Fig. 1 OAuth 2.0 integrated applications section

![Fig. 1 OAuth 2.0 integrated applications section](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.2/src_oauth_2_0_integrated_application.png)

2. **Open the System settings section**. To do this, click ![](https://academy.creatio.com/docs/sites/academy_en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **System settings**.

3. **Fill out the system settings**.



| System setting | System setting description | Example of system setting value |
| --- | --- | --- |
| Authorization server Url for OAuth 2.0 integrations (OAuth20IdentityServerUrl code) | Website URL you specified in the **Sites** area of the IIS | \[Identity Service URL\] |
| Client id for OAuth 2.0 integrations (OAuth20IdentityServerClientId code) | Client Id you specified in the `ClientId` parameter of the appsettings.json file | IdServiceUser |
| Client secret for OAuth 2.0 integrations (OAuth20IdentityServerClientSecret code) | Secrets you specified in the `Secrets` parameter of the appsettings.json file | ItIsMyPasswordForIdentityService |


**As a result**, the Identity Service will be connected to Creatio.

You can **set up automated monitoring systems** based on OAuth health monitoring. Instructions: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513). If needed, use **Postman** to check the health of OAuth functionality. The Postman request collection that tests requests is available in [Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#0e2dd1ce-1a5d-4870-bb0b-c0cc2eb25a31).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service\#see-also "Direct link to See also")

[Manage the OAuth 2.0 client credentials](https://academy.creatio.com/documents?id=2508)

[Deploy the Identity Service](https://academy.creatio.com/documents?id=2466)

[OAuth health monitoring](https://academy.creatio.com/documents?id=2513)

[Update the Identity Service using IIS](https://academy.creatio.com/documents?id=2468)

[Authorize external requests using OAuth 2.0 (developer documentation)](https://academy.creatio.com/documents?id=15058)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service\#e-learning-courses "Direct link to E-learning courses")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#e-learning-courses)