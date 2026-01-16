<!-- Source: page_103 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

## Common parameters [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings\#title-15969-1 "Direct link to Common parameters")

```cli
name
```

Name of your app.

```cli
web_resources_path
```

Path to the directory that contains the resources used in the app, i. e., the logo and background on the login page.

```cli
tasks
```

Actions the utility executes. This is a string array where you can specify a combination of the tasks.

Available values

|     |     |
| --- | --- |
| prepare | Preparation/rebranding of your iOS/Android project. This step makes all the necessary changes. You will get a finished project you can publish in AppStore and Google Play. |
| build | Build the project. You will get an assembled \*.ipa iOS app file and/or \*.apk Android app file. |
| deploy | Publish the app to TestFlight. iOS only. |

```cli
use_extended_logging
```

Show detailed logs in the terminal when the utility is running. The recommended value is `true`. If set to `false`, the terminal displays only the currently executed step without details.

```cli
server_url
```

Default server. The server URL will be automatically specified on the login page when you log in to the app for the first time.

```cli
repository_path
```

Path to the GitLab repository that hosts the original Android/iOS project.

```cli
source_path
```

Path to the local Windows/Mac directory where the original Android/iOS project is located. If you specify this parameter the utility uses it in place of the `repository_path` parameter.

```cli
google_service_info_file
```

Path to the `GoogleService-Info.plist` (iOS) or `google-services.json` (Android) file downloaded from the Firebase project. Required to connect to the Firebase push notification service.

```cli
version_number
```

App version in the following format: `0.0.1`.

```cli
build_number
```

Build number (string). Always update the build number before you perform the `deploy` task.

```cli
launch_storyboard_image_path
```

Path to the image displayed when the app starts (2732x2732 px). iOS only.

```cli
app_identifier
```

A unique app ID, for example, `com.myapp.mobile`. This is the Bundle ID specified when you registered the app in App Store Connect. iOS only.

```cli
app_icon_path
```

Path to the app icon (1024x1024 px). This is a master image the utility uses to generate the required icons for current iOS devices. iOS only.

```cli
app_store_login
```

Account (Apple ID) required to connect to App Store Connect / TestFlight. iOS only.

```cli
certificate_path
```

Path to the distribution certificate required when publishing to TestFlight. iOS only.

```cli
certificate_password
```

Certificate password. To restore the password, contact the certificate author. iOS only.

```cli
apple_2FA_specific_password
```

Specific password. iOS only.

Currently, all Apple accounts support two-factor authentication. To enable third-party services to connect to Apple services, the `app-specific passwords` were added. To get a specific password:

1. Open the [Apple ID](https://appleid.apple.com/#!&page=signin) URL while signed in to your Apple account.
2. Open the **Security** section → **Generate password...** command.
3. Follow the instructions to get a new password generated.

```cli
testflight_changelog
```

Description of the published changes to TestFlight (what’s new). The description is published for the primary app language set in App Store. iOS only.

```cli
app_provision_name
```

Distribution provisioning name to sign the Creatio app target.

```cli
callerid_app_provision_name
```

Distribution provisioning name to sign the `CallerId` target in the Creatio project.

```cli
build_type
```

Build type. Android only.

Available values

|     |     |
| --- | --- |
| debug | Build for debugging |
| release | Release build |
| bundleRelease | Release build for Google Play platform |
| release-unsigned | Unsigned build |
| intuneRelease | Build for Microsoft Intune integration |

```cli
package_name
```

A unique app ID, for example, `com.myapp.mobile`. Android only.

```cli
native_resources_path
```

Path to app resources, such as the app icon and the startup image. Learn more: [official vendor documentation](https://developer.android.com/studio/write/create-app-icons#about).

Structure the contents of this directory similarly to the `res` folder in the Android project. The directory can contain subdirectories that have drawable, drawable-xhdpi, and other icons. Android only.

```cli
key_file
```

Path to the key file (keystore) required to sign the app. Learn more: [official vendor documentation](https://developer.android.com/studio/publish/app-signing). Android only.

```cli
store_password
```

Password for the keystore required to sign the app. Android only.

```cli
key_alias
```

The key alias. Android only.

```cli
key_password
```

The password of the alias from the `key_alias` parameter in the keystore. Android only.

## Microsoft Intune parameters [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings\#title-15969-2 "Direct link to Microsoft Intune parameters")

```cli
intune_config
```

Configuration for building wrapped/integrated Intune app. The list of parameters is based on the mobile OS.

Available values (Android only)

|     |     |
| --- | --- |
| app\_wrapping\_tool\_script\_path | Path to the directory that includes Intune wrapping tool. |
| build\_tools\_path | Path to the Android build tools usually installed with Android Studio. Learn more: [Launch the mobile app emulator created in Android Studio](https://academy.creatio.com/documents?id=15029). |

Available values (iOS only)

|     |     |
| --- | --- |
| intune\_mam\_packager\_path | Path to the Intune wrapping tool. |
| intune\_app\_provision\_file\_path | Path to the distribution provisioning file. |
| intune\_callerid\_app\_provision\_file\_path | Path to the `CallerId` distribution provisioning file. |
| intune\_sha1 | SHA1 of Apple/iOS Distribution certificate.<br>Instructions: official [macOS](https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request) and [Windows](https://learn.microsoft.com/en-us/xamarin/ios/deploy-test/app-distribution/app-store-distribution/?tabs=windows#creating-a-distribution-certificate) vendor documentation. |

- [Common parameters](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings#title-15969-1)
- [Microsoft Intune parameters](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings#title-15969-2)