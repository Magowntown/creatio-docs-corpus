<!-- Source: page_116 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use data bindings to ensure data visualization in Creatio UI and synchronization of this data operate as intended.

The `viewConfig` schema section of the Freedom UI page implements a tree of Freedom UI Mobile components. A Freedom UI Mobile component can contain parameters that have constant or dynamic values. Creatio lets you bind the parameter value to the attribute value from the `viewModelConfig` schema section.

Creatio lets you bind the parameter value to the following attribute types:

- attribute that contains nested `view model` instance
- custom attribute
- resource attribute

To bind the parameter value to the attribute value, use the following pattern: `$SomeAttributeName`, where `SomeAttributeName` is an arbitrary name of the attribute from the `viewModelConfig` schema section.

## Bind Freedom UI Mobile component to the attribute that contains nested view model instance [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile\#title-15086-1 "Direct link to Bind Freedom UI Mobile component to the attribute that contains nested view model instance")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/documents?id=15088&anchor=title-15088-1) (steps 1-3).

2. **Go to the**`viewModelConfig` **schema section**.

3. **Add an attribute** if needed. To do this, add the column to the `attributes` configuration object property. For example, add the `Account` column.



viewModelConfig schema section





```js
"viewModelConfig": {
       ...,
       "attributes": {
           "Account": {
               "modelConfig": {
                   "path": "PDS.Account"
               }
           }
       }
},
...
```









**As a result**, Creatio will load data from the column and set the corresponding attribute.

Creatio lets you configure the column paths relative to the root schema. Instructions: [Configure the column paths relative to the root schema](https://academy.creatio.com/documents?id=15330&anchor=title-1297-1).

For example, add the `TimeZone` column from the `City` root schema.



viewModelConfig schema section





```js
"viewModelConfig": {
       ...,
       "attributes": {
           "City.TimeZone": {
               "modelConfig": {
                   "path": "PDS.City.TimeZone"
               }
           }
       }
},
...
```

4. **Go to the**`viewConfig` **schema section**.

5. **Bind the parameter value** to the attribute value. For example, bind the **Input** component to the `$Account` attribute value.



viewConfig schema section





```js
"viewConfig": {
       ...,
       "type": "crt.EditField",
       "value": "$Account",
       ...
},
...
```


**As a result**, Creatio will display the attribute value as the value of the bound component parameter. Creatio will update the parameter value when the attribute value changes.

## Bind Freedom UI Mobile component to the custom attribute [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile\#title-15086-2 "Direct link to Bind Freedom UI Mobile component to the custom attribute")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/documents?id=15088&anchor=title-15088-1) (steps 1-3).

2. **Go to the**`viewModelConfig` **schema section**.

3. **Add an attribute** if needed. To do this, add the custom attribute to the `attributes` configuration object property. For example, add the `SomeAttribute` attribute.



viewModelConfig schema section





```js
"viewModelConfig": {
       ...,
       "attributes": {
           "SomeAttribute": {}
       }
},
...
```









Creatio lets you configure the default attribute value. To do this, add the default value to the `value` attribute property.

For example, use the `DefaultAttributeValue` value as the default attribute property.



viewModelConfig schema section





```js
"viewModelConfig": {
       ...,
       "attributes": {
           "SomeAttribute": {
               "value": "DefaultAttributeValue"
           }
       }
},
...
```

4. **Go to the**`viewConfig` **schema section**.

5. **Bind the parameter value** to the attribute value. For example, bind the **Button** component to the `$SomeAttribute` attribute value.



viewConfig schema section





```js
"viewConfig": {
       ...,
       "type": "crt.Button",
       "value": "$SomeAttribute",
       ...
},
...
```


**As a result**, Creatio will display the attribute value as the value of the bound component parameter. Creatio will update the parameter value when the attribute value changes.

## Bind Freedom UI Mobile component to the resource attribute [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile\#title-15086-3 "Direct link to Bind Freedom UI Mobile component to the resource attribute")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/documents?id=15088&anchor=title-15088-1) (steps 1-3).

2. **Add a resource attribute** if needed. Instructions: [Add a localizable string](https://academy.creatio.com/documents?id=15272&anchor=title-2174-3). For example, add the `SomeString` localizable string.

3. **Go to the**`viewConfig` **schema section**.

4. **Bind the parameter value** to the resource attribute value. For example, bind the **Button** component to the `SomeString` attribute value.



viewConfig schema section





```js
"viewConfig": {
       ...,
       "type": "crt.Button",
       "value": "#ResourceString(SomeString)#",
       ...
},
...
```


**As a result**, Creatio will display the attribute value as the value of the bound component parameter. Creatio will update the parameter value when the attribute value changes.

## Bind a converter to the attribute of the Freedom UI Mobile component [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile\#title-15086-4 "Direct link to Bind a converter to the attribute of the Freedom UI Mobile component")

1. **Implement the data source**. Instructions: [Implement the data source](https://academy.creatio.com/documents?id=15088&anchor=title-15088-1) (steps 1-3).

2. **Go to the**`viewModelConfig` **schema section**.

3. **Add an attribute** if needed. To do this, add the custom attribute to the `attributes` configuration object property. For example, add the `SomeAttribute` attribute.



viewModelConfig schema section





```js
"viewModelConfig": {
       ...,
       "attributes": {
           "SomeAttribute": {}
       }
},
...
```

4. **Go to the**`viewConfig` **schema section**.

5. **Bind the converter** to the attribute value. For example, bind the `crt.ToObjectProp` converter to the `$SomeAttribute` attribute of the **Button** component.



viewConfig schema section





```js
"viewConfig": {
       ...,
       "type": "crt.Button",
       "value": "$SomeAttribute | crt.ToObjectProp : 'someProperty':'somePropertyValue'",
       ...
},
...
```


**As a result**, Creatio will display the value of the specified object property as the attribute value.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile\#see-also "Direct link to See also")

[Get started with Creatio Freedom UI](https://academy.creatio.com/documents?id=2445)

[Freedom UI page schema](https://academy.creatio.com/documents?id=15342)

[Operations with localizable resources](https://academy.creatio.com/documents?id=15272)

- [Bind Freedom UI Mobile component to the attribute that contains nested view model instance](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#title-15086-1)
- [Bind Freedom UI Mobile component to the custom attribute](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#title-15086-2)
- [Bind Freedom UI Mobile component to the resource attribute](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#title-15086-3)
- [Bind a converter to the attribute of the Freedom UI Mobile component](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#title-15086-4)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/bind-data-mobile#see-also)