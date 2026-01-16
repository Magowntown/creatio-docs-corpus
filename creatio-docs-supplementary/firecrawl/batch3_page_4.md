<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication)** (8.3).

Version: 8.2

On this page

## Set up user authentication through LDAP on .NET Framework [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication\#title-2020-24 "Direct link to Set up user authentication through LDAP on .NET Framework")

To enable user authentication through LDAP, modify the Web.config file in the Creatio root folder. Active Directory and OpenLDAP settings are different.

1. Specify "Ldap" and "SspLdapProvider" in the list of available authentication providers. The step is the same for Active Directory and OpenLDAP.





```xml
<terrasoft>
       <auth providerNames="InternalUserPassword,SSPUserPassword,SsoAuthProvider,SSPSsoAuthProvider,Ldap,SSPLdapProvider" autoLoginProviderNames="" defLanguage="en-US" defWorkspaceName="Default" useIPRestriction="false" loginTimeout="30000">
       <providers>
```







Important





Upper/lowercase characters must be as in the example. Also, note that the provider names must be separated by commas with no blank spaces.

2. Specify the server IP or URL, as well as user domain parameters in the "Ldap" section. Active Directory and OpenLDAP parameters are different.



   - For Active Directory
   - For OpenLDAP

```xml
<provider name="Ldap" type="Terrasoft.WebApp.Loader.Authentication.Ldap.LdapProvider, Terrasoft.WebApp.Loader">
<parameters>
    ...
    <add name="ServerPath" value="testactivedirectory.com" />
    <add name="AuthType" value="Ntlm" />
    <add name="DistinguishedName" value="dc=tscrm,dc=com" />
    <add name="UseLoginUserLDAPEntryDN" value="false" />
    <!--<add name="SearchPattern"
    value="(&amp;(objectCategory=person)(objectClass=user)
    (!(userAccountControl:1.2.840.113556.1.4.803:=2))
    memberOf=CN=SVNUsers,OU=groups,OU=Terrasoft,DC=tscrm,DC=com))" />-->
    <add name="SearchPattern"
    value="(&amp;(sAMAccountName={0})(objectClass=person))" />
    <!--With Kerberos authentication-->
    <add name="KeyDistributionCenter" value="ctl.com" />
</parameters>
```

```xml
<provider name="Ldap" type="Terrasoft.WebApp.Loader.Authentication.Ldap.LdapProvider, Terrasoft.WebApp.Loader">
<parameters>
    ...
    <add name="ServerPath" value="testopenldap.com" />
    <add name="AuthType" value="Basic" />
    <add name="DistinguishedName" value="dc=example,dc=org" />
    <add name="UseLoginUserLDAPEntryDN" value="true" />
    <add name="SearchPattern"
    value="(&amp;(uid={0})(objectClass=inetOrgPerson))" />
    <!--With Kerberos authentication-->
    <add name="KeyDistributionCenter" value="ctl.com" />
</parameters>
```

   - **ServerPath** – the LDAP server domain name. It must be a URL, not an IP address.
   - **KeyDistributionCenter** – the domain name. It must be a URL, not an IP address.

note

If you select "Kerberos" authentication type, make sure your Creatio application server is joined to the same domain as the LDAP server and the key distribution center.

3. Specify the server IP or URL, as well as portal user domain parameters in the "SspLdapProvider" section. The step is the same for Active Directory and OpenLDAP:





```xml
<provider name="SSPLdapProvider" type="Terrasoft.WebApp.Loader.Authentication.SSPUserPassword.SSPLdapProvider, Terrasoft.WebApp.Loader">
<parameters>
       ...
       <add name="ServerPath" value="ldapserver.domain.com" />
       ...
       <add name="DistinguishedName" value="dc=domain, dc=com" />
       ...
</parameters>
```

4. Save the changes in the Web.config file.

5. **Additional step for OpenLDAP**: before you synchronize with the OpenLDAP server, specify the "true" value for "UseLoginUserLDAPEntryDN" in the Web.config file of Terrasoft.WebApp.





```xml
<appSettings>
       ...
       <add key="UseLoginUserLDAPEntryDN" value="true" />
```


This setting ensures that Creatio does not us an empty **LDAPEntryDN** field in the **SysAdminUnit** table to synchronize the users. An empty **LDAPEntryDN** field is known to cause authentication issues.

## Set up user authentication through LDAP on .NET [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication\#title-2020-25 "Direct link to Set up user authentication through LDAP on .NET")

To enable user authentication through LDAP, modify the Terrasoft.WebHost.dll.config file in the Creatio root folder. Active Directory and OpenLDAP settings are the same.

1. Specify "Ldap" in the list of available authentication providers. Add the "SspLdapProvider" provider to allow portal users to log in to Creatio:





```xml
<terrasoft>
       <auth providerNames="InternalUserPassword,SSPUserPassword,SsoAuthProvider,SSPSsoAuthProvider,Ldap,SSPLdapProvider" autoLoginProviderNames="" defLanguage="en-US" defWorkspaceName="Default" useIPRestriction="false" loginTimeout="30000">
       <providers>
```







Important





Upper/lowercase characters must be as in the example. Also note that the provider names must be separated by commas with no blank spaces.

2. Specify the "Ldap" authentication provider settings:





```xml
<provider name="LdapProvider" type="Terrasoft.Authentication.Core.Ldap.NetStandardLdapProvider, Terrasoft.Authentication">
       <parameters>
           <add name="ServerPath" value="testldap.com" />
           <add name="DistinguishedName" value="dc=ctl,dc=com" />
           <add name="UseLoginUserLDAPEntryDN" value="false" />
           <add name="SearchPattern" value="(&amp;(sAMAccountName={0})(objectClass=person))" />
           <add name="KeyDistributionCenter" value="ctl.com" />
           <!--When using LDAPS-->
           <add name="SecureSocketLayer" value="false" />
           <add name="CertificateFileName" value="" />
       </parameters>
</provider>
```






   - **ServerPath** is the LDAP server domain name. It must be a URL address, not an IP address.
   - **KeyDistributionCenter** is the domain name. It must be a URL address, not an IP address.

note

If you select "Kerberos" authentication type, make sure your Creatio application server is joined to the same domain as the LDAP server and the key distribution center.

To use the **secure LDAPS protocol**, specify the following parameters in the authentication provider settings:
   - **SecureSocketLayer** is the flag that enables LDAPS.

   - **CertificateFileName** is the name of the SSL certificate that validates the LDAPS connection. The certificate must be located in the Creatio root folder. This is a requried parameter if "SecureSocketLayer=true" is specified. For instance:





     ```xml
     <add name="CertificateFileName" value="ldap_certificate_example.cer" />
     <add name="SecureSocketLayer" value="true" />
     ```
3. Specify the server IP or URL, as well as portal user domain parameters in the "SspLdapProvider" section.





```xml
<provider name="SSPLdapProvider" type="Terrasoft.WebApp.Loader.Authentication.SSPUserPassword.SSPLdapProvider, Terrasoft.WebApp.Loader">
       <parameters>
           <add name="ServerPath" value="ldapserver.domain.com" />
           ...
           <add name="DistinguishedName" value="dc=domain, dc=com" />
           ...
       </parameters>
```

4. Save the changes in the Terrasoft.WebHost.dll.config file.


## Set up the authentication providers [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication\#title-2020-26 "Direct link to Set up the authentication providers")

The authentication provider setup is the same for Creatio **.NET Framework**, Creatio **.NET**. Modify the following files in the Creatio root directory:

- **Web.config** for Creatio **.NET Framework**.
- **Terrasoft.WebHost.dll.config** for Creatio **.NET**.

Open the file in a text editor and specify the authentication providers:

```js
auth providerNames="InternalUserPassword,SSPLdapProvider,Ldap"
autoLoginProviderNames="NtlmUser,SSPNtlmUser"
```

- **InternalUserPassword** – the default provider. If you would like to provide NTLM authentication only to the users not synchronized with LDAP, do not specify additional values for the **providerNames** parameter.
- **Ldap** – add this provider to the **providerNames** parameter value to provide NTLM authentication to the users synchronized with LDAP.
- **SSPLdapProvider** – add this provider to the **providerNames** parameter value to provide NTLM authentication to the self-service portal's users synchronized with LDAP.
- **NtlmUser** – add this provider to the **autoLoginProviderNames** parameter value to provide NTLM authentication to the main application's users regardless of their LDAP synchronization status and the authentication type configured for the users in Creatio.
- **SSPNtlmUser** – add this provider to the **autoLoginProviderNames** parameter value to provide NTLM authentication to the self-service portal's users regardless of their LDAP synchronization status and the authentication type configured for the Creatio users.
- The order of records in the **autoLoginProviderNames** parameter defines the order in which Creatio checks if its users are available in the main application's user list (NtlmUser) or the self-service portal's user list (SSPNtlmUser). For example, if you would like Creatio to check the main application's user list first, put the **NtlmUser** provider at the head of the list of **autoLoginProviderNames** parameter values.

Important

Only specify the **SSPNtlmUser** provider as the **autoLoginProviderNames** parameter's value if you also specify the **NtlmUser** provider. However, you can use the **NtlmUser** parameter without the other providers.

## Set up the domain authentication [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication\#title-2020-27 "Direct link to Set up the domain authentication")

If you would like to activate the **pass-through authentication** that lets users authenticate in Creatio without visiting the login page, specify the "true" value for the **UsePathThroughAuthentication** parameter of the `<appSettings>` element:

```xml
<appSettings>
    <add key="UsePathThroughAuthentication" value="true" />
    ...
</appSettings>
```

If you would like to **display the login page** with the available **Log in as domain user** link, specify the "false" value for the **UsePathThroughAuthentication** parameter. The pass-through authentication will be performed only when accessing the main Creatio page. Add "/Login/NuiLogin.aspx" to the Creatio website address to display the login page.

As a result, users will be able to log in to Creatio as domain users. They may still be required to enter their credentials in a domain authentication window, which will pop up on a login attempt. Modify Windows settings to prevent the domain authentication window from being displayed:

1. Click "Start" → "Settings" → "Control Panel" → "Network and Internet" menu. Select "Internet options" (Fig. 1).
Fig. 1 Modifying Windows settings

![Fig. 1 Modifying Windows settings](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/LDAP/chapter_ldap_synchronization_ie_internet_options.png)

2. This will open a new window. Select the "Security" tab and click "Custom level" to go to security settings (Fig. 2).
Fig. 2 Security settings

![Fig. 2 Security settings](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/LDAP/chapter_ldap_synchronization_ie_internet_options_security_tab.png)

3. Select the "Automatic logon with current user name and password" authentication methods in the "User authentication" settings group (Fig. 3).
Fig. 3 Selecting the authentication method

![Fig. 3 Selecting the authentication method](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/LDAP/chapter_ldap_synchronization_ie_internet_options_user_authentication.png)

4. Click "OK."


As a result, the domain authentication window will not pop up and the users will not have to re-enter their domain credentials each time they access Creatio.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication\#see-also "Direct link to See also")

[Set up LDAP synchronization](https://academy.creatio.com/documents?id=513)

[Set up Active Directory filters](https://academy.creatio.com/documents?id=1868)

[Import new users and roles from Active Directory](https://academy.creatio.com/documents?id=1996)

- [Set up user authentication through LDAP on .NET Framework](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#title-2020-24)
- [Set up user authentication through LDAP on .NET](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#title-2020-25)
- [Set up the authentication providers](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#title-2020-26)
- [Set up the domain authentication](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#title-2020-27)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/synchronize-users-with-ldap/set-up-ldap-authentication#see-also)