<!-- Source: page_28 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/select-a-field-by-condition#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

Example

Highlight the field with the result of the activity, if its status is "Completed", the **Result** field is not filled and the **ProcessElementId** column has a value.

## Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/select-a-field-by-condition\#title-1520-1 "Direct link to Example implementation")

Highlight the field by condition

```js
// Rule for the activity edit page.
Terrasoft.sdk.Model.addBusinessRule("Activity", {
    // The name of the business rule.
    name: "ActivityResultRequiredByStatusFinishedAndProcessElementId",
    // Business rule type: custom.
    ruleType: Terrasoft.RuleTypes.Custom,
    //The rule is initiated by the Status and Result columns.
    triggeredByColumns: ["Status", "Result"],
    // The rule will work before saving the data and after changing the data.
    events: [Terrasoft.BusinessRuleEvents.ValueChanged, Terrasoft.BusinessRuleEvents.Save],
    // Handler function.
    executeFn: function(record, rule, column, customData, callbackConfig) {
        // A flag of the validity of the property and the rule.
        var isValid = true;
        // The value of the ProcessElementId column.
        var processElementId = record.get("ProcessElementId");
        // If the value is not empty.
        if (processElementId && processElementId !== Terrasoft.GUID_EMPTY) {
            // Set the validity flag.
            isValid = !(record.get("Status.Id") === Terrasoft.Configuration.ActivityStatus.Finished &&
                Ext.isEmpty(record.get("Result")));
        }
        // Change the properties of the Result column.
        record.changeProperty("Result", {
            // Set the column correctness indicator.
            isValid: {
                value: isValid,
                message: Terrasoft.LS["Sys.RequirementRule.message"]
            }
        });
        // Asynchronous return of values.
        Ext.callback(callbackConfig.success, callbackConfig.scope, [isValid]);
    }
});
```

- [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/select-a-field-by-condition#title-1520-1)