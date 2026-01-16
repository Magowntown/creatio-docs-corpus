<!-- Source: page_177 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 08/03/2020

We at Creatio are constantly working to deliver advanced capabilities to accelerate your sales, service, and marketing processes. Here are the **new features** included in Creatio version 7.16.3.

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Creatio Marketing [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-1 "Direct link to Creatio Marketing")

- Adding a dynamic folder with no filters to a bulk email audience no longer results in adding the entire contact database as the bulk email recipients.
- Fixed an issue with rendering the cover of custom blocks of the Content Designer library in the Safari browser.

## Creatio Sales [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-2 "Direct link to Creatio Sales")

### Forecasts [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-3 "Direct link to Forecasts")

- You can now use objects from other forecasts in the "Value from object" indicators. This enables creating interdependent forecasts, as well as using historical data in the forecast metrics.

- Implemented easy high-level planning. If you edit a total value on a higher level of a forecast (e.g., total sales by all regions) the changes will proportionally distribute between all records that the total value includes (e.g., sales by separate regions). Upon modifying a forecast structure, make sure that you initiate the re-calculation of the forecast metrics before editing total values.

- You can now hide the fractional portion of the forecast values without rounding. Also, you can hide editable forecast columns. To do this, use the **Hide column** and **Hide decimal numbers** checkboxes in the column setup
The Hide decimal numbers checkbox in the column settings

![The Hide decimal numbers checkbox in the column settings](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.3/BPMonlineHelp/release_notes/hide_decimal_numbers.png)


## Portal [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-19 "Direct link to Portal")

- Global search is now available for portal sections. You can use the command line to search for records by keywords, similarly to main Creatio application.

## Core functions [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-4 "Direct link to Core functions")

- We will soon discontinue support for the outdated Internet Explorer 11 browser. Creatio will no longer support legacy browsers starting with version 7.17. Microsoft recommends Microsoft Edge for browsing in Windows. Read more in the [Microsoft Tech Community](https://techcommunity.microsoft.com/t5/windows-it-pro-blog/the-perils-of-using-internet-explorer-as-your-default-browser/ba-p/331732) article. We recommend Google Chrome and Mozilla Firefox for working with Creatio on Windows-based workstations.

### Working with emails [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-5 "Direct link to Working with emails")

- Improved the UX of working with emails in the communication panel. Creatio will now notify you when attempting to save an email connected to an activity with an empty required field. You can also link an entire email thread to Creatio record.

### Analytics [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-6 "Direct link to Analytics")

- You can now change the column width in pivot tables.
- Pivot tables display dates based on the format selected in the Creatio user profile.
- The captions in bar charts with negative values no longer overlap or collide with other chart elements.

## Customer database management tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-7 "Direct link to Customer database management tools")

- Improved the display of bulk duplicate search results. The results page now displays the percentage of processed records during the search. Result groups now display the records whose duplicates have been found. These features are available when the "LazyLoadDeduplicationResult" feature is enabled. Learn more about enabling additional functions in the " [Feature Toggle. Mechanism of enabling and disabling functions](https://academy.creatio.com/documents/technic-sdk/7-15/feature-toggle-mechanism-enabling-and-disabling-functions)" article.

## Mobile application [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-8 "Direct link to Mobile application")

- The twelve-digit numbers saved using the mobile app now properly display in the Creatio desktop app.

## Phone integration and managing communications [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-9 "Direct link to Phone integration and managing communications")

- Creatio Messaging Service now works with the Asterisk phone integration on Linux.

## Business processes [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-10 "Direct link to Business processes")

- Multi-instance subprocesses can be configured to continue running even if one of the instances ends with an error. Use the corresponding checkbox in the **Subprocess** element setup area.
Continue execution on errors checkbox

![Continue execution on errors checkbox](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.3/BPMonlineHelp/release_notes/multi_instance_subprocess_execute_on_errors.png)

- Multi-instance subprocesses now store information on their instance execution in a set of special parameters: "Number of completed instances," "Number of terminated instances," and "Total number of instances." The values are populated after the **Subprocess** element completes.


### Process log [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-11 "Direct link to Process log")

- Creatio now logs business process errors that do not originate from an element: for example, conditional flow errors. The error descriptions are available in the process log.

## User customization tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-12 "Direct link to User customization tools")

- You can now show or hide tabs, details, field groups and separate page modules dynamically, via business rules. For example, you can display a tab for additional data on closing an opportunity, or display a new field group for specific users only.
- When adding a new section based on an existing Creatio object, the Section Wizard now automatically adds the **Attachments and notes** tab. We have also implemented a notification that working with dynamic folders and tags is unavailable for an existing third-party object.

## Administration [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-13 "Direct link to Administration")

- You can now verify your Exchange Listener settings using a special service page. Use the page to check Exchange Listener availability, subscription information, verify the URL of the Exchange event processing service in Creatio, and test the mailbox.

## Security [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-14 "Direct link to Security")

- You can now change the mode of file security using the "File Security Mode" system setting. Set the value to "File extensions AllowList" to enable working only with the file types specified in the "File extensions AllowList" setting. Uploading other file types will be restricted.
Setting the file security mode when uploading a file to Creatio

![Setting the file security mode when uploading a file to Creatio](https://academy.creatio.com/sites/default/files/documents/docs_en/product/bpm'online%20release%20notes/release%20notes/7.16.3/BPMonlineHelp/release_notes/file_check_mode_system_setting.png)

- Use the "Allow processing files of unknown type" system setting to permit processing the files of unknown types in Creatio. This mode is enabled by default.


## Development tools [​](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes\#title-139-15 "Direct link to Development tools")

- The jQuery library has been updated to version 3.5.1. Specify the library version in the "jQuery file name" system setting.
  - specify "jQuery" to use version 3.4.1
  - specify "jQuery-3.5.1" to use version 3.5.1.

- [Creatio Marketing](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-1)
- [Creatio Sales](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-2)
  - [Forecasts](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-3)
- [Portal](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-19)
- [Core functions](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-4)
  - [Working with emails](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-5)
  - [Analytics](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-6)
- [Customer database management tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-7)
- [Mobile application](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-8)
- [Phone integration and managing communications](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-9)
- [Business processes](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-10)
  - [Process log](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-11)
- [User customization tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-12)
- [Administration](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-13)
- [Security](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-14)
- [Development tools](https://academy.creatio.com/docs/8.x/resources/release-notes/7163-release-notes#title-139-15)