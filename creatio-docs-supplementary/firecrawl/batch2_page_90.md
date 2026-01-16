<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/content-security-policy)** (8.3).

Version: 8.1

On this page

note

This functionality is available for Creatio 8.1.2 and later. Instructions for an earlier Creatio versions: [Manage HTTP response headers](https://academy.creatio.com/documents?id=2404).

**Content security policy** (CSP) is an additional layer of security that helps to detect and prevent web attacks of multiple types, from data theft to site defacement or malware distribution. The main goal of CSP is to prevent [cross-site scripting](https://owasp.org/www-community/attacks/xss/) and other code injection attacks. CSP provides an extensive set of policy directives that let you control the resources a website page can load. Each directive defines the restrictions for a specific type of resource.

When CSP works in blocking mode, it enhances security by blocking connections, scripts, fonts, and other types of resources that originate from unknown or malicious sources. Web browsers follow CSP rules specified in web page headers to block requests to unknown servers for resources that include scripts, images, and other data. Learn more: [Content Security Policy Reference](https://content-security-policy.com/) (official vendor documentation).

Out-of-the-box, Creatio provides the list of trusted sources that ensure full functionality of base products. This list cannot be modified. System administrators can configure trusted sources for content loading and associate them with directives in the **Content Security Policy** section of the System Designer.

Creatio includes multiple CSP working modes. You can change the mode in the "Content security mode" ("CspMode" code) [system setting](https://academy.creatio.com/documents?id=1259).

| Content security mode | Description |
| --- | --- |
| Log violations of content security policies | Use this mode to collect information about all sources your Creatio instance reaches to retrieve data. This information lets you set up a stricter security policy. Default mode for Creatio in the cloud. |
| Block download and execution of content that violates security policies | Use this mode to enforce a strict security policy to prevent XSS attacks, data injection attacks, and other web security vulnerabilities. |
| Disable content security | Default mode for Creatio on-site. |

Any changes made to the CSP and trusted sources affect the content security headers in real-time.

important

Before you enable blocking content security mode, review the existing and planned browser-level integrations, such as CTI connectors. Include the corresponding domains in the trusted sources list of the CSP. Otherwise, the browser-level integrations will stop working.

We recommend taking the following steps to **switch to blocking content security mode**:

1. Enable "Log violations of content security policies" mode.
2. Collect a list of CSP violations to understand which resources are being flagged.
3. Configure the CSP header based on the collected data to define trusted resources.
4. Enable "Block download and execution of content that violates security policies" mode to enforce the CSP rules.

**As a result**, Creatio will activate blocking content security mode without blocking essential requests.

## Add trusted sources​ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#title-2501-5 "Direct link to Add trusted sources​")

There are several equal ways to set up content security policy in Creatio:

- Add trusted sources and associate them with directives. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-1)
- Add trusted sources from directive page. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-2)
- Add trusted sources from violations log. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-3)

### Add trusted sources and associate them with directives [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#title-2501-1 "Direct link to Add trusted sources and associate them with directives")

Trusted sources specify URLs or other valid values from which content can be loaded safely. After you add the trusted source, associate it with a CSP directive.

To add trusted sources:

1. **Open the Content Security Policy section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) → **Security** → **Content Security Policy**.

2. **Click Add source** in the **Trusted sources** tab. This opens a page.

3. **Fill out the properties** of the trusted source.



| Property | Property description |
| --- | --- |
| Source URL | Trusted source URL. |
| Active | Whether the trusted source is used when constructing the CSP header. |
| Verified | Whether the administrator verified the trusted source. If cleared, trusted sources are not verified yet. Selected by default for records manually added by the administrator. |
| Description | A description of the trusted source. For example, which integration uses it. |

4. **Add allowed directives**. To do this, click **New** at the bottom of the **Allowed directives** expanded list → select the needed directives in the drop-down list → save changes.

5. **Repeat steps 2–4 for all trusted sources needed**.


**As a result**, Creatio will add the list of custom trusted sources.

### Add trusted sources from directive page [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#title-2501-2 "Direct link to Add trusted sources from directive page")

Most URLs are only required to load a limited number of resource types. To control what type of content can be downloaded from a specific source, associate CSP directives with trusted sources. Learn more: [CSP Directive Reference](https://content-security-policy.com/#directive) (official vendor documentation).

To associate directives with trusted sources:

1. **Open the Content Security Policy section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) → **System setup** → **Content Security Policy**.
2. **Open the Directives tab** that includes all CSP directives.
3. **Open the directive page**. To do this, click the directive name, for example, `script-src-elem`.
4. **Associate a trusted source with the directive**. To do this, click **New** at the bottom of the **Trusted sources** expanded list → select the needed source in the drop-down list → save changes.
5. **Repeat step 4 for all trusted sources needed**.

**As a result**, Creatio will associate the directive with trusted sources and define type of content these resources can download.

### Add trusted sources from violations log [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#title-2501-3 "Direct link to Add trusted sources from violations log")

The **Violations log** tab of the **Content Security Policy** section lists all violations of the CSP. Some of the blocked hosts might be sources that can be trusted. For example, this might be the source required by some integration in the Marketplace app. After checking the host you can add it as a trusted source.

To do this:

1. **Open the Content Security Policy section**. To do this, click ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) → **Security** → **Content Security Policy**.
2. **Open the Violations log tab**.
3. **Select the host** in the list of violations, click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/AddCustomCommunicationOption/8.0/scr_MenuButton.png) → **Add to trusted sources**.

**As a result**, Creatio will add the URL of the blocked host to trusted sources and associate it with the same CSP directive that was recorded in the violation. If the trusted source already exists, the CSP directive will be associated with it.

## Bind CSP settings [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#title-2501-4 "Direct link to Bind CSP settings")

When you develop an app with some integrations you can set up content security policy and transfer it together with the app to other environments. To do this bind your CSP settings to the app package. Learn more: [Bind data to a package](https://academy.creatio.com/documents?id=15123) (developer documentation).

| Element to bind | Property value |
| --- | --- |
| Trusted source of content | SysCspUserTrustedSrc |
| Trusted source in directive | SysCspUsrSrcInDirectv |

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy\#see-also "Direct link to See also")

[Recommended information security settings](https://academy.creatio.com/documents?id=2370)

[Official vendor documentation (CSP documentation)](https://content-security-policy.com/)

[Bind data to a package](https://academy.creatio.com/documents?id=15123) (developer documentation)

- [Add trusted sources​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-5)
  - [Add trusted sources and associate them with directives](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-1)
  - [Add trusted sources from directive page](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-2)
  - [Add trusted sources from violations log](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-3)
- [Bind CSP settings](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#title-2501-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/content-security-policy#see-also)