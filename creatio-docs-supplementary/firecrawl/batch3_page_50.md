<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.2All Creatio products

On this page

The ConnectionStrings.config file in the Creatio root directory stores the connection parameters of the database and external services for your application.

### Set up ConnectionStrings.config [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database\#title-259-1 "Direct link to Set up ConnectionStrings.config")

1. Go to the root directory of the Creatio application **~\\WebAppRoot\\Creatio**.
2. Open the ConnectionStrings.config file in a text editor.
3. Specify the connection parameters ( **connectionStrings**).

A sample ConnectionStrings.config file

```xml
<?xml version="1.0" encoding="utf-8"?>
    <connectionStrings>
        <add name="db" connectionString="Data Source=(DESCRIPTION =
 (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST =[Database server name])(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME =[Oracle service name]) (SERVER = DEDICATED)));User Id=[Schema name];Password=[Schema password];Statement Cache Size = 300" />
        <add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379;maxReadPoolSize=10;maxWritePoolSize=500" />
        <add name="defRepositoryUri" connectionString="" />
        <add name="defWorkingCopyPath" connectionString="%TEMP%\%WORKSPACE%" />
        <add name="defPackagesWorkingCopyPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\TerrasoftPackages" />
        <add name="clientUnitContentPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\ClientUnitSrc" />
        <add name="sourceControlAuthPath" connectionString="%TEMP%\%APPLICATION%\%WORKSPACE%\Svn" />
    </connectionStrings>
```

### Required ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database\#title-259-2 "Direct link to Required ConnectionStrings.config settings")

Creatio requires the database and caching server connection parameters for operation.

- **name="db"** manages the connection to the restored database, where:


  - **Database server name** is the network address of the database server.
  - **Oracle service name** is the service name.
  - **Schema name** is the schema name of the restored database.
  - **Schema password** is the schema password of the restored database.

```xml
<add name="db" connectionString="Data Source=(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST =[Database server name])(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME =[Oracle service name]) (SERVER = DEDICATED)));User Id=[Schema name];Password=[Schema password];Statement Cache Size = 300" />
```

- **name="redis"** manages the interaction with the Redis server.





```xml
<add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379; maxReadPoolSize=10;maxWritePoolSize=500" />
```


### Optional ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database\#title-259-3 "Direct link to Optional ConnectionStrings.config settings")

The external service connection parameters are optional. Fill them out only if your Creatio configuration requires it. For example, do that if you want to integrate the version control system.

- **tempDirectoryPath** is the path to the temporary directory the package installation mechanism requires:





```xml
<add name="tempDirectoryPath" connectionString=[Path to the temporary directory the package installation mechanism requires] />
```

- **defPackagesWorkingCopyPath** is the path to the working copy of Creatio user-made packages. Fill out this parameter only if you use the SVN version control system. The working copy contains user-made packages arranged as directories and files. The built-in Creatio SVN client synchronizes the working copy with the repository of the SVN version control system. Set up this parameter when integrating the version control system. Creatio will use it only in the default development mode; i. e., if the file system development mode is disabled. The default value is a temporary directory, which the operating system may clear. We recommend specifying a custom directory. If you specify an existing Creatio directory, for example, .\\Terrasoft.WebApp\\Terrasoft.Configuration\\Pkg, that may cause compilation errors.





```xml
<add name="defPackagesWorkingCopyPath" connectionString=[Path to the working copy of user-made packages] />
```

- **sourceControlAuthPath** is the path to the authorization data of the built-in client of the SVN version control system (if used): The default value is a temporary directory, which the operating system may clear. If you use a version control system, we recommend specifying the path to a permanent directory in this parameter.





```xml
<add name="sourceControlAuthPath" connectionString=[Path to the authorization data of the version storage system (SVN)] />
```


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database\#see-also "Direct link to See also")

[Enable required Windows components](https://academy.creatio.com/documents?id=2081)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?id=2142)

[Set up WebSockets](https://academy.creatio.com/documents?id=2143)

[Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Set up ConnectionStrings.config](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database#title-259-1)
- [Required ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database#title-259-2)
- [Optional ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database#title-259-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-oracle-database#see-also)