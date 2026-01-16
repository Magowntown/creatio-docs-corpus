<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-sso-via-okta)** (8.3).

Version: 8.2

On this page

You can integrate Creatio with Okta to manage single sign-on for all Creatio users that work in the corporate network.

Important

This example uses the `https://site01.creatio.com/Demo_161215/` Creatio URL. Replace this URL with the corresponding URL of your website when you perform the actual setup.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Download the file that contains integration metadata. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-1)
2. Perform the setup in Okta. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-2)
3. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-3)

## Download the metadata [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta\#title-2451-1 "Direct link to Download the metadata")

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Okta". This opens the setup page.
5. Click **Get metadata**.
6. Save the file to your local machine.

## Perform the setup in Okta [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta\#title-2451-2 "Direct link to Perform the setup in Okta")

1. **Add a new SAML 2.0 app**.
Fig. 1 New SAML 2.0 app

![Fig. 1 New SAML 2.0 app](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_Okta_add_saml20.png)

2. **Fill out the general parameters**: app name, logo, and description. These parameters will be displayed to all users. Click **Next**.
Fig. 2 The general parameters

![Fig. 2 The general parameters](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_okta_general_settings.png)

3. **Fill out the SSO parameters**.


1. Enter the URL of your Creatio website SSO in the **Single sign on URL** parameter. Use the following pattern: `https://yoursite.com/ServiceModel/AuthService.svc/SsoLogin`.
2. Enter the URL of your Creatio website in the **Audience URI (SP Entity ID)** parameter. For example, `https://site01.creatio.com/Demo_161215/`.
3. Select "Unspecified" in the **Name ID Format** parameter. This specifies the data type required to log in to your website.
4. Select "Email" in the **Application username** parameter. This specifies the parameter required for Just-In-Time Provisioning to work correctly.

Fig. 3 The SSO parameters

![Fig. 3 The SSO parameters](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_Okta_sso_settings.png)

4. **Fill out the advanced settings**.


1. Specify whether to sign queries for safe data transfer in the **Response** parameter. Select "Signed" for the production environment or "Unsigned" for the testing environment.
2. Specify the security configuration type in the **Assertion Signature** parameter. Select "Signed" for the production environment or "Unsigned" for the testing environment.
3. Set **Enable Single Logout** to turn on single sign-out for your Creatio website.

Fig. 4 The advanced settings

![Fig. 4 The advanced settings](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_Okta_advanced_settings.png)

5. **Map the following fields** for JIT Provisioning (optional):
1. Map **Name** to "name".

2. Map **Name format** to "Basic".

3. Map **Value** to "user.email".
      Fig. 5 Mapping fields

      ![Fig. 5 Mapping fields](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_Okta_attribute_statement.png)
6. **Download the Okta Certificate** if you are going to use Signed Response, Assertion Signature, and Single Logout.
Fig. 6 The Okta certificate download

![Fig. 6 The Okta certificate download](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/okta_sso/scr_Okta_certificate.png)


## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta\#title-2451-3 "Direct link to Perform the setup in Creatio")

Follow these steps to set up single sign-on in Creatio:

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Azure AD". This opens the setup page.
5. Fill out the following parameters:

| Parameter | Parameter Value |
| --- | --- |
| IdP Issuer | The unique ID of the client. Retrieved while setting Okta up. |
| SingleSignOnServiceUrl | The URL of the identity provider’s single sign-on. For Okta, this is usually `https://okta.com/qmBNBnkAkopZXwJpjpu5/sso/saml`. |
| SingleLogoutServiceUrl | The URL of the identity provider’s single sign-off. For Okta, this is usually `https://test-site.okta.com/app/test-site_creatio_1/qmBNBnkAkopZXwJpjpu5/sso/saml`. |

6. **Fill out the provider's name** to display on the Creatio login page in the **Display name** field.

7. **Save the changes**.

8. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 7).
Fig. 7 Set up Just-In-Time Provisioning

![Fig. 7 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)

9. **Define your provider**. To do this, specify the provider in the "Default SSO provider" system setting ("DefaultSsoProvider" code) and save the changes.

10. **Test** whether the provider is working correctly (optional). To do this, open the provider page and click **Test Sign In**.


Fig. 8 Test the provider

![Fig. 8 Test the provider](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/scr_test_sso_provider.png)

## Set up SSO authentication for Mobile Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta\#title-2451-4 "Direct link to Set up SSO authentication for Mobile Creatio")

Mobile Creatio lets you log in using the Single Sign-On technology. To set up SSO authentication for Mobile Creatio, **turn on the "Use SSO in the mobile app" ("MobileUseSSO" code) system setting**.

If the **SSO authentication for Mobile Creatio is turned on**, the app displays an identity provider page that includes the login and password fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta\#see-also "Direct link to See also")

[Single Sign-On via a custom provider](https://academy.creatio.com/documents?id=1650)

[Single Sign-On via AD FS](https://academy.creatio.com/documents?id=1649)

- [Download the metadata](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-1)
- [Perform the setup in Okta](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-2)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-3)
- [Set up SSO authentication for Mobile Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#title-2451-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-okta#see-also)