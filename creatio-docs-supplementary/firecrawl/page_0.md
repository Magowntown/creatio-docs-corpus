<!-- Source: page_0 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

All Creatio products

On this page

## Why will the mobile app not sync in online mode (Error "Item% 24 batch not found)? [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#title-771-1 "Direct link to Why will the mobile app not sync in online mode (Error \"Item% 24 batch not found)?")

Online sync errors are often associated with the on-site deployment of Creatio. Certain combinations of the IIS, .NET Framework, and ASP.NET services screen special characters ($ character) in website URLs. The mobile app cannot connect to the Creatio website because of that.

To omit the “$” character while generating request URLs, introduce a different type of query generation by setting up configuration files on the Creatio server. To do this:

1. **Open** the **Creatio root directory path** \\Web.config file using any text editor, e.g., Notepad.

2. **Go to** the `<appSettings>` part.

3. **Add** the following line:





```js
<add key="aspnet:UseLegacyRequestUrlGeneration" value="true" />
```

4. **Save the changes**.

5. **Make the same adjustments** to the **Creatio root directory path** \\Terrasoft.WebApp\\Web.config configuration file.

6. **Restart the website** in IIS and clear the Redis server cache.


## How to resolve the synchronization conflict in the offline mode? [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#title-771-2 "Direct link to How to resolve the synchronization conflict in the offline mode?")

If the conflict occurrs because of access permissions during the synchronization with the desktop application, you can resolve it by canceling the modifications you made in the mobile application.

Example

The administrator restricted the permissions to edit the account type for all employees. The mobile user changes the account type in the offline mode. During the synchronization process, the user gets a notification about conflict.

note

Learn more about managing user access permission to the Creatio objects: [Access management](https://academy.creatio.com/docs/8.x/setup-and-administration/category/access-management).

To resolve the conflict:

1. **Tap** the **Review issues** button.

2. **Select** a record that invoked a conflict of permissions in the synchronization log.

3. **Tap** the **Revert changes** button (Fig. 1).
Fig. 1 Revert changes action in the synchronization log

![Fig. 1 Revert changes action in the synchronization log](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Platform_basics/mobile_faq/scr_permission_conflict.png)


As a result, all changes made in the account record will be reverted and the record will be removed from the synchronization log. The local record will be updated with the latest data from the desktop application.

You can send a request for access permission to an administrator. Learn more about actions with records in a separate article: [Get started with the Creatio Mobile setup](https://academy.creatio.com/documents?id=1920#title-773-6).

## How can I clear the mobile app cache? [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#title-771-3 "Direct link to How can I clear the mobile app cache?")

You can clear the mobile app cache in one of the following options:

- Log out of the application. In this case, the app cache will be cleaned automatically.
- Clean the cache of the mobile device.

Important

After cleaning the mobile application cache, all data modifications that were made offline and not synchronized with the main application will be deleted.

## How can I set up push notifications for mobile application users? [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#title-771-4 "Direct link to How can I set up push notifications for mobile application users?")

Mobile application users will receive push notifications and reminders that contain valuable updates, such as meeting reminders or feed notifications. Customize them using the Business Process Designer. Learn more: [Set up push notifications for mobile application users](https://academy.creatio.com/documents?id=2360) guide.

## How does the app open Creatio links? [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#title-771-5 "Direct link to How does the app open Creatio links?")

Creatio links have the following format: `https://mysite.creatio.com/Navigation/Navigation.aspx?schemaName=Contact&recordId=bc260218-b43b-493a-9da6-1f2f8e8e28f2`

where:

- **mysite** is the website name.
- **Contact** is the schema name.
- **bc260218-b43b-493a-9da6-1f2f8e8e28f2** is the ID of the schema record.

Creatio Mobile deals with links as follows:

- If the website name is the same as the website into which you are logged in the app, the link is opened in the app. If the website name is different, the link is opened in the default browser.
- If the schema name is invalid, the app opens the link and sends you to the start page.
- If the record ID is invalid, the app opens the link and displays a message that a record does not exist.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq\#see-also "Direct link to See also")

[Get started with the mobile app setup](https://academy.creatio.com/documents?id=1945)

[Get started with the mobile app setup](https://academy.creatio.com/documents?id=1945)

[Get started with the mobile app UI](https://academy.creatio.com/documents?id=1955)

[Work with the mobile app calendar](https://academy.creatio.com/documents?id=2300)

[Work with service cases in the mobile app](https://academy.creatio.com/documents?id=2315)

[Work with dashboards in the mobile app](https://academy.creatio.com/documents?id=2314)

- [Why will the mobile app not sync in online mode (Error "Item% 24 batch not found)?](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#title-771-1)
- [How to resolve the synchronization conflict in the offline mode?](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#title-771-2)
- [How can I clear the mobile app cache?](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#title-771-3)
- [How can I set up push notifications for mobile application users?](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#title-771-4)
- [How does the app open Creatio links?](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#title-771-5)
- [See also](https://academy.creatio.com/docs/8.x/mobile/basics/mobile-application-faq#see-also)