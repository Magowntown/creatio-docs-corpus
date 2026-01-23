/**
 * UsrPage_ebkv9e8 - DIAGNOSTIC Version (v10d)
 * Package: BGApp_eykaguu
 *
 * PURPOSE: Verify schema is loading AT ALL
 * If you see "[v10-DIAG]" in console, the schema loaded successfully.
 * Then we know the issue is elsewhere.
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    // IMMEDIATE console log - proves the module loaded
    console.log("[v10-DIAG] ========== SCHEMA LOADED ==========");
    console.log("[v10-DIAG] Time:", new Date().toISOString());

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // MINIMAL: Just hide iframe (known working from parent)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // INIT: Minimal diagnostic
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    console.log("[v10-DIAG] HandleViewModelInitRequest FIRED");
                    console.log("[v10-DIAG] Context exists:", !!request.$context);
                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
