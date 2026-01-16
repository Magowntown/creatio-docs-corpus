<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/recommended-information-security-settings)** (8.3).

Version: 8.1

On this page

This article covers best practices for Creatio settings related to information security.

## Unified organization password policy [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-1 "Direct link to Unified organization password policy")

Make sure the password and login settings comply with your company's security policy. You can use the recommended values if the policy does not specify the exact requirements.

**Password length**. We recommend using passwords that are at least 9 characters long. Set up the desired password complexity in the following [system settings](https://academy.creatio.com/documents?id=1259#title-1880-11):

- "Password complexity: Minimum length" ("MinPasswordLength" code)
- "Password complexity: Minimum quantity of lower case characters" ("MinPasswordLowercaseCharCount" code)
- "Password complexity: Minimum quantity of upper case characters" ("MinPasswordUppercaseCharCount" code)
- "Password complexity: Minimum quantity of digits" ("MinPasswordNumericCharCount" code)
- "Password complexity: Minimum quantity of special characters" ("MinPasswordSpecialCharCount" code)

**Password history**. Creatio compares previous user passwords to the new password to ensure they do not match. Specify how many previous passwords to compare in the "Quantity of analyzed passwords" ("PasswordHistoryRecordCount" code) system setting.

The number of **permitted login attempts** and **user lockout time**. We recommend permitting 5 login attempts and setting the lockout time to 15 minutes. Configure the lockout behavior in the following system settings:

- "Number of logon attempts" ("LoginAttemptCount" code). Sets the number of permitted login attempts.
- "Quantity of login attempts for warning message" ("LoginAttemptBeforeWarningCount" code). Sets the number of failed login attempts after which Creatio displays the warning message that contains the number of login attempts remaining before lockout.
- "User locking time" ("UserLockoutDuration" code). Sets the period in minutes during which the user cannot log in to Creatio if they run out of specified login attempts.

Learn more in a separate article: [Unblock a user](https://academy.creatio.com/documents?id=2385).

**Login failure** and **possible user lockout** messages. We recommend displaying a unified message that does not specify the exact issue. To do this, make sure the values of the following system settings are "false:"

- "Show message about locking account during logging in" (the "DisplayAccountLockoutMessageAtLogin" code)
- "Show message about incorrect password during logging in" (the "DisplayIncorrectPasswordMessageAtLogin" code)

## Session expiration time [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-6 "Direct link to Session expiration time")

Set up the user inactivity period in minutes after which to close the session in the "User session timeout" ("UserSessionTimeout" code) system setting. By default, "60."

## TLS protocol recommendations for Creatio websites and integrations [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-2 "Direct link to TLS protocol recommendations for Creatio websites and integrations")

Creatio supports TLS 1.2 protocol out-of-the-box. We recommend using the following secure TLS cipher suites:

- TLS\_ECDHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_CHACHA20\_POLY1305\_SHA256
- TLS\_DHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_DHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_DHE\_RSA\_WITH\_CHACHA20\_POLY1305\_SHA256
- TLS\_DHE\_RSA\_WITH\_AES\_256\_CCM
- TLS\_DHE\_RSA\_WITH\_AES\_128\_CCM

The following functionality is obsolete, considered a security risk, and is not recommended for use:

- TLS 1.0/1.1 protocols
- DES, 3DES/TDEA, RC2, RC4 ciphers
- CBC encryption mode
- MD5 hashing algorithm
- DH (TLS\_DH\_\*) key exchange

Learn more: [NSA Releases Guidance on Eliminating Obsolete TLS Protocol Configurations](https://www.cisa.gov/news-events/alerts/2021/01/05/nsa-releases-guidance-eliminating-obsolete-tls-protocol), [Decision to Revise NIST SP 800-38A, Recommendation for Block Cipher Modes of Operation: Methods and Techniques](https://csrc.nist.gov/News/2023/decision-to-revise-nist-sp-800-38a), [Deprecating Obsolete Key Exchange Methods in TLS 1.2](https://www.ietf.org/id/draft-ietf-tls-deprecate-obsolete-kex-02.html).

## Secure HTML header configurations for Creatio on-site [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-3 "Direct link to Secure HTML header configurations for Creatio on-site")

Ensure browsers are not susceptible to preventable vulnerabilities. To do this, enable the following headers that comply with OWASP (Open Web Applications Security Project) [Secure Headers Project](https://owasp.org/www-project-secure-headers/):

**HTTP Strict Transport Security (HSTS)**. Enable the Strict-Transport-Security header and set the time to store the parameter in browser memory to 1 year:

```cli
Strict-Transport-Security: max-age=3153600
```

**Clickjacking protection**. Enable the X-Frame-Options header and set it to allow pages to be embedded only on addresses that have the same location as your Creatio application:

```cli
X-Frame-Options: sameorigin
```

**Cross-site scripting attack (XSS) protection**. Disable the X-XSS-Protection header. The X-XSS-Protection header has been deprecated by modern browsers and its use can introduce additional security issues on the client side. As such, OWASP recommends to set the header as X-XSS-Protection: 0 in order to disable the XSS Auditor, and not allow it to take the default behavior of the browser handling the response.

```cli
X-XSS-Protection: 0
```

**MIME-sniffing protection**. Enable the X-Content-Type-Options header and set its mode to "nosniff." The mode prevents the browser from trying to determine the content type of a resource different from the declared content type:

```cli
X-Content-Type-Options: nosniff
```

**Referrer Policy**. Enable the Referrer-Policy header and set it to "origin-when-cross-origin." The header specifies how much referrer information (sent with the Referrer header) to include in requests:

```cli
Referrer-Policy: origin-when-cross-origin
```

## Request responses for Creatio on-site [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-4 "Direct link to Request responses for Creatio on-site")

Limit the amount and type of information available in responses. To do this, modify the Web.config file in Creatio root directory as follows:

1. Disable X-Powered-By.





```xml
<system.webServer>
       <httpProtocol>
           <customHeaders>
               <remove name="X-Powered-By" />
           </customHeaders>
       </httpProtocol>
</system.webServer>
```

2. Disable X-AspNet-Version. To do this, make changes to every httpRuntime section of the Web.config files in the Creatio root directory and Terrasoft.WebApp directory.





```xml
<httpRuntime enableVersionHeader="false" />
```

3. Disable Server Header (available for IIS version 10 and later).





```xml
<system.webServer>
       <security>
           <requestFiltering removeServerHeader ="true" />
       </security>
</system.webServer>
```


## Redis setup for Creatio on-site [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-5 "Direct link to Redis setup for Creatio on-site")

We recommend using a combination of stable Debian and up-to-date Redis versions.

We also recommend **setting up authentication on the Redis server**.

- Use the password authentication on the Redis server for version 8.0.1 and earlier.
- Use any authentication option on the Redis server for version 8.0.2 and later.

Learn more in a separate article: [Set up secure connection to Redis](https://academy.creatio.com/documents?id=2403).

## Restrict access to metadata service for Creatio on-site [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-16 "Direct link to Restrict access to metadata service for Creatio on-site")

If you deploy Creatio by yourself using a cloud service, for example, Azure, AWS, GCP, we recommend restricting access to the 169.254.169.254 IP address of the metadata service using Windows firewall or Linux iptables. This eliminates a potential SSRF attack vector.

## Configure secure cookies for an HTTPS instance [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#title-2395-17 "Direct link to Configure secure cookies for an HTTPS instance")

If your Creatio instance is served over HTTPS, configure secure cookies in the Web.config file both in the root Creatio directory and Terrasoft.WebApp directory. To do this, add the following string to the file:

```xml

<httpCookies httpOnlyCookies="true" requireSSL="true" /> <forms requireSSL="true" />
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings\#see-also "Direct link to See also")

[Manage system settings](https://academy.creatio.com/documents?id=269)

[Modify Web.config](https://academy.creatio.com/documents?id=2141)

[Set up secure connection to Redis](https://academy.creatio.com/documents?id=2403)

- [Unified organization password policy](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-1)
- [Session expiration time](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-6)
- [TLS protocol recommendations for Creatio websites and integrations](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-2)
- [Secure HTML header configurations for Creatio on-site](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-3)
- [Request responses for Creatio on-site](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-4)
- [Redis setup for Creatio on-site](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-5)
- [Restrict access to metadata service for Creatio on-site](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-16)
- [Configure secure cookies for an HTTPS instance](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#title-2395-17)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/recommended-information-security-settings#see-also)