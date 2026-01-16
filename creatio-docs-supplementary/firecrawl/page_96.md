<!-- Source: page_96 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

**Mobile portal (mobile application for portal users)** is a mobile workplace. The **purpose** of the mobile portal is to enable the mobile portal users to create cases and communicate with customer support.

A mobile portal has **configurable**:

- mobile portal user workplace
- case list
- case page
- page that adds cases

## Add base package schema to the user-made package [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-12 "Direct link to Add base package schema to the user-made package")

If you are yet to perform the setup using the Mobile application wizard, the base package schema might not be available in the user-made package.

To **add base package schema to the user-made package**:

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.
3. Open the **Portal** workplace in the section list.
4. Click **Set up sections** on the toolbar.
5. Select the **Cases** section in the section list and click **Page setup**.
6. Save the settings of the **Cases** section page.
7. Save the settings of the **Mobile application wizard** section.

## Set up the workplace of a mobile portal user [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-1 "Direct link to Set up the workplace of a mobile portal user")

You can set up the workplace of a mobile portal user in the following **ways**:

- Add a new workplace.
- Hide a workplace.
- Delete a workplace.

### Add a workplace of a mobile portal user [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-2 "Direct link to Add a workplace of a mobile portal user")

To **check if the Portal workplace** is available:

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.

The **Portal** workplace is in the **Mobile application wizard** section. By default, all mobile portal users can access the workplace.

If the **Portal** workplace is not available in the **Mobile application wizard** section, add the workplace.

To **add a workplace of a mobile portal user**:

1. Make sure that your Creatio application includes the mobile portal functionality.

2. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.

3. Go to the **System setup** block → **Mobile application wizard**.

4. Click **New workplace** in the **Mobile application wizard** section toolbar.

5. Fill out the **workplace properties**.
   - Set **Name** to the workplace name.
   - Set **Code** to "Portal."
6. Configure the access permissions to the workplace for users or user groups on the **Roles** detail. Learn more: [Object operation permissions](https://academy.creatio.com/documents?id=250).

7. Click **Set up sections** on the toolbar. By default, the workplace of a mobile portal user includes the **Cases** section.

8. Save the settings of the **Mobile application wizard** section.


As a result, Creatio will add a workplace of a mobile portal user.

Learn more about adding a workplace to a mobile application: [Set up mobile app workplaces](https://academy.creatio.com/documents?id=1391&anchor=title-240-1).

### Hide the workplace of a mobile portal user [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-3 "Direct link to Hide the workplace of a mobile portal user")

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.
3. Open the **Portal** workplace in the section list.
4. Delete users or user groups of the **Portal** workplace. To do this, click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Settings.png) and select **Delete** on the **Roles** detail.

As a result, Creatio will hide the workplace of a mobile portal user.

### Delete the workplace of a mobile portal user [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-4 "Direct link to Delete the workplace of a mobile portal user")

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.
3. Select the **Portal** workplace in the section list and click **Delete**.

As a result, Creatio will delete the workplace of a mobile portal user.

## Set up the case list [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-5 "Direct link to Set up the case list")

You can set up the case list of a mobile portal in the following **ways**:

- Add a column to the case list.
- Make a case list column searchable.
- Hide the column title from the case list.
- Change the case sorting order in the list.

### Add a column to the case list [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-6 "Direct link to Add a column to the case list")

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.
3. Open the **Portal** workplace in the section list.
4. Click **Set up sections** on the toolbar.
5. Select the **Cases** section in the section list and click **List setup**.
6. Click the **New column** button in the **Subtitle** or **Additional columns** block and select the required column.
7. Save the list settings in the **Cases** section.
8. Save the settings of the **Mobile application wizard** section.

As a result, Creatio will add a column to the case list. However, the column will not be searchable. To **make the case list column searchable**, follow the instructions in different section: [Add a searchable column to the case list](https://academy.creatio.com/documents?id=15903&anchor=title-3641-11).

Learn more about adding a column to the section list: [Set up mobile application section list](https://academy.creatio.com/documents?id=1393).

### Make a case list column searchable [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-11 "Direct link to Make a case list column searchable")

**Number** and **Description** columns of the case list are searchable. You can make other columns searchable as well. To do this, add the columns to the `MobileCaseGridPageSettingsPortal` schema.

To **make a case list column searchable**:

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. Open the `MobileCaseGridPageSettingsPortal` schema in the user-made [package](https://academy.creatio.com/documents?id=15121). If you are yet to set up the case list using the Mobile application wizard, the `MobileCaseGridPageSettingsPortal` schema will not be available in the user-made package. To **add** the `MobileCaseGridPageSettingsPortal` schema **to the user-made package**, follow the instructions in a different section: [Add a base package schema to the user-made package](https://academy.creatio.com/documents?id=15903&anchor=title-3641-12).

3. Make a **case list column searchable**.

Add a `merge` operation of the `diffV2` property. This will let you add any operation that modifies metadata to the property as a string.

The example below makes the `[Subject]` column of the case list searchable in Creatio.



Example of the searchExpressions property setup





```js
[\
       {\
           "operation": "merge",\
           "name": "settings",\
           "values": {"diffV2":"[{\"operation\":\"insert\",\"name\":\"Case_Controller_SearchExpression_Subject\",\"parentName\":\"Case_Controller\",\"propertyName\":\"searchExpressions\",\"values\":{\"leftCondition\":\"Subject\"}}]"\
           }\
       }\
       ...\
]
```









This example adds the `[Subject]` column settings to the current search settings in the `searchExpressions` property.

4. Click **Save** on the Module Designer’s toolbar.


As a result, **Number**, **Description**, and **Subject** columns of the case list will be searchable.

### Hide the column title from the case list [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-7 "Direct link to Hide the column title from the case list")

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. Open the `MobileCaseGridPageSettingsPortal` schema in the user-made [package](https://academy.creatio.com/documents?id=15121). If you are yet to set up the case list using the Mobile application wizard, the `MobileCaseGridPageSettingsPortal` schema will not be available in the user-made package. To **add** the `MobileCaseGridPageSettingsPortal` schema **to the user-made package**, follow the instructions in a different section: [Add base package schema to the user-made package](https://academy.creatio.com/documents?id=15903&anchor=title-3641-12).

3. Hide the **column title from the case list**.

Add the configuration object of the column whose title to hide to the beginning of the `diffV2` array of modifications.


1. Specify the column in the `name` property. Column name template is as follows: `ObjectName_ListItem_Subtitle_ColumnName`.
2. Set the `visible` property to `false`. The `visible` property specifies whether to display the column title.

The example below hides the `[Status]` column title in Creatio.

Example of the values property setup

```js
[\
    {\
        "operation": "merge",\
        "name": "settings",\
        "values": {"diffV2":"[{\"operation\":\"merge\",\"name\":\"Case_ListItem_Subtitle_Status\",\"values\":{\"label\":{\"visible\":false}}}]"\
        }\
    }\
    ...\
]
```

`Case_ListItem_Subtitle_Status` is the value of the `name` property of the `[Status]` column in the `Case` object in Creatio.

4. Click **Save** on the Module Designer’s toolbar.


As a result, Creatio will hide the column title from the case list.

### Change the case sorting order in the list [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-8 "Direct link to Change the case sorting order in the list")

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. Open the `MobileCaseGridPageSettingsPortal` schema in the user-made [package](https://academy.creatio.com/documents?id=15121). If you are yet to set up the case list using the Mobile application wizard, the `MobileCaseGridPageSettingsPortal` schema will not be available in the user-made package. To **add** the `MobileCaseGridPageSettingsPortal` schema **to the user-made package**, follow the instructions in a different section: [Add base package schema to the user-made package](https://academy.creatio.com/documents?id=15903&anchor=title-3641-12).

3. Change the **sorting order in the case list**.

Add the configuration object that contains the list display settings to the beginning of the `diffV2` array of modifications.


1. Specify the column to use for sorting in the `name` property. Column name template is as follows: `ObjectName_Model_Column_ColumnName`.
2. Specify the sorting order in the `orderDirection` property: `1` for ascending, `2` for descending.
3. Use the `orderPosition` property to specify the index of the column in the column collection to use for sorting.

The example below changes the case list sorting in Creatio. The cases in the list are sorted by the `[RegisteredOn]` column in ascending order.

Example of the values property setup

```js
[\
    {\
        "operation": "merge",\
        "name": "settings",\
        "values": {"diffV2":"[{\"operation\":\"merge\",\"name\":\"Case_Model_Column_RegisteredOn\",\"values\":{\"orderDirection\":1}}]"\
        }\
    }\
    ...\
]
```

`Case_Model_Column_RegisteredOn` is the value of the `name` property for the `[RegisteredOn]` column in the `Case` object in Creatio.

4. Click **Save** on the Module Designer’s toolbar.


As a result, Creatio will display cases sorted in the specified order in the list.

## Set up the case page [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-9 "Direct link to Set up the case page")

Set up the case page to add a column to the **Details** tab.

To **add a column to the Details tab** of the case page:

1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_system_designer.png) to open the System Designer.
2. Go to the **System setup** block → **Mobile application wizard**.
3. Open the **Portal** workplace in the section list.
4. Click **Set up sections** on the toolbar.
5. Select the **Cases** section in the section list and click **Page setup**.
6. Click **New column** in the **General information** block and select the **Number** column.
7. Save the settings of the **Cases** section page.
8. Save the settings of the **Mobile application wizard** section.

note

Columns of the **Details** tab are read-only.

## Set up the page that adds cases [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#title-3641-10 "Direct link to Set up the page that adds cases")

You can add a column to the page that adds cases.

To **add a column to the page that adds cases**:

1. Create a **schema of the case page module**.
1. [Go to the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. Open the `MobileCaseMiniPagePortal` schema of the `CaseMobile` package and copy its contents.

3. select a user-made [package](https://academy.creatio.com/documents?id=15121) to add the schema.

4. Click **Add** → **Module** on the section list toolbar.


      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_module.png)

5. Fill out the **schema properties**.


      - Enter the schema name in the **Code**\* property. The name must start with the prefix specified in the **Prefix for object name** (`SchemaNamePrefix` code) system setting, `Usr` by default. Can contain Latin characters and digits. When you create a schema, Creatio adds the prefix specified in the **Prefix for object name** (`SchemaNamePrefix` code) system setting to the current field automatically. Creatio checks whether the prefix exists and matches the system setting when you save the schema properties. If the prefix does not exist or does not match, Creatio sends a corresponding user notification.
      - Enter the localizable schema title in the **Title**\* property. The schema title is generated automatically and matches the value of the **Code** property without a prefix.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobilePortal/7.18/scr_MobileCaseMiniPagePortal_props.png)

6. Add the copied contents of the `MobileCaseMiniPagePortal` schema of the `CaseMobile` package to the custom module.

7. Move the [localized strings](https://academy.creatio.com/documents?id=15271) of the `MobileCaseMiniPagePortal` schema of the `CaseMobile` package to the custom module.

8. Add a **column**.
      1. Specify the column in the `value` property of the `viewConfig` configuration object. Column name template is as follows: `$ColumnName`.

         The example below adds the `[$ConfItem]` column in Creatio.



         Example that adds the column to the viewConfig property





         ```js
         {
             "operation": "insert",
             "name": "CaseAddCardConfItem",
             "values": {"type": "EditField", "properties": {"value": "$ConfItem"}},
             "parentName": "CaseAddCardBody",
             "propertyName": "items",
             "index": 2
         },
         ```









         `$ConfItem` is the column name in Creatio.

      2. Add the description of the required column to the `controllers` property. Use the `columnPath` property to specify the name of the schema column of the `Case` object.

         The example below adds the description of the `[ConfItem]` column in Creatio.



         Example that adds the column to the controllers property





         ```js
         {
             "operation": "insert",
             "name": "CaseModelConfItemColumn",
             "values": {"expression": {"columnPath": "ConfItem", "expressionType": 0}},
             "parentName": "CaseModel",
             "propertyName": "columns",
             "index": 3
         },
         ```
9. Click **Save** on the Module Designer’s toolbar.
2. **Register** the earlier created `UsrMobileCaseMiniPagePortal` custom schema in the portal workplace manifest.
1. Open the `MobileApplicationManifestPortal` schema in the user-made [package](https://academy.creatio.com/documents?id=15121). If you are yet to set up the app using the Mobile application wizard, the `MobileApplicationManifestPortal` schema will not be available in the user-made package. To **add** the `MobileApplicationManifestPortal` schema **to the user-made package**, follow the instructions in a different section: [Add base package schema to the user-made package](https://academy.creatio.com/documents?id=15903&anchor=title-3641-12).

2. Register the **schema**.


      1. Specify the schema used to add the schema record of the `Case` object in the `Modules` schema section.
      2. Specify the schema used to extend the schema of the `Case` object in the `Models` schema section.

The example below registers the `UsrMobileCaseMiniPagePortal` schema.

Example of the Modules and Models schema sections setup

```js
{
    ...,
    "Modules": {
        "Case": {
            ...
            "screens": {
                ...
                "add": {
                    "schemaName": "UsrMobileCaseMiniPagePortal"
                }
                ...
            }
            ...
        }
        ...
    },
    "Models": {
        "Case": {
            ...
            "PagesExtensions": [\
                "UsrMobileCaseMiniPagePortal"\
            ]
        }
        ...
    },
    ...
}
```
3. Click **Save** on the Module Designer’s toolbar.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview\#see-also "Direct link to See also")

[Set up mobile app workplaces](https://academy.creatio.com/documents?id=1391)

[Set up mobile application section page](https://academy.creatio.com/documents?id=1394)

[Set up mobile application section list](https://academy.creatio.com/documents?id=1393)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101)

[Packages basics](https://academy.creatio.com/documents?id=15121)

[Object operation permissions](https://academy.creatio.com/documents?id=262)

- [Add base package schema to the user-made package](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-12)
- [Set up the workplace of a mobile portal user](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-1)
  - [Add a workplace of a mobile portal user](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-2)
  - [Hide the workplace of a mobile portal user](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-3)
  - [Delete the workplace of a mobile portal user](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-4)
- [Set up the case list](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-5)
  - [Add a column to the case list](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-6)
  - [Make a case list column searchable](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-11)
  - [Hide the column title from the case list](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-7)
  - [Change the case sorting order in the list](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-8)
- [Set up the case page](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-9)
- [Set up the page that adds cases](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#title-3641-10)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/overview#see-also)