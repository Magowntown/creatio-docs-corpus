<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/limit-ip-for-login)** (8.3).

Version: 8.1

On this page

Access restrictions to specific IP addresses for some Creatio users can be a part of your company's privacy policies for working with sensitive content. You can apply these restrictions to individual users or user roles. For example, you can restrict your financial department to IP addresses you use in your local network. This way these employees will be able to login to Creatio only from the office.

The restriction setup procedure consists of multiple steps:

1. Set up IP address restrictions in configuration files. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-1)
2. Set up restrictions for users or roles. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-2)
3. Set up operations permissions. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-3)

## Set up IP addresses restrictions in configuration files [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login\#title-2637-1 "Direct link to Set up IP addresses restrictions in configuration files")

Take this step only if you use Creatio **on-site**. If you use Creatio in the **cloud**, contact the support team `support@creatio.com` so that they make the needed changes.

Set the useIPRestriction parameter to true in web.config files of your Creatio instance.

## Set up restrictions for users [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login\#title-2637-2 "Direct link to Set up restrictions for users")

1. Click ![btn_system_designer00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/assigning_roles/btn_system_designer00002.png) → **Organizational roles**.

2. Select the corresponding organization and/or division in the list of organizational roles. This brings up the selected role page to the right.

3. Open **Access rules** tab.

4. Click ![btn_com_add_tab00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/assigning_roles/btn_com_add_tab00003.png) on the **Range of allowed IP addresses** detail and fill out the **Start IP address** and **End IP address** fields.

5. Repeat step 4 for all the needed IP addresses.



note





To set up restrictions for a specific user take the same step on the **Access rules** tab of the user page.

6. Add IP address restrictions for manager role (optional). To do this click ![btn_com_add_tab00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/assigning_roles/btn_com_add_tab00003.png) on the **Range of allowed IP addresses for managers** detail and fill out the **Start IP address** and **End IP address** fields.


## Set up operation permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login\#title-2637-3 "Direct link to Set up operation permissions")

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_system_designer.png) → System Designer → **Operation permissions**.
2. Apply the "Name = Ignore access check by IP address" (or "Code = SuppressIPRestriction") filter. **Click the operation name** to open the operation.
3. Click ![btn_mobile_add_product.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/system_operation_permissions/btn_mobile_add_product.png) and specify the necessary **user/role** on the **Operation permission** detail. For example the "Finance" organizational role. The user/role will show up on the **Operation permission** detail with the "NO" value in the "Access level" column.

As a result, employees that have the "Finance" role will not be able to log in to Creatio outside of the permitted range of IP addresses.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login\#see-also "Direct link to See also")

[Description of system settings](https://academy.creatio.com/documents?id=1259)

- [Set up IP addresses restrictions in configuration files](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-1)
- [Set up restrictions for users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-2)
- [Set up operation permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#title-2637-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/limit-ip-for-login#see-also)