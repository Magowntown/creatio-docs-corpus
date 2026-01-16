<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/file-migration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3

On this page

**FileMigrator** is a utility that migrates files between the database and external file storage, for example, AWS S3 or Azure Blob storage.

Before migrating files between file storages in Creatio, ensure that all custom functionality and integrations use supported file handling APIs only.

- **File API**. Learn more: [File API](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/manage-files) (developer documentation).
- **OData 4 API**. Available in Creatio 8.3.2 and later. Learn more: [Manage files using OData 4](http://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/file-api-odata-4) (developer documentation).

If you use Creatio **in the cloud**, contact [Creatio support](mailto:support@creatio.com) to migrate files.

If you use Creatio **on-site**, set up a connection to the external storage. Out of the box, Creatio can be integrated with AWS S3 and Azure Blob file storages. Instructions: [Use external files storages](https://academy.creatio.com/documents?id=2399).

View an example that migrates files from Creatio database to the AWS S3 file storage below. To do this:

1. **Install the WorkspaceConsole utility**. Instructions: [Set up the WorkspaceConsole utility](https://academy.creatio.com/documents?id=15207&anchor=title-2138-7) (developer documentation). Skip this step if you already have the utility installed.

2. **Receive the FileMigrator.dll file**. To do this, contact [Creatio support](mailto:support@creatio.com).

3. **Copy the "FileMigrator.dll" file** to the "..\\Terrasoft.WebApp\\DesktopBin\\WorkspaceConsole" directory.

4. **Migrate files**.

For this example, migrate files from Creatio database to the AWS S3 file storage. To do this:
1. Open the "..\\Terrasoft.WebApp\\DesktopBin\\WorkspaceConsole" directory.

2. Run the command that migrates files. Structure the command as follows:



      - For .NET Framework
      - For .NET

```cli
[Path to WorkspaceConsole]\Terrasoft.Tools.WorkspaceConsole.exe -operation=ExecuteScript -fileName=FileMigrator.dll -typeName=FileMigrator.Executor -workspaceName=Default -confRuntimeParentDirectory="[Path to the directory that contains an installed Creatio instance]\Terrasoft.WebApp" -logPath=[Path to the directory that contains log files] -sourceStorage="[Storage name]" -targetStorage="[Storage name]" -excludeSchemaNames="[List of schemas to exclude from the operation]" -schemaNames="[List of schemas to include in the operation]" -numberOfFiles=[Number of files to migrate] -autoExit=true
```

```cli
dotnet [Path to WorkspaceConsole]\Terrasoft.Tools.WorkspaceConsole.dll  -operation=ExecuteScript -fileName=FileMigrator.dll -typeName=FileMigrator.Executor -workspaceName=Default -confRuntimeParentDirectory="[Path to the directory that contains an installed Creatio instance]" -logPath=[Path to the directory that contains log files] -sourceStorage="[Storage name]" -targetStorage="[Storage name]" -excludeSchemaNames="[List of schemas to exclude from the operation]" -schemaNames="[List of schemas to include in the operation]" -numberOfFiles=[Number of files to migrate] -autoExit=true
```

View the WorkspaceConsole parameters for migrating files in the table below.

| Parameter | Parameter value | Parameter description |
| --- | --- | --- |
| -operation | ExecuteScript | Runs out-of-the-box or custom executable code (\*.dll). Required. |
| -fileName | FileMigrator.dll | The path to the "FileMigrator.dll" file. Required. |
| -typeName | FileMigrator.Executor | `FileMigrator.Executor` class whose instance is required for work. Service information. Required. |
| -workspaceName | Default | The name of the workspace (configuration). Out of the box, all users work in the "Default" workspace. Required. |
| -confRuntimeParentDirectory | For . **NET Framework**: \[Path to the directory that contains an installed Creatio instance\]\\Terrasoft.WebApp<br>For **.NET**: \[Path to the directory that contains an installed Creatio instance\] | Path to the parent directory of the "..\\Terrasoft.WebApp\\conf" directory. You must use the parameter in commands that compile Creatio or generate the static content. Required. |
| -logPath | \[Path to the directory that contains log files\] | The utility saves the operation log file to this directory. The file name consists of the operation start date and time. Optional. |
| -sourceStorage | \[Storage name\] | Type of storage from which files are migrated. Find the list of all the available values in the "Code" column of the **File content storages** lookup. To migrate files from Creatio database to the AWS S3 file storage, set `-sourceStorage` parameter to "Database." Required. |
| -targetStorage | \[Storage name\] | Type of storage to which files are migrated. Find the list of all the available values in the "Code" column of the **File content storages** lookup. To migrate files from Creatio database to the AWS S3 file storage, set `-targetStorage` parameter to "S3\_storage." Required. |
| -excludeSchemaNames | \[List of schemas to exclude from the operation\] | List of schemas whose files to forcibly exclude from the operation. Can accept multiple values separated by semicolon. Use the parameter to exclude files in listed objects from migration. Optional.<br>If you omit the parameter, the utility migrates all files from "Object" type schema that inherits the "File" (`File` code) object. As a rule, the names of these schemas contain the "File" suffix.<br>To **migrate files except specific schemas**, for example, do not migrate files of the **Contacts** section, use the "ContactFile" parameter value. "Contact attachment" (`ContactFile` code) object stores files from the contact attachments. The utility will migrate all files except files of the **Contacts** section. |
| -schemaNames | \[List of schemas to include in the operation\] | List of schemas whose files to include in the operation. Can accept multiple values separated by semicolon. Use the parameter to migrate only files in listed objects. Optional.<br>If you omit the parameter, the utility migrates all files from "Object" type schema that inherits the "File" (`File` code) object. As a rule, the names of these schemas contain the "File" suffix. For example, "Contact attachment" (`ContactFile` code) object that stores files from the contact attachments. |
| -numberOfFiles | \[Number of files to migrate\] | Number of files to migrate. Use the parameter to migrate files in multiple stages. If you omit the parameter, the utility migrates all files. Optional. |
| -autoExit | "true" or "false" | Specify whether to finish the utility process automatically after performing the operation. By default, "false." Optional. |

**As a result**, Creatio will migrate files from database to AWS S3 file storage. If the files were migrated successfully, the utility automatically deletes the files from the database. After you integrate AWS S3 file storage and migrate files to it, Creatio will store all files in the file storage.

After migration, file content is no longer stored in the database. The database keeps only file metadata and references to the external file storage, for example, AWS S3 or Azure Blob Storage. Therefore, any custom logic that relies on direct access to file content in the database will stop working after migration if it uses unsupported approaches for file handling.

If an **error occurs during migration**, FileMigrator utility:

- Stops the migration process.
- Logs an error for the affected file.
- Keeps the file that caused the error in the initial storage.

If you **migrate files from external file storage to Creatio database**, migrated files will remain in the external file storage. If needed, delete the migrated files manually.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/file-migration\#see-also "Direct link to See also")

[Use external files storages](https://academy.creatio.com/documents?id=2399)

[File API](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/manage-files) (developer documentation)

[Manage files using OData 4](http://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/file-api-odata-4) (developer documentation)

[Delivery using the WorkspaceConsole utility](https://academy.creatio.com/documents?id=15207) (developer documentation)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/file-migration#see-also)