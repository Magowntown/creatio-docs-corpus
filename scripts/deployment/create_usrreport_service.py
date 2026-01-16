#!/usr/bin/env python3
"""
Create a new Source Code schema for UsrExcelReportService via Creatio API
"""

import os
import requests
import json
import uuid

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# The service code with proper DataContract
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
    /// Request class with proper DataContract for JSON deserialization
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
        /// Generate report with proper DataContract deserialization
        /// </summary>
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
                return new IntExcelExport.Models.IntExcelReportServiceResponse {
                    success = false,
                    message = ex.Message,
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
    """Login to Creatio"""
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def get_package_uid(session, package_name):
    """Get the UID of a package by name"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    query = {
        "RootSchemaName": "SysPackage",
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
                    "RightExpression": {"ParameterValue": package_name, "Type": 0}
                }
            }
        }
    }

    response = session.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("rows") and len(data["rows"]) > 0:
            return data["rows"][0]["UId"]
    return None

def check_schema_exists(session, schema_name):
    """Check if a schema with the given name already exists"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

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
                    "RightExpression": {"ParameterValue": schema_name, "Type": 0}
                }
            }
        }
    }

    response = session.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("rows") and len(data["rows"]) > 0:
            return data["rows"][0]["UId"]
    return None

def create_source_code_schema(session, package_uid, schema_name, code):
    """Create a new source code schema"""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Generate a new UID for the schema
    schema_uid = str(uuid.uuid4())

    # Try the SchemaDesignerService approach
    url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/SaveSchema"

    payload = {
        "schemaUId": schema_uid,
        "packageUId": package_uid,
        "name": schema_name,
        "body": code
    }

    print(f"Creating schema with UID: {schema_uid}")
    print(f"In package UID: {package_uid}")

    response = session.post(url, json=payload, headers=headers)
    print(f"SaveSchema response: {response.status_code}")

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return data
        except:
            print(f"Response text: {response.text[:500]}")
    else:
        print(f"Error: {response.text[:500]}")

    return None

def compile_schema(session):
    """Compile all schemas"""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    response = session.post(url, json={}, headers=headers)
    print(f"Build response: {response.status_code}")
    if response.status_code == 200:
        try:
            print(f"Build result: {response.json()}")
        except:
            print(f"Build result: {response.text[:500]}")

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")

    # Use the UsrTestApp package (Customer package)
    package_uid = "772f974a-21dc-417b-93a2-aac5272e8c39"
    print(f"\nUsing UsrTestApp package UID: {package_uid}")

    # Check if schema already exists
    print("\nChecking if UsrExcelReportService already exists...")
    existing_uid = check_schema_exists(session, "UsrExcelReportService")

    if existing_uid:
        print(f"Schema already exists with UID: {existing_uid}")
        print("Will try to update it...")

    # Create/update the schema
    print("\nCreating UsrExcelReportService schema...")
    result = create_source_code_schema(session, package_uid, "UsrExcelReportService", SERVICE_CODE)

    if result:
        print("\nSchema created/updated successfully!")
        print("\nCompiling...")
        compile_schema(session)
    else:
        print("\nFailed to create schema")

if __name__ == "__main__":
    main()
