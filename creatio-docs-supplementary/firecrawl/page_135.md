<!-- Source: page_135 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 12/07/2021

At Creatio, we are committed to delivering increasingly more advanced low-code/no-code capabilities that let you create workflows, applications, and vertical solutions easier than ever before. Here are the **new features** included in Creatio version 7.18.5.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/node/143/).

## Low-code platform [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-1 "Direct link to Low-code platform")

### Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-5 "Direct link to Business processes")

#### Duplicate search [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-6 "Direct link to Duplicate search")

- New **Find and merge duplicates** element was added. The element searches for and merges the duplicates of the selected record automatically according to specified rules. The element requires global search and bulk duplicate search to be set up.

Set up the Find and merge duplicates element

![Set up the Find and merge duplicates element](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_5/scr_element_find_duplicates.png)

### Base interface and system capabilities [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-7 "Direct link to Base interface and system capabilities")

#### Lead duplicate search [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-8 "Direct link to Lead duplicate search")

- The lead page now includes the widget that displays the number of possible lead duplicates. The widget helps you to acquire information about similar needs of your customers quickly. Use this data to develop further lead nurturing tactics and disqualify duplicate leads in a timely manner. Creatio displays the widget if the **Lead** section has active duplicate search rules configured and global duplicate search is set up. At the same time, Creatio hides the **Similar leads** detail from the page. The functionality is available for beta testing in Creatio version 7.18.5. Contact Creatio support to receive early access to new duplicate search options. We appreciate your feedback. The new feature will be available publicly in the upcoming Creatio releases.

### Performance [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-11 "Direct link to Performance")

#### Background execution of operations [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-12 "Direct link to Background execution of operations")

- The task distribution among handlers was optimized. This enables Creatio to execute background operations faster.

### Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-7 "Direct link to Development tools")

#### Assembly package [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-9 "Direct link to Assembly package")

- The compilation error of assembly packages whose schemas contain JavaScript was fixed.

#### Schema Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-10 "Direct link to Schema Designer")

- The development of objects and replacing objects was streamlined. You can now publish objects without compiling the configuration. The object compilation on publishing might be required if the embedded process of the object was saved while editing but not published in the Process Designer. To compile the object on publishing, use the new **Publish and compile** command of the **Publish** button menu.

Publish a new object

![Publish a new object](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_5/scr_publish_without_compilation.png)

## CRM solutions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-11 "Direct link to CRM solutions")

### Marketing tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-22 "Direct link to Marketing tools")

#### Website event tracking [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-23 "Direct link to Website event tracking")

- [Website event tracking](https://academy.creatio.com/documents?id=1596) functionality will be retired in the next release. As an alternative, you can use Matomo analytics service. Import Matomo data to Creatio via a Marketplace application: [Matomo connector for Creatio](https://marketplace.creatio.com/app/matomo-connector-creatio).

Learn more about viewing Matomo data in Creatio in a separate article: [Review online behavior of a contact](https://academy.creatio.com/documents?id=2372).

The retirement will not affect other Creatio functionality.


#### Lead generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-13 "Direct link to Lead generation")

- An option to register leads from LinkedIn lead generation forms automatically was added. To do this, connect your LinkedIn ad account to Creatio and map the form fields to the lead page fields.

Register LinkedIn leads in Creatio

![Register LinkedIn leads in Creatio](https://academy.creatio.com/docs/sites/en/files/images/Release_notes/release_notes_7_18_5/gif_linkedin_leadgen.gif)

#### Email delivery analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-14 "Direct link to Email delivery analytics")

- Creatio now processes situations when the Mail Privacy Protection (MPP) system of Apple Mail opens an email. In these cases, Creatio receives the "Open (machine)" response, which is not taken into account in the aggregate email opening stats.

### Mobile app [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-15 "Direct link to Mobile app")

#### Mobile portal [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-16 "Direct link to Mobile portal")

- Mobile app now supports Portal Creatio functionality. Through the app, portal users can:
  - create cases
  - attach photos and other files from the device memory or cloud storage to cases
  - chat with support agents
  - receive push notifications about new messages and case status updates
- The administrator of the main app can manage the view of the list and case pages for mobile portal users.


#### Support for new operating systems [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-2175-17 "Direct link to Support for new operating systems")

- Support for iOS 15 and Android 12 was added.

## New functionality beta testing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes\#title-3653-28 "Direct link to New functionality beta testing")

New app customization tools are available in version 7.18.5 for beta testing. Learn more: [Description of beta functionality in Creatio 7.18.5](https://academy.creatio.com/node/2177).

- [Low-code platform](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-1)
  - [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-5)
  - [Base interface and system capabilities](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-7)
  - [Performance](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-11)
  - [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-7)
- [CRM solutions](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-11)
  - [Marketing tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-22)
  - [Mobile app](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-2175-15)
- [New functionality beta testing](https://academy.creatio.com/docs/8.x/resources/release-notes/7185-release-notes#title-3653-28)