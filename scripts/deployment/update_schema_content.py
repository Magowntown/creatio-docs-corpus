#!/usr/bin/env python3
"""
Update schema content via DataService UpdateQuery
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Direct call version (no reflection!)
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
                // DIRECT CALL - same as original IntExcelReportService
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
                        errorCode = inner != null ? "InnerException" : "Exception",
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
    
    # Try UpdateQuery to update the Content
    print(f"\n=== Updating schema content (Id: {content_id}) ===")
    
    update_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
    update_query = {
        "RootSchemaName": "SysSchemaContent",
        "OperationType": 1,  # Update
        "ColumnValues": {
            "Items": {
                "Content": {
                    "ExpressionType": 2,
                    "Parameter": {
                        "DataValueType": 1,
                        "Value": NEW_CODE
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
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("\n✅ Content updated! Now need to compile...")
            
            # Trigger compile
            import time
            build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
            
            for attempt in range(5):
                time.sleep(5)
                response = session.post(build_url, json={}, headers=headers, timeout=120)
                result = response.json()
                
                if result.get("success"):
                    print("✅ Compilation successful!")
                    
                    # Test the service
                    print("\nTesting updated service...")
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
                        print(f"Result: {json.dumps(result, indent=2)}")
                    break
                else:
                    error = result.get("errorInfo", {}).get("message", "")
                    if "another compilation" in error.lower():
                        print(f"⏳ Waiting... (attempt {attempt+1})")
                        time.sleep(15)
                    else:
                        print(f"❌ Compilation: {error}")
                        if result.get("errors"):
                            for e in result["errors"][:10]:
                                print(f"  {e}")
                        break

if __name__ == "__main__":
    main()
