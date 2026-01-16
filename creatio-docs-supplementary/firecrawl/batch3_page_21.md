<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration)** (8.3).

Version: 8.2

On this page

Level: intermediate

**S3 file storage** is a cloud-based object storage REST service. It lets you use data as is without scalability restrictions.

**S3 (Simple Storage Service)** is a data transfer protocol developed by Amazon. We recommend using Amazon S3 storage. Learn more: [official vendor documentation](https://docs.aws.amazon.com/s3/index.html?nc2=h_ql_doc_s3).

note

You can only connect one S3 storage to Creatio.

note

If you want to develop functionality that will create, download, delete or do any other operations with files that are stored in external file storage, then use FileAPI for that. Learn more: [API for file management (developer documentation)](https://academy.creatio.com/documents?id=15282)

If you use Creatio **in the cloud**, contact Creatio support to integrate an S3 file storage.

To integrate an S3 file storage to Creatio **on-site**:

1. Setup in S3. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#title-3428-1)
2. Setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#title-3428-2)

## Setup in S3 [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration\#title-3428-1 "Direct link to Setup in S3")

1. **Create an account that has an S3-capable storage service**.

2. **Enable Creatio to access the storage**. To do this, generate a "ServiceUrl" parameter.

3. **Enable authorized requests to the storage**. To do this, generate the "AccessKey" and "SecretKey" parameters.

4. **Create "ObjectBucketName" and "RecycleBucketName" buckets** that have unique names.


   - "ObjectBucketName" is a bucket for storing files. The files are stored indefinitely.
   - "RecycleBucketName" is a bucket for storing deleted files. They are kept for database backups. Working with the buckets is based on the soft deletion principle: a file deleted from the "ObjectBucketName" bucket is moved to the "RecycleBucketName" bucket. The storage time for deleted files is controlled by the bucket settings of the service. For example, a file can be stored in the bucket for 90 days, then deleted automatically. In Creatio, the storage time for deleted files is the same as the storage time for database backups.

Learn more: [official vendor documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html).

## Setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration\#title-3428-2 "Direct link to Setup in Creatio")

To save new files uploaded to the **Attachments** detail or email attachments in the S3 storage rather than the database, make the following adjustments on the Creatio side:

1. **Set up a connection to the S3 storage**. To do this, add an S3 storage connection string to the `connectionString` parameter of the ConnectionStrings.config configuration file:





```xml
<connectionStrings>
       ...
       <add name="s3Connection" connectionString="ServiceUrl=SOME_SERVICE_URL; AccessKey=SOME_ACCESS_KEY; SecretKey=SOME_SECRET_KEY; ObjectBucketName=SOME_OBJECT_BUCKET_NAME; RecycleBucketName=SOME_RECYCLE_BUCKET_NAME;" />
</connectionStrings>
```









where
   - `ServiceUrl` is the endpoint for accessing the S3 storage.
   - `AccessKey` is the account access key for making an authorized request to the S3 storage.
   - `SecretKey` is the account key for making an authorized request to the S3 storage.
   - `ObjectBucketName` is the name of the bucket for storing files.
   - `RecycleBucketName` is the name of the bucket for storing deleted files. They are kept for database backups.
2. **Enable the "UseBaseEntityFileDeleteListener" additional feature** to ensure that connected files are also moved to "RecycleBucketName" correctly when a section record is deleted. To do this, change the status of the "UseBaseEntityFileDeleteListener" additional feature. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?id=15631&anchor=title-3459-3) (developer documentation).

3. **Set the S3 storage as the active file storage**. To do this, open the "Active File Content Storage" ("ActiveFileContentStorage" code) system setting. Select "S3 storage" in the **Default value** field.


**As a result**, all files added to Creatio after connecting the S3 storage will be uploaded there. Files previously added to Creatio will remain in the original storage. You can migrate previously added files from Creatio database to the "ObjectBucketName" bucket in the S3 file storage and vice versa. Instructions: [Migrate files between database and external file storages](https://academy.creatio.com/documents?id=2517).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration\#see-also "Direct link to See also")

[Migrate files between database and external file storages](https://academy.creatio.com/documents?id=2517)

[Set up Azure Blob file storage integration](https://academy.creatio.com/documents?id=2398)

[Manage an existing additional feature](https://academy.creatio.com/documents?id=15631) (developer documentation)

[Official Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html?nc2=h_ql_doc_s3)

- [Setup in S3](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#title-3428-1)
- [Setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#title-3428-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration#see-also)