<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8)** (8.3).

Version: 8.2All Creatio products

On this page

Since Microsoft ended official support for .NET 6 in November 2024, starting from version 8.2.1 Creatio no longer supports .NET 6 and switches to .NET 8.

You can migrate Creatio .NET 6 to .NET 8 as part of the Creatio update process. In general, the migration procedure comprises the following steps:

1. Prepare the application server. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-1)
2. Adapt custom C# code. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-2)
3. Update Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-3)

## Step 1. Prepare the application server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8\#title-2625-1 "Direct link to Step 1. Prepare the application server")

The server must contain software required for .NET 8 to operate as intended. As such, install the following components into the server:

- **.NET 8 SDK version 8.0.404 or later**. You can download it from the official Microsoft website. [Download](https://dotnet.microsoft.com/en-us/download/dotnet/8.0).
- **Hosting Bundle for ASP.NET Core Runtime version 8.0.11 or later** (for Windows). You can download it from the official Microsoft website. [Download](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-8.0.11-windows-hosting-bundle-installer).

## Step 2. Adapt custom C\# code [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8\#title-2625-2 "Direct link to Step 2. Adapt custom C\# code")

note

If you customized Creatio only using no-code tools, skip this step.

Depending on the libraries you used in C# schemas to customize Creatio, you might need to adapt custom C# code when moving to .NET 8. Learn more about breaking changes in .NET 8 that might require code adaptation in the official Microsoft documentation: [Breaking changes in .NET 8](https://learn.microsoft.com/en-us/dotnet/core/compatibility/8.0).

To find custom C# code to adapt, we recommend updating a test or pre-production environment to .NET 8 first and testing the functionality implemented using custom C# code on the environment. This lets you find breaking changes that only appear in runtime and adapt required code before updating the production environment.

## Step 3. Update Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8\#title-2625-3 "Direct link to Step 3. Update Creatio")

The update process is similar to updating Creatio .NET 6. However, you have to use Creatio .NET 8 archive as part of the update. Learn more about updating Creatio in a separate article: [Update guide](https://academy.creatio.com/documents?id=2495).

If you adapted custom C# code, install packages that contain adapted code into the environment after you update it.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8\#see-also "Direct link to See also")

[Update guide](https://academy.creatio.com/documents?id=2495)

- [Step 1. Prepare the application server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-1)
- [Step 2. Adapt custom C# code](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-2)
- [Step 3. Update Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#title-2625-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8#see-also)