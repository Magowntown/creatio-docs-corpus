<!-- Source: page_94 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Identity Service implements OAuth 2.0 protocol to securely authorize third-party apps and web services you integrate with Creatio. If you use Creatio **in the cloud**, contact Creatio support to set up the Identity Service for integrated applications.

General procedure to set up the Identity Service for Creatio **on-site**:

1. Install the Identity Service. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-1)
2. Make sure the Identity Service is running. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-7)

## 1\. Install the Identity Service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#title-2002-1 "Direct link to 1. Install the Identity Service")

This is a one-time procedure. Before you install the Identity Service, deploy the database and Creatio application servers.

You can install the Identity Service in multiple ways:

- Using IIS. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-5)
- Using Docker. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-6)

### Install the Identity Service using IIS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#title-2002-5 "Direct link to Install the Identity Service using IIS")

Install the Identity Service into the Creatio application server. Each Creatio instance needs an individual Identity Service.

To install the Identity Service using IIS:

01. **Install additional components**.
    For Creatio version 8.0.8 and later







    .NET 6 Runtime. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)



    .NET 6 Hosting Bundle. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-6.0.14-windows-hosting-bundle-installer)







    For Creatio version 7.16.4-8.0.7







    .NET Core runtime 2.2. [Download the install file](https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-2.2.207-windows-x64-installer)



    .NET Core Hosting Bundle. [Download the install file](https://dotnet.microsoft.com/download/dotnet-core/thank-you/runtime-aspnetcore-3.1.8-windows-hosting-bundle-installer)

02. **Restart the IIS**.

03. **Extract the IdentityService.zip archive** to an arbitrary directory in the root Creatio directory. For example, "IdentityService."

04. **Add the Identity Service application pool** to the IIS. Use dedicated application pool for every Creatio instance.


    1. Open the **Application Pools** section in the **Connections** area of the IIS.

    2. Select **Add Application Pool...** in the **Actions** area (Fig. 1). This opens the **Add Application Pool** window.
       Fig. 1 Add the pool to the IIS

       ![Fig. 1 Add the pool to the IIS](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/add_pool.png)

    3. Fill out the settings.



       | Setting | Setting value |
       | --- | --- |
       | Name | Must be unique. For example, "IDServicePool." |
       | .NET CLR Version | No Managed Code |
       | Managed pipeline mode | Integrated |

    4. Save the changes.


As a result, the "IDServicePool" pool will be added (Fig. 2).
Fig. 2 Identity Service pool

![Fig. 2 Identity Service pool](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/identity_service_pool.png)

05. **Set up access** to the application pool (optional for development environment). By default, the Windows user accesses the application pool.
    1. Select "IDServicePool" in the **Application Pools** area.

    2. Click ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/details_button.png) in the **Identity** setting of the **Advanced Settings** window (Fig. 3). This opens the **Application Pool Identity** window.
       Fig. 3 Set up access

       ![Fig. 3 Set up access](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/identity_service_pool_access.png)

    3. Select the **Custom account** checkbox and click **Set...** (Fig. 4). This opens the **Set Credentials** window.
       Fig. 4 Add a new user

       ![Fig. 4 Add a new user](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/add_a_new_user.png)

    4. Fill out the **User name**, **Password**, **Confirm password** user settings.

    5. Save the changes.
06. **Create the Identity Service website** in the IIS.


    1. Click **Sites** → **Add Website** in the **Connections** area of the IIS. This opens the **Add Website** window.

    2. Fill out the website settings.



       | Setting | Setting value |
       | --- | --- |
       | Site name | An arbitrary website name. For example, "IDServiceWebsite." |
       | Application pool | Click **Select...** and select the "IDServicePool" in the **Application pool** setting. |
       | Physical path | The path to the root Identity Service directory. |
       | Port | The port for the Identity Service. Must be unique. For example, "8090." |

    3. Save the changes.


As a result, the website for Identity Service will be created (Fig. 5).
Fig. 5 Website for Identity Service

![Fig. 5 Website for Identity Service](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/website_for_identity_service.png)

07. **Connect the website** to your Creatio DBMS.
    1. Open the appsettings.json file in the root Identity Service directory.

    2. Modify the file parameters.



       | Parameter | Parameter value |
       | --- | --- |
       | DbProvider | "MsSqlServer" or "Postgres" |
       | DatabaseConnectionString | Use the same connection string you specified in the `connectionString` attribute of the ConnectionStrings.config file. Use escaped characters. |


       The user that connects to the database must have permissions to create and update the tables.

       If you need to connect the Identity Service to Creatio that uses **Oracle DBMS**, deploy an additional PostgreSQL or Microsoft SQL database instance.

    3. Save the changes.
08. Set up the Identity Service **system client**.
    1. Open the appsettings.json file in the root Identity Service directory.

    2. Modify the file parameters. The Identity Service uses these values to interact with Creatio. All parameters support uppercase and lowercase letters, numbers, and special characters, for example, brackets or punctuation marks.



       | Parameter | Parameter value | Requirements for parameter value |
       | --- | --- | --- |
       | ClientId | An arbitrary client ID. For example, "IdServiceUser." | 16 characters |
       | ClientName | An arbitrary client name. For example, "MyIdentityServiceApp." | Any number of characters |
       | Secrets | An arbitrary client secret. For example, "ItIsMyPasswordForIdentityService." | 32 characters |




       appsettings.json file





       ```json
       "[{\"ClientId\":\"SOME_CLIENT_ID\",\"ClientName\":\"SOME_CLIENT_NAME\",\"Secrets\":[\"SOME_CLIENT_SECRET\"],\"AllowedGrantTypes\":[\"implicit\",\"client_credentials\"],\"RedirectUris\":[\"http://localhost:8090\",\"http://localhost:8090/lib\",\"http://localhost:8090/lib/\"],\"PostLogoutRedirectUris\":[\"http://localhost:8090\"],\"IdentityTokenLifetime\": 300,\"AccessTokenLifetime\": 3600,\"Properties\": {\"AllowedQueryParameters\": \"[\\\"invitationHash\\\",\\\"targetSubject\\\"]\"},\"AllowedScopes\": [\"register_own_resource\", \"get_resource_list\", \"get_client_info\", \"find_clients\", \"remove_client\", \"update_client\", \"add_registrar_client\", \"IdentityServerApi\"]}]",
       ```

    3. Save the changes.
09. Set up the **access to openssl.pfx certificate**.
    1. Open the appsettings.json file in the root Identity Service directory.
    2. Specify the full path to openssl.pfx certificate from the root Identity Service directory in the `X509CertificatePath` parameter. Use escaped characters.
    3. Save the changes.
10. Switch the Identity Service to **HTTPS** (optional for development environment). The setup process is similar to switching Creatio to HTTPS. Instructions: [Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632).

11. Set up the Identity Service **logging**. Enable logging to verify that the Identity Service operates as expected. For optimal performance, enable logging only while testing and debugging.
    1. Open the web.config file in the root Identity Service directory.

    2. Set the `stdoutLogEnabled` parameter to "true."

    3. Specify the directory to store the Identity Service logs in the `stdoutLogFile` parameter. You can leave default parameter value. The directory will be created automatically when you first launch the IdentityService.dll library.

    4. Save the changes.

    5. Open the appsettings.json file in the root Identity Service directory.

    6. Configure the log level.



       appsettings.json file





       ```json
       "Logging": {
         "LogLevel": {
           "Default": "Debug"
         }
       }
       ```









       Specify the log level based on your business goals. Learn more: [Define the log rules](https://academy.creatio.com/documents?id=15181&anchor=title-2121-4) (developer documentation).

    7. Save the changes.

**As a result**, you will have the application pool and website for Identity Service.

### Install the Identity Service using Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#title-2002-6 "Direct link to Install the Identity Service using Docker")

Since Creatio version 8.0.8, you can install the Identity Service using Docker. If you use Creatio version 7.16.4-8.0.7, install the Identity Service using IIS. Instructions: [Install the Identity Service using IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-5).

To install the Identity Service using Docker:

1. **Extract the IdentityService.zip archive** to an arbitrary directory in the root Creatio directory. For example, "IdentityService."

2. **Connect the website** to your Creatio DBMS. You can do this in multiple ways:


   - Modify the appsettings.json file in the Identity Service root directory before building.
   - Modify the Dockerfile-OAuth file and add environment variables using the ENV directive. For example, specify "Postgres" in the `ENV DbProvider` parameter. The parameter value will be set when the container starts.
   - Specify the environment variables when running the container. For example, use the `docker run --env=DbProvider=Postgres` command.

Regardless of the chosen method, configure the following parameters:

| Parameter | Parameter value |
| --- | --- |
| DbProvider | "MsSqlServer" or "Postgres" |
| MsSqlConnection or PostgresConnection | Use the same connection string you specified in the `connectionString` attribute of the ConnectionStrings.config file. |

The user that connects to the database must have permissions to create and update the tables.

If you need to connect the Identity Service to Creatio that uses **Oracle DBMS**, deploy an additional PostgreSQL or Microsoft SQL database instance.

3. Set up the Identity Service **system client**. To do this, modify the file parameters. The Identity Service uses these values to interact with Creatio. All parameters support uppercase and lowercase letters, numbers, and special characters, for example, brackets or punctuation marks.



| Parameter | Parameter value | Requirements for parameter value |
| --- | --- | --- |
| ClientId | An arbitrary client ID. For example, "IdServiceUser." | 16 characters |
| ClientName | An arbitrary client name. For example, "MyIdentityServiceApp." | Any number of characters |
| Secrets | An arbitrary client secret. For example, "ItIsMyPasswordForIdentityService." | 32 characters |




Example that sets up the Identity Service system client





```json
"[{\"ClientId\":\"SOME_CLIENT_ID\",\"ClientName\":\"SOME_CLIENT_NAME\",\"Secrets\":[\"SOME_CLIENT_SECRET\"],\"AllowedGrantTypes\":[\"implicit\",\"client_credentials\"],\"RedirectUris\":[\"http://localhost:8090\",\"http://localhost:8090/lib\",\"http://localhost:8090/lib/\"],\"PostLogoutRedirectUris\":[\"http://localhost:8090\"],\"IdentityTokenLifetime\": 300,\"AccessTokenLifetime\": 3600,\"Properties\": {\"AllowedQueryParameters\": \"[\\\"invitationHash\\\",\\\"targetSubject\\\"]\"},\"AllowedScopes\": [\"register_own_resource\", \"get_resource_list\", \"get_client_info\", \"find_clients\", \"remove_client\", \"update_client\", \"add_registrar_client\", \"IdentityServerApi\"]}]",
```

4. Configure the **Redis connection**. The `RedisConnection` parameter stores the "machineKey" value to prevent spoofing during runtime. Leave the `RedisConnection` parameter blank if additional security settings for the Identity Service are not required.

5. **Build the Docker image**. To do this, run the `docker build -t creatio-identity-service -f ./Dockerfile-OAuth .` command.

6. **Run the container** using the following command:





```cli
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
   --env=ASPNETCORE_URLS=http://+:80 --env=DOTNET_RUNNING_IN_CONTAINER=true
   --env=DOTNET_VERSION=6.0.15 --env=ASPNET_VERSION=6.0.15 --workdir=/app
   -p 80:80 -d creatio-identity-service:latest
```

7. Switch the Identity Service to **HTTPS**.
1. Obtain a digital certificate from the certification center. Instructions: [Windows using Linux containers](https://learn.microsoft.com/en-us/aspnet/core/security/docker-https?view=aspnetcore-7.0#windows-using-linux-containers) (vendor documentation).

2. Run the following command:





      ```cli
      docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      -e ASPNETCORE_URLS="https://+;http://+" -e ASPNETCORE_HTTPS_PORT=443
      -e DOTNET_RUNNING_IN_CONTAINER=true -e DOTNET_VERSION=6.0.15
      -e ASPNET_VERSION=6.0.15 -e ASPNETCORE_Kestrel__Certificates__Default__Password=SOME_CERTIFICATE_PASSWORD
      -e ASPNETCORE_Kestrel__Certificates__Default__Path=/https/aspnetapp.pfx
      -v %USERPROFILE%\.aspnet\https:/https/ --workdir=/app -p SOME_HTTP_PORT:80 -p SOME_HTTPS_PORT:443
      -d creatio-identity-service:latest
      ```











      | Parameter | Parameter value | Parameter description |
      | --- | --- | --- |
      | -e ASPNETCORE\_URLS | https://+;http://+ | Environment variable that switches the Identity Service to HTTPS |
      | -e ASPNETCORE\_HTTPS\_PORT | 443 | Environment variable that sets the port number for HTTPS |
      | -e DOTNET\_RUNNING\_IN\_CONTAINER | true | Variables for working via .NET |
      | -e DOTNET\_VERSION | 6.0.15 |
      | -e ASPNET\_VERSION | 6.0.15 |
      | -e ASPNETCORE\_Kestrel\_\_Certificates\_\_Default\_\_Password | SOME\_CERTIFICATE\_PASSWORD | Password for the openssl.pfx certificate |
      | -e ASPNETCORE\_Kestrel\_\_Certificates\_\_Default\_\_Path | SOME\_CERTIFICATE\_PATH. For example, "/https/aspnetapp.pfx." | Path to the openssl.pfx certificate |
      | -v %USERPROFILE%.aspnet\\https:/https/ |  | Path to the certificate storage |
      | --workdir | /app | Working directory |
      | -p SOME\_HTTP\_PORT:80 |  | Port numbers that map the container to Docker environment. Docker serves the HTTP version of Identity Service via this port. |
      | -p SOME\_HTTPS\_PORT:443 |  | Port numbers that map the container to Docker environment. Docker serves the HTTPS version of Identity Service via this port. |
      | -d |  | A container startup format. Does not depend on the process that runs the container. |
      | creatio-identity-service:latest |  | The name of the Docker image to run. |
8. Set up the Identity Service **logging**. Enable logging to verify that the Identity Service operates as expected. For optimal performance, enable logging only while testing and debugging.
1. Open the appsettings.json file in the root Identity Service directory.

2. Configure the log level.



      appsettings.json file





      ```json
      "Logging": {
        "LogLevel": {
          "Default": "Debug"
        }
      }
      ```









      Specify the log level based on your business goals. Learn more: [Define the log rules](https://academy.creatio.com/documents?id=15181&anchor=title-2121-4) (developer documentation).

3. Save the changes.

**As a result**, you will have the application pool and website for Identity Service.

## 2\. Make sure the Identity Service is running [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#title-2002-7 "Direct link to 2. Make sure the Identity Service is running")

To make sure the Identity Service is running, use the `[Identity Service URL]/.well-known/openid-configuration` link.

**As a result**:

- The Identity Service will be launched.
- The Identity Service will create a set of database tables (Fig. 6).
- The client settings from the appsettings.json file will be added to the "Clients" database table.

Fig. 6 Database tables created by Identity Service

![Fig. 6 Database tables created by Identity Service](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/database_tables.png)

If you need to **change the client settings**:

1. Delete the record from the "Clients," "ClientScopes," "ClientSecrets," "ClientClaims" database tables.
2. Relaunch the IdentityService.dll library.
3. Make sure the Identity Service is running.

## Next steps [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#title-2823-1 "Direct link to Next steps")

Now you can set up the OAuth 2.0 authorization. Instructions: [Set up the OAuth 2.0 authorization](https://academy.creatio.com/documents?id=2467).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#see-also "Direct link to See also")

[Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632)

[Set up the OAuth 2.0 authorization](https://academy.creatio.com/documents?id=2467)

[Update the Identity Service using IIS](https://academy.creatio.com/documents?id=2468)

[NLog](https://academy.creatio.com/documents?id=15182)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction\#resources "Direct link to Resources")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [1\. Install the Identity Service](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-1)
  - [Install the Identity Service using IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-5)
  - [Install the Identity Service using Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-6)
- [2\. Make sure the Identity Service is running](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2002-7)
- [Next steps](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#title-2823-1)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/set_up_the_identity_service_instruction#resources)