<!-- Source: page_6 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: advanced

**Business rules** represent a Creatio mechanism that enables setting up the behavior of record edit page fields. You can use business rules to, e.g., set up visible or required fields, make fields enabled, etc.

Important

Business rules work only on record edit and view pages.

Adding business rules to a page is performed via the `Terrasoft.sdk.Model.addBusinessRule(name, config)` method, where

- `name` – is the name of the model, bound to the edit page, e.g., "Contact."
- `config` – is the object defining business rule properties. The list of properties depends on a specific business rule type.

In the mobile application you can add business rule that implements custom logic (custom business rule). The `Terrasoft.RuleTypes.Custom` method is provided for this type of business rules.