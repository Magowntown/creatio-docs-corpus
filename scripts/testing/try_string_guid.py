#!/usr/bin/env python3
"""
Test approach: Use string for ReportId to bypass WCF Guid deserialization bug
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# New approach: ReportId as STRING, not Guid
# We parse it server-side to avoid WCF Guid bug
NEW_SERVICE_CODE = '''using System;
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
    /// Request with ReportId as STRING to bypass WCF Guid deserialization bug
    /// </summary>
    [DataContract]
    public class UsrExcelReportRequest {
        [DataMember(Name = "EsqString")]
        public string EsqString { get; set; }

        // KEY FIX: ReportId as STRING, not Guid
        [DataMember(Name = "ReportId")]
        public string ReportId { get; set; }

        [DataMember(Name = "RecordCollection")]
        public List<string> RecordCollection { get; set; }
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
                // Parse ReportId string to Guid ourselves
                Guid reportGuid;
                if (!Guid.TryParse(request.ReportId, out reportGuid)) {
                    return new IntExcelExport.Models.IntExcelReportServiceResponse {
                        success = false,
                        message = $"Invalid ReportId format: {request.ReportId}"
                    };
                }
                
                // Parse RecordCollection strings to Guids
                var records = new List<Guid>();
                if (request.RecordCollection != null) {
                    foreach (var s in request.RecordCollection) {
                        Guid g;
                        if (Guid.TryParse(s, out g)) {
                            records.Add(g);
                        }
                    }
                }
                
                // Create request for internal API
                var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
                    EsqString = request.EsqString,
                    ReportId = reportGuid,
                    RecordCollection = records
                };
                
                return IntExcelExport.Utilities.ReportUtilities.Generate(serviceRequest, UserConnection);
            } catch (Exception ex) {
                var inner = ex.InnerException;
                return new IntExcelExport.Models.IntExcelReportServiceResponse {
                    success = false,
                    message = $"Error: {ex.Message}",
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
    
    # Create a NEW schema with different name
    print("\nCreating new schema UsrExcelReportService2...")
    
    save_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"
    package_uid = "772f974a-21dc-417b-93a2-aac5272e8c39"
    
    # Generate new UID for new schema
    import uuid
    new_schema_uid = str(uuid.uuid4())
    
    # Update code to use new class names
    code = NEW_SERVICE_CODE.replace("UsrExcelReportRequest", "UsrExcelReportRequest2")
    code = code.replace("UsrExcelReportService", "UsrExcelReportService2")
    
    response = session.post(save_url, json={
        "schemaUId": new_schema_uid,
        "packageUId": package_uid,
        "name": "UsrExcelReportService2",
        "body": code,
        "isNew": True
    }, headers=headers, timeout=60)
    
    print(f"SaveSchema: {response.status_code}")
    result = response.json()
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        print("\n✅ Schema created! Now compiling...")
        
        import time
        build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
        for attempt in range(5):
            response = session.post(build_url, json={}, headers=headers, timeout=120)
            result = response.json()
            if result.get("success"):
                print("✅ Compilation successful!")
                
                # Test the new service
                print("\nTesting UsrExcelReportService2...")
                test_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService2/Generate"
                data = {
                    "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
                    "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",  # Still send as string
                    "RecordCollection": []
                }
                response = session.post(test_url, json=data, headers=headers, timeout=60)
                print(f"Test: {response.status_code}")
                if response.status_code == 200:
                    print(f"Result: {json.dumps(response.json(), indent=2)}")
                break
            else:
                error = result.get("errorInfo", {}).get("message", "")
                if "another compilation" in error.lower():
                    print(f"⏳ Waiting... (attempt {attempt+1})")
                    time.sleep(15)
                else:
                    print(f"❌ {error}")
                    if result.get("errors"):
                        for e in result["errors"][:5]:
                            print(f"  {e}")
                    break

if __name__ == "__main__":
    main()
