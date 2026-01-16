<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad)** (8.3).

Version: 8.2

On this page

You can integrate Creatio with Microsoft Entra Active Directory (Microsoft Entra AD) to manage single sign-on for all Creatio users that work in the corporate network.

Important

This example uses the `https://site01.creatio.com/Demo_161215/` Creatio URL. Replace these URLs with the corresponding URLs of your sites when you perform the actual setup.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Download the file that contains integration metadata. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-1)
2. Perform the setup in Microsoft Entra AD. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-2)
3. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-3)

## Download the metadata [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad\#title-2449-1 "Direct link to Download the metadata")

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Microsoft Entra AD (formerly Azure AD)". This opens the setup page.
5. Click **Get metadata**.
6. Save the file to your local machine, then upload it to the Microsoft Entra portal to speed up the configuration.

## Perform the setup in Microsoft Entra AD [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad\#title-2449-2 "Direct link to Perform the setup in Microsoft Entra AD")

To configure the settings below, register Creatio in the administrator account of the enterprise identity service of Microsoft Entra AD. Learn more: [Official vendor documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).

1. Add a new SSO application (Trusted Relaying Party) to Microsoft Entra AD:
1. Open the **Enterprise applications** section → **All Applications**.
2. Click **New application**.
3. Select "Creatio" in the **Add from the gallery** section and add the application. Learn more: \[Official vendor documentation\]\]( [https://docs.microsoft.com/en-us/azure/active-directory/saas-apps/bpmonline-tutorial#add-creatio-from-the-gallery](https://docs.microsoft.com/en-us/azure/active-directory/saas-apps/bpmonline-tutorial#add-creatio-from-the-gallery)).
2. Open the **Single sign-on** section and specify the following parameters:


| Parameter | Parameter Value |
| --- | --- |
| Single Sign-on Mode | Select SAML in this field. |
| Identifier | The full name of the website, for example: `https://site01.creatio.com/Demo_161215/`. |
| Reply URL | The full website name and `/ServiceModel/AuthService.svc/SsoLogin` address, for example: `https://site01.creatio.com/Demo_161215/ServiceModel/AuthService.svc/SsoLogin` |

3. Save the following data to perform the setup in Creatio (Fig. 1):
   - Microsoft Entra AD Identifier
   - Login URL
   - Logout URL

Fig. 1 Data required to perform the setup in Creatio

![Fig. 1 Data required to perform the setup in Creatio](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/azure_ad/8_1/scr_creatio_entra_settings.png)

note

By default, Microsoft Entra AD passes the following fields to Creatio: **Given name**, **Surname**, **Email address**, **Name**. The email address serves as the username.

## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad\#title-2449-3 "Direct link to Perform the setup in Creatio")

Follow these steps to set up single sign-on in Creatio:

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Microsoft Entra ID (formerly Azure AD)". This opens the setup page.
5. Fill out the following parameters:

| Parameter | Parameter Value |
| --- | --- |
| Microsoft Entra identifier | The unique ID of the client. Retrieved while setting Okta up. |
| SingleSignOnServiceUrl | The URL of the identity provider’s single sign-on. For Microsoft Entra AD, this is usually `https://login.microsoftonline.com/\<azure account="" id="">/saml2`. Find out the settings of the added connector in your Microsoft account. |
| SingleLogoutServiceUrl | The URL of the identity provider’s single sign-off. For Microsoft Entra AD, this is usually `https://logout.microsoftonline.com/\<azure account="" id="">/saml2`. Find out the settings of the added connector in your Microsoft account. |

6. **Fill out the provider's name** to display on the Creatio login page in the **Display name** field.

7. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 2).
Fig. 2 Set up Just-In-Time Provisioning

![Fig. 2 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)

8. **Define your provider**. To do this, select the **Default provider** checkbox.

9. **Test** whether the provider is working correctly (optional). To do this, open the provider page and click **Test Sign In**.
Fig. 3 Test the provider

![Fig. 3 Test the provider](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/azure_ad/8_1/scr_test_sso_provider.png)


## Set up SSO authentication for Mobile Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad\#title-2449-4 "Direct link to Set up SSO authentication for Mobile Creatio")

Mobile Creatio lets you log in using the Single Sign-On technology. To set up SSO authentication for Mobile Creatio, **turn the "Use SSO in the mobile app" ("MobileUseSSO" code) system setting on**.

If **SSO authentication for Mobile Creatio is turned on**, the app displays an identity provider page that includes the login and password fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad\#see-also "Direct link to See also")

[Single Sign-On via OneLogin](https://academy.creatio.com/documents?id=1650)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

[Microsoft Entra Seamless Single Sign-On: Quickstart (Official vendor documentation)](https://docs.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-sso-quick-start)

[Microsoft Entra AD portal](https://www.microsoft.com/en/security/business/identity-access/microsoft-entra-id)

[Instructions on publishing your application in the gallery (Microsoft documentation)](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/v2-howto-app-gallery-listing)

- [Download the metadata](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-1)
- [Perform the setup in Microsoft Entra AD](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-2)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-3)
- [Set up SSO authentication for Mobile Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#title-2449-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-sso-via-azure-ad#see-also)