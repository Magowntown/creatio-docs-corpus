<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/audit-log/set-up-the-audit-log#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/logging-tools/audit-log/set-up-the-audit-log)** (8.3).

Version: 8.1

On this page

The **audit log** records system settings, events, and data. It logs events related to changes in the user role structure, the distribution of access permissions, changes in the system setting values, user authorization in Creatio, etc.

The **change log** records changes to business data. You can use it to track product price or account balance changes. Learn more: [Set up the change log](https://academy.creatio.com/documents?id=506).

note

Enable the "View "Audit log" section" ("CanViewSysOperationAudit" code) system operation to view the audit log. Enable the "Manage "Audit log" section" ("CanViewSysOperationAudit" code) system operation to view and archive the audit log records. Learn more: [System operation permissions](https://academy.creatio.com/documents?id=258).

The audit log is disabled by default. Follow the steps in this article to enable this feature.

To enable the audit log using the system settings:

1. Click the ![system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_audit_log/system_designer.png) button to open the System designer.

2. Click "System settings" in the "System setup" block.

3. Select the "Audit log" folder subordinate to the "Administration" folder. This folder contains all system settings that control the audit log. Each logged event type has a dedicated system setting that enables or disables it. Learn more about the audit log system settings: [Description of system settings](https://academy.creatio.com/documents?id=1259&anchor=title-1880-10).

4. Open the setting and select the **Default value** checkbox to enable it. For example, select the checkbox in the **Log user authorization management events** system setting (Fig. 1) to record user log in and log out events.
Fig. 1 An audit log system setting

![Fig. 1 An audit log system setting](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/logging_tools/BPMonlineHelp/set_up_audit_log/scr_chapter_system_operations_log_system_setting.png)


After disabling an audit log system setting, you may need to restart the Redis session server for the changes to take effect.

note

If the audit log is enabled on the configuration file level, Creatio will ignore the system setting values.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/audit-log/set-up-the-audit-log\#see-also "Direct link to See also")

[View and archive the audit log](https://academy.creatio.com/documents?id=2320)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/audit-log/set-up-the-audit-log\#resources "Direct link to Resources")

[Tech Hour: User session analytics - tracking and analyzing individual user log stats](https://www.youtube.com/watch?v=YFdqmbM-SUs)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/audit-log/set-up-the-audit-log#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/logging-tools/audit-log/set-up-the-audit-log#resources)