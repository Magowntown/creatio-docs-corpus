<!-- Source: page_35 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/calendar-date-picker-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Calendar date picker** component to select month date.

View the example of a configuration object that implements the calendar date picker below.

Example of a configuration object that implements the calendar date picker

```js
{
    "type": "crt.CalendarDatePicker",
    "showHeader": true,
    "value": "SomeAttribute"
}
```

* * *

```js
string type
```

Component type. `crt.CalendarDatePicker` for the **Calendar date picker** component.

* * *

```js
boolean showHeader
```

The flag that determines whether to display the month name when you select a date. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The month name is displayed. |
| false | The month name is not displayed. |

* * *

```js
string value
```

The name of attribute from the `viewModelConfig` schema section that is changed when you select of change the date.