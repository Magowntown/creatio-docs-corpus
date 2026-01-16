<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0On-site

On this page

Update the Identity Service when you update the on-site Creatio instance. The Identity Service archive is provided with the Creatio install file. Before you update the Identity Service on the Creatio application server, update the Creatio instance. Instructions: [Update guide](https://academy.creatio.com/documents?id=2495).

## Update the Identity Service using IIS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction\#title-2468-1 "Direct link to Update the Identity Service using IIS")

01. **Install additional components**.

    .NET 6 Runtime. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)

    .NET 6 Hosting Bundle. [Download the install file](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-6.0.14-windows-hosting-bundle-installer)

02. **Restart the IIS**.

03. **Back up the files** of the root Identity Service directory to an arbitrary place.

04. **Back up the database** connected to the current version of Identity Service. Instructions: [Creating database backup](https://academy.creatio.com/documents?id=2495&anchor=title-143-2).

05. **Stop the application pool** of the Identity Service in the IIS.

06. **Stop the website** of the Identity Service in the IIS.

07. **Extract the IdentityService.zip archive** to the Creatio install file directory.

08. **Replace the files in the root Identity Service directory** with the unpacked files.

09. **Reconfigure the Identity Service** using IIS. Instructions: [Install the Identity Service using IIS](https://academy.creatio.com/documents?id=2466&anchor=title-2002-5) (steps 7-11).

10. **Start the application pool** of the Identity Service in the IIS.

11. **Start the website** of the Identity Service in the IIS.

12. **Test the Identity Service**. To do this, access the `[Identity Service URL]/.well-known/openid-configuration` URL from the browser.

    If the Identity Service is not working as expected, restore the previous version of the Identity Service. [Read more >>>](https://academy.creatio.com/documents?id=2468&anchor=2468-3)


**As a result**, the Identity Service will be updated using IIS.

## Update the Identity Service using Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction\#title-2468-2 "Direct link to Update the Identity Service using Docker")

1. **Stop and remove an existing container** using the following command:





```cli
docker stop SOME_CONTAINER_ID

docker rm SOME_CONTAINER_ID
```

2. **Extract a new IdentityService.zip archive** to an arbitrary directory in the root Creatio directory. For example, "IdentityService."

3. **Build the Docker image**. To do this, run the `docker build -t creatio-identity-service -f ./Dockerfile-OAuth .` command.

4. **Run the container** using the following command:



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

**As a result**, the Identity Service will be updated using Docker.

## Restore the previous version of the Identity Service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction\#title-2468-3 "Direct link to Restore the previous version of the Identity Service")

If an error occurs during the updating, restore the previous version and try again.

To restore the previous version of the Identity Service:

1. **Restore the files** from the Identity Service backup.
2. **Restore the database** from the backup.
3. **Restart the application pool** of the Identity Service in the IIS.
4. **Restart the website** of the Identity Service in the IIS.
5. **Test the Identity Service**. To do this, access the `[Identity Service URL]/.well-known/openid-configuration` URL from the browser.

If the Identity service is not working, contact Creatio support.

You can **set up automated monitoring systems** based on OAuth health monitoring. Instructions: [OAuth health monitoring](https://academy.creatio.com/documents?id=2513). If needed, use **Postman** to check the health of OAuth functionality. The Postman request collection that tests requests is available in [Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#0e2dd1ce-1a5d-4870-bb0b-c0cc2eb25a31).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction\#see-also "Direct link to See also")

[Set up the Identity Service](https://academy.creatio.com/documents?id=2466)

[Set up the OAuth 2.0 authorization](https://academy.creatio.com/documents?id=2467)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction\#resources "Direct link to Resources")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [Update the Identity Service using IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#title-2468-1)
- [Update the Identity Service using Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#title-2468-2)
- [Restore the previous version of the Identity Service](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#title-2468-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/oauth_2_0_authorization/update_the_identity_service_using_iis_instruction#resources)