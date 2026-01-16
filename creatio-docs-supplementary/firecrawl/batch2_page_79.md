<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-management/unblock-a-user)** (8.3).

Version: 8.1

On this page

If the user [mistypes their credentials](https://academy.creatio.com/documents?id=2385&anchor=title-2108-5) several times in a row, their account will be blocked for some time.

The system administrator can [set up the blocking conditions](https://academy.creatio.com/documents?id=2385&anchor=title-2108-1):

- the number of attempts after which the user account is blocked
- the period after which the user account is unblocked.

## User account blocking principles [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#title-2108-5 "Direct link to User account blocking principles")

Several [system settings](https://academy.creatio.com/documents?id=1259&anchor=title-1880-28) are considered when blocking a user account:

- "Number of logon attempts" ("LoginAttemptCount" code).
- "Quantity of login attempts for warning message" ("LoginAttemptBeforeWarningCount" code).
- "User locking time" ("UserLockoutDuration" code).

The user account blocking **mechanism** is as follows:

- If the number of failed login attempts does not exceed the value of the **"Number of logon attempts"** ("LoginAttemptCount" code) system setting, Creatio displays a failed login attempt message (Fig. 1).
Fig. 1 A failed login attempt message

![Fig. 1 A failed login attempt message](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/unblock_user/scr_incorrect_password_message.png)

- If the number of failed login attempts exceeds the value of the **"Number of logon attempts"** ("LoginAttemptCount" code) system setting, Creatio displays a lockout warning message (Fig. 2).
Fig. 2 A lockout warning message

![Fig. 2 A lockout warning message](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/unblock_user/scr_warning_message.png)

- If the number of failed login attempts equals the value of the **"Quantity of login attempts for warning message"** ("LoginAttemptBeforeWarningCount" code) system setting, Creatio displays a lockout message (Fig. 3).
Fig. 3 A lockout message

![Fig. 3 A lockout message](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/unblock_user/scr_block_message.png)


As a result, the user will be blocked for the period specified in the **"User locking time"** ("UserLockoutDuration" code) system setting. The user account will be unblocked after the specified period. To unblock a user account earlier, use the following instruction: [Unblock a user account](https://academy.creatio.com/documents?id=2385&anchor=title-2108-2).

## Specify the user account blocking conditions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#title-2108-1 "Direct link to Specify the user account blocking conditions")

### Set the number of login attempts [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#title-2108-3 "Direct link to Set the number of login attempts")

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/licensing/BPMonlineHelp/licensing_creatio/btn_system_designer.png) to open the System Designer.

2. Click **"System settings"** in the "System setup" block.

3. Open the **"Number of logon attempts"** system setting ("LoginAttemptCount" code).

Specify the acceptable number of failed login attempts in the **Default value** field. The recommended system setting value is 5.

4. Open the **"Quantity of login attempts for warning message"** system setting ("LoginAttemptBeforeWarningCount" code).

Specify the number of failed login attempts after which Creatio displays the lockout warning message in the **Default value** field. The user will be blocked after the next failed login attempt. The recommended system setting value is 3.


note

The value of the "Number of logon attempts" system setting ("LoginAttemptCount" code) must not exceed that of the "Quantity of login attempts for warning message" system setting ("LoginAttemptBeforeWarningCount" code).

### Set up the user lockout period [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#title-2108-4 "Direct link to Set up the user lockout period")

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/licensing/BPMonlineHelp/licensing_creatio/btn_system_designer.png) to open the System Designer.

2. Click **"System settings"** in the "System setup" block.

3. Open the **"User locking time"** system setting ("UserLockoutDuration" code).

Specify the user account blocking time (in minutes) after a number of failed login attempts in the **Default value** field. The recommended system setting value is 15.


As a result, Creatio will set the account blocking conditions for all system users.

## Unblock a user account [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#title-2108-2 "Direct link to Unblock a user account")

To **unblock a user account** before the lockout period expires, do the following:

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/licensing/BPMonlineHelp/licensing_creatio/btn_system_designer.png) to open the System Designer.

2. Click **"System users"** in the "Users and administration" block.

3. Open the user page.

4. Click **Unblock** (Fig. 4).
Fig. 4 Unblock a user

![Fig. 4 Unblock a user](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/unblock_user/scr_unblock_user.png)


As a result, the user account will be unblocked.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user\#see-also "Direct link to See also")

[Description of system settings](https://academy.creatio.com/documents?id=1259)

- [User account blocking principles](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#title-2108-5)
- [Specify the user account blocking conditions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#title-2108-1)
  - [Set the number of login attempts](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#title-2108-3)
  - [Set up the user lockout period](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#title-2108-4)
- [Unblock a user account](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#title-2108-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-management/unblock-a-user#see-also)