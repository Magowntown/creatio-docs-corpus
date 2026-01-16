<!-- Source: page_113 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy)** (8.3).

Version: 8.0

On this page

Level: beginner

The telephony features in Creatio vary depending on the connected phone system. By default, Creatio is integrated with Webitel telephone service. If necessary, you can connect a different system.

Below is a feature comparison table for different phone systems:

| TAPI | Cisco Finesse | Avaya | Webitel | Asterisk | CallWay | Velvetel |
| --- | --- | --- | --- | --- | --- | --- |
| "Search by caller ID" phone system functionality |
| [Note 1](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-1) | + | + | + | + | + | + |
| "Make outgoing calls" phone system functionality |
| + | + | + | + | [Note 2](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-2) | [Note 3](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-3) | + |
| "Receive incoming calls" phone system functionality |
| + | + | + | + | − | [Note 4](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-5) | + |
| "Place calls on hold, unhold calls" phone system functionality |
| + | + | + | + | + | + | + |
| "End calls" phone system functionality |
| + | + | + | + | + | + | + |
| "Manage agent status" phone system functionality |
| [Note 5](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-6) | + | + | + | − | + | + |
| "Transfer calls" phone system functionality |
| + | + | + | + | + | + | + |
| "Save the information to **Calls** section" phone system functionality |
| + | + | + | + | + | + | + |
| "Call from browser" phone system functionality |
| − | − | − | + | − | − | + |
| "Replay calls" phone system functionality |
| − | − | − | + | − | − | + |
| Telephone system versions |
| All phone systems that use TAPI 2.X | Cisco Finesse 11.5+ | AES v5.2-10.1 |  | 13, 16, 18 |  |  |

### Notes [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-7 "Direct link to Notes")

#### 1 [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-1 "Direct link to 1")

Due to TAPI limitations, caller identification is unavailable for calls routed through UCCX while using CUCM.

#### 2 [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-2 "Direct link to 2")

The user might have to respond to an incoming system call to initiate an outgoing call from Creatio. The call flow depends on the software/hardware phone version/model.

#### 3 [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-3 "Direct link to 3")

CallWay software phones are fully supported. If the agent uses a different IP or software phone, they have to respond to an incoming "system" call to initiate an outgoing call from Creatio.

#### 4 [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-5 "Direct link to 4")

Only CallWay software phones are fully supported.

#### 5 [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#title-2356-6 "Direct link to 5")

The following 2 statuses are available: "Ready" and "Do not disturb" (DND). Cisco is currently not supported.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy\#see-also "Direct link to See also")

[Set up integration with Webitel](https://academy.creatio.com/documents?id=1366)

[Set up integration with Asterisk](https://academy.creatio.com/documents?id=1368)

[Set up integration with Avaya](https://academy.creatio.com/documents?id=1373)

[Set up integration with Cisco Finesse](https://academy.creatio.com/documents?id=1369)

[Set up integration with TAPI](https://academy.creatio.com/documents?id=1370)

[Set up integration with CallWay](https://academy.creatio.com/documents?id=1371)

[Set up integration with Infinity X](https://academy.creatio.com/documents?id=1372)

[Set up integration with Velvetel (vendor's documentation)](https://velvetech.atlassian.net/wiki/spaces/VVTL/pages/1093238987/Connector+Installation)

- [Notes](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#title-2356-7)
- [See also](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/base-integrations/phone-integration-connectors/feature-comparison-for-supported-phone-systems%20copy#see-also)