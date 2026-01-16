<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-entra#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3

On this page

You can enable Just-In-Time User Provisioning when setting up the identity provider integration. Read more: [Single Sign-On via Microsoft Entra AD](https://academy.creatio.com/documents?id=2393).

When JIT is enabled and a new user logs in via SSO, Creatio automatically adds a new user, grants them all available licenses, and creates a corresponding contact. The contact columns are populated based on the columns mapped in the SAML settings in Creatio. To map additional columns:

1. Click ![btn_system_designer.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/jit_via_entra_ad/btn_system_designer.png) to **open the System Designer**.
2. **Go to** the **Users and administration** block → **Single Sign On configuration**.
3. **Go to** the **SAML data to contact fields mapping** expanded list → double-click any column value (Fig. 2). This opens a lookup page.Fig. 2 SAML data to contact fields mapping expanded list

![Fig. 2 SAML data to contact fields mapping expanded list](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/jit_via_entra_ad/scr_single_sign_on_settings.png)

4. **Click** **New** on the lookup page.
5. **Enter the Entra AD column name** in the **SAML field attribute** column.
6. **Click**![btn_dropdown.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/jit_via_entra_ad/btn_dropdown.png) → select the corresponding contact field in the **Contact field name** column.
7. **Click**![btn_confirm.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/jit_via_entra_ad/btn_confirm.png).
8. **Repeat steps 5-7** for other relevant columns.

As a result, when an existing user logs in via SSO, their **Username** Creatio field will be mapped to the value of the **Unique User Identifier (Name ID)** claim in Entra. For example, if the claim value is set to user email and the user logs in as [example@outlook.com](mailto:example@outlook.com) via SSO, the **Username** field in Creatio must have the same value. You can change the value of this claim in Entra if needed.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-entra\#see-also "Direct link to See also")

[Single Sign-On via Microsoft Entra AD](https://academy.creatio.com/documents?id=2393)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/authentication/set-up-jit/just-in-time-user-provisioning-via-entra#see-also)