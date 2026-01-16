<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server)** (8.3).

Version: 8.2All Creatio products

On this page

The ConnectionStrings.config file in the Creatio root directory stores the connection parameters of the database and external services for your application.

### Set up ConnectionStrings.config [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server\#title-258-1 "Direct link to Set up ConnectionStrings.config")

1. Go to the root directory of the Creatio application **~\\WebAppRoot\\Creatio**.
2. Open the ConnectionStrings.config file in a text editor.
3. Specify the connection parameters ( **connectionStrings**) of your site.

A sample ConnectionStrings.config file

```xml
<?xml version="1.0" encoding="utf-8"?>
    <connectionStrings>
    <add name="db" connectionString="Data Source=[Database server name]; Initial Catalog=[Database name]; Persist Security Info=True; MultipleActiveResultSets=True; Integrated Security=SSPI; Pooling = true; Max Pool Size = 100; Async = true" />
    <add name="redis" connectionString="host=[Redis server machine name];db=[Redis DB number];port=6379; maxReadPoolSize=10;maxWritePoolSize=500" /> <Integrated Security=SSPI" />
    <add name="defRepositoryUri" connectionString="" />
    <add name="defWorkingCopyPath" connectionString="%TEMP%\%WORKSPACE%" />
    <add name="defPackagesWorkingCopyPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\TerrasoftPackages" />
    <add name="clientUnitContentPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\ClientUnitSrc" />
    <add name="sourceControlAuthPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\Svn" />
    <add name="elasticsearchCredentials" connectionString="User=[ElasticSearch username]; Password=[ElasticSearch password];" />
</connectionStrings>
```

### Required ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server\#title-258-2 "Direct link to Required ConnectionStrings.config settings")

Creatio requires the database and caching server connection parameters for operation.

- **name="db"** manages the connection to the restored database.

You can see the database server name ( **Data Source**) in the authorization window while connecting to the server using Microsoft SQL Server Management Studio (Fig. 1).
Fig. 1 The SQL server authorization window

![Fig. 1 The SQL server authorization window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/modify_config_for_MSSQL/scr_setup_server_name.png)


The database name (Initial Catalog) must match the **Database** field value you specified when restoring the database.

By default, Creatio uses **Windows authentication** (Integrated Security) based on the SPPI interface to connect to the database server. To ensure successful connection to the database, specify the Windows user on whose behalf you will connect to the database server.





```xml
<add name="db" connectionString="Data Source=[Database server name]; Initial Catalog=[Database name]; Persist Security Info=True; MultipleActiveResultSets=True; Integrated Security=SSPI; Pooling = true; Max Pool Size = 100; Async = true" />
```









If you want to log in to the database server using the **Microsoft SQL user credentials**, create the credentials on the Microsoft SQL server and specify them in the ConnectionStrings.config file. Replace the **Integrated Security=SSPI** variable with the **User ID** and **Password** variables in the database connection string (add name="db"):





```xml
<add name="db" connectionString="Data Source=TSW\\MSSQL2014; Initial Catalog=7.10.2.1416_SalesEnterprise_Demo; Persist Security Info=True; MultipleActiveResultSets=True; User ID=Sup; Password=password; Pooling = true; Max Pool Size = 100; Async = true" />
```

- **name="redis"** manages the interaction with the Redis server.





```xml
<add name="redis" connectionString="host=[Redis server machine name];db=[Redis DB number];port=6379;
maxReadPoolSize=10;maxWritePoolSize=500" />
```


### Optional ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server\#title-258-3 "Direct link to Optional ConnectionStrings.config settings")

The external service connection parameters are optional. Fill them out only if your Creatio configuration requires it. For example, do that if you want to integrate the version control system.

- **tempDirectoryPath** is the path to the temporary directory the package installation mechanism requires:





```xml
<add name="tempDirectoryPath" connectionString=[Path to the temporary directory the package installation mechanism requires] />
```

- **defPackagesWorkingCopyPath** is the path to the working copy of Creatio user-made packages. Fill out this parameter only if you use the SVN version control system. The working copy contains user-made packages organized as directories and files. The built-in Creatio SVN client synchronizes the working copy with the repository of the SVN version control system. Set up this parameter when integrating the version control system. Creatio will use it only in the default development mode; i. e., if the file system development mode is disabled. The default value is a temporary directory, which the operating system may clear. We recommend specifying a custom directory. If you specify an existing Creatio directory, for example, .\\Terrasoft.WebApp\\Terrasoft.Configuration\\Pkg, that may cause compilation errors.





```xml
<add name="defPackagesWorkingCopyPath" connectionString=[Path to the working copy of user-made packages] />
```

- **sourceControlAuthPath** is the path to the authorization data of the built-in client of the SVN version control system (if used): The default value is a temporary directory, which the operating system may clear. If you use a version control system, we recommend specifying the path to a permanent directory in this parameter.





```xml
<add name="sourceControlAuthPath" connectionString=[Path to the authorization data of the version storage system (SVN)] />
```

- **Influx** manages the interaction with the site analytics collection service. Fill out this parameter only if you need to collect the functionality use analytics for debugging.





```xml
<add name="influx" connectionString="url=[Site analytics collection service address]; user=[User on whose behalf the connection is established]; password=[Password]; batchIntervalMs=5000" />
```

- **clientPerformanceLoggerServiceUri** manages the interaction with the logging service. Fill out this parameter only if you need to collect the data about how Creatio pages load.





```xml
<add name="clientPerformanceLoggerServiceUri" connectionString="[Logging service address] " />
```

- **messageBroker** manages the interaction with the RabbitMQ service. Fill out this parameter only if you need to set up horizontal load scaling using RabbitMQ.





```xml
<add name="messageBroker" connectionString="amqp://[MessageBroker username]:[Password] @[Address of the server where the service is deployed] /[Virtual server name] " />
```


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server\#see-also "Direct link to See also")

[Enable required Windows components](https://academy.creatio.com/documents?id=2081)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?id=2142)

[Set up WebSockets](https://academy.creatio.com/documents?id=2143)

[Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Set up ConnectionStrings.config](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server#title-258-1)
- [Required ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server#title-258-2)
- [Optional ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server#title-258-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server#see-also)