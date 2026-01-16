<!-- Source: page_153 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 05/25/2021

We at Creatio are constantly working to deliver advanced low-code/no-code capabilities to accelerate your process automation and application development for customer-facing, IT, and back-office teams. Here are the **new features** included in Creatio version 7.18.0.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

[![tech_hour](https://academy.creatio.com/sites/en/files/images/Release_notes/tech-hour-rn_bg_small.jpg)](https://youtu.be/qXMjf5mbiiE)

## Low-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-1 "Direct link to Low-code platform")

### User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-15 "Direct link to User customization tools")

#### Homepages [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-48 "Direct link to Homepages")

- Introducing **homepages**, a brand new feature designed to aggregate dashboard information for workplace users. The homepage can be found at the top of the workplace section list in the side panel.

You can open the homepage from the side panel. The homepage will also replace the main Creatio page if you have not customized the main page previously.

All preset workplaces have homepages: "Sales," "Marketing," "Service," etc.

Edit the homepage content with no-code tools that offer powerful customization opportunities.
Opening the homepage editor

![Opening the homepage editor](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/open_page_wizard.gif)


You can also create new homepages when setting up workplaces.
Creating a workplace's homepage

![Creating a workplace's homepage](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/open_page_wizard_for_new_wp.gif)


#### The homepage designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-48 "Direct link to The homepage designer")

- Added a new no-code homepage customization tool. The homepage designer has an intuitive UI and offers powerful customization opportunities. For easier setup, the elements in the homepage designer replicate that of the homepage.
Setting up the homepage

![Setting up the homepage](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/page_wizard.gif)

- It is now possible to fine-tune the homepage color scheme. You can select from 16 available colors for all dashboards. You can customize the header color and the series color independently in charts with several series. Hovering over the chart will show the tooltips for all series at once. This allows you to compare the series visually.
Setting up a chart with several series

![Setting up a chart with several series](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/Open_page_wizard_3.gif)

- It is now possible to customize chart header styles.
Setting up the chart header styles

![Setting up the chart header styles](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/set_up_dashboard_style.gif)

- Added various style options for "Metric" dashboard.
The fill options for Metric dashboard

![The fill options for Metric dashboard](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/dashboard_styles.png)

- Added a new "Doughnut" chart. Hovering over any sector of the chart will show the tooltip in the center, allowing you to direct more attention to chart values.
A doughnut chart

![A doughnut chart](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/dashboard_donut.png)


### Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-10 "Direct link to Base interface and system capabilities")

#### Batch data prediction [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-49 "Direct link to Batch data prediction")

- It is now possible to use batch prediction to streamline data classification. This feature lets you predict lookup fields in a record collection. For instance, you can determine the opportunity category based on existing patterns. Set up batch prediction in the business process element or on the machine learning model page.

Setting up data prediction for a record collection

![Setting up data prediction for a record collection](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/prediction_for_collection.png)

#### Training dataset review [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-50 "Direct link to Training dataset review")

- Creatio will now review training datasets automatically, streamlining the machine learning model setup. Now you can view detailed information about dataset composition issues and the ways to resolve them for various ML models before you start to train the model.

Results of the training dataset review

![Results of the training dataset review](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/test_model_before_training.png)

#### Prediction data transparency [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-51 "Direct link to Prediction data transparency")

- You can now view the top 20 words and phrases that affect prediction results when setting up ML models that use text data. This information will help you understand the models' prediction principles and results.

![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/top_words_ML_full.png)

### Integrations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-5 "Direct link to Integrations")

#### Web services [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-6 "Direct link to Web services")

- It is now possible to examine the response from the web service, test its functionality, and debug it during setup. You can send a request and receive a response directly from the web service setup UI without the need to configure and run a business process.

Testing a web service

![Testing a web service](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/web_service_test.gif)

### Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-3 "Direct link to Administration")

#### Authentication [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-31 "Direct link to Authentication")

- Streamlined Creatio user authentication. It is now possible to log in to Creatio with both a username and an email. To set up email login, fill out the **Email** field on the user pages. You need system administrator permissions to edit this field.

#### Licensing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-31 "Direct link to Licensing")

- You need to order licenses before updating Creatio on-site to version 7.18.0. You can order licenses in the license manager.

The issued licenses are valid for the version you specify during the order and earlier, streamlining the update process.


#### Logging [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-4 "Direct link to Logging")

- It is now possible to add multiple columns simultaneously to the change log. This allows for faster data logging setup.

Selecting multiple columns for logging

![Selecting multiple columns for logging](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/change_log_multiply_select.gif)

#### Redis Cluster support [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-21 "Direct link to Redis Cluster support")

- Creatio now supports Redis Cluster. This is a more advanced fault tolerant technology for Redis repositories. It lets you minimize Creatio downtime in case of a Redis subsystem emergency, and it ensures maximum performance. The deprecated Redis Sentinel fault tolerant configuration will be retired in version 7.18.3. Install and set up Redis Cluster before updating to version 7.18.3. Read more: [Redis Cluster](https://academy.creatio.com/node/2010/).

### Security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-14 "Direct link to Security")

#### Password security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-36 "Direct link to Password security")

- Implemented secure password storage for iOS and Android devices to ensure the highest level of security. The passwords are stored in a secure storage not only when using Single Sign-On (SSO), but also when using the basic authentication.

### Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-7 "Direct link to Development tools")

#### Work with data [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-8 "Direct link to Work with data")

- Improved the flow for binding data to packages. When you select the bound object, Creatio will now add all available object fields that are compatible with the package, except fields with "Never" use mode.

## CRM solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-9 "Direct link to CRM solutions")

### Marketing tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-22 "Direct link to Marketing tools")

#### Email delivery schedule [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-47 "Direct link to Email delivery schedule")

- It is now possible to send out emails on a set schedule by configuring the settings in the email parameters. You can select:


  - Delivery mode: every day or specific days of the week.
  - Email delivery time: for example, from 9:00 AM to 6:00 PM.
  - Time zone for email delivery time.

Read more: [Set up the email delivery schedule](https://academy.creatio.com/node/2014/).

Setting up the delivery schedule

![Setting up the delivery schedule](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/email_additional_settings_delivery_time.png)

#### Email sending priority [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-51 "Direct link to Email sending priority")

- Added an option to specify the email sending priority. For instance, you can configure the email priority so that registration confirmation emails are sent earlier than news digests.

Read more: [Set up the email priority](https://academy.creatio.com/node/2017/).


Setting up the sending priority

![Setting up the sending priority](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/email_additional_settings_priority.png)

#### Email throttling [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-52 "Direct link to Email throttling")

- You can now throttle emails to send them gradually. This lets you warm up the cold audience and improve the sender domain reputation. Throttling divides a large list of recipients into several parts. Creatio will forward the parts to the email provider one by one during a specified time period. This approach will help you to improve the email delivery rate and avoid the diversion of emails into the "Spam" folder or bounces.

You can establish several outgoing queues to segment different cold contact lists and warm them up individually.

Read more: [Set up the email throttling queue](https://academy.creatio.com/node/2016/).


Setting up the throttling

![Setting up the throttling](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/email_additional_settings_throttling.png)

#### Email expiration date [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-54 "Direct link to Email expiration date")

- Added an option to specify the date and time when Creatio will stop sending the email regardless of whether it processed all recipients. This is important when sending time-sensitive content, such as special offers or event invites.

Creatio stops processing recipients after the expiration date. However, the email provider will send the emails to the recipients it has already received from Creatio.

Read more: [Set up the email expiration date](https://academy.creatio.com/node/2015/).


Setting up the expiration date

![Setting up the expiration date](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/email_additional_settings_expire.png)

#### Email cancelling [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-55 "Direct link to Email cancelling")

- It is now possible to manually cancel an active email regardless of its status. Click **Stop sending** to cancel the email. Once you select this option, Creatio stops processing recipients. However, the email provider will send the emails to recipients it has already received from Creatio. If you click **Stop sending** in an email with "Preparing to send" status, you will be able to edit the email and restart it. It is not possible to restart emails with other statuses.

#### Landing page element [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-59 "Direct link to Landing page element")

- Added new **Landing page**![](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/element_landing_mini.png) campaign element. It lets you integrate landing pages with campaigns at any intermediate part of the flow. The element can filter contacts based on whether they submitted the web form on the landing page, the response type, and object parameters.

The Landing page element in a campaign flow

![The Landing page element in a campaign flow](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/element_landing.png)

#### Campaign flow analytics update [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-57 "Direct link to Campaign flow analytics update")

- Improved the analytics UI on the campaign page. It is now easier to compare the numbers of campaign participants during each step.
- Added checkboxes that toggle participant counters.

Campaign participant counters

![Campaign participant counters](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/new_counters.png)

#### Save the element settings [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-58 "Direct link to Save the element settings")

- It is now possible to save the campaign element settings and use them in any campaign when setting up similar elements in the future.

Saving the element settings

![Saving the element settings](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/save_data.png)

### Finance and banking [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-16 "Direct link to Finance and banking")

#### Product selection [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-35 "Direct link to Product selection")

- Added an option to search through the product catalog by set conditions to quickly find the most suitable offer for the customer. For salespersons' convenience, it is possible to quickly review the product description, general information, advantages of the product, as well as issue a new order. Creatio can pass the product recommendation data in the incoming process parameters, allowing you to set up custom product sale and order logic.

Selecting a product by set conditions

![Selecting a product by set conditions](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/product_selection.png)

#### Next best offers [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-63 "Direct link to Next best offers")

- Creatio now uses predictive data analysis to recommend bank products and services to clients. Next best offers let you develop a personalized approach, better fulfill the needs of existing clients, and easily attract new ones.

Next best offers on a contact page

![Next best offers on a contact page](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/NBO.png)

### Service tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-64 "Direct link to Service tools")

#### WhatsApp chat channel [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-11 "Direct link to WhatsApp chat channel")

- Added WhatsApp messenger customer communication channel. Creatio uses Twilio, an official Facebook partner, for integration.

You need to register and verify a Twilio account to add a WhatsApp channel. Read more about the registration in [Twilio documentation](https://www.twilio.com/docs/whatsapp/tutorial/connect-number-business-profile#overview-of-the-registration-process).

Agents can process all messages sent through WhatsApp in the communications panel.

This feature is only available for beta testing in Creatio version 7.18.0. It is not possible to send files through chat. We appreciate your feedback!


### Portal [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-60 "Direct link to Portal")

- It is now possible to transfer contacts between the portal organizations. You can add an existing contact to a new organization when they change their job. Creatio will add a new user with up-to-date permissions and deactivate the previous user. This lets you gather complete data about a contact's career and lower the risk of duplicate users.

### Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-13 "Direct link to Mobile application")

#### Approvals in the mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes\#title-2013-27 "Direct link to Approvals in the mobile app")

- It is now possible to tag any employee in the approval feed. For users' convenience, the app displays the previous approval participants first when selecting contacts.
Tagging contacts in the approval feed

![Tagging contacts in the approval feed](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_0/visa_mobile.png)

- The mobile app now has a history of approvals that have been processed in desktop Creatio.


- [Low-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-1)
  - [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-15)
  - [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-10)
  - [Integrations](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-5)
  - [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-3)
  - [Security](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-14)
  - [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-7)
- [CRM solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-9)
  - [Marketing tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-22)
  - [Finance and banking](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-16)
  - [Service tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-64)
  - [Portal](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-60)
  - [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7180-release-notes#title-2013-13)