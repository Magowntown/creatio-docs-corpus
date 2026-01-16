<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/creatio-maintenance/process-complex-database-queries-faster)** (8.3).

Version: 8.1

On this page

Some Creatio database queries take a long time to process, which might affect page loading or task completion time significantly. Such queries are usually called "heavy." They include:

- complex filters in pages and dynamic folders
- complex analytical selections in section dashboards
- complex custom queries implemented using development tools

You can accelerate the processing of heavy queries by forwarding them to a read-only database replica. This will reduce the load on the main database significantly and free up resources for the activity of users and the operation of other Creatio elements.

To set up the redirection of heavy queries, take the following steps:

1. Create a read-only database replica.
2. Configure access to the database replica in Creatio.

## Step 1. Create a database replica [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster\#title-2194-1 "Direct link to Step 1. Create a database replica")

The procedure to create a database replica is DBMS-specific. Learn more about the process in vendor documentation:

- [Create a database replica in PostgreSQL](https://www.postgresql.org/docs/current/warm-standby.html).
- [Create a database replica in Microsoft SQL](https://docs.microsoft.com/en-us/sql/relational-databases/replication/sql-server-replication?view=sql-server-ver15).
- [Create a database replica in Oracle](https://docs.oracle.com/cd/B19306_01/server.102/b14228/config_simple.htm#STREP056).

## Step 2. Set up redirection of heavy queries [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster\#title-2194-2 "Direct link to Step 2. Set up redirection of heavy queries")

1. **Set up redirection** of heavy queries to the database replica. Perform the setup in the Terrasoft.WebHost.dll.config file for **Creatio .NET Core and .NET 6** and in the web.config file for Creatio **NET Framework**.
1. Select the UseQueryKinds checkbox.





      ```xml
      <add key="UseQueryKinds" value="true" />
      ```

2. Add the replicaConnectionStringName="db\_Replica" value to the db general parameter.



      - For Microsoft SQL
      - For PostgreSQL

```xml
<general connectionStringName="db" replicaConnectionStringName="db_Replica" securityEngineType="Terrasoft.DB.MSSql.MSSqlSecurityEngine, Terrasoft.DB.MSSql" executorType="Terrasoft.DB.MSSql.MSSqlExecutor, Terrasoft.DB.MSSql" engineType="Terrasoft.DB.MSSql.MSSqlEngine, Terrasoft.DB.MSSql" metaEngineType="Terrasoft.DB.MSSql.MSSqlMetaEngine, Terrasoft.DB.MSSql" metaScriptType="Terrasoft.DB.MSSql.MSSqlMetaScript, Terrasoft.DB.MSSql" typeConverterType="Terrasoft.DB.MSSql.MSSqlTypeConverter, Terrasoft.DB.MSSql" enableRetryDBOperations="false" retryDBOperationFactoryType="Terrasoft.DB.MSSql.MSSqlRetryOperationFactory, Terrasoft.DB.MSSql" binaryPackageSize="1048576" currentSchemaName="dbo" enableSqlLog="false" sqlLogQueryTimeElapsedThreshold="5000" sqlLogRowsThreshold="100" useOrderNullsPosition="false" maxEntitySchemaNameLength="128" />
```

```xml
<general connectionStringName="db" replicaConnectionStringName="db_Replica" maxEntitySchemaNameLength="128" useOrderNullsPosition="false" sqlLogRowsThreshold="100" sqlLogQueryTimeElapsedThreshold="5000" enableSqlLog="false" currentSchemaName="public" binaryPackageSize="1048576" typeConverterType="Terrasoft.DB.PostgreSql.PostgreSqlTypeConverter, Terrasoft.DB.PostgreSql" metaScriptType="Terrasoft.DB.PostgreSql.PostgreSqlMetaScript, Terrasoft.DB.PostgreSql" metaEngineType="Terrasoft.DB.PostgreSql.PostgreSqlMetaEngine, Terrasoft.DB.PostgreSql" engineType="Terrasoft.DB.PostgreSql.PostgreSqlEngine, Terrasoft.DB.PostgreSql" maxAnsiJoinCount="0" isCaseInsensitive="true" executorType="Terrasoft.DB.PostgreSql.PostgreSqlExecutor, Terrasoft.DB.PostgreSql" securityEngineType="Terrasoft.DB.PostgreSql.PostgreSqlSecurityEngine, Terrasoft.DB.PostgreSql"/>
```
2. **Configure access** to the database replica in Creatio. To do this, add the db\_Replica parameter to the ConnectionStrings.config file:



   - For Microsoft SQL
   - For PostgreSQL
   - For Oracle

```xml
<add name="db_Replica" connectionString="Data Source=[ Database server name ]; Initial Catalog=[ Database name ]; Persist Security Info=True; MultipleActiveResultSets=True; Integrated Security=SSPI; Pooling = true; Max Pool Size = 100; Async = true" />
```

```xml
<add name="db_Replica" connectionString="Server=[ Database server name ];Port=[ Database server port ];Database=[ Database name ];User ID=[ PostgreSQL user that connects to the database ];password=[ PostgreSQL user password ];Timeout=500; CommandTimeout=400;MaxPoolSiz>
```

```xml
<add name="db_Replica" connectionString="Data Source=(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST =[Database server name])(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME =[Oracle service name]) (SERVER = DEDICATED)));User Id=[Schema name];Password=[Schema password];Statement Cache Size = 300" />
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster\#see-also "Direct link to See also")

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

[General Creatio deployment procedure](https://academy.creatio.com/documents?id=1263)

[Set up a dedicated query pool (developer documentation)](https://academy.creatio.com/documents?id=15261)

- [Step 1. Create a database replica](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster#title-2194-1)
- [Step 2. Set up redirection of heavy queries](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster#title-2194-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/process-complex-database-queries-faster#see-also)