<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/single-sign-on)** (8.3).

Version: 8.2

On this page

The Single Sign-On technology in Creatio enables users to log in to multiple services using a single account. After a user signs in once via an identity provider, they can access their applications and services without the need to enter their login credentials. When a user signs out of any of the applications, any sessions in other, connected applications end as well.

**Prerequisites**:

1. A Creatio website available over HTTPS.
2. Administrator privileges on the website.
3. Administrator privileges in the identity provider.
4. Users in the corporate domain.

You can expedite the setup by using one of the following pre-configured providers:

- AD FS
- Azure AD
- Okta
- Cognito
- Google

You can also integrate Creatio with any identity provider that supports the SAML 2.0 protocol.

For detailed instructions, check out the individual provider articles. In general, the **following steps** are required to set up Single Sign-On:

1. Download the file that contains integration metadata.
2. Set up the identity provider by adding Creatio to trusted websites.
3. Set up the trusted identity provider in Creatio.

## SSL Certificate [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#ssl-certificate "Direct link to SSL Certificate")

An SSL Certificate is used for signing and encrypting SAML requests sent to the SSO provider. SAML requests, outlined below in the next section, are mandatory.

You can upload a public Secure Sockets Layer (SSL) Certificate to sign and encrypt SAML requests by clicking the Upload Certificate button (Fig. 1).

Fig. 1 Certificate Upload

![Fig. 1 Certificate Upload](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/single_sign_on/8_1/scr_sso_upload_certificate.png)

## SAML Request Validation [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#saml-request-validation "Direct link to SAML Request Validation")

SAML requests signing is a minimum required option for secure SSO configuration. An SSO configuration without SAML requests signing is considered vulnerable, and will be automatically disabled.

To validate the signing of any SAML requests, select the **Signature Validation** checkbox (Fig. 2).

Fig. 2 Encryption And Signing

![Fig. 2 Encryption And Signing](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/single_sign_on/single_sign_on_encryption_and_signing.png)

Important

We strongly recommend not using SSO login without SAML signing or SAML encryption. This configuration is insecure and should be used exclusively in development environments.

## Display login via SSO [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#display-login-via-sso "Direct link to Display login via SSO")

You can specify where the user will see the **Login via SSO** link depending on their user type, with the main login page, the login page for external users, or both as the available options. This option allows you to enable SSO login exclusively for a specific group of users. To specify its location, perform its set up in the **User Type** field of the **Additional Parameters** section of an individual SSO provider's page (Fig.  3).

Fig. 3 Specifying Login Location

![Fig. 3 Specifying Login Location](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/single_sign_on/single_sign_on_login_specifying.png)

## Import SSO Configuration [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#import-sso-configuration "Direct link to Import SSO Configuration")

You can also import the configuration of your SSO provider from an existing SSO metadata file. Importing the configuration this way greatly simplifies the SSO setup. This functionality allows you to quickly and efficiently create either a new SSO provider, or to update an existing provider. To do this, you need a metadata file, which is a specifically formatted XML file that contains all the required information for setting SSO up on Creatio's side, and the SSL Certificate to be installed. An overwhelming majority of SSO providers supports this functionality. After you upload the metadata file (Fig. 4), Creatio automatically adds all the settings, including the SSO certificate for signing and encryption of your SAML requests.

Fig. 4 Uploading Metadata

![Fig. 4 Uploading Metadata](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/single_sign_on/single_sign_on_upload_metadata.png)

## turn SLO for SSO off [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#turn-slo-for-sso-off "Direct link to turn SLO for SSO off")

You can turn Single Logout (SLO) off in your SSO configuration. This is an entirely optional option, and not mandatory. If SLO is turned off, the user is only logged out from Creatio upon logging out from Creatio. If SLO is turned on on the other hand, the user is logged out from all services that use the corresponding SSO service (Fig. 5).

Fig. 5 Single Log Out

![Fig. 5 Single Log Out](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/single_sign_on/single_sign_on_single_sign_out.png)

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on\#see-also "Direct link to See also")

[Single Sign-On via OneLogin](https://academy.creatio.com/documents?id=1650)

[Just-In-Time User Provisioning](https://academy.creatio.com/documents?id=1759)

- [SSL Certificate](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#ssl-certificate)
- [SAML Request Validation](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#saml-request-validation)
- [Display login via SSO](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#display-login-via-sso)
- [Import SSO Configuration](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#import-sso-configuration)
- [turn SLO for SSO off](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#turn-slo-for-sso-off)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/single-sign-on#see-also)