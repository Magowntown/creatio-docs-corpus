<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/export-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/export-permissions)** (8.3).

Version: 8.1

On this page

Grant permissions to export lists of either specific objects or all Creatio sections to roles and individual users.

Data export permissions are a subset of Creatio [object permissions](https://academy.creatio.com/documents?id=1966). You can grant full data export permissions to some roles and users. For example, the company management. To do this, grant them permission to the "Export list records" (the "CanExportGrid" code) [system operation](https://academy.creatio.com/documents?id=2000). If the information is confidential and sensitive, we recommend setting up export permissions for specific objects. For example, grant permission to export invoices to the finance department managers.

Example

Set up permission to export only the invoice list for the "Finance department managers" role.

1. Go to the System designer. For example, click the ![btn_system_designer.png](https://academy.creatio.com/docs/sites/en/files/documentation/user/en/licensing/BPMonlineHelp/licensing_manage/btn_system_designer.png) button.

2. Go to the "Users and administration" block → "Object permissions."

3. Find the needed section, lookup, or detail object in the Creatio object list. Apply the "Sections" filter and select the "Invoice" object.

4. Click the name or title of the object to open the permission setup page of the **Invoices** section object.

5. Go to the **Advanced operations** tab of the permission setup page.

6. Click the **Add** button. This will open a dialog box. Specify the role or user to whom to grant the list export permission in the box.
1. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Platform_basics/export_excel/icon_search.png) in the **User or role who obtains permissions** field. Select the needed organizational role, functional role, or user, then click **Select** to confirm the action.
2. Specify "Export" in the **Entity operation** field.
3. Click the **Add** button to confirm the selection.
7. Repeat step 6 to grant the export permission to other roles and users, if needed.

8. Click the **Apply** button to save the settings (Fig. 1).
Fig. 1 Set up the list export permission

![Fig. 1 Set up the list export permission](https://academy.creatio.com/docs/sites/en/files/images/Platform_basics/export_excel/export_save_role_1.png)


As a result, employees that have the "Finance department managers" role will be able to export only the **Invoices** section list. They will not be able to export other Creatio lists.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/export-permissions\#see-also "Direct link to See also")

[Excel data export](https://academy.creatio.com/documents?id=1864)

[Record permissions](https://academy.creatio.com/documents?id=1966)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/access-management/export-permissions#see-also)