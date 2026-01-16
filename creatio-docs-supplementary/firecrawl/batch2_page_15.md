<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/host-header-protection)** (8.3).

Version: 8.1

On this page

Browsers send host headers to specify the URL the client wants to visit. Malicious actors can inject the host header to display their website instead of the target website. For example, they can spoof a password reset form.

All instances of **Creatio in the cloud** are protected from host header injection attack out-of-the-box. If you use **Creatio on-site**, set up the protection yourself. You can do it in the following ways:

1. Use Microsoft URL rewrite module for **IIS**. To do this, follow the [official Microsoft instructions](https://techcommunity.microsoft.com/t5/iis-support-blog/host-header-vulnerability/ba-p/1031958).
2. Use the built-in mechanism in Creatio version 8.1.2 and later. For example, this is useful if you use **.NET 6** on Linux. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection#title-111-2)

## Use the built-in Creatio mechanism [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection\#title-111-2 "Direct link to Use the built-in Creatio mechanism")

Make sure to fill out the settings correctly to ensure Creatio operates as intended.

To turn on the built-in host header protection mechanism, fill out the `AllowedHostHeaderPattern` setting of the web.config file in the WebApp.Loader. You can do it as follows:

```xml
<add key="AllowedHostHeaderPattern" value="myhost.domain.com" />
```

In this case, the value follows the "contains" rule. The setting also supports regular expressions. This lets you set up more flexible options, for example:

```xml
<add key="AllowedHostHeaderPattern" value="^myhost\.domain\.(com|it|eu)$" />
```

If you **use IP addresses** to contact the website, display both the IP address and DNS name of the website using the the "or" regular expression.

If you **use a web farm**, set the value as balancer host and IP address in a single regular expression:

```xml
<add key="AllowedHostHeaderPattern" value="mybalancerhost.domain.com|192.168.11.12" />
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection\#see-also "Direct link to See also")

[Description of system settings](https://academy.creatio.com/documents?id=1259)

- [Use the built-in Creatio mechanism](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection#title-111-2)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/host-header-protection#see-also)