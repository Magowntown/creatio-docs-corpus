<!-- Source: page_104 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 06/29/2021

We at Creatio are constantly working to deliver advanced low-code/no-code capabilities to accelerate your process automation and application development for customer-facing, IT, and back-office teams. Here are the **new features** included in Creatio version 7.18.1.

The update guide for on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## Low-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-1 "Direct link to Low-code platform")

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-111 "Direct link to Business processes")

#### Assign process tasks to roles [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-50 "Direct link to Assign process tasks to roles")

- An option to assign process tasks to roles in a couple of clicks with custom no-code tools was added. Any user who is a member of a given role can complete a task assigned to that role, allowing you to optimize the workflow and distribute the tasks more efficiently.

- You can manually assign all interactive business process elements, such as a task or a user question, to other users or roles. Complete the action in the task page or the communication panel.
The business process task owner list

![The business process task owner list](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/reassign_task.png)

- It is now possible to view the list of available group tasks and start working on them in the communication panel. Use the new quick actions menu for group tasks to start working on the task, assign it to yourself to finish it later, or assign it to another employee directly from the communication panel.
Group task actions on the communication panel

![Group task actions on the communication panel](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/working_with_group_tasks.png)

- If you have a process task or another interactive process element open and a different user finishes it, Creatio will send you a corresponding notification. Read more: [Check notifications and process tasks](https://academy.creatio.com/node/2099/#title-2099-13).


#### Pre-configured pages [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-36 "Direct link to Pre-configured pages")

- Users can now see the changes made in the pre-configured page designer without reloading the Creatio web app.

#### Work with data collections [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-37 "Direct link to Work with data collections")

- **Pre-configured page** and **User task** process elements now support record collections. Use record collections to pass the records sets in the parameters of these elements. For example, populate the pre-configured page's details with data. Add and set up a "Serializable list of composite values" parameter for the desired element in the **Configuration** section to enable this feature in the Process designer.

Record collections in the Pre-configured page business process element

![Record collections in the Pre-configured page business process element](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/data_collection_parameters.png)

### User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-2 "Direct link to User customization tools")

#### Refresh the homepage data [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-35 "Direct link to Refresh the homepage data")

- You no longer need to refresh the browser tab to update the information on the homepage. Simply click the page header instead.
- Users can now see the changes made in the homepage editor without reloading the Creatio web app. Simply reopen the homepage by any other means to see the changes.

#### Homepage setup [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-39 "Direct link to Homepage setup")

- It is now possible to edit the automatically generated element code when creating a homepage, making it easier to identify the page in the list of schemas. You can edit the code of the existing pages as long as the homepage does not replace another page.
Editing the unique homepage code

![Editing the unique homepage code](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/gif_change_homepage_code.gif)

- It is possible to delete a homepage element by pressing Delete.


#### Homepages on mobile devices [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-32 "Direct link to Homepages on mobile devices")

- The homepage layout on mobile devices was improved. The elements are grouped in a single column, making them easier to view.

### Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-3 "Direct link to Base interface and system capabilities")

#### Chats [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-18 "Direct link to Chats")

- An option to transfer chats to another department was added. After the chat is transferred, Creatio will assign it to an agent of the selected queue according to the routing rules.
The list of chat queues

![The list of chat queues](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/list_of_queues.png)

- The processing of messages sent in Facebook Messenger's guest mode was improved. If a user communicates as a guest and closes the page, an agent will receive a notification when sending a reply.

- Push notifications were added for new chat messages. This way, agents will be aware of new messages even if the chat's browser tab is inactive. The browser must allow the Creatio website to send notifications for this feature to work correctly.


### Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-7 "Direct link to Development tools")

#### OData [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-46 "Direct link to OData")

- The retrieval of paged data via "$skip" and "$top" parameters was sped up for OData 4 protocol, optimizing the CPU resource usage. Oracle databases have to be version 12 or later to take advantage of this improvement.

## CRM solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-8 "Direct link to CRM solutions")

### Marketing tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-9 "Direct link to Marketing tools")

#### Custom throttling limits [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-47 "Direct link to Custom throttling limits")

- It is now possible to specify the daily limit and throttling rules for emails to be sent. Use the new "Manual limit" throttling mode in the [throttling](https://academy.creatio.com/node/2016/) settings to customize these values. The parameters specified for this mode will remain the same throughout the email sending process. Use this feature to balance the load on the site and optimize the workflow of employees processing the email feedback.

The custom limit setup

![The custom limit setup](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/user_limits.png)

### Sales tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-14 "Direct link to Sales tools")

#### Sales Playbook [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-24 "Direct link to Sales Playbook")

- Sales Playbook hints were implemented. The hints let users access the up-to-date information from the knowledge base when working with a lead, opportunity, order, or any dynamic case object. For example, navigate to the "Presentation" step of the corporate sales process to learn more about the best practices and recommendations for creating presentations.

Set up hints in the **Playbook** tab of the **Knowledge base** section articles.


Accessing a Playbook hint in the Opportunities section case

![Accessing a Playbook hint in the Opportunities section case](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/gif_sales_playbook.gif)

### Banks and finances [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-52 "Direct link to Banks and finances")

#### Product selection [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-51 "Direct link to Product selection")

- It is now possible to work with product selection as part of a business process. To achieve this, add a "Product selection" pre-configured page to a business process and set up its parameters. For example, have a consultant see next best offers or the up-to-date product catalog when they reach this part of the flow.

The Product selection pre-configured page

![The Product selection pre-configured page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_1/product_selection_page.png)

### Service tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-11 "Direct link to Service tools")

#### Support service mailbox language [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-28 "Direct link to Support service mailbox language")

- An option to use the default language for specific support mailboxes was added for cases registered via an employee's email. This way, the mailboxes will always use the selected language regardless of any other rules.

### Portal [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-12 "Direct link to Portal")

#### Portal organization permissions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes\#title-3432-30 "Direct link to Portal organization permissions")

- Creatio now grants case permissions to the portal organization, allowing the organization's users to track the status of incidents created by their colleagues.

Control this behavior with the "Grant case permissions for portal user organization" ("GrantCasePermissionsForPortalOrganization" code) system setting, which is enabled by default.


- [Low-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-1)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-111)
  - [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-2)
  - [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-3)
  - [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-7)
- [CRM solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-8)
  - [Marketing tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-9)
  - [Sales tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-14)
  - [Banks and finances](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-52)
  - [Service tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-11)
  - [Portal](https://academy.creatio.com/docs/8.x/resources/release-notes/7181-release-notes#title-3432-12)