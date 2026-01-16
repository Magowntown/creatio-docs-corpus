<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/access-management/creatio-ai-permissions)** (8.3).

Version: 8.2

On this page

In Creatio, you can set up permissions for AI Skills. You can also transfer these permissions between environments using Creatio’s data binding mechanism.

## Configure default execution permissions [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#title-2625-1 "Direct link to Configure default execution permissions")

Creatio assigns default execution permissions for all newly-made AI Skills. You can edit them later if needed. To change which users or roles receive the default permissions, configure the **Default schema operation right** lookup. To do this:

1. **Open** the **AI command center** workplace → **Creatio.ai skills**.

2. **Open** the **Default schema operation right** lookup.

3. **Click** **New**. This adds a new lookup record. Fill out the fields of the record as follows:



| Field | Value |
| --- | --- |
| Name | `CopilotIntentSchemaManager` |
| Description | Arbitrary value |
| User/role | The user or role who must have default execution permissions for new AI Skills |
| Operation type | 7 (Execute) |

4. **Save the changes**.


## Configure execution permissions for an existing AI Skill [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#title-2625-2 "Direct link to Configure execution permissions for an existing AI Skill")

If an AI Skill has no permissions configured, Creatio grants default permissions when you install the AI Skill for the first time.

You can modify the execution permissions for an existing AI Skill directly from the skill list. To do this:

1. **Open** the **AI command center** workplace → **Creatio.ai skills**.
2. **Open the relevant AI Skill**.
3. **Expand** the **Permission to execute** expanded list → **New**. This opens a window.
4. **Select the needed role** → **Select**.
5. **Save the changes**.

## Grant file upload permissions to external users [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#title-2625-3 "Direct link to Grant file upload permissions to external users")

External users must be granted explicit permissions to upload files and run AI Skills. To do this:

1. Make sure the "Can run Creatio.ai" (`CanRunCreatioAI` code) system operation permission is enabled for external users. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

2. Make sure external users have permission to use AI Skill.

3. Update the following **system settings** to allow access for external users:


   - "Maximum session file size, in MB" (`CreatioAIMaxSessionFileSize` code)
   - "Allowed file extensions" (`CreatioAIAllowedFileExtensions` code)
   - "Session file content size limit" (`CreatioAISessionFileContentSizeLimit` code)

Learn more: [Manage system settings](https://academy.creatio.com/documents?id=269). Ensure these settings are reviewed and configured carefully to avoid granting excessive access to external users.

## Transfer default permissions between environments [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#title-2625-4 "Direct link to Transfer default permissions between environments")

To transfer the **default execution permissions**, create data bindings for the `SysSchemaDefOperationRight` database table and transfer the package. To transfer **execution permissions for existing AI Skills**, create bindings for the `SysSchemaOperationRight` database table and transfer the package. Learn more: [Configuration elements of the Data type](https://academy.creatio.com/documents?id=15117) (developer documentation), [Transfer packages](https://academy.creatio.com/documents?id=15204) (developer documentation).

## Attach access permissions to AI Skills for package export [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#title-2625-5 "Direct link to Attach access permissions to AI Skills for package export")

If you need to export AI Skill access permissions together with the AI Skill package, take the following steps:

01. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_ai_permissions/btn_system_designer.png) to **open the System Designer**.

02. **Go to** the **Admin area** block → **Advanced settings**.

03. **Select the target package** in the left area. For example, `TestPackage`.

04. **Click** **Add** → **Data**.

05. **Search for and select**`SysSchemaOperationRight` in the **Object** field.

06. **Set** **Name** to a unique ID, for example, `SysSchemaOperationRight_myCustom`.

07. **Open** the **Bound data** tab.

08. **Click** **Add** → **Schema unique identifier**.

09. Open the skill page in a different tab and **copy** the **GUID** from the browser address bar (Fig. 1).
    Fig. 1 GUID of an AI Skill

    ![Fig. 1 GUID of an AI Skill](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/creatio_ai_permissions/scr_ai_skill_guid.png)

10. Return to the configuration screen, search by GUID, and **select the skill**.

11. **Save the changes**.


**As a result**, Creatio will add the **data configuration item** linked to your AI Skill to the package.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions\#see-also "Direct link to See also")

[System operation permissions](https://academy.creatio.com/documents?id=258)

[Creatio.ai overview](https://academy.creatio.com/documents?id=2528)

[Configuration elements of the Data type](https://academy.creatio.com/documents?id=15117) (developer documentation)

[Transfer packages](https://academy.creatio.com/documents?id=15204) (developer documentation)

- [Configure default execution permissions](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#title-2625-1)
- [Configure execution permissions for an existing AI Skill](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#title-2625-2)
- [Grant file upload permissions to external users](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#title-2625-3)
- [Transfer default permissions between environments](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#title-2625-4)
- [Attach access permissions to AI Skills for package export](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#title-2625-5)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/administration/user-and-access-management/access-management/creatio-ai-permissions#see-also)