<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/remote-access-for-creatio-support)** (8.3).

Version: 8.1

On this page

Creatio cloud users can set up secure remote access for Creatio technical support specialists to troubleshoot and resolve cases faster. Remote access sessions will not compromise your personal and commercial data security since you do not have to share your login credentials with support.

note

Remote support sessions use the following system settings: "Default external access client id" (DefaultExternalAccessClientId), "Identity server client secret" (IdentityServerClientSecret), Identity server Url (IdentityServerUrl), "Identity server client id" (IdentityServerClientId). The values in these system settings are populated automatically.

- To hide section record data from the technical support specialists, use the **data isolation mode**.
- To restrict technical support specialists from modifying configuration settings, use the **configuration restriction mode**. The support specialists will still have permission to read configuration settings needed to resolve the customer’s case.

To enable remote support access, a user must have system administrator privileges (have the "System administrators" role). Technical support specialists can connect remotely under the administrator account or the account of any other application user. All remote support session data are logged and can be retrieved later. Logged connection data include the time of the connection and information on which data were modified during the session.

## Set up remote sessions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support\#title-293-1 "Direct link to Set up remote sessions")

1. Click ![btn_help_1.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/external_access/btn_help_1.png) → "Grant access to support" in the upper right corner of the application window. ( [Fig. 1](https://academy.creatio.com/#XREF_42442_487))
Fig. 1 Locating remote sessions set up in the help menu

![Fig. 1 Locating remote sessions set up in the help menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/external_access/chapter_external_access_via_help_btn.png)




note





To grant access to support, you need permissions to read and add records in the "External access" object. Users with the "System administrators" role have these permissions by default. Learn more about object operation permissions in the " [Managing object operation permissions](https://academy.creatio.com/documents?product=administration&ver=7&id=262)" article.

2. Fill out the displayed mini page ( [Fig. 2](https://academy.creatio.com/#XREF_82683_487)):
Fig. 2 Remote session parameters

![Fig. 2 Remote session parameters](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/external_access/chapter_external_access_parameters.png)

3. In the **Reason to grant access** field, specify what problem requires granting access to support, the request number, or the list of services a technical support specialist has to provide.

4. In the **Access close date** field, specify the date when the granted access expires. Granted access will expire at 11:59 PM on the specified date.

5. In the **Grantor** field, the user who is granting access is specified by default. You can specify a different user account to use by technical support specialists for accessing your application.

6. Select or clear the **Deny access to data** and **Deny configuration** checkboxes to enable or disable the data isolation mode and configuration restriction mode respectively. By default, both checkboxes are selected. This means that a technical support specialist will not be able to see your section record data or configure the system.
   - If you need the technical support specialist to have the same permissions as the user under whose account remote access is granted, clear both of the checkboxes.
   - If you need the technical support specialist to modify the current configuration without being able to see your records, only clear the **Deny configuration** checkbox. The technical support specialist will also be able to access the System designer functions required for updating configuration (for instance, the **Lookups**, **Advanced settings**, **Process library** sections and more). The record data in the main sections will remain unavailable to the Creatio support.
   - If you need the technical support specialist to be able to access your records without being able to modify the configuration of the system, you should only clear the **Deny access to data** checkbox. In this case, Creatio support will be able to access the system configuration in the read-only mode.
7. Save the record.

As a result, a new record will be added in the **External access** section. Technical support specialists will be able to log in under the user account specified as the **Grantor**. Support specialists will not need login credentials. The specialists will have access to the corresponding permissions not otherwise restricted in the sessions settings. The remote access session will expire on the specified date at 11:59 PM.


## View remote access logs [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support\#title-293-2 "Direct link to View remote access logs")

1. Open the System designer and click **External access** ( [Fig. 1](https://academy.creatio.com/#XREF_32923_488)).
Fig. 1 The External access section

![Fig. 1 The External access section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/external_access/chapter_external_access_section.png)

2. Open the required record in the section list. On the record page, you can view all access parameters ( [Fig. 2](https://academy.creatio.com/#XREF_48138_491)). After the support session is over, the **Sessions** tab will display the session data.
Fig. 2 An example record with remote access parameters in the External access section

![Fig. 2 An example record with remote access parameters in the External access section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/external_access/chapter_external_access_record_page_example.png)


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support\#see-also "Direct link to See also")

[Add a regular employee user](https://academy.creatio.com/documents?id=2009)

- [Set up remote sessions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support#title-293-1)
- [View remote access logs](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support#title-293-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/remote-access-for-creatio-support#see-also)