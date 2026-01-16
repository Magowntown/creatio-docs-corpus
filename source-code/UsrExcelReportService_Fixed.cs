using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.Reflection;
using System.IO;
using Terrasoft.Web.Common;
using Terrasoft.Core;
using Terrasoft.Core.Entities;

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
        /// <summary>
        /// Builds a single filter JSON string
        /// </summary>
        private string BuildFilterJson(string columnPath, Guid value)
        {
            return string.Format(@"{{
                ""filterType"": 1,
                ""comparisonType"": 3,
                ""isEnabled"": true,
                ""trimDateTimeParameterToDate"": false,
                ""leftExpression"": {{
                    ""expressionType"": 0,
                    ""columnPath"": ""{0}""
                }},
                ""rightExpression"": {{
                    ""expressionType"": 2,
                    ""parameter"": {{
                        ""dataValueType"": 0,
                        ""value"": ""{1}""
                    }}
                }}
            }}", columnPath, value.ToString());
        }

        /// <summary>
        /// Gets the IntExcelReport configuration and modifies ESQ with filters
        /// </summary>
        private string GetModifiedEsq(UserConnection userConnection, Guid reportId, UsrExcelReportRequest request)
        {
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            esq.AddColumn("IntEsq");
            esq.AddColumn("IntEntitySchemaName");

            var entity = esq.GetEntity(userConnection, reportId);
            if (entity == null)
            {
                return null;
            }

            var intEsq = entity.GetTypedColumnValue<string>("IntEsq");
            var entitySchemaName = entity.GetTypedColumnValue<string>("IntEntitySchemaName");

            if (string.IsNullOrEmpty(intEsq))
            {
                return null;
            }

            // Check if we have any filters to apply
            if (request.YearMonthId == Guid.Empty && request.SalesRepId == Guid.Empty)
            {
                return intEsq;
            }

            try
            {
                // Build filter items using string manipulation
                var filterItems = new List<string>();
                int filterIndex = 0;

                // Add YearMonth filter if provided
                if (request.YearMonthId != Guid.Empty)
                {
                    string yearMonthColumn = "BGYearMonthId";
                    if (entitySchemaName == "IWPayments")
                    {
                        yearMonthColumn = "IWBGYearMonth";
                    }
                    filterItems.Add(string.Format(@"""Filter{0}"": {1}", filterIndex++,
                        BuildFilterJson(yearMonthColumn, request.YearMonthId)));
                }

                // Add SalesRep filter if provided
                if (request.SalesRepId != Guid.Empty)
                {
                    string salesColumn = "BGSalesRepId";
                    if (entitySchemaName == "IWPayments")
                    {
                        salesColumn = "IWPaymentsInvoice.BGSalesGroup";
                    }
                    filterItems.Add(string.Format(@"""Filter{0}"": {1}", filterIndex++,
                        BuildFilterJson(salesColumn, request.SalesRepId)));
                }

                if (filterItems.Count == 0)
                {
                    return intEsq;
                }

                // Find the "items":{} section and inject our filters
                string itemsPattern = @"""items"":\s*\{";
                var match = System.Text.RegularExpressions.Regex.Match(intEsq, itemsPattern);

                if (match.Success)
                {
                    // Find the position right after "items":{
                    int insertPos = match.Index + match.Length;

                    // Check if items is empty (just closing brace)
                    string afterItems = intEsq.Substring(insertPos).TrimStart();

                    if (afterItems.StartsWith("}"))
                    {
                        // Empty items, just insert our filters
                        string filterStr = string.Join(",", filterItems);
                        intEsq = intEsq.Insert(insertPos, filterStr);
                    }
                    else
                    {
                        // Has existing items, prepend our filters with comma
                        string filterStr = string.Join(",", filterItems) + ",";
                        intEsq = intEsq.Insert(insertPos, filterStr);
                    }
                }
                else
                {
                    // No filters section exists, we need to add one
                    // Find end of "filters":{ and add items
                    string filtersPattern = @"""filters"":\s*\{";
                    var filtersMatch = System.Text.RegularExpressions.Regex.Match(intEsq, filtersPattern);

                    if (filtersMatch.Success)
                    {
                        int pos = filtersMatch.Index + filtersMatch.Length;
                        string filterContent = string.Format(@"""filterType"":6,""items"":{{{0}}}",
                            string.Join(",", filterItems));

                        // Replace existing content if any
                        int endBrace = intEsq.IndexOf('}', pos);
                        if (endBrace > pos)
                        {
                            intEsq = intEsq.Substring(0, pos) + filterContent + intEsq.Substring(endBrace);
                        }
                    }
                }

                return intEsq;
            }
            catch (Exception)
            {
                return intEsq;
            }
        }

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

                System.Diagnostics.Debug.WriteLine(string.Format(
                    "UsrExcelReportService.Generate - ReportId: {0}, YearMonthId: {1}, SalesRepId: {2}",
                    request.ReportId, request.YearMonthId, request.SalesRepId));

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

                var requestType = parameters[0].ParameterType;
                var serviceRequest = FormatterServices.GetUninitializedObject(requestType);

                var reportIdProp = requestType.GetProperty("ReportId");
                if (reportIdProp != null)
                {
                    reportIdProp.SetValue(serviceRequest, request.ReportId);
                }

                // Set esqString with modified ESQ containing filters
                var esqStringProp = requestType.GetProperty("esqString") ?? requestType.GetProperty("EsqString");
                if (esqStringProp != null)
                {
                    var modifiedEsq = GetModifiedEsq(userConnection, request.ReportId, request);
                    if (!string.IsNullOrEmpty(modifiedEsq))
                    {
                        esqStringProp.SetValue(serviceRequest, modifiedEsq);
                    }
                }

                var recordCollectionProp = requestType.GetProperty("recordCollection");
                if (recordCollectionProp != null)
                {
                    recordCollectionProp.SetValue(serviceRequest, request.RecordCollection ?? new List<Guid>());
                }

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

                var result = generateMethod.Invoke(target, new object[] { serviceRequest });
                if (result == null)
                {
                    return new UsrExcelReportResponse { success = false, message = "result is null" };
                }

                string resultStr = result.ToString();

                if (resultStr.StartsWith("ExportFilterKey_"))
                {
                    return new UsrExcelReportResponse
                    {
                        success = true,
                        key = resultStr,
                        message = "Report generated successfully"
                    };
                }

                Guid fileKey;
                if (Guid.TryParse(resultStr, out fileKey))
                {
                    return new UsrExcelReportResponse
                    {
                        success = true,
                        key = resultStr,
                        message = "Report generated successfully"
                    };
                }

                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Unexpected result: " + resultStr
                };
            }
            catch (TargetInvocationException tie)
            {
                var inner = tie.InnerException;
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = inner?.GetType().Name + ": " + inner?.Message
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = ex.GetType().Name + ": " + ex.Message
                };
            }
        }

        [OperationContract]
        [WebInvoke(Method = "GET", UriTemplate = "GetMethods",
            ResponseFormat = WebMessageFormat.Json)]
        public UsrExcelReportResponse GetMethods()
        {
            try
            {
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

                var methods = utilitiesType.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static);
                var methodList = new List<string>();
                foreach (var m in methods)
                {
                    var paramList = new List<string>();
                    foreach (var p in m.GetParameters())
                    {
                        paramList.Add(p.ParameterType.Name);
                    }
                    methodList.Add(m.Name + "(" + string.Join(",", paramList) + ")->" + m.ReturnType.Name);
                }
                var methodInfo = string.Join("; ", methodList);

                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod != null)
                {
                    var requestType = generateMethod.GetParameters()[0].ParameterType;
                    var props = requestType.GetProperties();
                    var propList = new List<string>();
                    foreach (var p in props)
                    {
                        propList.Add(p.Name + ":" + p.PropertyType.Name);
                    }
                    methodInfo += " | RequestProps: " + string.Join(",", propList);
                }

                return new UsrExcelReportResponse
                {
                    success = true,
                    message = methodInfo
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse { success = false, message = ex.Message };
            }
        }

        [OperationContract]
        [WebInvoke(Method = "GET", UriTemplate = "DiagnoseCache/{key}",
            ResponseFormat = WebMessageFormat.Json)]
        public UsrExcelReportResponse DiagnoseCache(string key)
        {
            try
            {
                var diagnostics = new List<string>();

                // Check session keys
                diagnostics.Add($"Session keys count: {HttpContext.Current.Session.Keys.Count}");
                foreach (string sessionKey in HttpContext.Current.Session.Keys)
                {
                    if (sessionKey.Contains("Export") || sessionKey.Contains("Filter") || sessionKey == key)
                    {
                        var obj = HttpContext.Current.Session[sessionKey];
                        diagnostics.Add($"Session[{sessionKey}]: {obj?.GetType().Name ?? "null"}");
                    }
                }

                // Check HttpRuntime.Cache
                var cacheEnum = System.Web.HttpRuntime.Cache.GetEnumerator();
                int cacheCount = 0;
                while (cacheEnum.MoveNext())
                {
                    cacheCount++;
                    var cacheKey = cacheEnum.Key?.ToString();
                    if (cacheKey != null && (cacheKey.Contains("Export") || cacheKey.Contains("Filter") || cacheKey == key))
                    {
                        diagnostics.Add($"Cache[{cacheKey}]: {cacheEnum.Value?.GetType().Name ?? "null"}");
                    }
                }
                diagnostics.Add($"Cache total items: {cacheCount}");

                // Check for specific key
                var sessionVal = HttpContext.Current.Session[key];
                var cacheVal = System.Web.HttpRuntime.Cache[key];
                diagnostics.Add($"Direct session lookup [{key}]: {sessionVal?.GetType().Name ?? "not found"}");
                diagnostics.Add($"Direct cache lookup [{key}]: {cacheVal?.GetType().Name ?? "not found"}");

                return new UsrExcelReportResponse
                {
                    success = true,
                    message = string.Join(" | ", diagnostics)
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = $"Error: {ex.Message}"
                };
            }
        }

        [OperationContract]
        [WebGet(UriTemplate = "GetFile/{key}")]
        public Stream GetFile(string key)
        {
            try
            {
                // Try to get file from session cache (where IntExcelExport stores it)
                var sessionObj = HttpContext.Current.Session[key];
                if (sessionObj != null)
                {
                    if (sessionObj is byte[] bytes)
                    {
                        WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                        WebOperationContext.Current.OutgoingResponse.Headers.Add("Content-Disposition", "attachment; filename=Report.xlsx");
                        return new MemoryStream(bytes);
                    }
                    else if (sessionObj is Stream stream)
                    {
                        WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                        WebOperationContext.Current.OutgoingResponse.Headers.Add("Content-Disposition", "attachment; filename=Report.xlsx");
                        return stream;
                    }
                }

                // Try HttpRuntime.Cache
                var cacheObj = System.Web.HttpRuntime.Cache[key];
                if (cacheObj != null)
                {
                    if (cacheObj is byte[] bytes)
                    {
                        WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                        WebOperationContext.Current.OutgoingResponse.Headers.Add("Content-Disposition", "attachment; filename=Report.xlsx");
                        return new MemoryStream(bytes);
                    }
                    else if (cacheObj is Stream stream)
                    {
                        WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                        WebOperationContext.Current.OutgoingResponse.Headers.Add("Content-Disposition", "attachment; filename=Report.xlsx");
                        return stream;
                    }
                }

                // Try to get via reflection on IntExcelExport internal caches
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    // Look for cache manager types
                    var cacheTypes = new[] {
                        "IntExcelExport.Utilities.ExportCache",
                        "IntExcelExport.Cache.ExportCache",
                        "IntExcelExport.ExportFileCache"
                    };

                    foreach (var typeName in cacheTypes)
                    {
                        var cacheType = assembly.GetType(typeName);
                        if (cacheType != null)
                        {
                            var getMethod = cacheType.GetMethod("Get")
                                ?? cacheType.GetMethod("GetFile")
                                ?? cacheType.GetMethod("GetBytes");

                            if (getMethod != null)
                            {
                                object target = null;
                                if (!getMethod.IsStatic)
                                {
                                    target = Activator.CreateInstance(cacheType);
                                }

                                var result = getMethod.Invoke(target, new object[] { key });
                                if (result is byte[] resultBytes)
                                {
                                    WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                                    WebOperationContext.Current.OutgoingResponse.Headers.Add("Content-Disposition", "attachment; filename=Report.xlsx");
                                    return new MemoryStream(resultBytes);
                                }
                            }
                        }
                    }
                }

                return null;
            }
            catch
            {
                return null;
            }
        }
    }
}
