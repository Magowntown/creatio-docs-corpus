<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/use-external-file-storages#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/use-external-file-storages)** (8.3).

Version: 8.2

On this page

Level: intermediate

Reduce the size of the database and time for maintenance by integrating external file storages into Creatio. By default, all files uploaded to Creatio are stored in the database. After connecting to an external file storage, files uploaded to Creatio will be automatically saved to the storage. That includes files uploaded to the **Attachments** detail via the UI, the mobile app, a business process, files attached to emails, etc. Learn more: [API for file management](https://academy.creatio.com/documents?id=15282) (developer documentation).

The **file upload** process works as follows (Fig. 1):

Fig. 1 Upload a file

![Fig. 1 Upload a file](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/On-site_deployment/use_external_file_storage/scr_upload_file.png)

1. User uploads the file.
2. Creatio saves file metadata, for example, size, extension, etc., to the database.
3. Creatio uploads file content to external storage using its ID from the database as the file name.

The **file download** process works as follows (Fig. 2)

Fig. 2 Download a file

![Fig. 2 Download a file](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/On-site_deployment/use_external_file_storage/scr_download_file.png)

1. User initiates the download process.
2. Creatio receives the download request and reads file metadata from the database.
3. Creatio reads file content from external storage.
4. Creatio sends the file as a response to the user.

Out of the box, the following file storage integrations are available in Creatio:

- **S3**. A cloud-based solution by AWS. Learn more: [Set up S3 file storage integration](https://academy.creatio.com/documents?id=2397).
- **Azure Blob**. A cloud-based solution by Microsoft. Learn more: [Set up Azure Blob file storage integration](https://academy.creatio.com/documents?id=2398).

Creatio can be **integrated with custom file storage**. To do this:

01. **Deploy external file storage**. Learn more in the official vendor documentation.
02. **Implement file storage in Creatio** using file management API. Instructions: [Implement a file content storage](https://academy.creatio.com/documents?id=15284) (developer documentation).
03. **Open the Lookups section**. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **Lookups**.
04. **Open the File content storages lookup**.
05. **Create a new record**.
06. **Fill out the storage parameters** based on your business goals.
07. **Save the changes**.
08. **Open** the **System settings** section. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **System settings**.
09. **Open** the "Active file content storage" (`ActiveFileContentStorage` code) system setting.
10. **Set** the external file storage as the system setting value.
11. **Save the changes**.

The setup details differ based on the parameters of the chosen file storage.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/use-external-file-storages\#see-also "Direct link to See also")

[API for file management (developer documentation)](https://academy.creatio.com/documents?id=15282)

[Set up S3 file storage integration](https://academy.creatio.com/documents?id=2397)

[Set up Azure Blob file storage integration](https://academy.creatio.com/documents?id=2398)

[Migrate files between database and external file storages](https://academy.creatio.com/documents?id=2517)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/use-external-file-storages#see-also)