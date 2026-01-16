<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-onelogin#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-onelogin)** (8.3).

Version: 8.2

On this page

You can enable JIT UP (Just-In-Time User Provisioning) when setting up the identity provider integration. Read more: [Single Sign-On via ADFS](https://academy.creatio.com/documents?id=1649), [Single Sign-On via OneLogin](https://academy.creatio.com/documents?id=1650).

To specify contact fields that should be populated with data from the identity provider, configure the mapping of the SAML Assertion fields with Creatio columns. This is done in the SAML Assertion of the identity provider and in the **SAML field name converters to contact field name** lookup.

To set up mapping, you will need a configured account in the identity provider (Fig. 2) with the data required for Creatio.

Fig. 2 Account fields in the OneLogin identity provider

![Fig. 2 Account fields in the OneLogin identity provider](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/just_in_time_user_provisioning/scr_chapter_single_sign_on_jit_setup_onelogin_user_profile.png)

To set up field population parameters:

1. **Ensure** that all required field values are transferred to Creatio. For example, to fill the profile of John Best with data from the **Company**, **Department**, **Email**, **First Name**, **Last Name**, and **Phone** fields (Fig. 3).
Fig. 3 Application parameters in the OneLogin identity provider

![Fig. 3 Application parameters in the OneLogin identity provider](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/just_in_time_user_provisioning/scr_chapter_single_sign_on_jit_setup_onelogin_application_parameters.png)




note





Use the [SAML Decoder](https://chrome.google.com/webstore/detail/saml-message-decoder/mpabchoaimgbdbbjjieoaeiibojelbhm) Google Chrome extension to verify the parameters.

2. **Verify** that correct rules to receive values and update the columns for each required field are specified on the Creatio side. Rules are configured in the **SAML field name converters to contact field name** lookup. Specify a column in the Creatio for each field received from the identity provider. For example, to fill the **Department**, **Account**, **Phone**, **Email**, **Given name**, and **Surname** columns in Creatio, specify them next to the corresponding SAML attributes (Fig. 4).



note





Specify column names in the Creatio database as contact columns.




Fig. 4 The SAML field name converters to contact field name lookup configuration

![Fig. 4 The SAML field name converters to contact field name lookup configuration](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/just_in_time_user_provisioning/scr_chapter_single_sign_on_jit_setup_saml_converter_lookup.png)

3. A field that is missing in the identity provider data can be populated with the value specified in the **Column default value** field of the **SAML field name converters to contact field name** lookup. For example, the OneLogin identity provider does not contain the **Type** field and does not pass it when the user logs on. To populate this field in Creatio, create a rule in the lookup and specify the "Employee" value as default (Fig. 4). In this case, all created contacts will have the "Employee" value in the **Type** field.

4. You can add custom parameters to the OneLogin identity provider and specify macros for them. Learn more about how to work with macros in [OneLogin documentation](https://onelogin.service-now.com/support?id=kb_article&sys_id=f33ad943db109700d5505eea4b9619d1).


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-onelogin\#see-also "Direct link to See also")

[Single Sign-On via ADFS](https://academy.creatio.com/documents?id=1649)

[Single Sign-On via OneLogin](https://academy.creatio.com/documents?id=1650)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-onelogin#see-also)