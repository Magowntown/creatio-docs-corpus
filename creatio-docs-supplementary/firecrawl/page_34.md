<!-- Source: page_34 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#__docusaurus_skipToContent_fallback)

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

You can migrate Creatio .NET Core 3.1 to .NET 6 as part of the Creatio update process. In general, the migration procedure comprises the following steps:

1. Prepare the application server. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-1)
2. Adapt custom C# code. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-2)
3. Update Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-3)

## Step 1. Prepare the application server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6\#title-2625-1 "Direct link to Step 1. Prepare the application server")

The server must contain software required for .NET 6 to operate as intended. As such, install the following components into the server:

- **.NET 6 SDK version 6.0.404 or later**. You can download it from the official Microsoft website. [Download](https://dotnet.microsoft.com/en-us/download/dotnet/6.0).
- **Hosting Bundle for ASP.NET Core Runtime version 6.0.14 or later** (for Windows). You can download it from the official Microsoft website. [Download](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-6.0.14-windows-hosting-bundle-installer).

## Step 2. Adapt custom C\# code [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6\#title-2625-2 "Direct link to Step 2. Adapt custom C\# code")

note

If you customized Creatio only using no-code tools, skip this step.

Depending on the libraries you used in C# schemas to customize Creatio, you might need to adapt custom C# code when moving to .NET 6. For example:

- If the client package code reads from **CryptoStream**, **GZipStream**, **DeflateStream**, add a check that the requested number of bytes was read. Learn more in the official Microsoft documentation: [Partial and zero-byte reads in DeflateStream, GZipStream, and CryptoStream](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/6.0/partial-byte-reads-in-streams).
- Use **ImageSharp**, **SkiaSharp**, **Microsoft.Maui.Graphics** libraries instead of System.Drawing.Common. The behavior of this library might differ on Windows and Unix systems, therefore Microsoft recommends not using it. Learn more in the official Microsoft documentation: [System.Drawing.Common only supported on Windows](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/6.0/system-drawing-common-windows-only).

Learn more about breaking changes in .NET 6 that might require code adaptation in the official Microsoft documentation: [Breaking changes in .NET 6](https://learn.microsoft.com/en-us/dotnet/core/compatibility/6.0).

To find custom C# code to adapt, we recommend updating a test or pre-production environment to .NET 6 first and testing the functionality implemented using custom C# code on the environment. This lets you find breaking changes that only appear in runtime and adapt required code before updating the production environment.

## Step 3. Update Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6\#title-2625-3 "Direct link to Step 3. Update Creatio")

The update process is similar to updating Creatio .NET Core. However, you have to use Creatio .NET 6 archive as part of the update. Learn more about updating Creatio in a separate article: [Update guide](https://academy.creatio.com/documents?id=2495).

If you adapted custom C# code, install packages that contain adapted code into the environment after you update it.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6\#see-also "Direct link to See also")

[Update guide](https://academy.creatio.com/documents?id=2495)

- [Step 1. Prepare the application server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-1)
- [Step 2. Adapt custom C# code](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-2)
- [Step 3. Update Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#title-2625-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_linux/move_creatio_net_core_3_1_to_net_6#see-also)