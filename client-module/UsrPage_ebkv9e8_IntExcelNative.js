define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {
	return {
		viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
			{
				"operation": "merge",
				"name": "GridContainer_fh039aq",
				"values": {
					"visible": false
				}
			},
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
		viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
		modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,
		handlers: /**SCHEMA_HANDLERS*/[
			{
				request: "crt.HandleViewModelAttributeChangeRequest",
				handler: async (request, next) => {
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
								const url = "/0/odata/UsrReportesPampa(" + lookupVal.value + ")?$select=Id,Name,Description,UsrURL";
								const resp = await fetch(url, {
									method: "GET",
									headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
								});
								if (resp.ok) {
									const data = await resp.json();
									request.$context.UsrURL = data.UsrURL || "";
								}
							} catch (e) {
								console.log("[UsrPage_ebkv9e8] Metadata lookup failed:", e);
							}
						}
					}
					return next?.handle(request);
				}
			},
			{
				request: "usr.GenerateExcelReportRequest",
				handler: async (request, next) => {
					const context = request.$context;
					const selectedReport = await context.LookupAttribute_0as4io2;

					if (!selectedReport || !selectedReport.value) {
						Terrasoft.showErrorMessage("Please select a report");
						return next?.handle(request);
					}

					let reportName = selectedReport.displayValue || "";
					let reportCode = reportName;

					const getCookie = (name) => {
						const value = `; ${document.cookie}`;
						const parts = value.split(`; ${name}=`);
						if (parts.length === 2) return parts.pop().split(';').shift();
						return "";
					};
					const bpmcsrf = getCookie("BPMCSRF");

					// Get report code from UsrReportesPampa
					try {
						const url = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=Id,Name,UsrCode";
						const resp = await fetch(url, {
							method: "GET",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
						});
						if (resp.ok) {
							const data = await resp.json();
							reportName = data.Name || reportName;
							reportCode = data.UsrCode || reportCode;
						}
					} catch (e) {}

					// Find IntExcelReport by name
					let intExcelReportId = null;
					try {
						const searchUrl = "/0/odata/IntExcelReport?$filter=" +
							"(IntName eq '" + reportName + "'" +
							" or IntName eq 'Rpt " + reportName + "'" +
							" or IntName eq '" + reportCode + "'" +
							" or IntName eq 'Rpt " + reportCode + "')" +
							"&$select=Id,IntName&$top=1";

						const resp = await fetch(searchUrl, {
							method: "GET",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
						});
						const result = await resp.json();

						if (result.value && result.value.length > 0) {
							intExcelReportId = result.value[0].Id;
						} else {
							Terrasoft.showErrorMessage("Report template not found: " + reportName);
							return next?.handle(request);
						}
					} catch (e) {
						Terrasoft.showErrorMessage("Error finding report: " + e.message);
						return next?.handle(request);
					}

					// Call native IntExcelExport service
					try {
						const resp = await fetch("/0/rest/IntExcelReportService/Generate", {
							method: "POST",
							headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
							body: JSON.stringify({
								reportId: intExcelReportId,
								recordId: null,
								recordCollection: []
							})
						});

						const result = await resp.json();

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
							Terrasoft.showErrorMessage("Failed: " + (result.message || result.errorMessage || "Unknown error"));
						}
					} catch (e) {
						Terrasoft.showErrorMessage("Error: " + e.message);
					}

					return next?.handle(request);
				}
			}
		]/**SCHEMA_HANDLERS*/,
		converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
		validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
	};
});
