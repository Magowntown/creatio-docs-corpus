#!/usr/bin/env python3
"""
Deploy wrapper service code using all possible endpoints.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Clean wrapper service code
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

                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                var reportIdProp = requestType.GetProperty("ReportId");
                if (reportIdProp != null)
                {
                    reportIdProp.SetValue(serviceRequest, request.ReportId);
                }

                var filtersConfigProp = requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null)
                {
                    filtersConfigProp.SetValue(serviceRequest, null);
                }

                var recordCollectionProp = requestType.GetProperty("recordCollection");
                if (recordCollectionProp != null && request.RecordCollection != null)
                {
                    recordCollectionProp.SetValue(serviceRequest, request.RecordCollection);
                }

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

                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

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

    # Try multiple GET endpoints
    print("\n=== Trying GET endpoints ===")
    get_endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/GetSchemaData",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchemaData",
        "/0/rest/SourceCodeDesignerService/GetSchemaData",
        "/0/ServiceModel/SourceCodeDesignerService.svc/GetSchemaData",
        "/0/rest/SchemaDesignerService/GetSchema",
        "/0/rest/ConfigurationService/GetSchemaMetaData",
    ]

    schema_data = None
    for endpoint in get_endpoints:
        url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying: {endpoint}")

        response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())[:5]}")
                    if "body" in data or "Body" in data or "metaData" in data:
                        schema_data = data
                        print(f"  >>> Found schema data!")
                        break
            except:
                pass

    # Try direct OData to get SysSchema
    print("\n=== Trying OData for SysSchema ===")
    odata_url = f"{CREATIO_URL}/0/odata/SysSchema({SCHEMA_UID})"
    response = session.get(odata_url, headers=headers, timeout=30)
    print(f"OData GET: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Keys: {list(data.keys())}")

        # Check if there's a Body property or similar
        for key in ["Body", "body", "Source", "source", "MetaData", "metaData"]:
            if key in data:
                print(f"Found {key}: {str(data[key])[:100]}...")

    # Try getting via SelectQuery
    print("\n=== Trying DataService SelectQuery ===")
    select_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    select_data = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 6,
            "items": {
                "UId": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "isEnabled": True,
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

    response = session.post(select_url, json=select_data, headers=headers, timeout=30)
    print(f"SelectQuery: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            row = rows[0]
            print(f"Columns: {list(row.keys())}")

    # Let's try SourceCodeEditService
    print("\n=== Trying SourceCodeEditService ===")
    edit_endpoints = [
        "/0/rest/SourceCodeEditService/GetSourceCode",
        "/0/ServiceModel/SourceCodeEditService.svc/GetSourceCode",
    ]

    for endpoint in edit_endpoints:
        url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying: {endpoint}")

        response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {str(data)[:200]}")
            except:
                print(f"  Response: {response.text[:200]}")

if __name__ == "__main__":
    main()
