<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration)** (8.3).

Version: 8.1

On this page

Level: intermediate

**Azure Blob file storage** is a cloud-based solution by Microsoft. Learn more: [official vendor documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction). Using the Azure Blob storage lets you reduce the Creatio database size. Data is stored as BLOB objects. Learn more: [Wikipedia](https://en.wikipedia.org/w/index.php?title=Binary_large_object&oldid=1087063332).

note

You can only connect Creatio to one Azure Blob storage.

If you use Creatio **in the cloud**, contact Creatio support to integrate an Azure Blob storage.

To integrate an Azure Blob file storage to Creatio **on-site**:

1. Setup in Azure Blob. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#title-3921-1)
2. Setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#title-3921-2)

## Setup in Azure Blob [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration\#title-3921-1 "Direct link to Setup in Azure Blob")

1. **Sign up to the Microsoft Azure portal**. Learn more: [official vendor documentation](https://azure.microsoft.com/en-us/features/azure-portal/).

2. **Enable Creatio to access the storage**. To do this, generate a "Blob Service endpoint" parameter.

3. **Enable authorized requests to the storage**. To do this, generate the "AccountName" and "AccountKey" parameters. Learn more: [official vendor documentation](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal).

4. **Create "ObjectContainerName" and "RecycleContainerName" containers** that have unique names.


   - "ObjectContainerName" is a container that stores files The files are stored indefinitely.
   - "RecycleContainerName" is a container that stores deleted files. They are kept for database backups. Container management is based on the soft deletion principle: a file deleted from the "ObjectContainerName" container is moved to the "RecycleContainerName" container. The storage time for deleted files is controlled by the container settings of the service. For example, a file can be stored in the container for 90 days, then deleted automatically. In Creatio, the storage time for deleted files is the same as the storage time for database backups.

Learn more: [official vendor documentation](https://docs.microsoft.com/en-us/azure/vs-azure-tools-storage-explorer-blobs#create-a-blob-container).

## Setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration\#title-3921-2 "Direct link to Setup in Creatio")

To save new files uploaded to the **Attachments** detail or email attachments to the Azure Blob storage rather than the database, take the following steps in Creatio:

1. **Set up a connection to the Azure Blob storage**. To do this, add an Azure Blob storage connection string to the `connectionStrings` parameter of the ConnectionStrings.config configuration file:





```xml
<connectionStrings>
       ...
       <add name="azureConnection" connectionString="AccountName=SOME_ACCOUNT_NAME; AccountKey=SOME_ACCOUNT_KEY; BlobEndpoint=SOME_BLOB_ENDPOINT; ObjectContainerName=SOME_OBJECT_CONTAINER_NAME; RecycleContainerName=SOME_RECYCLE_CONTAINER_NAME;" />
</connectionStrings>
```





where
   - `AccountName` is the account name for making an authorized request to the Azure Blob storage.
   - `AccountKey` is the account key for making an authorized request to the Azure Blob storage.
   - `BlobEndpoint` is the endpoint for accessing the Azure Blob storage. The value of the "Blob Service endpoint" parameter obtained in the previous step.
   - `ObjectContainerName` is the name of the container that stores files.
   - `RecycleContainerName` is the name of the container that stores deleted files. They are kept for database backups.
2. **Enable the "UseBaseEntityFileDeleteListener" additional feature** to ensure that connected files are also moved to "RecycleContainerName" correctly when a section record is deleted. To do this, change the status of the "UseBaseEntityFileDeleteListener" additional feature. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3) (developer documentation).

3. **Set the Azure Blob storage as the active file storage**. To do this, open the "Active File Content Storage" ("ActiveFileContentStorage" code) system setting. Select "Azure Blob storage" in the **Default value** field.


**As a result**, all files added to Creatio after connecting the Azure Blob storage will be uploaded there. Files previously added to Creatio will remain in the original storage. You can migrate previously added files from Creatio database to the "ObjectContainerName" container in the Azure Blob file storage and vice versa. Instructions: [Migrate files between database and external file storages](https://academy.creatio.com/documents?id=2517).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration\#see-also "Direct link to See also")

[Migrate files between database and external file storages](https://academy.creatio.com/documents?id=2517)

[Set up S3 file storage integration](https://academy.creatio.com/documents?id=2397)

[Manage an existing additional feature](https://academy.creatio.com/documents?id=15631) (developer documentation)

[Official Azure Blob documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)

[Binary large object](https://en.wikipedia.org/w/index.php?title=Binary_large_object&oldid=1087063332) (Wikipedia)

[Official Microsoft Azure documentation](https://azure.microsoft.com/en-us/features/azure-portal/)

- [Setup in Azure Blob](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#title-3921-1)
- [Setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#title-3921-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration#see-also)