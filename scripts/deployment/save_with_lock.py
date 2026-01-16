#!/usr/bin/env python3
import os
import requests
import json

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
    
    # Try GetSchema to open it
    print("\n1. Getting schema...")
    get_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchema"
    response = session.post(get_url, json={"schemaUId": schema_uid}, headers=headers, timeout=30)
    get_result = response.json()
    print(f"GetSchema success: {get_result.get('success')}")
    
    if get_result.get("success"):
        package_uid = get_result.get("packageUId")
        print(f"Package UId: {package_uid}")
        
        # Try SetSchemaBody
        print("\n2. Setting schema body...")
        set_body_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SetSchemaBody"
        response = session.post(set_body_url, json={
            "schemaUId": schema_uid,
            "body": SERVICE_CODE
        }, headers=headers, timeout=30)
        print(f"SetSchemaBody: {response.status_code}")
        print(f"Result: {response.text[:500]}")
        
        # Try UpdateSchema
        print("\n3. Trying UpdateSchema...")
        update_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/UpdateSchema"
        response = session.post(update_url, json={
            "schemaUId": schema_uid,
            "body": SERVICE_CODE
        }, headers=headers, timeout=30)
        print(f"UpdateSchema: {response.status_code}")
        print(f"Result: {response.text[:500]}")
        
        # Try SaveSchema with IsNew=false
        print("\n4. Trying SaveSchema with isNew=false...")
        save_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"
        response = session.post(save_url, json={
            "schemaUId": schema_uid,
            "packageUId": package_uid,
            "name": "UsrExcelReportService",
            "body": SERVICE_CODE,
            "isNew": False
        }, headers=headers, timeout=30)
        print(f"SaveSchema: {response.status_code}")
        print(f"Result: {response.text[:500]}")

if __name__ == "__main__":
    main()
