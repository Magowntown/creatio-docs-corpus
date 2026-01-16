<!-- Source: page_80 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

## Example 1 [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-2 "Direct link to Example 1")

Example

Filter values in a column by condition.

When selecting a value in the **Product** lookup column, only the products containing the `true` value in the **Active** column of the **Product in invoice** detail are available.

### Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-1 "Direct link to Example implementation")

Filtration example

```js
Terrasoft.sdk.Model.addBusinessRule("InvoiceProduct", {
    ruleType: Terrasoft.RuleTypes.Filtration,
    events: [Terrasoft.BusinessRuleEvents.Load],
    triggeredByColumns: ["Product"],
    filters: Ext.create("Terrasoft.Filter", {
        modelName: "Product",
        property: "Active",
        value: true
    })
});
```

## Example 2 [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-4 "Direct link to Example 2")

Example

Filter values in a column by the value in another column.

The **Contact** field on the record edit page of the **Invoices** section should be filtered based on the **Account** field value.

### Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-1 "Direct link to Example implementation")

Filtration example

```js
Terrasoft.sdk.Model.addBusinessRule("Invoice", {
    ruleType: Terrasoft.RuleTypes.Filtration,
    events: [Terrasoft.BusinessRuleEvents.Load, Terrasoft.BusinessRuleEvents.ValueChanged],
    triggeredByColumns: ["Account"],
    filteredColumn: "Contact",
    filters: Ext.create("Terrasoft.Filter", {
        property: "Account"
    })
});
```

## Example 3 [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-6 "Direct link to Example 3")

Example

Add and delete filtration by custom logic.

### Example implementation [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values\#title-1519-1 "Direct link to Example implementation")

Filtration example

```js
Terrasoft.sdk.Model.addBusinessRule("Activity", {
    name: "ActivityResultByAllowedResultFilterRule",
    position: 1,
    ruleType: Terrasoft.RuleTypes.Custom,
    triggeredByColumns: ["Result"],
    events: [Terrasoft.BusinessRuleEvents.ValueChanged, Terrasoft.BusinessRuleEvents.Load],
    executeFn: function(record, rule, column, customData, callbackConfig) {
        var allowedResult = record.get("AllowedResult");
        var filterName = "ActivityResultByAllowedResultFilter";
        if (!Ext.isEmpty(allowedResult)) {
            var allowedResultIds =  Ext.JSON.decode(allowedResult, true);
            var resultIdsAreCorrect = true;
            for (var i = 0, ln = allowedResultIds.length; i < ln; i++) {
                var item = allowedResultIds[i];
                if (!Terrasoft.util.isGuid(item)) {
                    resultIdsAreCorrect = false;
                    break;
                }
            }
            if (resultIdsAreCorrect) {
                var filter = Ext.create("Terrasoft.Filter", {
                    name: filterName,
                    property: "Id",
                    funcType: Terrasoft.FilterFunctions.In,
                    funcArgs: allowedResultIds
                });
                record.changeProperty("Result", {
                    addFilter: filter
                });
            } else {
                record.changeProperty("Result", {
                    removeFilter: filterName
                });
            }
        } else {
            record.changeProperty("Result", {
                removeFilter: filterName
            });
        }
        Ext.callback(callbackConfig.success, callbackConfig.scope, [true]);
    }
});
```

- [Example 1](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-2)
  - [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-1)
- [Example 2](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-4)
  - [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-1)
- [Example 3](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-6)
  - [Example implementation](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/examples/filter-values#title-1519-1)