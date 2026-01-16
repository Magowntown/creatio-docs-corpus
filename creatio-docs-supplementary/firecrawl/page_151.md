<!-- Source: page_151 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3

On this page

Level: beginner

WhatsApp is a Meta product. Due to this, you need the following to integrate this messenger:

- A **Meta Business Manager** account. If you have not signed up yet, follow the [Meta instructions](https://www.facebook.com/business/help/1710077379203657?id=180505742745347).
- Integration with a Facebook partner platform that provides access to WhatsApp Business API. You can use **Twilio**.

You can sign up for a trial account with limited functionality to **get acquainted** with the WhatsApp integration features. **Verify your accounts** to take full advantage of WhatsApp integration. This will help you secure your and your customers' data. In general, the WhatsApp integration setup consists of the following steps:

1. Set up a Twilio free trial account to get acquainted with the integration (optional). [Read more >>>](https://academy.creatio.com/documents?id=2355&anchor=title-2025-1)
2. Set up a Twilio business account. [Read more >>>](https://academy.creatio.com/documents?id=2355&anchor=title-2025-4)
3. Set up a WhatsApp chat channel in Creatio. [Read more >>>](https://academy.creatio.com/documents?id=2355&anchor=title-2025-5)

File transfer in WhatsApp channel is **limited** to:

- **Receiving files**. At the moment, Creatio only works with incoming files, sending files is not available.

- **File size** up to 16 Mb.

- **File formats**:
  - Images: \*.jpg, \*.jpeg, \*.png.
  - Audio files: \*.mp3, \*.ogg, \*.amr.
  - Documents: \*.pdf.
  - Videos: \*.mp4.

To enable Twilio to send media files, turn off the **HTTP Basic Authentication for media access** setting in Twilio. Learn more about supported file formats in [Twilio documentation](https://www.twilio.com/docs/whatsapp/guidance-whatsapp-media-messages).

note

Twilio is partnered with telecom service providers in a limited number of countries. View the country list in [Twilio documentation](https://support.twilio.com/hc/en-us/articles/115000781088-International-Porting-Process). Besides the specified countries, Twilio has no restrictions on US phone numbers. If your number is not eligible, follow [Twilio instructions](https://support.twilio.com/hc/en-us/articles/360052171393-Can-I-activate-my-own-phone-number-for-WhatsApp-on-Twilio-).

While you can connect multiple WhatsApp numbers to a single Creatio instance, we recommend connecting a particular WhatsApp number only to a single Creatio instance. If you add the number to several instances, e. g., development, testing, and production environments, only the last integrated instance will receive messages.

## Set up a trial account (optional) [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#title-2025-1 "Direct link to Set up a trial account (optional)")

You can set up a Twilio free trial account without verification and subscription to paid platform services. This will let you test Creatio WhatsApp integration, including messaging and file transfer. To set up the test integration:

1. Set up a Twilio free trial account. [Read more >>>](https://academy.creatio.com/documents?id=2355&anchor=title-2025-2)
2. Set up a WhatsApp chat channel in Creatio [Read more >>>](https://academy.creatio.com/documents?id=2355&anchor=title-2025-3)

### Set up a Twilio free trial account [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#title-2025-2 "Direct link to Set up a Twilio free trial account")

1. **Sign up** on [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio). You will be able to set up a test integration after the signup. Twilio will grant you limited virtual funds to help you review the functionality.



note





Should you decide to convert the account to a full-fledged business account, the trial features and virtual funds will become unavailable. We recommend using separate accounts for working and testing purposes.

2. **Specify the endpoint URL** for transferring chats to Creatio. To do this, navigate to the sandbox settings in Twilio:

[Twilio Console](https://www.twilio.com/console) → Messaging → Try it out → Send a WhatsApp message → Sandbox Settings → Sandbox Configuration and enter the `https://sm-receiver.creatio.com/api/webhook/LeadGen/whatsapp` value in the **WHEN A MESSAGE COMES IN** field.

3. **Set up the Twilio sandbox**: [Twilio Console](https://www.twilio.com/console) → Messaging → Try it out → Send a WhatsApp message.

4. Twilio will generate a code. **Send the code** from your phone number to your trial account number using WhatsApp. Twilio will notify you upon success. As a result, Twilio will add your number to Sandbox Participants.

5. If you would like to use several test numbers, **repeat step 3** for each of them. To review the test numbers in the Sandbox Participants list, go to Twilio Console → Messaging → Try it out → Send a WhatsApp message → Sandbox settings → Sandbox Participants. After that your trial account number will be able to receive messages from the numbers you added in the previous step.


### Set up a test WhatsApp channel in Creatio [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#title-2025-3 "Direct link to Set up a test WhatsApp channel in Creatio")

Before you start setting up the WhatsApp channel, make sure the following system settings are populated:

- "Identity server Url" ("IdentityServerUrl" code)
- "Identity server client id" ("IdentityServerClientId" code)
- "Identity server client secret" ("IdentityServerClientSecret" code)

If the values of these system settings are not populated, contact [Creatio support](mailto:support@creatio.com).

1. Click the ![](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/Chats/btn_system_designer_0.png) button to **open the System Designer**.

2. **Click Chat settings**.

3. **Click**![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/Chats/btn_chapter_mobile_wizard_new_role.png) button in the **Channels** list. Select "WhatsApp" in the drop-down menu. This will open a mini page with the channel parameters.

4. **Fill out the channel parameters**:



| Parameter | Value |
| --- | --- |
| Phone number | Your Twilio free trial account phone number. |
| Application Id | The Twilio free trial account SID specified in the **ACCOUNT SID** field of the Twilio Console. |
| Token | The token Twilio generates for the trial account. Specified in the **AUTH TOKEN** field of the Twilio Console. |
| Queue | Select the chat queue that will process the messages that come via this channel. |
| Language | Select the expected channel message language. This will let the agents use quick reply templates in the customer language. |

5. Click **Save**.


**As a result**, Creatio will connect a test WhatsApp channel. You will be able to receive and process test messages and files.

## Set up a business account [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#title-2025-4 "Direct link to Set up a business account")

Sign up for Twilio and complete the verification to take advantage of all Twilio business features. Learn more in [Twilio documentation](https://www.twilio.com/docs/whatsapp/tutorial/connect-number-business-profile).

note

Follow WhatsApp [display name guidelines](https://developers.facebook.com/docs/whatsapp/guides/display-name/) when filling out your profile.

The general setup procedure is as follows:

1. **Sign up** for [Meta Business Manager](https://business.facebook.com/overview).
1. If your company **already has an account**, proceed to step 2.
2. If your company **does not have an account yet**, follow the instructions in [Meta documentation](https://www.facebook.com/business/help/1710077379203657?id=180505742745347).
2. **Sign up** for [Twilio](https://www.twilio.com/).

3. **Submit the WhatsApp sender** to Twilio.
1. Add the **phone number**:

      Go to Twilio Console → Messaging → Senders → WhatsApp Senders and click the **New WhatsApp Sender** button.

      You can use [your own phone number](https://support.twilio.com/hc/en-us/articles/360052171393-Can-I-activate-my-own-phone-number-for-WhatsApp-on-Twilio-) or buy a [Twilio number](https://www.twilio.com/console/phone-numbers/search).

2. Specify the endpoint URL for transferring chats to Creatio. To do this, navigate to the Twilio account settings: Twilio console → Messaging → Senders → WhatsApp senders → Edit sender → enter [https://sm-receiver.creatio.com/api/webhook/LeadGen/whatsapp](https://sm-receiver.creatio.com/api/webhook/LeadGen/whatsapp) in the **Webhook URL for incoming messages** field.

3. Allow Twilio to **send messages** on your behalf. To do this, go to Meta Business Manager and approve Twilio's request to send messages on your company's behalf. To approve the request:
      - Go to business.facebook.com → Settings → Business Settings → Requests → **Approve**
      - Follow the link in the initial phone number confirmation email
4. **Verify your Meta Business Manager account**. If you have already verified your business account, proceed to the next step. To verify your business account:

      Go to Meta Business Manager → Settings → Business Settings → Security Center and click the **Start verification** or **Continue** button in the **Verification** section.

      Learn more about verifying the business in [Meta documentation](https://www.facebook.com/business/help/2058515294227817?id=180505742745347).

After you approve Twilio to message on your behalf, Twilio will complete the registration process for your WhatsApp sender. You will receive an email confirmation that Twilio finalized the registration of your profile.

**As a result**, you will be able to communicate with customers using WhatsApp via the registered number within 24 hours after the verification.

## Add a WhatsApp channel to Creatio [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#title-2025-5 "Direct link to Add a WhatsApp channel to Creatio")

Before you start setting up the WhatsApp channel, make sure the following system settings are populated:

- "Identity server Url" ("IdentityServerUrl" code)
- "Identity server client id" ("IdentityServerClientId" code)
- "Identity server client secret" ("IdentityServerClientSecret" code)

If the values of these system settings are not populated, contact [Creatio support](mailto:support@creatio.com).

1. Click the ![](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/Chats/btn_system_designer_0.png) button to **open the System Designer**.

2. **Click Chat settings**.

3. **Click** the ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/Chats/btn_chapter_mobile_wizard_new_role.png) button in the **Channels** list → "WhatsApp". This will open a mini page with channel parameters.

4. **Fill out the channel parameters**:



| Parameter | Value |
| --- | --- |
| Phone number | Your Twilio free trial account phone number. |
| Application Id | The Twilio free trial account SID specified in the **ACCOUNT SID** field of the Twilio Console. |
| Token | The token Twilio generates for the trial account. Specified in the **AUTH TOKEN** field of the Twilio Console. |
| Queue | Select the chat queue that will process the messages that come via this channel. |
| Language | Select the expected channel message language. This will let the agents use quick reply templates in the customer language. |

5. **Click Save**.
Fig. 1 Setting up a WhatsApp channel

![Fig. 1 Setting up a WhatsApp channel](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/Chats/8_1/scr_setup_chat_channel_whatsapp.png)


**As a result**, this will connect a WhatsApp channel to Creatio. Contact center agents will be able to process messages received via this channel in the communication panel and view the chat history in the **Chats** section.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration\#see-also "Direct link to See also")

[Set up chat processing](https://academy.creatio.com/documents?id=2382)

[Chat access](https://academy.creatio.com/documents?id=2383)

[Set up Facebook Messenger integration](https://academy.creatio.com/documents?id=2384)

[Set up Telegram integration](https://academy.creatio.com/documents?id=2354)

[Work with chats](https://academy.creatio.com/documents?id=2378)

- [Set up a trial account (optional)](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#title-2025-1)
  - [Set up a Twilio free trial account](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#title-2025-2)
  - [Set up a test WhatsApp channel in Creatio](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#title-2025-3)
- [Set up a business account](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#title-2025-4)
- [Add a WhatsApp channel to Creatio](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#title-2025-5)
- [See also](https://academy.creatio.com/docs/8.x/no-code-customization/base-integrations/set-up-chats/whatsapp/set-up-whatsapp-integration#see-also)