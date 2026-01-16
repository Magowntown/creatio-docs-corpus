<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider)** (8.3).

Version: 8.1

On this page

Creatio can be integrated with any identity provider that supports the SAML 2.0 protocol. You can use OneLogin SSO portal as a single sign-on point for all your services, including Creatio. To do this, perform the setup in both OneLogin and Creatio.

Important

This example uses the `https://site01.creatio.com/` Creatio URL and the "appid" application ID in OneLogin. Replace these values with your website URL and the ID of the corresponding application in OneLogin when you perform the actual setup.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Download the file that contains integration metadata. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-1)
2. Perform the setup in your provider. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-2)
3. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-3)

## Download the metadata [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider\#title-2452-1 "Direct link to Download the metadata")

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Custom SAML". This opens the setup page.
5. Click **Get metadata**.
6. Save the file to your local machine.

## Perform the setup in OneLogin [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider\#title-2452-2 "Direct link to Perform the setup in OneLogin")

1. **Log in** to OneLogin using an administrator account.

2. Click **Apps** and select **Add Apps**. Enter "Creatio" in the search bar and select the Creatio application.

3. If needed, **change the value** in the **Display name** field, modify the application icons, or clear the **Visible in portal** checkbox. These settings affect the way the website is displayed on the OneLogin website.

4. Click **Save**.

5. Go to the **Configuration** tab and enter your website domain name in the **Creatio site** field (Fig. 1). For example, "site01".
Fig. 1 Website configuration page

![Fig. 1 Website configuration page](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/onelogin_integration/scr_chapter_single_sign_on_onelogin_step3_set_site.png)


## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider\#title-2452-3 "Direct link to Perform the setup in Creatio")

Follow these steps to set up single sign-on in Creatio:

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Custom "SAML". This opens the setup page.
5. **Fill out the following parameters**:

|     |     |
| --- | --- |
| Entity ID | The website of your provider |
| Single Sign On URL | The URL of your identity provider's Single Sign On Service. You can retrieve the URL from the SAML 2.0 Endpoint (HTTP) on the trusted application page. |
| Single Logout URL | The URL of your identity provider's Single Sign Off service. You can retrieve the URL from the SLO Endpoint (HTTP) on the trusted application page. |

6. \\*\\* Fill out the provider's name\*\* to display on the Creatio login page in the **Display name** field.

7. **Save the changes**.

8. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 2).
Fig. 2 Set up Just-In-Time Provisioning

![Fig. 2 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)

9. **Define your provider**. To do this, specify the provider in the "Default SSO provider" system setting ("DefaultSsoProvider" code) and save the changes.

10. **Test** whether the provider is working correctly (optional). To do this, open the provider page and click **Test**.
Fig. 3 Test the provider

![Fig. 3 Test the provider](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/scr_test_sso_provider.png)


## Set up SSO authentication for Mobile Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider\#title-2452-4 "Direct link to Set up SSO authentication for Mobile Creatio")

Mobile Creatio lets you log in using the Single Sign-On technology. To set up SSO authentication for Mobile Creatio, **turn on the "Use SSO in the mobile app" ("MobileUseSSO" code) system setting**.

**If SSO authentication for Mobile Creatio is turned on**, the app displays an identity provider page that includes the login and password fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider\#see-also "Direct link to See also")

[Single Sign-On via ADFS](https://academy.creatio.com/documents?id=1649)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

- [Download the metadata](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-1)
- [Perform the setup in OneLogin](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-2)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-3)
- [Set up SSO authentication for Mobile Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#title-2452-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-custom-provider#see-also)