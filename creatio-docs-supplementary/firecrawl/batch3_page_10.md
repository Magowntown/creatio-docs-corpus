<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-windows/modify-web-config)** (8.3).

Version: 8.2All Creatio products

On this page

Generate a unique `machineKey` value for your Creatio application. To do this:

1. Download the PowerShell script. [Download the script](https://academy.creatio.com/sites/default/files/documents/downloads/UpdateMachineKey.zip).

2. Run the PowerShell console as an administrator.

3. Specify the path to the root Creatio directory in the PowerShell terminal and run the script. Example of the command to run:





```cli
.\UpdateMachineKey.ps1 "[Path to the root Creatio directory]"
```


As a result, the script will generate a unique `machineKey` value in Web.config files located in the root Creatio directory and the Terrasoft.WebApp directory.

## Additional Web.config setup for Oracle [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config\#title-2394-1 "Direct link to Additional Web.config setup for Oracle")

After you set up the database connection parameters in the ConnectionStrings.config file for the Oracle database, set up the Web.config configuration file that includes certain configuration parameters required for Creatio to operate as intended.

To set up Web.config:

1. Ensure the Creatio website can access the configuration parameters described in the ConnectionStrings.config configuration file. To do this, open the Web.config configuration file in the root Creatio directory and set the `currentSchemaName` attribute of the `general` parameter in the `db` section to the name of the schema specified in the ConnectionStrings.config configuration file.





```xml
<configuration>
       ...
       <terrasoft>
           <db>
               <general ... currentSchemaName="SOME_SCHEMA_NAME_OF_ORACLE_DATABASE" />
           </db>
       </terrasoft>
       ...
</configuration>
```









where `currentSchemaName` is the name of the Oracle database schema.

2. Save the changes.


### Enable the Managed ODAC 12 library [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config\#title-3966-1 "Direct link to Enable the Managed ODAC 12 library")

Make sure that you are using Creatio version 8.0 Atlas or later. If you are using an earlier version, update Creatio. To do this, follow the [update guide](https://academy.creatio.com/node/143).

To **enable the Managed ODAC 12 library**:

1. Check the Oracle 19c database connector the website uses.





```xml
<configuration>
       ...
       <system.data>
           <DbProviderFactories>
               <add name="Oracle.ManagedDataAccess, Managed Driver" invariant="Oracle.ManagedDataAccess.Client" description="Oracle Data Provider for .NET, Managed Driver" type="Oracle.ManagedDataAccess.Client.OracleClientFactory, Oracle.ManagedDataAccess"/>
           </DbProviderFactories>
       </system.data>
       ...
</configuration>
```

2. Back up the Web.config configuration file in the root Creatio directory.

3. Set up the interaction between the Creatio website and database via the Managed ODAC 12 library. To do this, set the `executorType` parameter in the Web.config configuration file to `Terrasoft.DB.Oracle.OracleManagedExecutor, Terrasoft.DB.Oracle`:





```xml
<configuration>
       ...
       <terrasoft>
           <db>
               <general ... executorType="Terrasoft.DB.Oracle.OracleManagedExecutor, Terrasoft.DB.Oracle" ... />
           </db>
       </terrasoft>
</configuration>
```









where `executorType` is the library that manages the Creatio database.

4. Set up the interaction between the scheduler and database tables via the Managed ODAC 12 library. To do this, set the `quartz.dataSource.SchedulerDb.provider` key in the Web.config configuration file to `OracleManagedProvider`:





```xml
<configuration>
       ...
       <quartzConfig defaultScheduler="BPMonlineQuartzScheduler">
           <quartz isActive="true">
               ...
               <add key="quartz.dataSource.SchedulerDb.provider" value="OracleManagedProvider" />
           </quartz>
       </quartzConfig>
</configuration>
```









where `quartz.dataSource.SchedulerDb.provider` is the key that enables the scheduler to interact with database tables.

5. Run Creatio and check the functionality in operation. If you notice issues, restore the Web.config configuration file from backup and repeat the setup.

6. Repeat the setup in the production environment or transfer changes to the production environment. Learn more in developer documentation: [Environments](https://academy.creatio.com/documents?id=15201&anchor=title-2124-3).


### Update the Oracle DBMS to version 19c [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config\#title-3966-1 "Direct link to Update the Oracle DBMS to version 19c")

To update the Creatio Oracle DBMS to version 19c, follow the [official vendor documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/index.html).

As a result, your Creatio application will use Oracle 19c DBMS.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config\#see-also "Direct link to See also")

[Enable required Windows components](https://academy.creatio.com/documents?id=2081)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?id=2142)

[Set up WebSockets](https://academy.creatio.com/documents?id=1631)

[Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

[Official Oracle 19c documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19)

[Environments (developer documentation)](https://academy.creatio.com/documents?id=15201)

[Update guide](internal:/node/143)

- [Additional Web.config setup for Oracle](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config#title-2394-1)
  - [Enable the Managed ODAC 12 library](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config#title-3966-1)
  - [Update the Oracle DBMS to version 19c](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config#title-3966-1)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-web-config#see-also)