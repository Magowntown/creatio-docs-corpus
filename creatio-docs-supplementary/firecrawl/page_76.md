<!-- Source: page_76 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 09/12/2024

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code app development, and CRM. Today we are pushing things forward with Creatio version 8.1.5 Quantum, featuring the **following new capabilities and upgrades**.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio composable apps [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-1 "Direct link to Creatio composable apps")

### Lead Generation [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-113 "Direct link to Lead Generation")

**Spanish in Facebook forms**. You can now receive leads from Facebook forms in Spanish in all Creatio versions that support the forms.

## End user experience​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-8 "Direct link to End user experience​")

**Product gallery**. The product selection page, accessible from the order page, now includes a gallery view.

Product gallery

![Product gallery](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_5/scr_product_gallery.png)

**Timeline UX improvement**. You can now open call and chat pages directly from calls and chats in the timeline.

**Indonesian localization**. You can now use Creatio in Indonesian.

## No-code tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-9 "Direct link to No-code tools")

### Application Hub [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-2 "Direct link to Application Hub")

**Installation of large apps**. It is now possible to install apps up to 300 MB in size. Customize the limit within 300 MB in the "Max file size for installed apps" ("ApplicationInstallationMaxFileSize" code) system setting.

### Business rules [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-3 "Direct link to Business rules")

**Rule failsafe**. Failure of a single business rule no longer affects other business rules.

### Freedom UI Designer [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-10 "Direct link to Freedom UI Designer")

**Dropdown field improvements**.

- Display a secondary object column next to the field using the Field value details parameter.
Field value detail

![Field value detail](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_5/scr_field_value_detail.png)

- Display a secondary object column next to dropdown field values using the Supplementary display value parameter.
Supplementary display values

![Supplementary display values](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_5/scr_supplementary_display_value_0.png)


**Gallery improvements**.

- Specify the page to open while clicking on the caption in the component’s settings.
- Specify tile sizes in the component's settings.
- View dynamic placeholders in the Freedom UI Designer.

**Sidebar customization improvements**.

- System administrator can now customize sidebars that are available out of the box.
- You can now open the Freedom UI Designer for any sidebar by clicking the ![btn_edit.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Release_notes/release_notes_8_1_5/btn_edit.png) button in the top right.
- Creatio now includes the sidebar template page. All sidebar headers are editable.
- Creatio now validates that the sidebar code is unique.
- Sidebar management options are now available in the Freedom UI Designer out of the box without the need to turn on additional features.
- Set up sidebar permissions based on whether the user has a corresponding license.
- All new sidebars are now available only to company employees out of the box. You can make them available for external users by using operation permissions.

Learn more: [Implement the license verification from the front-end for a custom sidebar](https://academy.creatio.com/documents?id=15960&anchor=title-15960-8) (developer documentation).

### Business processes​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-11 "Direct link to Business processes​")

**New parameter type**. It is now possible to store various action-process object parameters together automatically using the new **Composite object** data type. For example, this is useful so that you can return the parameters to Copilot for further analysis.

## Advanced customization [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-13 "Direct link to Advanced customization")

**Template list**. You can now dynamically display a series of identical UI elements based on different conditions using the **Template list** component while editing the page schema. For example, you can generate a list of buttons that represent available business processes or other criteria. Learn more: [Render repeated Freedom UI components](https://academy.creatio.com/documents?id=15199), [TemplateList component](https://academy.creatio.com/documents?id=15198).

## Administration​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-14 "Direct link to Administration​")

**Two-factor authentication**. It is now possible to use two-factor authentication without additional integrations or package installation. It provides an extra level of protection by requiring you to enter a verification code in addition to the password. This helps safeguard your data from unauthorized access, even if your password is compromised or stolen. Learn more: [Set up two-factor authentication](https://academy.creatio.com/documents?id=2538), [Use two-factor authentication](https://academy.creatio.com/documents?id=2539), [Integrate the cell connection provider with Creatio for two-factor authentication via SMS](https://academy.creatio.com/documents?id=15164) (developer documentation).

**Content security policy**. Since version 8.1.5, all new websites have a CSP mechanism configured in blocking mode out of the box. This increases the level of security of the website by blocking the download of content from untrusted sources. Learn more about CSP: [Set up content security policy](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/content-security-policy).

**Chat channel deletion**. You can now only delete a chat channel if it does not contain incomplete chats.

## Beta testing of new features​ [​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes\#title-2782-17 "Direct link to Beta testing of new features​")

Important

The feature below is available for beta testing in Creatio version 8.1.5 Quantum. If you have any feedback, contact us at: `beta@creatio.com`. All feedback is appreciated.

**Integrations without licenses**. You can now integrate Creatio with third party systems without spending licenses by using technical users. A technical user is a separate Creatio user type whose purpose is to integrate Creatio with external systems. Unlike all other user types, technical users can interact with Creatio without any issued licenses. Technical users have the following restrictions:

- You cannot log in to Creatio web or mobile application using technical user credentials. Technical users can use only our API, not the UI.
- Technical users can only authenticate in Creatio using OAuth authentication.
- Out of the box, a technical user cannot access any Creatio object or operation. Only explicitly issued privileges are applied to the technical user.

To access the technical user functionality, contact [Creatio support](mailto:support@creatio.com).

- [Creatio composable apps](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-1)
  - [Lead Generation](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-113)
- [End user experience​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-8)
- [No-code tools](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-9)
  - [Application Hub](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-2)
  - [Business rules](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-3)
  - [Freedom UI Designer](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-10)
  - [Business processes​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-11)
- [Advanced customization](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-13)
- [Administration​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-14)
- [Beta testing of new features​](https://academy.creatio.com/docs/8.x/resources/release-notes/815-quantum-release-notes#title-2782-17)