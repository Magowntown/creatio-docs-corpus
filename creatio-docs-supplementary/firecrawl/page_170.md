<!-- Source: page_170 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/generate-the-title-of-an-activity#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Implement generating the activity header for the FieldForce solution.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/generate-the-title-of-an-activity\#title-1522-1 "Direct link to Example implementation")

Generating the activity header

```js
Terrasoft.sdk.Model.addBusinessRule("Activity", {
    name: "FieldForceActivityTitleRule",
    ruleType: Terrasoft.RuleTypes.Custom,
    triggeredByColumns: ["Account", "Type"],
    events: [Terrasoft.BusinessRuleEvents.ValueChanged, Terrasoft.BusinessRuleEvents.Load],
    executeFn: function(record, rule, column, customData, callbackConfig, event) {
        if (event === Terrasoft.BusinessRuleEvents.ValueChanged || record.phantom) {
            var type = record.get("Type");
            var typeId = type ? type.get("Id") : null;
            if (typeId !== Terrasoft.Configuration.ActivityTypes.Visit) {
                Ext.callback(callbackConfig.success, callbackConfig.scope, [true]);
                return;
            }
            var account = record.get("Account");
            var accountName = (account) ? account.getPrimaryDisplayColumnValue() : "";
            var title = Ext.String.format("{0}: {1}", Terrasoft.LocalizableStrings.FieldForceTitlePrefix, accountName);
            record.set("Title", title, true);
        }
        Ext.callback(callbackConfig.success, callbackConfig.scope, [true]);
    }
});
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/generate-the-title-of-an-activity#title-1522-1)