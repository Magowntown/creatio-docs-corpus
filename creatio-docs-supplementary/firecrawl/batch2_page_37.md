<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/page-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/page-permissions)** (8.3).

Version: 8.2

On this page

When users try to open pages, Creatio checks for permissions automatically to ensure maximum security and prevent users from accessing unauthorized pages. Page permissions function only in Freedom UI and are applicable to both Freedom UI and Classic UI pages.

The permission checks are as follows:

- **By page data source**. Whether the user has permission to an object when they try to open a page whose data source is that object. If they do not, Creatio loads the desktop instead.
- **By page setting in page data source**. Whether the page is assigned for the user role in the object settings when a user tries to open a form page whose data source is that object. If they do not, Creatio loads the desktop instead.
- **By the availability of a section in the workplace for the list page**. Whether the section list page is added to any workplace the user can access. If it is not, Creatio loads the desktop instead.
- **By Classic UI pages**. Whether the Classic UI page belongs to a section added to a workplace the user can access. If it does not, Creatio loads the desktop instead.

We recommend keeping those checks intact, but you can set up an allowlist of pages users can open regardless of permissions or exclude users and roles from those checks.

You can set up an **allowlist of pages any user can open** regardless of configured permissions. We recommend using this as an exception for pages that cannot be configured using proper access permissions. To do this, add the relevant pages to the **Whitelist of pages to bypass page opening restrictions** lookup. Learn more: [Manage lookup values](https://academy.creatio.com/documents?id=271).

The restrictions do not apply to pages opened via business processes as well as users or roles that have permissions to the “Can use bypass page opening restrictions” (“CanBypassPageOpeningRestrictions” code) system operation. For Creatio instances updated from version 8.1 and earlier, these roles include “All Employees” and “All External Users.” Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258). We recommend using this option only as an exception to provide the best level of security.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/page-permissions\#see-also "Direct link to See also")

[System operation permissions](https://academy.creatio.com/documents?id=258)

[Manage lookup values](https://academy.creatio.com/documents?id=271)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/page-permissions#see-also)