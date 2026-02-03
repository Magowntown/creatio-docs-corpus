/**
 * DIAGNOSTIC HANDLER
 *
 * PURPOSE: Diagnose what's happening when reports are clicked.
 * This handler logs everything and shows alerts to help debug.
 *
 * DEPLOY THIS TEMPORARILY TO UNDERSTAND THE CURRENT STATE
 *
 * Schema: UsrPage_ebkv9e8
 * Package: BGApp_eykaguu
 * PROD: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{}/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{}/**SCHEMA_MODEL_CONFIG_DIFF*/,
        handlers: /**SCHEMA_HANDLERS*/[
            {
                request: "OpenReport",
                handler: async (request, next) => {
                    console.log("=== DIAGNOSTIC HANDLER START ===");

                    // Log all context attributes
                    console.log("Context attributes:", Object.keys(request.$context.attributes || {}));

                    // Get selected report
                    var selectedReport = null;
                    try {
                        selectedReport = await request.$context.LookupAttribute_0as4io2;
                        console.log("Selected report:", selectedReport);
                    } catch (e) {
                        console.error("Error getting report:", e);
                    }

                    // Get UsrURL
                    var usrUrl = request.$context.attributes?.UsrURL;
                    console.log("UsrURL:", usrUrl);

                    // Show diagnostic alert
                    var diagMsg = "DIAGNOSTIC INFO:\n" +
                        "Report: " + (selectedReport?.displayValue || "N/A") + "\n" +
                        "Report ID: " + (selectedReport?.value || "N/A") + "\n" +
                        "UsrURL: " + (usrUrl || "EMPTY") + "\n" +
                        "Has URL: " + (usrUrl && usrUrl.trim() !== "" ? "YES (Looker)" : "NO (Excel)") + "\n\n" +
                        "What SHOULD happen:\n" +
                        "- Looker reports: Open in new tab\n" +
                        "- Excel reports: Download Excel file\n\n" +
                        "Click OK to let parent handler continue.";

                    alert(diagMsg);

                    console.log("=== DIAGNOSTIC HANDLER END - DELEGATING TO PARENT ===");

                    // Always delegate to parent to see what it does
                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/
    };
});
