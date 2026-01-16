<!-- Source: page_86 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/landing_page_integration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

This functionality is available in all configurations containing **the Landing pages and web forms section**.

Customers who have their Creatio application deployed on-site may need to perform additional setup to have the HTML code displayed correctly on the landing page. It is required when according to URL safety rules the URL displayed in the user's browser must be different from the one used for external access to Creatio. For example, when the URL gets blocked by the firewall.

To set up landing pages:

1. Go to System Designer → **System settings**.
2. Open the " **Landing pages data collection service URL**" system setting in the **Landing pages section settings** folder.
3. In the **Default value** field, enter the **external URL** of your Creatio application, for example, `http://creatio-marketing.mydomain.com`, and save your settings.

As a result, the HTML code embedded in your landing page will use the correct URL to call the web service for creating a new lead in Creatio, for example:

```xml
serviceUrl: "http://mysite.creatio-marketing/ServiceModel/GeneratedWebFormService.svc/SaveWebFormLeadData"
```

If you use a **secure connection protocol**, enter the URL and specify https:// in it. The web service call address, in this case, will be as follows:

```xml
serviceUrl: "https://mysite.creatio-marketing/ServiceModel/GeneratedWebFormService.svc/SaveWebFormLeadData"
```

note

By default, this setting is not configured and the application URL is generated automatically.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/landing_page_integration\#see-also "Direct link to See also")

[The \[Landing pages and web forms\] section](https://academy.creatio.com/documents?product=marketing&ver=7&id=1081)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_additional_setup/landing_page_integration#see-also)