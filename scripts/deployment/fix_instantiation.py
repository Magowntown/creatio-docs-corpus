#!/usr/bin/env python3
"""
Fix UsrExcelReportService - proper ReportUtilities instantiation
The issue: FormatterServices.GetUninitializedObject() doesn't call constructors,
leaving internal fields null and causing NullReferenceException.
Solution: Check if method is static, if not, use proper constructor with UserConnection.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Fixed code with proper instance handling
NEW_CODE = '''using System;
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

                // Search for ReportUtilities class in IntExcelExport namespace
                Type utilitiesType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies()) {
                    utilitiesType = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                    if (utilitiesType != null) break;
                }

                if (utilitiesType == null) {
                    return new UsrExcelReportResponse {
                        success = false,
                        message = "ReportUtilities not found"
                    };
                }

                // Get Generate method - it takes 1 parameter (IntExcelReportServiceRequest)
                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod == null) {
                    return new UsrExcelReportResponse {
                        success = false,
                        message = "Generate method not found"
                    };
                }

                var parameters = generateMethod.GetParameters();
                if (parameters.Length != 1) {
                    return new UsrExcelReportResponse {
                        success = false,
                        message = "Generate method has unexpected signature: " + parameters.Length + " params"
                    };
                }

                // Get request type from first parameter
                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                // Set properties using reflection - map our request to their request type
                var reportIdProp = requestType.GetProperty("reportId");
                var filtersConfigProp = requestType.GetProperty("filtersConfig");

                if (reportIdProp != null) reportIdProp.SetValue(serviceRequest, request.ReportId);
                if (filtersConfigProp != null) {
                    // Build filtersConfig object that matches expected format
                    var filtersConfigType = filtersConfigProp.PropertyType;
                    var filtersConfig = FormatterServices.GetUninitializedObject(filtersConfigType);

                    // Set reportId inside filtersConfig if it has that property
                    var fcReportIdProp = filtersConfigType.GetProperty("reportId");
                    if (fcReportIdProp != null) fcReportIdProp.SetValue(filtersConfig, request.ReportId);

                    filtersConfigProp.SetValue(serviceRequest, filtersConfig);
                }

                // Create proper instance for method invocation
                object target = null;
                if (!generateMethod.IsStatic) {
                    // Try constructor with UserConnection parameter first
                    var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
                    if (ctor != null) {
                        target = ctor.Invoke(new object[] { userConnection });
                    } else {
                        // Try parameterless constructor
                        try {
                            target = Activator.CreateInstance(utilitiesType);
                        } catch {
                            // Last resort - uninitialized object (may fail if fields are needed)
                            target = FormatterServices.GetUninitializedObject(utilitiesType);
                        }
                    }
                }

                // Call Generate method
                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

                var resultType = result.GetType();
                return new UsrExcelReportResponse {
                    success = (bool)resultType.GetProperty("success").GetValue(result),
                    key = resultType.GetProperty("key")?.GetValue(result)?.ToString(),
                    message = resultType.GetProperty("message")?.GetValue(result)?.ToString(),
                    reportName = resultType.GetProperty("reportName")?.GetValue(result)?.ToString()
                };
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

    # First get the existing schema data - try multiple endpoint formats
    print("\n=== Getting existing schema ===")
    endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/GetSchemaData",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchemaData",
        "/0/rest/SourceCodeDesignerService/GetSchemaData",
    ]

    schema_data = None
    for endpoint in endpoints:
        get_url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying: {endpoint}")
        response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            try:
                schema_data = response.json()
                if "body" in schema_data or "Body" in schema_data:
                    print(f"  Found schema with keys: {list(schema_data.keys())}")
                    break
            except:
                pass

    if schema_data is None:
        print("Could not get schema from any endpoint")
        return False

    # Update the body with fixed code
    schema_data["body"] = NEW_CODE

    # Save using the full schema data - try multiple endpoint formats
    print("\n=== Saving fixed code ===")
    save_endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/SaveSchema",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema",
        "/0/rest/SourceCodeDesignerService/SaveSchema",
    ]

    for endpoint in save_endpoints:
        save_url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying save: {endpoint}")
        response = session.post(save_url, json=schema_data, headers=headers, timeout=60)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            try:
                result = response.json()
                print(f"  Result: {json.dumps(result, indent=2)[:500]}")

                if result.get("success") != False:
                    print("\n>>> Schema saved successfully!")
                    return True
                else:
                    print(f"  Save failed: {result}")
            except Exception as e:
                print(f"  Parse error: {e}")

    print("Could not save schema via any endpoint")
    return False

if __name__ == "__main__":
    main()
