<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/windows-authentication)** (8.3).

Version: 8.2

On this page

Windows (NTLM) authentication can be used concurrently with LDAP authentication. Windows authentication requires entering login credentials in the browser. During LDAP authentication, user’s password is checked on the Active Directory server. Both Windows (NTLM) and LDAP authentications trigger when the user clicks the "Log in as domain user" link (provided that the user account is synchronized with LDAP).

note

Windows authentication is only available for Creatio on-site due to cloud architecture specifics.

If the user attempts to log in to the system using the domain credentials, the following authentication algorithm is performed:

1. A user authentication check within the domain is performed.

2. If the domain username and the password are stored in a cookie, they will be retrieved from this cookie. Otherwise, a browser window will be displayed to enter the user credential.

Further steps depend on the user synchronization with the LDAP directory.

3. If the user is not synchronized with LDAP:
   - User authentication check is performed through the comparison of the username and the password from the cookie and the corresponding credentials of the Creatio account. Thus, it is required to specify the same username and password that are used in the domain to enable Windows authentication for the users who are not synchronized with LDAP.
   - Based on the check results, if the data matches and the user account is [licensed](https://academy.creatio.com/documents?id=1472), the user authorization will be performed.
4. If the user is synchronized with LDAP:


   - The browser sends a request to the Active Directory service to authenticate the user.

   - The query returns the credentials of the current domain user that are compared with the username and the password details stored in the cookie.

   - If the data matches and the user account is [licensed](https://academy.creatio.com/documents?id=1472), the user authorization will be performed.



     note





     User authentication is performed either for the users of the main application or for the self-service portal users. You can set the check order in the Web.config file of the loader application. Learn more: [Set up the Web.config file of the loader application](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#title-306-2).


To use Windows authentication via the NTLM protocol, first add system users (manually or by importing from LDAP) and license them. Users will need to allow writing local data to cookie files in their browsers to be able to store the data locally.

The authentication setup is performed on the application server and consists of two steps:

- IIS server setup that activates authentication using the NTLM protocol. Learn more: [Set up the Windows authentication on IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#title-306-1).
- Web.config file setup of the loader application that defines authentication providers and users availability check order among those registered in Creatio. Learn more: [Set up the Web.config file of the loader application](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#title-306-2).

## Set up the Windows authentication on IIS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication\#title-306-1 "Direct link to Set up the Windows authentication on IIS")

1. Enable anonymous authentication and form authentication for both the web application and loader application (Fig. 1).
Fig. 1 Authentication settings for the loader application in IIS

![Fig. 1 Authentication settings for the loader application in IIS](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/windows_authentication/chapter_ldap_synchronization_ntlm_auth.png)




note





Make sure you disable the "Windows Authentication" setting that is enabled in IIS by default.

2. Disable the form authentication; enable anonymous authentication and Windows authentication for the "Login" directory within the loader application (Fig. 2).
Fig. 2 The login directory settings

![Fig. 2 The login directory settings](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/Windows_authentication/chapter_ldap_synchronization_ntlm_login_auth.png)


Please note that anonymous authentication of the loader application and working applications must be conducted under application pool identity. To enable this, edit anonymous authentication credentials by clicking the **Edit** button in the **Actions** area of the IIS manager and select **Application pool identity** (Fig. 3).

Fig. 3 Enter the credentials for anonymous authentication in IIS

![Fig. 3 Enter the credentials for anonymous authentication in IIS](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/windows_authentication/chapter_ldap_synchronization_ntlm_auth_anonymous.png)

note

Learn more about Windows Authentication in [Microsoft documentation](https://technet.microsoft.com/en-us/library/828f9515-cc83-435e-bee3-1ebe14711fb8).

## Set up the Web.config file of the loader application [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication\#title-306-2 "Direct link to Set up the Web.config file of the loader application")

1. Open the Web.config file of the loader application to be edited.

2. In this file, specify the Windows Authentication providers:





```js
auth providerNames="InternalUserPassword,SSPLdapProvider,Ldap"
autoLoginProviderNames="NtlmUser,SSPNtlmUser"
```









**InternalUserPassword** – provider that is specified in the Web.config file by default. If you want to provide NTLM authentication only for the users who are not synchronized with LDAP, do not specify an additional value for the providerNames parameter.

**Ldap** – add this provider to the **providerNames** parameter values. As a result, the users who are synchronized with LDAP will be able to perform NTLM authentication.

**SSPLdapProvider** – add this parameter to the **providerNames** parameter value for the users of the self-service portal who are synchronized with LDAP to be able to perform NTLM authentication.

**NtlmUser** – add this provider to the **autoLoginProviderNames** parameter value. As a result, the users will able to perform NTLM authentication regardless of their synchronization with LDAP and the authentication type configured for these Creatio users.

**SSPNtlmUser** – add this parameter to the **autoLoginProviderNames** parameter value for the users of the self-service portal to be able to perform NTLM authentication regardless of their synchronization with LDAP and the authentication type configured for these Creatio users.

The record order of the **autoLoginProviderNames** parameter defines the order, in which Creatio checks if the system users are available in the list of application users (NtlmUser) or in the list of the self-service portal users (SSPNtlmUser). For example, if you want the check to be performed among the main application users primarily, place the **NtlmUser** provider at the top of the list of the values of the **autoLoginProviderNames** parameter.



Important





You can specify the **SSPNtlmUser** provider as an **autoLoginProviderNames** parameter value only if the **NtlmUser** provider is specified additionally. You can use the **NtlmUser** provider separately.

3. If you want to authenticate in Creatio at once, specify the "true" value for the **UsePathThroughAuthentication** parameter of the `<appSettings>` element:





```xml
<appSettings>
       <add key="UsePathThroughAuthentication" value="true" />
       ...
</appSettings>
```


If you want the login page to be displayed with the available **Log in as domain user** link, specify the "false" value for the **UsePathThroughAuthentication** parameter. The end-to-end authentication will be performed only when accessing application main page. Add "/Login/NuiLogin.aspx" to Creatio website address.

As a result, users will be able to log in to Creatio as domain users. They may still be required to enter their credentials in a domain authentication window, which will pop up on login attempt.

To prevent displaying of the domain authentication window:

1. Click "Start" → "Settings" → "Control Panel" → "Network and Internet" menu and select "Internet options" (Fig. 4).
Fig. 4 Access the Internet options of the Windows Explorer

![Fig. 4 Access the Internet options of the Windows Explorer](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/windows_authentication/chapter_ldap_synchronization_ie_internet_options.png)

2. In the opened window, select the "Security" tab and click the "Custom level" button to go to security settings (Fig. 5).
Fig. 5 The security settings

![Fig. 5 The security settings](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/windows_authentication/chapter_ldap_synchronization_ie_internet_options_security_tab.png)

3. In the "User authentication" group of settings, select the "Automatic logon with current user name and password" authentication method (Fig. 6).
Fig. 6 Select the user authentication method

![Fig. 6 Select the user authentication method](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/windows_authentication/chapter_ldap_synchronization_ie_internet_options_user_authentication.png)

4. Click "OK."

As a result, the users who are already authenticated in the domain will be able to log in to Creatio by clicking the "Log in as domain user" link, and will not have to re-enter their domain credentials each time they access Creatio.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication\#see-also "Direct link to See also")

[Windows authentication](internal:#XREF_43633_NTLM)

[How Windows authentication works](internal:#XREF_36524__NTLM)

- [Set up the Windows authentication on IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#title-306-1)
- [Set up the Web.config file of the loader application](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#title-306-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/windows-authentication#see-also)