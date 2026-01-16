<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/demo-version-of-the-app#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

A **demo version** of a Marketplace app is a set of packages that contain sample data and pre-configured functionality, such as test integration for the connector. A demo version enables the user to use the Marketplace app immediately after installation without additional setup. The demo version availability minimizes the time for preparing the presentation to the users and ensures a sufficient user satisfaction level. The demo version showcases how the Marketplace app operates in Creatio.

View the **types of sample data** that the Marketplace app must contain in the table below.

| Type of sample data | Description of sample data type |
| --- | --- |
| Softkey data | Samples of the base Creatio objects or sections that enable users to get to know the product quicker. Add softkey data to the package that contains the Marketplace app functionality. Softkey records must be in English and have the `(sample)` suffix at the end of the name. |
| Demo data (demo records) | Samples of Creatio object records stored in an individual package. This package must depend on the package that contains the Marketplace app functionality. |
| Showcase records | Section records that contain the maximum volume of demo data. The first three records in a section must be showcase records. |

Before you create a demo version, ensure that you follow the [Requirements for demo records](https://academy.creatio.com/documents?id=15003&anchor=title-3995-6).

General procedure to **create a demo version of the Marketplace app**:

01. **Deploy a build of the latest Creatio version** that contains demo data.

    You can order a build in the following ways:
    - using the [free trial page](https://www.creatio.com/trial/creatio)
    - by contacting the [Creatio support](mailto:support@creatio.com)
02. **Install a package that contains the Marketplace app functionality**. Instructions: [Install an app from a file](https://academy.creatio.com/documents?id=2377&anchor=title-2304-2) (user documentation).

03. **Create a dedicated app for demo data**. Instructions: [Create an app manually](https://academy.creatio.com/documents?id=2377&anchor=title-2232-6) (user documentation). Use the following package name template: `PackageName_Demo`. For example, `LabReports_Demo`. Store this app in an individual package.

04. **Add a package that contains the Marketplace app functionality** to the package dependencies.

05. **Add demo data to sections and lookups**.
    - If you use Creatio **trial**, add demo data on behalf of the Application Hub user that ordered the trial.

    - If you use Creatio **on-site** or in the **cloud**, add demo data on behalf of the `John Best` user (`76929f8c-7e15-4c64-bdb0-adc62d383727` contact ID). To do this:
      1. Add a filter `id = 76929f8c-7e15-4c64-bdb0-adc62d383727` to the **Contacts** section and fix the contact name.
      2. Add a Creatio user and connect them to the contact from the previous step. Instructions: [Add users](https://academy.creatio.com/documents?id=1441) (user documentation).
      3. Log in to Creatio as the created user and add demo data on their behalf.
06. **Bind Marketplace app demo data to Creatio demo data**. Binding is recommended for data integrity. Showcase records must be bound to the `Alexander Wilson` contact (`98dae6f4-70ae-4f4b-9db5-e4fcb659ef19` ID) and `Alpha Business` account (`98dae6f4-70ae-4f4b-9db5-e4fcb659ef19` ID) where appropriate.

07. **Configure the sorting of demo records** so that the showcase records are displayed at the top of the section list. If you have not selected or filled out the showcase records yet, configure the sorting before populating the showcase records.

08. **Bind the list settings, sorting, app demo data, and needed base demo data** to the package. Instructions: [Bind data to the package](https://academy.creatio.com/documents?id=15123).

09. **Download a demo version of the Marketplace app**. Instructions: [Download an app](https://academy.creatio.com/documents?id=2377&anchor=title-2232-8) (user documentation).

10. **Verify the completeness and correctness of bound data**.
    1. Order a Creatio trial using the [free trial page](https://www.creatio.com/trial/creatio).
    2. Install packages that contain the Marketplace app functionality. Instructions: [Install an app from a file](https://academy.creatio.com/documents?id=2377&anchor=title-2304-2) (user documentation).
    3. Install the package that contains the Marketplace app demo version. Instructions: [Install an app from a file](https://academy.creatio.com/documents?id=2377&anchor=title-2304-2) (user documentation).

**As a result**, the package that contains the Marketplace app demo data will be created. While managing the Marketplace listings, add the package that contains the Marketplace app demo data to the Creatio Marketplace Console ( **Packages and updates** tab → **Demo data file** property). Learn more: [Steps to publish the Marketplace listing using Creatio Marketplace Console](https://academy.creatio.com/documents?id=15957&anchor=title-2399-8).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/demo-version-of-the-app\#see-also "Direct link to See also")

[Requirements for Marketplace app](https://academy.creatio.com/documents?id=15003)

[Manage apps](https://academy.creatio.com/documents?id=2377) (user documentation)

[Add users](https://academy.creatio.com/documents?id=1441) (user documentation)

[Bind data to the package](https://academy.creatio.com/documents?id=15123)

[Steps to publish the Marketplace listing using Creatio Marketplace Console](https://academy.creatio.com/documents?id=15957)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/demo-version-of-the-app\#resources "Direct link to Resources")

[Creatio free trial page](https://www.creatio.com/trial/creatio)

[Marketplace updates](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/category/marketplace-updates)

- [See also](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/demo-version-of-the-app#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/demo-version-of-the-app#resources)