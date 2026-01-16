using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Linq;
using Terrasoft.Web.Common;
using Terrasoft.Core;
using Terrasoft.Core.Entities;

namespace Terrasoft.Configuration
{
    [DataContract]
    public class UsrExcelReportRequest
    {
        [DataMember(Name = "ReportId")]
        public Guid ReportId { get; set; }

        [DataMember(Name = "YearMonthId")]
        public Guid YearMonthId { get; set; }

        [DataMember(Name = "SalesRepId")]
        public Guid SalesRepId { get; set; }

        [DataMember(Name = "ExecutionId")]
        public Guid ExecutionId { get; set; }

        [DataMember(Name = "RecordCollection")]
        public List<Guid> RecordCollection { get; set; }
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
        private static readonly Dictionary<string, byte[]> ReportCache = new Dictionary<string, byte[]>();
        private static readonly object CacheLock = new object();

        private string GetYearMonthName(UserConnection uc, Guid id)
        {
            if (id == Guid.Empty) return null;
            try
            {
                var esq = new EntitySchemaQuery(uc.EntitySchemaManager, "BGYearMonth");
                esq.AddColumn("Name");
                var e = esq.GetEntity(uc, id);
                return e == null ? null : e.GetTypedColumnValue<string>("Name");
            }
            catch { return null; }
        }

        private bool ParseYearMonth(string name, out DateTime start, out DateTime end)
        {
            start = DateTime.MinValue;
            end = DateTime.MinValue;
            if (string.IsNullOrEmpty(name)) return false;
            var m = Regex.Match(name.Trim(), @"^(\d{4})-(\d{2})$");
            if (!m.Success) return false;
            int y = int.Parse(m.Groups[1].Value);
            int mo = int.Parse(m.Groups[2].Value);
            if (mo < 1 || mo > 12) return false;
            start = new DateTime(y, mo, 1);
            end = start.AddMonths(1);
            return true;
        }

        private byte[] GetTemplateFile(UserConnection uc, Guid reportId)
        {
            var esq = new EntitySchemaQuery(uc.EntitySchemaManager, "IntExcelReport");
            var fileCol = esq.AddColumn("IntFile");
            var e = esq.GetEntity(uc, reportId);
            if (e == null) return null;

            // Use the column's Name property (the ESQ alias) to access the value
            return e.GetBytesValue(fileCol.Name);
        }

        private string CacheBytes(byte[] data)
        {
            var key = "ReportCacheKey_" + Guid.NewGuid().ToString();
            lock (CacheLock)
            {
                if (ReportCache.Count > 50)
                {
                    var old = ReportCache.Keys.Take(25).ToList();
                    foreach (var k in old) ReportCache.Remove(k);
                }
                ReportCache[key] = data;
            }
            return key;
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
                var uc = (UserConnection)HttpContext.Current.Session["UserConnection"];

                // Get template
                var template = GetTemplateFile(uc, request.ReportId);
                if (template == null || template.Length == 0)
                {
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = "Template not found"
                    };
                }

                // Build query for Commission data with date-based filtering
                var esq = new EntitySchemaQuery(uc.EntitySchemaManager, "BGCommissionReportDataView");
                esq.PrimaryQueryColumn.IsAlwaysSelect = true;

                // Add columns (skip BGYearMonth to avoid INNER JOIN on NULL)
                esq.AddColumn("BGSalesRep");
                esq.AddColumn("BGDescription");
                esq.AddColumn("BGTransactionDate");
                esq.AddColumn("BGCommission");
                esq.AddColumn("BGAmount");

                // Apply date filter if YearMonth specified
                if (request.YearMonthId != Guid.Empty)
                {
                    var ymName = GetYearMonthName(uc, request.YearMonthId);
                    DateTime start, end;
                    if (ParseYearMonth(ymName, out start, out end))
                    {
                        esq.Filters.Add(esq.CreateFilterWithParameters(
                            FilterComparisonType.GreaterOrEqual, "BGTransactionDate", start));
                        esq.Filters.Add(esq.CreateFilterWithParameters(
                            FilterComparisonType.Less, "BGTransactionDate", end));
                    }
                }

                // Apply SalesGroup filter
                if (request.SalesRepId != Guid.Empty)
                {
                    esq.Filters.Add(esq.CreateFilterWithParameters(
                        FilterComparisonType.Equal, "BGSalesRep.BGSalesGroupLookup", request.SalesRepId));
                }

                var data = esq.GetEntityCollection(uc);
                int rowCount = data.Count;

                // For now, just cache the template and return success with row count
                // The template already has macros that will recalculate
                var cacheKey = CacheBytes(template);

                return new UsrExcelReportResponse
                {
                    success = true,
                    key = cacheKey,
                    message = "Query returned " + rowCount + " rows",
                    reportName = "Commission"
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
        [WebInvoke(Method = "GET", UriTemplate = "GetReport/{key}/{reportNameSegment}",
            ResponseFormat = WebMessageFormat.Json)]
        public Stream GetReport(string key, string reportNameSegment)
        {
            try
            {
                byte[] data = null;
                lock (CacheLock)
                {
                    if (ReportCache.ContainsKey(key))
                        data = ReportCache[key];
                }

                if (data == null)
                {
                    var ctx = WebOperationContext.Current;
                    ctx.OutgoingResponse.StatusCode = System.Net.HttpStatusCode.NotFound;
                    return new MemoryStream(Encoding.UTF8.GetBytes("{\"error\":\"Not found\"}"));
                }

                var ctx2 = WebOperationContext.Current;
                ctx2.OutgoingResponse.ContentType = "application/vnd.ms-excel.sheet.macroEnabled.12";
                ctx2.OutgoingResponse.Headers.Add("Content-Disposition",
                    "attachment; filename=\"Commission.xlsm\"");

                return new MemoryStream(data);
            }
            catch (Exception ex)
            {
                var ctx = WebOperationContext.Current;
                ctx.OutgoingResponse.StatusCode = System.Net.HttpStatusCode.InternalServerError;
                return new MemoryStream(Encoding.UTF8.GetBytes("{\"error\":\"" + ex.Message + "\"}"));
            }
        }
    }
}
