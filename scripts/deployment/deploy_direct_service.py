#!/usr/bin/env python3
"""
Deploy UsrExcelReportService with direct call to IntExcelExport (no reflection)
"""

import os
import requests
import json
import time

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Direct call approach - SAME as original IntExcelReportService
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
    /// <summary>
    /// Request with proper DataContract for JSON deserialization
    /// </summary>
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
        /// Generate report - DIRECT call like original IntExcelReportService
        /// The key fix: [DataContract]/[DataMember] ensures ReportId deserializes correctly
        /// </summary>
        [OperationContract]
        [WebInvoke(Method = "POST", UriTemplate = "Generate",
            RequestFormat = WebMessageFormat.Json,
            ResponseFormat = WebMessageFormat.Json,
            BodyStyle = WebMessageBodyStyle.Bare)]
        public IntExcelExport.Models.IntExcelReportServiceResponse Generate(UsrExcelReportRequest request) {
            try {
                // Create request object for internal API - EXACTLY like original service
                var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
                    EsqString = request.EsqString,
                    ReportId = request.ReportId,
                    RecordCollection = request.RecordCollection ?? new List<Guid>()
                };
                
                // Call with UserConnection - SAME as original IntExcelReportService.Generate
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

def save_schema(session, code):
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"
    package_uid = "772f974a-21dc-417b-93a2-aac5272e8c39"  # UsrTestApp
    schema_uid = "721e70eb-4e9c-4364-87a8-4eda367e5d05"   # Existing schema

    payload = {
        "schemaUId": schema_uid,
        "packageUId": package_uid,
        "name": "UsrExcelReportService",
        "body": code
    }

    print("Saving schema...")
    response = session.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("✅ Schema saved successfully")
            return True
        else:
            print(f"❌ Save failed: {result.get('errorInfo', {}).get('message', 'Unknown')}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return False

def compile_workspace(session):
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    
    print("Compiling workspace...")
    response = session.post(url, json={}, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("✅ Compilation successful")
            return True
        else:
            error = result.get("errorInfo", {}).get("message", "Unknown")
            if "another compilation" in error.lower():
                print("⏳ Another compilation in progress, waiting...")
                time.sleep(30)
                return compile_workspace(session)
            print(f"❌ Compilation failed: {error}")
    return False

def test_service(session, bpmcsrf):
    print("\nTesting UsrExcelReportService...")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }

    response = session.post(url, json=data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })

    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)[:600]}")
        if result.get("success"):
            print("\n✅ SUCCESS! Report generated!")
            return True
    else:
        print(f"HTTP Error: {response.status_code}")
    return False

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")
    bpmcsrf = session.cookies.get("BPMCSRF", "")

    if save_schema(session, SERVICE_CODE):
        if compile_workspace(session):
            print("\n" + "="*50)
            test_service(session, bpmcsrf)

if __name__ == "__main__":
    main()
