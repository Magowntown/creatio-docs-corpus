<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/system-operation-reference)** (8.3).

Version: 8.2

On this page

System operations to which you can manage access are described below.

## Creatio.ai [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-9 "Direct link to Creatio.ai")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Can run Creatio.ai | CanRunCreatioAI | Permissions to use the Creatio.ai chat panel. |

## User and role administration [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-1 "Direct link to User and role administration")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Manage user list | CanManageUsers | Permissions to add, modify and delete [user accounts](https://academy.creatio.com/documents?id=1426) in the System Designer's user and role management sections. |
| Manage user licenses | CanManageLicUsers | Access to the [License manager](https://academy.creatio.com/documents?id=1472) section. Out of the box, this permission is granted to users that have the "Creatio Maintenance," "Developer," "Administrator," "System administrators" role. Users who have permission to manage licenses can still log in to Creatio and redistribute licenses even if the instance is locked due to exceeding the number of allocated licenses. |
| Change delegated permissions | CanChangeAdminUnitGrantedRight | The ability to delegate the access rights of some users to others using the [Delegate permissions](https://academy.creatio.com/documents?id=1998) detail on the user page. |
| Change system operations permissions | CanChangeAdminOperationGrantee | Ability to manage [access permissions](https://academy.creatio.com/documents?id=258) to system operations. The scope of rights granted by this operation includes the right to register additional system operations. |

## Creatio Portal management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-2 "Direct link to Creatio Portal management")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Manage portal users | CanAdministratePortalUsers | Permissions to add, modify and delete portal user accounts in the System Designer's user and role management sections. |
| Access to portal main page setup module | CanManagePortalMainPage | Permission to set up the [portal main page](https://academy.creatio.com/documents?id=1790). |

## Data management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-3 "Direct link to Data management")

Data management operations refer to all records in all objects. Data access is usually provided to users that have the "System administrators" role.

Important

Access to these operations overrides object permissions (object operations, records and columns). For example, if a user has access to the "View any data" operation, this user will be able to view records of all objects, even those in which the read operation is restricted.

| System operation name | System operation code | Description |
| --- | --- | --- |
| View any data | CanSelectEverything | Permission to view any data in any object. |
| Add any data | CanInsertEverything | Permission to add records to any object. |
| Edit any data | CanUpdateEverything | Permissions to edit any data in any object. |
| Delete any data | CanDeleteEverything | Permission to delete any records in any object. |

## Creatio section management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-5 "Direct link to Creatio section management")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Access to "Access rights" workspace | CanManageAdministration | Access to the [Object permissions](https://academy.creatio.com/documents?id=262) and [Operation permissions](https://academy.creatio.com/documents?id=258) sections. Required for sysAdminUnit record management. Grant access to specific administering operations separately. |
| Access to "Process design" section | CanManageProcessDesign | Access to the [Process Designer](https://academy.creatio.com/documents?id=7003), and the ability to add and modify business processes. |
| Access to "Change log" section | CanManageChangeLog | Access to the [Change log](https://academy.creatio.com/documents?id=506) section. |
| Access to "System settings" section | CanManageSysSettings | Access to the [System settings](https://academy.creatio.com/documents?id=269) section. |
| Access to "Lookups" section | CanManageLookups | Access to the [Lookups](https://academy.creatio.com/documents?id=271) section. |
| Can manage configuration elements | CanManageSolution | Access to the [Configuration](https://academy.creatio.com/documents?id=15101) section. |
| View "Audit log" section | CanViewSysOperationAudit | Permission to to view the contents of the [Audit log](https://academy.creatio.com/documents?id=2320) section. |
| Manage "Audit log" section | CanManageSysOperationAudit | Permission to view the contents of the **Audit log** section and to archive the log. |

## Bulk duplicate search management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-6 "Direct link to Bulk duplicate search management")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Duplicates search | CanSearchDuplicates | Permission to search for duplicates in sections with active [duplicate search rules](https://academy.creatio.com/documents?id=1591). |
| Duplicates processing | CanMergeDuplicates | Permission to merge duplicate records on the duplicate search results page. Additionally, permission to merge records manually in all accessible sections and lookups. |
| Access to "Duplicates rules setup" | CanManageDuplicatesRules | Permission to add and edit duplicate search rules. |

## Integration setting management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-7 "Direct link to Integration setting management")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Access to OData | CanUseODataService | Permission to use OData protocol for external integration. |

## Email setting management [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-8 "Direct link to Email setting management")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Email providers list setup | CanManageMailServers | Permission to create a list of email servers used to send and receive emails. |
| Shared mailbox synchronization setup | CanManageSharedMailboxes | Permission to manage shared mailboxes (mailboxes with the **Allow shared access** checkbox enabled). |

## General settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#title-1885-9 "Direct link to General settings")

| System operation name | System operation code | Description |
| --- | --- | --- |
| Change access rights to record | CanChangeEntitySchemaRecordRight | Lets users grant [record permissions](https://academy.creatio.com/documents?id=1966). The **Use operation permissions** switch must be toggled on in the corresponding object for record permissions to work. |
| Ignore access check by IP address | SuppressIPRestriction | When a user who has access to this operation logs in to the system, the IP address restrictions will be ignored. |
| Export list records | CanExportGrid | Permission to export list data in a \*.xlsx file. If a user does not have permission for this operation, the [Export to Excel](https://academy.creatio.com/documents?id=1864) action in sections and the "List" dashboard tile menu is disabled. |
| Permission to run business processes | CanRunBusinessProcesses | Permission to run business processes in Creatio. All users have permission to perform this operation by default. |
| Cancel running processes | CanCancelProcess | Permission to cancel a running business process in the process log. |
| Access to workplace setup | CanManageWorkplaceSettings | Permission to create and set up [workplaces](https://academy.creatio.com/documents?id=1248), i.e., managing the section list available in the side panel. |
| Access to comments | CanEditOrDeleteComment | Permission to edit and delete comments on the feed messages. |
| Permission to delete messages and comments | CanDeleteAllMessageComment | Permission to delete messages and comments left by other users in the **Feed** section, on the **Feed** tab of the Notification Panel, and on the **Feed** tab of the view and edit pages of system sections. Users can edit and delete their own messages and comments even if they do not have access permissions to this system operation. |

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference\#see-also "Direct link to See also")

[System operation permissions](https://academy.creatio.com/documents?id=258)

[Object permissions by system operations](https://academy.creatio.com/documents?id=2553)

- [Creatio.ai](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-9)
- [User and role administration](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-1)
- [Creatio Portal management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-2)
- [Data management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-3)
- [Creatio section management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-5)
- [Bulk duplicate search management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-6)
- [Integration setting management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-7)
- [Email setting management](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-8)
- [General settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#title-1885-9)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/system-operation-reference#see-also)