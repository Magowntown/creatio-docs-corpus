define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {
	return {
		viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
			{
				"operation": "merge",
				"name": "Button_bwctkw5",
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

					// Get filter values
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

					// Get BPMCSRF token
					const getCookie = (name) => {
						const value = `; ${document.cookie}`;
						const parts = value.split(`; ${name}=`);
						if (parts.length === 2) return parts.pop().split(';').shift();
						return "";
					};
					const bpmcsrf = getCookie("BPMCSRF");

					// Fetch UsrReportesPampa metadata to get UsrCode
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
						// Call our wrapper service
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

							console.log("Download URL:", downloadUrl);

							// METHOD 1: Use hidden iframe for download (bypasses CSP restrictions that can break object-URL downloads)
							// This is more reliable in restricted environments
							try {
								const iframe = document.createElement("iframe");
								iframe.style.display = "none";
								iframe.src = downloadUrl;
								document.body.appendChild(iframe);

								// Clean up iframe after 2 minutes
								setTimeout(function() {
									if (iframe.parentNode) {
										document.body.removeChild(iframe);
									}
								}, 120000);

								Terrasoft.showInformation("Report download started. Check your downloads folder.");
							} catch (iframeError) {
								console.error("Iframe download failed:", iframeError);

								// METHOD 2: Fallback - try window.open
								try {
									window.open(downloadUrl, "_blank");
									Terrasoft.showInformation("Report opened in new tab.");
								} catch (windowError) {
									console.error("Window.open failed:", windowError);
									Terrasoft.showErrorMessage("Could not download report. URL: " + downloadUrl);
								}
							}
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
