<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https)** (8.3).

Version: 8.2All Creatio products

On this page

The HTTPS protocol ensures secure connection between a client and a web service. Switching from HTTP to HTTPS is recommended to increase system security and enable additional services, such as WebRTC support in Webitel. Please note that this article refers only to on-site applications. To switch to HTTPS, you need to change several options of the website in IIS and edit the Web.config file. Creatio cloud uses secure connection by default.

note

You will not be able to use the advantages of HTTPS if Creatio application is deployed on Windows Server 2008.

## IIS setup [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https\#title-272-1 "Direct link to IIS setup")

Before configuring HTTPS, do the following:

- Obtain a digital certificate from the certification center in PFX format;



note





If you are using a self-signed certificate, Creatio mobile application will not be able to connect to the Creatio site due to the security policies of mobile applications.

- [Set up websockets](https://academy.creatio.com/documents?product=studio&ver=7&id=1631) for the correct operation of all system components;

- Additionally, check the list of installed [IIS components](https://academy.creatio.com/documents?product=studio&ver=7&id=2081) to avoid errors during Creatio setup and operation.


The received digital certificate must be loaded into the server certificate storage:

1. Open Internet Information Services (IIS) Manager.

2. In the main IIS window, double-click the **Server Certificates** detail ( [Fig. 1](https://academy.creatio.com/#XREF_77594_371_Server)).
Fig. 1 Selecting the Server Certificates detail

![Fig. 1 Selecting the Server Certificates detail](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_iis_server_certificates.png)

3. In the **Server Certificates** window, click the **import** link in the action menu to the right ( [Fig. 2](https://academy.creatio.com/#XREF_69608_372_Import)).
Fig. 2 Opening the Import window

![Fig. 2 Opening the Import window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_iis_import_link.png)

4. In the import dialog box, specify:
1. Path to the import file hosted on the server

2. Password (if required)

3. Certificate storage ( [Fig. 3](https://academy.creatio.com/#XREF_95244_373))
      Fig. 3 Certificate import window

      ![Fig. 3 Certificate import window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_import_certificate.png)
5. Click **OK** to import the certificate.


Next, connect the imported certificate to the Creatio application:

1. In the IIS window, go to the application website by clicking its name in the left **Connections** menu ( [Fig. 4](https://academy.creatio.com/#XREF_94357_374_bpm_online_IIS)).
Fig. 4 Selecting the Creatio website in the IIS window

![Fig. 4 Selecting the Creatio website in the IIS window](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_iis_site_select.png)

2. Click the **Bindings** link in the action menu ( [Fig. 5](https://academy.creatio.com/#XREF_85776_375)).
Fig. 5 Selecting website bindings

![Fig. 5 Selecting website bindings](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_iis_site_bindings_link.png)

3. In the website bindings menu, click **Add** and add a new binding. In the **Add Site Binding** window, specify:
1. Type "https"

2. Website address

3. SSL certificate ( [Fig. 6](https://academy.creatio.com/#XREF_15061_376_bpm_online)).
      Fig. 6 Binding a certificate to the Creatio website

      ![Fig. 6 Binding a certificate to the Creatio website](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/switch_from_HTTP_to_HTTPS/scr_chapter_setup_http_wnd_site_binding.png)
4. Click **OK** to confirm the settings.

Now the certificate is successfully bound to the web application.


## Web.config setup [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https\#title-272-2 "Direct link to Web.config setup")

After adding the certificate, you need to make changes to the Web.config configuration file, located in the **root directory** of the Creatio website.

1. At the end of the file, find:





```xml
<behaviors configSource="Terrasoft.WebApp\ServiceModel\http\behaviors.config" />
<bindings configSource="Terrasoft.WebApp\ServiceModel\http\bindings.config" />
```

2. Change paths from "http" to "https":





```xml
<behaviors configSource="Terrasoft.WebApp\ServiceModel\https\behaviors.config" />
<bindings configSource="Terrasoft.WebApp\ServiceModel\https\bindings.config" />
```


Edit the Web.config file located in the **Path to the root website directory\\Terrasoft.WebApp** directory.

1. Set the variable value to encrypted="true". The configuration differs depending on the operating system of the server with Creatio application.

For Windows Server 2016 and higher, the configuration string should look as follows:





```xml
<wsService
    type="Terrasoft.Messaging.MicrosoftWSService.MicrosoftWSService,
    Terrasoft.Messaging.MicrosoftWSService" encrypted="true"
    portForClientConnection="443" maxConnectionNumber="100"
    clearIdleSession="false" clearIdleSessionInterval="120" />
```

2. At the end of the file, find:





```xml
<services configSource="ServiceModel\http\services.config" />
```

3. Change the path from "http" to "https":





```xml
<services configSource="ServiceModel\https\services.config" />
```


Save the configuration files.

Restart the application in the IIS and then go to your Creatio website. If all is done right, then in the address bar you will see "https://" before the web address of the application.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https\#see-also "Direct link to See also")

[Setting up additional parameters and integrations](https://academy.creatio.com/documents?product=studio&ver=7&id=1633)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=studio&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [IIS setup](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https#title-272-1)
- [Web.config setup](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https#title-272-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https#see-also)