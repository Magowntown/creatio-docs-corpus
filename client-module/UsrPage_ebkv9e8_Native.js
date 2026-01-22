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
			// Business rules - handle report selection change (replaces sdk.Model version)
			{
				request: "crt.HandleViewModelAttributeChangeRequest",
				handler: async (request, next) => {
					// Handle the ORIGINAL lookup attribute (LookupAttribute_0as4io2) from BGlobalLookerStudio
					if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
						const lookupVal = await request.$context.LookupAttribute_0as4io2;

						if (lookupVal && lookupVal.value) {
							const getCookie = (name) => {
								const value = `; ${document.cookie}`;
								const parts = value.split(`; ${name}=`);
								if (parts.length === 2) return parts.pop().split(';').shift();
								return "";
							};
							const bpmcsrf = getCookie("BPMCSRF");

							try {
								// Load report metadata using fetch instead of sdk.Model
								const reportMetaUrl = "/0/odata/UsrReportesPampa(" + lookupVal.value + ")?$select=Id,Name,Description,UsrURL";
								const reportMetaResp = await fetch(reportMetaUrl, {
									method: "GET",
									headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
								});

								if (reportMetaResp.ok) {
									const reportMeta = await reportMetaResp.json();
									// Set UsrURL attribute (for Looker Studio reports)
									request.$context.UsrURL = reportMeta.UsrURL || "";
								}
							} catch (e) {
								console.log("[UsrPage_ebkv9e8] Report metadata lookup failed:", e);
							}
						}
					}

					return next?.handle(request);
				}
			},
			// Report generation - uses native IntExcelExport endpoint
			{
				request: "usr.GenerateExcelReportRequest",
				handler: async (request, next) => {
					const context = request.$context;

					// Try both lookup attribute names (BGApp uses bsixu8a, BGlobalLookerStudio uses 0as4io2)
					let selectedReport = await context.LookupAttribute_bsixu8a;
					if (!selectedReport || !selectedReport.value) {
						selectedReport = await context.LookupAttribute_0as4io2;
					}

					if (!selectedReport || !selectedReport.value) {
						Terrasoft.showErrorMessage("Please select a report");
						return next?.handle(request);
					}
					const pampaReportId = selectedReport.value;

					let reportDisplayName = selectedReport.displayValue || "";
					let reportCode = reportDisplayName;

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
						console.log("[UsrPage_ebkv9e8] UsrReportesPampa metadata lookup failed:", e);
					}

					// Resolve to IntExcelReport ID
					let intExcelReportId = null;
					try {
						const odataUrl = "/0/odata/IntExcelReport?$filter=" +
							"(IntName eq '" + reportDisplayName + "'" +
							" or IntName eq 'Rpt " + reportDisplayName + "'" +
							" or IntName eq '" + reportCode + "'" +
							" or IntName eq 'Rpt " + reportCode + "')" +
							"&$select=Id,IntName&$top=1";

						const odataResponse = await fetch(odataUrl, {
							method: "GET",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
						});

						const odataResult = await odataResponse.json();
						if (odataResult.value && odataResult.value.length > 0) {
							intExcelReportId = odataResult.value[0].Id;
							console.log("[UsrPage_ebkv9e8] Found IntExcelReport:", odataResult.value[0].IntName, "->", intExcelReportId);
						} else {
							Terrasoft.showErrorMessage("Excel report template not found for: " + reportDisplayName);
							return next?.handle(request);
						}
					} catch (e) {
						Terrasoft.showErrorMessage("Error finding report template: " + e.message);
						return next?.handle(request);
					}

					// Call NATIVE IntExcelExport endpoint
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
							Terrasoft.showErrorMessage("Failed to generate report: " + (result.message || result.errorMessage || "Unknown error"));
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
