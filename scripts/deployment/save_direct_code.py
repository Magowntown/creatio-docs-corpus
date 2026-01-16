#!/usr/bin/env python3
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
                    message = $"ReportId: {request.ReportId} | {ex.Message}",
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

def main():
    session = requests.Session()
    
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")
        
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    schema_uid = "ed794ab8-8a59-4c7e-983c-cc039449d178"
    package_uid = "772f974a-21dc-417b-93a2-aac5272e8c39"  # UsrTestApp
    
    # Save schema
    print("\nSaving schema...")
    save_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"
    save_payload = {
        "schemaUId": schema_uid,
        "packageUId": package_uid,
        "name": "UsrExcelReportService",
        "body": SERVICE_CODE
    }
    
    response = session.post(save_url, json=save_payload, headers=headers, timeout=60)
    print(f"SaveSchema: {response.status_code}")
    result = response.json()
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if not result.get("success"):
        print("Save failed!")
        return
    
    # Compile
    print("\nCompiling...")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    
    for attempt in range(5):
        response = session.post(build_url, json={}, headers=headers, timeout=120)
        result = response.json()
        
        if result.get("success"):
            print("✅ Compilation successful!")
            break
        else:
            error = result.get("errorInfo", {}).get("message", "")
            if "another compilation" in error.lower():
                print(f"⏳ Waiting... (attempt {attempt+1})")
                time.sleep(15)
                continue
            print(f"❌ Compilation failed: {error}")
            
            # Check for compile errors
            if result.get("errors"):
                for err in result["errors"][:5]:
                    print(f"  - {err}")
            break
    
    # Test
    print("\n" + "="*50)
    print("Testing service...")
    test_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    
    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }
    
    response = session.post(test_url, json=data, headers=headers, timeout=60)
    print(f"Test status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Test result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
