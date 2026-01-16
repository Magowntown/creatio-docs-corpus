<!-- Source: page_57 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/resources/finserv-release-notes/1-2-finserv-release-notes#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Release date: 12/18/2025

At Creatio, we are committed to empowering our customers with industry-leading product innovations for workflow automation, no-code development, and modern CRM. Today we are advancing new forms of innovation with Creatio Financial Services CRM version 1.2, featuring the **following new capabilities and enhancements**.

A comprehensive overview of technical changes and enhancements can be found in the [1.2 Creatio Financial Services CRM changelog](https://academy.creatio.com/docs/8.x/resources/releases/finserv-changelog/1-2-finserv-changelog).

The update guide for the on-site applications is available in a separate [article](https://academy.creatio.com/documents?id=2495).

## Key updates [​](https://academy.creatio.com/docs/8.x/resources/finserv-release-notes/1-2-finserv-release-notes\#title-2782-201 "Direct link to Key updates")

**Streamlined underwriting**.

- Applications that have manual checks now generate approval requests upon completion of these checks. If all manual checks are approved, the application status automatically updates to "Passed." Applications without manual checks are auto-approved by Creatio System Underwriter.
- New evaluation statuses ("Auto checks processing," "Auto checks completed," "Auto checks declined," "Cancelled") and detailed logs provide full visibility into evaluation and approval progress.
- Creatio now updates the contact type to "Customer" automatically once an application reaches the "Settled" stage, ensuring accurate customer identification in future consultations.
- Upload functionality and document management options are visible only during the "Underwriting" stage, maintaining a focused and streamlined interface.

**Enhanced document management within the application process**. You can now upload required documents directly on the application full page, using the same familiar UI and logic available on the application submission page.

**AI insights for households**. It is now possible to have a clear, at-a-glance view of the most important updates using the new AI insights for households and household members.

The new feature displays the top five alerts per active member, enabling quick identification of key activities or potential risks without switching between pages. By consolidating all relevant insights into a single, centralized view, this enhancement improves visibility, accelerates decision-making, and supports more proactive customer engagement.

**Add contact to household**. You can now manage contact-household relationships on the contact page more efficiently with enhanced navigation. A new button is available directly on the contact page in the Households expanded list, providing quick access to adding the contact to the household. The **Household** field on the contact page is now read-only to ensure data consistency.

Creatio now prevents adding the same contact to a household more than once, improving data quality and operational efficiency. This ensures each household record remains clean and accurate, reducing manual data cleanup and enabling teams to rely on consistent, trustworthy information when managing customer relationships.

**Enhanced primary contact management for households**.

- Creatio now synchronizes household records automatically when you add or change the primary contact. Creatio clears outdated links when members move out or are removed, reducing manual cleanup.
- You can assign a primary contact directly during household creation without needing additional steps or post-creation adjustments.
- When a selected contact already serves as a primary contact elsewhere, Creatio prompts you to confirm or reject the contact's migration to the new household, helping maintain clean and intentional household structures.

**Household address management**. Creatio now automatically inherits the household address from the primary contact’s primary address. Any updates to the primary contact—whether a change to their address or the assignment of a new primary contact—are immediately reflected in the household address. To ensure data integrity and prevent manual inconsistencies, household address fields on the household page are now read-only.

**Household history**. You can now have full visibility into key household updates and strengthen data auditability using new household history. Creatio records changes to critical data, for example, full addresses, automatically, capturing who made the update and when. A dedicated **History** tab on the household page presents a clear chronological view of these changes, allowing you to trace modifications over time easily. This enhancement ensures greater transparency, supports compliance, and provides valuable historical context for more informed customer management decisions.

**Compliant consultation flow**. Administrators can now control whether users are allowed to open the contact page, restricting access to customer data until identification is successfully completed. Automatic navigation to the contact page is disabled by default, preventing unintended exposure of sensitive customer information and ensuring full control over access timing and compliance requirements.

**Enhanced evaluation process**. Now restarting KYC evaluation is available directly on the application full page, ensuring consistent control and flexibility in managing KYC checks across the application process. You can now have more control over and ensure transparency for evaluation processing as it is no longer possible to restart KYC evaluations for applications that are already closed.

**Streamlined financial data management**. Financial information is now captured more consistently by preventing users from creating duplicate income, expense, or liability records of the same type. When you add a new record, Creatio hides any types already used for that contact or application automatically, ensuring each financial category is entered only once. Existing records also have a read-only **Type** field to avoid accidental changes. Additionally, financial items that have "Not started" verification status are now visible during application processing, giving teams a full and accurate picture of the customer's financial situation. This update reduces data conflicts, improves clarity, and makes financial reviews more reliable.

- [Key updates](https://academy.creatio.com/docs/8.x/resources/finserv-release-notes/1-2-finserv-release-notes#title-2782-201)