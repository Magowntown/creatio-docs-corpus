<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/platform-cookies#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/platform-cookies)** (8.3).

Version: 8.1

On this page

Creatio may use the following types of cookies and similar technologies to operate and improve products and services offered through the sites (Creatio Services), Application Hub functionality available in Creatio cloud for user accounts connected to an organization account (Application Hub, Cloud), and any other digital properties that Creatio owns or control.:

- **Essential / strictly necessary cookies** required for the operation of the Creatio Services. For example, this includes cookies that let you log in to secure areas. Strictly necessary cookies facilitate the operation of Creatio Services and websites. Without these cookies, parts of Creatio Services and websites will not function properly.
- **Functional cookies** that remember choices you make and recognize you when you return. This enables Creatio to personalize content, greet you by name and remember your preferences (for example, your choice of language or region) or allow the pre-population of certain resource request forms, making it easier for you to access Creatio content.
- **Analytical / performance** cookies that collect information about how you use Creatio Services. They allow Creatio to recognize and count the number of visitors and to see how visitors move around in Creatio Services. This helps us improve the way software works. These cookies may be sometimes placed by third-party providers of web traffic analysis services.

See more details on cookies and how Creatio processes cookie data in the [Creatio Privacy Policy](https://www.creatio.com/privacy-policy).

This article covers only cookies used by Creatio Services, but does not include cookies found in Creatio Marketplace Applications. For the details of each Marketlace app, please read the corresponding app's documentation.

This table describes the cookies used by Creatio platform:

| Cookie Name | Duration | Cookie Type | Description | Product |
| --- | --- | --- | --- | --- |
| ASPXAUTH | Session cookie | Strictly necessary | Stores information about the authorized status of the user and to provide access to protected resources only to authorized users.<br>May store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| BPMLOADER | Session cookie | Strictly necessary | Required for the website to work properly.<br>Stores the unique IDs of anonymous sessions.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| BPMSESSIONID | Session cookie | Strictly necessary | Required for the website to work properly.<br>Stores a unique ID of the session.<br>May store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| BPMCSRF | Session cookie | Strictly necessary | Protects against cross-site requests (CSRF).<br>Stores a unique token that is checked by the server to confirm the legitimacy of requests, thereby preventing possible CSRF attacks.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| UserName | Cookie exists `<number-of-days-to-remember-cookie>` set in system setting UserNameExpireDays.<br>Disabled by default. | Functional cookie (Optional) | Stores a user ID for easier log in to the platform.<br>Set after successful user authorization. Can be activated and deactivated on the customer’s level by setting the UserNameExpireDays system setting.<br>To activate, set the system setting "User name expiration term (days)" ("UserNameExpireDays" code) to `<number-of-days-to-remember-cookie>`.<br>To deactivate, set the system setting "User name expiration term (days)" ("UserNameExpireDays" code) to `0`.<br>May store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Creatio Success Portal |
| UserType | Session cookie | Strictly necessary | Stores user type. Set after successful user authorization.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Creatio Success Portal |
| SsoSessionId | Session cookie | Strictly necessary (for Single Sign-On functionality) | Stores the session ID of a user authenticated via the Single Sign-On mechanism.<br>May store identifiable data | Creatio Services<br>Application Hub, Cloud |
| CookieConscent | 1 year | Strictly necessary | Stores cookie consent preferences.<br>Does not store identifiable data. | Creatio corporate websites<br>Application Hub, Cloud<br>Studio Creatio, free edition |
| \_ga | 1 year | Analytical / performance | Tracks user activities inside Creatio Services.<br>May store identifiable data. | Creatio Services (Cloud deployment)<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| \_ga\_\* | 1 year | Analytical / performance | Tracks user activities inside Creatio Services.<br>May store identifiable data | Creatio Services (Cloud deployment)<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| verto\_session\_uuid | 1 day | Strictly necessary (needed for Webitel integration) | Stores Verto telephony session ID for successful integration with Webitel.<br>Does not store identifiable data. | Creatio Services |
| visid\_incap\_\* | 1 year | Strictly necessary | Encapsulates DDoS Protection and Web Application Firewall. A cookie in which sessions are bound to a specific visitor, with a visitor representing a specific computer. This helps identify clients that have already visited the site.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| incap\_ses\_\* | Session cookie | Strictly necessary | Encapsulates DDoS Protection and Web Application Firewall. A cookie in which HTTP requests are related to a specific session.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition<br>Creatio Success Portal |
| .AspNet.SharedCookie | Session cookie | Strictly necessary | Provides Single Sign-On capability to Creatio Services.<br>Does not store identifiable data. | Creatio Services |
| CreatioIdentityServerAuthenticated | Session cookie | Strictly necessary | Stores the Creatio Identity Service authentication state. The cookie is needed for provision of access to Creatio Services.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition |
| ExistingAlmUser | Session cookie | Strictly necessary | Stores the user’s status in Application Hub, Cloud. The cookie is needed for provision of access to Application Hub, Cloud.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition |
| idsrv.session | Session cookie | Strictly necessary | Stores Creatio Identity Service session information.<br>The cookie is needed for authentication in the Creatio Identity Service to access different Creatio Services.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition |
| sticky-session-id | Session cookie | Strictly necessary | Stores Creatio Istio Service sticky session information.<br>The cookie is needed for the Creatio Istio Service to authenticate traffic between different microservices in Creatio Services.<br>Does not store identifiable data. | Creatio Services<br>Application Hub, Cloud<br>Studio Creatio, free edition |
| product | Session cookie | Strictly necessary | Stores the Creatio trial product type selected by the user.<br>The cookie is needed for Application Hub, Cloud to work properly.<br>Does not store identifiable data. | Application Hub, Cloud |
| bpmHref | 180 days | Strictly necessary | Required for the website to work properly.<br>Stores the complete web address (full URL) of the current page the user is visiting.<br>May store identifiable data. | Creatio Services |
| bpmRef | 180 days | Strictly necessary | Required for the website to work properly.<br>Stores the web address of the page the user came from before visiting the current page.<br>Does not store identifiable data. | Creatio Services |
| TotpSetupToken | 20 mins | Strictly necessary | Required for two-factor authentication to work properly. Stores the token to bind authenticator app.<br>May contain identifiable data. | Creatio Services |
| FirstFactor | 20 mins | Strictly necessary | Required for two-factor authentication to work properly. Stores first factor authentication data.<br>May contain identifiable data. | Creatio Services |
| PasswordRecover | 20 mins | Strictly necessary | Required for the password recovery functionality to work. Stores temporary authentication state in a process of password recovery.<br>May contain identifiable data. | Creatio Services |

Creatio Services can run without the use of functional and analytical / performance cookies, but doing so can reduce functionality. The impact on functionality depends on the purpose of the blocked cookie.

Creatio does not currently provide functionality for cookie consent management.

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/platform-cookies\#see-also "Direct link to See also")

[Recommended information security settings](https://academy.creatio.com/documents?id=2370)

[Set up content security policy](https://academy.creatio.com/documents?id=2501)

[Set up secure storage of sensitive data using Vault](https://academy.creatio.com/documents?id=2395)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/platform-cookies#see-also)