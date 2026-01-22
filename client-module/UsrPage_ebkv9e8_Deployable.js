define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
	return {
		viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
			// Hide parent's original containers
			{
				"operation": "merge",
				"name": "GridContainer_oshnwh8",
				"values": {
					"visible": false
				}
			},
			{
				"operation": "remove",
				"name": "ComboBox_bo00lsk"
			},
			{
				"operation": "merge",
				"name": "GridContainer_xdy25v1",
				"values": {
					"alignItems": "stretch"
				}
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
				"operation": "move",
				"name": "CreatedFrom",
				"parentName": "FlexContainer_bz6bzit",
				"propertyName": "items",
				"index": 0
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
				"operation": "move",
				"name": "CreatedTo",
				"parentName": "FlexContainer_r5g4x6l",
				"propertyName": "items",
				"index": 0
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
				"operation": "move",
				"name": "ShippingFrom",
				"parentName": "FlexContainer_bz6bzit",
				"propertyName": "items",
				"index": 1
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
				"operation": "move",
				"name": "ShippingTo",
				"parentName": "FlexContainer_r5g4x6l",
				"propertyName": "items",
				"index": 1
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
				"operation": "move",
				"name": "DeliveryFrom",
				"parentName": "FlexContainer_bz6bzit",
				"propertyName": "items",
				"index": 2
			},
			{
				"operation": "merge",
				"name": "DeliveryTo",
				"values": {
					"visible": false,
					"layoutConfig": {}
				}
			},
			{
				"operation": "move",
				"name": "DeliveryTo",
				"parentName": "FlexContainer_r5g4x6l",
				"propertyName": "items",
				"index": 2
			},
			{
				"operation": "remove",
				"name": "GridContainer_knkow5v"
			},
			{
				"operation": "remove",
				"name": "ComboBox_8w0dlcf"
			},
			// MAKE THE BUTTON VISIBLE - key fix
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
			// Hide iframe (Looker Studio)
			{
				"operation": "merge",
				"name": "GridContainer_fh039aq",
				"values": {
					"visible": false
				}
			},
			// Report selection - visible
			{
				"operation": "insert",
				"name": "BGReport",
				"values": {
					"type": "crt.ComboBox",
					"label": "$Resources.Strings.LookupAttribute_0as4io2",
					"ariaLabel": "Report",
					"isAddAllowed": true,
					"showValueAsLink": true,
					"labelPosition": "auto",
					"controlActions": [],
					"listActions": [],
					"tooltip": "",
					"readonly": false,
					"control": "$LookupAttribute_0as4io2",
					"layoutConfig": {},
					"visible": true,
					"placeholder": ""
				},
				"parentName": "GridContainer_oshnwh8",
				"propertyName": "items",
				"index": 0
			},
			// Report selection container
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
				"index": 2
			},
			// Main report lookup (BGPampaReport) - this is the primary selector
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
			// Warning label - bound to visibility attribute
			{
				"operation": "insert",
				"name": "BGWarningLabel",
				"values": {
					"type": "crt.Label",
					"caption": "Date/transaction info derived from QuickBooks synced data.",
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
				"index": 3
			},
			// Filter fields container - bound to visibility attribute
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
				"index": 4
			},
			// Left filter column
			{
				"operation": "insert",
				"name": "FlexContainer_bz6bzit",
				"values": {
					"layoutConfig": {
						"column": 1,
						"row": 1,
						"colSpan": 1,
						"rowSpan": 1
					},
					"type": "crt.FlexContainer",
					"direction": "column",
					"items": [],
					"fitContent": true
				},
				"parentName": "GridContainer_3asa01r",
				"propertyName": "items",
				"index": 0
			},
			// Right filter column
			{
				"operation": "insert",
				"name": "FlexContainer_r5g4x6l",
				"values": {
					"layoutConfig": {
						"column": 2,
						"row": 1,
						"colSpan": 1,
						"rowSpan": 1
					},
					"type": "crt.FlexContainer",
					"direction": "column",
					"items": [],
					"fitContent": true
				},
				"parentName": "GridContainer_3asa01r",
				"propertyName": "items",
				"index": 1
			},
			// Year-Month field - VISIBLE when Commission selected
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
					"visible": true,
					"placeholder": "",
					"tooltip": ""
				},
				"parentName": "FlexContainer_bz6bzit",
				"propertyName": "items",
				"index": 7
			},
			// Sales Group field - VISIBLE when Commission selected
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
					"visible": true,
					"placeholder": "",
					"tooltip": "",
					"mode": "List"
				},
				"parentName": "FlexContainer_r5g4x6l",
				"propertyName": "items",
				"index": 6
			},
			// Button container for report generation
			{
				"operation": "insert",
				"name": "FlexContainer_raycxry",
				"values": {
					"type": "crt.FlexContainer",
					"direction": "row",
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
					},
					"justifyContent": "center",
					"alignItems": "center",
					"gap": "large",
					"wrap": "wrap"
				},
				"parentName": "MainContainer",
				"propertyName": "items",
				"index": 6
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
					// Reload Sales Group when report or Year-Month changes
					if (request.attributeName === "LookupAttribute_bsixu8a" || request.attributeName === "LookupAttribute_yubshr1") {
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

					// Handle report selection - show/hide Commission filters
					if (request.attributeName === "LookupAttribute_bsixu8a" && !request.silent) {
						const selectedReport = await request.$context.LookupAttribute_bsixu8a;

						if (selectedReport && selectedReport.displayValue) {
							const reportName = selectedReport.displayValue.toLowerCase();
							// Show Year-Month and Sales Group for Commission reports
							const isCommissionReport = reportName.includes("commission") ||
								reportName.includes("iw_commission");
							request.$context.UsrShowCommissionFilters = isCommissionReport;

							// Clear filter values when report changes
							request.$context.LookupAttribute_yubshr1 = null;
							request.$context.LookupAttribute_nt0mer7 = null;
						} else {
							request.$context.UsrShowCommissionFilters = false;
						}
					}

					return next?.handle(request);
				}
			},
			// Report generation - uses native IntExcelExport
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
					let reportCode = reportDisplayName;

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

					// Fetch report metadata
					try {
						const reportMetaUrl = "/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrCode";
						const reportMetaResp = await fetch(reportMetaUrl, {
							method: "GET",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
						});
						if (reportMetaResp.ok) {
							const reportMeta = await reportMetaResp.json();
							reportDisplayName = reportMeta.Name || reportDisplayName;
							reportCode = reportMeta.UsrCode || reportCode;
						}
					} catch (e) {
						console.log("[UsrPage_ebkv9e8] Metadata lookup failed:", e);
					}

					// Find IntExcelReport by name
					let intExcelReportId = null;
					try {
						const escapeName = (s) => s.replace(/'/g, "''");
						const odataUrl = "/0/odata/IntExcelReport?$filter=" +
							"(IntName eq '" + escapeName(reportDisplayName) + "'" +
							" or IntName eq 'Rpt " + escapeName(reportDisplayName) + "'" +
							" or IntName eq '" + escapeName(reportCode) + "'" +
							" or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
							"&$select=Id,IntName&$top=1";

						const odataResponse = await fetch(odataUrl, {
							method: "GET",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
						});

						const odataResult = await odataResponse.json();
						if (odataResult.value && odataResult.value.length > 0) {
							intExcelReportId = odataResult.value[0].Id;
							console.log("[UsrPage_ebkv9e8] Found IntExcelReport:", odataResult.value[0].IntName);
						} else {
							Terrasoft.showErrorMessage("Excel report template not found for: " + reportDisplayName);
							return next?.handle(request);
						}
					} catch (e) {
						Terrasoft.showErrorMessage("Error finding report template: " + e.message);
						return next?.handle(request);
					}

					// Call native IntExcelExport service
					try {
						const response = await fetch("/0/rest/IntExcelReportService/Generate", {
							method: "POST",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
							body: JSON.stringify({
								reportId: intExcelReportId,
								recordId: null,
								recordCollection: []
							})
						});

						const result = await response.json();
						console.log("[UsrPage_ebkv9e8] IntExcelReportService response:", result);

						if (result.success && result.key) {
							const downloadUrl = "/0/rest/IntExcelReportService/GetReport/" + result.key;

							// Use hidden iframe for download
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
							Terrasoft.showErrorMessage("Failed: " + (result.message || result.errorMessage || "Unknown error"));
						}
					} catch (error) {
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
