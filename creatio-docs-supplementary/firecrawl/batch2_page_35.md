<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.1

On this page

In Creatio, user's access permissions are determined by multiple factors:

- **User type**. You need to create and license a user account for each Creatio user. Each user record must be linked to a specific contact.
- **Personal license type** grants user access to Creatio platform and functionality.
- **Access to business data** grants permission to perform CRUD (creating, reading, updating and deleting) operations with data.
- **Access to functionality** can be granted via system operations. System operations let you manage access to a broad list of Creatio functionality, including user registration, workplace setup, lookup management, system configuration, etc.

Access permissions are set up by your company's system administrator and can be changed whenever you need. User type and license restrictions are set up by Creatio company and cannot be changed. The resulting set of user permissions is the combination of all mentioned settings.

Fig. 1 Access restrictions in Creatio

![Fig. 1 Access restrictions in Creatio](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/users_and_access_overview/scr_access_rights_mechanisms.png)

## User type restrictions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#title-2432-1 "Direct link to User type restrictions")

Creatio has two types of users: external user and company employee. **Company employee** type has only one restriction. You cannot issue this user an external license. **External user** type has the following restrictions:

- Cannot be a part of the "All employees" organizational role.
- User's email address cannot use your company domain.
- Chats, email synchronization, and phone integration are not available.
- App creation and customization are not available.
- Cannot be imported from LDAP.

Since Creatio version 8.0.10 set access permissions for external users in the **Object permissions** section. You do not need to use the "List of objects available for external users" and "List of schema fields for external access" lookups.

Objects must have operation permissions set up to be available for external users. Creatio warns you if you have not set up permissions to dropdown fields of an object on a page available for external users or the permissions you have set up are not secure.

Fig. 2 Object permission warning

![Fig. 2 Object permission warning](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_8_0_10/scr_permission_warning.png)

Instructions for Creatio versions 8.0.9 and earlier you can find in the [Manage Portal Creatio in the main application](https://academy.creatio.com/documents?id=2456#title-2837-7) article.

## Restrictions of personal license types [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#title-2432-2 "Direct link to Restrictions of personal license types")

Creatio version 8.0.9 and earlier support only one type of personal license. Creatio version 8.0.10 and later support the following personal license types that have different restrictions:

- external user license,
- limited internal user license,
- mobile-only user license,
- full user license.

Learn more: [Creatio licenses overview](https://academy.creatio.com/documents?id=1264).

## Access to business data [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#title-2432-3 "Direct link to Access to business data")

To grant access to business data, configure access permissions to corresponding Creatio objects. Creatio objects are roughly equivalent to database tables and correspond to sections, details, lookups, etc.

You can manage access to business data on several levels:

- Ability to perform CRUD operations with any data of an object. Learn more: [Object operation permissions](https://academy.creatio.com/documents?id=262).
- Ability to view, edit or delete individual records. Learn more: [Record permissions](https://academy.creatio.com/documents?id=1966).
- Ability to view, edit or delete values of individual object columns. Learn more: [Column permissions](https://academy.creatio.com/documents?id=264).

## Access to functionality [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#title-2432-4 "Direct link to Access to functionality")

Permissions to add, view, edit, and delete object data cannot be used to manage access to some Creatio functionality. For example, import and export operations, business process creation, workplace setup, system configuration, etc. Use system operations to manage access to such functionality. System operation permissions (access to Creatio functionality) are different from object operation permissions (access to CRUD operations in objects). A system operation can have one of the two access levels:

- User or role can perform the operation.
- User or role cannot perform the operation.

Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

## Troubleshoot access [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#title-2432-5 "Direct link to Troubleshoot access")

License restrictions work together with user type restrictions and access permissions. If a user has problems with access to some Creatio data, check the following:

- user type
- personal license type
- access permissions set up for the object that the user cannot reach

Example

The user cannot open the **Requests** section.

To troubleshoot the issue:

1. Check the user type.
1. If the user is a company employee, proceed to step 2.

2. If the user is an external user, check whether the **Requests** section has an external page.
      1. If the section has an external page, proceed to step 2.
      2. If the section has no external page, create and configure the page. Instructions: [Customize Portal Creatio in Freedom UI](https://academy.creatio.com/documents?id=2460).
2. Check the user’s license type and organizational role.

3. Check the access permissions set up for the "Requests" object.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview\#see-also "Direct link to See also")

[Creatio licensing](https://academy.creatio.com/documents?id=1264)

[Manage user licenses](https://academy.creatio.com/documents?id=1472)

- [User type restrictions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#title-2432-1)
- [Restrictions of personal license types](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#title-2432-2)
- [Access to business data](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#title-2432-3)
- [Access to functionality](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#title-2432-4)
- [Troubleshoot access](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#title-2432-5)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/user-access-overview#see-also)