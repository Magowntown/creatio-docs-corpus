<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-windows/enable-required-windows-components)** (8.3).

Version: 8.2All Creatio products

On this page

Make sure that you install the following components into the web server before you create and set up a website:

- Windows components. Microsoft Visual C++ 2013 component is required.
- Web Server IIS components.

## Required Windows components for Creatio NET Framework [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components\#title-252-1 "Direct link to Required Windows components for Creatio NET Framework")

To ensure correct compilation of the application, download and install .NET 8 SDK and .NET Framework SDK v 4.7.2.

Grant permissions to read, create, and delete files and subfolders of the \\Terrasoft.WebApp\\Terrasoft.Configuration catalog to the user who runs the application pool in IIS.

[Download 64-bit .NET 8 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

[Download 64-bit .NET Framework SDK v 4.7.2](https://dotnet.microsoft.com/download/thank-you/net472-developer-pack)

Important

Production environment for Creatio .NET Framework requires a Windows Server OS. You can deploy application server on Windows 10 only for development and pre-production environments.

| Component | Component items |
| --- | --- |
| Common HTTP Features | Static Content<br>Default Document<br>HTTP Errors<br>HTTP Redirection |
| Application Development | ASP.Net<br>.Net extensibility<br>ISAPI extensions<br>ISAPI Filters<br>WebSocket Protocol |
| Microsoft .Net framework 3.5.1 | Windows Communication Foundation HTTP Activation<br>Windows Communication Foundation Non-HTTP Activation |
| Microsoft .Net Framework 4.7 Advanced Services and up (Windows 8, Windows 10, Windows Server 2016). | ASP.NET 4.6.2 or 4.7;<br>WCF services<br>HTTP Activation<br>Message Queuing (MSMQ) Activation<br>Named Pipe Activation<br>TCP Activation<br>TCP Port Sharing |
| Health and Diagnostics: | HTTP Logging<br>Logging Tools<br>Request Monitor<br>Custom Logging |
| Security | Basic Authentication<br>Request Filtering<br>IP and Domain Restriction |

## Required Windows Components for Creatio .NET [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components\#title-252-3 "Direct link to Required Windows Components for Creatio .NET")

Important

Since Microsoft ended official support for .NET 6 in November 2024, starting from version 8.2.1 Creatio no longer supports .NET 6 and switches to .NET 8.

To ensure correct compilation of the application, download and install .NET SDK and .NET Hosting bundle.

Grant permissions to read, create, and delete files and subfolders of the \\Terrasoft.WebApp\\Terrasoft.Configuration catalog to the user who runs the application pool in IIS.

For .NET 8

[Download 64-bit .NET 8 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

[Download .NET 8 Hosting bundle](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-8.0.11-windows-hosting-bundle-installer)

For .NET 6

[Download 64-bit .NET 6 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)

[Download .NET 6 Hosting bundle](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-aspnetcore-6.0.14-windows-hosting-bundle-installer)

Important

Production environment for Creatio .NET requires a Windows Server OS. You can deploy application server on Windows 10 or Windows 11 only for development and pre-production environments.

| Component | Component items |
| --- | --- |
| Common HTTP Features | Static Content<br>Default Document<br>HTTP Errors<br>HTTP Redirection |
| Application Development | ASP.Net<br>.Net extensibility<br>ISAPI extensions<br>ISAPI Filters<br>WebSocket Protocol |
| Microsoft .Net Framework 4.8 Advanced Services and later | Windows Communication Foundation HTTP Activation<br>Windows Communication Foundation Non-HTTP Activation |
| Microsoft .Net Framework 4.7 Advanced Services and later (Windows 8, Windows 10, Windows Server 2016). | ASP.NET 4.8;<br>WCF services<br>HTTP Activation<br>Message Queuing (MSMQ) Activation<br>Named Pipe Activation<br>TCP Activation<br>TCP Port Sharing |
| Health and Diagnostics: | HTTP Logging<br>Logging Tools<br>Request Monitor<br>Custom Logging |
| Security | Basic Authentication<br>Request Filtering<br>IP and Domain Restriction |

## Enable required Windows components on Windows Server 2016 [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components\#title-252-1 "Direct link to Enable required Windows components on Windows Server 2016")

To check the availability of the needed components:

01. Enter "control panel" in the **Start** menu → **Control Panel** (Fig. 1).
    Fig. 1 Control Panel section in the Start menu

    ![Fig. 1 Control Panel section in the Start menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_main_menu_windows_server.png)

02. Select **Turn Windows features on or off** in the control panel (Fig. 2).
    Fig. 2 Select Turn Windows features on or off

    ![Fig. 2 Select Turn Windows features on or off](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_turn_windows_windows_server.png)

03. Select **Role-based or feature-based installation** → **Next** in the **Add Roles and Features Wizard** (Fig. 3).
    Fig. 3 Select the role-based installation

    ![Fig. 3 Select the role-based installation](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_role_based_model_win2016.png)

04. Select the destination server from the available server pool and click **Next** (Fig. 4).
    Fig. 4 Select the destination server

    ![Fig. 4 Select the destination server](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_select_destination_server_win2016.png)

05. Select the "Web Server (IIS)" role to apply to the selected server. Click **Next** (Fig. 5).
    Fig. 5 Select the Web Server (IIS) role

    ![Fig. 5 Select the Web Server (IIS) role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_server_selecting_iis_role_win2016_next.png)

06. Click **Add features** (Fig. 6).
    Fig. 6 Confirm selected features

    ![Fig. 6 Confirm selected features](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_server_add_features_win2016.png)

07. Select features → **Next** (Fig. 7).
    Fig. 7 Select features

    ![Fig. 7 Select features](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_server_selecting_iis_role_win2016_next_features.png)

08. Click **Next** to proceed to the next step (Fig. 8).
    Fig. 8 Confirm the web server role

    ![Fig. 8 Confirm the web server role](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_server_finalize_win2016.png)

09. Make sure that you select the same components as on the Fig. 9.
    Fig. 9 Required components

    ![Fig. 9 Required components](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_iis_required_componnets_win2016.png)

10. Click **Install** (Fig. 10).


Fig. 10 Confirm installation

![Fig. 10 Confirm installation](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_installing_iis_win2016.png)

11. Reboot the server.

## Enable required Windows Components on Windows 10 [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components\#title-252-2 "Direct link to Enable required Windows Components on Windows 10")

To check the availability of the needed components:

1. Enter "control panel" in the **Start** menu → **Control Panel** (Fig. 11).
Fig. 11 Control Panel section in the Start menu

![Fig. 11 Control Panel section in the Start menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_main_menu.png)

2. Select the **Programs** option in the control panel (Fig. 12).
Fig. 12 Programs menu

![Fig. 12 Programs menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_programs.png)

3. Select the **Turn Windows features on or off** option from the **Programs and Features** menu (Fig. 13).
Fig. 13 Select the Turn Windows features on or off option

![Fig. 13 Select the Turn Windows features on or off option](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_turn_windows.png)

4. Select all required components in the **Windows Features** window (Fig. 14).
Fig. 14 Select Web Server IIS and Windows components

![Fig. 14 Select Web Server IIS and Windows components](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/enable_required_windows_components/scr_setup_turn_windows_on.png)


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components\#see-also "Direct link to See also")

[Configure the application site on IIS](https://academy.creatio.com/documents?product=administration&ver=7&id=2142)

[Set up websockets](https://academy.creatio.com/documents?product=administration&ver=7&id=1631)

[Switching from HTTP to HTTPS](https://academy.creatio.com/documents?product=administration&ver=7&id=1632)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Required Windows components for Creatio NET Framework](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#title-252-1)
- [Required Windows Components for Creatio .NET](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#title-252-3)
- [Enable required Windows components on Windows Server 2016](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#title-252-1)
- [Enable required Windows Components on Windows 10](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#title-252-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/enable-required-windows-components#see-also)