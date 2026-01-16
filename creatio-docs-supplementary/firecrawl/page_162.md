<!-- Source: page_162 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/button-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: beginner

Use the **Button** component to add buttons.

View the example of a configuration object that adds the button below.

Example of a configuration object that adds the button

```js
{
    "type": "crt.Button",
    "clicked": {
        /* Creatio lets you bind the sending of base or custom request to the button click event. */
        "request": "crt.CreateRecordRequest"
    },
    "icon": "open-button-icon",
    "caption": "Button",
    "color": "primary",
    "size": "medium",
    "iconPosition": "left-icon",
    "menuTitle": "Menu title" /*Added.*/,
    "menuItems": [\
        {\
            "type": "crt.MenuItem",\
            "caption": "Menu item 1",\
            "clicked": {\
                /* Creatio lets you bind the sending of base or custom request to the button click event. */\
                "request": "crt.SetViewModelAttributeRequest",\
                "params": {\
                    "attributeName": "CalendarViewMode",\
                    "value": "day"\
                }\
            },\
        },\
        {...}\
        ...\
    ]
}
```

## Common properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/button-mobile\#title-15089-2 "Direct link to Common properties")

```js
string type
```

Component type. `crt.Button` for the **Button** component.

* * *

```js
object clicked
```

The request fires when a user clicks the button. Creatio lets you bind the sending of a base request or custom request handlers implemented in remote module to the button click event.

* * *

```js
string icon
```

Icon to display next to the menu item caption.

Available values

|     |     |
| --- | --- |
| actions-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/actions_button_icon.png) |
| add-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/add_button_icon.png) |
| back-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/back_button_icon.png) |
| bars-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/bars_button_icon.png) |
| calculator-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/calculator_button_icon.png) |
| clip-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/clip_button_icon.png) |
| close-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/close_button_icon.png) |
| delete-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/delete_button_icon.png) |
| disk-warn-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/disk_warn_button_icon.png) |
| document-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/document_button_icon.png) |
| document-new-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/document_new_button_icon.png) |
| upload-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/upload_button_icon.png) |
| download-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/download_button_icon.png) |
| edit-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/edit_button_icon.png) |
| email-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/email_button_icon.png) |
| export-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/export_button_icon.png) |
| export-data-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/export_data_button_icon.png) |
| flag-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/flag_button_icon.png) |
| gear-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/gear_button_icon.png) |
| horn-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/horn_button_icon.png) |
| import-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/import_button_icon.png) |
| import-data-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/import_data_button_icon.png) |
| lock-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/lock_button_icon.png) |
| contact-lock-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/contact_lock_icon.png) |
| message-warn-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/message_warn_button_icon.png) |
| more-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/more_button_icon.png) |
| open-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/open_button_icon.png) |
| pencil-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/pencil_button_icon.png) |
| print-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/print_button_icon.png) |
| process-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/process_button_icon.png) |
| reload-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/reload_button_icon.png) |
| save-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/save_button_icon.png) |
| settings-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/settings_button_icon.png) |
| social-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/social_button_icon.png) |
| call-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/call_button_icon.png) |
| folder-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/folder_button_icon.png) |
| person-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/person_button_icon.png) |
| timeline-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/timeline_button_icon.png) |
| facebook-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/facebook_button_icon.png) |
| linkedin-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/linkedin_button_icon.png) |
| webforms-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/webforms_button_icon.png) |
| webhooks-integration-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/webhooks_integration_button_icon.png) |
| copy-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/copy_icon.png) |
| message-composer-checkmark | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/message_composer_checkmark.png) |
| relationship-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/relationship_button_icon.png) |
| date | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/date.png) |
| date-time | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/date_time.png) |
| box-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/box_icon.png) |
| car-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/car_icon.png) |
| contact-leads-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/contact_leads_icon.png) |
| database-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/database_icon.png) |
| employee-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/employee_icon.png) |
| filter-column-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/filter_column_icon.png) |
| filter-funnel-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/filter_funnel_icon.png) |
| money-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/money_icon.png) |
| newspaper-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/newspaper_icon.png) |
| organizational-structure-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/organizational_structure_icon.png) |
| tag-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/tag_icon.png) |
| trolley-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/trolley_icon.png) |
| work-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/work_icon.png) |
| replace-squares-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/replace_squares_icon.png) |
| sum-button-icon | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/sum_button_icon.png) |

* * *

```js
string caption
```

Localizable button caption.

* * *

## Optional properties [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/button-mobile\#title-15089-3 "Direct link to Optional properties")

```js
string color
```

Button style. By default, `default`.

Available values

|     |     |     |
| --- | --- | --- |
| primary | Primary. Blue button. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_primaryButton.png) |
| accent | Accent. Green button. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_accentButton.png) |
| warn | Warning. Red button. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_warnButton.png) |
| default | Auxiliary white button. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_defaultButton.png) |

* * *

```js
string size
```

Button size. By default, `large`.

Available values

|     |     |
| --- | --- |
| small | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_smallButton.png) |
| medium | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_mediumButton.png) |
| large | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_largeButton.png) |

* * *

```js
string iconPosition
```

Position of the icon relative to the button caption. By default, `left-icon`.

Available values

|     |     |     |
| --- | --- | --- |
| only-text | Do not display the icon. Display only the button caption. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_only_text.png) |
| left-icon | Display the icon to the left of the button caption. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_left_icon.png) |
| right-icon | Display the icon to the right of the button caption. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_right_icon.png) |
| only-icon | Display only the icon. Do not display the button caption. | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MobileComponentsReference/scr_only_icon.png) |

* * *

```js
string menuTitle
```

Title of the menu picker.

* * *

```js
array of objects menuItems
```

List of button menu items. Displayed at the bottom of the page after clicking the button. When the `menuItems` property is used the `clicked` button property is ignored. To add the button menu item, use the **Menu item** component.

- [Common properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/button-mobile#title-15089-2)
- [Optional properties](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/button-mobile#title-15089-3)