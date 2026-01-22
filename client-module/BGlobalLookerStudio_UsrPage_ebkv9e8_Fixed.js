define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[
  "@creatio-devkit/common",
  "UsrIframe",
 ]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/ (sdk,UsrIframe
) /**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            {
                "operation": "insert",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)"
                    ],
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
            {
                "operation": "insert",
                "name": "ComboBox_bo00lsk",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "$Resources.Strings.LookupAttribute_0as4io2",
                    "ariaLabel": "#ResourceString(ComboBox_bo00lsk_ariaLabel)#",
                    "isAddAllowed": true,
                    "showValueAsLink": true,
                    "labelPosition": "auto",
                    "controlActions": [],
                    "listActions": [],
                    "tooltip": "",
                    "readonly": false,
                    "control": "$LookupAttribute_0as4io2",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "placeholder": ""
                },
                "parentName": "GridContainer_oshnwh8",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "GridContainer_xdy25v1",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)"
                    ],
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
                "index": 1
            },
            {
                "operation": "insert",
                "name": "CreatedFrom",
                "values": {
                    "control": "$CreatedFrom",
                    "type": "crt.DateTimePicker",
                    "pickerType": "date",
                    "label": "#ResourceString(CreatedFrom_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "CreatedTo",
                "values": {
                    "control": "$CreatedTo",
                    "type": "crt.DateTimePicker",
                    "pickerType": "date",
                    "label": "#ResourceString(CreatedTo_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 2,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 1
            },
            {
                "operation": "insert",
                "name": "ShippingFrom",
                "values": {
                    "type": "crt.DateTimePicker",
                    "control": "$ShippingFrom",
                    "pickerType": "date",
                    "label": "#ResourceString(DateTimePicker_d37b7ga_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 1,
                        "colSpan": 1,
                        "rowSpan": 1,
                        "row": 2
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 2
            },
            {
                "operation": "insert",
                "name": "ShippingTo",
                "values": {
                    "type": "crt.DateTimePicker",
                    "control": "$ShippingTo",
                    "pickerType": "date",
                    "label": "#ResourceString(DateTimePicker_jdmn1nz_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 2,
                        "colSpan": 1,
                        "rowSpan": 1,
                        "row": 2
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 3
            },
            {
                "operation": "insert",
                "name": "DeliveryFrom",
                "values": {
                    "type": "crt.DateTimePicker",
                    "control": "$DeliveryFrom",
                    "pickerType": "date",
                    "label": "#ResourceString(DeliveryFrom_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 1,
                        "colSpan": 1,
                        "rowSpan": 1,
                        "row": 3
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 4
            },
            {
                "operation": "insert",
                "name": "DeliveryTo",
                "values": {
                    "type": "crt.DateTimePicker",
                    "control": "$DeliveryTo",
                    "pickerType": "date",
                    "label": "#ResourceString(DeliveryTo_label)#",
                    "placeholder": "",
                    "readonly": false,
                    "labelPosition": "auto",
                    "tooltip": "",
                    "visible": true,
                    "layoutConfig": {
                        "column": 2,
                        "colSpan": 1,
                        "rowSpan": 1,
                        "row": 3
                    }
                },
                "parentName": "GridContainer_xdy25v1",
                "propertyName": "items",
                "index": 5
            },
            {
                "operation": "insert",
                "name": "GridContainer_knkow5v",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)"
                    ],
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
            {
                "operation": "insert",
                "name": "ComboBox_8w0dlcf",
                "values": {
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "type": "crt.ComboBox",
                    "label": "$Resources.Strings.LookupAttribute_tytkx09",
                    "ariaLabel": "#ResourceString(ComboBox_8w0dlcf_ariaLabel)#",
                    "isAddAllowed": true,
                    "showValueAsLink": true,
                    "labelPosition": "auto",
                    "controlActions": [],
                    "listActions": [],
                    "tooltip": "",
                    "visible": true,
                    "placeholder": "",
                    "readonly": false,
                    "control": "$LookupAttribute_tytkx09"
                },
                "parentName": "GridContainer_knkow5v",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "GridContainer_1yo7dlx",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)"
                    ],
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
                "index": 3
            },
            {
                "operation": "insert",
                "name": "Button_vae0g6x",
                "values": {
                    "type": "crt.Button",
                    "caption": "#ResourceString(Button_vae0g6x_caption)#",
                    "color": "primary",
                    "disabled": false,
                    "size": "large",
                    "iconPosition": "right-icon",
                    "visible": true,
                    "icon": "process-button-icon",
                    "clicked": {
                        "request": "OpenReport",
                        "params": {}
                    },
                    "clickMode": "default",
                    "layoutConfig": {
                        "column": 2,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    }
                },
                "parentName": "GridContainer_1yo7dlx",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "ReportIView",
                "values": {
                    "layoutConfig": {
                        "column": 3,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "type": "crt.Button",
                    "caption": "#ResourceString(ReportIView_caption)#",
                    "color": "default",
                    "disabled": false,
                    "size": "large",
                    "iconPosition": "left-icon",
                    "visible": false,
                    "icon": "webhooks-integration-button-icon",
                    "clicked": {
                        "request": "OpenReportIview",
                        "params": {}
                    },
                    "clickMode": "default"
                },
                "parentName": "GridContainer_1yo7dlx",
                "propertyName": "items",
                "index": 1
            },
            {
                "operation": "insert",
                "name": "GridContainer_fh039aq",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)"
                    ],
                    "rows": "minmax(max-content, 32px)",
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "padding": {
                        "top": "medium",
                        "right": "large",
                        "bottom": "medium",
                        "left": "large"
                    },
                    "color": "primary",
                    "borderRadius": "medium",
                    "visible": true
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 4
            },
            {
                "operation": "insert",
                "name": "UsrIframe",
                "values": {
                    "control": "$iframe",
                    "type": "usr.CustomViewElement",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 3,
                        "rowSpan": 31
                    }
                },
                "parentName": "GridContainer_fh039aq",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfig: /**SCHEMA_VIEW_MODEL_CONFIG*/{
            "attributes": {
                "DataGrid_zgugl4y": {
                    "isCollection": true,
                    "modelConfig": {
                        "path": "DataGrid_zgugl4yDS"
                    },
                    "viewModelConfig": {
                        "attributes": {
                            "DataGrid_zgugl4yDS_UsrUrl": {
                                "modelConfig": {
                                    "path": "DataGrid_zgugl4yDS.UsrUrl"
                                }
                            },
                            "DataGrid_zgugl4yDS_Id": {
                                "modelConfig": {
                                    "path": "DataGrid_zgugl4yDS.Id"
                                }
                            }
                        }
                    }
                },
                "LookupAttribute_0as4io2": {
                    "modelConfig": {
                        "path": "UsrEntity_e7ac661DS.UsrReporte"
                    }
                },
                "CreatedFrom": {},
                "iframe": {},
                "CreatedTo": {},
                "DeliveryTo": {
                    "modelConfig": {}
                },
                "DeliveryFrom": {
                    "modelConfig": {}
                },
                "ShippingFrom": {
                    "modelConfig": {}
                },
                "ShippingTo": {
                    "modelConfig": {}
                },
                "UsrURL": {},
                "LookupAttribute_tytkx09": {
                    "modelConfig": {
                        "path": "UsrEntity_e7ac661DS.UsrStatusOrder"
                    }
                }
            }
        }/**SCHEMA_VIEW_MODEL_CONFIG*/,
        modelConfig: /**SCHEMA_MODEL_CONFIG*/{
            "dataSources": {
                "DataGrid_zgugl4yDS": {
                    "type": "crt.EntityDataSource",
                    "scope": "viewElement",
                    "config": {
                        "entitySchemaName": "UsrEntity_e7ac661",
                        "attributes": {
                            "UsrUrl": {
                                "path": "UsrUrl"
                            }
                        }
                    }
                },
                "UsrEntity_e7ac661DS": {
                    "type": "crt.EntityDataSource",
                    "scope": "page",
                    "config": {
                        "entitySchemaName": "UsrEntity_e7ac661"
                    }
                }
            },
            "primaryDataSourceName": "UsrEntity_e7ac661DS"
        }/**SCHEMA_MODEL_CONFIG*/,
        handlers: /**SCHEMA_HANDLERS*/ [
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        var lookupVal = await request.$context.LookupAttribute_0as4io2;
                        const model = await sdk.Model.create("UsrReportesPampa");
                        const results = await model.load({
                            attributes: ["Id", "Name", "Description", "UsrURL"],
                            parameters: [
                                {
                                    type: sdk.ModelParameterType.PrimaryColumnValue,
                                    value: lookupVal.value,
                                },
                            ],
                        });
                        const UsrURL = results[0].UsrURL;
                        request.$context.UsrURL = UsrURL;
                    }
                    return next?.handle(request);
                },
            },
            {
                request: "OpenReport",
                handler: async (request, next) => {
                    var createdfrom, createdto, shippingfrom, shippingto, deliveryfrom, deliveryto;
                    var BGFrom, BGTo, BGDate;

                    if (request.$context.attributes.CreatedFrom != null)
                        createdfrom =
                            request.$context.attributes.CreatedFrom.getFullYear() + "-" +
                            (request.$context.attributes.CreatedFrom.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.CreatedFrom.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.CreatedTo != null)
                        createdto =
                            request.$context.attributes.CreatedTo.getFullYear() + "-" +
                            (request.$context.attributes.CreatedTo.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.CreatedTo.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.ShippingFrom != null)
                        shippingfrom =
                            request.$context.attributes.ShippingFrom.getFullYear() + "-" +
                            (request.$context.attributes.ShippingFrom.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.ShippingFrom.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.ShippingTo != null)
                        shippingto =
                            request.$context.attributes.ShippingTo.getFullYear() + "-" +
                            (request.$context.attributes.ShippingTo.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.ShippingTo.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.DeliveryFrom != null)
                        deliveryfrom =
                            request.$context.attributes.DeliveryFrom.getFullYear() + "-" +
                            (request.$context.attributes.DeliveryFrom.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.DeliveryFrom.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.DeliveryTo != null)
                        deliveryto =
                            request.$context.attributes.DeliveryTo.getFullYear() + "-" +
                            (request.$context.attributes.DeliveryTo.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.DeliveryTo.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.BGFrom != null)
                        BGFrom =
                            request.$context.attributes.BGFrom.getFullYear() + "-" +
                            (request.$context.attributes.BGFrom.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.BGFrom.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.BGTo != null)
                        BGTo =
                            request.$context.attributes.BGTo.getFullYear() + "-" +
                            (request.$context.attributes.BGTo.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.BGTo.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    if (request.$context.attributes.BGDate != null)
                        BGDate =
                            request.$context.attributes.BGDate.getFullYear() + "-" +
                            (request.$context.attributes.BGDate.getMonth() + 1).toString().padStart(2, "0") + "-" +
                            ("0" + request.$context.attributes.BGDate.getDate()).slice(-2) + "T00:00:00.0-00:00";

                    var Param = '?params=%7B"ds0.additionalFilters":';
                    var addedFirstFilter = false;

                    if (createdfrom) {
                        Param = Param + '"CreatedOn ge ' + createdfrom;
                        addedFirstFilter = true;
                    }
                    if (createdto) {
                        if (addedFirstFilter)
                            Param = Param + " and CreatedOn le " + createdto;
                        else {
                            Param = Param + '"CreatedOn le ' + createdto;
                            addedFirstFilter = true;
                        }
                    }
                    if (shippingfrom) {
                        if (addedFirstFilter)
                            Param = Param + " and BGShipDate ge " + shippingfrom;
                        else {
                            Param = Param + '"BGShipDate ge ' + shippingfrom;
                            addedFirstFilter = true;
                        }
                    }
                    if (shippingto) {
                        if (addedFirstFilter)
                            Param = Param + " and BGShipDate le " + shippingto;
                        else {
                            Param = Param + '"BGShipDate le ' + shippingto;
                            addedFirstFilter = true;
                        }
                    }
                    if (deliveryfrom) {
                        if (addedFirstFilter)
                            Param = Param + " and BGDeliveryDate ge " + deliveryfrom;
                        else {
                            Param = Param + '"BGDeliveryDate ge ' + deliveryfrom;
                            addedFirstFilter = true;
                        }
                    }
                    if (deliveryto) {
                        if (addedFirstFilter)
                            Param = Param + " and BGDeliveryDate le " + deliveryto;
                        else {
                            Param = Param + '"BGDeliveryDate le ' + deliveryto;
                            addedFirstFilter = true;
                        }
                    }
                    if (BGTo) {
                        if (addedFirstFilter)
                            Param = Param + " and BGDate le " + BGTo;
                        else {
                            Param = Param + '"BGDate le ' + BGTo;
                            addedFirstFilter = true;
                        }
                    }
                    if (BGFrom) {
                        if (addedFirstFilter)
                            Param = Param + " and BGDate ge " + BGFrom;
                        else {
                            Param = Param + '"BGDate ge ' + BGFrom;
                            addedFirstFilter = true;
                        }
                    }
                    if (BGDate) {
                        if (addedFirstFilter)
                            Param = Param + " and CreatedOn eq " + BGDate;
                        else {
                            Param = Param + '"CreatedOn eq ' + BGDate;
                            addedFirstFilter = true;
                        }
                    }

                    // Status order filter
                    if (request.$context.attributes.LookupAttribute_tytkx09 != null) {
                        if (request.$context.attributes.LookupAttribute_tytkx09.displayValue != "All") {
                            if (addedFirstFilter)
                                Param = Param + ` and contains(BGStatus, '` +
                                    request.$context.attributes.LookupAttribute_tytkx09.displayValue + `')`;
                            else {
                                Param = Param + '"' + `contains(BGStatus, '` +
                                    request.$context.attributes.LookupAttribute_tytkx09.displayValue + `')`;
                                addedFirstFilter = true;
                            }
                        }
                    }

                    // Theme filter
                    if (request.$context.attributes.LookupAttribute_4ufq0og != null) {
                        if (addedFirstFilter)
                            Param = Param + ` and contains(BGTheme , '` +
                                request.$context.attributes.LookupAttribute_4ufq0og.displayValue + `')`;
                        else {
                            Param = Param + '"' + `contains(BGTheme, '` +
                                request.$context.attributes.LookupAttribute_4ufq0og.displayValue + `')`;
                            addedFirstFilter = true;
                        }
                    }

                    // Sales rep filter
                    if (request.$context.attributes.LookupAttribute_houdnx9 != null) {
                        if (addedFirstFilter)
                            Param = Param + ` and contains(BGSalesRep , '` +
                                request.$context.attributes.LookupAttribute_houdnx9.displayValue + `')`;
                        else {
                            Param = Param + '"' + `contains(BGSalesRep, '` +
                                request.$context.attributes.LookupAttribute_houdnx9.displayValue + `')`;
                            addedFirstFilter = true;
                        }
                    }

                    // Customer type filter
                    if (request.$context.attributes.LookupAttribute_c4ubvuy != null) {
                        if (addedFirstFilter)
                            Param = Param + ` and contains(BGCustomerType , '` +
                                request.$context.attributes.LookupAttribute_c4ubvuy.displayValue + `')`;
                        else {
                            Param = Param + '"' + `contains(BGCustomerType, '` +
                                request.$context.attributes.LookupAttribute_c4ubvuy.displayValue + `')`;
                            addedFirstFilter = true;
                        }
                    }

                    if (addedFirstFilter) Param += '","ds0.top":"1000000"%7D';
                    else Param += '"","ds0.top":"1000000"%7D';

                    window.open(request.$context.attributes.UsrURL + Param);

                    return next?.handle(request);
                },
            },
            {
                request: "OpenReportIview",
                handler: async (request, next) => {
                    return next?.handle(request);
                },
            },
        ] /**SCHEMA_HANDLERS*/,
        converters: /**SCHEMA_CONVERTERS*/ {} /**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/ {} /**SCHEMA_VALIDATORS*/
    };
});
