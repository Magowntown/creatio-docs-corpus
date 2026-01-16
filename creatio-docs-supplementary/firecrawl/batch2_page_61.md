<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/single-sign-on-via-adfs)** (8.3).

Version: 8.1

On this page

You can integrate your Active Directory Federation Services (AD FS) instance to manage single sign-on for your members. To do this, perform the setup both in AD FS and Creatio.

Important

This example uses the `https://site01.creatio.com/Demo_161215/` Creatio website and `http://ADFS01.mysite.com/ADFS/` AD FS website. Replace these URLs with the corresponding URLs of your websites when you perform the actual setup.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Download the file that contains integration metadata. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-1)
2. Perform the setup in AD FS. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-2)
3. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-3)

## Download the metadata [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs\#title-2415-1 "Direct link to Download the metadata")

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "AD FS". This opens the setup page.
5. Click **Get metadata**.
6. Save the file to your local machine.

## Perform the setup in AD FS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs\#title-2415-2 "Direct link to Perform the setup in AD FS")

01. Add a new Relying Party Trust to ADFS (Fig. 1).
    Fig. 1 Relying Party Trust menu

    ![Fig. 1 Relying Party Trust menu](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step1_add_party.png)

02. Select "Import data about the relying party from file," (Fig. 2).
    Fig. 2 Import data about the relying party from file option

    ![Fig. 2 Import data about the relying party from file option](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/scr_chapter_single_sign_on_adfs_step2_import_data.png)

03. Specify the full website address in the "relying party trust identifier" field and click **Add** (Fig. 3).
    Fig. 3 Identifier

    ![Fig. 3 Identifier](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step7_set_identifier.png)




    Important





    The identifier is required to verify the authenticity of a source that requests authentication. The URL must match verbatim, including the "/" at the end.

04. Set up the rest of the parameters according to your security requirements. You can leave default values for test purposes.

05. Click **Finish**. This opens a window.

06. Click **Add Rule** and add a new SAML Assertion to SAML Response rule (Fig. 4).
    Fig. 4 Add rule button

    ![Fig. 4 Add rule button](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step9_add_rule.png)




    note





    Creatio will use the data generated based on the new rule to search for users, as well as to update their profiles and roles.

07. Keep the default settings and click **Next** on the first step of the Rule Wizard. Set up a set of parameters to receive from the user’s data (Fig. 5). In this example, the user’s name and a list of domain groups will be passed via SAML Assertion.
    Fig. 5 Rule parameters

    ![Fig. 5 Rule parameters](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step10_rule_parameters.png)

08. Click **Save**.

09. Open the Trusted Relay settings, go to the **Advanced** tab, and specify SHA-1 encryption according to the website certificate algorithm.

10. Add the public certificate key on the **Encryption** tab to set up the SAML encryption (Fig. 6). This step is required only for on-site Creatio.



    note





    If you are using Creatio in the cloud, get the public certificate key from the Creatio support service.




    Fig. 6 Encryption tab

    ![Fig. 6 Encryption tab](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step13_add_public_key.png)

11. Add the logout endpoint and set the following parameters (Fig. 7) on the **Endpoints** tab:


    - Set **Endpoint type** to "SAML Logout".
    - Set **Binding** to "Redirect".
    - Enter `https://site01.creatio.com/Demo_161215/ServiceModel/AuthService.svc/SsoLogout` in the **Trusted URL** parameter.

Fig. 7 Endpoint parameters

![Fig. 7 Endpoint parameters](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step13_add_endpoint.png)

12. Add the Logout Request certificate to the **Signature** tab (Fig. 8).
    Fig. 8 Logout Request certificate

    ![Fig. 8 Logout Request certificate](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/scr_chapter_single_sign_on_adfs_step14_add_certificate.png)


Important

Single Sign-Out needs a certificate to .

## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs\#title-2415-3 "Direct link to Perform the setup in Creatio")

Follow these steps to set up single sign-on in Creatio:

01. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.

02. Click **Single Sign On configuration**.

03. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.

04. Select "AD FS". This opens the setup page.

05. Fill out the **AD FS tenant URL** parameter. Creatio will populate other parameters automatically.

06. Fill out the provider's name to display on the Creatio login page in the **Display name** field (Fig. 9).
    Fig. 9 AD FS settings

    ![Fig. 9 AD FS settings](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/scr_ad_fs_settings_example_807_updated.png)

07. **Save the changes**.

08. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 10).
    Fig. 10 Set up Just-In-Time Provisioning

    ![Fig. 10 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)

09. **Define your provider**. To do this, specify the provider in the "Default SSO provider" system setting ("DefaultSsoProvider" code) and save the changes.

10. **Test** whether the provider is working correctly (optional).
    1. Open the provider page and click **Test Sign In**.

    2. Click **Test** (Fig. 11).
       Fig. 11 Test the provider

       ![Fig. 11 Test the provider](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/scr_test_sso_provider.png)

## Set up SSO authentication for Mobile Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs\#title-2415-4 "Direct link to Set up SSO authentication for Mobile Creatio")

Mobile Creatio lets you log in using the Single Sign-On technology. To set up SSO authentication for Mobile Creatio, **turn on the "Use SSO in the mobile app" ("MobileUseSSO" code) system setting**.

If the **SSO authentication for Mobile Creatio is turned on**, the app displays an identity provider page that includes the login and password fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs\#see-also "Direct link to See also")

[Single Sign-On via OneLogin](ihttps://academy.creatio.com/documents?id=1650)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

- [Download the metadata](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-1)
- [Perform the setup in AD FS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-2)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-3)
- [Set up SSO authentication for Mobile Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#title-2415-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/single-sign-on-via-adfs#see-also)