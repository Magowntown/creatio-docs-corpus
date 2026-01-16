<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

**Creatio Marketplace Console** is a tool that enables partners to manage their own Marketplace listings. A **Marketplace listing** comprises the Marketplace app and resources to publish on Creatio Marketplace. A listing includes information visible to users on Creatio Marketplace. A listing can have multiple revisions. Use revisions to add or modify listing resources.

Creatio Marketplace Console lets you accelerate the Marketplace app development process and streamline the Marketplace listing support on Creatio Marketplace. Creatio Marketplace Console is a part of the [Success Portal](https://success.creatio.com/) and includes **Marketplace listings**, **Cases**, **Public profile** sections.

Creatio Marketplace Console lets you execute the following actions:

- Create and manage the listing revisions.
- Send a listing revision to Creatio Marketplace support for review.
- Discuss your listing revision with Creatio Marketplace support and track the revision life cycle.
- Publish a listing on Creatio Marketplace. Creatio Marketplace support must complete this action on their end.
- Update a listing on Creatio Marketplace.
- Retrieve a summary of all published listings within 30 days or the entire publishing period.

## Life cycle of a Marketplace listing [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2751-5 "Direct link to Life cycle of a Marketplace listing")

The life cycle of a listing is represented by the following statuses.

| Status | Status description |
| --- | --- |
| Idea | Initial listing status. The Marketplace listing is in development and not available to the Creatio Marketplace users. |
| Planned | An innovative app concept that the users need. The planned listing does not have a developer and scheduled release date. Creatio displays planned listings on the [Application map](https://marketplace.creatio.com/catalog?f%5B0%5D=upcoming:1&f%5B1%5D=upcoming:2) with the `Planned` badge. Learn more: [Coming soon Marketplace app](https://academy.creatio.com/documents?id=15026). |
| Coming soon | A listing with an app that is being developed and has a scheduled release date. These listings are displayed on the [Application map](https://marketplace.creatio.com/catalog?f%5B0%5D=upcoming:1&f%5B1%5D=upcoming:2) with the `Coming soon` badge. Learn more: [Coming soon Marketplace app](https://academy.creatio.com/documents?id=15026). |
| Published | A listing that is reviewed, published, and available to Creatio Marketplace users. These listings are displayed on the [Creatio Marketplace](https://marketplace.creatio.com/catalog) with different badges. |
| Unpublished | A listing that is removed from publication and not available to Creatio Marketplace users. |

The listing status is changed by Creatio Marketplace support and displayed in the **Status** column of the **Marketplace listings** section list.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_MarketplaceListingsSection.png)

When you create a new listing, a new listing revision is created automatically. Track the life cycle of a revision using the following statuses.

| Status | Status description |
| --- | --- |
| Draft | Initial status of the revision. New data about the Marketplace listing is added and not available to Creatio Marketplace users. The status is set automatically. |
| Review | The developer sent the revision for review. Creatio Marketplace support is reviewing the revision. One of the review process stages is ensuring the loaded packages that contain the Marketplace app functionality are compatible with base Creatio packages. As such, implement and test the claimed compatibility of the Marketplace app in accordance with the requirements. Learn more: [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4). The status is set by a Marketplace developer. |
| Updates Required | The revision that was sent for review requires updating because it does not meet the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008), [Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003). The status is set by Creatio Marketplace support. |
| Approved | The revision is reviewed, published, and available to Creatio Marketplace users. The status is set by Creatio Marketplace support. |
| Archived | A revision that is removed from publication and not available to Creatio Marketplace users. The status is set by Creatio Marketplace support after a new listing revision is published. You can track listing changes using the revision history. |

The revision status is displayed on the **Revisions** tab of a listing page.

## Manage the Marketplace listing [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2751-4 "Direct link to Manage the Marketplace listing")

Marketplace listing management includes the following steps:

1. Make sure the listing meets the requirements. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-10)
2. Register the listing on Creatio Marketplace Console. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-1)
3. Send the listing revision for review. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-3)
4. Update the listing. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-9)

### 1\. Make sure the listing meets the requirements [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-10 "Direct link to 1. Make sure the listing meets the requirements")

Make sure the listing meets the [Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003), [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008).

### 2\. Register the listing on Creatio Marketplace Console [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-1 "Direct link to 2. Register the listing on Creatio Marketplace Console")

Creatio lets you register the listing on any app development step. Learn more: [Steps to develop a Marketplace app](https://academy.creatio.com/documents?id=15952).

To register the listing:

1. **Log in to the** [Success Portal](https://success.creatio.com/) **website**.
2. **Open the Marketplace listings section**.
3. **Click New listing**.
4. **Fill out the listing properties**. Instructions: [Revision page](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2751-6).
5. **Save the changes** without sending the revision to Creatio Marketplace support for review.

**As a result**, the listing status will be set to `Idea`. Creatio Marketplace Console will create a new revision automatically. The status of the revision will be set to `Draft`.

### 3\. Send the listing revision for review [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-3 "Direct link to 3. Send the listing revision for review")

1. **Open the Marketplace listings section**.
2. **Open the listing page** to publish.
3. **Select the revision** whose status is `Draft` on the **Revisions** tab.
4. **Submit revision for review**. This changes the revision status from `Draft` to `Review`.
5. **Save the changes**.

note

You can only send a revision whose properties are filled out completely for review.

**As a result**, the revision will be sent to Creatio Marketplace support for review. A case will be created automatically in the **Cases** section. Creatio Marketplace support checks whether the revision meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008), [Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003). You will receive the comments in a separate case.

Creatio Marketplace takes the following actions after the listing **revision is reviewed** successfully:

- The revision status is changed from `Review` to `Approved` on the revision page.

- The listing status is changed from `Idea` to `Published`.

- The listing is published on Creatio Marketplace automatically.

- You are notified that revision was published on Creatio Marketplace via email.

- A list of licensed products for paid listing is displayed on the **Licensed products** tab. The licensed product name matches the official license name that is used in commercial proposals, client contracts, and other legal documents.

View the example of the **Licensed products** tab for the **Case Management** listing below.


![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_LicensedProductsTab.png)


If Creatio Marketplace support has feedback for your revision, you will receive the comments that contain detailed issue descriptions and recommendations. Creatio Marketplace Console displays the comments in a separate case. The revision status is changed from `Review` to `Updates Required`. Fix the mentioned issues and resend the revision for review.

### 4\. Update the listing [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-9 "Direct link to 4. Update the listing")

You can update a published listing. To do this:

1. **Open the Marketplace listings section**.
2. **Open the revision page**.
3. **Add a new or open an existing revision** whose status is `Draft`. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) on the **Revisions** tab.
4. **Modify the required properties** in the listing revision.
5. **Submit revision for review**. Instructions: [Send the listing revision for review](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-3).

If you want to **unpublish the listing**, take the following steps:

1. Notify Creatio Marketplace support via `marketplace@creatio.com`.
2. Wait until Creatio Marketplace support reviews the request and unpublishes the listing.

## Revision page [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2751-6 "Direct link to Revision page")

A listing includes information visible for users on Creatio Marketplace. Use the revision page to add or modify listing resources. A revision page contains the following elements.

### Overview tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-4 "Direct link to Overview tab")

The **Overview** tab contains the following properties.

| Property | Property description |
| --- | --- |
| Logo | The corporate logo of the Marketplace listing. Displayed on Creatio Marketplace after the listing is published. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) to upload the file. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-4). |
| Revision | The list of listing changes. The property is populated automatically and non-editable. |
| Name | The unique listing name that describes the app functionality. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-2). |
| Type | The Marketplace listing type. Learn more: [Marketplace listing types](https://academy.creatio.com/documents?id=15007).

Available values

|     |
| --- |
| AI Agent on Creatio platform |
| Application on Creatio platform |
| Component for Creatio platform |
| Integration via Creatio API |
| Product on Creatio platform | |
| Summary | Brief information about the Marketplace listing. Describe the primary functionality and the problems the app solves. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-3). |
| Screenshots and video | Media files that demonstrate the Marketplace app functionality and sell your app. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-8). |
| ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) | Upload the file. |
| Link to video | The link to the video that demonstrates key features, primary functionality, and the problems the Marketplace app solves. |
| Marketing materials (optional) | Files that contain marketing data about the Marketplace listing. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) to upload the file. |

View the example of the **Overview** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_overview_tab.png)

### Details tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-15957-1 "Direct link to Details tab")

The **Details** tab contains the following properties.

| Property | Property description |
| --- | --- |
| Description | Detailed Marketplace listing description. Use the template from the revision page to describe the benefits of the Marketplace app. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-6). |
| Key features | Detailed description of the listing key features. Indicate the essential features and benefits of the Marketplace app. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) to add the key feature. This opens the **Key feature** window. Key features will be displayed in the order of addition. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-15008-2). |
| ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) | Upload the file that demonstrates the key feature of the Marketplace app. |
| Title | The name of the key feature's purpose. |
| Description | The key feature's functionality and benefits. |

View the example of the **Details** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_details_tab.png)

### Pricing and support tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-5 "Direct link to Pricing and support tab")

The **Pricing and support** tab contains the following properties.

| Property | Property description |
| --- | --- |
| Payment model | The payment model of the Marketplace listing.

Available values

|     |     |
| --- | --- |
| Free | The listing is free |
| Paid | The listing requires payment | |
| Pricing | The pricing details of the Marketplace listing. Fill out the properties if you set the **Payment model** property to "Paid." Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) to fill out the pricing details.<br>If the app has optional items or features sold separately, such as add-ons or API limit increases, specify them as well. Make sure the property values meet the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-10). |
| Name | The name of the Marketplace listing pricing. |
| Pricing model | The pricing model of the Marketplace listing.

Available values

|     |     |
| --- | --- |
| / year | One-year server-based license without a user cap |
| user / year | One-year user-based license | |
| Price $ | The Marketplace listing price. Follow the selected pricing model in the **Pricing model** property. |
| Does this app require a subscription outside Creatio? | Specify whether Marketplace listing requires additional payments beyond [Creatio pricing](https://www.creatio.com/products/pricing).

Available values

|     |     |
| --- | --- |
| External subscription is included in pricing (ISV / Reselling) | Marketplace app connects to external app or service that developed by Creatio. Available for "Paid" value of the **Payment model** property. |
| External subscription must be purchased separately | Marketplace app connects to external app or service that requires a separate subscription. Specify the link to the corresponding price list or contact details to receive the price list in the **Link to external pricing** property. |
| No external subscription required | Marketplace app does not connect to external app or service that requires a separate subscription. | |
| Link to external pricing | The link to the corresponding price list or contact details to receive the price list. Fill out the property if you set the **Does this app require a subscription outside Creatio?** property to "External subscription must be purchased separately." |
| Pricing description (optional) | The developer comments on the pricing model of the Marketplace listing. You can add more licensing information. Explicitly state the requirement to purchase the following:<br>- Another Marketplace listing or multiple license types of the current Marketplace listing.<br>- External apps or services, for example, for connectors. Specify the link to the corresponding price list or contact details to receive the price list. Specify whether the external apps are sold separately or their price is included in the connector price.<br>Make sure the value meets the [Requirements for pricing of paid listings](https://academy.creatio.com/documents?id=15008&anchor=title-4007-12). |
| Support conditions | The tech support terms and conditions for Marketplace listing. Fill out the property if you set the **Payment model** property to "Free" or set the **Does this app require a subscription outside Creatio?** property to "External subscription is included in pricing (ISV / Reselling)" for "Paid" value of the **Payment model** property. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-7). |
| I understand the requirements and confirm that we will provide support in line with the [Marketplace Technical Support Policy](https://marketplace.creatio.com/sites/marketplace/files/2024-07/Creatio-Marketplace-Support-Policy-Effective-as-of-July-01-2024.pdf) | Select the checkbox to confirm that you will follow the current Creatio Marketplace Technical Support Policy, and to provide technical support in line with its requirements. Select the checkbox if you set the **Does this app require a subscription outside Creatio?** property to "External subscription must be purchased separately" or "No external subscription required." |
| Basic support package (required) | The checkbox is selected automatically and non-editable if you set the **Does this app require a subscription outside Creatio?** property to "External subscription must be purchased separately" or "No external subscription required." |
| Business support package (required) | The checkbox is selected automatically and non-editable if you set the **Does this app require a subscription outside Creatio?** property to "External subscription must be purchased separately" or "No external subscription required." |
| Premium support package (optional) | Select or clear the checkbox if you set the **Does this app require a subscription outside Creatio?** property to "External subscription must be purchased separately" or "No external subscription required." |
| Terms and conditions | List the responsibilities of users and the Marketplace app developer. This lets you control how the users use the Marketplace app. Terms and conditions also help to ensure your Marketplace app complies with international and national legislation requirements. Finalize the terms and conditions when you publish the Marketplace listing.<br>note<br>Terms and conditions that list developer responsibilities improve reputation when a potential user selects Marketplace apps. Such terms and conditions also imply the seriousness, scale, and responsibility of the Marketplace app developer. |
| Link to Terms & Conditions | The link to the terms and conditions that comply with the law and policies of your company. |
| Use default [Terms & Conditions](https://d3a7ykdi65m4cy.cloudfront.net/en/s3fs-public/static-site/partnership-documents/MP-Terms-and-Conditions-effective-as-of-September-01-2024.pdf) | Whether to use the standardized terms and conditions that Creatio Marketplace offers to streamline the procurement workflow. |

View the example of the **Pricing and support** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_pricing_and_support_tab.png)

### Installation and setup tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-6 "Direct link to Installation and setup tab")

The **Installation and setup** tab contains the following properties.

| Property | Property description |
| --- | --- |
| How to set up (optional) | A step-by-step guide on how to set up the Marketplace app from scratch. |
| Guides (optional) | The file that contains the setup guide and user guide. For example, step-by-step YouTube video that demonstrates how to install and use the Marketplace app effectively. Make sure the property value meets the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-15008-7). |
| ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) | Upload the file. |
| Link to guide | The link to the setup guide and user guide for the Marketplace app. |
| Title to link | The name of the setup guide for the Marketplace app. |

View the example of the **Installation and setup** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_installation_and_setup_tab.png)

### Compatibility tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-7 "Direct link to Compatibility tab")

The **Compatibility** tab contains the following properties.

| Property | Property description |
| --- | --- |
| Installation method | The installation method of the Marketplace app.

Available values

|     |     |
| --- | --- |
| Automatic installation | The app includes the package that implements the functionality and is available to install on the Creatio Marketplace. Available for "Application on Creatio platform, "Component for Creatio platform," "Product on Creatio platform" values of the **Type** property. |
| Manual installation | The app includes the package that implements the functionality and is not available to install on the Creatio Marketplace. The package and demo data package are delivered by the developer on request. |

Other properties available on the tab list depend on the delivery option. |
| Creatio version from | The earliest version of Creatio products from the **Creatio products** property with which the Marketplace app is compatible. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4). |
| Deployment | Available deployment options of the Marketplace app.

Available values

|     |     |
| --- | --- |
| Cloud | The app can be deployed on the cloud |
| On-site | The app can be deployed on the customer's local servers |
| Both options | The app can be deployed both on the cloud and on the customer's local servers | |
| .NET platforms | The framework with which the Marketplace app is compatible. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4).

Available values

|     |
| --- |
| .NET 6 (supported from 8.0.9) |
| .NET Core (deprecated from 8.0.9) |
| .NET Framework | |
| DBMS | The DBMS with which the Marketplace app is compatible. To specify the value:

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) on the **DBMS** property.
2. Select a DBMS in the **Database management system** property.
3. Save the changes.

You can select multiple values. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4).

Available values

|     |
| --- |
| Any supported DBMS |
| MS SQL |
| Oracle |
| PostgreSQL | |
| Creatio products | The base Creatio products with which the Marketplace app is compatible. To specify the value:<br>1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) on the **Creatio products** property.<br>2. Select a product in the **Creatio product** property.<br>3. Save the changes.<br>You can select multiple values. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4). |
| Compatibility notes (optional) | The additional compatibility requirements for the Marketplace app. Learn more: [Requirements for compatibility​](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4). |
| Translations | Available languages of the Marketplace app. To specify the value:<br>1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) on the **Translations** property.<br>2. Select a language in the **Translation** property.<br>3. Save the changes.<br>You can select multiple values. Make sure that your property value meets the [Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003&anchor=title-4007-12). |
| UI Frameworks | The UI Framework with which the Marketplace app is compatible. To specify the value:

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png) on the **UI Frameworks** property.
2. Select a UI Framework in the **UI Framework** property.
3. Save the changes.

You can select multiple values. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4).

Available values

|     |
| --- |
| Classic UI |
| Freedom UI | |

View the example of the **Compatibility** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_compatibility_tab.png)

### Release details tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#title-2399-8 "Direct link to Release details tab")

The **Release details** tab contains the following properties.

| Property | Property description |
| --- | --- |
| Application file | The \*.zip file that contains the Marketplace app functionality. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) to upload the file. Make sure the value meets the [Requirements for package](https://academy.creatio.com/documents?id=15003&anchor=title-3995-5). |
| Demo data file | The \*.zip file that contains demo data of the Marketplace app. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_upload.png) to upload the file. Make sure the sample records meet the [Requirements for demo records](https://academy.creatio.com/documents?id=15003&anchor=title-3995-6).<br>We recommend creating a demo version to showcase how the Marketplace app operates in Creatio. Learn more: [Demo version of the Marketplace app](https://academy.creatio.com/documents?id=15025). |
| What's new | Brief notes on the Marketplace app updates. If you modify the existing Marketplace app, specify the changes made and new capabilities introduced. Make sure the value meets the [Requirements for compatibility](https://academy.creatio.com/documents?id=15003&anchor=title-3995-4). |
| Licensed elements | The details of the Marketplace listing's licensed elements. Make sure the property values meet the [Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008&anchor=title-4007-9). |
| Pricing | The name of the Marketplace listing's pricing. Populated automatically based on the **Name** property of the **Pricing** expanded list from the **Pricing and support** tab. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_EditButton.png) to modify the name. |
| Licensed objects | Names of custom objects added to the Marketplace app. Licensed objects are key custom objects, for example, section. Learn more: [Marketplace app licensing](https://academy.creatio.com/documents?id=15008&anchor=title-2398-20). |
| Licensed operations | Names of operations added to the Marketplace app logic to review the availability of a license for specific functionality. For example, an additional action was added to a base Creatio section. Learn more: [Marketplace app licensing](https://academy.creatio.com/documents?id=15008&anchor=title-2398-20). |
| Comment for licensing | The developer comments on the licensing of the Marketplace listing. |
| Application properties | The property details of the Marketplace app. Properties are populated automatically based on the `app-descriptor.json` file and non-editable. |
| Name | The name of the Marketplace app. |
| Version | The version of the Marketplace app. |
| Code | The code of the Marketplace app. |
| Maintainer | The maintainer of the Marketplace app. |

View the example of the **Release details** tab for the **Case Management** listing below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.2/scr_release_details_tab.png)

* * *

## See also [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#see-also "Direct link to See also")

[Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008)

[Marketplace listing types](https://academy.creatio.com/documents?id=15008)

[Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003)

[Coming soon Marketplace app](https://academy.creatio.com/documents?id=15026)

[Steps to develop the Marketplace app](https://academy.creatio.com/documents?id=15952)

[Demo version of the Marketplace app](https://academy.creatio.com/documents?id=15025)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#e-learning-courses "Direct link to E-learning courses")

[Tech Hour - Build Your Marketplace App And Generate Income](https://www.youtube.com/watch?v=A_l4rRXCRsg)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings\#resources "Direct link to Resources")

[Official Creatio Marketplace website](https://marketplace.creatio.com/)

[Official Success Portal website](https://success.creatio.com/?_gl=1*1nb3es2*_gcl_au*MzUxNzE4MTM5LjE2OTE5ODUwNDY.)

[Creatio pricing](https://www.creatio.com/products/pricing)

[Marketplace updates](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/category/marketplace-updates)

- [Life cycle of a Marketplace listing](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2751-5)
- [Manage the Marketplace listing](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2751-4)
  - [1\. Make sure the listing meets the requirements](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-10)
  - [2\. Register the listing on Creatio Marketplace Console](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-1)
  - [3\. Send the listing revision for review](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-3)
  - [4\. Update the listing](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-9)
- [Revision page](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2751-6)
  - [Overview tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-4)
  - [Details tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-15957-1)
  - [Pricing and support tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-5)
  - [Installation and setup tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-6)
  - [Compatibility tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-7)
  - [Release details tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#title-2399-8)
- [See also](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#e-learning-courses)
- [Resources](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/marketplace-listings#resources)