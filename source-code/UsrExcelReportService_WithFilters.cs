using System;
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

        // Filter parameters - these are lookup GUIDs
        [DataMember(Name = "YearMonthId")]
        public Guid YearMonthId { get; set; }

        [DataMember(Name = "SalesRepId")]
        public Guid SalesRepId { get; set; }

        [DataMember(Name = "ExecutionId")]
        public Guid ExecutionId { get; set; }
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

                // Build filters config with Year-Month, Sales Rep, and Execution if provided
                string filtersConfig = BuildFiltersConfig(request.YearMonthId, request.SalesRepId, request.ExecutionId);

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
        /// Build the filtersConfig JSON for Year-Month, Sales Rep, and Execution filters.
        /// All filters use GUID lookup columns.
        /// </summary>
        private string BuildFiltersConfig(Guid yearMonthId, Guid salesRepId, Guid executionId)
        {
            // If no filters provided, return null
            if (yearMonthId == Guid.Empty && salesRepId == Guid.Empty && executionId == Guid.Empty)
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

            // Add Year-Month filter if provided (lookup column)
            if (yearMonthId != Guid.Empty)
            {
                items["YearMonthFilter"] = new JObject
                {
                    ["filterType"] = 1,  // CompareFilter
                    ["comparisonType"] = 3,  // Equal
                    ["isEnabled"] = true,
                    ["leftExpression"] = new JObject
                    {
                        ["expressionType"] = 0,  // SchemaColumn
                        ["columnPath"] = "BGYearMonth"
                    },
                    ["rightExpression"] = new JObject
                    {
                        ["expressionType"] = 2,  // Parameter
                        ["parameter"] = new JObject
                        {
                            ["dataValueType"] = 0,  // GUID
                            ["value"] = yearMonthId.ToString()
                        }
                    }
                };
            }

            // Add Sales Rep filter if provided (lookup column)
            if (salesRepId != Guid.Empty)
            {
                items["SalesRepFilter"] = new JObject
                {
                    ["filterType"] = 1,  // CompareFilter
                    ["comparisonType"] = 3,  // Equal
                    ["isEnabled"] = true,
                    ["leftExpression"] = new JObject
                    {
                        ["expressionType"] = 0,  // SchemaColumn
                        ["columnPath"] = "BGSalesRep"
                    },
                    ["rightExpression"] = new JObject
                    {
                        ["expressionType"] = 2,  // Parameter
                        ["parameter"] = new JObject
                        {
                            ["dataValueType"] = 0,  // GUID
                            ["value"] = salesRepId.ToString()
                        }
                    }
                };
            }

            // Add Execution filter if provided (original @P1@ replacement)
            if (executionId != Guid.Empty)
            {
                items["ExecutionFilter"] = new JObject
                {
                    ["filterType"] = 1,  // CompareFilter
                    ["comparisonType"] = 3,  // Equal
                    ["isEnabled"] = true,
                    ["leftExpression"] = new JObject
                    {
                        ["expressionType"] = 0,  // SchemaColumn
                        ["columnPath"] = "BGExecutionId"
                    },
                    ["rightExpression"] = new JObject
                    {
                        ["expressionType"] = 2,  // Parameter
                        ["parameter"] = new JObject
                        {
                            ["dataValueType"] = 0,  // GUID
                            ["value"] = executionId.ToString()
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
