<!-- Source: page_85 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 10/12/2021

At Creatio, we are committed to delivering increasingly more advanced low-code/no-code capabilities that let you create workflows, applications, and vertical solutions easier than ever before. Here are the **new features** included in Creatio version 7.18.4.

The update guide for on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## Low-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-1 "Direct link to Low-code platform")

### Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-3 "Direct link to Base interface and system capabilities")

#### Duplicate search [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-9 "Direct link to Duplicate search")

- You can now learn about possible duplicates directly on the record page. Use the new widget to view and merge the duplicates of the corresponding record without running the duplicate search for the entire section. The widget is displayed in **Contacts** and **Accounts** sections if they have active duplicate search rules configured and global duplicate search is set up. The functionality is available for beta testing in Creatio version 7.18.4. Contact Creatio support to receive early access to the new duplicate search feature. We appreciate your feedback. The functionality will become available publicly in the upcoming Creatio releases.

Opening record duplicates from the contact page

![Opening record duplicates from the contact page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_4/gif_release_notes_open_duplicates.gif)

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-5 "Direct link to Integrations")

#### Exchange calendars synchronization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-9 "Direct link to Exchange calendars synchronization")

Important

This functionality is available for beta testing in Creatio version 7.18.4. Contact Creatio support to receive early access to the new calendar features. We appreciate your feedback.

The new feature will become available publicly in the upcoming Creatio releases.

The mechanism of Exchange calendars synchronization was updated as follows:

- Creatio uploads and displays meetings in real time without requiring you to reload the page.

- You can now send meeting invitations in Creatio from the activity page and view the responses on the **Participants** detail.


  - After sending the invitations, only the owner retains the permission to edit the meeting.
  - If the meeting details change (for example, time, place, description, participant list), Creatio sends out updated invitations automatically.
  - If the participants do not respond to invitations, you can resend the invitations from the meeting page in a single click.

Send invitations to meeting participants

![Send invitations to meeting participants](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_4/scr_release_notes_send_invitations.png)

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-6 "Direct link to Administration")

#### Permission setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-19 "Direct link to Permission setup")

- It is now possible to set up permissions to export section lists for specific objects. For example, you can permit the sales department employees to export invoices but not the customer base. You can grant export permissions to both individual users and user roles. Set up the permissions in the **Object permissions** section.

Set up permissions to export the section list

![Set up permissions to export the section list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_4/scr_release_notes_export_permissions.png)

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2070-10 "Direct link to Performance")

#### Acceleration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2070-11 "Direct link to Acceleration")

- Dynamic cases and tasks on the action panel now load 10 times faster.
- It is now possible to improve Creatio page loading time by forwarding dashboard and dynamic folder SELECT queries to a database replica. To enable this functionality, modify the Creatio web configuration and set up the database replica connection in the ConnectionStrings.config file. Currently you can forward queries to a single replica per master database.

### Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-5 "Direct link to Development tools")

#### Source code generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes\#title-2151-14 "Direct link to Source code generation")

- Creatio now generates source code for all schemas in the background. This operation does not affect the Creatio user workflows but precludes other types of source code generation, as well as compilation. If you attempt to run these actions, Creatio will warn you that the source code generation is in progress. We also do not recommend working on functionality that requires Creatio compilation (for example, installing applications and extensions, configuring the UI and business logic) while the operation is in progress. Once the process is completed, Creatio will display the corresponding notification in the communication panel.

The notification about the schemas' source code generation results

![The notification about the schemas' source code generation results](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_4/scr_release_notes_generate_source_code_notification.png)

- [Low-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2151-1)
  - [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2151-3)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2151-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2151-6)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2070-10)
  - [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7184-release-notes#title-2151-5)