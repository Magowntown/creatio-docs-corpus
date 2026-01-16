<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3On-site

On this page

Identity Service implements OAuth 2.0 in Creatio. Before you connect the Identity Service to Creatio **on-site**, deploy the Identity Service. Instructions: [Deploy the Identity Service](https://academy.creatio.com/documents?id=2396).

note

This functionality is available for Creatio deployed on .NET Framework only.

If you use Creatio **in the cloud**, the Identity Service is connected out of the box. Proceed with generating OAuth 2.0 client credentials. Instructions: [Set up client credentials grant](https://academy.creatio.com/documents?id=2508&anchor=title-2508-1), [Set up authorization code grant](https://academy.creatio.com/documents?id=2576&anchor=title-2576-3).

To connect the Identity Service to Creatio **on-site**:

1. **Enable the OAuth 2.0 integration** in Creatio. To do this, change the status of the `OAuth20Integration` additional feature. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3) (developer documentation).

As a result, the **OAuth 2.0 integrated applications** will be displayed in the **Import and integration** block of the System Designer (Fig. 1).
Fig. 1 OAuth 2.0 integrated applications section

![Fig. 1 OAuth 2.0 integrated applications section](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.3/src_oauth_2_0_integrated_applications.png)

2. **Open the OAuth integrated applications page** (Fig. 2). To do this, click **OAuth 2.0 integrated applications** in the **Import and integration** block.
Fig. 2 OAuth integrated applications page

![Fig. 2 OAuth integrated applications page](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.3/scr_OAuth_integrated_applications_page_with_Diagnostic_tab.png)


The **Diagnostic** tab displays the status of Identity Service connection and OAuth setup.

3. **Fill out the parameters** to connect the Identity Service to Creatio. To do this, click the **Open settings** button on the **Diagnostic** tab. This opens the **Connection settings** mini page (Fig. 3).
Fig. 3 Connection settings mini page

![Fig. 3 Connection settings mini page](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.3/scr_Connection_settings_mini_page.png)




| Parameter | Parameter description |
| --- | --- |
| Identity Service URL | Website URL you specified in the **Sites** area of the IIS. Creatio saves the specified value to the "Authorization server Url for OAuth 2.0 integrations" (`OAuth20IdentityServerUrl` code) system setting. |
| Client ID | Client Id you specified in the `ClientId` parameter of the appsettings.json file. Creatio saves the specified value to the "Client id for OAuth 2.0 integrations" (`OAuth20IdentityServerClientId` code) system setting. |
| Client secret | Secrets you specified in the `Secrets` parameter of the appsettings.json file. Creatio saves the specified value to the "Client secret for OAuth 2.0 integrations" (`OAuth20IdentityServerClientSecret` code) system setting. |

4. **Test connection** to the Identity Service. To do this, click **Test connection**.
   - If Creatio displays the "Connection established" notification, click **Save**.
   - If Creatio displays the "Connection failed" notification, identify potential issues or errors in the Identity Service or OAuth setup and usage. Instructions: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513).

**As a result**:

- All checkboxes on the **Diagnostic** tab will be selected (Fig. 4).
- The Identity Service will be connected to Creatio.

Fig. 4 Diagnostic tab

![Fig. 4 Diagnostic tab](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.3/scr_Diagnostic_tab.png)

If you change the deployment parameters of the Identity Service, click the **Refresh** button on the **Diagnostic** tab to display up-to-date status of Identity Service connection and OAuth setup.

You can **set up automated monitoring systems** based on OAuth health monitoring. Instructions: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513). If needed, use **Postman** to check the health of OAuth functionality. The Postman request collection that tests requests is available in [Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#0e2dd1ce-1a5d-4870-bb0b-c0cc2eb25a31).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service\#see-also "Direct link to See also")

[Deploy the Identity Service](https://academy.creatio.com/documents?id=2466)

[OAuth health monitoring](https://academy.creatio.com/documents?id=2513)

[Set up client credentials grant](https://academy.creatio.com/documents?id=2508)

[Set up authorization code grant](https://academy.creatio.com/documents?id=2576)

[Update the Identity Service using IIS](https://academy.creatio.com/documents?id=2468)

[Authorize external requests using client credentials grant (developer documentation)](https://academy.creatio.com/documents?id=15058)

[Authorize external requests using authorization code grant (developer documentation)](https://academy.creatio.com/documents?id=15188)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service\#e-learning-courses "Direct link to E-learning courses")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/connect-the-identity-service#e-learning-courses)