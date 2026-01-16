<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/creatio-maintenance/manage-resource-intensive-queries)** (8.3).

Version: 8.1

On this page

Execution of resource-intensive business operations (queries) can utilize a significant amount of database resources, which often leads to lower Creatio performance for all users. Such operations include:

- **Queries that filter strings by the "contains" mask**. For example, standard filter that has the "Name contains %Jane%" condition in the **Contacts** section.
- **Unfiltered, non-paginated queries** generated using OData service or server-side Creatio development tools. For example, "get all contacts" query executed when you have more than 20,000 contact records.
- **Queries sorted by a non-indexed column**.For example, **Contacts** section records sorted by the custom **Account country** column, for which no index has been created in the database.
- **Queries sorted by complex columns that contain a subquery** For example, **Accounts** section records sorted by the column with feedback: the sum of sales for the last year for sales related to the account.

To detect such queries, Creatio uses templates stored in the **Query detector** lookup.

You can apply multiple actions to resource-intensive queries to reduce the load on the database significantly and free up resources for user activity and operation of other Creatio elements. These actions are listed in the **Query action** lookup.

- **Limit query execution time**. Cancel the query after the time limit specified in the "Query execution timeout" ("QueryExecutionTimeout" code) system setting passes.
- **Logging**. Log only query data to the **Query rule apply log** lookup. This helps to track the problematic queries.
- **Limit the number of threads**. Limit the number of threads to execute the request to the value specified in the "MaxDopQueryHint thread count" ("MaxDopHintThreadsCount" code) system setting. We recommend using a quarter to a half of total available threads, assuming one thread corresponds to one CPU core. This way, resource-intensive operations will be unable to take all available threads.
- **Cancel execution**. Cancel the query immediately.

Important

We do not recommend changing the contents of the **Query detector** and **Query action** lookups. This can lead to violations of query handling rules.

## Configure query handling rules [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries\#title-2516-1 "Direct link to Configure query handling rules")

You can restrict the handling of heavy queries to improve database performance. To do this, define the type of the heaviest queries in your Creatio application and set rules that restrict their execution.

note

A system administrator or user who has permissions to execute the "Can manage query rules" ("CanManageQueryRules" code) system operation can configure the rules.

The basic rule structure looks as follows:

```cli
If the query goes to the <name> table, the table contains more than <n> rows, and the query matches the <query detector> template, then the <query action> action must be applied to the query.
```

To set up a rule:

1. Click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/business_rules/btn_system_designer.png) → System Designer.

2. Click **Lookups**.

3. Open the **Query handle rule** lookup.

4. Click **Add**.

5. Fill out the rule parameters:
1. Enter a unique rule name in the **Name** parameter. Required.

2. Specify the schema (database table) to which the query must be executed in the **Entity schema** parameter. If no schema is specified, Creatio applies the rule to all schemas.

3. Set the minimum number of table rows required for the rule to apply in the **Min row count** parameter. Minimum value: 1000. Required.

4. Select the template of the query type to which to apply the rule in the **Query Detector** parameter. Available values are stored in the **Query Detector** lookup. Required.

5. Select the action to apply to the query in the **Query Action** parameter. Available values are stored in the \[Query Action\] lookup. Required.



      note





      **System** checkbox determines the rule editability and priority. System rules can be configured only by cloud administrators in accordance with the cloud policies and restrictions. These rules are mandatory and cannot be modified or deleted by Creatio users.

6. Specify the rule availability in the **Active** — determines whether the rule is used or not.

7. Specify whether to log the Stack trace of the call of the operation that executes the query to which the rule was applied in the **Log stack trace** parameter. Logs are saved to the **Query rule apply log** lookup.

8. Specify whether to log the query execution time in the **Log query execution time** parameter.
6. Save the changes.

7. Repeat steps 4–6 for other needed rules.


## Execute rules [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries\#title-2516-2 "Direct link to Execute rules")

Rule priorities are based on the detector, system character, schema (table), and number of table rows. When the query is executed, Creatio checks the following:

- query detectors used
- entity schema and row number
- whether **System** checkbox is set

If multiple rules apply to the same query detector and entity schema, Creatio applies only one system and one regular rule that match the most closely.

The examples below explain how rules affect the execution of resource-intensive queries. In the examples, the following set of rules is configured in Creatio.

| Entity schema | Min number of rows | Query detector | Query action | Is System | Is Active |
| --- | --- | --- | --- | --- | --- |
| Like 1 rule |
| Not set | 20000 | Text filter detector by pattern "%..." | Limit query execution time | No | Yes |
| Like 2 rule |
| Not set | 500000 | Text filter detector by pattern "%..." | Cancel execution | No | Yes |
| Index 1 rule |
| Not set | 10000 | Not indexed column sorting detector | Limit query execution time | No | Yes |
| Index 2 rule |
| Not set | 500000 | Not indexed column sorting detector | Cancel execution | No | Yes |
| Activity Like 1 rule |
| Activity | 20000 | Text filter detector by pattern "%..." | Limit query execution time | No | Yes |
| Activity Like rule |
| Activity | 1000000 | Text filter detector by pattern "%..." | Cancel execution | No | Yes |
| Activity Like sys rule |
| Activity | 10000 | Text filter detector by pattern "%..." | Limit the number of threads | Yes | Yes |
| Activity no fil no pag sys rule |
| Activity | 10000 | Not indexed column sorting detector | Limit the number of threads | Yes | Yes |

note

The user searches in the **Contacts** section by filtering " **Full name** contains `<Jane>`" and sorting by the non-indexed column **Date of birth**. The "Contacts" table has 100,000 entries.

The rule selection logic works as follows:

- The query fits two detectors: "Text filter detector by pattern "%..." and "Not indexed column sorting detector."
- "Contact" entity schema has no specific rules.
- Fitting rules have no system rules.

As a result, the most suitable rule will be executed for each query detector.

| Entity schema | Min number of rows | Query detector | Query action | Is System | Is Active |
| --- | --- | --- | --- | --- | --- |
| Like 1 rule |
| Not set | 20000 | Text filter detector by pattern "%..." | Limit query execution time | No | Yes |
| Index 1 rule |
| Not set | 10000 | Not indexed column sorting detector | Limit query execution time | No | Yes |

note

The user searches in the **Activities** section using the filter " **Name** contains `<account>`" and sorting by the non-indexed **Created Date** column. The "Activity" table has 120,000 entries.

The rule selection logic works as follows:

- The query fits two detectors: "Text filter detector by pattern "%..." and "Not indexed column sorting detector".
- "Activity" entity schema has specific rules.
- Fitting rules include system rules.

As a result, the most suitable system rule and common rule will be executed for "Text filter detector by pattern "%..." query detector. Only the most suitable system rule will be executed for "Not indexed column sorting detector" because no common rules for this query detector were configured.

| Entity schema | Min number of rows | Query detector | Query action | Is System | Is Active |
| --- | --- | --- | --- | --- | --- |

| Activity Like 1 rule |
| Activity | 20000 | Text filter detector by pattern "%..." | Limit query execution time | No | Yes |
| Activity Like sys rule |
| Activity | 10000 | Text filter detector by pattern "%..." | Limit the number of threads | Yes | Yes |
| Activity no fil no pag sys rule |
| Activity | 10000 | Not indexed column sorting detector | Limit the number of threads | Yes | Yes |

## Analyze rules execution [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries\#title-2516-3 "Direct link to Analyze rules execution")

Creatio stores the logged query execution data in the **Query rule apply log** lookup. For each of the configured rules, only the first operation for each of the users during the day is logged. This enables the administrator to identify Creatio bottlenecks and make appropriate changes based on the rules that are used most often.

In the log you can find the following information:

- **Schema name**. The root schema (database table) to which the request is made.
- **User login**. The user who initiated the request.
- **Last detection date**. Date of the last rule triggering on request.
- **Query detector**. Query type template for which the rule was applied.
- **Query action**. The action that was applied to the request.
- **Message**. Information that additionally reveals the reasons for triggering the rules: the number of records in the table, as well as by what criterion the trigger was triggered (for example, which heavy filter for which column).
- **Recommendation**. A recommendation to the system administrator how to reduce the impact of the query (for example, depending on the detector, add an index to the column, clear irrelevant/historical data in the table, strengthen the filter, etc.).
- **Execution time, sec**. A query execution time in database (to log this parameter, column **Log query execution time** of Query handle rule must be set up to "Yes").

To view the SQL text and stack trace of the query, you can use the **Show SQL text** and **Show stack trace** buttons, which are available after clicking on the log entry. This information may be needed to analyze the request in more detail and determine the functionality that generated it. Stack trace logging is off by default. But you can turn it on in the **Query handle rule** lookup.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries\#see-also "Direct link to See also")

[System requirements calculator](https://academy.creatio.com/docs/calculator)

[Limit the number of simultaneous DB queries](https://academy.creatio.com/documents?id=2407)

- [Configure query handling rules](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries#title-2516-1)
- [Execute rules](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries#title-2516-2)
- [Analyze rules execution](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries#title-2516-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/creatio-maintenance/manage-resource-intensive-queries#see-also)