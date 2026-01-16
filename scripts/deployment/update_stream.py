#!/usr/bin/env python3
"""
Update schema content with binary stream encoding
"""

import os
import requests
import json
import base64

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

NEW_CODE = '''using System;
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
                        errorCode = inner != null ? "Inner" : "Exception",
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
    
    content_id = "ad87ec24-9520-4178-b0a8-2ea17e47b460"
    
    # Encode code as base64 for binary column
    code_bytes = NEW_CODE.encode('utf-8')
    code_base64 = base64.b64encode(code_bytes).decode('ascii')
    
    print(f"\n=== Updating with base64 encoded content ===")
    print(f"Code length: {len(NEW_CODE)} chars, Base64: {len(code_base64)} chars")
    
    update_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
    update_query = {
        "RootSchemaName": "SysSchemaContent",
        "OperationType": 1,
        "ColumnValues": {
            "Items": {
                "Content": {
                    "ExpressionType": 2,
                    "Parameter": {
                        "DataValueType": 13,  # Binary
                        "Value": code_base64
                    }
                }
            }
        },
        "Filters": {
            "FilterType": 6,
            "Items": {
                "IdFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ExpressionType": 0, "ColumnPath": "Id"},
                    "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 0, "Value": content_id}}
                }
            }
        }
    }
    
    response = session.post(update_url, json=update_query, headers=headers, timeout=60)
    print(f"Update status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        print("\n✅ Content updated!")
        
        # Trigger rebuild
        import time
        print("\nTriggering compilation...")
        build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
        
        for attempt in range(5):
            response = session.post(build_url, json={}, headers=headers, timeout=120)
            build_result = response.json()
            
            if build_result.get("success"):
                print("✅ Compilation successful!")
                
                # Test
                print("\nTesting...")
                test_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
                data = {
                    "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
                    "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
                    "RecordCollection": []
                }
                response = session.post(test_url, json=data, headers=headers, timeout=60)
                print(f"Test: {response.status_code}")
                if response.status_code == 200:
                    print(f"Result: {json.dumps(response.json(), indent=2)}")
                break
            else:
                error = build_result.get("errorInfo", {}).get("message", "")
                if "another compilation" in error.lower():
                    print(f"⏳ Waiting... ({attempt+1})")
                    time.sleep(15)
                else:
                    print(f"❌ {error}")
                    if build_result.get("errors"):
                        for e in build_result["errors"][:5]:
                            print(f"  {e}")
                    break

if __name__ == "__main__":
    main()
