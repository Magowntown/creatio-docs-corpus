<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

The **public profile** is a presentation of a Creatio partner that introduces them to users. [**Partner catalog**](https://www.creatio.com/partners/catalog) includes public profiles of all Creatio partners. If a partner develops Marketplace listings, the public profile is also displayed in the [**Developers** section](https://marketplace.creatio.com/catalog/services) of the Creatio Marketplace. The published profile can include the following data:

- General information to display in **Partner catalog** and **Developers** section.
- A list of developed Marketplace listings to display in the **Developers** section if a partner develops Marketplace listings.

## Life cycle of a public profile [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-1 "Direct link to Life cycle of a public profile")

The life cycle of a public profile is represented by the following statuses.

| Status | Status description |
| --- | --- |
| Draft | Initial status of the public profile. New data about the partner was added and is not available in **Partner catalog** and **Developers** section. The status is set automatically. |
| Review | The partner sent the public profile for review. Creatio Marketplace support is reviewing the profile. The status is set by an administrator of the partner organization or Marketplace developer. |
| Published | A public profile that is reviewed, published, and available in **Partner catalog** and **Developers** section. These public profiles are displayed in the **Partner catalog**. If a partner has Marketplace listings published, the public profile is also displayed in the **Developers** section of the Creatio Marketplace. |
| Updated | A public profile that is reviewed, published, and available in **Partner catalog** and **Developers** section. However, newly added data is not available in **Partner catalog** and **Developers** section. The status is set by an administrator of the partner organization or Marketplace developer. These public profiles are displayed in the **Partner catalog**. If a partner has Marketplace listings published, the public profile is also displayed in the **Developers** section of the Creatio Marketplace. |
| Unpublished | A public profile that is removed from publication and not available in **Partner catalog** and **Developers** section. |

## Manage the public profile [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-2 "Direct link to Manage the public profile")

Public profile management includes the following steps:

1. Register a public profile. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-3)
2. Send the public profile for review. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-4)
3. Update the public profile. [Read more >>>](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-5)

### 1\. Register a public profile [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-3 "Direct link to 1. Register a public profile")

note

By default, only administrators of the partner organization or Marketplace developers can access the **Public profile** section.

1. **Log in to the [Success Portal](https://success.creatio.com/) website**.

2. **Open the Public profile section**.

If you do not have a public profile, Creatio Marketplace Console opens a new public profile page. The status of the public profile will be set to `Draft`. Otherwise, Creatio Marketplace Console opens an existing public profile page.

3. **Fill out the profile properties**. Instructions: [Public profile page](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-6).

4. **Save the changes**.


### 2\. Send the public profile for review [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-4 "Direct link to 2. Send the public profile for review")

1. **Open the Public profile section**.
2. Click **Submit for review**.
3. **Save the changes**.

note

You can only send a public profile whose properties are filled out completely for review.

**As a result**, the public profile will be sent to Creatio Marketplace support for review. A case will be created automatically in the **Cases** section. You will receive the comments in a separate case. The public profile status is changed from `Draft` to `Review` on the public profile page. If you change the properties of the published profile, the public profile status is changed from `Published` to `Updated` on the public profile page.

Creatio Marketplace support takes the following actions after the **public profile is reviewed** successfully:

- The public profile status is changed from `Review` to `Published` on the public profile page.
- The public profile is automatically published in the **Partner catalog** and **Developers** section of the Creatio Marketplace.
- You are notified that the public profile was published via email.

If Creatio Marketplace support has feedback for your public profile, you will receive comments that contain detailed issue descriptions and recommendations. Creatio Marketplace Console displays the comments in a separate case. The public profile status is changed from `Review` to `Draft` on the public profile page. Fix the mentioned issues and resend the public profile for review.

### 3\. Update the public profile [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-5 "Direct link to 3. Update the public profile")

You can update a published profile. To do this:

1. **Open the Public profile section**.
2. **Modify the required properties** on the public profile page.
3. **Send the profile for review**. Instructions: [Send the public profile for review](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-4).

If you want to **unpublish the public profile**, take the following steps:

1. Notify Creatio Marketplace support via `marketplace@creatio.com`.
2. Wait until Creatio Marketplace support reviews the request, unpublishes the public profile, and changes the public profile status from `Published` to `Unpublished` on the public profile page.

## Public profile page [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-6 "Direct link to Public profile page")

A public profile includes information visible for users in the **Partner catalog** and **Developers** section of the Creatio Marketplace. Use the public profile page to add or modify general information about the partner.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/PublicProfile/8.2/scr_CreatioPublicProfile.png)

A public profile page contains the following elements.

### Overview area [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-7 "Direct link to Overview area")

The **Overview** area contains the following properties.

| Property | Property description |
| --- | --- |
| Logo\* | The corporate logo of the partner. Displayed in **Partner catalog** and **Developers** section after the public profile is published. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_UploadScreenshotButton.png) to upload the file. We recommend using \*.png, \*.gif, \*.jpg images that have white background and are 200px wide. |
| Name\* | The unique partner name. Displayed in **Partner catalog** and **Developers** section after the public profile is published. |

### General information tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-8 "Direct link to General information tab")

The **General information** tab contains the following properties.

| Property | Property description |
| --- | --- |
| About company\* | Brief information about mission, values, and core competencies of the partner. |
| Address | The physical or mailing address of your company. Demonstrates that the company is accessible for users interested in collaboration or contact. |
| Target regions | Continent, region, or country where the company works. Inform users about your business reach. To specify the value:<br>1. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_AddButton.png) on the **Target regions** property.<br>2. Select a continent, region, or country in the **Target region** property.<br>3. Save the changes.<br>You can select multiple values. |

### Development tab [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-9 "Direct link to Development tab")

The **Development** tab is available only for Marketplace app developers and contains the following properties.

| Property | Property type | Property description |
| --- | --- | --- |
| Developer prefix | Required for Marketplace developer | The unique ID of the Marketplace app developer. Marketplace app developer must use the prefix in the names of custom schemas, packages, objects, and columns in the objects that inherit from base objects. This enables users to identify the functionality created by the Marketplace app developer. Can contain Latin characters and digits. Must be from 3 to 15 characters long. To specify the value:<br>1. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_AddButton.png) on the **Developer prefix** property.<br>2. Enter the unique ID of the Marketplace app developer in the **Name** property.<br>3. Save the changes.<br>You can select multiple values. |
| Developer maintainer | Required for Marketplace developer | The maintainer of the Marketplace app functionality. Creatio uses the property value to identify a party that makes changes to the configuration. The maintainer name is assigned to each Marketplace app package separately. You can edit only Marketplace app packages that have been published by your company. The setting is used for developing user workspaces for third parties. To specify the value:<br>1. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_AddButton.png) on the **Developer maintainer** property.<br>2. Enter the maintainer name in the **Name** property.<br>3. Save the changes.<br>You can select multiple values. |

### Communication options area [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#title-15092-10 "Direct link to Communication options area")

The **Communication options** area contains the following properties.

| Property | Property description |
| --- | --- |
| Support contacts | Partner communication channels dedicated to supporting users of partner products or services. |
| Email\* | The support email of the partner. |
| Phone | The support phone of the partner. |
| Marketplace communications | Partner communication channel dedicated to receiving notifications from Creatio Marketplace and reviews from customers related to the partner products and services. |
| Commercial notifications\* | The partner email to receive notifications from Creatio Marketplace. |
| Customer review notifications\* | The partner email to receive customer reviews. |
| Business contacts | Partner communication channels dedicated to business inquiries, collaboration, or communication with the partner company. |
| Web | The website of the partner company. |
| Email\* | The email of the partner. |
| Phone 1<br>Phone 2 (additional)<br>Phone 3 (additional) | Main and additional phone numbers of the partner. |

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile\#resources "Direct link to Resources")

[Partner catalog](https://www.creatio.com/partners/catalog)

[Developers section](https://marketplace.creatio.com/catalog/services) (Creatio Marketplace)

[Official Success Portal website](https://success.creatio.com/?_gl=1*1nb3es2*_gcl_au*MzUxNzE4MTM5LjE2OTE5ODUwNDY.)

- [Life cycle of a public profile](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-1)
- [Manage the public profile](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-2)
  - [1\. Register a public profile](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-3)
  - [2\. Send the public profile for review](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-4)
  - [3\. Update the public profile](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-5)
- [Public profile page](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-6)
  - [Overview area](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-7)
  - [General information tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-8)
  - [Development tab](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-9)
  - [Communication options area](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#title-15092-10)
- [Resources](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-publication/marketplace-console/public-profile#resources)