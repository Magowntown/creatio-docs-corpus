<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/single-sign-on-via-google)** (8.3).

Version: 8.2All Creatio products

On this page

You can integrate Creatio with Google to manage single sign-on for all Creatio users that work in the corporate network.

Important

This example uses the `https://site01.creatio.com/` Creatio URL and "appid" application id in OneLogin. Replace these values with your website URL and the id of the corresponding application in OneLogin when you perform the actual setup.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Perform the setup in Google. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#title-2452-2)
2. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#title-2452-3)

## Perform the setup in Google [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google\#title-2452-2 "Direct link to Perform the setup in Google")

01. **Open** the [https://admin.google.com/](https://admin.google.com/) page.

02. **Log in** as a Workspace administrator.

03. **Go to** **Menu** → **Apps** → **Web and mobile apps**.

04. **Click** **Add App** → **Add custom SAML app** (Fig. 1).
    Fig. 1 Add custom SAML app

    ![Fig. 1 Add custom SAML app](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/scr_add_app_0.png)

05. **Enter the app name** → **Continue**.

06. **Copy** the **SSO URL** and **Entity ID** for later (Fig. 2).
    Fig. 2 SSO parameters

    ![Fig. 2 SSO parameters](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/scr_sso_data.png)

07. **Download the certificate**.

08. **Click** **Continue**. This opens a window.

09. **Fill out** the following parameters (Fig. 3):
    Fig. 3 Provider details

    ![Fig. 3 Provider details](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/scr_provider_details.png)



    |     |     |
    | --- | --- |
    | **Parameter** | **Parameter value** |
    | ACS URL | Enter the full website path together with the /ServiceModel/AuthService.svc/SsoLogin address. For example, `https://site01.creatio.com/ServiceModel/AuthService.svc/SsoLogin` |
    | Entity ID | Enter the full website path. For example, `https://site01.creatio.com` |
    | Signed response | Indicates that your service provider requires the entire SAML authentication response to be signed. Select the checkbox for the production environment and clear it for the testing environment. |
    | Name ID format | Select "Email." |
    | Name ID | Select "Basic information - Primary Email". |

10. **Click** **Continue**.

11. **Click** **Add mapping** to map user attributes.

12. **Select** "Basic information - Primary Email" in the **Google Directory attributes** field and enter "name" in the **App attributes** field (Fig. 4).
    Fig. 4 Map attributes

    ![Fig. 4 Map attributes](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/scr_map_attributes.png)

13. **Click** **Finish**.


## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google\#title-2452-3 "Direct link to Perform the setup in Creatio")

Follow these steps to set up single sign-on in Creatio:

1. Click ![](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/btn_system_designer.png) to **open the System Designer**.

2. **Go to** the **Users and administration** group → **Single Sign On configuration**.

3. **Click** → "Custom SAML". This opens the setup page.

4. **Fill out** the following parameters:


|     |     |
| --- | --- |
| **Parameter** | **Parameter value** |
| Entity ID | Enter the Entity ID you acquired from Google. |
| Single Sign On URL | Enter the SSO URL you acquired from Google. |
| Single Logout URL | Enter the SSO URL you acquired from Google. |
| Display name | Enter the provider name to display on the Creatio login page. |

5. **Save the changes**.

6. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 5).

7. **Select** the **Create and update users data when log in (Just-In-Time Provisioning)** checkbox.

8. Map Google fields to Creatio.


Fig. 5 Set up Just-In-Time Provisioning

![Fig. 5 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)

7. **Define your provider**. To do this, specify the provider in the "Default SSO provider" ("DefaultSsoProvider" code) system setting. Learn more: [Manage system settings](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/system-settings-and-lookups/manage-system-settings).
8. **Test** whether the provider is working correctly (optional). To do this, open the provider page → **Test sign in** (Fig. 6).Fig. 6 Test sign in

![Fig. 6 Test sign in](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/set_up_sso_via_google/scr_test_sign_in.png)


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google\#see-also "Direct link to See also")

[Single Sign-On via ADFS](https://academy.creatio.com/documents?id=1649)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

- [Perform the setup in Google](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#title-2452-2)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#title-2452-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-google#see-also)