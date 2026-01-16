<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction)** (8.3).

Version: 8.2On-site

On this page

Identity Service implements OAuth 2.0 in Creatio.

note

If you use Creatio **in the cloud**, the Identity Service is deployed out of the box. Proceed to getting OAuth 2.0 credentials. Instructions: [Generate OAuth 2.0 client credentials](https://academy.creatio.com/documents?id=2508&anchor=title-2508-1).

## Install the Identity Service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#title-2002-1 "Direct link to Install the Identity Service")

This is a one-time procedure. Before you install the Identity Service, deploy the database and Creatio application servers.

You can install the Identity Service in multiple ways:

- Using IIS. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-5)
- Using Docker. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-6)

To encrypt access tokens, the Identity Service utilizes OpenSSL certificates. You can use a certificate issued by a trusted certificate authority (CA) or alternatively, a manually generated certificate. Learn more: [Generate PFX certificate using OpenSSL](https://academy.creatio.com/documents?id=2565).

Important

To maintain robust security standards, it is strongly recommended to use unique certificates for each individual instance of the Identity Service.

### Install the Identity Service using IIS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#title-2002-5 "Direct link to Install the Identity Service using IIS")

Install the Identity Service into the Creatio application server. Each Creatio instance needs an individual Identity Service.

To install the Identity Service using IIS:

01. **Install additional components**.
    For Creatio 8.2.1 and later







    .NET 8 Runtime. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)



    .NET 8 Hosting Bundle. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-8.0.10-windows-hosting-bundle-installer)







    For Creatio 8.2.0







    .NET 6 Runtime. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)



    .NET 6 Hosting Bundle. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-6.0.14-windows-hosting-bundle-installer)

02. **Restart the IIS**.

03. **Extract the IdentityService.zip archive** to an arbitrary directory in the root Creatio directory. For example, "IdentityService."

04. **Add the Identity Service application pool** to the IIS. Use dedicated application pool for every Creatio instance.


    1. Open the **Application Pools** section in the **Connections** area of the IIS.

    2. Select **Add Application Pool...** in the **Actions** area (Fig. 1). This opens the **Add Application Pool** window.
       Fig. 1 Add the pool to the IIS

       ![Fig. 1 Add the pool to the IIS](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/add_pool.png)

    3. Fill out the settings.



       | Setting | Setting value |
       | --- | --- |
       | Name | Must be unique. For example, "IDServicePool." |
       | .NET CLR Version | No Managed Code |
       | Managed pipeline mode | Integrated |

    4. Save the changes.


As a result, the "IDServicePool" pool will be added (Fig. 2).
Fig. 2 Identity Service pool

![Fig. 2 Identity Service pool](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/identity_service_pool.png)

05. **Set up access to the application pool** (optional for development environment). By default, the Windows user accesses the application pool.
    1. Select "IDServicePool" in the **Application Pools** area.

    2. Select **Advanced Settings...** in the **Actions** area (Fig. 3). This opens the **Advanced Settings** window.
       Fig. 3 Set up access

       ![Fig. 3 Set up access](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/identity_service_pool_access.png)

    3. Set **Load User Profile** parameter to "True."

    4. Click ![](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/details_button.png) in the **Identity** setting of the **Advanced Settings** window (Fig. 3). This opens the **Application Pool Identity** window.

    5. Select the **Custom account** checkbox and click **Set...** (Fig. 4). This opens the **Set Credentials** window.
       Fig. 4 Add a new user

       ![Fig. 4 Add a new user](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/add_a_new_user.png)

    6. Fill out the **User name**, **Password**, **Confirm password** user settings.

    7. Save the changes.
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

![Fig. 5 Website for Identity Service](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/website_for_identity_service.png)

07. **Connect the website to your Creatio DBMS**.
    1. Open the appsettings.json file in the root Identity Service directory.

    2. Modify the file parameters.



       | Parameter | Parameter value |
       | --- | --- |
       | DbProvider | "MsSqlServer" or "Postgres" |
       | DatabaseConnectionString | Use the same connection string you specified in the `connectionString` attribute of the ConnectionStrings.config file. Use escaped characters. |


       The user that connects to the database must have permissions to create and update the tables.

       If you need to connect the Identity Service to Creatio that uses **Oracle DBMS**, deploy an additional PostgreSQL or Microsoft SQL database instance.

    3. Save the changes.
08. **Set up the Identity Service system client**.
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
09. **Generate openssl.pfx certificate** by a trusted certificate authority (CA) or manually. Instructions: [Generate PFX certificate using OpenSSL](https://academy.creatio.com/documents?id=2565).

    Since Creatio version 8.2.3, OAuth and OpenID authorization functionality support certificates encrypted with RSA, or ECDSA using the following combinations: P-256 with SHA-256, P-384 with SHA-384, or P-521 with SHA-512. When using certificates from a certificate authority, ensure they are signed with a supported encryption type to guarantee compatibility.

10. **Set up the access to openssl.pfx certificate**.
    1. Open the appsettings.json file in the root Identity Service directory.
    2. Specify the full path to openssl.pfx certificate from the root Identity Service directory in the `X509CertificatePath` parameter. Use escaped characters.
    3. Save the changes.
11. **Switch the Identity Service to HTTPS** (optional for development environment). The setup process is similar to switching Creatio to HTTPS. Instructions: [Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632).

12. **Set up the Identity Service logging**. Enable logging to verify that the Identity Service operates as expected. For optimal performance, enable logging only while testing and debugging.
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

**As a result**:

- The application pool and website for Identity Service will be created.
- The Identity Service will be launched.
- The Identity Service will create a set of database tables (Fig. 6).
- The client settings from the appsettings.json file will be added to the "Clients" database table.

Fig. 6 Database tables created by Identity Service

![Fig. 6 Database tables created by Identity Service](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/setup_oauth20_for_external_apps/8.0/database_tables.png)

If you need to **change the client settings**:

1. Delete the record from "Clients," "ClientScopes," "ClientSecrets," "ClientClaims" Identity Service database tables.
2. Relaunch the IdentityService.dll library.
3. Restart the Identity Service application pool.
4. Test the Identity Service.

### Install the Identity Service using Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#title-2002-6 "Direct link to Install the Identity Service using Docker")

1. **Extract the IdentityService.zip archive** to an arbitrary directory in the root Creatio directory. For example, "IdentityService."

2. **Connect the website to your Creatio DBMS**. You can do this in multiple ways:


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

3. **Generate openssl.pfx certificate** by a trusted certificate authority (CA) or manually. Instructions: [Generate PFX certificate using OpenSSL](https://academy.creatio.com/documents?id=2565).

Since Creatio version 8.2.3, OAuth and OpenID authorization functionality support certificates encrypted with RSA, or ECDSA using the following combinations: P-256 with SHA-256, P-384 with SHA-384, or P-521 with SHA-512. When using certificates from a certificate authority, ensure they are signed with a supported encryption type to guarantee compatibility.

4. **Set up the Identity Service system client**. To do this, modify the file parameters. The Identity Service uses these values to interact with Creatio. All parameters support uppercase and lowercase letters, numbers, and special characters, for example, brackets or punctuation marks.



| Parameter | Parameter value | Requirements for parameter value |
| --- | --- | --- |
| ClientId | An arbitrary client ID. For example, "IdServiceUser." | 16 characters |
| ClientName | An arbitrary client name. For example, "MyIdentityServiceApp." | Any number of characters |
| Secrets | An arbitrary client secret. For example, "ItIsMyPasswordForIdentityService." | 32 characters |




Example that sets up the Identity Service system client





```json
"[{\"ClientId\":\"SOME_CLIENT_ID\",\"ClientName\":\"SOME_CLIENT_NAME\",\"Secrets\":[\"SOME_CLIENT_SECRET\"],\"AllowedGrantTypes\":[\"implicit\",\"client_credentials\"],\"RedirectUris\":[\"http://localhost:8090\",\"http://localhost:8090/lib\",\"http://localhost:8090/lib/\"],\"PostLogoutRedirectUris\":[\"http://localhost:8090\"],\"IdentityTokenLifetime\": 300,\"AccessTokenLifetime\": 3600,\"Properties\": {\"AllowedQueryParameters\": \"[\\\"invitationHash\\\",\\\"targetSubject\\\"]\"},\"AllowedScopes\": [\"register_own_resource\", \"get_resource_list\", \"get_client_info\", \"find_clients\", \"remove_client\", \"update_client\", \"add_registrar_client\", \"IdentityServerApi\"]}]",
```

5. **Build the Docker image**. To do this, run the `docker build -t creatio-identity-service -f ./Dockerfile-OAuth .` command.

6. **Run the container** using the following command:



   - For Creatio 8.2.1 and later
   - For Creatio 8.2.0

```cli
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
--env=ASPNETCORE_URLS=http://+:80 --env=DOTNET_RUNNING_IN_CONTAINER=true
--env=DOTNET_VERSION=8.0.10 --env=ASPNET_VERSION=8.0.10 --workdir=/app
-p 80:80 -d creatio-identity-service:latest
```

```cli
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
--env=ASPNETCORE_URLS=http://+:80 --env=DOTNET_RUNNING_IN_CONTAINER=true
--env=DOTNET_VERSION=6.0.15 --env=ASPNET_VERSION=6.0.15 --workdir=/app
-p 80:80 -d creatio-identity-service:latest
```

7. **Switch the Identity Service to HTTPS**.
1. Obtain a digital certificate from the certification center. Instructions: [Windows using Linux containers](https://learn.microsoft.com/en-us/aspnet/core/security/docker-https?view=aspnetcore-7.0#windows-using-linux-containers) (vendor documentation).

2. Run the following command:



      - For Creatio 8.2.1 and later
      - For Creatio 8.2.0

```cli
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
-e ASPNETCORE_URLS="https://+;http://+" -e ASPNETCORE_HTTPS_PORT=443
-e DOTNET_RUNNING_IN_CONTAINER=true -e DOTNET_VERSION=8.0.10
-e ASPNET_VERSION=8.0.10 -e ASPNETCORE_Kestrel__Certificates__Default__Password=SOME_CERTIFICATE_PASSWORD
-e ASPNETCORE_Kestrel__Certificates__Default__Path=/https/aspnetapp.pfx
-v %USERPROFILE%\.aspnet\https:/https/ --workdir=/app -p SOME_HTTP_PORT:80 -p SOME_HTTPS_PORT:443
-d creatio-identity-service:latest
```

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
8. **Set up the Identity Service logging**. Enable logging to verify that the Identity Service operates as expected. For optimal performance, enable logging only while testing and debugging.
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

**As a result**:

- The application pool and website for Identity Service will be created.
- The Identity Service will be launched.
- The Identity Service will create a set of database tables (Fig. 6).
- The client settings from the appsettings.json file will be added to the "Clients" database table.

If you need to **change the client settings**:

1. Delete the record from "Clients," "ClientScopes," "ClientSecrets," "ClientClaims" Identity Service database tables.
2. Relaunch the IdentityService.dll library.
3. Restart the Identity Service application pool.
4. Test the Identity Service.

## Test the Identity Service (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#title-2002-7 "Direct link to Test the Identity Service (optional)")

To test the Identity Service, access the `[Identity Service URL]/.well-known/openid-configuration` URL from the browser.

**As a result**, the list of Identity Service settings will be displayed.

You can **set up automated monitoring systems** based on OAuth health monitoring. Instructions: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513). If needed, use **Postman** to test the Identity Service and check the health of OAuth functionality. The Postman request collection that tests requests is available in [Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#0e2dd1ce-1a5d-4870-bb0b-c0cc2eb25a31).

Now you can connect the Identity Service to Creatio. Instructions: [Connect the Identity Service to Creatio](https://academy.creatio.com/documents?id=2467).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#see-also "Direct link to See also")

[Connect the Identity Service to Creatio](https://academy.creatio.com/documents?id=2467)

[Manage the OAuth 2.0 client credentials](https://academy.creatio.com/documents?id=2508)

[OAuth health monitoring](https://academy.creatio.com/documents?id=2513)

[Authorize external requests using OAuth 2.0 (developer documentation)](https://academy.creatio.com/documents?id=15058)

[NLog (developer documentation)](https://academy.creatio.com/documents?id=15182)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction\#e-learning-courses "Direct link to E-learning courses")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [Install the Identity Service](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-1)
  - [Install the Identity Service using IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-5)
  - [Install the Identity Service using Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-6)
- [Test the Identity Service (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#title-2002-7)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction#e-learning-courses)