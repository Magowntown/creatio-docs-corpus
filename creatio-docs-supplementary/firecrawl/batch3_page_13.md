<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-faq/creatio-setup-faq)** (8.3).

Version: 8.2All Creatio products

On this page

## Which Internet Information Services (IIS) components are required for Creatio? [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq\#title-270-1 "Direct link to Which Internet Information Services (IIS) components are required for Creatio?")

To ensure the correct operation of Creatio on-site, enable the following components in the Windows **Programs and Features** menu:

1. .NET Framework 3.5:
1. Windows Communication Foundation Non-HTTP Activativation
2. Windows Communication Foundation HTTP Activation
2. .NET Framework 4.7.2

3. ASP.NET 4.7.2

4. For WCF Services:
   - HTTP Activation

   - Message Queuing (MSMQ) Activation

   - Named Pipe Activation

   - TCP Activation

   - TCP Port Sharing



     note





     Microsoft .Net Framework 4.7 or higher – for version 7.11.1 – 7.13.1, Microsoft .Net Framework 4.7.2 – for version 7.13.2 or higher;

Additionally, IIS services are key component for operation of websites and web applications deployed on Windows Server. Enable the following IIS components:

1. On the "Web Management Tools" tab:
1. IIS Management Console
2. IIS Management Script and Tools
3. IIS Management Service
2. On the "World Wide Web Services" tab:
   - For the Application Development Features component:
     - All ASP.NET elements
     - All .NET Extensibility elements
     - ISAPI extensions
     - ISAPI Filters
     - WebSocket Protocol
   - For the Common HTTP Features component:
     - Default Document
     - HTTP Errors
     - HTTP Redirection
     - Static Content
   - For the "Health and Diagnostics" component:
     - Custom Logging
     - HTTP Logging
     - Logging Tools
     - Request Monitor
   - For the "Security" component:
     - Request filtering
     - IP and Domain Restriction

## How do I switch from HTTP to HTTPS? [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq\#title-270-2 "Direct link to How do I switch from HTTP to HTTPS?")

The detailed procedure for switching from HTTP to HTTPS is covered in a separate article.

## Which account is used when you first log in to the system? [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq\#title-270-3 "Direct link to Which account is used when you first log in to the system?")

After the successful deployment of Creatio on-site, log in with these credentials: user - Supervisor, password - Supervisor.

## Does the number of active Creatio users affect the number of Microsoft SQL Server? [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq\#title-270-4 "Direct link to Does the number of active Creatio users affect the number of Microsoft SQL Server?")

The number Microsoft SQL Server users does not depend on the number Creatio users, though depends on the number of servers with databases. Please see the [System requirements](https://academy.creatio.com/documents?product=base&ver=7&id=1263) for on-site deployment

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq\#see-also "Direct link to See also")

[Set up websockets](https://academy.creatio.com/documents?product=base&ver=7&id=1631)

[Switch Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?product=base&ver=7&id=1632)

[Additional setup](https://academy.creatio.com/documents?product=base&ver=7&id=1633)

- [Which Internet Information Services (IIS) components are required for Creatio?](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#title-270-1)
- [How do I switch from HTTP to HTTPS?](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#title-270-2)
- [Which account is used when you first log in to the system?](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#title-270-3)
- [Does the number of active Creatio users affect the number of Microsoft SQL Server?](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#title-270-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-faq/creatio-setup-faq#see-also)