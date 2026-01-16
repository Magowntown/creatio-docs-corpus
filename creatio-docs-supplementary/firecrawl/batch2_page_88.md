<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/clear-the-change-log#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/logging-tools/change-log/clear-the-change-log)** (8.3).

Version: 8.1

On this page

When working with Creatio, you may need to clear the change log history to avoid storing outdated log records in Creatio. For example, you can clear the log records of a specific contract created within the specified period of time.

note

We recommend clearing the change log regularly to ensure that the **Change log** section contains only the currently valid information.

1. Open the System Designer, e.g., by clicking ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/clear_change_log/btn_system_designer.png).

2. Under **Users and administration**, click **Change log**.

3. Click **Actions** → **Clear log**.



note





Deleting records in the change log requires permission to the **Can clear change log** (CanClearChangeLog) system operation permission.



Learn more about using system operations in the " [System operation permissions](https://academy.creatio.com/documents?product=base&ver=7&id=258)" article.

4. Select the objects whose log records must be cleared and specify the period for which to clear the record. Click **Clear** (Fig. 1) to delete the specified log records.
Fig. 1 Clearing record in the change log

![Fig. 1 Clearing record in the change log](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/clear_change_log/scr_section_change_log_clear_log.png)


As a result, the selected records will be deleted.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/clear-the-change-log\#see-also "Direct link to See also")

[Set up the audit log](https://academy.creatio.com/documents?id=1260)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/change-log/clear-the-change-log#see-also)