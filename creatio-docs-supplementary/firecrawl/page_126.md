<!-- Source: page_126 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

You can set a section icon only when you create a section, but you can change it at any moment. A newly created section has the same icon for both the main Creatio instance and the Creatio Mobile app. Creatio lets you set up a dedicated section icon for Creatio Mobile that differs from the section icon for the Creatio instance.

Creatio lets you use the following icons as a dedicated section icon for Creatio Mobile:

- Custom icon
- Icon of the existing section. For example, the icon of the **Contacts** section.

The general procedure to set up a dedicated icon differs for the Freedom UI and Classic UI sections.

## Use a custom icon as a Freedom UI section icon in Creatio Mobile [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-1 "Direct link to Use a custom icon as a Freedom UI section icon in Creatio Mobile")

### 1\. Upload a custom icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-2 "Direct link to 1. Upload a custom icon")

1. **Create an app** based on the **Records & business processes** template. Instructions: [Create an app manually](https://academy.creatio.com/documents?id=2377&anchor=title-2232-6). For example, create an **Image upload** app.

2. **Open the Image upload form page**.

3. **Add an "Image" type field** to an arbitrary place in the Freedom UI Designer. Leave default field parameter values.

4. **Save the changes**.

5. **Open the Image upload section**.

6. **Create a new page**. To do this, click **New**.

7. **Fill out the image properties**.



| Property | Property value |
| --- | --- |
| Name | Image\_1 |
| ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_UploadScreenshotButton.png) | Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatioMarketplaceConsole/8.0/scr_UploadScreenshotButton.png) to upload the icon. |

8. **Save the changes**.


**As a result**, the custom icon will be uploaded to the `SysImage` database table.

### 2\. Find the icon ID [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-3 "Direct link to 2. Find the icon ID")

1. **Open the Lookups section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **Lookups**.

2. **Create a lookup**.
1. Click **New lookup**.

2. Fill out the lookup properties.



      | Property | Property value |
      | --- | --- |
      | Name | Images |
      | Object | Image |

3. Save the changes.
3. **Open the Images lookup**.

4. **Set up the lookup list**.
1. Click **View** → **Select fields to display**.
2. Add the column to the lookup list. To do this, click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionEditableList/7.18/scr_add_button.png) → select the **Id** column → **Select**.
3. Save the changes.

**As a result**, the **Id** column will include the ID of the custom icon. For example, the `scr_RequestsAppIcon.svg` icon ID is "4e462f54-eb43-8a32-869b-b46e6f4293c4."

### 3\. Change the section icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-4 "Direct link to 3. Change the section icon")

1. **Open the mobile app manifest**.
1. Open the **Advanced settings** tab of a custom app in the No-Code Designer. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **Application management** → **Application Hub** → select the needed app → **Advanced settings**.
2. Open the client module schema that has the "Manifest" suffix. For example, `MobileApplicationManifestDefaultWorkplace`.
2. **Apply a new icon to the section**.
1. Go to the `Modules` schema section → configuration object of a section. For example, the `UsrRequests` configuration object of a **Requests** section.

2. Set the `iconId` property to the icon ID value.

      View the example that sets the custom icon whose ID is "4e462f54-eb43-8a32-869b-b46e6f4293c4" for the **Requests** section below.



      Modules schema section





      ```js
      {
          ...,
          "Modules": {
              "UsrRequests": {
                  ...,
                  "iconId": "4e462f54-eb43-8a32-869b-b46e6f4293c4",
                  ...,
              }
          },
          ...
      }
      ```
3. **Save the changes**.


**As a result**, the custom icon will be used as the icon of a Freedom UI section in Creatio Mobile.

## Use the icon of an existing section as a Freedom UI section icon in Creatio Mobile [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-5 "Direct link to Use the icon of an existing section as a Freedom UI section icon in Creatio Mobile")

Unlike a custom icon, when you use the icon of an existing section, Creatio applies both the icon and the name of the existing section to the Freedom UI section.

### 1\. Find the section ID [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-6 "Direct link to 1. Find the section ID")

1. **Open the Lookups section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **Lookups**.

2. **Create a lookup**.
1. Click **New lookup**.

2. Fill out the lookup properties.



      | Property | Property value |
      | --- | --- |
      | Name | Sections |
      | Object | Section in SysModule folder |

3. Save the changes.
3. **Open the Sections lookup**.

4. **Set up the lookup list**.
1. Click **View** → **Select fields to display**.
2. Add the column to the lookup list. To do this, click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionEditableList/7.18/scr_add_button.png) → ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/icn_add_object_in_lookup.png) → select the **Section** object → select the **Id** column → **Select**.
3. Save the changes.

**As a result**, the **Section.Id** column will include the section ID. For example, the **Contacts** section ID is "065063c9-8180-e011-afbc-00155d04320c."

### 2\. Change the section icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-7 "Direct link to 2. Change the section icon")

1. **Open the mobile app manifest**.
1. Open the **Advanced settings** tab of a custom app in the No-Code Designer. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **Application management** → **Application Hub** → select the needed app → **Advanced settings**.
2. Open the client module schema that has the "Manifest" suffix. For example, `MobileApplicationManifestDefaultWorkplace`.
2. **Apply a new icon to the section**.
1. Go to the `Modules` schema section → configuration object of a section. For example, the `UsrRequests` configuration object of a **Requests** section.

2. Set the `sysModuleId` property to the section ID value.

      View the example that sets the same icon whose ID is "065063c9-8180-e011-afbc-00155d04320c" for both the **Requests** and **Contacts** sections below.



      Modules schema section





      ```js
      {
          ...,
          "Modules": {
              "UsrRequests": {
                  ...,
                  "sysModuleId": "065063c9-8180-e011-afbc-00155d04320c",
                  ...,
              }
          },
          ...
      }
      ```
3. **Save the changes**.


**As a result**, the icon of an existing section will be used as the icon of a Freedom UI section in Creatio Mobile.

## Use a custom icon as a Classic UI section icon in Creatio Mobile [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-8 "Direct link to Use a custom icon as a Classic UI section icon in Creatio Mobile")

### 1\. Upload a custom icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-9 "Direct link to 1. Upload a custom icon")

1. **Open the Configuration section**. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Create the client module schema** to upload an icon. Instructions: [Implement a non-visual module](https://academy.creatio.com/documents?id=15106&anchor=title-3028-9).

For example, use the schema properties as follows.



| Property | Property value |
| --- | --- |
| Code\* | UsrMobileImageList |
| Title\* | MobileImageList |

4. **Save the changes**.

5. **Go to the Images node’s context menu**.

6. **Open the image properties**. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/scr_add_button_in_schema.png).

7. **Fill out the image properties**.



| Property | Property value |
| --- | --- |
| Code\* | UsrRequestsAppIcon |
| Title | RequestsAppIcon |
| Image | 1. Click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/icn_upload_image.png). This opens the default downloads directory.<br>   2. Select the icon file to upload. |

8. **Click Add**.

9. **Save the changes**.


**As a result**, the custom icon will be uploaded to the `SysImage` database table.

### 2\. Change the section icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-10 "Direct link to 2. Change the section icon")

1. **Open the mobile app manifest**.
1. Open the **Configuration** section. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).
2. Select a user-made package.
3. Open the client module schema that has the "Manifest" suffix. For example, `MobileApplicationManifestDefaultWorkplace`.
2. **Apply a new icon to the section**.
1. Create a new property or select an existing `CustomSchemas` property.

2. Set the `CustomSchemas` schema section to the code of the client module schema that has the icon uploaded.

3. Go to the `Modules` schema section → configuration object of a section. For example, the `UsrRequests` configuration object of a **Requests** section.

4. Set the `IconV2` property to the icon ID value. The template for the icon ID value is as follows: `[SchemaCode][IconCode]`, where:


      - `[SchemaCode]` is the code of the client module schema that has the icon uploaded.
      - `[IconCode]` is the code of the image uploaded to the client module schema.

View the example that sets the custom icon uploaded to the `UsrMobileImageList` schema for the **Requests** section below.

CustomSchemas and Modules schema sections

```js
{
    ...,
    "CustomSchemas": [\
        "UsrMobileImageList"\
        ...\
    ],
    "Modules": {
        "UsrRequests": {
            ...,
            "IconV2": {
                "ImageId": "UsrMobileImageListUsrRequestsAppIcon",
                ...,
            },
            ...,
        },
    },
    ...
}
```
3. **Save the changes**.


**As a result**, the custom icon will be used as the icon of a Classic UI section in Creatio Mobile.

## Use the icon of an existing section as a Classic UI section icon in Creatio Mobile [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-11 "Direct link to Use the icon of an existing section as a Classic UI section icon in Creatio Mobile")

### 1\. Find the section ID [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-12 "Direct link to 1. Find the section ID")

1. **Open the Configuration section**. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).
2. **Open the**`MobileImageList` **client module schema**.
3. **Go to the** **Images** **node’s context menu**.
4. **Open the list of section icons**. To do this, click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/icn_open_node_menu.png).
5. **Open the Image window**. To do this, go to the row of the section whose icon to use → click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/icn_view_image_properties.png). For example, the `ContactModuleImage` code is the code of the image for the **Contacts** section.

**As a result**, the `Code` property will include the code of the image for an existing section.

### 2\. Change the section icon [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#title-15170-13 "Direct link to 2. Change the section icon")

1. **Open the mobile app manifest**.
1. Open the **Configuration** section. Instructions: [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).
2. Select a user-made package.
3. Open the client module schema that has the "Manifest" suffix. For example, `MobileApplicationManifestDefaultWorkplace`.
2. **Apply a new icon to the section**.
1. Go to the `Modules` schema section → configuration object of a section. For example, the `UsrRequests` configuration object of a **Requests** section.

2. Set the `IconV2` property to the icon ID value. The template for the icon ID value is as follows: `[SchemaCode][IconCode]`, where:


      - `[SchemaCode]` is the code of the client module schema that has the icon uploaded.
      - `[IconCode]` is the code of the image for an existing section.

View the example that sets the same icon for both the **Requests** and **Contacts** sections below.

Modules schema section

```js
{
    ...,
    "Modules": {
        "UsrRequests": {
            ...,
            "IconV2": {
                "ImageId": "MobileImageListContactModuleImage",
                ...,
            },
            ...,
        },
    },
    ...
}
```
3. **Save the changes**.


**As a result**, the icon of an existing section will be used as the icon of a Classic UI section in Creatio Mobile.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon\#see-also "Direct link to See also")

[Manage apps](https://academy.creatio.com/documents?id=2377)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101) (developer documentation)

["Client module" type schema](https://academy.creatio.com/documents?id=15106) (developer documentation)

- [Use a custom icon as a Freedom UI section icon in Creatio Mobile](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-1)
  - [1\. Upload a custom icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-2)
  - [2\. Find the icon ID](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-3)
  - [3\. Change the section icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-4)
- [Use the icon of an existing section as a Freedom UI section icon in Creatio Mobile](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-5)
  - [1\. Find the section ID](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-6)
  - [2\. Change the section icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-7)
- [Use a custom icon as a Classic UI section icon in Creatio Mobile](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-8)
  - [1\. Upload a custom icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-9)
  - [2\. Change the section icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-10)
- [Use the icon of an existing section as a Classic UI section icon in Creatio Mobile](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-11)
  - [1\. Find the section ID](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-12)
  - [2\. Change the section icon](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#title-15170-13)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/set-up-section-icon#see-also)