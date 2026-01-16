using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.IO;
using System.IO.Packaging;
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

    /// <summary>
    /// Standalone Excel report service using System.IO.Packaging (OPC format).
    /// </summary>
    [ServiceContract]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
    public class UsrExcelReportService : BaseService
    {
        private static readonly Dictionary<string, byte[]> _reportCache = new Dictionary<string, byte[]>();
        private static readonly object _cacheLock = new object();

        #region Helper Methods

        private string GetYearMonthName(UserConnection userConnection, Guid yearMonthId)
        {
            if (yearMonthId == Guid.Empty) return null;
            try
            {
                var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGYearMonth");
                esq.AddColumn("Name");
                var entity = esq.GetEntity(userConnection, yearMonthId);
                return entity?.GetTypedColumnValue<string>("Name");
            }
            catch { return null; }
        }

        private bool TryParseYearMonth(string yearMonthName, out DateTime startDate, out DateTime endDate)
        {
            startDate = DateTime.MinValue;
            endDate = DateTime.MinValue;
            if (string.IsNullOrEmpty(yearMonthName)) return false;

            var match = Regex.Match(yearMonthName.Trim(), @"^(\d{4})-(\d{2})$");
            if (!match.Success) return false;

            int year = int.Parse(match.Groups[1].Value);
            int month = int.Parse(match.Groups[2].Value);
            if (month < 1 || month > 12 || year < 2000 || year > 2100) return false;

            startDate = new DateTime(year, month, 1, 0, 0, 0, DateTimeKind.Utc);
            endDate = startDate.AddMonths(1);
            return true;
        }

        private (string IntEsq, byte[] IntFile, string SheetName, string ReportName) GetReportConfig(
            UserConnection userConnection, Guid reportId)
        {
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            esq.AddColumn("IntEsq");
            esq.AddColumn("IntFile");
            esq.AddColumn("IntSheetName");
            esq.AddColumn("IntName");

            var entity = esq.GetEntity(userConnection, reportId);
            if (entity == null) return (null, null, null, null);

            return (
                entity.GetTypedColumnValue<string>("IntEsq"),
                entity.GetTypedColumnValue<byte[]>("IntFile"),
                entity.GetTypedColumnValue<string>("IntSheetName") ?? "Data",
                entity.GetTypedColumnValue<string>("IntName") ?? "Report"
            );
        }

        private List<(string Caption, string ColumnPath)> ParseColumnsFromIntEsq(string intEsqJson)
        {
            var columns = new List<(string Caption, string ColumnPath)>();
            if (string.IsNullOrEmpty(intEsqJson)) return columns;

            var matches = Regex.Matches(intEsqJson,
                "\"(?<caption>[^\"]+)\"\\s*:\\s*\\{[^}]*\"columnPath\"\\s*:\\s*\"(?<path>[^\"]+)\"");

            foreach (Match m in matches)
            {
                var caption = m.Groups["caption"].Value;
                var path = m.Groups["path"].Value;
                if (caption == "className" || caption == "items" || caption == "expression") continue;
                columns.Add((caption, path));
            }
            return columns;
        }

        private string ParseRootSchemaName(string intEsqJson)
        {
            if (string.IsNullOrEmpty(intEsqJson)) return null;
            var match = Regex.Match(intEsqJson, "\"rootSchemaName\"\\s*:\\s*\"(?<name>[^\"]+)\"");
            return match.Success ? match.Groups["name"].Value : null;
        }

        private EntityCollection ExecuteQuery(
            UserConnection userConnection,
            string rootSchemaName,
            List<(string Caption, string ColumnPath)> columns,
            UsrExcelReportRequest request,
            out int rowCount)
        {
            rowCount = 0;
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, rootSchemaName);
            esq.PrimaryQueryColumn.IsAlwaysSelect = true;

            var addedPaths = new HashSet<string>();
            foreach (var col in columns)
            {
                if (col.ColumnPath.Contains("BGYearMonth")) continue;
                if (addedPaths.Contains(col.ColumnPath)) continue;
                try
                {
                    esq.AddColumn(col.ColumnPath);
                    addedPaths.Add(col.ColumnPath);
                }
                catch { }
            }

            if (request.YearMonthId != Guid.Empty)
            {
                var yearMonthName = GetYearMonthName(userConnection, request.YearMonthId);
                DateTime startDate, endDate;
                if (TryParseYearMonth(yearMonthName, out startDate, out endDate))
                {
                    esq.Filters.Add(esq.CreateFilterWithParameters(
                        FilterComparisonType.GreaterOrEqual, "BGTransactionDate", startDate));
                    esq.Filters.Add(esq.CreateFilterWithParameters(
                        FilterComparisonType.Less, "BGTransactionDate", endDate));
                }
            }

            if (request.SalesRepId != Guid.Empty)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Equal, "BGSalesRep.BGSalesGroupLookup", request.SalesRepId));
            }

            var collection = esq.GetEntityCollection(userConnection);
            rowCount = collection.Count;
            return collection;
        }

        private string GetColumnLetter(int col)
        {
            var sb = new StringBuilder();
            while (col > 0)
            {
                col--;
                sb.Insert(0, (char)('A' + col % 26));
                col /= 26;
            }
            return sb.ToString();
        }

        private string EscapeXml(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";
            return s.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;")
                    .Replace("\"", "&quot;").Replace("'", "&apos;");
        }

        /// <summary>
        /// Modifies xlsx using System.IO.Packaging (OPC format).
        /// </summary>
        private byte[] WriteDataToTemplate(
            byte[] templateBytes,
            string targetSheetName,
            List<(string Caption, string ColumnPath)> columns,
            EntityCollection data)
        {
            using (var ms = new MemoryStream())
            {
                ms.Write(templateBytes, 0, templateBytes.Length);
                ms.Position = 0;

                using (var package = Package.Open(ms, FileMode.Open, FileAccess.ReadWrite))
                {
                    // Find the sheet part
                    var sheetUri = new Uri("/xl/worksheets/sheet1.xml", UriKind.Relative);
                    PackagePart sheetPart = null;

                    if (package.PartExists(sheetUri))
                    {
                        sheetPart = package.GetPart(sheetUri);
                    }
                    else
                    {
                        // Try to find any worksheet
                        foreach (var part in package.GetParts())
                        {
                            if (part.Uri.ToString().Contains("/xl/worksheets/") &&
                                part.Uri.ToString().EndsWith(".xml"))
                            {
                                sheetPart = part;
                                sheetUri = part.Uri;
                                break;
                            }
                        }
                    }

                    if (sheetPart == null)
                    {
                        throw new Exception("No worksheet found in template");
                    }

                    // Read existing XML
                    string sheetXml;
                    using (var reader = new StreamReader(sheetPart.GetStream(FileMode.Open, FileAccess.Read)))
                    {
                        sheetXml = reader.ReadToEnd();
                    }

                    // Build new sheetData
                    var activeColumns = columns.Where(c => !c.ColumnPath.Contains("BGYearMonth")).ToList();
                    var newSheetData = BuildSheetDataXml(activeColumns, data);

                    // Replace sheetData in XML
                    var sheetDataPattern = @"<sheetData[^>]*>.*?</sheetData>";
                    var newXml = Regex.Replace(sheetXml, sheetDataPattern, newSheetData,
                        RegexOptions.Singleline);

                    if (!newXml.Contains("<sheetData"))
                    {
                        newXml = newXml.Replace("</worksheet>", newSheetData + "</worksheet>");
                    }

                    // Write back
                    using (var writer = new StreamWriter(sheetPart.GetStream(FileMode.Create, FileAccess.Write)))
                    {
                        writer.Write(newXml);
                    }
                }

                return ms.ToArray();
            }
        }

        private string BuildSheetDataXml(
            List<(string Caption, string ColumnPath)> columns,
            EntityCollection data)
        {
            var sb = new StringBuilder();
            sb.Append("<sheetData>");

            // Header row
            sb.Append("<row r=\"1\">");
            for (int i = 0; i < columns.Count; i++)
            {
                var cellRef = GetColumnLetter(i + 1) + "1";
                sb.AppendFormat("<c r=\"{0}\" t=\"inlineStr\"><is><t>{1}</t></is></c>",
                    cellRef, EscapeXml(columns[i].Caption));
            }
            sb.Append("</row>");

            // Data rows
            int rowNum = 2;
            foreach (var entity in data)
            {
                sb.AppendFormat("<row r=\"{0}\">", rowNum);

                for (int i = 0; i < columns.Count; i++)
                {
                    var cellRef = GetColumnLetter(i + 1) + rowNum.ToString();
                    object value = null;

                    try
                    {
                        var columnPath = columns[i].ColumnPath;
                        var parts = columnPath.Split('.');
                        var colName = parts.Last();
                        var schemaColumn = entity.Schema.Columns.FindByName(colName);
                        if (schemaColumn != null)
                        {
                            value = entity.GetColumnValue(schemaColumn);
                        }
                    }
                    catch { }

                    AppendCellXml(sb, cellRef, value);
                }

                sb.Append("</row>");
                rowNum++;
            }

            sb.Append("</sheetData>");
            return sb.ToString();
        }

        private void AppendCellXml(StringBuilder sb, string cellRef, object value)
        {
            if (value == null)
            {
                sb.AppendFormat("<c r=\"{0}\" t=\"inlineStr\"><is><t></t></is></c>", cellRef);
                return;
            }

            var valueType = value.GetType();

            if (valueType == typeof(decimal) || valueType == typeof(double) ||
                valueType == typeof(int) || valueType == typeof(long) || valueType == typeof(float))
            {
                sb.AppendFormat("<c r=\"{0}\"><v>{1}</v></c>",
                    cellRef,
                    Convert.ToString(value, System.Globalization.CultureInfo.InvariantCulture));
            }
            else if (valueType == typeof(DateTime))
            {
                var dt = (DateTime)value;
                sb.AppendFormat("<c r=\"{0}\"><v>{1}</v></c>",
                    cellRef,
                    dt.ToOADate().ToString(System.Globalization.CultureInfo.InvariantCulture));
            }
            else if (valueType == typeof(bool))
            {
                sb.AppendFormat("<c r=\"{0}\" t=\"b\"><v>{1}</v></c>",
                    cellRef, (bool)value ? "1" : "0");
            }
            else
            {
                sb.AppendFormat("<c r=\"{0}\" t=\"inlineStr\"><is><t>{1}</t></is></c>",
                    cellRef, EscapeXml(value.ToString()));
            }
        }

        private string CacheReport(byte[] reportBytes)
        {
            var key = "ReportCacheKey_" + Guid.NewGuid().ToString();
            lock (_cacheLock)
            {
                if (_reportCache.Count > 50)
                {
                    var oldKeys = _reportCache.Keys.Take(25).ToList();
                    foreach (var k in oldKeys) _reportCache.Remove(k);
                }
                _reportCache[key] = reportBytes;
            }
            return key;
        }

        private bool HasVbaMacros(byte[] fileBytes)
        {
            try
            {
                using (var ms = new MemoryStream(fileBytes))
                using (var package = Package.Open(ms, FileMode.Open, FileAccess.Read))
                {
                    foreach (var part in package.GetParts())
                    {
                        if (part.Uri.ToString().ToLower().Contains("vbaproject.bin"))
                        {
                            return true;
                        }
                    }
                }
            }
            catch { }
            return false;
        }

        #endregion

        #region Service Methods

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

                var (intEsq, intFile, sheetName, reportName) = GetReportConfig(userConnection, request.ReportId);

                if (string.IsNullOrEmpty(intEsq))
                {
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = "IntEsq is empty for this report"
                    };
                }

                if (intFile == null || intFile.Length == 0)
                {
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = "IntFile (template) is empty"
                    };
                }

                var rootSchemaName = ParseRootSchemaName(intEsq);
                if (string.IsNullOrEmpty(rootSchemaName))
                {
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = "Could not parse rootSchemaName"
                    };
                }

                var columns = ParseColumnsFromIntEsq(intEsq);
                if (columns.Count == 0)
                {
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = "Could not parse columns from IntEsq"
                    };
                }

                int rowCount;
                var data = ExecuteQuery(userConnection, rootSchemaName, columns, request, out rowCount);

                var reportBytes = WriteDataToTemplate(intFile, sheetName, columns, data);
                var cacheKey = CacheReport(reportBytes);

                return new UsrExcelReportResponse
                {
                    success = true,
                    key = cacheKey,
                    message = $"Generated: {rowCount} rows",
                    reportName = reportName
                };
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = $"{ex.GetType().Name}: {ex.Message}"
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
                byte[] reportBytes = null;
                lock (_cacheLock)
                {
                    if (_reportCache.ContainsKey(key))
                        reportBytes = _reportCache[key];
                }

                if (reportBytes == null)
                {
                    var ctx = WebOperationContext.Current;
                    ctx.OutgoingResponse.ContentType = "application/json";
                    ctx.OutgoingResponse.StatusCode = System.Net.HttpStatusCode.NotFound;
                    return new MemoryStream(Encoding.UTF8.GetBytes("{\"error\":\"Not found\"}"));
                }

                bool hasVba = HasVbaMacros(reportBytes);
                var ext = hasVba ? "xlsm" : "xlsx";
                var contentType = hasVba
                    ? "application/vnd.ms-excel.sheet.macroEnabled.12"
                    : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

                var safeName = Regex.Replace(reportNameSegment ?? "Report", @"[^a-zA-Z0-9_\-]", "_");

                var ctx2 = WebOperationContext.Current;
                ctx2.OutgoingResponse.ContentType = contentType;
                ctx2.OutgoingResponse.Headers.Add("Content-Disposition",
                    $"attachment; filename=\"{safeName}.{ext}\"");

                return new MemoryStream(reportBytes);
            }
            catch (Exception ex)
            {
                var ctx = WebOperationContext.Current;
                ctx.OutgoingResponse.ContentType = "application/json";
                ctx.OutgoingResponse.StatusCode = System.Net.HttpStatusCode.InternalServerError;
                return new MemoryStream(Encoding.UTF8.GetBytes("{\"error\":\"" + ex.Message.Replace("\"", "'") + "\"}"));
            }
        }

        #endregion
    }
}
