#!/usr/bin/env python3
"""
Deploy the fixed wrapper service that properly handles GUID deserialization.
Uses SourceCodeSchemaDesigner API to update the code.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Clean, working wrapper service code
WRAPPER_CODE = '''using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.Reflection;
using Terrasoft.Web.Common;
using Terrasoft.Core;

namespace Terrasoft.Configuration
{
    [DataContract]
    public class UsrExcelReportRequest
    {
        [DataMember(Name = "EsqString")]
        public string EsqString { get; set; }

        [DataMember(Name = "ReportId")]
        public Guid ReportId { get; set; }

        [DataMember(Name = "RecordCollection")]
        public List<Guid> RecordCollection { get; set; }
    }

    [DataContract]
    public class UsrExcelReportResponse
    {
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
        public UsrExcelReportResponse Generate(UsrExcelReportRequest request)
        {
            try
            {
                var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                // Find ReportUtilities type
                Type utilitiesType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    utilitiesType = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                    if (utilitiesType != null) break;
                }

                if (utilitiesType == null)
                {
                    return new UsrExcelReportResponse { success = false, message = "ReportUtilities not found" };
                }

                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod == null)
                {
                    return new UsrExcelReportResponse { success = false, message = "Generate method not found" };
                }

                var parameters = generateMethod.GetParameters();
                if (parameters.Length != 1)
                {
                    return new UsrExcelReportResponse { success = false, message = "Generate has " + parameters.Length + " params" };
                }

                // Create IntExcelReportServiceRequest via reflection
                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                // Set ReportId property - this is the key fix!
                var reportIdProp = requestType.GetProperty("ReportId");
                if (reportIdProp != null)
                {
                    reportIdProp.SetValue(serviceRequest, request.ReportId);
                }

                // Set filtersConfig to null or empty
                var filtersConfigProp = requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null)
                {
                    filtersConfigProp.SetValue(serviceRequest, null);
                }

                // Set recordCollection to empty list
                var recordCollectionProp = requestType.GetProperty("recordCollection");
                if (recordCollectionProp != null && request.RecordCollection != null)
                {
                    recordCollectionProp.SetValue(serviceRequest, request.RecordCollection);
                }

                // Create ReportUtilities instance
                object target = null;
                if (!generateMethod.IsStatic)
                {
                    var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
                    if (ctor != null)
                    {
                        target = ctor.Invoke(new object[] { userConnection });
                    }
                    else
                    {
                        target = Activator.CreateInstance(utilitiesType);
                    }
                }

                // Call Generate method
                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

                // Map result to our response
                var resultType = result.GetType();
                var response = new UsrExcelReportResponse
                {
                    success = (bool)resultType.GetProperty("success").GetValue(result),
                    key = resultType.GetProperty("key")?.GetValue(result)?.ToString(),
                    message = resultType.GetProperty("message")?.GetValue(result)?.ToString(),
                    reportName = resultType.GetProperty("reportName")?.GetValue(result)?.ToString()
                };

                return response;
            }
            catch (TargetInvocationException tie)
            {
                var inner = tie.InnerException;
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "ReportId=" + request.ReportId + " | " + (inner != null ? inner.Message : tie.Message)
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "ReportId=" + request.ReportId + " | Error: " + ex.Message
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

    # Get existing schema
    print("\n=== Getting current schema ===")
    get_url = f"{CREATIO_URL}/0/rest/SourceCodeSchemaDesignerService/GetSchemaData"
    response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        return False

    schema_data = response.json()
    print(f"Got schema: {schema_data.get('name', 'N/A')}")

    # Update body
    schema_data["body"] = WRAPPER_CODE

    # Save
    print("\n=== Saving updated code ===")
    save_url = f"{CREATIO_URL}/0/rest/SourceCodeSchemaDesignerService/SaveSchema"
    response = session.post(save_url, json=schema_data, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"Save failed: {response.status_code}")
        print(response.text[:500])
        return False

    result = response.json()
    print(f"Save result: {json.dumps(result, indent=2)[:200]}")

    if result.get("success") == False:
        print(f"Save error: {result}")
        return False

    # Compile
    print("\n=== Compiling ===")
    compile_and_test(session, headers)

def compile_and_test(session, headers):
    import time

    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        print(f"Build attempt {attempt + 1}...")
        try:
            response = session.post(build_url, json={}, headers=headers, timeout=300)

            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                time.sleep(10)
                continue

            result = response.json()

            if result.get("success"):
                print(">>> Compilation successful!")
                time.sleep(3)
                test_wrapper_service(session, headers)
                return True
            else:
                error = result.get("errorInfo", {}).get("message", str(result))
                if "another compilation" in error.lower():
                    print("Waiting for other compilation...")
                    time.sleep(30)
                else:
                    print(f"Compilation error: {error[:500]}")
                    return False
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

    return False

def test_wrapper_service(session, headers):
    print("\n=== Testing UsrExcelReportService ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }

    print(f"Request: {json.dumps(data, indent=2)}")

    response = session.post(url, json=data, headers=headers, timeout=120)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")

        if result.get("success"):
            print("\n>>> SUCCESS!")
            if result.get("key"):
                print(f"Download key: {result.get('key')}")
        else:
            print(f"\nError: {result.get('message', 'Unknown')}")
    else:
        print(f"HTTP Error: {response.text[:500]}")

if __name__ == "__main__":
    main()
