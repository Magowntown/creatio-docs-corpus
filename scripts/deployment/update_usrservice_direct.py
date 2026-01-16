#!/usr/bin/env python3
"""
Update UsrExcelReportService to use direct call like original service
"""

import os
import requests
import json
import uuid

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Try direct call like the original service
SERVICE_CODE = '''using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using Terrasoft.Web.Common;
using Terrasoft.Core;
using System.Web;

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

    [ServiceContract]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
    public class UsrExcelReportService : BaseService
    {
        private UserConnection _userConnection;
        private UserConnection UserConnection {
            get {
                return _userConnection ?? (_userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"]);
            }
        }

        /// <summary>
        /// Generate report - direct call to IntExcelExport like original service
        /// </summary>
        [OperationContract]
        [WebInvoke(Method = "POST", UriTemplate = "Generate",
            RequestFormat = WebMessageFormat.Json,
            ResponseFormat = WebMessageFormat.Json,
            BodyStyle = WebMessageBodyStyle.Bare)]
        public IntExcelExport.Models.IntExcelReportServiceResponse Generate(UsrExcelReportRequest request) {
            try {
                // Same approach as BGIntExcelReportService2 - direct call
                var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
                    EsqString = request.EsqString,
                    ReportId = request.ReportId,
                    RecordCollection = request.RecordCollection ?? new List<Guid>()
                };
                return IntExcelExport.Utilities.ReportUtilities.Generate(serviceRequest, UserConnection);
            } catch (Exception ex) {
                return new IntExcelExport.Models.IntExcelReportServiceResponse {
                    success = false,
                    message = $"Error: {ex.Message} | ReportId received: {request.ReportId}",
                    errorInfo = new IntExcelExport.Models.IntExcelReportErrorInfo {
                        errorCode = "Exception",
                        message = ex.Message,
                        stackTrace = ex.StackTrace
                    }
                };
            }
        }
    }
}
'''

def login(session):
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def save_schema(session, code):
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Use the SchemaDesignerService
    url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"

    # We need to find the existing schema UID first
    check_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "SysSchema",
        "OperationType": 0,
        "Columns": {
            "Items": {
                "UId": {"Expression": {"ColumnPath": "UId"}},
                "Name": {"Expression": {"ColumnPath": "Name"}}
            }
        },
        "Filters": {
            "FilterType": 1,
            "Items": {
                "NameFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ColumnPath": "Name"},
                    "RightExpression": {"ParameterValue": "UsrExcelReportService", "Type": 0}
                }
            }
        }
    }

    response = session.post(check_url, json=query, headers=headers)
    existing_uid = None
    if response.status_code == 200:
        data = response.json()
        if data.get("rows") and len(data["rows"]) > 0:
            existing_uid = data["rows"][0]["UId"]
            print(f"Found existing schema UID: {existing_uid}")

    schema_uid = existing_uid or str(uuid.uuid4())
    package_uid = "772f974a-21dc-417b-93a2-aac5272e8c39"  # UsrTestApp

    payload = {
        "schemaUId": schema_uid,
        "packageUId": package_uid,
        "name": "UsrExcelReportService",
        "body": code
    }

    print(f"Saving schema with UID: {schema_uid}")
    response = session.post(url, json=payload, headers=headers)
    print(f"SaveSchema response: {response.status_code}")

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        except:
            print(f"Response: {response.text[:500]}")
    else:
        print(f"Error: {response.text[:500]}")
    return False

def compile_schema(session):
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    response = session.post(url, json={}, headers=headers)
    print(f"Build response: {response.status_code}")
    if response.status_code == 200:
        try:
            result = response.json()
            print(f"Build result: {json.dumps(result, indent=2)}")
            return result.get("success", False)
        except:
            print(f"Build result: {response.text[:500]}")
    return False

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")

    print("\nSaving direct-call version of UsrExcelReportService...")
    if save_schema(session, SERVICE_CODE):
        print("\nCompiling...")
        if compile_schema(session):
            print("\n✅ Schema compiled successfully!")
        else:
            print("\n⚠️ Compilation may have issues")

if __name__ == "__main__":
    main()
