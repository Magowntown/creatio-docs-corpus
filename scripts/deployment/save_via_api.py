#!/usr/bin/env python3
"""
Save UsrExcelReportService code via the correct Creatio API endpoint
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

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

                // Get Generate method and discover its request type from parameters
                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod == null) {
                    return new UsrExcelReportResponse {
                        success = false,
                        message = "Generate method not found"
                    };
                }

                var parameters = generateMethod.GetParameters();
                if (parameters.Length < 2) {
                    return new UsrExcelReportResponse {
                        success = false,
                        message = "Generate method has unexpected signature: " + parameters.Length + " params"
                    };
                }

                // Get request type from first parameter
                var requestType = parameters[0].ParameterType;

                // Create request object using discovered type
                var serviceRequest = Activator.CreateInstance(requestType);

                // Set properties using reflection
                var esqProp = requestType.GetProperty("EsqString");
                var reportIdProp = requestType.GetProperty("ReportId");
                var recordCollProp = requestType.GetProperty("RecordCollection");

                if (esqProp != null) esqProp.SetValue(serviceRequest, request.EsqString);
                if (reportIdProp != null) reportIdProp.SetValue(serviceRequest, request.ReportId);
                if (recordCollProp != null) recordCollProp.SetValue(serviceRequest, request.RecordCollection ?? new List<Guid>());

                // Call Generate method
                var result = generateMethod.Invoke(null, new object[] { serviceRequest, userConnection });

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
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # First get the existing schema data
    print("\n=== Getting existing schema ===")
    get_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchemaData"
    response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
    print(f"GetSchemaData: {response.status_code}")

    if response.status_code == 200:
        schema_data = response.json()
        print(f"Schema keys: {list(schema_data.keys())}")

        # Update the body
        schema_data["body"] = NEW_CODE

        # Save using the full schema data
        print("\n=== Saving via SourceCodeSchemaDesignerService ===")
        save_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"

        response = session.post(save_url, json=schema_data, headers=headers, timeout=120)
        print(f"SaveSchema: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Result: {json.dumps(result, indent=2)[:500]}")

            if result.get("success") != False:
                print("✅ Schema saved!")
                trigger_compile(session, headers)
            else:
                print(f"❌ Save failed: {result}")
        else:
            print(f"Error: {response.text[:500]}")
    else:
        print(f"Error getting schema: {response.text[:300]}")

def trigger_compile(session, headers):
    """Trigger compilation"""
    import time
    print("\n=== Triggering compilation ===")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        response = session.post(build_url, json={}, headers=headers, timeout=300)
        build_result = response.json()

        if build_result.get("success"):
            print("✅ Compilation successful!")
            test_service(session, headers)
            break
        else:
            error = build_result.get("errorInfo", {}).get("message", str(build_result))
            if "another compilation" in error.lower():
                print(f"⏳ Waiting for other compilation... ({attempt+1})")
                time.sleep(30)
            else:
                print(f"❌ Compilation: {error[:200]}")
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
            print("\n✅ SUCCESS! Report generated!")
        else:
            print(f"\n❌ Service returned error: {result.get('message', '')[:200]}")

if __name__ == "__main__":
    main()
