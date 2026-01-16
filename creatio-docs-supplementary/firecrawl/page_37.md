<!-- Source: page_37 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_oracle_database_for_creatio#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Install Oracle Database on the database server. Installation instructions are available in the [Oracle Database Online Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/index.html). The "sqlplus" and "impdp" utilities required for restoring the application database from backup are installed with Oracle Database.

note

Please refer to the [Oracle Database Online Documentation](https://docs.oracle.com/database/121/nav/portal_16.htm) for more details on Oracle Database clustering.

In Oracle Database, create two database users.

- A user with the " **admin**" role, who has maximum access privileges on the database server level. This user will restore the Creatio database from a backup file and assign access permissions.
- A user with the " **public**" role, whose permissions are limited. You will need this user to set up a secure connection to the restored Creatio database using Oracle authentication.

For more on creating users and access permissions on the database server, see [Oracle Database Online Documentation](https://docs.oracle.com/database/121/SQLRF/statements_8003.htm#SQLRF01503).

Download and unzip the [archive with the SQL scripts](https://academy.creatio.com/sites/default/files/documents/downloads/Oracle_restore_database_scripts.zip) that are used to restore the database from the Oracle backup file.

By default the Oracle DB backup file is located in the ~\\db folder with the Creatio executable files. If the backup file is located not on the Oracle server, it should be located in the network folder with general access.

To restore the database:

1. Open the CreateUser.sql and RecompileSchema.sql scripts in the editor and modify the following macros:

`YOUR_SCHEMA_NAME` – schema name.

`YOUR_SCHEMA_PASSWORD` – schema password.

`\your_server.com\Share` – path to the backup (\*.dmp file).

2. Open the backup file in a text editor, find and save the name of the used schema located before the ".SYS\_EXPORT\_SCHEMA" record (Fig. 1).
Fig. 1 The schema name in the backup file

![Fig. 1 The schema name in the backup file](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/deploy_oracle_database/chapter_setup_oracle_find_schema_name.png)

3. Remove the modified scripts on the Oracle server. To create a new schema, execute the following command from the folder with the scripts:





```sql
sqlplus.exe "SYS/SYS_PASSWORD@your_server.com:1521/YOUR_SERVICE_NAME AS SYSDBA" @CreateUser.sql
```





`SYS_PASSWORD` – a password for authorization on the Oracle server.

`your_server.com` – network address of the Oracle server.

`YOUR_SERVICE_NAME` – Oracle service name.

4. Run import of the DB backup copy in the created schema:





```sql
impdp "YOUR_SCHEMA_NAME/YOUR_SCHEMA_NAME@//your_server.com:1521/BPMBUILD"
    REMAP_SCHEMA=ORIGINAL_SCHEMA_NAME:YOUR_SCHEMA_NAME
    DIRECTORY=BACKUPDIR DUMPFILE=filename.dmp NOLOGFILE=YES
```





`YOUR_SCHEMA_NAME` – the name of the schema specified in the CreateUser.sql.

`your_server.com` – network address of the Oracle server.

`ORIGINAL_SCHEMA_NAME` – the name of the schema from the backup file (step 2).

5. Consistently run:





```sql
sqlplus.exe "YOUR_SCHEMA_NAME/YOUR_SCHEMA_PASSWORD@your_server.com:1521/YOUR_SERVICE_NAME"
    @tspkg_UtilitiesGlobalTypes.sql

sqlplus.exe "YOUR_SCHEMA_NAME/YOUR_SCHEMA_PASSWORD@your_server.com:1521/ YOUR_SERVICE_NAME"
    @RecompileSchema.sql
```


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_oracle_database_for_creatio\#see-also "Direct link to See also")

[Set up Creatio caching server](https://academy.creatio.com/documents?product=administration&ver=7&id=2135)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?product=administration&ver=7&id=2136)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=administration&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_oracle_database_for_creatio#see-also)