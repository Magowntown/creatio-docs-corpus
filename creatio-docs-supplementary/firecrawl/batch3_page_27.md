<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/chat-access-setup#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/chat-access-setup)** (8.3).

Version: 8.2All Creatio products

On this page

To manage Facebook Messenger and WhatsApp chat channels in Creatio on-site:

- Switch Creatio from HTTP to HTTPS. Learn more in a separate article: [Switch a Creatio website from HTTP to HTTPS](https://academy.creatio.com/documents?id=1632).
- Set up access to the chat service at `https://sm-account.creatio.com/` on the application server.
- Set up an incoming connection to HTTPS protocol and protection by a valid certificate for the sm-account.creatio.com chat service on the application server.
- Ensure that the firewall whitelist includes the `mcs.us1.twilio.com/*` domain so that the WhatsApp chat channel can receive messages.

To manage Telegram chat channels, make sure the application server has internet access.

If your Creatio application uses two-factor authentication, grant FacebookOmnichannelMessagingService, TelegramOmnichannelMessagingService, WhatsappOmnichannelMessagingService services access to incoming requests.

To manage **Ada chat** channels in Creatio on-site, make sure the Creatio webhook service is available. Learn more: [Work with webhooks basics](https://academy.creatio.com/documents?id=2412).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/chat-access-setup\#see-also "Direct link to See also")

[Set up chat](https://academy.creatio.com/documents?id=2382)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/chat-access-setup#see-also)