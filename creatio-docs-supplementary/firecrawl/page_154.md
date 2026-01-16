<!-- Source: page_154 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Setting up Creatio application server (web server) on IIS involves setting up application website in IIS and adding an application pool.

note

.NET 6 application deployment is available for Creatio 8.0.8 and later.

## Add an application pool [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis\#title-269-2 "Direct link to Add an application pool")

To add an application pool:

01. Go to the **Application Pools** section in the **Connections** area of the IIS control window.

02. Select the **Creatio** pool.

03. Select the **Integrated** mode in the **Managed pipeline mode** field.

04. Fill out the **.NET CLR version** field:
    Fig. 1 Window for Applications Pool parameters

    ![Fig. 1 Window for Applications Pool parameters](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_applications_tool.png)

    - Specify ".NET CLR Version v.4.0.30319" for **.NET Framework**.
    - Specify "No Managed Code" for **.NET 6**.
05. Go to the ISAPI and CGI Restrictions on the web server level (Fig. 2) and check if the specified ASP.NET version is allowed.
    Fig. 2 ISAPI and CGI Restrictions menu

    ![Fig. 2 ISAPI and CGI Restrictions menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_isapi.png)

06. Make sure that the **Allowed** status is set in the **Restriction** field for the ASP.NET version (Fig. 3).
    Fig. 3 Status of the ASP.NET version

    ![Fig. 3 Status of the ASP.NET version](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_isapi_allowed.png)

07. Open the Handler Mappings on the server level and make sure that all the required permissions are active (Fig. 4).
    Fig. 4 Handler Mappings menu

    ![Fig. 4 Handler Mappings menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_handler.png)

08. Click **Edit Feature Permissions** in the **Actions** area.

09. Make sure that all the required checkboxes are selected in the **Edit Feature Permissions** window (Fig. 5).
    Fig. 5 Edit Feature Permissions window

    ![Fig. 5 Edit Feature Permissions window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_handler_settings.png)

10. Make sure that MIME-type for .svg and .json files is configured in the new application. This configuration can be performed both on the server (in this case, all applications on this server inherit it) and application level. To check the configuration:
    1. Go to MIME Types on the server or application level (Fig. 6).
       Fig. 6 MIME Types menu

       ![Fig. 6 MIME Types menu](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_mime.png)

    2. Make sure that configuration for .svg and .json files is available. If the configuration is available, go to step 12.
11. If the configuration is not available, click **Add...** in the **Actions** area. This opens a new window. Specify .svg and MIME type of data that corresponds to this extension (Fig. 7) in the window. Repeat the step for .json extension ("application/json" MIME type).
    Fig. 7 MIME data type for .svg files

    ![Fig. 7 MIME data type for .svg files](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_mime_add_svg.png)

12. Restart the website using the **Restart** command in the **Manage Website** area (Fig. 8).
    Fig. 8 Restart command in the Manage Websites area

    ![Fig. 8 Restart command in the Manage Websites area](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_restart_website.png)

13. Open the site by going to the address or using the **Browse** command (Fig. 9). Make sure that the Creatio login page is displayed.
    Fig. 9 Browse command in the Actions area

    ![Fig. 9 Browse command in the Actions area](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_browse.png)




    note





    To log in to a newly deployed application, use the default Supervisor user account. Login: Supervisor; Password: Supervisor. We highly recommend changing the Supervisor password immediately.

14. To enable additional UI language:
    1. Go to the **Languages** section in the system designer.

    2. Select the needed language and click **Open**. This opens a page.

    3. Select the **Active** and **Use by default** checkboxes. Save the changes.

       To enable a language, the user who has run the IIS application pool needs to have access permissions to read, edit and delete application files and content subordinate catalogs (catalog .\\Terrasoft.WebApp\\conf).
15. Click **System settings** in the System Designer and change the **Order of first/last names** system setting value to "Last name, First name **Middle name**." This is required to correctly display contact names in individual columns: **Last name**, **First name**, **Middle name**.


## Set up application website in IIS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis\#title-269-1 "Direct link to Set up application website in IIS")

To create and set up a website:

1. Go to the IIS control window, right-click the **Sites** folder, and select the **Add Website** option from the context menu (Fig. 10).
Fig. 10 The Add website option

![Fig. 10 The Add website option](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_add_website.png)

2. Specify the name of the website, the path to the root folder that contains Creatio files, IP address and website port (Fig. 11). The default website path is C:\\INETpub\\wwwroot. If needed, specify your own IP address.
Fig. 11 New website parameters window

![Fig. 11 New website parameters window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_add_web_site_parametres.png)

3. For NET Framework only







Right-click the created website in the **Connections** area and select the **Add Application** option (Fig. 12).

Fig. 12 Add Application option

![Fig. 12 Add Application option](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_add_application.png)

4. Enter the "0" application name in the **Alias** field. Specify the "Terrasoft.WEBApp" directory (Fig. 13).
Fig. 13 Application parameter selection window

![Fig. 13 Application parameter selection window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/setup_app_server_on_IIS/scr_setup_add_applications_settings.png)


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis\#see-also "Direct link to See also")

[Set up websockets](https://academy.creatio.com/documents?product=studio&ver=7&id=1631)

[Switching from HTTP to HTTPS](https://academy.creatio.com/documents?product=studio&ver=7&id=1632)

[Additional setup](https://academy.creatio.com/documents?product=studio&ver=7&id=1633)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=studio&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Add an application pool](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis#title-269-2)
- [Set up application website in IIS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis#title-269-1)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/application_server_on_windows/deploy_creatio_application_server_on_iis#see-also)