define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's original report container (we use our own)
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "visible": false
                }
            },
            // Remove original report combo from parent
            {
                "operation": "remove",
                "name": "ComboBox_bo00lsk"
            },
            // Hide parent's date filters
            {
                "operation": "merge",
                "name": "CreatedFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "CreatedTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            // Remove parent's status order container
            {
                "operation": "remove",
                "name": "GridContainer_knkow5v"
            },
            {
                "operation": "remove",
                "name": "ComboBox_8w0dlcf"
            },
            // Hide iframe container (Looker Studio - blocked by CSP anyway)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },
            // Wire report button to our Excel handler
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "visible": true,
                    "clicked": {
                        "request": "usr.GenerateExcelReportRequest"
                    }
                }
            },
            // Add container for report selection
            {
                "operation": "insert",
                "name": "GridContainer_amm2zmo",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "visible": true,
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": {
                        "top": "none",
                        "right": "none",
                        "bottom": "none",
                        "left": "none"
                    }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 0
            },
            // Report selection combo
            {
                "operation": "insert",
                "name": "BGPampaReport",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Report",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_bsixu8a",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select a report...",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": ""
                },
                "parentName": "GridContainer_amm2zmo",
                "propertyName": "items",
                "index": 0
            },
            // Warning label for Commission reports
            {
                "operation": "insert",
                "name": "BGWarningLabel",
                "values": {
                    "type": "crt.Label",
                    "caption": "Date and transaction info derived from QuickBooks synced data.",
                    "labelType": "placeholder",
                    "labelThickness": "default",
                    "labelEllipsis": false,
                    "labelColor": "#D2310D",
                    "labelBackgroundColor": "transparent",
                    "labelTextAlign": "center",
                    "visible": "$UsrShowCommissionFilters"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },
            // Filter fields container (for Commission reports)
            {
                "operation": "insert",
                "name": "GridContainer_3asa01r",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCommissionFilters",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": {
                        "top": "none",
                        "right": "none",
                        "bottom": "none",
                        "left": "none"
                    }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },
            // Year-Month field
            {
                "operation": "insert",
                "name": "BGYearMonth",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_yubshr1",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": ""
                },
                "parentName": "GridContainer_3asa01r",
                "propertyName": "items",
                "index": 0
            },
            // Sales Group field
            {
                "operation": "insert",
                "name": "BGSalesGroup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_nt0mer7",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "",
                    "layoutConfig": {
                        "column": 2,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "",
                    "mode": "List"
                },
                "parentName": "GridContainer_3asa01r",
                "propertyName": "items",
                "index": 1
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
                    "LookupAttribute_bsixu8a": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGPampaReport"
                        }
                    },
                    "LookupAttribute_nt0mer7": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },
                    "LookupAttribute_yubshr1": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },
                    "LookupAttribute_nt0mer7_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [
                                    {
                                        "columnName": "BGSalesGroupName",
                                        "direction": "asc"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,
        handlers: /**SCHEMA_HANDLERS*/[
            // Handle report selection change - show/hide Commission filters
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_bsixu8a" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_bsixu8a;

                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission") ||
                                reportName.includes("iw_commission");
                            request.$context.UsrShowCommissionFilters = isCommissionReport;
                            request.$context.LookupAttribute_yubshr1 = null;
                            request.$context.LookupAttribute_nt0mer7 = null;
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                        }
                    }

                    if (request.attributeName === "LookupAttribute_yubshr1" && !request.silent) {
                        try {
                            const reloadDataRequest = {
                                type: "crt.LoadDataRequest",
                                $context: request.$context,
                                config: {
                                    loadType: "reload",
                                    useLastLoadParameters: true
                                },
                                dataSourceName: "LookupAttribute_nt0mer7_List_DS",
                                scopes: request.scopes ? [...request.scopes] : [],
                                customSource: "LookupAttribute_nt0mer7_List_DS"
                            };
                            await sdk.HandlerChainService.instance.process(reloadDataRequest);
                        } catch (e) {
                            console.log("[UsrPage_ebkv9e8] Sales Group reload failed:", e);
                        }
                    }

                    return next?.handle(request);
                }
            },
            // Report generation handler - uses UsrExcelReportService (NOT IntExcelReportService)
            {
                request: "usr.GenerateExcelReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;

                    // Get selected report
                    const selectedReport = await context.LookupAttribute_bsixu8a;
                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    let reportDisplayName = selectedReport.displayValue || "";

                    // Get filter values
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;

                    try {
                        const yearMonth = await context.LookupAttribute_yubshr1;
                        if (yearMonth && yearMonth.value) {
                            yearMonthId = yearMonth.value;
                        }
                    } catch (e) {}

                    try {
                        const salesGroup = await context.LookupAttribute_nt0mer7;
                        if (salesGroup && salesGroup.value) {
                            salesGroupId = salesGroup.value;
                        }
                    } catch (e) {}

                    // Get BPMCSRF token
                    const getCookie = (name) => {
                        const value = `; ${document.cookie}`;
                        const parts = value.split(`; ${name}=`);
                        if (parts.length === 2) return parts.pop().split(';').shift();
                        return "";
                    };
                    const bpmcsrf = getCookie("BPMCSRF");

                    // Call UsrExcelReportService (our custom service that properly stores bytes)
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({
                                ReportId: pampaReportId,
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId
                            })
                        });

                        const result = await response.json();
                        console.log("[UsrPage_ebkv9e8] UsrExcelReportService response:", result);

                        if (result.success && result.key) {
                            // Use UsrExcelReportService's GetReport endpoint
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName || "Report");

                            let iframe = document.getElementById('reportDownloadFrame');
                            if (!iframe) {
                                iframe = document.createElement('iframe');
                                iframe.id = 'reportDownloadFrame';
                                iframe.style.display = 'none';
                                document.body.appendChild(iframe);
                            }
                            iframe.src = downloadUrl;

                            Terrasoft.showInformation("Report generated - download starting...");
                        } else {
                            const errorMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Failed to generate report: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[UsrPage_ebkv9e8] Error:", error);
                        Terrasoft.showErrorMessage("Error generating report: " + error.message);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,
        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
