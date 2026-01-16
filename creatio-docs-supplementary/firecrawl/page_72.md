<!-- Source: page_72 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 04/14/2021

We at Creatio are constantly working to deliver advanced capabilities to accelerate sales, service, and marketing processes. The following are the **new features** included in Creatio version 7.17.4.

The update guide for Creatio on-site is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Low-code Platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-50 "Direct link to Low-code Platform")

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-1 "Direct link to Business processes")

#### Navigation to the parent process [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-2 "Direct link to Navigation to the parent process")

- To improve process log UX, we have added an option to navigate to a parent process from a sub-process page.

Navigating to the parent process page

![Navigating to the parent process page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/subprocess_to_parent_process.gif)

#### Permissions to run a process [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-3 "Direct link to Permissions to run a process")

- Streamlined the UI. Users will only see manually launched business processes they are allowed to run.

If a user lacks permissions to run a process, Creatio will also hide the run button from the record and section pages.


#### Filters by time [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-4 "Direct link to Filters by time")

- To allow greater filter precision, we have added filters by time in addition to filters by date to business process elements. To activate these filters, set **Consider time in the filter** in the element's advanced setup area to "True."

Activating a filter by time

![Activating a filter by time](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/data_time_filter.gif)

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-5 "Direct link to Administration")

#### Licensing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-6 "Direct link to Licensing")

- You will need to order new licenses before updating Creatio on-site to version 7.18.0. You can order licenses in the license manager (available for version 7.17.3 and later).

The issued licenses are valid for the version you specify during the order and earlier, streamlining the update process.


### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-7 "Direct link to Integrations")

#### Web services [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-8 "Direct link to Web services")

- It is now possible to quickly set up SOAP services with a link to a WSDL file. Simply paste the link, and Creatio will apply the necessary settings automatically without requiring you to download the file and upload it to Creatio manually.
- It is now possible to pass a generated request body to REST and SOAP web services in JSON, XML, plain text formats as a process element parameter. Use this feature to set up web service calling parameters when passing the parameters separately is not possible, for instance, if the request body has to be generated automatically. You can set up the parameter mapping in the **Call web service** element setup area's advanced mode.

### Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-9 "Direct link to Development tools")

#### Work with data [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-10 "Direct link to Work with data")

- Retired the following deprecated Core API methods and properties from version 7.17.4:


  - QueryColumnExpression.SqlText;
  - Column.SqlText;
  - DBExecutor.ExecuteReader;
  - DBExecutor.ExecuteScalar;
  - DBExecutor.Execute;
  - DBExecutor.ExecuteBatches.

We recommend using DBMS-independent server classes Select, Delete, Insert, InsertSelect, Update, UpdateSelect instead. Learn more about the server classes in the [Data access through ORM](https://academy.creatio.com/node/1263//) article. Creatio will display a deprecated method warning when compiling a configuration. You will also need to re-generate the source code of Oracle-based products before the compilation.

## CRM Tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-60 "Direct link to CRM Tools")

### Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-11 "Direct link to Base interface and system capabilities")

#### Chats [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-12 "Direct link to Chats")

- Creatio now automatically saves chat message drafts. An agent can return to editing the message at any time after leaving the chat. The draft is displayed in the message field and is visible in the active chat list.
Chat message draft

![Chat message draft](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/chat_draft.png)

- For agent's convenience, chats with unread messages are marked with a blue dot: ![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/unread_chat.png).

- It is now possible to complete chats directly from the communication panel's active chat list. This streamlines the chat workflow.
Completing the chat from the communication panel

![Completing the chat from the communication panel](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/complete_chat.png)

- New chats are grouped into a separate list at the bottom of the communication panel, streamlining the agent workflow. Once an agent starts the conversation, the chat is moved to the active chat list. The counter at the top of the new chat list displays the number of unprocessed chats.
New chat list on the communication panel

![New chat list on the communication panel](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/chat_new_expand.gif)


### Sales tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-13 "Direct link to Sales tools")

#### Quick opportunity filter [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-14 "Direct link to Quick opportunity filter")

- Added a new closing date quick filter to the **Opportunities** section, streamlining the salespeople's workflow.

Filtering by date in the Opportunities section

![Filtering by date in the Opportunities section](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_17_4/opportunities_filter_date.png)

### Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-15 "Direct link to Mobile application")

#### Background synchronization on iOS [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-16 "Direct link to Background synchronization on iOS")

- Added background synchronization mechanism to iOS devices, improving the Creatio mobile app performance.

#### Approvals in the mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes\#title-1976-17 "Direct link to Approvals in the mobile app")

- It is now possible to copy any approval field, as well as approval heading and the approver's name, from the approval history.

- [Low-code Platform](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-50)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-1)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-5)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-7)
  - [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-9)
- [CRM Tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-60)
  - [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-11)
  - [Sales tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-13)
  - [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7174-release-notes#title-1976-15)