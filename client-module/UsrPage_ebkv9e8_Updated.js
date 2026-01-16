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
					}
				}
			}
		]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
		modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,
		handlers: /**SCHEMA_HANDLERS*/[
			{
				request: "crt.HandleViewModelAttributeChangeRequest",
				handler: async (request, next) => {
					// Cascade Sales Group options by selected Year-Month.
					// Trigger: when Report or Year-Month changes, reload the Sales Group lookup list DS.
					// Applies to:
					// - Commission (uses BGCommissionSalesGroupByYearMonth)
					// - IW_Commission (uses Payments object: IWPayments / IWPaymentsInvoice)
					try {
						if (
							request.attributeName === "LookupAttribute_bsixu8a" ||
							request.attributeName === "LookupAttribute_yubshr1"
						) {
							const reloadDataRequest = {
								type: "crt.LoadDataRequest",
								$context: request.$context,
								config: {
									loadType: "reload",
									useLastLoadParameters: true
								},
								dataSourceName: "LookupAttribute_nt0mer7_List_DS",
								scopes: [...(request.scopes || [])],
								customSource: "LookupAttribute_nt0mer7_List_DS"
							};
							await sdk.HandlerChainService.instance.process(reloadDataRequest);
						}
					} catch (e) {
						// best-effort; do not block the page
						console.log("SalesGroup cascade reload failed:", e);
					}
					return next?.handle(request);
				}
			},
			{
				request: "crt.LoadDataRequest",
				handler: async (request, next) => {
					// Apply dynamic filters to lookup list data sources.
					// - Report dropdown: only active reports
					// - Sales Group dropdown: filter to groups that have data for the selected Year-Month
					const addOrReplaceFilterParam = (params, filterValue) => {
						const existing = Array.isArray(params) ? params : [];
						const kept = existing.filter(p => p && p.type !== "filter");
						return [...kept, { type: "filter", value: filterValue }];
					};

					// Active reports only
					if (request.dataSourceName === "LookupAttribute_bsixu8a_List_DS") {
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

					const salesGroupDS = "LookupAttribute_nt0mer7_List_DS";
					if (request.dataSourceName === salesGroupDS || request.customSource === salesGroupDS) {
						const emptyGuid = "00000000-0000-0000-0000-000000000000";

						// Read Year-Month and Report selection from context
						const ym = request.$context?.attributes?.LookupAttribute_yubshr1;
						const yearMonthId = ym && ym.value ? ym.value : null;

						const reportSel = request.$context?.attributes?.LookupAttribute_bsixu8a;
						const reportId = reportSel && reportSel.value ? reportSel.value : null;
						let reportCode = reportSel && reportSel.displayValue ? reportSel.displayValue : null;

						// Resolve UsrCode when possible (more stable than displayValue)
						if (reportId) {
							try {
								const reportModel = await sdk.Model.create("UsrReportesPampa");
								const rows = await reportModel.load({
									attributes: ["Id", "UsrCode"],
									parameters: [
										{
											type: sdk.ModelParameterType.PrimaryColumnValue,
											value: reportId
										}
									]
								});
								if (rows && rows.length > 0 && rows[0].UsrCode) {
									reportCode = rows[0].UsrCode;
								}
							} catch (e) {
								console.log("UsrReportesPampa UsrCode lookup failed:", e);
							}
						}

						// Only apply cascade for the two target reports.
						if (!yearMonthId || !(reportCode === "Commission" || reportCode === "IW_Commission")) {
							return await next?.handle(request);
						}

						let allowedGroupIds = [];

						if (reportCode === "Commission") {
							// Source of truth for valid combos: BGCommissionSalesGroupByYearMonth
							try {
								const model = await sdk.Model.create("BGCommissionSalesGroupByYearMonth");
								const filters = new sdk.FilterGroup();
								await filters.addSchemaColumnFilterWithParameter(
									sdk.ComparisonType.Equal,
									"BGYearMonth",
									yearMonthId
								);
								const groups = await model.load({
									attributes: ["Id", "BGSalesGroup"],
									parameters: [
										{ type: sdk.ModelParameterType.Filter, value: filters }
									]
								});
								for (let i = 0; i < (groups || []).length; i++) {
									const sg = groups[i]?.BGSalesGroup;
									if (sg && sg.value) {
										allowedGroupIds.push(sg.value);
									}
								}
							} catch (e) {
								console.log("Commission SalesGroup cascade query failed:", e);
								// best-effort: if we can't compute allowed groups, don't filter
								return await next?.handle(request);
							}
						} else if (reportCode === "IW_Commission") {
							// IW_Commission uses the Payments object: IWPayments / IWPaymentsInvoice
							try {
								const paymentsModel = await sdk.Model.create("IWPayments");
								const filters = new sdk.FilterGroup();
								await filters.addSchemaColumnFilterWithParameter(
									sdk.ComparisonType.Equal,
									"IWBGYearMonth",
									yearMonthId
								);

								// First try: load SalesGroup directly via ESQ column path.
								let payments = [];
								try {
									payments = await paymentsModel.load({
										attributes: ["Id", "IWPaymentsInvoice.BGSalesGroup"],
										parameters: [
											{ type: sdk.ModelParameterType.Filter, value: filters }
										]
									});
								} catch (e) {
									payments = [];
								}

								for (let i = 0; i < (payments || []).length; i++) {
									const sg = payments[i]?.["IWPaymentsInvoice.BGSalesGroup"];
									if (sg && sg.value) {
										allowedGroupIds.push(sg.value);
									}
								}

								// Fallback: if direct path didn't work, try 2-step via IWPaymentsInvoice.
								if (allowedGroupIds.length === 0) {
									let payments2 = [];
									try {
										payments2 = await paymentsModel.load({
											attributes: ["Id", "IWPaymentsInvoice"],
											parameters: [
												{ type: sdk.ModelParameterType.Filter, value: filters }
											]
										});
									} catch (e) {
										payments2 = [];
									}

									const invoiceIds = [];
									for (let i = 0; i < (payments2 || []).length; i++) {
										const inv = payments2[i]?.IWPaymentsInvoice;
										if (inv && inv.value) {
											invoiceIds.push(inv.value);
										}
									}

									// Keep the filter manageable.
									const uniqueInvoiceIds = Array.from(new Set(invoiceIds)).slice(0, 200);
									if (uniqueInvoiceIds.length > 0) {
										try {
											const invModel = await sdk.Model.create("IWPaymentsInvoice");
											const invFilter = new sdk.FilterGroup();
											for (let i = 0; i < uniqueInvoiceIds.length; i++) {
												await invFilter.addSchemaColumnFilterWithParameter(
													sdk.ComparisonType.Equal,
													"Id",
													uniqueInvoiceIds[i]
												);
											}
											// OR semantics
											invFilter.logicalOperation = Terrasoft.LogicalOperatorType.OR;
											const invoices = await invModel.load({
												attributes: ["Id", "BGSalesGroup"],
												parameters: [
													{ type: sdk.ModelParameterType.Filter, value: invFilter }
												]
											});
											for (let i = 0; i < (invoices || []).length; i++) {
												const sg = invoices[i]?.BGSalesGroup;
												if (sg && sg.value) {
													allowedGroupIds.push(sg.value);
												}
											}
										} catch (e) {
											console.log("IWPaymentsInvoice fallback cascade query failed:", e);
										}
									}
								}
							} catch (e) {
								console.log("IW SalesGroup cascade query failed:", e);
								// best-effort: if we can't compute allowed groups, don't filter
								return await next?.handle(request);
							}
						}

						// De-dupe and cap size to keep request small.
						allowedGroupIds = Array.from(new Set(allowedGroupIds)).slice(0, 200);

						// If no groups exist for the selected (report, year-month), warn and do NOT filter the lookup list.
						// This keeps the user unblocked (they can still pick any group and export), but signals likely empties.
						if (allowedGroupIds.length === 0) {
							try {
								const warnKey = `${reportCode}|${yearMonthId}`;
								if (request.$context && request.$context.UsrLastSalesGroupEmptyWarningKey !== warnKey) {
									request.$context.UsrLastSalesGroupEmptyWarningKey = warnKey;
									Terrasoft.showInformation(
										"No Sales Groups found for the selected Year-Month. Export may be empty, but you can still export."
									);
								}
							} catch (e) {
								// ignore
							}
							return await next?.handle(request);
						}

						const filter = new sdk.FilterGroup();
						for (let i = 0; i < allowedGroupIds.length; i++) {
							await filter.addSchemaColumnFilterWithParameter(
								sdk.ComparisonType.Equal,
								"Id",
								allowedGroupIds[i]
							);
						}

						// OR semantics across allowed groups.
						// Use a plain object (not the FilterGroup instance) to match Creatio request expectations.
						const newFilter = Object.assign({}, filter);
						newFilter.items = filter.items;
						newFilter.logicalOperation = Terrasoft.LogicalOperatorType.OR;
						request.parameters = addOrReplaceFilterParam(request.parameters, newFilter);
					}

					return await next?.handle(request);
				}
			},
			{
				request: "usr.GenerateExcelReportRequest",
				handler: async (request, next) => {
					const context = request.$context;

					// Get the selected report from UsrReportesPampa lookup
					// FreedomUI uses LookupAttribute_bsixu8a which maps to BGPampaReport
					const selectedReport = await context.LookupAttribute_bsixu8a;
					if (!selectedReport || !selectedReport.value) {
						Terrasoft.showErrorMessage("Please select a report");
						return next?.handle(request);
					}
					const pampaReportId = selectedReport.value;

					// In DEV, /IntExcelReportService/GetReport/{key}/{reportNameSegment} is sensitive to the
					// {reportNameSegment} value. For most reports this should be the *code* (UsrReportesPampa.UsrCode),
					// not the user-facing name (UsrReportesPampa.Name) which may include spaces.
					let reportDisplayName = selectedReport.displayValue || "";
					let reportCode = reportDisplayName;

					// Get filter values with defensive null handling
					const emptyGuid = "00000000-0000-0000-0000-000000000000";
					let yearMonthId = emptyGuid;
					let salesGroupId = emptyGuid;

					try {
						// FreedomUI uses LookupAttribute_yubshr1 which maps to BGYearMonth
						const yearMonth = await context.LookupAttribute_yubshr1;
						if (yearMonth && yearMonth.value) {
							yearMonthId = yearMonth.value;
						}
					} catch (e) {
						console.log("BGYearMonth not available:", e);
					}

					try {
						// FreedomUI uses LookupAttribute_nt0mer7 which maps to BGSalesGroup
						const salesGroup = await context.LookupAttribute_nt0mer7;
						if (salesGroup && salesGroup.value) {
							salesGroupId = salesGroup.value;
						}
					} catch (e) {
						console.log("BGSalesGroup not available:", e);
					}

					// Get BPMCSRF token for authentication
					const getCookie = (name) => {
						const value = `; ${document.cookie}`;
						const parts = value.split(`; ${name}=`);
						if (parts.length === 2) return parts.pop().split(';').shift();
						return "";
					};
					const bpmcsrf = getCookie("BPMCSRF");

					// Fetch UsrReportesPampa metadata to get a stable code for downloads.
					// NOTE: In this env, the OData key lookup works as UsrReportesPampa(<guid>) (no guid'...' wrapper).
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
						console.log("UsrReportesPampa metadata lookup failed:", e);
					}

					// Resolve UsrReportesPampa to IntExcelReport
					// The UI uses UsrReportesPampa but the service needs IntExcelReport.Id
					let intExcelReportId = emptyGuid;
					try {
						// Use OData to find IntExcelReport by name pattern.
						// - reportDisplayName is user-facing (often matches the IntName suffix)
						// - reportCode is the stable code (good as an extra fallback)
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
							console.log("Found IntExcelReport:", odataResult.value[0].IntName, "->", intExcelReportId);
						} else {
							console.warn("IntExcelReport not found for:", reportDisplayName);
							Terrasoft.showErrorMessage("Excel report template not found for: " + reportDisplayName);
							return next?.handle(request);
						}
					} catch (e) {
						console.error("Error looking up IntExcelReport:", e);
						Terrasoft.showErrorMessage("Error finding report template: " + e.message);
						return next?.handle(request);
					}

					console.log("Report generation request:", {
						pampaReportId: pampaReportId,
						intExcelReportId: intExcelReportId,
						reportDisplayName: reportDisplayName,
						reportCode: reportCode,
						yearMonthId: yearMonthId,
						salesGroupId: salesGroupId
					});

					try {
						// Call our wrapper service with the correct IntExcelReport ID
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
						console.log("Service response:", result);

						if (result.success && result.key) {
							// File name is user-facing; download segment must be the *code*.
							const reportNameSegment = reportCode || reportDisplayName || "Report";
							// Use IntExcelReportService/GetReport since the library stores report data there.
							// UsrExcelReportService/Generate calls the library internally, which stores in IntExcelReportService's cache.
							const downloadUrl = "/0/rest/IntExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportNameSegment);

							console.log("Initiating download via:", downloadUrl);

							// ROBUST DOWNLOAD APPROACH - Hidden Iframe
							// Why iframe instead of other methods:
							// - object-URL downloads (URL.createObjectURL): Chrome can show "File wasn't available on site"
							//   if URL.revokeObjectURL() is called too quickly (common timing bug)
							// - window.open(): Can be blocked by popup blockers
							// - Hidden iframe: Works reliably for same-origin authenticated requests
							//   with proper Content-Disposition headers (which IntExcelReportService provides)
							//
							// The iframe receives cookies (BPMCSRF) automatically since it's same-origin.
							// The server's Content-Disposition: attachment header triggers the download.

							let iframe = document.getElementById('reportDownloadFrame');
							if (!iframe) {
								iframe = document.createElement('iframe');
								iframe.id = 'reportDownloadFrame';
								iframe.style.display = 'none';
								iframe.setAttribute('aria-hidden', 'true');
								document.body.appendChild(iframe);
							}

							// Set src to trigger download
							iframe.src = downloadUrl;

							Terrasoft.showInformation("Report generated - download starting...");
						} else {
							Terrasoft.showErrorMessage("Failed to generate report: " + (result.message || "Unknown error"));
						}
					} catch (error) {
						console.error("Report generation error:", error);
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
