<!-- Source: page_114 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3

On this page

Level: beginner

Dashboards let you group analytics widgets easier as well as connect them to data sources and apply filter by page data (Fig. 1). Certain apps as well as the list page of the **Records and business processes** app template have dashboards included out of the box.

Fig. 1 Dashboard

![Fig. 1 Dashboard](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCodePlatform/set_up_dashboards/scr_dashboards.png)

note

In Creatio 8.3 Twin, list page template of the **Records and business processes** app template was enhanced with the **Dashboards** component. If you have an existing app that uses this template, update the page to include the component as well. Learn more: [Update list page template to include dashboards](https://academy.creatio.com/documents?id=2595).

## Dashboard types [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics\#title-15196-2 "Direct link to Dashboard types")

The ability to transfer dashboards between environments depends on dashboard type. The dashboard type is determined by how the dashboard is added. Creatio provides the following dashboard types:

- **Configuration dashboard**. A dashboard that is added by no-code creators at design-time using the **Dashboards** component in Freedom UI Designer. Learn more: [Set up dashboards in Freedom UI Designer](https://academy.creatio.com/documents?id=2577).
- **Environment dashboard**. A dashboard that is added by end users at runtime using UI in the **Dashboards** view of Creatio sections. Learn more: [View and manage dashboards](https://academy.creatio.com/documents?id=1405).

When you **add a configuration dashboard**, Creatio performs the following actions:

- Stores the configuration dashboard as a configuration schema (a "Client module" type schema of the Freedom UI page) in the app package automatically. Learn more: [Freedom UI page schema](https://academy.creatio.com/documents?id=15106&anchor=title-2123-10), [Configuration schemas](https://academy.creatio.com/documents?id=15347&anchor=title-15347-1) (developer documentation).
- Displays configuration schemas in the working area of the app package (the **Package settings** tab in the No-Code Designer), the main workspace of the app package (the **Packages** directory in the **Configuration** section), and the **Dashboards** parameter block in the Freedom UI Designer setup area.
- Displays the configuration dashboard in the dashboard list in the **Dashboards** view of Creatio sections if a dashboard is added to a section list page.
- Binds access rights for the configuration dashboard to the app package using a "Data" type schema whose **Object** property is set to "SysSchemaAdminUnitRight" and **Installation type** property is set to "Initial data installation." Learn more: ["Data" type schema](https://academy.creatio.com/documents?id=15123&anchor=initial-data-installation) (developer documentation).

When you **add an environment dashboard**, Creatio performs the following actions:

- Stores the environment dashboard as an environment schema and alerts end users who have access rights to the "Can manage configuration elements" (`CanManageSolution` code) system operation that the environment dashboard is available in the current environment only and cannot be transferred between environments. Those messages are enabled only for environments whose "Environment type" (`EnvironmentType` code) system setting includes a value other than "Production." This ensures that environment dashboard is implemented without package binding and is stored as an environment schema, reducing confusion for system administrators expecting package-level edits. Permissions to read, edit, and delete environment dashboards can be granted using access rights. Learn more: [Share records](https://academy.creatio.com/documents?id=1014).
- Stores environment schemas in the database independently of packages, so they are not included in the working area of the app package (the **Package settings** tab in the No-Code Designer) and and the **Dashboards** parameter block in the Freedom UI Designer setup area.
- Since version 8.3.1, Creatio includes environment schemas in the **Environment schemas** group in the **Configuration** section. Learn more: [Environment schemas](https://academy.creatio.com/documents?id=15347&anchor=title-15347-2) (developer documentation).
- Displays the environment dashboard in the dashboard list in the **Dashboards** view of Creatio sections.

## Transfer dashboard customizations [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics\#title-15196-3 "Direct link to Transfer dashboard customizations")

The ability to transfer dashboard customizations between environments also depends on dashboard type:

- Edit the configuration dashboard using Freedom UI Designer if you **need to transfer dashboard customizations between environments**. Creatio stores dashboard customizations in the **Replacing view model** schema type that can be transferred between environments as part of package.
- Edit the configuration or environment dashboard using UI if you **do not need to transfer dashboard customizations between environments**. Regardless of dashboard type, Creatio stores dashboard customizations as an environment schema. Since version 8.3.1, Creatio lets users who have access rights to the "Can manage configuration elements" (`CanManageSolution` code) system operation convert an environment schema to a configuration schema to transfer the dashboard between environments as part of a package. Learn more: [Move a schema to another package](https://academy.creatio.com/documents?ver=8.3&id=15339&anchor=title-15339-7) (developer documentation).

If a no-code creator adds a dashboard at runtime using UI in the **Dashboards** view of Creatio sections, i. e., an environment dashboard, the environment dashboard page includes the toolbar whose message alerts users who have access rights to the "Can manage configuration elements" (`CanManageSolution` code) system operation that the environment dashboard is available in current environment only and cannot be transferred between environments until you convert the environment schema to the configuration schema. Those messages are enabled only for environments whose "Environment type" (`EnvironmentType` code) system setting includes a value other than "Production." Creatio displays the same warning message for no-code creators who modify configuration dashboards using UI in the **Dashboards** view of Creatio sections.

If a no-code creator adds an environment dashboard and needs to **change the dashboard type** during the dashboard creation stage:

1. **Click Open in the package** button in the Freedom UI Designer toolbar. This determines package to store configuration dashboard and creates a new blank configuration dashboard. Learn more about how Creatio determines the package to store configuration dashboard: [Store app data](https://academy.creatio.com/documents?id=2419&anchor=title-2534-4).

If you set up environment dashboard before clicking **Open in the package** button, Creatio does not transfer customizations of the environment dashboard to configuration dashboard.

2. **Set up the configuration dashboard from scratch**. Instructions: [Set up dashboards in Freedom UI Designer](https://academy.creatio.com/documents?id=2577).


## Permissions for dashboard management [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics\#title-15196-1 "Direct link to Permissions for dashboard management")

Managing dashboards requires the following permission levels:

- **By license**. External users, i. e., users that have "studio creatio self-service portal cloud," "studio creatio external b2b portal cloud," and "studio creatio external b2c portal cloud" licenses, can only view dashboards regardless of their permissions.
- **By system operation**. You need to have permissions to the "Analytics setup" (`CanManageAnalytics` code) system operation. Learn more: [Set up system operation permissions](https://academy.creatio.com/documents?id=2000). Out of the box, the permission is granted to users that have the "All employees" role.
- **By dashboard record**. Available only for environment dashboards. Learn more: [Share records](https://academy.creatio.com/documents?id=1014).

The list of environment dashboards you can view depends on your current access rights and the following rules:

- You can view and manage dashboards you created.
- You can view dashboards someone shared with you.
- Users that have management roles cannot view dashboards of users that have employee roles and vice versa out of the box.

Out of the box, "All employees" organizational role has permissions to read the configuration dashboard. To **change the out-of-the-box access rights** to transfer them together with transferring configuration dashboard between environments:

1. Set up access rights for a dashboard. Instructions: [View and manage dashboards](https://academy.creatio.com/documents?id=1405).
2. Open the "Data" type schema whose **Object** property is set to "SysSchemaAdminUnitRight."
3. Select new "System administration object" to bind to the package. Instructions: ["Data" type schema](https://academy.creatio.com/documents?id=15123&anchor=initial-data-installation), step 6 (developer documentation).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics\#see-also "Direct link to See also")

[Set up widgets](https://academy.creatio.com/documents?id=2144)

[Set up dashboards in Freedom UI Designer](https://academy.creatio.com/documents?id=2577)

[View and manage dashboards](https://academy.creatio.com/documents?id=1405)

[Update list page template to include dashboards](https://academy.creatio.com/documents?id=2595)

[Store app data](https://academy.creatio.com/documents?id=2419)

[Schemas overview](https://academy.creatio.com/documents?id=15347) (developer documentation)

[Tech Hour: UI/ UX Building pages in Freedom UI Designer](https://www.youtube.com/watch?v=qyqnRbUHnjQ)

[Tech Hour: UI/ UX Best practices in Creatio](https://www.youtube.com/watch?v=BdoiOu9ncmw)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics\#e-learning-courses "Direct link to E-learning courses")

[Analytics in Creatio. Working with dashboards](https://academy.creatio.com/node/542493/takecourse)

- [Dashboard types](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#title-15196-2)
- [Transfer dashboard customizations](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#title-15196-3)
- [Permissions for dashboard management](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#title-15196-1)
- [See also](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/dashboards-basics#e-learning-courses)