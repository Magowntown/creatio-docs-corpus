<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-two-factor-authentication)** (8.3).

Version: 8.1

On this page

Use two-factor authentication (2FA) to enhance account security by adding a second factor verification that confirms the user identity on various actions in Creatio, most importantly login. 2FA is available for both external users and company employees. Audit log records all actions related to 2FA. Learn more: [View and archive the audit log](https://academy.creatio.com/documents?id=2320).

Creatio supports the following 2FA options:

- **Integration with external identity providers via SAML 2.0 protocol**. If you store users and their passwords outside of Creatio, you can integrate external identity providers via SAML 2.0 protocol to get a wide range of 2FA capabilities. For example, integrations with Azure AD, Okta, OneLogin.
- **2FA functionality in Creatio**. If you store users and passwords in Creatio and use a basic authentication mechanism via login and password, you can use 2FA functionality available natively in Creatio. Integrations work only via OAuth. Forms authorization method is not available.

The native 2FA functionality provides the following options:

- Authenticate via email, SMS, or mobile app (TOTP).
- Use multiple 2FA options as part of the authentication process.
- Use 2FA to confirm changing the password on the user profile page.
- Use 2FA to confirm administrator actions, such as disabling 2FA for administrators or changing administrator login, password, phone, or email.
- Recover the password using 2FA.
- Disconnect the authenticator app, for example, when changing or losing a device.

## Set up 2FA [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-1 "Direct link to Set up 2FA")

### Set up 2FA via email [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-2 "Direct link to Set up 2FA via email")

This authentication method sends the verification code to the email specified in the **Email** field of the system user or to the login email if you use it. Before you set up this method, make sure all users have email specified and you have a mailbox from which to send the emails configured. Learn more: [Set up a personal mailbox](https://academy.creatio.com/documents?id=1841).

#### 1\. Activate the email 2FA method [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-5 "Direct link to 1. Activate the email 2FA method")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **Lookups**.
3. **Open** the **2FA methods** lookup.
4. Click the **Email** row → **select the checkbox** in the **Enabled** column.
5. **Select the checkbox** in the **Primary** column if you want email to be the main 2FA method.
6. **Click**![btn_select.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_select.png).

#### 2\. Specify the mailbox from which to send verification emails [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-6 "Direct link to 2. Specify the mailbox from which to send verification emails")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "Mailbox for sending emails that contain 2FA verification code" ("2FAmailbox" code) system setting.
4. **Select the needed mailbox** in the **Default value** field.
5. **Save the changes**.

#### 3\. Activate 2FA [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-7 "Direct link to 3. Activate 2FA")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "Enable 2FA" ("Enable2FA" code) system setting.
4. **Select** the **Default value** checkbox.
5. **Save the changes**.

At this point, the users can already use 2FA. Proceed further to customize additional aspects of the functionality.

#### 4\. Specify the user groups to activate 2FA (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-8 "Direct link to 4. Specify the user groups to activate 2FA (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **Users and administration** block → **Operation permissions**.
3. **Open** the "Can use 2FA" ("CanUse2FA" code) system operation.
4. **Specify the user groups** to activate 2FA in the **Operation permission** detail. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

#### 5\. Set for how long the verification code remains active (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-9 "Direct link to 5. Set for how long the verification code remains active (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "2FA confirmation code lifetime (seconds)" ("SecondFactorCodeTTL" code) system setting.
4. **Specify for how long to keep the verification code active** in seconds in the **Default value** field.
5. **Save the changes**.

#### 6\. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-10 "Direct link to 6. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "The number of attempts to verify the second factor" ("SecondFactorAttemptCount" code) system setting.
4. **Specify how many attempts to verify the second factor the user** has before they are locked out or deactivated in the **Default value** field. The exact penalty depends on the value of the "User locking time" ("UserLockoutDuration" system setting).
5. **Save the changes**.

#### 7\. Customize the 2FA email (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-11 "Direct link to 7. Customize the 2FA email (optional)")

1. **Open** the **Studio** workplace → **Message templates**.
2. Open and edit the "2FA verification code" template to **customize the 2FA email**. Learn more: [Work with message templates](https://academy.creatio.com/documents?id=2357).

### Set up 2FA via SMS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-3 "Direct link to Set up 2FA via SMS")

This authentication method sends the verification code to the phone specified in the **Phone** field of the system user via SMS. The method requires an additional integration with the cell connection provider. Before you set up this method, make sure all users have the phone specified and you integrated the cell connection provider. Instructions: [Integrate the cell connection provider with Creatio for two-factor authentication via SMS](https://academy.creatio.com/documents?id=15164) (developer documentation).

#### 1\. Activate the SMS 2FA method [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-12 "Direct link to 1. Activate the SMS 2FA method")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **Lookups**.
3. **Open** the **2FA methods** lookup.
4. Click the **SMS** row → **select the checkbox** in the **Enabled** column.
5. **Select the checkbox** in the **Primary** column if you want SMS to be the main 2FA method.
6. **Click**![btn_select.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_select.png).

#### 2\. Activate 2FA [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-14 "Direct link to 2. Activate 2FA")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "Enable 2FA" ("Enable2FA" code) system setting.
4. **Select** the **Default value** checkbox.
5. **Save the changes**.

At this point, the users can already use 2FA. Proceed further to customize additional aspects of the functionality.

#### 3\. Specify the user groups to activate 2FA (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-15 "Direct link to 3. Specify the user groups to activate 2FA (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **Users and administration** block → **Operation permissions**.
3. **Open** the "Can use 2FA" ("CanUse2FA" code) system operation.
4. **Specify the user groups** to activate 2FA in the Operation permission detail. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

#### 4\. Set for how long the verification code remains active (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-16 "Direct link to 4. Set for how long the verification code remains active (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "2FA confirmation code lifetime (seconds)" ("SecondFactorCodeTTL" code) system setting.
4. **Specify how long to keep the verification code active** in seconds in the **Default value** field.
5. **Save the changes**.

#### 5\. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-17 "Direct link to 5. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "The number of attempts to verify the second factor" ("SecondFactorAttemptCount" code) system setting.
4. **Specify how many attempts to verify the second factor the user has** before they are locked out or deactivated in the **Default value** field. The exact penalty depends on the value of the "User locking time" ("UserLockoutDuration" system setting).
5. **Save the changes**.

### Set up 2FA via the authenticator app​ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-4 "Direct link to Set up 2FA via the authenticator app​")

This authentication option uses the verification code generated by an authenticator app. You can use an app of your choice, for example, Google Authenticator, Microsoft Authenticator, etc.

#### 1\. Activate the authenticator app​ 2FA method [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-18 "Direct link to 1. Activate the authenticator app​ 2FA method")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **Lookups**.
3. **Open** the **2FA methods** lookup.
4. Click the **Authenticator app** row → **select the checkbox** in the **Enabled** column.
5. **Select the checkbox** in the **Primary** column if you want email to be the default 2FA option.
6. **Click**![btn_select.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_select.png).

#### 2\. Activate 2FA [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-19 "Direct link to 2. Activate 2FA")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "Enable 2FA" ("Enable2FA" code) system setting.
4. **Select** the **Default value** checkbox.
5. **Save the changes**.

At this point, the users can already use 2FA. Proceed further to customize additional aspects of the functionality.

#### 3\. Specify the user groups to activate 2FA (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-20 "Direct link to 3. Specify the user groups to activate 2FA (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **Users and administration** block → **Operation permissions**.
3. **Open** the "Can use 2FA" ("CanUse2FA" code) system operation.
4. **Specify the user groups** to activate 2FA in the **Operation permission** detail. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

#### 4\. Specify who can disconnect the authenticator app for the user (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-21 "Direct link to 4. Specify who can disconnect the authenticator app for the user (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **Users and administration** block → **Operation permissions**.
3. **Open** the "Can disconnect 2FA authenticator app" ("CanReset2FA" code) system operation.
4. **Specify who can disconnect the authenticator app** for the user in the **Operation permission** detail. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

#### 5\. Set for how long the authenticator app connection code remains valid (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-22 "Direct link to 5. Set for how long the authenticator app connection code remains valid (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "TOTP Setup Token Ttl" ("TotpSetupTokenTtl" code) system setting.
4. **Specify for how long the authenticator app connection code remails valid** in minutes in the **Default value** field.
5. **Save the changes**.

#### 6\. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#title-2538-23 "Direct link to 6. Specify how many attempts to verify the second factor the user has before they are locked out or deactivated (optional)")

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/set_up_two-factor_authentication/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **System setup** block → **System settings**.
3. **Open** the "The number of attempts to verify the second factor" ("SecondFactorAttemptCount" code) system setting.
4. **Specify how many attempts to verify the second factor the user has** before they are locked out or deactivated in the **Default value** field. The exact penalty depends on the value of the "User locking time" ("UserLockoutDuration" system setting).
5. **Save the changes**.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication\#see-also "Direct link to See also")

[Use two-factor authentication](https://academy.creatio.com/documents?id=2539)

[Description of system settings](https://academy.creatio.com/documents?id=1259)

[Integrate the cell connection provider with Creatio for two-factor authentication via SMS](https://academy.creatio.com/documents?id=15164) (developer documentation)

- [Set up 2FA](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#title-2538-1)
  - [Set up 2FA via email](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#title-2538-2)
  - [Set up 2FA via SMS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#title-2538-3)
  - [Set up 2FA via the authenticator app​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#title-2538-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/authentication/set-up-two-factor-authentication#see-also)