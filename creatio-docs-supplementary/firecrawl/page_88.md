<!-- Source: page_88 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/slider-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Slider** component to slide the value up and down with a preset step value and display an integer or double within a range.

View the example of a configuration object that displays a double within a range below.

Example of a configuration object that displays a double within a range

```js
{
    "type": "crt.Slider",
    "color": "accent",
    "minValue": 3.333,
    "maxValue": 4.3333,
    "step": 0.333,
    "label": "#ResourceString(SomeLabel)#",
    "readonly": false,
    "control": "$PDS_SomeControl",
    "visible": true,
    "labelPosition": "auto"
}
```

* * *

```js
string type
```

Component type. `crt.Slider` for the **Slider** component.

* * *

```js
string color
```

Slider style. By default, `default`.

Available values

|     |     |
| --- | --- |
| primary | Primary. Blue slider. |
| accent | Accent. Green slider. |
| warn | Warning. Red slider. |
| default | Auxiliary white slider. |

* * *

```js
number minValue
```

Minimum value of the slider range, displayed in the bottom left. The value can be either an integer or a double.

* * *

```js
number maxValue
```

Maximum value of the slider range, displayed in the bottom right. The value can be either an integer or a double.

* * *

```js
number step
```

Interval between values within the slider range. The value can be either an integer or a double and affects the UX. If the range between `minValue` and `maxValue` is not evenly divisible by the step, the maximum value is not selectable.

* * *

```js
string label
```

Slider title.

* * *

```js
boolean readonly
```

Whether to set the component to read-only. By default, `false`.

Available values

|     |     |
| --- | --- |
| true | The component is editable. |
| false | The component is not editable. |

* * *

```js
string control
```

Data source attribute bound to the slider value. The attribute value updates automatically when the slider changes.

* * *

```js
boolean visible
```

Whether to make the component label visible. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | The component label is visible. |
| false | The component label is not visible. |

* * *

```js
string position
```

Position of the slider label. By default, `auto`.

Available values

|     |     |
| --- | --- |
| auto | Display the label in the default position based on the layout. |
| hidden | Hide the label. |