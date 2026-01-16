<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/secure-file-upload)** (8.3).

Version: 8.1

On this page

Restrict the types of files uploaded to Creatio to improve application security. The security restrictions apply to both users and integrations such as third-party web services.

With the secure file upload enabled, Creatio checks the type of the files uploaded via the **Attachments and notes** detail. If the file type is not restricted, the file will be uploaded successfully. Otherwise, the file will not be uploaded, and the user will receive a notification that uploading the file is not allowed for security reasons. The security restrictions do not apply to files that have been added to Creatio earlier.

The restrictions only apply to the upload of new files to Creatio. Any users can download a file of a restricted type if they have sufficient permissions to access the file.

Creatio supports the following file security modes:

- File extensions **AllowList**. Only files with explicitly specified extensions are allowed for upload.
- File extensions **DenyList**. Files with any extensions not explicitly restricted are allowed for upload.
- **Unknown file types** are restricted. Allow or disallow uploading files without an extension when the type of the file cannot be determined by its content.

Secure file upload is managed by system administrators. The general procedure for **secure file upload** is as follows:

1. Select the preferable file security mode for uploading files.
2. Set up the file extensions allow list or deny list.
3. Define Creatio behavior upon uploading a file of an unknown type.
4. Set up security exceptions for web services if required.

## Select file security mode [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload\#title-294-1 "Direct link to Select file security mode")

1. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/file_security/btn_system_designer.png) to open the **System Designer**.

2. Open the **System settings** section.

3. Open the **File Security Mode** (FileSecurityMode) system setting.

4. Select the required restriction type in the **Default value** field:
1. " **Disable file security**" – disable all restrictions on file upload.
2. " **File extensions DenyList**" – disallow uploading files with specific file types.
3. " **File extensions AllowList**" – only allow uploading files with specific file types.
5. Click **Save**.


## Set up the file type list [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload\#title-294-2 "Direct link to Set up the file type list")

1. Click ![btn_system_designer00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/file_security/btn_system_designer00001.png) to open the **System Designer**.

2. Open the **System settings** section.

3. Open one of the following system settings:
1. **File extensions AllowList** (FileExtensionsAllowList) – to set up a list of allowed file extensions. By default, this setting contains the most frequently used file extensions.
2. **File extensions DenyList** (FileExtensionsDenyList) – to set up a list of restricted file extensions. By default, this setting contains extensions associated with potentially malicious file types.
4. Enter **file extensions** as a comma-separated list without whitespace characters in the **Default value** field ( [Fig. 1](https://academy.creatio.com/#XREF_86300_429)) and verify the entered data.
Fig. 1 Setting up the File extensions AllowList

![Fig. 1 Setting up the File extensions AllowList](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/file_security/scr_chapter_security_list_of_allowed.png)

5. Click **Save**.


## Set up restrictions for files of unknown types [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload\#title-294-3 "Direct link to Set up restrictions for files of unknown types")

Creatio determines the type of a file type by its extension. If the file extension is not available, Creatio uses the content of the file to determine the file type. By default, uploading files of unknown types is allowed. Denying such files from uploading will make working with Creatio more secure. However, this mode requires setting up a file extension allow list or deny list.

To **deny uploading** files of unknown types to Creatio:

1. Click ![btn_system_designer00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/file_security/btn_system_designer00002.png) to open the **System Designer**.
2. Open the **System settings** section.
3. Open the **Allow processing files of unknown type** (AllowFilesWithUnknownType) system setting.
4. Clear the **Default value** checkbox.
5. Click **Save**.

## Set up web services excluded from file security [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload\#title-294-4 "Direct link to Set up web services excluded from file security")

File security restrictions apply to all Creatio web services, including services added during customization, in project solutions, and Marketplace applications. **Add web services to the list of file security exclusions** to allow them to upload files of the restricted file types. To do this:

1. Click ![btn_system_designer00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/file_security/btn_system_designer00003.png) to open the **System Designer**.

2. Open the **Lookups** section.

3. Open the **List of file security excluded Uris** lookup.

4. Click **New**.

5. In the **Name** field, specify the **URI** of the web service to exclude from restrictions. The record will be saved automatically.
1. A **.NET Framework** example: /0/rest/ **Custom service name**/ **Custom service endpoint**, without specifying the application domain.
2. A **.NET Core and NET 6** example: /rest/ **Custom service name**/ **Custom service endpoint**, without specifying the application domain.
6. **Repeat** for other web services to enable them to upload files to the application without restrictions.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload\#see-also "Direct link to See also")

[Manage system settings](https://academy.creatio.com/documents?product=studio&ver=7&id=269)

[Manage lookup values](https://academy.creatio.com/documents?product=studio&ver=7&id=271)

- [Select file security mode](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#title-294-1)
- [Set up the file type list](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#title-294-2)
- [Set up restrictions for files of unknown types](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#title-294-3)
- [Set up web services excluded from file security](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#title-294-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/secure-file-upload#see-also)