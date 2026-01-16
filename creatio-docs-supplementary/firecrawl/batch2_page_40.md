<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/single-sign-on-via-cognito)** (8.3).

Version: 8.2

On this page

Creatio can be integrated with any identity provider that supports the Open ID protocol. You can use Cognito AWS portal as a single sign-on point for all your services, including Creatio. To do this, perform he setup both in Cognito AWS and Creatio.

The following **steps** are the general procedure required to set up Single Sign-On in Creatio:

1. Sign up for [Cognito AWS](https://aws.amazon.com/cognito/).
2. Perform the setup in Cognito AWS. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#title-2660-1)
3. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#title-2660-2)

## Perform the setup in Cognito AWS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito\#title-2660-1 "Direct link to Perform the setup in Cognito AWS")

1. Sign in to Aws.Amazon as root user.

2. Click **App client list** → **Create app client**.

3. Enter "Creatio" in the **App client list** field.

4. Click **Client secret** → **Generate a client secret**.

5. Enter `[CreatioURL]/ServiceModel/AuthService.svc/OpenIdCallback` in **Allowed callback URLs** where \[CreatioURL\] is the URL of your Creatio instance.

6. Enter `[CreatioURL]/ServiceModel/AuthService.svc/OpenIdLogoutCallback` in **Allowed sign-out URLs** where \[CreatioURL\] is the URL of your Creatio instance.

7. Select **Email**, **OpenId**, **Phone**, **Profile** in the **OpenID Connect scopes** block.
Fig. 1 OpenID Connect scopes block

![Fig. 1 OpenID Connect scopes block](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/Cognito_integration/scr_chapter_single_sign_on_Cognito_step3_set_site.png)

8. Click **Create app client**.

9. **Save the following data** from Cognito AWS console to your machine:


| Parameter | Parameter Value |
| --- | --- |
| Client ID | The ID of the client. Consists of 26 letters and digits. To find this value, open the **App integration** section → **App client list**. |
| Client Secret | The secret of the client. Consists of 52 letters and digits. To find this value, open the **App integration** section → **App clients and analytics** block → click the name of your application. |
| User pool ID | The pool ID of the User. View the value in the settings of a specific user pool. |
| Region | The region of the user. Matches the "Region" parameter in the "User pool ID" value. For example, `User pool ID = cognito-idp.us-east-1.amazonaws.com/us-east-1_123456789`, where us-east-1 is the required region. Learn more in [Cognito documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-integrating-user-pools-with-identity-pools.html). |

## Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito\#title-2660-2 "Direct link to Perform the setup in Creatio")

note

If you use Creatio **in the cloud**, the Open ID authorization is enabled out of the box.

To evaluate Open ID authorization in Creatio **on-site**, enable the "EnableOpenIDAuth" additional feature. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3) (developer documentation).

Follow these steps to configure single sign-on in Creatio:

1. Click the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_system_designer_8_shell.png) button to open the **System Designer**.
2. Click **Single Sign On configuration**.
3. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/adfs_integration/8_0/btn_add_record.png). This opens a drop-down menu.
4. Select "Cognito AWS." This opens the setup page.
5. Fill out the following parameters:

| Parameter | Parameter Value |
| --- | --- |
| Client ID | The ID of the client. Consists of 26 letters and digits. To find this value, retrieve it from Cognito AWS in the **Client ID** parameter. |
| Client Secret | The secret of the client. Consists of 52 letters and digits. To find this value, retrieve it from CognitoAWS in the **Client secret** parameter. |
| URL | The URL of your provider’s website. The URL template is as follows `https://[userPoolId].auth.[Region].amazoncognito.com`. \[Region\] and \[UserPoolId\] are "Region" and "User pool ID" values retrieved from Cognito AWS console, respectively. |
| Discovery URL | The URL of the identity provider’s single sign-on. The URL template looks like `https://cognito-idp.[region].amazonaws.com/[userPoolId]/.well-known/openid-configuration`. \[Region\] and \[UserPoolId\] are "Region" and "User pool ID" values retrieved from Cognito AWS console, respectively. |
| End session endpoint | The URL of the identity provider’s single sign-off. The URL template is as follows `https://[userPoolId].auth.[region].amazoncognito.com/logout?client_id={client_id}&logout_uri={redirect_uri}&state={state}`. \[Region\] and \[UserPoolId\] are "Region" and "User pool ID" values retrieved from Cognito AWS console, respectively. |

6. **Fill out the provider name** to display on the Creatio login page in the **Display name** field.

7. **Save the changes**.

8. **Turn on Just-In-Time Provisioning** (optional). This mechanism automatically creates the corresponding Creatio user account with data from the identity provider, such as user group, employee name, contact information, etc. For company employees, select the **Create and update company employees data when log in (Just-In-Time Provisioning)** checkbox and map the fields. For external users, select the **Create and update external users data when log in (Just-In-Time Provisioning)** checkbox and map the fields (Fig. 2).
Fig. 2 Set up Just-In-Time Provisioning

![Fig. 2 Set up Just-In-Time Provisioning](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/adfs_integration/8_0/scr_set_up_JIT_updated.png)


## Set up SSO authentication for Mobile Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito\#title-2660-3 "Direct link to Set up SSO authentication for Mobile Creatio")

Mobile Creatio lets you log in using the Single Sign-On technology. To set up SSO authentication for Mobile Creatio, **turn on the "Use SSO in the mobile app" ("MobileUseSSO" code) system setting**.

If the **SSO authentication for Mobile Creatio is turned on**, the app displays an identity provider page that includes the login and password fields.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito\#see-also "Direct link to See also")

[Single Sign-On via ADFS](https://academy.creatio.com/documents?id=1649)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

- [Perform the setup in Cognito AWS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#title-2660-1)
- [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#title-2660-2)
- [Set up SSO authentication for Mobile Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#title-2660-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on-via-cognito#see-also)