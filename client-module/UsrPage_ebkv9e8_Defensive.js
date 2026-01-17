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
					// DEFENSIVE: Only run cascade logic if we're on the reports page
					// and the changed attribute is one we care about
					const isReportsPage = request.$context?.pageName === "UsrPage_ebkv9e8" ||
						request.$context?.modelName === "UsrPage_ebkv9e8" ||
						(request.$context?.attributes?.LookupAttribute_bsixu8a !== undefined);

					if (!isReportsPage) {
						// Not our page - pass through immediately without any custom logic
						return next?.handle(request);
					}

					// Only trigger cascade for specific attribute changes
					const cascadeAttributes = ["LookupAttribute_bsixu8a", "LookupAttribute_yubshr1"];
					if (!cascadeAttributes.includes(request.attributeName)) {
						return next?.handle(request);
					}

					// Cascade Sales Group options by selected Year-Month (defensive)
					try {
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
					} catch (e) {
						// DEFENSIVE: Log but never block - cascade is a UX feature, not critical
						console.log("[UsrPage_ebkv9e8] SalesGroup cascade reload failed (non-blocking):", e);
					}

					return next?.handle(request);
				}
			},
			{
				request: "crt.LoadDataRequest",
				handler: async (request, next) => {
					// DEFENSIVE: Early exit for unrelated data sources
					// Only intercept specific data sources we need to filter
					const targetDataSources = [
						"LookupAttribute_bsixu8a_List_DS",  // Report dropdown
						"LookupAttribute_nt0mer7_List_DS"   // Sales Group dropdown
					];

					const isTargetDS = targetDataSources.includes(request.dataSourceName) ||
						targetDataSources.includes(request.customSource);

					if (!isTargetDS) {
						// Not a data source we care about - pass through immediately
						return next?.handle(request);
					}

					// DEFENSIVE: Verify we're on the reports page context
					const hasReportContext = request.$context?.attributes?.LookupAttribute_bsixu8a !== undefined;
					if (!hasReportContext) {
						// No report context - this might be a different page loading similar data
						return next?.handle(request);
					}

					// Helper function to safely add/replace filter parameters
					const addOrReplaceFilterParam = (params, filterValue) => {
						try {
							const existing = Array.isArray(params) ? params : [];
							const kept = existing.filter(p => p && p.type !== "filter");
							return [...kept, { type: "filter", value: filterValue }];
						} catch (e) {
							console.log("[UsrPage_ebkv9e8] Filter param error (using original):", e);
							return params;
						}
					};

					// Active reports only filter
					if (request.dataSourceName === "LookupAttribute_bsixu8a_List_DS") {
						try {
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
						} catch (e) {
							console.log("[UsrPage_ebkv9e8] Active reports filter failed (non-blocking):", e);
						}
						return next?.handle(request);
					}

					// Sales Group cascade filter
					const salesGroupDS = "LookupAttribute_nt0mer7_List_DS";
					if (request.dataSourceName === salesGroupDS || request.customSource === salesGroupDS) {
						try {
							const emptyGuid = "00000000-0000-0000-0000-000000000000";

							// Read Year-Month and Report selection from context
							const ym = request.$context?.attributes?.LookupAttribute_yubshr1;
							const yearMonthId = ym && ym.value ? ym.value : null;

							const reportSel = request.$context?.attributes?.LookupAttribute_bsixu8a;
							const reportId = reportSel && reportSel.value ? reportSel.value : null;
							let reportCode = reportSel && reportSel.displayValue ? reportSel.displayValue : null;

							// DEFENSIVE: If no year-month selected, skip cascade (show all groups)
							if (!yearMonthId) {
								return next?.handle(request);
							}

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
									// DEFENSIVE: Use displayValue as fallback
									console.log("[UsrPage_ebkv9e8] UsrCode lookup failed, using displayValue:", e);
								}
							}

							// Only apply cascade for specific reports
							if (!(reportCode === "Commission" || reportCode === "IW_Commission")) {
								return next?.handle(request);
							}

							let allowedGroupIds = [];

							if (reportCode === "Commission") {
								// Commission uses BGCommissionSalesGroupByYearMonth
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
									// DEFENSIVE: If query fails, don't filter - show all groups
									console.log("[UsrPage_ebkv9e8] Commission cascade query failed (showing all groups):", e);
									return next?.handle(request);
								}
							} else if (reportCode === "IW_Commission") {
								// IW_Commission uses IWPayments - DEFENSIVE wrapper
								try {
									const paymentsModel = await sdk.Model.create("IWPayments");
									const filters = new sdk.FilterGroup();
									await filters.addSchemaColumnFilterWithParameter(
										sdk.ComparisonType.Equal,
										"IWBGYearMonth",
										yearMonthId
									);

									// First try: load SalesGroup directly
									let payments = [];
									try {
										payments = await paymentsModel.load({
											attributes: ["Id", "IWPaymentsInvoice.BGSalesGroup"],
											parameters: [
												{ type: sdk.ModelParameterType.Filter, value: filters }
											]
										});
									} catch (e) {
										// Direct path failed - will try fallback
										payments = [];
									}

									for (let i = 0; i < (payments || []).length; i++) {
										const sg = payments[i]?.["IWPaymentsInvoice.BGSalesGroup"];
										if (sg && sg.value) {
											allowedGroupIds.push(sg.value);
										}
									}

									// Fallback: 2-step via IWPaymentsInvoice (only if direct failed)
									if (allowedGroupIds.length === 0) {
										try {
											const payments2 = await paymentsModel.load({
												attributes: ["Id", "IWPaymentsInvoice"],
												parameters: [
													{ type: sdk.ModelParameterType.Filter, value: filters }
												]
											});

											const invoiceIds = [];
											for (let i = 0; i < (payments2 || []).length; i++) {
												const inv = payments2[i]?.IWPaymentsInvoice;
												if (inv && inv.value) {
													invoiceIds.push(inv.value);
												}
											}

											// Keep filter manageable - limit to 200 invoices
											const uniqueInvoiceIds = Array.from(new Set(invoiceIds)).slice(0, 200);
											if (uniqueInvoiceIds.length > 0) {
												const invModel = await sdk.Model.create("IWPaymentsInvoice");
												const invFilter = new sdk.FilterGroup();
												for (let i = 0; i < uniqueInvoiceIds.length; i++) {
													await invFilter.addSchemaColumnFilterWithParameter(
														sdk.ComparisonType.Equal,
														"Id",
														uniqueInvoiceIds[i]
													);
												}
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
											}
										} catch (e) {
											// DEFENSIVE: Fallback also failed - show all groups
											console.log("[UsrPage_ebkv9e8] IWPayments fallback failed (showing all groups):", e);
										}
									}
								} catch (e) {
									// DEFENSIVE: IWPayments query failed - don't block, show all groups
									console.log("[UsrPage_ebkv9e8] IW cascade query failed (showing all groups):", e);
									return next?.handle(request);
								}
							}

							// De-dupe and cap size
							allowedGroupIds = Array.from(new Set(allowedGroupIds)).slice(0, 200);

							// If no groups found, warn but don't filter (allow all)
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
									// Ignore warning display errors
								}
								return next?.handle(request);
							}

							// Build filter for allowed groups
							try {
								const filter = new sdk.FilterGroup();
								for (let i = 0; i < allowedGroupIds.length; i++) {
									await filter.addSchemaColumnFilterWithParameter(
										sdk.ComparisonType.Equal,
										"Id",
										allowedGroupIds[i]
									);
								}

								const newFilter = Object.assign({}, filter);
								newFilter.items = filter.items;
								newFilter.logicalOperation = Terrasoft.LogicalOperatorType.OR;
								request.parameters = addOrReplaceFilterParam(request.parameters, newFilter);
							} catch (e) {
								// DEFENSIVE: Filter build failed - show all groups
								console.log("[UsrPage_ebkv9e8] Filter build failed (showing all groups):", e);
							}
						} catch (e) {
							// DEFENSIVE: Outer catch - any unexpected error, just pass through
							console.log("[UsrPage_ebkv9e8] Sales Group cascade error (non-blocking):", e);
						}
					}

					return next?.handle(request);
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
						console.log("BGYearMonth not available:", e);
					}

					try {
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
						console.log("UsrReportesPampa metadata lookup failed:", e);
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
						console.log("Service response:", result);

						if (result.success && result.key) {
							const reportNameSegment = reportCode || reportDisplayName || "Report";
							const downloadUrl = "/0/rest/IntExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportNameSegment);

							console.log("Initiating download via:", downloadUrl);

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
