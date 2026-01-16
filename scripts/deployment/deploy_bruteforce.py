#!/usr/bin/env python3
"""
Deploy brute-force code via direct SQL update
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Brute force code - sets ALL Guid properties
NEW_CODE = r'''using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.Reflection;
using System.Linq;
using Terrasoft.Web.Common;
using Terrasoft.Core;

namespace Terrasoft.Configuration
{
    [DataContract]
    public class UsrExcelReportRequest {
        [DataMember(Name = "EsqString")]
        public string EsqString { get; set; }

        [DataMember(Name = "ReportId")]
        public Guid ReportId { get; set; }

        [DataMember(Name = "RecordCollection")]
        public List<Guid> RecordCollection { get; set; }
    }

    [DataContract]
    public class UsrExcelReportResponse {
        [DataMember(Name = "success")]
        public bool success { get; set; }

        [DataMember(Name = "key")]
        public string key { get; set; }

        [DataMember(Name = "message")]
        public string message { get; set; }

        [DataMember(Name = "reportName")]
        public string reportName { get; set; }
    }

    [ServiceContract]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
    public class UsrExcelReportService : BaseService
    {
        [OperationContract]
        [WebInvoke(Method = "POST", UriTemplate = "Generate",
            RequestFormat = WebMessageFormat.Json,
            ResponseFormat = WebMessageFormat.Json,
            BodyStyle = WebMessageBodyStyle.Bare)]
        public UsrExcelReportResponse Generate(UsrExcelReportRequest request) {
            try {
                var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];
                var guidPropsSet = new List<string>();

                Type utilitiesType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies()) {
                    utilitiesType = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                    if (utilitiesType != null) break;
                }

                if (utilitiesType == null) {
                    return new UsrExcelReportResponse { success = false, message = "ReportUtilities not found" };
                }

                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod == null) {
                    return new UsrExcelReportResponse { success = false, message = "Generate method not found" };
                }

                var parameters = generateMethod.GetParameters();
                if (parameters.Length != 1) {
                    return new UsrExcelReportResponse { success = false, message = "Generate method has " + parameters.Length + " params" };
                }

                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                // BRUTE FORCE: Set ALL Guid properties to ReportId
                foreach (var prop in requestType.GetProperties()) {
                    if (prop.PropertyType == typeof(Guid) && prop.CanWrite) {
                        prop.SetValue(serviceRequest, request.ReportId);
                        guidPropsSet.Add(prop.Name);
                    }
                }

                // Also handle nested filtersConfig
                var filtersConfigProp = requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null) {
                    var fcType = filtersConfigProp.PropertyType;
                    var filtersConfig = FormatterServices.GetUninitializedObject(fcType);
                    foreach (var prop in fcType.GetProperties()) {
                        if (prop.PropertyType == typeof(Guid) && prop.CanWrite) {
                            prop.SetValue(filtersConfig, request.ReportId);
                            guidPropsSet.Add("fc." + prop.Name);
                        }
                    }
                    filtersConfigProp.SetValue(serviceRequest, filtersConfig);
                }

                // Create proper instance
                object target = null;
                if (!generateMethod.IsStatic) {
                    var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
                    if (ctor != null) {
                        target = ctor.Invoke(new object[] { userConnection });
                    } else {
                        target = Activator.CreateInstance(utilitiesType);
                    }
                }

                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

                var resultType = result.GetType();
                var response = new UsrExcelReportResponse {
                    success = (bool)resultType.GetProperty("success").GetValue(result),
                    key = resultType.GetProperty("key")?.GetValue(result)?.ToString(),
                    message = resultType.GetProperty("message")?.GetValue(result)?.ToString(),
                    reportName = resultType.GetProperty("reportName")?.GetValue(result)?.ToString()
                };

                if (!response.success) {
                    response.message += " | Props: " + string.Join(",", guidPropsSet);
                }
                return response;
            } catch (Exception ex) {
                var inner = ex.InnerException;
                return new UsrExcelReportResponse {
                    success = false,
                    message = "ReportId: " + request.ReportId + " | Error: " + (inner != null ? inner.Message : ex.Message)
                };
            }
        }
    }
}
'''

def main():
    session = requests.Session()

    # Login
    print("=== Logging in ===")
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Try SQL update via OData
    print("\n=== Trying OData update ===")
    odata_url = f"{CREATIO_URL}/0/odata/SysSchema({SCHEMA_UID})"

    response = session.patch(odata_url,
        json={"Body": NEW_CODE},
        headers=headers,
        timeout=60
    )
    print(f"OData PATCH: {response.status_code}")
    if response.status_code in [200, 204]:
        print(">>> OData update successful!")
        trigger_compile(session, headers)
        return True
    else:
        print(f"Response: {response.text[:300]}")

    # Try InsertQuery for update
    print("\n=== Trying DataService InsertQuery ===")
    update_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
    update_data = {
        "rootSchemaName": "SysSchema",
        "isDistinct": False,
        "rowCount": -1,
        "columnValues": {
            "items": {
                "Body": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": NEW_CODE
                    }
                }
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "id": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "isEnabled": True,
                    "trimDateTimeParameterToDate": False,
                    "leftExpression": {
                        "expressionType": 0,
                        "columnPath": "UId"
                    },
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {
                            "dataValueType": 0,
                            "value": SCHEMA_UID
                        }
                    }
                }
            }
        }
    }
    response = session.post(update_url, json=update_data, headers=headers, timeout=60)
    print(f"UpdateQuery: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)[:300]}")
        if result.get("success") or result.get("rowsAffected", 0) > 0:
            print(">>> DataService update successful!")
            trigger_compile(session, headers)
            return True

    return False

def trigger_compile(session, headers):
    import time
    print("\n=== Triggering compilation ===")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(3):
        print(f"Build attempt {attempt+1}...")
        try:
            response = session.post(build_url, json={}, headers=headers, timeout=300)
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(">>> Compilation successful!")
                    return True
                else:
                    error = result.get("errorInfo", {}).get("message", str(result))
                    if "another compilation" in error.lower():
                        print("Waiting for other compilation...")
                        time.sleep(30)
                    else:
                        print(f"Compilation error: {error[:200]}")
                        return False
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
    return False

if __name__ == "__main__":
    main()
