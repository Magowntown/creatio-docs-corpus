<!-- Source: page_137 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/reset-negative-values-to-0#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Implement the logic for dropping negative values to 0.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/reset-negative-values-to-0\#title-1521-1 "Direct link to Example implementation")

Reset negative values to 0

```js
Terrasoft.sdk.Model.addBusinessRule("Opportunity", {
    name: "OpportunityAmountValidatorRule",
    ruleType: Terrasoft.RuleTypes.Custom,
    triggeredByColumns: ["Amount"],
    events: [Terrasoft.BusinessRuleEvents.ValueChanged, Terrasoft.BusinessRuleEvents.Save],
    executeFn: function(model, rule, column, customData, callbackConfig) {
        var revenue = model.get("Amount");
        if ((revenue < 0) || Ext.isEmpty(revenue)) {
            model.set("Amount", 0, true);
        }
        Ext.callback(callbackConfig.success, callbackConfig.scope);
    }
});
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/reset-negative-values-to-0#title-1521-1)