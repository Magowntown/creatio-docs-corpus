<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Important

The deprecated .NET Core framework will be retired in Creatio version 8.1. We using .NET 6 to deploy Creatio version 8.0.8 and later.

.NET Core platform is an open-source cross-platform software that can be deployed on **Linux**, **Windows**, **Mac OS** systems.

We recommend using **Linux** to deploy Creatio .NET Core products. This OS is highly reliable, well-performing, has an optimal cost and is actively being developed.

## Feature support in Creatio .NET Core products [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#feature-support-in-creatio-net-core-products "Direct link to Feature support in Creatio .NET Core products")

| Feature | .NET Core Support |
| --- | --- |
| **Windows authentication** | Supported since version 7.16.4. |
| **Configuration development** ( **Configuration** section, object designer) | Supported since version 7.17.0. |
| **LDAP integration** | Supported since version 7.17.2. |
| **Fault-tolerant Redis Sentinel configuration** | We do not plan to support it. More modern fault-tolerant [Redis Cluster](https://academy.creatio.com/documents?id=2349) configuration is supported since Creatio version 7.18.0. |
| **Telephony integration** | Asterisk connector is supported since version 7.16.3.<br>We plan to support Cisco Finesse integration without using IIS and ARR in the future releases. |
| **Oracle DBMS** | We plan to support it in the future releases. |
| **Exchange\\Office365 calendar and contact synchronization** | Supported since version 7.18.2. |
| **Google Calendar and contact synchronization** | We plan to support it in the future releases. |
| **Facebook integration** | We plan to support it in the future releases. |
| **Lead registration from social networks** (Facebook and LinkedIn) | We plan to support it in the future releases. |

note

Deploy the messaging service (Creatio Messaging Service) on Windows to integrate Avaya, TAPI telephony systems.

You need to deploy the Microsoft IIS web server and its expansion — Application Request Routing (ARR) — on Windows to integrate Cisco Finesse.

## The lifecycle of products using .NET Framework and .NET Core platforms [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#the-lifecycle-of-products-using-net-framework-and-net-core-platforms "Direct link to The lifecycle of products using .NET Framework and .NET Core platforms")

Microsoft released the **.NET 5** platform, thus integrating .NET Framework and .NET Core platforms.

This allows the platform to support the maximum number of the APIs that used to be available on the .NET Framework platform. However, it is important to note that the API is not backwards compatible, therefore you need to adapt the .NET Core features previously developed using .NET Framework to ensure .NET Core and .NET 5 support.

We plan to move the Creatio product lineup to the unified .NET platform in the future.

## Developing features with simultaneous .NET Framework and .NET Core support [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#developing-features-with-simultaneous-net-framework-and-net-core-support "Direct link to Developing features with simultaneous .NET Framework and .NET Core support")

To streamline the adaptation to .NET Core and .NET 5, we recommend developing new features with simultaneous .NET Framework and .NET Core platform support.

Recommendations:

1. Your external libraries have to support .NET Standard 2.0. This will let you use them with both .NET Framework and .NET Core.
2. Your framework's API also has to support .NET Standard 2.0. You can check the compatibility using [Microsoft documentation](https://docs.microsoft.com/en-us/dotnet/api/?view=netstandard-2.0).
3. When coding configuration web services, you need to inherit from Terrasoft.Web.Common.BaseService and use HttpContextAccessor for HttpContext access. Read more: [Custom web services](https://academy.creatio.com/documents?id=15262).

Important

If you use or plan to use Creatio Marketplace applications to expand Creatio’s functionality, you will need to specify whether they support Creatio .NET Core products.

## Migrating Creatio from .NET Framework to .NET Core [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#migrating-creatio-from-net-framework-to-net-core "Direct link to Migrating Creatio from .NET Framework to .NET Core")

We plan to support Creatio migration from .NET Framework to .NET Core in the upcoming releases.

## Deploying Creatio .NET Core application [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#deploying-creatio-net-core-application "Direct link to Deploying Creatio .NET Core application")

You can find the instructions on deploying Creatio in the [Deploy Creatio .NET Core application server on Linux](https://academy.creatio.com/documents?id=2148) article.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products\#see-also "Direct link to See also")

[Prepare Creatio .NET Core setup files](https://academy.creatio.com/documents?id=2120)

[Deploy Creatio .NET Core application server on Linux](https://academy.creatio.com/documents?id=2148)

[Framework compatibility](https://academy.creatio.com/documents?id=2455)

- [Feature support in Creatio .NET Core products](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#feature-support-in-creatio-net-core-products)
- [The lifecycle of products using .NET Framework and .NET Core platforms](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#the-lifecycle-of-products-using-net-framework-and-net-core-platforms)
- [Developing features with simultaneous .NET Framework and .NET Core support](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#developing-features-with-simultaneous-net-framework-and-net-core-support)
- [Migrating Creatio from .NET Framework to .NET Core](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#migrating-creatio-from-net-framework-to-net-core)
- [Deploying Creatio .NET Core application](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#deploying-creatio-net-core-application)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/deployment_faq/creatio_net_core_products#see-also)