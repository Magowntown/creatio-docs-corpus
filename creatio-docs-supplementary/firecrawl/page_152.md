<!-- Source: page_152 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

The ConnectionStrings.config file in the Creatio root directory stores the connection parameters of the database and external services for your application.

### Set up ConnectionStrings.config [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql\#title-260-1 "Direct link to Set up ConnectionStrings.config")

1. Go to the root directory of the Creatio application **~\\WebAppRoot\\Creatio**.
2. Open the ConnectionStrings.config file in a text editor.
3. Specify the connection parameters ( **connectionStrings**).

A sample ConnectionStrings.config file

```xml
<?xml version="1.0" encoding="utf-8"?>
    <connectionStrings>
        <add name="db" connectionString="Server=[Database server name];Port=[Database server port];Database=[Database name];User ID=[PostgreSQL user that will connect to the database];password=[PostgreSQL user password];Timeout=500; CommandTimeout=400;MaxPoolSize=1024;" />
        <add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379;maxReadPoolSize=10;maxWritePoolSize=500" />
        <add name="redisSentinel" connectionString="sentinelHosts=localhost:26380,localhost:26381,localhost:26382;masterName=mymaster;scanForOtherSentinels=false;db=1;maxReadPoolSize=10;maxWritePoolSize=500" />
        <add name="defPackagesWorkingCopyPath" connectionString="%TEMP%\%APPLICATION%\%APPPOOLIDENTITY%\%WORKSPACE%\TerrasoftPackages" />
        <add name="tempDirectoryPath" connectionString="%TEMP%\%APPLICATION%\%APPPOOLIDENTITY%\%WORKSPACE%\" />
        <add name="sourceControlAuthPath" connectionString="%TEMP%\%APPLICATION%\%APPPOOLIDENTITY%\%WORKSPACE%\Svn" />
        <add name="elasticsearchCredentials" connectionString="User=[ElasticSearch username]; Password=[ElasticSearch password];" />
        <add name="influx" connectionString="url=http://10.0.7.161:30359; user=; password=; batchIntervalMs=5000" />
    </connectionStrings>
```

### Required ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql\#title-260-2 "Direct link to Required ConnectionStrings.config settings")

Creatio requires the database and caching server connection parameters for operation.

1. For the restored database ( **name="db"**).





```xml
<add name="db" connectionString="Server=[Database server name];Port=[Database server port];Database=[Database name];User ID=[PostgreSQL user that will connect to the database];password=[PostgreSQL user password];Timeout=500; CommandTimeout=400;MaxPoolSize=1024;" />
```

2. For Redis Server ( **name="redis"**):





```xml
<add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379;maxReadPoolSize=10;maxWritePoolSize=500" />
```


### Optional ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql\#title-260-3 "Direct link to Optional ConnectionStrings.config settings")

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
<add name="clientPerformanceLoggerServiceUri" connectionString="[Logging service address]" />
```

- **messageBroker** manages the interaction with the RabbitMQ service. Fill out this parameter only if you need to set up the horizontal load scaling using RabbitMQ.





```xml
<add name="messageBroker" connectionString="amqp://[MessageBroker username]:[Password] @[Address of the server where the service is deployed]/[Virtual server name]" />
```


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql\#see-also "Direct link to See also")

[Enable required Windows components](https://academy.creatio.com/documents?id=2081)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?id=2142)

[Set up WebSockets](https://academy.creatio.com/documents?id=2143)

[Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Set up ConnectionStrings.config](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql#title-260-1)
- [Required ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql#title-260-2)
- [Optional ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql#title-260-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/modify_connectionstrings_config_for_postgresql#see-also)