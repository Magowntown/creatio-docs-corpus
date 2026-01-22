define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {
	return {
		viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
			{
				"operation": "merge",
				"name": "Button_vae0g6x",
				"values": {
					"clicked": {
						"request": "usr.GenerateExcelReportRequest"
					}
				}
			}
		]/**SCHEMA_VIEW_CONFIG_DIFF*/,
		viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
			{
				"operation": "merge",
				"path": [
					"attributes"
				],
				"values": {
					"LookupAttribute_bsixu8a_List": {
						"isCollection": true,
						"modelConfig": {
							"sortingConfig": {
								"default": [
									{
										"columnName": "Name",
										"direction": "asc"
									}
								]
							}
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
			// Sales Group Fix Version
			// - Restores Sales Group loading via crt.LoadDataRequest
			// - Uses only fetch() and Terrasoft (no sdk dependency)
			// - NO framework interceptors that could block page loading
			{
				request: "crt.LoadDataRequest",
				handler: async (request, next) => {
					// Only intercept for Sales Group data source - apply active filter
					const salesGroupDS = "LookupAttribute_nt0mer7_List_DS";

					if (request.dataSourceName === salesGroupDS || request.customSource === salesGroupDS) {
						// Add filter for active sales groups only (if BGIsActive column exists)
						const addOrReplaceFilterParam = (params, filterValue) => {
							const existing = Array.isArray(params) ? params : [];
							const kept = existing.filter(p => p && p.type !== "filter");
							return [...kept, { type: "filter", value: filterValue }];
						};

						// Filter to active groups only
						request.parameters = addOrReplaceFilterParam(request.parameters, {
							items: {
								"ActiveOnly": {
									filterType: 1,
									comparisonType: 3,
									isEnabled: true,
									trimDateTimeParameterToDate: false,
									leftExpression: { expressionType: 0, columnPath: "BGIsActive" },
									isAggregative: false,
									dataValueType: 12,
									rightExpression: {
										expressionType: 2,
										parameter: { dataValueType: 12, value: true }
									}
								}
							},
							logicalOperation: 0,
							isEnabled: true,
							filterType: 6
						});
					}

					// Active reports filter
					if (request.dataSourceName === "LookupAttribute_bsixu8a_List_DS") {
						const addOrReplaceFilterParam = (params, filterValue) => {
							const existing = Array.isArray(params) ? params : [];
							const kept = existing.filter(p => p && p.type !== "filter");
							return [...kept, { type: "filter", value: filterValue }];
						};

						request.parameters = addOrReplaceFilterParam(request.parameters, {
							items: {
								"UsrActiveOnly": {
									filterType: 1,
									comparisonType: 3,
									isEnabled: true,
									trimDateTimeParameterToDate: false,
									leftExpression: { expressionType: 0, columnPath: "UsrActive" },
									isAggregative: false,
									dataValueType: 12,
									rightExpression: {
										expressionType: 2,
										parameter: { dataValueType: 12, value: true }
									}
								}
							},
							logicalOperation: 0,
							isEnabled: true,
							filterType: 6
						});
					}

					return await next?.handle(request);
				}
			},
			{
				request: "usr.GenerateExcelReportRequest",
				handler: async (request, next) => {
					const context = request.$context;

					// Get the selected report from UsrReportesPampa lookup
					const selectedReport = await context.LookupAttribute_bsixu8a;
					if (!selectedReport || !selectedReport.value) {
						Terrasoft.showErrorMessage("Please select a report");
						return next?.handle(request);
					}
					const pampaReportId = selectedReport.value;

					let reportDisplayName = selectedReport.displayValue || "";
					let reportCode = reportDisplayName;

					// Get filter values with defensive null handling
					const emptyGuid = "00000000-0000-0000-0000-000000000000";
					let yearMonthId = emptyGuid;
					let salesGroupId = emptyGuid;

					try {
						const yearMonth = await context.LookupAttribute_yubshr1;
						if (yearMonth && yearMonth.value) {
							yearMonthId = yearMonth.value;
						}
					} catch (e) {
						console.log("[UsrPage_ebkv9e8] BGYearMonth not available:", e);
					}

					try {
						const salesGroup = await context.LookupAttribute_nt0mer7;
						if (salesGroup && salesGroup.value) {
							salesGroupId = salesGroup.value;
						}
					} catch (e) {
						console.log("[UsrPage_ebkv9e8] BGSalesGroup not available:", e);
					}

					// Get BPMCSRF token for authentication
					const getCookie = (name) => {
						const value = `; ${document.cookie}`;
						const parts = value.split(`; ${name}=`);
						if (parts.length === 2) return parts.pop().split(';').shift();
						return "";
					};
					const bpmcsrf = getCookie("BPMCSRF");

					// Fetch UsrReportesPampa metadata to get a stable code
					try {
						const reportMetaUrl = "/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrCode";
						const reportMetaResp = await fetch(reportMetaUrl, {
							method: "GET",
							headers: {
								"Content-Type": "application/json",
								"BPMCSRF": bpmcsrf
							}
						});
						if (reportMetaResp.ok) {
							const reportMeta = await reportMetaResp.json();
							reportDisplayName = reportMeta.Name || reportDisplayName;
							reportCode = reportMeta.UsrCode || reportCode;
						}
					} catch (e) {
						console.log("[UsrPage_ebkv9e8] UsrReportesPampa metadata lookup failed:", e);
					}

					// Resolve UsrReportesPampa to IntExcelReport
					let intExcelReportId = emptyGuid;
					try {
						const odataUrl = "/0/odata/IntExcelReport?$filter=" +
							"(IntName eq '" + reportDisplayName + "'" +
							" or IntName eq 'Rpt " + reportDisplayName + "'" +
							" or IntName eq '" + reportCode + "'" +
							" or IntName eq 'Rpt " + reportCode + "')" +
							"&$select=Id,IntName&$top=1";

						const odataResponse = await fetch(odataUrl, {
							method: "GET",
							headers: {
								"Content-Type": "application/json",
								"BPMCSRF": bpmcsrf
							}
						});

						const odataResult = await odataResponse.json();
						if (odataResult.value && odataResult.value.length > 0) {
							intExcelReportId = odataResult.value[0].Id;
							console.log("[UsrPage_ebkv9e8] Found IntExcelReport:", odataResult.value[0].IntName, "->", intExcelReportId);
						} else {
							console.warn("[UsrPage_ebkv9e8] IntExcelReport not found for:", reportDisplayName);
							Terrasoft.showErrorMessage("Excel report template not found for: " + reportDisplayName);
							return next?.handle(request);
						}
					} catch (e) {
						console.error("[UsrPage_ebkv9e8] Error looking up IntExcelReport:", e);
						Terrasoft.showErrorMessage("Error finding report template: " + e.message);
						return next?.handle(request);
					}

					console.log("[UsrPage_ebkv9e8] Report generation request:", {
						pampaReportId: pampaReportId,
						intExcelReportId: intExcelReportId,
						reportDisplayName: reportDisplayName,
						reportCode: reportCode,
						yearMonthId: yearMonthId,
						salesGroupId: salesGroupId
					});

					try {
						// Call wrapper service with correct IntExcelReport ID
						const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
							method: "POST",
							headers: {
								"Content-Type": "application/json",
								"BPMCSRF": bpmcsrf
							},
							body: JSON.stringify({
								ReportId: intExcelReportId,
								YearMonthId: yearMonthId,
								SalesRepId: salesGroupId,
								ExecutionId: emptyGuid,
								RecordCollection: []
							})
						});

						const result = await response.json();
						console.log("[UsrPage_ebkv9e8] Service response:", result);

						if (result.success && result.key) {
							const reportNameSegment = reportCode || reportDisplayName || "Report";
							const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportNameSegment);

							console.log("[UsrPage_ebkv9e8] Initiating download via:", downloadUrl);

							// Hidden iframe download (robust approach)
							let iframe = document.getElementById('reportDownloadFrame');
							if (!iframe) {
								iframe = document.createElement('iframe');
								iframe.id = 'reportDownloadFrame';
								iframe.style.display = 'none';
								iframe.setAttribute('aria-hidden', 'true');
								document.body.appendChild(iframe);
							}

							iframe.src = downloadUrl;

							Terrasoft.showInformation("Report generated - download starting...");
						} else {
							Terrasoft.showErrorMessage("Failed to generate report: " + (result.message || "Unknown error"));
						}
					} catch (error) {
						console.error("[UsrPage_ebkv9e8] Report generation error:", error);
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
