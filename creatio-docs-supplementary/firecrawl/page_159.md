<!-- Source: page_159 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

Administrators have to ensure that end users have access to the apps they need for their work. To do this, administrators can use Microsoft Intune to manage the custom apps that users use. This functionality also facilitates additional data protection while managing devices. Learn more: [official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/apps/app-management).

To **manage the Creatio Mobile app for iOS**, follow the instructions: [Manage the Creatio Mobile app for iOS using Microsoft Intune](https://academy.creatio.com/documents?id=15212).

Before you start managing the Android app in Microsoft Intune:

1. **Sign in to the** [Microsoft Intune admin center](https://intune.microsoft.com/).
2. **Make sure your user has the "Application administrator" role**.

## 1\. Create a group to manage users and add users to the group [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-1 "Direct link to 1. Create a group to manage users and add users to the group")

Instructions: [official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/fundamentals/quickstart-create-group).

For example, create the "Mobile users" group.

## 2\. Add the Android app to the Microsoft Intune admin center [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-2 "Direct link to 2. Add the Android app to the Microsoft Intune admin center")

Add the Creatio Mobile app for Android to the Microsoft Intune admin center using app package file.

1. **Contact** [Creatio support](mailto:support@creatio.com) to receive the app package file for the Android app.

2. **Click Apps** → **All Apps** → **Create**.

3. **Set App type property to "Line-of-business app."**

4. **Click Select**. This opens the **Add App** page.

5. **Fill out the app properties**.



| Property | Property value |
| --- | --- |
| App information tab |
| Select file | Click **Select app package file** → ![scr_add_file.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_add_file.png) → select the "app-intune-release.apk" file provided by Creatio support → **OK** |
| Publisher | An arbitrary value. For example, "Creatio." |
| Target platform | Android device administrator |
| Category | Business |
| Assignments tab |
| Available with or without enrollment | Click **Add group** → select your group → **Select** |

6. **Click Create**.


**As a result**, your Creatio Mobile app for Android will be added to the Microsoft Intune.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.3/scr_android_app_in_microsoft_intune.png)

## 3\. Create the Android app compliance policy [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-3 "Direct link to 3. Create the Android app compliance policy")

1. **Click Devices** → **Manage devices** → **Compliance** → **Policies** tab → **Create policy**.

2. **Set Platform property to "Android device administrator."**

3. **Click Create**. This opens the **Android compliance policy** page.

4. **Fill out the policy properties**.



| Property | Property value |
| --- | --- |
| Basics tab |
| Name | An arbitrary value. For example, "Android." |
| Assignments tab |
| Included groups | Click **Add groups** → select your group → **Select** |

5. **Click Create**.


**As a result**, the compliance policy for the Creatio Mobile app for Android will be created.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.3/scr_android_compliance_policy.png)

## 4\. Set up the Android protection policies [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-4 "Direct link to 4. Set up the Android protection policies")

If you need to **use previously created protection policy**, refresh the configuration. To do this, change some of Mobile Application Management parameters. For example, restrict Copy/Paste operation. [Read more >>>](https://academy.creatio.com/documents?id=15079&anchor=restrict-copy-paste-operation)

To set up the Android protection policies:

1. **Click Apps** → **Manage apps** → **Protection** → **Create** → **Android**.

2. **Fill out the policy properties**.



| Property | Property value |
| --- | --- |
| Basics tab |
| Name | An arbitrary value. For example, "Android." |
| Apps tab |
| Custom apps | Click **Select custom apps** → select "app-intune-release.apk" → **Select** |
| Assignments tab |
| Included groups | Click **Add groups** → select your group → **Select** |

3. **Click Create**.


**As a result**, the protection policy for the Creatio Mobile app for Android will be configured.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.3/scr_android_protection_policy.png)

If you need, **set up an additional data protection policy**. For example, restrict Copy/Paste operation. To do this:

1. **Click Apps** → **Manage devices** → **Protection** → select the policy → **Properties** → **Data protection** → **Edit**.

2. **Edit the data protection properties**.



| Property | Property value |
| --- | --- |
| Data protection tab → Data transfer block |
| Restrict cut, copy, and paste between other apps | Blocked |
| Cut and copy character limit for any app | 10 |

3. **Click Review + save**.

4. **Click Save**.


**As a result**, the protection policy for the Creatio Mobile app for Android will include the additional settings.

## 5\. Set up the Android device management [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-5 "Direct link to 5. Set up the Android device management")

Set up device administrator enrollment. Instructions: [official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/enrollment/android-enroll-device-administrator).

## 6\. Apply the changes [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#title-15079-6 "Direct link to 6. Apply the changes")

1. **Re-login to your mobile portal**.
2. **Reinstall the Creatio Mobile for Intune app**.

**As a result**, Creatio Mobile app for Android will be available to administrators via Microsoft Intune with managed security policies.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#see-also "Direct link to See also")

[Manage the Creatio Mobile app for iOS using Microsoft Intune](https://academy.creatio.com/documents?id=15212)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android\#resources "Direct link to Resources")

[Official Microsoft Intune documentation](https://learn.microsoft.com/en-us/mem/intune/)

- [1\. Create a group to manage users and add users to the group](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-1)
- [2\. Add the Android app to the Microsoft Intune admin center](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-2)
- [3\. Create the Android app compliance policy](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-3)
- [4\. Set up the Android protection policies](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-4)
- [5\. Set up the Android device management](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-5)
- [6\. Apply the changes](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#title-15079-6)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/microsoft-intune/mobile-creatio-for-android#resources)