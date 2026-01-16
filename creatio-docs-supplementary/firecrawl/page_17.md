<!-- Source: page_17 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/set-up-dashboards-in-freedom-ui-designer#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3

On this page

Level: beginner

Example

Set up the **Dashboards** component on the request page.

To set up the component:

1. **Drag** the component to the canvas and open its setup area.

2. **Set up** the dashboard properties.
Fig. 1 Dashboard properties

![Fig. 1 Dashboard properties](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCodePlatform/set_up_dashboards/scr_dashboard_parameters_8_3.png)




| Parameter | Parameter value |
| --- | --- |
| Data source | Data source of the dashboard. Required to enable users to filter dashboards live.<br>This data source will be set as the primary data source for every dashboard created in this component. No-code developer can change it, but connections to the page will not work for those dashboards that have different primary data sources from this element. |
| Apply filter by page data | Whether to filter dashboard data by page data source, page parameters, **Attachment list**, or **List** component.<br>Connections to the page can be configured only in the **Dashboards** component. They work for all dashboards that have the same primary data source. |
| Apply pre-configured filter | Whether the users can filter dashboard data by a specific component, for example, **Folders** or **Quick filter**. |
| Dashboards | Click ![btn_new.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCodePlatform/set_up_dashboards/btn_new.png) to add and set up a new dashboard. This opens a new window of the Freedom UI Designer. Dashboard setup UX is similar to general Freedom UI Designer UX. Learn more about configuring dashboard widgets: [Set up widgets](http://academy.creatio.com/documents?id=2144).<br>To ensure widgets can be filtered, Creatio applies filter by page data source to them during the setup. You can remove it if needed. |
| Visibility | Click ![btn_visible.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCodePlatform/set_up_dashboards/btn_visible.png) or ![btn_not_visible.png](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCodePlatform/set_up_dashboards/btn_not_visible.png) button to make the component visible or invisible by default on the page, respectively. |
| Setup conditions | Configure element business rules. Learn more: [Set up business rules](https://academy.creatio.com/documents?id=2409). |
| Element code | Code of the component required for low-code customization. The field is non-editable. |

3. **Save the changes**.


**As a result**, Creatio will add a dashboard that can be viewed by users in the "All employees" role. You can change access rights on the live dashboard page. Learn more: [View and manage dashboards](https://academy.creatio.com/documents?id=1405). If you transfer the dashboard to a different environment, Creatio applies only default access rights in the target environment out of the box.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/set-up-dashboards-in-freedom-ui-designer\#see-also "Direct link to See also")

[Set up widgets](https://academy.creatio.com/documents?id=2144)

[View and manage dashboards](https://academy.creatio.com/documents?id=1405)

[Update list page template to include dashboards](https://academy.creatio.com/documents?id=2595)

[Tech Hour: UI/ UX Building pages in Freedom UI Designer](https://www.youtube.com/watch?v=qyqnRbUHnjQ)

[Tech Hour: UI/ UX Best practices in Creatio](https://www.youtube.com/watch?v=BdoiOu9ncmw)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/set-up-dashboards-in-freedom-ui-designer\#e-learning-courses "Direct link to E-learning courses")

[Analytics in Creatio. Working with dashboards](https://academy.creatio.com/node/542493/takecourse)

- [See also](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/set-up-dashboards-in-freedom-ui-designer#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ui-and-business-logic-customization/analytics/dashboards/set-up-dashboards-in-freedom-ui-designer#e-learning-courses)