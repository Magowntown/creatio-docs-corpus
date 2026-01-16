#!/usr/bin/env python3
"""
Deploy the UsrExcelReportService with Year-Month and Sales Group filter support.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"  # UsrExcelReportService

# Updated wrapper service code with filter support
WRAPPER_CODE = '''using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.Reflection;
using System.Linq;
using Terrasoft.Web.Common;
using Terrasoft.Core;
using Terrasoft.Core.Entities;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Terrasoft.Configuration
{
    [DataContract]
    public class UsrExcelReportRequest
    {
        [DataMember(Name = "EsqString")]
        public string EsqString { get; set; }

        [DataMember(Name = "ReportId")]
        public Guid ReportId { get; set; }

        [DataMember(Name = "RecordCollection")]
        public List<Guid> RecordCollection { get; set; }

        // New filter parameters
        [DataMember(Name = "YearMonth")]
        public string YearMonth { get; set; }

        [DataMember(Name = "SalesGroupId")]
        public Guid SalesGroupId { get; set; }
    }

    [DataContract]
    public class UsrExcelReportResponse
    {
        [DataMember(Name = "success")]
        public bool success { get; set; }

        [DataMember(Name = "key")]
        public string key { get; set; }

        [DataMember(Name = "message")]
        public string message { get; set; }

        [DataMember(Name = "reportName")]
        public string reportName { get; set; }
    }

    [ServiceContract]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
    public class UsrExcelReportService : BaseService
    {
        [OperationContract]
        [WebInvoke(Method = "POST", UriTemplate = "Generate",
            RequestFormat = WebMessageFormat.Json,
            ResponseFormat = WebMessageFormat.Json,
            BodyStyle = WebMessageBodyStyle.Bare)]
        public UsrExcelReportResponse Generate(UsrExcelReportRequest request)
        {
            try
            {
                var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                // Find ReportUtilities type
                Type utilitiesType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    utilitiesType = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                    if (utilitiesType != null) break;
                }

                if (utilitiesType == null)
                {
                    return new UsrExcelReportResponse { success = false, message = "ReportUtilities not found" };
                }

                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod == null)
                {
                    return new UsrExcelReportResponse { success = false, message = "Generate method not found" };
                }

                var parameters = generateMethod.GetParameters();
                if (parameters.Length != 1)
                {
                    return new UsrExcelReportResponse { success = false, message = "Generate has " + parameters.Length + " params" };
                }

                // Create IntExcelReportServiceRequest via reflection
                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                // Set ReportId property
                var reportIdProp = requestType.GetProperty("ReportId");
                if (reportIdProp != null)
                {
                    reportIdProp.SetValue(serviceRequest, request.ReportId);
                }

                // Build filters config with Year-Month and Sales Group if provided
                string filtersConfig = BuildFiltersConfig(request.YearMonth, request.SalesGroupId);

                var filtersConfigProp = requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null)
                {
                    filtersConfigProp.SetValue(serviceRequest, filtersConfig);
                }

                // Set recordCollection
                var recordCollectionProp = requestType.GetProperty("recordCollection");
                if (recordCollectionProp != null && request.RecordCollection != null)
                {
                    recordCollectionProp.SetValue(serviceRequest, request.RecordCollection);
                }

                // Create ReportUtilities instance
                object target = null;
                if (!generateMethod.IsStatic)
                {
                    var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
                    if (ctor != null)
                    {
                        target = ctor.Invoke(new object[] { userConnection });
                    }
                    else
                    {
                        target = Activator.CreateInstance(utilitiesType);
                    }
                }

                // Call Generate method
                var result = generateMethod.Invoke(target, new object[] { serviceRequest });

                // Handle string result (ExportFilterKey)
                if (result is string resultString)
                {
                    if (resultString.StartsWith("ExportFilterKey_"))
                    {
                        return new UsrExcelReportResponse
                        {
                            success = true,
                            key = resultString,
                            message = "Report generated successfully"
                        };
                    }
                    else
                    {
                        return new UsrExcelReportResponse
                        {
                            success = false,
                            message = "Unexpected result: " + resultString
                        };
                    }
                }

                // Handle object result (fallback)
                var resultType = result.GetType();
                var successProp = resultType.GetProperty("success");
                if (successProp != null)
                {
                    var response = new UsrExcelReportResponse
                    {
                        success = (bool)successProp.GetValue(result),
                        key = resultType.GetProperty("key")?.GetValue(result)?.ToString(),
                        message = resultType.GetProperty("message")?.GetValue(result)?.ToString(),
                        reportName = resultType.GetProperty("reportName")?.GetValue(result)?.ToString()
                    };
                    return response;
                }

                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Unknown result type: " + resultType.Name
                };
            }
            catch (TargetInvocationException tie)
            {
                var inner = tie.InnerException;
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "ReportId=" + request.ReportId + " | " + (inner != null ? inner.Message : tie.Message)
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "ReportId=" + request.ReportId + " | Error: " + ex.Message
                };
            }
        }

        /// <summary>
        /// Build the filtersConfig JSON for Year-Month and Sales Group filters.
        /// </summary>
        private string BuildFiltersConfig(string yearMonth, Guid salesGroupId)
        {
            // If no filters provided, return null
            if (string.IsNullOrEmpty(yearMonth) && salesGroupId == Guid.Empty)
            {
                return null;
            }

            var filterGroup = new JObject
            {
                ["filterType"] = 6,  // FilterGroup
                ["isEnabled"] = true,
                ["logicalOperation"] = 0,  // AND
                ["items"] = new JObject()
            };

            var items = (JObject)filterGroup["items"];
            int filterIndex = 0;

            // Add Year-Month filter if provided
            if (!string.IsNullOrEmpty(yearMonth))
            {
                items["YearMonthFilter"] = new JObject
                {
                    ["filterType"] = 1,  // CompareFilter
                    ["comparisonType"] = 3,  // Equal
                    ["isEnabled"] = true,
                    ["leftExpression"] = new JObject
                    {
                        ["expressionType"] = 0,  // SchemaColumn
                        ["columnPath"] = "UsrYearMonth"  // Adjust column name if different
                    },
                    ["rightExpression"] = new JObject
                    {
                        ["expressionType"] = 2,  // Parameter
                        ["parameter"] = new JObject
                        {
                            ["dataValueType"] = 1,  // Text
                            ["value"] = yearMonth
                        }
                    }
                };
                filterIndex++;
            }

            // Add Sales Group filter if provided
            if (salesGroupId != Guid.Empty)
            {
                items["SalesGroupFilter"] = new JObject
                {
                    ["filterType"] = 1,  // CompareFilter
                    ["comparisonType"] = 3,  // Equal
                    ["isEnabled"] = true,
                    ["leftExpression"] = new JObject
                    {
                        ["expressionType"] = 0,  // SchemaColumn
                        ["columnPath"] = "UsrSalesGroup"  // Adjust column name if different
                    },
                    ["rightExpression"] = new JObject
                    {
                        ["expressionType"] = 2,  // Parameter
                        ["parameter"] = new JObject
                        {
                            ["dataValueType"] = 0,  // GUID
                            ["value"] = salesGroupId.ToString()
                        }
                    }
                };
            }

            return filterGroup.ToString(Formatting.None);
        }

        [OperationContract]
        [WebInvoke(Method = "GET", UriTemplate = "GetFilterColumns",
            ResponseFormat = WebMessageFormat.Json)]
        public UsrExcelReportResponse GetFilterColumns()
        {
            // Helper endpoint to discover the correct column names for filtering
            try
            {
                var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];
                var esm = userConnection.EntitySchemaManager;
                var schema = esm.GetInstanceByName("BGCommissionReportDataView");

                var columns = schema.Columns.Select(c => c.Name + " (" + c.Caption + ")").ToList();

                return new UsrExcelReportResponse
                {
                    success = true,
                    message = string.Join(", ", columns)
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Error: " + ex.Message
                };
            }
        }
    }
}
'''

def main():
    session = requests.Session()

    # Login
    print("=== Logging in ===")
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Get existing schema
    print("\n=== Getting current schema ===")
    get_url = f"{CREATIO_URL}/0/rest/SourceCodeSchemaDesignerService/GetSchemaData"
    response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        return False

    schema_data = response.json()
    print(f"Got schema: {schema_data.get('name', 'N/A')}")

    # Update body
    schema_data["body"] = WRAPPER_CODE

    # Save
    print("\n=== Saving updated code with filter support ===")
    save_url = f"{CREATIO_URL}/0/rest/SourceCodeSchemaDesignerService/SaveSchema"
    response = session.post(save_url, json=schema_data, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"Save failed: {response.status_code}")
        print(response.text[:500])
        return False

    result = response.json()
    print(f"Save result: {json.dumps(result, indent=2)[:200]}")

    if result.get("success") == False:
        print(f"Save error: {result}")
        return False

    # Compile
    print("\n=== Compiling ===")
    compile_and_test(session, headers)

def compile_and_test(session, headers):
    import time

    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        print(f"Build attempt {attempt + 1}...")
        try:
            response = session.post(build_url, json={}, headers=headers, timeout=300)

            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                time.sleep(10)
                continue

            result = response.json()

            if result.get("success"):
                print(">>> Compilation successful!")
                time.sleep(3)
                # Test getting filter columns
                test_filter_columns(session, headers)
                return True
            else:
                error = result.get("errorInfo", {}).get("message", str(result))
                if "another compilation" in error.lower():
                    print("Waiting for other compilation...")
                    time.sleep(30)
                else:
                    print(f"Compilation error: {error[:500]}")
                    return False
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

    return False

def test_filter_columns(session, headers):
    """Test the GetFilterColumns endpoint to discover column names."""
    print("\n=== Getting Filter Column Names ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/GetFilterColumns"

    response = session.get(url, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"Available columns:\n{result.get('message', '')}")
        else:
            print(f"Error: {result.get('message', '')}")

if __name__ == "__main__":
    main()
