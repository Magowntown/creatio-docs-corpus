#!/usr/bin/env python3
"""
Update BGIntExcelReportService2 to add Generate method
"""

import os
import requests
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import ARTIFACTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# The Generate method code to add
GENERATE_METHOD = '''

		[DataContract]
		public class BGReportRequest {
			[DataMember(Name = "EsqString")]
			public string EsqString { get; set; }

			[DataMember(Name = "ReportId")]
			public Guid ReportId { get; set; }

			[DataMember(Name = "RecordCollection")]
			public List<Guid> RecordCollection { get; set; }
		}

		[OperationContract]
		[WebInvoke(Method = "POST", UriTemplate = "Generate",
			RequestFormat = WebMessageFormat.Json,
			ResponseFormat = WebMessageFormat.Json,
			BodyStyle = WebMessageBodyStyle.Bare)]
		public IntExcelExport.Models.IntExcelReportServiceResponse Generate(BGReportRequest request) {
			var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
				EsqString = request.EsqString,
				ReportId = request.ReportId,
				RecordCollection = request.RecordCollection
			};
			return IntExcelExport.Utilities.ReportUtilities.Generate(serviceRequest, SystemUserConnection);
		}

'''

def login(session):
    """Login to Creatio"""
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    login_data = {
        "UserName": USERNAME,
        "UserPassword": PASSWORD
    }
    response = session.post(login_url, json=login_data)
    print(f"Login response: {response.status_code}")

    # Get BPMCSRF token
    cookies = session.cookies.get_dict()
    print(f"Cookies: {list(cookies.keys())}")
    return "BPMCSRF" in cookies

def get_source_code(session, schema_uid):
    """Get source code schema content"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"

    query = {
        "RootSchemaName": "SysSchema",
        "OperationType": 0,
        "Columns": {
            "Items": {
                "Id": {"Expression": {"ColumnPath": "Id"}},
                "Name": {"Expression": {"ColumnPath": "Name"}},
                "Body": {"Expression": {"ColumnPath": "Body"}}
            }
        },
        "Filters": {
            "FilterType": 1,
            "Items": {
                "IdFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ColumnPath": "UId"},
                    "RightExpression": {"ParameterValue": schema_uid, "Type": 0}
                }
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    response = session.post(url, json=query, headers=headers)
    print(f"Get schema response: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get("rows") and len(data["rows"]) > 0:
            return data["rows"][0]
    return None

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("\nLogged in successfully!")

    # BGIntExcelReportService2 UID
    schema_uid = "ff5499a9-4aec-4403-9511-3394370035d3"

    print(f"\nFetching schema {schema_uid}...")
    schema = get_source_code(session, schema_uid)

    if schema:
        print(f"Schema Name: {schema.get('Name')}")
        body = schema.get('Body', '')
        print(f"Body length: {len(body) if body else 0} chars")

        if body:
            # Save the current body to a file
            out_path = ARTIFACTS_DIR / "current_service_body.txt"
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(body)
            print(f"Saved current body to {out_path}")
    else:
        print("Schema not found")

if __name__ == "__main__":
    main()
