#!/usr/bin/env python3
"""
Update schema using Configuration API
"""

import os
import requests
import json
import time

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

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

        [OperationContract]
        [WebInvoke(Method = "POST", UriTemplate = "Generate",
            RequestFormat = WebMessageFormat.Json,
            ResponseFormat = WebMessageFormat.Json,
            BodyStyle = WebMessageBodyStyle.Bare)]
        public IntExcelExport.Models.IntExcelReportServiceResponse Generate(UsrExcelReportRequest request) {
            try {
                var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
                    EsqString = request.EsqString,
                    ReportId = request.ReportId,
                    RecordCollection = request.RecordCollection ?? new List<Guid>()
                };
                return IntExcelExport.Utilities.ReportUtilities.Generate(serviceRequest, UserConnection);
            } catch (Exception ex) {
                var inner = ex.InnerException;
                return new IntExcelExport.Models.IntExcelReportServiceResponse {
                    success = false,
                    message = $"Received ReportId: {request.ReportId} | Error: {ex.Message}",
                    errorInfo = new IntExcelExport.Models.IntExcelReportErrorInfo {
                        errorCode = "Exception",
                        message = inner != null ? inner.Message : ex.Message,
                        stackTrace = ex.StackTrace
                    }
                };
            }
        }
    }
}
'''

def login(session):
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def update_schema_content(session):
    """Try to update schema content via SysSchemaContent"""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # First find the schema
    find_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "SysSchema",
        "OperationType": 0,
        "Columns": {"Items": {
            "Id": {"Expression": {"ColumnPath": "Id"}},
            "UId": {"Expression": {"ColumnPath": "UId"}},
            "Name": {"Expression": {"ColumnPath": "Name"}}
        }},
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

    response = session.post(find_url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("rows"):
            schema = data["rows"][0]
            print(f"Found schema: Id={schema.get('Id')}, UId={schema.get('UId')}")
            return schema
    return None

def try_schema_designer(session, schema_uid):
    """Try using the schema designer with GetSchema first"""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Get the schema first
    get_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchema"
    get_response = session.post(get_url, json={"schemaUId": schema_uid}, headers=headers)
    
    print(f"GetSchema response: {get_response.status_code}")
    if get_response.status_code == 200:
        result = get_response.json()
        print(f"GetSchema result: {json.dumps(result, indent=2)[:500]}")
        
        if result.get("success"):
            # Now try to save with the same package
            package_uid = result.get("packageUId") or "772f974a-21dc-417b-93a2-aac5272e8c39"
            
            save_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"
            save_payload = {
                "schemaUId": schema_uid,
                "packageUId": package_uid,
                "name": "UsrExcelReportService",
                "body": SERVICE_CODE
            }
            
            save_response = session.post(save_url, json=save_payload, headers=headers)
            print(f"SaveSchema response: {save_response.status_code}")
            if save_response.status_code == 200:
                save_result = save_response.json()
                print(f"SaveSchema result: {json.dumps(save_result, indent=2)}")
                return save_result.get("success", False)
    
    return False

def compile_all(session):
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    
    print("Compiling...")
    for attempt in range(3):
        response = session.post(url, json={}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Compilation successful")
                return True
            error = result.get("errorInfo", {}).get("message", "")
            if "another compilation" in error.lower():
                print(f"⏳ Waiting for compilation... (attempt {attempt+1})")
                time.sleep(20)
                continue
            print(f"❌ Compilation failed: {error}")
            break
    return False

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")

    schema = update_schema_content(session)
    if schema:
        schema_uid = schema.get("UId")
        if try_schema_designer(session, schema_uid):
            compile_all(session)

if __name__ == "__main__":
    main()
