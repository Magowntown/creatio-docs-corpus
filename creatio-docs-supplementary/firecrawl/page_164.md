<!-- Source: page_164 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_ms_sql_database_for_creatio#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Install Microsoft SQL Server Management Studio on the database server. Installation instructions are available in the [Microsoft SQL Server documentation](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15).

note

Microsoft SQL has been tested for deployment of clustered Creatio databases. Using Microsoft SQL Always On availability groups is a recommended method of setting up a high availability configuration. For more information on Microsoft SQL Always On technology, please refer to the [Microsoft SQL documentation](https://docs.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server?view=sql-server-ver15).

In Microsoft SQL Server Management Studio, create two database users.

- A user with the " **sysadmin**" role, who has maximum access privileges on the database server level. This user will restore the Creatio database from a backup file and assign access permissions.
- A user with the " **public**" role, whose permissions are limited. You will need this user to set up a secure connection to the restored Creatio database using Microsoft SQL authentication.

For more on creating users and access permissions on the database server, see [Microsoft SQL Server documentation](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-user?view=sql-server-ver15).

To restore a database:

1. Authenticate in Microsoft SQL Server Management Studio as a " **sysadmin**" user.

2. Click the **Databases** catalog and select the **Restore Database** option from the context menu (Fig. 1).
Fig. 1 Selecting database backup command

![Fig. 1 Selecting database backup command](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/deploy_mssql_database/scr_setup_restore_database.png)

3. In the **Restore Database** window:
1. Specify the name of the database in the **Database** field;

2. Specify the **Device** checkbox and specify the path to the database backup copy file. The database backup file is supplied together with executable files and is located in the **~\\db** folder (Fig. 2).
      Fig. 2 Selecting database backup

      ![Fig. 2 Selecting database backup](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/deploy_mssql_database/scr_setup_restore_database_data.png)
4. Specify a folder on the database server where the Creatio database will be restored. Creating a folder to restore database files is required beforehand, as the SQL Server is not permitted to create directories.
1. Go to the **Files** tab.

2. In the **Restore the database files as** area, select the **Relocate all files and folders** checkbox.

3. Specify paths to the folders where SQL Management Studio will save the **TS\_Data.mdf** and **TS\_Log.ldf** files (Fig. 3).
      Fig. 3 Specifying the names and paths to TS\_Data.mdf and TS\_Log.ldf files.

      ![Fig. 3 Specifying the names and paths to TS_Data.mdf and TS_Log.ldf files.](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/deploy_mssql_database/scr_setup_restore_database_options.png)
5. Click the **OK** button and wait for the database restore process to be finished.

6. Enable connection for the **public** Microsoft SQL user who Creatio will use to access the database.
1. Locate the restored Creatio database in Microsoft SQL Server Management Studio.
2. Click the **Security** tab.
3. Add the user to the **Users** list.
4. Click **Membership** and specify the **db\_owner**, which will grant the user full access to the restored Creatio database.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_ms_sql_database_for_creatio\#see-also "Direct link to See also")

[Set up Creatio caching server (Redis)](https://academy.creatio.com/documents?product=administration&ver=7&id=2135)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?product=administration&ver=7&id=2136)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=administration&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_ms_sql_database_for_creatio\#resources "Direct link to Resources")

[Tech Hour - Installing Local instance of Creatio](https://www.youtube.com/watch?v=lf-yWsJ4p0Q&list=PLnolcTT5TeE3v8WGd3VqlZSd2D02GWSGa&index=3)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_ms_sql_database_for_creatio#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_ms_sql_database_for_creatio#resources)