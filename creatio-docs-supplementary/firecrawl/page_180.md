<!-- Source: page_180 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Important

Support for .NET Core 3.1 will be retired in Creatio version 8.0.9. We recommend moving to .NET 6 when updating Creatio to version 8.0.8.

## Prepare the setup files [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#title-263-1 "Direct link to Prepare the setup files")

Creatio setup files come as a zip archive. To unpack the archive, run:

```cli
unzip -d /path/to/application/directory/ CREATIO_ARCHIVE_NAME.zip
```

where **/path/to/application/directory/** is the directory to which to extract the files. We recommend unpacking the archive to the current directory:

```cli
unzip creatio_archive_name.zip
```

Where **creatio\_archive\_name.zip** is the name of the Creatio setup archive.

note

If running the unzip command results in the "command not found" error, install the \*.zip file de-archiver: `sudo apt-get install unzip`.

## Set up ConnectionStrings.config [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#title-263-2 "Direct link to Set up ConnectionStrings.config")

The ConnectionStrings.config file in the Creatio root directory stores the connection parameters of the database and external services for your application.

### Edit the ConnectionStrings.config file [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#title-263-5 "Direct link to Edit the ConnectionStrings.config file")

1. Go to the root directory of the Creatio application **~\\WebAppRoot\\Creatio**.
2. Open the ConnectionStrings.config file in a text editor.
3. Specify the **connectionStrings** connection parameters of your site.

A sample ConnectionStrings.config file

```xml
<?xml version="1.0" encoding="utf-8"?>
    <connectionStrings>
        <add name="db" connectionString="Server=[Database server name];Port=31436;Database=[Database name]; User ID=[Name of the user who will connect to the DB];password=[Password of the user who will connect to the DB];Timeout=500; CommandTimeout=400;MaxPoolSize=1024;" />
        <add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379" />
        <add name="tempDirectoryPath" connectionString="%TEMP%/%USER%/%APPLICATION%" />
        <add name="influx" connectionString="url=[Address of the analytics collection service]; user=; password=; batchIntervalMs=5000" />
        <add name="clientPerformanceLoggerServiceUri" connectionString="[Logging service address]" />
        <add name="messageBroker" connectionString="amqp://[MessageBroker username]:[Password]@[Address of the server where the service is deployed]/[Virtual server name]" />
    </connectionStrings>
```

### Required ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#title-263-6 "Direct link to Required ConnectionStrings.config settings")

Creatio requires the database and caching server connection parameters for operation.

- **db** manages the database connection. Configure the path to the database to connect and the authorization method on the database server in this parameter.





```xml
<add name="db" connectionString="Server=[Database server name];Port=31436;Database=[Database name]; User ID=[Name of the user who will connect to the DB];password=[Password of the user who will connect to the DB];Timeout=500; CommandTimeout=400;MaxPoolSize=1024;" />
```

- **redis** manages the interaction with the Redis server:





```xml
<add name="redis" connectionString="host=[Machine name];db=[Redis DB number];port=6379; "/>
```











Important





The Redis database number must be unique for each Creatio site.


### Optional ConnectionStrings.config settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#title-263-7 "Direct link to Optional ConnectionStrings.config settings")

The external service connection parameters are optional. Fill them out only if your Creatio configuration requires it. For example, do that if you want to collect the site analytics.

- **tempDirectoryPath** is the path to the temporary directory the package installation mechanism requires:





```xml
<add name="tempDirectoryPath" connectionString=[Path to the temporary directory the package installation mechanism requires] />
```

- **Influx** manages the interaction with the site analytics collection service. Fill out this parameter only if you need to collect the functionality use analytics for debugging.





```xml
<add name="influx" connectionString="url=[Site analytics collection service]; user=[User on whose behalf the connection is established]; password=[Password]; batchIntervalMs=5000" />
```

- **clientPerformanceLoggerServiceUri** manages the interaction with the logging service. Fill out this parameter only if you need to collect the data about how Creatio pages load.





```xml
<add name="clientPerformanceLoggerServiceUri" connectionString="[Logging service address] " />
```

- **messageBroker** manages the interaction with the RabbitMQ service. Fill out this parameter only if you need to set up the horizontal load scaling using RabbitMQ.





```xml
<add name="messageBroker" connectionString="amqp://[MessageBroker username]:[Password] @[Address of the server where the service is deployed]/[Virtual server name] " />
```


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux\#see-also "Direct link to See also")

[Deploy PostgreSQL database (Linux)](https://academy.creatio.com/documents?id=2121)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Prepare the setup files](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#title-263-1)
- [Set up ConnectionStrings.config](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#title-263-2)
  - [Edit the ConnectionStrings.config file](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#title-263-5)
  - [Required ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#title-263-6)
  - [Optional ConnectionStrings.config settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#title-263-7)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/net_core_server/prepare_creatio_net_core_setup_files_on_linux#see-also)