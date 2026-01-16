<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/creatio-maintenance/backup-datadase)** (8.3).

Version: 8.1On-site

On this page

You will need a backup of your production database to create a test website, to update Creatio, as well as to roll back the changes in case of problems, for example, compatibility with customizations.

note

If you deploy a backup of the production database and you want to disable your integrations in it, run the Disable\_Synchronization.sql script. [Download the script](https://academy.creatio.com/sites/default/files/documents/downloads/Disable_Synchronization.sql).

## Back up Microsoft SQL Server database [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase\#title-143-3 "Direct link to Back up Microsoft SQL Server database")

1. Run Microsoft SQL Server Management Studio.

2. Select the **Back Up** command under the **Tasks** section in the context menu of the application database catalog.

3. Specify the name of the database copy and the directory to create backup. Click **OK** to start the backup process (Fig. 1).
Fig. 1 Back up the database

![Fig. 1 Back up the database](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/back_up_db/update_guide_backup.png)




note





Make sure the directory for the database backup already exists. The SQL server has no rights to create directories.





When updating the Creatio production version, we recommend creating a copy of the application using any file manager.


To **open a database backup**:

1. **Log in** to Microsoft SQL Studio.
2. **Create a new database** if you need to extract only certain data from the backup, or select an existing database if you need to restore all data.
3. Select the **Restore database** command in the context menu of the database. This opens a window.
4. **Specify the path** to the backup file.
5. Click **OK** and wait for the restoration process to complete.

Learn more about deploying the backup database: [Deploy Microsoft SQL Database for Creatio](https://academy.creatio.com/documents?id=2132).

## Back up Oracle Database [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase\#title-143-4 "Direct link to Back up Oracle Database")

1. Connect to the Oracle server using the SqlPlus utility:





```js
sqlplus "SYS/SYS_PASSWORD@ORACLE_HOST:ORACLE_PORT/SERVICE_NAME AS SYSDBA"
```





where:
   - `SYS_PASSWORD`: a password for authorization on the Oracle server.
   - `ORACLE_HOST`: Oracle server address.
   - `ORACLE_PORT`: Oracle server port.
   - `SERVICE_NAME`: Oracle service name.
2.  Execute the following SqlPlus commands:





```js
CREATE OR REPLACE DIRECTORY DIRECTORY_ALIAS AS 'PATH_TO_BACKUP_DIRECTORY';
```









```js
GRANT READ, WRITE ON DIRECTORY DIRECTORY_ALIAS to BACKUP_SCHEMA_NAME;
```





where:
   - `DIRECTORY_ALIAS`: an alias for the directory where the backup copy will be placed.
   - `PATH_TO_BACKUP_DIRECTORY`: full path to the directory where the backup copy will be placed.
   - `BACKUP_SCHEMA_NAME`: name of the schema for which the backup is made.
3.  Back up your schema using the expdp utility:





```js
expdp "BACKUP_SCHEMA_NAME/BACKUP_SCHEMA_PASSWORD@//ORACLE_HOST:ORACLE_PORT/SERVICE_NAME" SCHEMAS=BACKUP_SCHEMA_NAME DIRECTORY=DIRECTORY_ALIAS dumpfile=BACKUP_FILE_NAME NOLOGFILE=YES
```





where:
   - `ORACLE_HOST` – Oracle server address.
   - `ORACLE_PORT` – Oracle server port.
   - `SERVICE_NAME` – Oracle service name.
   - `DIRECTORY_ALIAS` – an alias for the directory where the backup copy will be placed.
   - `BACKUP_SCHEMA_NAME` – name of the schema for which the backup is made.
   - `BACKUP_SCHEMA_PASSWORD` – password for the schema for which the backup is made.
   - `BACKUP_FILE_NAME` – name of the file where the schema will be exported.

**As a result**, the expdp utility will create a backup copy of the `BACKUP_SCHEMANAME` schema that has the `BACKUP_FILE_NAME in the PATH_TO_BACKUP_DIRECTORY` directory.

Learn more about deploying the backup database: [Deploy Oracle Database for Creatio](https://academy.creatio.com/documents?id=2133).

## Back up PostgreSQL database [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase\#title-143-5 "Direct link to Back up PostgreSQL database")

To create a database backup, use the `pg_dump` utility. It is located in the software setup folder for PostgreSQL.

1.  Enter the data base connection password in the environment variable:



   - Windows
   - Linux

```js
set PGPASSWORD=#SysUserPassword#
```

```js
export PGPASSWORD=#SysUserPassword#
```

2.  Run the following command:





```js
"C:\\PostgreSQL\\pg_dump.exe" --host=#ServerIP# --port #ServerPort# --username #SysUserName# --format=c --blobs --verbose -clean -file=#BackupFilePath# #DatabaseName#
```





where
   - `ServerIP` – PostgreSQL server address.
   - `ServerPort` – PostgreSQL server port.
   - `SysUserName` – name of the PostgreSQL system user (you specify it when installing the PostgreSQL server).
   - `SysUserPassword` – password of the PostgreSQL system user (you specify it when installing the PostgreSQL server).
   - `BackupFilePath` – full path to the directory where the backup copy will be placed.
   - `DatabaseName` – name of the data base, whose backup to make.

**As a result**, the utility will create a database backup in the `BackupFilePath` directory.

Learn more about deploying the backup database: [Deploy PostgreSQL Database (Linux)](https://academy.creatio.com/documents?id=2121) and [Deploy PostgreSQL Database (Windows)](https://academy.creatio.com/documents?id=2134).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase\#see-also "Direct link to See also")

[Deploy database server](https://academy.creatio.com/docs/8.x/setup-and-administration/category/database-server)

[Compile an app on a web farm](https://academy.creatio.com/documents?id=2410)

[Update guide](https://academy.creatio.com/documents?id=2495)

- [Back up Microsoft SQL Server database](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase#title-143-3)
- [Back up Oracle Database](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase#title-143-4)
- [Back up PostgreSQL database](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase#title-143-5)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/backup-datadase#see-also)