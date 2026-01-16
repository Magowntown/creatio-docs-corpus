#!/usr/bin/env python3
"""
Fix UsrExcelReportService - brute force approach: set ALL Guid properties to ReportId
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Brute force: set ALL Guid properties to ReportId
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

                // Search for ReportUtilities class
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

                // Get request type
                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                // BRUTE FORCE: Set ALL Guid properties to ReportId
                var guidProps = new List<string>();
                foreach (var prop in requestType.GetProperties()) {
                    if (prop.PropertyType == typeof(Guid) && prop.CanWrite) {
                        prop.SetValue(serviceRequest, request.ReportId);
                        guidProps.Add(prop.Name);
                    }
                }

                // Also try nested filtersConfig object
                var filtersConfigProp = requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null) {
                    var filtersConfigType = filtersConfigProp.PropertyType;
                    var filtersConfig = FormatterServices.GetUninitializedObject(filtersConfigType);

                    // Set ALL Guid properties in filtersConfig too
                    foreach (var prop in filtersConfigType.GetProperties()) {
                        if (prop.PropertyType == typeof(Guid) && prop.CanWrite) {
                            prop.SetValue(filtersConfig, request.ReportId);
                            guidProps.Add("filtersConfig." + prop.Name);
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
                        try {
                            target = Activator.CreateInstance(utilitiesType);
                        } catch {
                            target = FormatterServices.GetUninitializedObject(utilitiesType);
                        }
                    }
                }

                // Call Generate
                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

                var resultType = result.GetType();
                var response = new UsrExcelReportResponse {
                    success = (bool)resultType.GetProperty("success").GetValue(result),
                    key = resultType.GetProperty("key")?.GetValue(result)?.ToString(),
                    message = resultType.GetProperty("message")?.GetValue(result)?.ToString(),
                    reportName = resultType.GetProperty("reportName")?.GetValue(result)?.ToString()
                };

                // Append which Guid props we set for debugging
                if (!response.success) {
                    response.message += " | GuidProps set: " + string.Join(", ", guidProps);
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

    # Get existing schema data - try multiple endpoints
    print("\n=== Getting existing schema ===")
    get_endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/GetSchemaData",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchemaData",
        "/0/rest/SourceCodeDesignerService/GetSchemaData",
    ]

    schema_data = None
    for endpoint in get_endpoints:
        get_url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying: {endpoint}")
        response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                if "body" in data or "Body" in data:
                    schema_data = data
                    print(f"  Got schema with keys: {list(data.keys())}")
                    break
            except:
                print(f"  Not JSON")

    if schema_data is None:
        print("Could not get schema from any endpoint")
        return False

    print(f"Schema keys: {list(schema_data.keys())}")

    # Update the body
    schema_data["body"] = NEW_CODE

    # Save - try multiple endpoints
    print("\n=== Saving brute-force code ===")
    save_endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/SaveSchema",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema",
    ]

    for save_endpoint in save_endpoints:
        save_url = f"{CREATIO_URL}{save_endpoint}"
        print(f"Trying save: {save_endpoint}")
        response = session.post(save_url, json=schema_data, headers=headers, timeout=120)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            try:
                result = response.json()
                print(f"  Result: {json.dumps(result, indent=2)[:300]}")

                if result.get("success") != False:
                    print("\n>>> Schema saved!")
                    trigger_compile(session, headers)
                    return True
                else:
                    print(f"  Save failed: {result}")
            except Exception as e:
                print(f"  Parse error: {e}")

    print("Could not save via any endpoint")

def trigger_compile(session, headers):
    """Trigger compilation"""
    import time
    print("\n=== Triggering compilation ===")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        print(f"Build attempt {attempt+1}...")
        response = session.post(build_url, json={}, headers=headers, timeout=300)

        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            time.sleep(10)
            continue

        build_result = response.json()

        if build_result.get("success"):
            print(">>> Compilation successful!")
            test_service(session, headers)
            break
        else:
            error = build_result.get("errorInfo", {}).get("message", str(build_result))
            if "another compilation" in error.lower():
                print(f"Waiting for other compilation... ({attempt+1})")
                time.sleep(30)
            else:
                print(f"Compilation error: {error[:300]}")
                break

def test_service(session, headers):
    """Test the service"""
    print("\n=== Testing UsrExcelReportService ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }

    response = session.post(url, json=data, headers=headers, timeout=60)
    print(f"Test status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")

        if result.get("success"):
            print("\n>>> SUCCESS! Report generated!")
        else:
            print(f"\nService returned: {result.get('message', '')}")

if __name__ == "__main__":
    main()
