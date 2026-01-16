<!-- Source: page_87 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: advanced

## Base business rule [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-1 "Direct link to Base business rule")

The base business rule is an abstract class, i.e., all business rules should be its inheritors.

The properties of the `config` configuration object that can be used by the inheritors of the business rule.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

The type of rule. The value must be included into the `Terrasoft.RuleTypes` enumeration.

```js
triggeredByColumns
```

The column array that triggers the rule.

```js
message
```

A text message displayed under the control element connected with the column in case business rule is not executed. It is necessary for rules that inform a user of warnings.

```js
name
```

A unique name of a business rule. It is necessary if you need to delete a rule by the `Terrasoft.sdk` methods.

```js
position
```

A position of a business rule that defines its order priority in the current queue.

```js
events
```

An event array, defining the time of running business rules. It should contain values included into the `Terrasoft.BusinessRuleEvents` enumeration.

Available values (Terrasoft.BusinessRuleEvents)

|     |     |
| --- | --- |
| Save | the rule is executed before saving the data |
| ValueChanged | the rule is executed when the data is modified (while editing) |
| Load | the rule is executed when the edit page is opened |

## **Is required** business rule (Terrasoft.RuleTypes.Requirement) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-2 "Direct link to title-1523-2")

Defines whether an edit page field is required.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.Requirement` value for this rule.

```js
requireType
```

Verification type. The value must be included into the `Terrasoft.RequirementTypes` enumeration. The rule can verify one or all the columns from `triggeredByColumns`.

```js
triggeredByColumns
```

The column array that triggers the rule. If the verification type equals `Terrasoft.RequirementTypes.Simple`, one column in the array should be specified.

Available values (Terrasoft.RequirementTypes)

|     |     |
| --- | --- |
| Simple | value verification in one column |
| OneOf | one of the columns specified in the `triggeredByColumns` should be populated |

Use case

```js
Terrasoft.sdk.Model.addBusinessRule("Contact", {
    ruleType: Terrasoft.RuleTypes.Requirement,
    requireType : Terrasoft.RequirementTypes.OneOf,
    events: [Terrasoft.BusinessRuleEvents.Save],
    triggeredByColumns: ["HomeNumber", "BusinessNumber"],
    columnNames: ["HomeNumber", "BusinessNumber"]
});
```

## Visibility business rule (Terrasoft.RuleTypes.Visibility) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-3 "Direct link to Visibility business rule (Terrasoft.RuleTypes.Visibility)")

You can hide and display fields per condition using this rule.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.Visibility` value for this rule.

```js
triggeredByColumns
```

The column array that triggers the rule.

```js
events
```

An event array, defining the time of running business rules. It should contain values included into the `Terrasoft.BusinessRuleEvents` enumeration.

```js
conditionalColumns
```

Condition array of business rule execution. Usually, these are specific column values.

```js
dependentColumnNames
```

Column name array that the business rule is applied to.

Use case

```js
Terrasoft.sdk.Model.addBusinessRule("Account", {
    ruleType: Terrasoft.RuleTypes.Visibility,
    conditionalColumns: [\
        {name: "Type", value: Terrasoft.Configuration.Consts.AccountTypePharmacy}\
    ],
    triggeredByColumns: ["Type"],
    dependentColumnNames: ["IsRx", "IsOTC"]
});
```

The fields connected with the `IsRx` and `IsOTC` columns are displayed if the `Type` column contains the value defined by the `Terrasoft.Configuration.Consts.AccountTypePharmacy` invariable.

```js
Terrasoft.Configuration.Consts = {
    AccountTypePharmacy: "d12dc11d-8c74-46b7-9198-5a4385428f9a"
};
```

You can use the 'd12dc11d-8c74-46b7-9198-5a4385428f9a’ value instead of the invariable.

## Enabled/Disabled business rule (Terrasoft.RuleTypes.Activation) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-4 "Direct link to Enabled/Disabled business rule (Terrasoft.RuleTypes.Activation)")

This business rule enables and disables fields for entering values per condition.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.Activation` value for this rule.

```js
triggeredByColumns
```

The column array that triggers the rule.

```js
events
```

An event array, defining the time of running business rules. It should contain values included into the `Terrasoft.BusinessRuleEvents` enumeration.

```js
conditionalColumns
```

Condition array of business rule execution. Usually, these are specific column values.

```js
dependentColumnNames
```

Column name array that the business rule is applied to.

Whether a field connected with the `Stock` column is enabled depends on the value in the `IsPresence` column.

Use case

```js
Terrasoft.sdk.Model.addBusinessRule("ActivitySKU", {
    ruleType: Terrasoft.RuleTypes.Activation,
    events: [Terrasoft.BusinessRuleEvents.Load, Terrasoft.BusinessRuleEvents.ValueChanged],
    triggeredByColumns: ["IsPresence"],
    conditionalColumns: [\
        {name: "IsPresence", value: true}\
    ],
    dependentColumnNames: ["Stock"]
});
```

## Filtration business rule (Terrasoft.RuleTypes.Filtration) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-5 "Direct link to Filtration business rule (Terrasoft.RuleTypes.Filtration)")

This business rule can be used for filtration of lookup columns by condition, or by another column value.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.Filtration` value for this rule.

```js
triggeredByColumns
```

The column array that triggers the rule.

```js
events
```

An event array, defining the time of running business rules. It should contain values included into the `Terrasoft.BusinessRuleEvents` enumeration.

```js
filters
```

Filter. The property should contain the `Terrasoft.Filter` class instance.

```js
filteredColumn
```

The column used for filtering values.

## Mutual Filtration business rule (Terrasoft.RuleTypes.MutualFiltration) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-6 "Direct link to Mutual Filtration business rule (Terrasoft.RuleTypes.MutualFiltration)")

This business rule enables mutual filtering of two lookup fields. Works only with columns with the "one-to-many" relationship, e.g., **Country** – **City**. Create a separate business rule for every field cluster. For example, for the **Country** – **Region** – **City** and the **Country** – **City** clusters, create three business rules:

- **Country** – **Region**;
- **Region** – **City**;
- **Country** – **City**.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.MutualFiltration` value for this rule.

```js
triggeredByColumns
```

The column array that triggers the rule.

```js
connections
```

Object array that configures cluster relationship

- Mutual filtration of the \[Country\], \[Region\] and \[City\] fields
- Mutual filtration of the \[Contact\], \[Account\] fields

```js
Terrasoft.sdk.Model.addBusinessRule("ContactAddress", {
    ruleType: Terrasoft.RuleTypes.MutualFiltration,
    triggeredByColumns: ["City", "Region", "Country"],
    connections: [\
        {\
            parent: "Country",\
            child: "City"\
        },\
        {\
            parent: "Country",\
            child: "Region"\
        },\
        {\
            parent: "Region",\
            child: "City"\
        }\
    ]
});
```

```js
Terrasoft.sdk.Model.addBusinessRule("Activity", {
    ruleType: Terrasoft.RuleTypes.MutualFiltration,
    triggeredByColumns: ["Contact", "Account"],
    connections: [\
        {\
            parent: "Contact",\
            child: "Account",\
            connectedBy: "PrimaryContact"\
        }\
    ]
});
```

## Regular expression business rule (Terrasoft.RuleTypes.RegExp) [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-7 "Direct link to Regular expression business rule (Terrasoft.RuleTypes.RegExp)")

Verifies the conformity of the column value with the regular expression.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-2430-12 "Direct link to Configuration object properties")

```js
ruleType
```

Should contain the `Terrasoft.RuleTypes.RegExp` value for this rule.

```js
RegExp
```

Regular expression whose conformity with all the `triggeredByColumns` array columns is verified.

```js
triggeredByColumns
```

The column array that triggers the rule.

Use case

```js
Terrasoft.sdk.Model.addBusinessRule("Contact", {
    ruleType: Terrasoft.RuleTypes.RegExp,
    regExp : /^([0-9\(\)\/\+ \-]*)$/
    triggeredByColumns: ["HomeNumber", "BusinessNumber"]
});
```

## Custom business rules [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-8 "Direct link to Custom business rules")

When adding a custom business rule via the `Terrasoft.sdk.Model.addBusinessRule(name, config)` method you can use properties of the `config` configuration object of the base business rule. In addition, the `executeFn` property is also provided.

### Configuration object properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-12 "Direct link to Configuration object properties")

```js
ruleType
```

Rule type. For the custom rules it should contain the `Terrasoft.RuleTypes.Custom` value.

```js
triggeredByColumns
```

Array of columns which initiates trigging of the business rule.

```js
events
```

Array of events determining the start time of the business rule. It should contain values from the `Terrasoft.BusinessRuleEvents` enumeration. Default value: `Terrasoft.BusinessRuleEvents.ValueChanged`.

Available values (Terrasoft.BusinessRuleEvents)

|     |     |
| --- | --- |
| Save | the rule trigs before saving the data |
| ValueChanged | the rule trigs after changing the data (at modification) |
| Load | the rule trigs when the edit page is opened |

```js
executeFn
```

A handler function that contains the user logic for executing the business rule.

### Properties of the executeFn handler function [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-10 "Direct link to Properties of the executeFn handler function")

Handler function signature

```js
executeFn: function(record, rule, checkColumnName, customData, callbackConfig, event) {    }
```

Parameters

|     |     |
| --- | --- |
| record | a record for which the business rule is executed |
| rule | an instance of the current business rule |
| checkColumnName | a column name that calls business-rules firing |
| customData | an object that is shared between all rules. Not used. Left for compatibility with previous versions |
| callbackConfig | a configuration object of the `Ext.callback` asynchronous callback |
| event | an event that triggered the business rul. |

After the completion of function operation it is necessary to call either the `callbackConfig.success` or `callbackConfig.failure`.

Use cases options

```js
Ext.callback(callbackConfig.success, callbackConfig.scope, [result]);
Ext.callback(callbackConfig.failure, callbackConfig.scope, [exception]);
```

Where:

- `result` – the returned boolean value obtained when the function is executed (`true`/`false`).
- `exception` – the exception of the `Terrasoft.Exception` type, which occurred in the handler function.

### Methods [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config\#title-1523-29 "Direct link to Methods")

In the source code of the handler function, you can use the following methods of the model passed in the `record` parameter:

```js
get(columnName)
```

To get the value of a record column. The `columnName` argument should contain the column name.

```js
set(columnName, value, fireEventConfig)
```

To set the value of the record column.

Parameters

|     |     |
| --- | --- |
| columnName | the name of the column |
| value | the value assigned to the column |
| fireEventConfig | a configuration object to set the properties that are passed to the column modification event |

```js
changeProperty(columnName, propertyConfig)
```

For changing column properties except its value. The `columnName` argument should contain the column name and the `propertyConfig` object that sets the column properties.

propertyConfig object properties

|     |     |
| --- | --- |
| disabled | activity of the column. If `true`, the control associated with the column will be inactive and disabled for operation |
| readOnly | "Read only" flag. If `true`, the control associated with the column will be available only for reading. If `false` – the access for reading and writing |
| hidden | column visibility. If `true`, the control associated with the column will be hidden. If `false` – the control will be displayed |
| addFilter | add filter. If the property is specified, it should have a filter of the `Terrasoft.Filter` type that will be added to the column filtration. Property is used only for lookup fields |
| removeFilter | remove the filter. If the property is specified, it should have a name of the filter that will be removed from the column filtration. Property is used only for lookup fields |
| isValid | flag of column validity. If the property is specified, it will change the validity flag of the control associated with the column. If the column is invalid, then this can mean canceling of saving the record, and can also lead to the determining the record as invalid |

Example of changing the properties (but not the values) of the Owner column

```js
record.changeProperty("Owner", {
    disabled: false,
    readOnly: false,
    hidden: false,
    addFilter: {
        property: "IsChief",
        value: true
    },
    isValid: {
        value: false,
        message: LocalizableStrings["Owner_should_be_a_chief_only"]
    }
 });
```

- [Base business rule](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-1)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [**Is required** business rule (Terrasoft.RuleTypes.Requirement)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-2)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [Visibility business rule (Terrasoft.RuleTypes.Visibility)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-3)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [Enabled/Disabled business rule (Terrasoft.RuleTypes.Activation)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-4)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [Filtration business rule (Terrasoft.RuleTypes.Filtration)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-5)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [Mutual Filtration business rule (Terrasoft.RuleTypes.MutualFiltration)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-6)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
- [Regular expression business rule (Terrasoft.RuleTypes.RegExp)](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-7)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-2430-12)
- [Custom business rules](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-8)
  - [Configuration object properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-12)
  - [Properties of the executeFn handler function](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-10)
  - [Methods](https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/business-rules/references/config#title-1523-29)