using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Activation;
using System.Web;
using System.Reflection;
using System.Linq;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;
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

        // NEW: Filter parameters
        [DataMember(Name = "YearMonthId")]
        public Guid YearMonthId { get; set; }

        // Note: frontend uses SalesRepId field name to carry SalesGroupId (legacy naming).
        [DataMember(Name = "SalesRepId")]
        public Guid SalesRepId { get; set; }

        [DataMember(Name = "ExecutionId")]
        public Guid ExecutionId { get; set; }

        // NEW: Customer (Account) filter for "Items by Customer" report
        [DataMember(Name = "CustomerId")]
        public Guid CustomerId { get; set; }

        // Customer name for filtering BGSalesByItemView.BGCustomer (varchar)
        [DataMember(Name = "CustomerName")]
        public string CustomerName { get; set; }

        // Date filters for "Items by Customer" and similar reports
        [DataMember(Name = "CreatedFrom")]
        public DateTime? CreatedFrom { get; set; }

        [DataMember(Name = "CreatedTo")]
        public DateTime? CreatedTo { get; set; }

        [DataMember(Name = "ShippingFrom")]
        public DateTime? ShippingFrom { get; set; }

        [DataMember(Name = "ShippingTo")]
        public DateTime? ShippingTo { get; set; }

        [DataMember(Name = "DeliveryFrom")]
        public DateTime? DeliveryFrom { get; set; }

        [DataMember(Name = "DeliveryTo")]
        public DateTime? DeliveryTo { get; set; }

        // Status filter
        [DataMember(Name = "StatusName")]
        public string StatusName { get; set; }
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
        // Stores the last error from PopulateExcelTemplate for diagnostics
        [ThreadStatic]
        private static string _lastPopulateError;

        /// <summary>
        /// Builds a single filter JSON (CompareFilter) for a given column path and GUID value.
        /// </summary>
        private string BuildFilterJson(string columnPath, Guid value)
        {
            // Keep output compact; whitespace doesn't matter but smaller strings reduce churn.
            return string.Format(
                "{{\"filterType\":1,\"comparisonType\":3,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":0,\"value\":\"{1}\"}}}}}}",
                columnPath,
                value.ToString()
            );
        }

        /// <summary>
        /// Builds a single filter JSON (CompareFilter) for a given column path and string value.
        /// Uses comparisonType 3 (Equals) for exact string match.
        /// </summary>
        private string BuildStringFilterJson(string columnPath, string value)
        {
            // Escape quotes in the value for JSON safety
            var escapedValue = (value ?? "").Replace("\\", "\\\\").Replace("\"", "\\\"");
            return string.Format(
                "{{\"filterType\":1,\"comparisonType\":3,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":1,\"value\":\"{1}\"}}}}}}",
                columnPath,
                escapedValue
            );
        }

        /// <summary>
        /// Builds a CONTAINS filter JSON for a given column path and string value.
        /// Uses comparisonType 11 (Contains) for substring match.
        /// </summary>
        private string BuildStringContainsFilterJson(string columnPath, string value)
        {
            // Escape quotes in the value for JSON safety
            var escapedValue = (value ?? "").Replace("\\", "\\\\").Replace("\"", "\\\"");
            return string.Format(
                "{{\"filterType\":1,\"comparisonType\":11,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":1,\"value\":\"{1}\"}}}}}}",
                columnPath,
                escapedValue
            );
        }

        /// <summary>
        /// Builds a "greater than or equal" date filter JSON (>= date).
        /// </summary>
        private string BuildDateGteFilterJson(string columnPath, DateTime date)
        {
            var isoDate = date.Date.ToString("yyyy-MM-ddT00:00:00.000Z");
            return string.Format(
                "{{\"filterType\":1,\"comparisonType\":4,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":7,\"value\":\"{1}\"}}}}}}",
                columnPath, isoDate);
        }

        /// <summary>
        /// Builds a "less than or equal" date filter JSON (<= date, uses end of day).
        /// </summary>
        private string BuildDateLteFilterJson(string columnPath, DateTime date)
        {
            // Use end of day (23:59:59.999) for inclusive "to" date
            var isoDate = date.Date.AddDays(1).AddMilliseconds(-1).ToString("yyyy-MM-ddTHH:mm:ss.999Z");
            return string.Format(
                "{{\"filterType\":1,\"comparisonType\":5,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":7,\"value\":\"{1}\"}}}}}}",
                columnPath, isoDate);
        }

        /// <summary>
        /// Builds a date range filter JSON (FilterGroup with >= startDate AND < endDate).
        /// </summary>
        private string BuildDateRangeFilterJson(string columnPath, DateTime startDate, DateTime endDate)
        {
            // Format: ISO 8601 date-time for comparison
            var startIso = startDate.ToString("yyyy-MM-ddTHH:mm:ss.000Z");
            var endIso = endDate.ToString("yyyy-MM-ddTHH:mm:ss.000Z");

            // Greater than or equal to start date (comparisonType 4 = >=)
            var gteFilter = string.Format(
                "{{\"filterType\":1,\"comparisonType\":4,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":7,\"value\":\"{1}\"}}}}}}",
                columnPath, startIso);

            // Less than end date (comparisonType 6 = <)
            var ltFilter = string.Format(
                "{{\"filterType\":1,\"comparisonType\":6,\"isEnabled\":true,\"trimDateTimeParameterToDate\":false,\"leftExpression\":{{\"expressionType\":0,\"columnPath\":\"{0}\"}},\"rightExpression\":{{\"expressionType\":2,\"parameter\":{{\"dataValueType\":7,\"value\":\"{1}\"}}}}}}",
                columnPath, endIso);

            // Combine as AND group
            return string.Format(
                "{{\"filterType\":6,\"isEnabled\":true,\"logicalOperation\":0,\"items\":{{\"DateGte\":{0},\"DateLt\":{1}}}}}",
                gteFilter, ltFilter);
        }

        /// <summary>
        /// Gets the Year-Month name from BGYearMonth lookup by ID.
        /// </summary>
        private string GetYearMonthName(UserConnection userConnection, Guid yearMonthId)
        {
            if (yearMonthId == Guid.Empty)
            {
                return null;
            }

            try
            {
                var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGYearMonth");
                esq.AddColumn("Name");
                var entity = esq.GetEntity(userConnection, yearMonthId);
                if (entity != null)
                {
                    return entity.GetTypedColumnValue<string>("Name");
                }
            }
            catch
            {
                // Ignore - fallback will be no filter
            }

            return null;
        }

        /// <summary>
        /// Parses a Year-Month name like "2025-01" and returns the start and end dates.
        /// </summary>
        private bool TryParseYearMonth(string yearMonthName, out DateTime startDate, out DateTime endDate)
        {
            startDate = DateTime.MinValue;
            endDate = DateTime.MinValue;

            if (string.IsNullOrEmpty(yearMonthName))
            {
                return false;
            }

            // Expected format: "YYYY-MM" e.g., "2025-01"
            var match = Regex.Match(yearMonthName.Trim(), @"^(\d{4})-(\d{2})$");
            if (!match.Success)
            {
                return false;
            }

            int year = int.Parse(match.Groups[1].Value);
            int month = int.Parse(match.Groups[2].Value);

            if (month < 1 || month > 12 || year < 2000 || year > 2100)
            {
                return false;
            }

            startDate = new DateTime(year, month, 1, 0, 0, 0, DateTimeKind.Utc);
            endDate = startDate.AddMonths(1);

            return true;
        }

        private string GetReportEntitySchemaName(UserConnection userConnection, Guid reportId)
        {
            // Get IntEsq to parse rootSchemaName - this column always exists
            // IntEntitySchemaName column may not exist in all Creatio environments
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            esq.AddColumn("IntEsq");

            // Try to add IntEntitySchemaName columns if they exist
            // NOTE: IntEntitySchemaName is a lookup to SysSchema - we need the display name
            EntitySchemaQueryColumn schemaNameColumn = null;
            try
            {
                esq.AddColumn("IntEntitySchemaName");
                // Add the lookup ID for GUID-based resolution fallback
                esq.AddColumn("IntEntitySchemaNameId");
                // Add the display name column for lookup resolution
                // Store the column reference to get the correct alias later
                schemaNameColumn = esq.AddColumn("IntEntitySchemaName.Name");
            }
            catch
            {
                // Column doesn't exist - that's OK, we'll use IntEsq
            }

            var entity = esq.GetEntity(userConnection, reportId);
            if (entity == null)
            {
                return null;
            }

            // 1) Try IntEntitySchemaName lookup display name (e.g., "BGSalesByItemView")
            try
            {
                // For lookup columns, use the column reference to get correct alias
                if (schemaNameColumn != null)
                {
                    var schemaDisplayName = (entity.GetTypedColumnValue<string>(schemaNameColumn.Name) ?? "").Trim();
                    if (!string.IsNullOrEmpty(schemaDisplayName))
                    {
                        return schemaDisplayName;
                    }
                }

                // Fallback: Try common alias patterns
                var aliasPatterns = new[] { "IntEntitySchemaName_Name", "IntEntitySchemaNameName", "IntEntitySchemaName1" };
                foreach (var alias in aliasPatterns)
                {
                    try
                    {
                        var name = (entity.GetTypedColumnValue<string>(alias) ?? "").Trim();
                        if (!string.IsNullOrEmpty(name))
                        {
                            return name;
                        }
                    }
                    catch { }
                }

                // Fallback: Try reading direct column value (might be string in some versions)
                var entitySchemaNameText = (entity.GetTypedColumnValue<string>("IntEntitySchemaName") ?? "").Trim();
                if (!string.IsNullOrEmpty(entitySchemaNameText))
                {
                    Guid tmp;
                    if (!Guid.TryParse(entitySchemaNameText, out tmp))
                    {
                        return entitySchemaNameText;
                    }
                }
            }
            catch
            {
                // Column doesn't exist or read failed - continue to fallback
            }

            // 2) Fallback: Resolve IntEntitySchemaNameId GUID via SysSchema lookup
            try
            {
                var schemaId = entity.GetTypedColumnValue<Guid>("IntEntitySchemaNameId");
                if (schemaId != Guid.Empty)
                {
                    var schemaEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "SysSchema");
                    schemaEsq.AddColumn("Name");
                    var schemaEntity = schemaEsq.GetEntity(userConnection, schemaId);
                    if (schemaEntity != null)
                    {
                        var schemaName = schemaEntity.GetTypedColumnValue<string>("Name");
                        if (!string.IsNullOrEmpty(schemaName))
                        {
                            return schemaName;
                        }
                    }
                }
            }
            catch
            {
                // SysSchema lookup failed - continue to IntEsq fallback
            }

            // 3) Fallback: parse IntEsq JSON for rootSchemaName
            try
            {
                var intEsq = entity.GetTypedColumnValue<string>("IntEsq");
                if (!string.IsNullOrEmpty(intEsq))
                {
                    var match = Regex.Match(intEsq, "\\\"rootSchemaName\\\"\\s*:\\s*\\\"(?<name>[^\\\"]+)\\\"");
                    if (match.Success)
                    {
                        return match.Groups["name"].Value;
                    }
                }
            }
            catch
            {
                // IntEsq read failed
            }

            return null;
        }

        /// <summary>
        /// Creates a BGReportExecution record to enable proper view filtering.
        /// The BGCommissionReportDataView SQL joins with BGReportExecution to get filter parameters.
        /// </summary>
        private Guid CreateReportExecution(UserConnection userConnection, string reportName, Guid yearMonthId, Guid salesGroupId)
        {
            try
            {
                var schema = userConnection.EntitySchemaManager.GetInstanceByName("BGReportExecution");
                var entity = schema.CreateEntity(userConnection);
                entity.SetDefColumnValues();

                entity.SetColumnValue("BGReportName", reportName);

                // Use lookup column base names (without Id suffix) - Creatio handles the FK relationship
                if (yearMonthId != Guid.Empty)
                {
                    entity.SetColumnValue("BGYearMonth", yearMonthId);
                }

                if (salesGroupId != Guid.Empty)
                {
                    entity.SetColumnValue("BGSalesGroup", salesGroupId);
                }

                // Set current user
                entity.SetColumnValue("BGUserId", userConnection.CurrentUser.Id);

                entity.Save();
                return entity.PrimaryColumnValue;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"CreateReportExecution error: {ex.Message}");
                return Guid.Empty;
            }
        }

        /// <summary>
        /// Builds the FiltersConfig JSON (FilterGroup) based on request parameters.
        /// For Commission reports, filters by BGTransactionDate date range instead of lookup.
        /// </summary>
        private string BuildFiltersConfig(UserConnection userConnection, UsrExcelReportRequest request, string entitySchemaName)
        {
            // Check if ANY filter is present
            bool hasAnyFilter =
                request.YearMonthId != Guid.Empty ||
                request.SalesRepId != Guid.Empty ||
                request.CustomerId != Guid.Empty ||
                !string.IsNullOrEmpty(request.CustomerName) ||
                !string.IsNullOrEmpty(request.StatusName) ||
                request.CreatedFrom.HasValue ||
                request.CreatedTo.HasValue ||
                request.ShippingFrom.HasValue ||
                request.ShippingTo.HasValue ||
                request.DeliveryFrom.HasValue ||
                request.DeliveryTo.HasValue;

            if (!hasAnyFilter)
            {
                return null;
            }

            var items = new List<string>();

            // FLT-004 FIX: For Commission reports, use BGExecutionId + date range filtering.
            // The view has a bug: WHERE filters on qb.BGTransactionDate but SELECT outputs so.BGInvoiceDate.
            // We need BOTH: BGExecutionId (for SalesGroup) AND date range (for actual output date filtering).
            bool usedExecutionIdFilter = false;
            if (entitySchemaName == "BGCommissionReportDataView" && request.YearMonthId != Guid.Empty)
            {
                // Create execution record (needed for SalesGroup filtering in view)
                var executionId = CreateReportExecution(userConnection, "Commission", request.YearMonthId, request.SalesRepId);
                if (executionId != Guid.Empty)
                {
                    items.Add(string.Format(
                        "\"ExecutionFilter\":{0}",
                        BuildFilterJson("BGExecutionId", executionId)
                    ));
                    usedExecutionIdFilter = true;
                }

                // FLT-004: Date range filter on BGTransactionDate disabled - using custom generator instead
                // The IntExcelExport library has issues parsing complex date filters in FiltersConfig
            }
            // FLT-002: IW_Commission - Direct filtering on IWCommissionReportDataView
            // WORKAROUND: IntExcelExport library internally uses IWPayments base table schema for filter application
            // despite IntEsq/IntEntitySchemaName pointing to the view. Use base table column names for filters.
            // NOTE: The library has issues with nested filter groups for dates, so we add separate filters.
            else if (entitySchemaName == "IWCommissionReportDataView")
            {
                // Date filter - Handled by custom generator (GenerateIWCommissionWithDateFilter)
                // IntExcelExport library throws ArgumentNullException with DateTime filters in FiltersConfig.
                // The custom generator in Generate() intercepts IW_Commission + YearMonthId and bypasses the library.
                // This path (BuildFiltersConfig) is only reached for Sales Group-only filtering.

                // Sales Group filter - use IWSalesGroup (lookup column name), not IWSalesGroupId (database column)
                // Creatio entity schema uses Lookup type without "Id" suffix; ESQ resolves to match by Id
                if (request.SalesRepId != Guid.Empty)
                {
                    items.Add(string.Format(
                        "\"SalesGroupFilter\":{0}",
                        BuildFilterJson("IWSalesGroup", request.SalesRepId)
                    ));
                }
            }
            // RPT-003 FIX: View-specific filter column mapping
            // Each view has different columns - only apply filters that exist in the target schema
            // Views without the filter column will throw "Collection item with name X not found"
            //
            // View mappings discovered from ACTION_LOG.md:
            // - BGCommissionReportDataView: Commission (handled above via ExecutionId)
            // - BGSalesByLineView: Sales By Line, Sales By Line With Ranking
            // - BGSalesByItemView: Sales By Item, Items by Customer, Sales By Item By Type Of Customer
            // - BGSalesByCustomerView: Sales By Customer, Sales by Customer Year Comparison, Customers did not buy
            // - BGSalesBySalesGroupView: Sales By Sales Group
            // - BGSalesBySalesRepView: Sales By Sales Rep, Sales Rep Monthly Report
            // - IWCommissionReportDataView: IW_Commission (handled above)
            //
            // BGYearMonth column ONLY exists in BGCommissionReportDataView
            // Other views use BGInvoiceDate or similar - filter mapping TBD
            else if (request.YearMonthId != Guid.Empty)
            {
                // Only IWPayments has IWBGYearMonth - other views don't have Year-Month lookup
                // Commission uses ExecutionId (handled above), IW_Commission uses custom generator
                // All other views: skip Year-Month filter, they'll return all data
                if (entitySchemaName == "IWPayments")
                {
                    items.Add(string.Format(
                        "\"YearMonthFilter\":{0}",
                        BuildFilterJson("IWBGYearMonth.Id", request.YearMonthId)
                    ));
                }
                // TODO: Add date-range filtering for other views if needed (BGInvoiceDate, etc.)
            }

            // Sales Group filter - view-specific column paths
            if (request.SalesRepId != Guid.Empty && !usedExecutionIdFilter && entitySchemaName != "IWCommissionReportDataView")
            {
                string salesGroupColumn = null;

                // Map each view to its Sales Group column path
                switch (entitySchemaName)
                {
                    case "IWPayments":
                        salesGroupColumn = "IWPaymentsInvoice.BGSalesGroup";
                        break;
                    case "BGSalesBySalesGroupView":
                        // This view is already grouped by Sales Group - filter directly
                        salesGroupColumn = "BGSalesGroup";
                        break;
                    case "BGSalesBySalesRepView":
                        // Sales Rep view - filter by rep's group
                        salesGroupColumn = "BGSalesRep.BGSalesGroupLookup";
                        break;
                    case "BGSalesByLineView":
                    case "BGSalesByItemView":
                    case "BGSalesByCustomerView":
                        // These views might have BGSalesGroup via Order or similar path
                        // For now skip to avoid errors - enable after column verification
                        // salesGroupColumn = "BGOrder.BGSalesGroup"; // TBD
                        break;
                    default:
                        // Unknown schema - skip filter to prevent errors
                        break;
                }

                if (!string.IsNullOrEmpty(salesGroupColumn))
                {
                    items.Add(string.Format(
                        "\"SalesGroupFilter\":{0}",
                        BuildFilterJson(salesGroupColumn, request.SalesRepId)
                    ));
                }
            }

            // Customer filter - uses BGCustomer (varchar name) for BGSalesByItemView
            // REQUIRED for "Items by Customer" - view has 4.8M rows, Excel max is 1M
            // Uses CONTAINS (comparisonType 11) for flexible matching - user can type partial name
            if (!string.IsNullOrEmpty(request.CustomerName))
            {
                if (entitySchemaName == "BGSalesByItemView")
                {
                    items.Add(string.Format(
                        "\"CustomerFilter\":{0}",
                        BuildStringContainsFilterJson("BGCustomer", request.CustomerName)
                    ));
                }
            }

            // Date filters for BGSalesByItemView ("Items by Customer" report)
            // Column mappings: CreatedOn, BGShipDate, BGDeliveryDate, BGStatus
            if (entitySchemaName == "BGSalesByItemView")
            {
                // Created From/To filter (CreatedOn column)
                if (request.CreatedFrom.HasValue)
                {
                    items.Add(string.Format(
                        "\"CreatedFromFilter\":{0}",
                        BuildDateGteFilterJson("CreatedOn", request.CreatedFrom.Value)
                    ));
                }
                if (request.CreatedTo.HasValue)
                {
                    items.Add(string.Format(
                        "\"CreatedToFilter\":{0}",
                        BuildDateLteFilterJson("CreatedOn", request.CreatedTo.Value)
                    ));
                }

                // Shipping From/To filter (BGShipDate column)
                if (request.ShippingFrom.HasValue)
                {
                    items.Add(string.Format(
                        "\"ShippingFromFilter\":{0}",
                        BuildDateGteFilterJson("BGShipDate", request.ShippingFrom.Value)
                    ));
                }
                if (request.ShippingTo.HasValue)
                {
                    items.Add(string.Format(
                        "\"ShippingToFilter\":{0}",
                        BuildDateLteFilterJson("BGShipDate", request.ShippingTo.Value)
                    ));
                }

                // Delivery From/To filter (BGDeliveryDate column)
                if (request.DeliveryFrom.HasValue)
                {
                    items.Add(string.Format(
                        "\"DeliveryFromFilter\":{0}",
                        BuildDateGteFilterJson("BGDeliveryDate", request.DeliveryFrom.Value)
                    ));
                }
                if (request.DeliveryTo.HasValue)
                {
                    items.Add(string.Format(
                        "\"DeliveryToFilter\":{0}",
                        BuildDateLteFilterJson("BGDeliveryDate", request.DeliveryTo.Value)
                    ));
                }

                // Status filter (BGStatus varchar column)
                if (!string.IsNullOrEmpty(request.StatusName))
                {
                    items.Add(string.Format(
                        "\"StatusFilter\":{0}",
                        BuildStringFilterJson("BGStatus", request.StatusName)
                    ));
                }
            }

            if (items.Count == 0)
            {
                return null;
            }

            return "{\"filterType\":6,\"isEnabled\":true,\"logicalOperation\":0,\"items\":{" + string.Join(",", items) + "}}";
        }

        #region Custom Excel Generator (FLT-004 fix)

        /// <summary>
        /// Parses Year-Month name (e.g., "2024-12") into start/end date range.
        /// </summary>
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

        /// <summary>
        /// Gets the template Excel file bytes from IntExcelReport.IntFile.
        /// </summary>
        private byte[] GetTemplateFile(UserConnection userConnection, Guid reportId)
        {
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            var fileCol = esq.AddColumn("IntFile");
            var entity = esq.GetEntity(userConnection, reportId);
            if (entity == null) return null;
            return entity.GetBytesValue(fileCol.Name);
        }

        /// <summary>
        /// Gets the sheet name from IntExcelReport.IntSheetName.
        /// </summary>
        private string GetSheetName(UserConnection userConnection, Guid reportId)
        {
            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            esq.AddColumn("IntSheetName");
            var entity = esq.GetEntity(userConnection, reportId);
            if (entity == null) return "Data";
            return entity.GetTypedColumnValue<string>("IntSheetName") ?? "Data";
        }

        /// <summary>
        /// Queries Commission data using date-based filtering (bypasses NULL BGYearMonth lookup).
        /// Returns list of dictionaries with column values.
        /// </summary>
        private List<Dictionary<string, object>> QueryCommissionData(
            UserConnection userConnection,
            DateTime startDate,
            DateTime endDate,
            Guid salesGroupId)
        {
            var results = new List<Dictionary<string, object>>();

            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGCommissionReportDataView");
            esq.PrimaryQueryColumn.IsAlwaysSelect = true;

            // Add columns matching the report template
            var colSalesRep = esq.AddColumn("BGSalesRep");
            var colDescription = esq.AddColumn("BGDescription");
            var colTransactionDate = esq.AddColumn("BGTransactionDate");
            var colCommission = esq.AddColumn("BGCommission");
            var colAmount = esq.AddColumn("BGAmount");
            var colCommissionRate = esq.AddColumn("BGCommissionRatePercentage");
            var colCustomer = esq.AddColumn("BGOrder.Account");
            var colInvoiceDate = esq.AddColumn("BGOrder.BGInvoiceDate");
            var colPONumber = esq.AddColumn("BGPONumber");
            var colTransactionType = esq.AddColumn("BGTransactionType");
            var colIsNote = esq.AddColumn("BGIsNote");
            var colSalesGroup = esq.AddColumn("BGSalesRep.BGSalesGroupLookup");

            // Apply date filter (Year-Month range)
            esq.Filters.Add(esq.CreateFilterWithParameters(
                FilterComparisonType.GreaterOrEqual, "BGTransactionDate", startDate));
            esq.Filters.Add(esq.CreateFilterWithParameters(
                FilterComparisonType.Less, "BGTransactionDate", endDate));

            // Apply Sales Group filter if specified
            if (salesGroupId != Guid.Empty)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Equal, "BGSalesRep.BGSalesGroupLookup", salesGroupId));
            }

            var collection = esq.GetEntityCollection(userConnection);

            foreach (var entity in collection)
            {
                var row = new Dictionary<string, object>();

                // Extract values - handle lookups by getting display values
                row["SalesRep"] = GetLookupDisplayValue(entity, colSalesRep.Name);
                row["Description"] = entity.GetTypedColumnValue<string>(colDescription.Name) ?? "";
                row["TransactionDate"] = entity.GetTypedColumnValue<DateTime>(colTransactionDate.Name);
                row["Commission"] = entity.GetTypedColumnValue<decimal>(colCommission.Name);
                row["Amount"] = entity.GetTypedColumnValue<decimal>(colAmount.Name);
                row["CommissionRate"] = entity.GetTypedColumnValue<decimal>(colCommissionRate.Name);
                row["Customer"] = GetLookupDisplayValue(entity, colCustomer.Name);
                row["InvoiceDate"] = entity.GetTypedColumnValue<DateTime>(colInvoiceDate.Name);
                row["PONumber"] = entity.GetTypedColumnValue<string>(colPONumber.Name) ?? "";
                row["TransactionType"] = GetLookupDisplayValue(entity, colTransactionType.Name);
                row["IsNote"] = entity.GetTypedColumnValue<bool>(colIsNote.Name);
                row["SalesGroup"] = GetLookupDisplayValue(entity, colSalesGroup.Name);

                results.Add(row);
            }

            return results;
        }

        /// <summary>
        /// Queries IW Commission data using date-based filtering (bypasses IntExcelExport library limitation).
        /// Returns list of dictionaries with column values matching the report template.
        /// </summary>
        private List<Dictionary<string, object>> QueryIWCommissionData(
            UserConnection userConnection,
            DateTime startDate,
            DateTime endDate,
            Guid salesGroupId)
        {
            var results = new List<Dictionary<string, object>>();

            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IWCommissionReportDataView");
            esq.PrimaryQueryColumn.IsAlwaysSelect = true;

            // Add columns - use Lookup paths for related entities (entity schema has Lookup columns, not text)
            // IWSalesGroup is a Lookup to BGSalesGroup - get the BGName via lookup path
            var colSalesGroupName = esq.AddColumn("IWSalesGroup.BGName");
            // IWAccount is a Lookup to Account - get the Name via lookup path
            var colAccountName = esq.AddColumn("IWAccount.Name");
            var colAmount = esq.AddColumn("IWAmount");
            var colCommission = esq.AddColumn("IWCommissionAmount");
            var colTransactionDate = esq.AddColumn("IWTransactionDate");
            var colDescription = esq.AddColumn("IWDescription");
            // IWPaymentsInvoice is a Lookup to Order - get the Number via lookup path
            var colOrderNumber = esq.AddColumn("IWPaymentsInvoice.Number");
            var colQBInvoiceNumber = esq.AddColumn("IWQBInvoiceNumber");

            // Apply date filter (Year-Month range) on IWTransactionDate (view column, aliased from IWPaymentDue)
            esq.Filters.Add(esq.CreateFilterWithParameters(
                FilterComparisonType.GreaterOrEqual, "IWTransactionDate", startDate));
            esq.Filters.Add(esq.CreateFilterWithParameters(
                FilterComparisonType.Less, "IWTransactionDate", endDate));

            // Apply Sales Group filter if specified (lookup column without "Id" suffix)
            if (salesGroupId != Guid.Empty)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Equal, "IWSalesGroup", salesGroupId));
            }

            var collection = esq.GetEntityCollection(userConnection);

            foreach (var entity in collection)
            {
                var row = new Dictionary<string, object>();

                // Extract values matching template column names
                row["Sales Group Name"] = entity.GetTypedColumnValue<string>(colSalesGroupName.Name) ?? "";
                row["Account Name"] = entity.GetTypedColumnValue<string>(colAccountName.Name) ?? "";
                row["Amount"] = entity.GetTypedColumnValue<decimal>(colAmount.Name);
                row["Commission"] = entity.GetTypedColumnValue<decimal>(colCommission.Name);
                row["Transaction Date"] = entity.GetTypedColumnValue<DateTime>(colTransactionDate.Name);
                row["Description"] = entity.GetTypedColumnValue<string>(colDescription.Name) ?? "";
                row["Order Number"] = entity.GetTypedColumnValue<string>(colOrderNumber.Name) ?? "";
                row["QB Invoice Number"] = entity.GetTypedColumnValue<string>(colQBInvoiceNumber.Name) ?? "";

                results.Add(row);
            }

            return results;
        }

        private string GetLookupDisplayValue(Entity entity, string columnName)
        {
            try
            {
                // Try to get the display value for lookup columns
                var value = entity.GetColumnValue(columnName);
                if (value == null) return "";

                // If it's a Guid, try to get the Name column
                if (value is Guid)
                {
                    var nameCol = columnName + "Name";
                    try
                    {
                        return entity.GetTypedColumnValue<string>(nameCol) ?? "";
                    }
                    catch
                    {
                        return value.ToString();
                    }
                }
                return value.ToString();
            }
            catch
            {
                return "";
            }
        }

        /// <summary>
        /// Populates an Excel template with data using available Excel libraries.
        /// Falls back to returning template with data count if no library works.
        /// </summary>
        private byte[] PopulateExcelTemplate(byte[] templateBytes, List<Dictionary<string, object>> data, string sheetName)
        {
            // Try ClosedXML first (simpler API)
            try
            {
                Type xlWorkbookType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    xlWorkbookType = assembly.GetType("ClosedXML.Excel.XLWorkbook");
                    if (xlWorkbookType != null) break;
                }

                if (xlWorkbookType != null)
                {
                    return PopulateWithClosedXml(templateBytes, data, sheetName, xlWorkbookType);
                }
            }
            catch
            {
                // ClosedXML failed, continue to fallback
            }

            // Try DocumentFormat.OpenXml (Microsoft OpenXML SDK)
            try
            {
                Type spreadsheetDocType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    spreadsheetDocType = assembly.GetType("DocumentFormat.OpenXml.Packaging.SpreadsheetDocument");
                    if (spreadsheetDocType != null) break;
                }

                if (spreadsheetDocType != null)
                {
                    return PopulateWithOpenXmlSdk(templateBytes, data, sheetName, spreadsheetDocType);
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"OpenXML SDK failed: {ex.Message}");
            }

            // Fallback: Use ZIP-based approach (xlsx/xlsm are ZIP archives with XML)
            string lastError = "none";
            try
            {
                return PopulateWithZipXml(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                // Unwrap TargetInvocationException to get the real error
                var innerEx = ex.InnerException ?? ex;
                lastError = innerEx.Message;
                if (innerEx != ex)
                {
                    lastError = $"{ex.Message} -> {innerEx.Message}";
                }
                System.Diagnostics.Debug.WriteLine($"ZIP-based approach failed: {lastError}");
            }

            // Last resort: Return template as-is with error info appended
            // Store error in a static field so it can be retrieved by GenerateIWCommissionWithDateFilter
            _lastPopulateError = lastError;
            System.Diagnostics.Debug.WriteLine($"All Excel methods failed, returning template with {data.Count} rows queried");
            return templateBytes;
        }

        /// <summary>
        /// Populates Excel using direct ZIP/XML manipulation via reflection.
        /// xlsx/xlsm files are ZIP archives containing XML files.
        /// Uses reflection to load System.IO.Compression assembly dynamically.
        /// </summary>
        private byte[] PopulateWithZipXml(byte[] templateBytes, List<Dictionary<string, object>> data, string sheetName)
        {
            // Try to load System.IO.Compression via reflection
            Assembly compressionAssembly = null;
            Type zipArchiveType = null;
            Type zipArchiveModeType = null;

            // Try different assembly loading approaches
            string[] assemblyNames = new[]
            {
                "System.IO.Compression, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
                "System.IO.Compression, Version=4.2.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
                "System.IO.Compression"
            };

            foreach (var assemblyName in assemblyNames)
            {
                try
                {
                    compressionAssembly = Assembly.Load(assemblyName);
                    if (compressionAssembly != null)
                    {
                        zipArchiveType = compressionAssembly.GetType("System.IO.Compression.ZipArchive");
                        zipArchiveModeType = compressionAssembly.GetType("System.IO.Compression.ZipArchiveMode");
                        if (zipArchiveType != null && zipArchiveModeType != null)
                        {
                            break;
                        }
                    }
                }
                catch
                {
                    // Continue to next assembly name
                }
            }

            // Also check already loaded assemblies
            if (zipArchiveType == null)
            {
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    zipArchiveType = assembly.GetType("System.IO.Compression.ZipArchive");
                    if (zipArchiveType != null)
                    {
                        zipArchiveModeType = assembly.GetType("System.IO.Compression.ZipArchiveMode");
                        break;
                    }
                }
            }

            if (zipArchiveType == null || zipArchiveModeType == null)
            {
                throw new Exception("System.IO.Compression.ZipArchive not available");
            }

            // Get ZipArchiveMode.Update enum value (Read=0, Create=1, Update=2)
            var updateMode = Enum.ToObject(zipArchiveModeType, 2);

            using (var memoryStream = new MemoryStream())
            {
                memoryStream.Write(templateBytes, 0, templateBytes.Length);
                memoryStream.Position = 0;

                // ZipArchive(Stream stream, ZipArchiveMode mode, bool leaveOpen)
                var ctor = zipArchiveType.GetConstructor(new[] { typeof(Stream), zipArchiveModeType, typeof(bool) });
                if (ctor == null)
                {
                    throw new Exception("ZipArchive constructor not found");
                }

                var archive = ctor.Invoke(new object[] { memoryStream, updateMode, true }) as IDisposable;
                if (archive == null)
                {
                    throw new Exception("Failed to create ZipArchive");
                }

                using (archive)
                {
                    // GetEntry(string entryName)
                    var getEntryMethod = zipArchiveType.GetMethod("GetEntry", new[] { typeof(string) });

                    // Find the correct sheet file based on sheetName
                    // 1. Read workbook.xml to find sheet's rId
                    // 2. Read workbook.xml.rels to map rId to file path
                    string sheetFilePath = "xl/worksheets/sheet1.xml";  // Default fallback

                    try
                    {
                        // Read workbook.xml to find sheet by name
                        var workbookEntry = getEntryMethod.Invoke(archive, new object[] { "xl/workbook.xml" });
                        if (workbookEntry != null)
                        {
                            var wbOpenMethod = workbookEntry.GetType().GetMethod("Open");
                            string workbookXml;
                            using (var wbStream = wbOpenMethod.Invoke(workbookEntry, null) as Stream)
                            using (var wbReader = new StreamReader(wbStream))
                            {
                                workbookXml = wbReader.ReadToEnd();
                            }

                            var wbDoc = new XmlDocument();
                            wbDoc.LoadXml(workbookXml);
                            var wbNsmgr = new XmlNamespaceManager(wbDoc.NameTable);
                            wbNsmgr.AddNamespace("x", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
                            wbNsmgr.AddNamespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships");

                            // Find sheet element by name (case-insensitive)
                            var sheetsNode = wbDoc.SelectNodes("//x:sheet", wbNsmgr);
                            string sheetRid = null;
                            foreach (XmlNode sheet in sheetsNode)
                            {
                                var nameAttr = sheet.Attributes["name"];
                                if (nameAttr != null && nameAttr.Value.Equals(sheetName, StringComparison.OrdinalIgnoreCase))
                                {
                                    var ridAttr = sheet.Attributes["r:id"];
                                    if (ridAttr != null)
                                    {
                                        sheetRid = ridAttr.Value;
                                        break;
                                    }
                                }
                            }

                            // Read relationships file to map rId to file path
                            if (!string.IsNullOrEmpty(sheetRid))
                            {
                                var relsEntry = getEntryMethod.Invoke(archive, new object[] { "xl/_rels/workbook.xml.rels" });
                                if (relsEntry != null)
                                {
                                    var relsOpenMethod = relsEntry.GetType().GetMethod("Open");
                                    string relsXml;
                                    using (var relsStream = relsOpenMethod.Invoke(relsEntry, null) as Stream)
                                    using (var relsReader = new StreamReader(relsStream))
                                    {
                                        relsXml = relsReader.ReadToEnd();
                                    }

                                    var relsDoc = new XmlDocument();
                                    relsDoc.LoadXml(relsXml);
                                    var relsNsmgr = new XmlNamespaceManager(relsDoc.NameTable);
                                    relsNsmgr.AddNamespace("r", "http://schemas.openxmlformats.org/package/2006/relationships");

                                    var relNodes = relsDoc.SelectNodes("//r:Relationship", relsNsmgr);
                                    foreach (XmlNode rel in relNodes)
                                    {
                                        var idAttr = rel.Attributes["Id"];
                                        if (idAttr != null && idAttr.Value == sheetRid)
                                        {
                                            var targetAttr = rel.Attributes["Target"];
                                            if (targetAttr != null)
                                            {
                                                // Target is relative to xl/ folder, e.g. "worksheets/sheet2.xml"
                                                sheetFilePath = "xl/" + targetAttr.Value;
                                                break;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    catch
                    {
                        // If sheet lookup fails, fall back to sheet1.xml
                        sheetFilePath = "xl/worksheets/sheet1.xml";
                    }

                    var sheetEntry = getEntryMethod.Invoke(archive, new object[] { sheetFilePath });

                    if (sheetEntry == null)
                    {
                        throw new Exception($"{sheetFilePath} not found in archive (looking for sheet '{sheetName}')");
                    }

                    var entryType = sheetEntry.GetType();

                    // Read existing content: entry.Open() returns Stream
                    var openMethod = entryType.GetMethod("Open");
                    string sheetXml;
                    using (var entryStream = openMethod.Invoke(sheetEntry, null) as Stream)
                    using (var reader = new StreamReader(entryStream))
                    {
                        sheetXml = reader.ReadToEnd();
                    }

                    // Modify the XML to add data rows
                    var modifiedXml = UpdateSheetWithData(sheetXml, data);

                    // Delete entry: entry.Delete()
                    var deleteMethod = entryType.GetMethod("Delete");
                    deleteMethod.Invoke(sheetEntry, null);

                    // Create new entry: archive.CreateEntry(string entryName)
                    var createEntryMethod = zipArchiveType.GetMethod("CreateEntry", new[] { typeof(string) });
                    var newEntry = createEntryMethod.Invoke(archive, new object[] { sheetFilePath });

                    // Write modified content
                    var newOpenMethod = newEntry.GetType().GetMethod("Open");
                    using (var newStream = newOpenMethod.Invoke(newEntry, null) as Stream)
                    using (var writer = new StreamWriter(newStream))
                    {
                        writer.Write(modifiedXml);
                    }
                }

                return memoryStream.ToArray();
            }
        }

        private byte[] PopulateWithClosedXml(byte[] templateBytes, List<Dictionary<string, object>> data, string sheetName, Type xlWorkbookType)
        {
            using (var inputStream = new MemoryStream(templateBytes))
            {
                // XLWorkbook(Stream stream)
                var ctor = xlWorkbookType.GetConstructor(new[] { typeof(Stream) });
                if (ctor == null)
                {
                    throw new Exception("XLWorkbook(Stream) constructor not found");
                }

                var workbook = ctor.Invoke(new object[] { inputStream }) as IDisposable;
                if (workbook == null)
                {
                    throw new Exception("Failed to create XLWorkbook");
                }

                using (workbook)
                {
                    // Get worksheet
                    var worksheetProp = xlWorkbookType.GetProperty("Worksheet");
                    var worksheetMethod = xlWorkbookType.GetMethod("Worksheet", new[] { typeof(string) });

                    object worksheet = null;
                    if (worksheetMethod != null)
                    {
                        worksheet = worksheetMethod.Invoke(workbook, new object[] { sheetName });
                    }

                    if (worksheet == null)
                    {
                        throw new Exception($"Worksheet '{sheetName}' not found");
                    }

                    // Get column order from data keys (preserves insertion order from Dictionary)
                    // This makes the function work for both Commission and IW_Commission
                    string[] columnOrder;
                    if (data.Count > 0)
                    {
                        columnOrder = data[0].Keys.ToArray();
                    }
                    else
                    {
                        columnOrder = new string[0];
                    }

                    // Add data rows starting at row 2 (row 1 is header)
                    int rowIndex = 2;
                    var cellMethod = worksheet.GetType().GetMethod("Cell", new[] { typeof(int), typeof(int) });

                    foreach (var dataRow in data)
                    {
                        int colIndex = 1;
                        foreach (var colName in columnOrder)
                        {
                            if (dataRow.ContainsKey(colName) && cellMethod != null)
                            {
                                var cell = cellMethod.Invoke(worksheet, new object[] { rowIndex, colIndex });
                                if (cell != null)
                                {
                                    var valueProp = cell.GetType().GetProperty("Value");
                                    if (valueProp != null)
                                    {
                                        valueProp.SetValue(cell, dataRow[colName]);
                                    }
                                }
                            }
                            colIndex++;
                        }
                        rowIndex++;
                    }

                    // Save to stream
                    using (var outputStream = new MemoryStream())
                    {
                        var saveAsMethod = xlWorkbookType.GetMethod("SaveAs", new[] { typeof(Stream) });
                        if (saveAsMethod != null)
                        {
                            saveAsMethod.Invoke(workbook, new object[] { outputStream });
                            return outputStream.ToArray();
                        }
                    }
                }
            }

            throw new Exception("Failed to save workbook");
        }

        /// <summary>
        /// Populates Excel using DocumentFormat.OpenXml SDK via reflection.
        /// </summary>
        private byte[] PopulateWithOpenXmlSdk(byte[] templateBytes, List<Dictionary<string, object>> data, string sheetName, Type spreadsheetDocType)
        {
            using (var stream = new MemoryStream())
            {
                stream.Write(templateBytes, 0, templateBytes.Length);
                stream.Position = 0;

                // SpreadsheetDocument.Open(stream, true)
                var openMethod = spreadsheetDocType.GetMethod("Open", new[] { typeof(Stream), typeof(bool) });
                if (openMethod == null)
                {
                    throw new Exception("SpreadsheetDocument.Open method not found");
                }

                using (var doc = openMethod.Invoke(null, new object[] { stream, true }) as IDisposable)
                {
                    if (doc == null)
                    {
                        throw new Exception("Failed to open SpreadsheetDocument");
                    }

                    // Get WorkbookPart
                    var workbookPartProp = spreadsheetDocType.GetProperty("WorkbookPart");
                    var workbookPart = workbookPartProp?.GetValue(doc);
                    if (workbookPart == null)
                    {
                        throw new Exception("WorkbookPart not found");
                    }

                    // Get first WorksheetPart
                    var worksheetPartsProp = workbookPart.GetType().GetProperty("WorksheetParts");
                    var worksheetParts = worksheetPartsProp?.GetValue(workbookPart) as System.Collections.IEnumerable;
                    object worksheetPart = null;
                    foreach (var wp in worksheetParts)
                    {
                        worksheetPart = wp;
                        break;
                    }

                    if (worksheetPart == null)
                    {
                        throw new Exception("WorksheetPart not found");
                    }

                    // Get Worksheet
                    var worksheetProp = worksheetPart.GetType().GetProperty("Worksheet");
                    var worksheet = worksheetProp?.GetValue(worksheetPart);
                    if (worksheet == null)
                    {
                        throw new Exception("Worksheet not found");
                    }

                    // Get SheetData
                    var getFirstChildMethod = worksheet.GetType().GetMethod("GetFirstChild");
                    if (getFirstChildMethod == null)
                    {
                        throw new Exception("GetFirstChild method not found");
                    }

                    // Find SheetData type
                    Type sheetDataType = null;
                    foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        sheetDataType = asm.GetType("DocumentFormat.OpenXml.Spreadsheet.SheetData");
                        if (sheetDataType != null) break;
                    }

                    if (sheetDataType == null)
                    {
                        throw new Exception("SheetData type not found");
                    }

                    var genericGetFirstChild = getFirstChildMethod.MakeGenericMethod(sheetDataType);
                    var sheetData = genericGetFirstChild.Invoke(worksheet, null);

                    if (sheetData == null)
                    {
                        throw new Exception("SheetData not found");
                    }

                    // Find Row and Cell types
                    Type rowType = null, cellType = null, cellValueType = null;
                    foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        if (rowType == null) rowType = asm.GetType("DocumentFormat.OpenXml.Spreadsheet.Row");
                        if (cellType == null) cellType = asm.GetType("DocumentFormat.OpenXml.Spreadsheet.Cell");
                        if (cellValueType == null) cellValueType = asm.GetType("DocumentFormat.OpenXml.Spreadsheet.CellValue");
                        if (rowType != null && cellType != null && cellValueType != null) break;
                    }

                    if (rowType == null || cellType == null || cellValueType == null)
                    {
                        throw new Exception("Row/Cell types not found");
                    }

                    // Get column order from data keys (dynamic - works for all report types)
                    string[] columnOrder;
                    if (data.Count > 0)
                    {
                        columnOrder = data[0].Keys.ToArray();
                    }
                    else
                    {
                        columnOrder = new string[0];
                    }

                    // Add data rows starting at row 2
                    var appendMethod = sheetData.GetType().GetMethod("Append", new[] { typeof(object[]) });
                    int rowIndex = 2;

                    foreach (var dataRow in data)
                    {
                        var row = Activator.CreateInstance(rowType);
                        var rowIndexProp = rowType.GetProperty("RowIndex");
                        rowIndexProp?.SetValue(row, (uint)rowIndex);

                        int colIndex = 0;
                        foreach (var colName in columnOrder)
                        {
                            var cell = Activator.CreateInstance(cellType);
                            var cellRefProp = cellType.GetProperty("CellReference");
                            cellRefProp?.SetValue(cell, GetCellReference(colIndex, rowIndex));

                            if (dataRow.ContainsKey(colName) && dataRow[colName] != null)
                            {
                                var cellValue = Activator.CreateInstance(cellValueType);
                                var textProp = cellValueType.GetProperty("Text");
                                textProp?.SetValue(cellValue, dataRow[colName].ToString());

                                var appendCellMethod = cell.GetType().GetMethod("Append", new[] { typeof(object[]) });
                                appendCellMethod?.Invoke(cell, new object[] { new[] { cellValue } });
                            }

                            var appendRowMethod = row.GetType().GetMethod("Append", new[] { typeof(object[]) });
                            appendRowMethod?.Invoke(row, new object[] { new[] { cell } });
                            colIndex++;
                        }

                        appendMethod?.Invoke(sheetData, new object[] { new[] { row } });
                        rowIndex++;
                    }

                    // Save
                    var saveMethod = worksheet.GetType().GetMethod("Save");
                    saveMethod?.Invoke(worksheet, null);
                }

                return stream.ToArray();
            }
        }

        private string UpdateSheetWithData(string sheetXml, List<Dictionary<string, object>> data)
        {
            if (data == null || data.Count == 0)
            {
                return sheetXml;
            }

            // Parse the XML
            var doc = new XmlDocument();
            doc.LoadXml(sheetXml);

            var nsmgr = new XmlNamespaceManager(doc.NameTable);
            nsmgr.AddNamespace("x", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");

            var sheetDataNode = doc.SelectSingleNode("//x:sheetData", nsmgr);
            if (sheetDataNode == null)
            {
                return sheetXml;
            }

            // Get column order from data keys (dynamic - works for all report types)
            string[] columnOrder;
            if (data.Count > 0)
            {
                columnOrder = data[0].Keys.ToArray();
            }
            else
            {
                return sheetXml;
            }

            // Remove ALL existing rows including row 1 (we'll write our own headers)
            var rowsToRemove = new List<XmlNode>();
            foreach (XmlNode row in sheetDataNode.SelectNodes("x:row", nsmgr))
            {
                rowsToRemove.Add(row);
            }
            foreach (var row in rowsToRemove)
            {
                sheetDataNode.RemoveChild(row);
            }

            // Write header row (row 1) with column names that VBA expects
            var headerRow = doc.CreateElement("row", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
            headerRow.SetAttribute("r", "1");
            int headerColIndex = 0;
            foreach (var colName in columnOrder)
            {
                var cellRef = GetCellReference(headerColIndex, 1);
                var cellElement = doc.CreateElement("c", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
                cellElement.SetAttribute("r", cellRef);
                cellElement.SetAttribute("t", "str");
                var valueElement = doc.CreateElement("v", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
                valueElement.InnerText = colName;  // Column name as header
                cellElement.AppendChild(valueElement);
                headerRow.AppendChild(cellElement);
                headerColIndex++;
            }
            sheetDataNode.AppendChild(headerRow);

            // Add data rows starting at row 2
            int currentRow = 2;
            foreach (var dataRow in data)
            {
                var rowElement = doc.CreateElement("row", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
                rowElement.SetAttribute("r", currentRow.ToString());

                int colIndex = 0;
                foreach (var colName in columnOrder)
                {
                    if (!dataRow.ContainsKey(colName))
                    {
                        colIndex++;
                        continue;
                    }

                    var value = dataRow[colName];
                    var cellRef = GetCellReference(colIndex, currentRow);

                    var cellElement = doc.CreateElement("c", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");
                    cellElement.SetAttribute("r", cellRef);

                    var valueElement = doc.CreateElement("v", "http://schemas.openxmlformats.org/spreadsheetml/2006/main");

                    if (value is decimal || value is double || value is int || value is float)
                    {
                        // Numeric value
                        valueElement.InnerText = Convert.ToDouble(value).ToString(System.Globalization.CultureInfo.InvariantCulture);
                    }
                    else if (value is DateTime dt)
                    {
                        // Excel date serial number - skip null/MinValue dates to prevent VBA Type mismatch
                        if (dt > DateTime.MinValue)
                        {
                            var oaDate = dt.ToOADate();
                            valueElement.InnerText = oaDate.ToString(System.Globalization.CultureInfo.InvariantCulture);
                        }
                        else
                        {
                            // Don't write empty dates - leave cell blank rather than writing invalid value
                            colIndex++;
                            continue;
                        }
                    }
                    else if (value is bool b)
                    {
                        cellElement.SetAttribute("t", "b");
                        valueElement.InnerText = b ? "1" : "0";
                    }
                    else
                    {
                        // String value - use simple string type (t="str") with <v> element
                        // This is simpler and more compatible than inlineStr with <is><t>
                        var strValue = value?.ToString() ?? "";
                        if (!string.IsNullOrEmpty(strValue))
                        {
                            cellElement.SetAttribute("t", "str");
                            valueElement.InnerText = strValue;
                        }
                        else
                        {
                            // Empty string - skip cell
                            colIndex++;
                            continue;
                        }
                    }

                    cellElement.AppendChild(valueElement);
                    rowElement.AppendChild(cellElement);
                    colIndex++;
                }

                sheetDataNode.AppendChild(rowElement);
                currentRow++;
            }

            return doc.OuterXml;
        }

        private string GetCellReference(int colIndex, int rowIndex)
        {
            string colRef = "";
            int col = colIndex;
            while (col >= 0)
            {
                colRef = (char)('A' + (col % 26)) + colRef;
                col = col / 26 - 1;
            }
            return colRef + rowIndex;
        }

        /// <summary>
        /// Generates Commission report with custom date-based filtering.
        /// Bypasses IntExcelExport library limitations with date filters.
        /// </summary>
        private UsrExcelReportResponse GenerateWithDateFilter(
            UserConnection userConnection,
            UsrExcelReportRequest request,
            string yearMonthName)
        {
            DateTime startDate, endDate;
            if (!ParseYearMonth(yearMonthName, out startDate, out endDate))
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Invalid Year-Month format: " + yearMonthName
                };
            }

            // Get template file
            var templateBytes = GetTemplateFile(userConnection, request.ReportId);
            if (templateBytes == null || templateBytes.Length == 0)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Template file not found"
                };
            }

            // Get sheet name
            var sheetName = GetSheetName(userConnection, request.ReportId);

            // Query data with date-based filtering
            var data = QueryCommissionData(userConnection, startDate, endDate, request.SalesRepId);

            // Populate Excel template
            byte[] populatedBytes;
            try
            {
                populatedBytes = PopulateExcelTemplate(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Excel population failed: " + ex.Message
                };
            }

            // Cache the result
            var cacheKey = "ExportFilterKey_" + Guid.NewGuid().ToString("N");
            userConnection.SessionData[cacheKey] = populatedBytes;

            return new UsrExcelReportResponse
            {
                success = true,
                key = cacheKey,
                message = $"Custom report generated with {data.Count} rows (Year-Month: {yearMonthName})"
            };
        }

        /// <summary>
        /// Generates Commission report without date filtering (all time data).
        /// Used when no Year-Month filter is specified.
        /// Bypasses library fallback to ensure bytes are stored in SessionData for download.
        /// </summary>
        private UsrExcelReportResponse GenerateWithDateFilterAllTime(
            UserConnection userConnection,
            UsrExcelReportRequest request)
        {
            // Get template file
            var templateBytes = GetTemplateFile(userConnection, request.ReportId);
            if (templateBytes == null || templateBytes.Length == 0)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Template file not found"
                };
            }

            // Get sheet name
            var sheetName = GetSheetName(userConnection, request.ReportId);

            // Query all commission data (last 24 months to avoid massive datasets)
            var startDate = DateTime.UtcNow.AddMonths(-24);
            var endDate = DateTime.UtcNow.AddDays(1);
            var data = QueryCommissionData(userConnection, startDate, endDate, request.SalesRepId);

            // Populate Excel template
            byte[] populatedBytes;
            try
            {
                populatedBytes = PopulateExcelTemplate(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Excel population failed: " + ex.Message
                };
            }

            // Cache the result - THIS IS THE KEY FIX
            // Library fallback doesn't do this, causing GetReport to return 404
            var cacheKey = "ExportFilterKey_" + Guid.NewGuid().ToString("N");
            userConnection.SessionData[cacheKey] = populatedBytes;

            return new UsrExcelReportResponse
            {
                success = true,
                key = cacheKey,
                message = $"Custom report generated with {data.Count} rows (all time, last 24 months)"
            };
        }

        /// <summary>
        /// Generates IW_Commission report with custom date-based filtering.
        /// Bypasses IntExcelExport library limitations with date filters (ArgumentNullException).
        /// </summary>
        private UsrExcelReportResponse GenerateIWCommissionWithDateFilter(
            UserConnection userConnection,
            UsrExcelReportRequest request,
            string yearMonthName)
        {
            DateTime startDate, endDate;
            if (!ParseYearMonth(yearMonthName, out startDate, out endDate))
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Invalid Year-Month format: " + yearMonthName
                };
            }

            // Get template file
            var templateBytes = GetTemplateFile(userConnection, request.ReportId);
            if (templateBytes == null || templateBytes.Length == 0)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Template file not found for IW_Commission"
                };
            }

            // Get sheet name
            var sheetName = GetSheetName(userConnection, request.ReportId);

            // Query data with date-based filtering using custom ESQ (bypasses library limitation)
            var data = QueryIWCommissionData(userConnection, startDate, endDate, request.SalesRepId);

            // Populate Excel template
            byte[] populatedBytes;
            try
            {
                populatedBytes = PopulateExcelTemplate(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Excel population failed for IW_Commission: " + ex.Message
                };
            }

            // Cache the result
            var cacheKey = "ExportFilterKey_" + Guid.NewGuid().ToString("N");
            userConnection.SessionData[cacheKey] = populatedBytes;

            // Include debug info about template vs populated size and any errors
            var sizeInfo = $"template={templateBytes.Length}, output={populatedBytes.Length}";
            var errorInfo = string.IsNullOrEmpty(_lastPopulateError) ? "" : $", err={_lastPopulateError}";
            _lastPopulateError = null; // Clear for next call

            return new UsrExcelReportResponse
            {
                success = true,
                key = cacheKey,
                message = $"IW_Commission: {data.Count} rows, {yearMonthName}, {sizeInfo}{errorInfo}"
            };
        }

        /// <summary>
        /// Custom generator for "Items by Customer" (BGSalesByItemView).
        /// IntExcelExport library doesn't properly apply FiltersConfig, so we build ESQ directly.
        /// </summary>
        private UsrExcelReportResponse GenerateSalesByItemWithFilters(
            UserConnection userConnection,
            UsrExcelReportRequest request)
        {
            // Get template file
            var templateBytes = GetTemplateFile(userConnection, request.ReportId);
            if (templateBytes == null || templateBytes.Length == 0)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Template file not found for Items by Customer"
                };
            }

            // Get sheet name
            var sheetName = GetSheetName(userConnection, request.ReportId);

            // Query data with proper filters
            List<Dictionary<string, object>> data;
            try
            {
                data = QuerySalesByItemData(userConnection, request);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Query error: " + ex.Message
                };
            }

            if (data.Count == 0)
            {
                // Build diagnostic info
                var filters = new List<string>();
                filters.Add("Customer=" + (request.CustomerName ?? "null"));
                if (request.CreatedFrom.HasValue) filters.Add("CreatedFrom=" + request.CreatedFrom.Value.ToString("yyyy-MM-dd"));
                if (request.CreatedTo.HasValue) filters.Add("CreatedTo=" + request.CreatedTo.Value.ToString("yyyy-MM-dd"));
                if (request.ShippingFrom.HasValue) filters.Add("ShipFrom=" + request.ShippingFrom.Value.ToString("yyyy-MM-dd"));
                if (request.ShippingTo.HasValue) filters.Add("ShipTo=" + request.ShippingTo.Value.ToString("yyyy-MM-dd"));
                if (request.DeliveryFrom.HasValue) filters.Add("DelFrom=" + request.DeliveryFrom.Value.ToString("yyyy-MM-dd"));
                if (request.DeliveryTo.HasValue) filters.Add("DelTo=" + request.DeliveryTo.Value.ToString("yyyy-MM-dd"));
                if (!string.IsNullOrEmpty(request.StatusName)) filters.Add("Status=" + request.StatusName);

                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "No data found. Filters: " + string.Join(", ", filters)
                };
            }

            // Check row limit (Excel max ~1M rows)
            if (data.Count > 1000000)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = $"Too many rows ({data.Count}). Please add more filters to reduce the data set."
                };
            }

            // Populate Excel template
            byte[] populatedBytes;
            try
            {
                populatedBytes = PopulateExcelTemplate(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Excel population failed: " + ex.Message
                };
            }

            // Cache the result
            var cacheKey = "ExportFilterKey_" + Guid.NewGuid().ToString("N");
            userConnection.SessionData[cacheKey] = populatedBytes;

            // Build appropriate success message
            var successMsg = !string.IsNullOrEmpty(request.CustomerName)
                ? $"Items by Customer: {data.Count} rows for {request.CustomerName}"
                : $"Sales By Item report: {data.Count} rows";

            return new UsrExcelReportResponse
            {
                success = true,
                key = cacheKey,
                message = successMsg
            };
        }

        /// <summary>
        /// Queries BGSalesByItemView with customer and date filters.
        /// IMPORTANT: Column order must match VBA macro expectations in Rpt sheet.
        ///
        /// VBA macro (PMPSalesByItem) reads columns BY POSITION, not by name:
        ///   - Column C: auxTot = Range("C").Value → Amount to sum
        ///   - Column E: Used for item grouping (loops through unique items)
        ///   - Column F: Quantity for totals
        ///
        /// Template original headers were:
        ///   A=BGCustomer, B=Created on, C=Last Price, D=Product, E=ProductCode, F=Quantity
        ///
        /// So we must output in this exact position order for VBA to work:
        /// </summary>
        private List<Dictionary<string, object>> QuerySalesByItemData(
            UserConnection userConnection,
            UsrExcelReportRequest request)
        {
            var results = new List<Dictionary<string, object>>();

            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGSalesByItemView");
            esq.PrimaryQueryColumn.IsAlwaysSelect = false;  // Don't auto-add Id column

            // Column mapping: ESQ column name -> Header name for Excel output
            // ORDER IS CRITICAL - VBA reads by column position:
            //   Col A: Customer name (template: BGCustomer)
            //   Col B: Date (template: Created on)
            //   Col C: Amount/Price (template: Last Price) - VBA SUMS this column
            //   Col D: Order number (template: Product - using order# as context)
            //   Col E: Item code (template: ProductCode) - VBA GROUPS by this
            //   Col F: Quantity (template: Quantity)
            //   Col G: Unit price (extra)
            var columnMapping = new List<Tuple<string, string>>
            {
                Tuple.Create("BGCustomer", "BGCustomer"),         // Column A: Customer name
                Tuple.Create("BGDeliveryDate", "Created on"),     // Column B: Delivery date
                Tuple.Create("BGAmount", "Last Price"),           // Column C: Amount - VBA SUMS THIS
                Tuple.Create("BGNumber", "Product"),              // Column D: Order number (context)
                Tuple.Create("BGItem", "ProductCode"),            // Column E: Item code - VBA GROUPS BY THIS
                Tuple.Create("BGQuantity", "Quantity"),           // Column F: Quantity
                Tuple.Create("BGPrice", "Filters")                // Column G: Unit price (extra)
            };

            // Track which ESQ columns were successfully added
            var addedColumns = new List<Tuple<string, string>>();

            foreach (var mapping in columnMapping)
            {
                try
                {
                    esq.AddColumn(mapping.Item1);
                    addedColumns.Add(mapping);
                }
                catch
                {
                    // Column doesn't exist - skip
                }
            }

            // REQUIRED: Customer filter (BGCustomer is varchar)
            // Use Contain for case-insensitive partial matching
            if (!string.IsNullOrEmpty(request.CustomerName))
            {
                var customerName = request.CustomerName.Trim();
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Contain,
                    "BGCustomer",
                    customerName
                ));
            }

            // Optional: Created date filters (CreatedOn column)
            if (request.CreatedFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "CreatedOn",
                    request.CreatedFrom.Value
                ));
            }
            if (request.CreatedTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "CreatedOn",
                    request.CreatedTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Optional: Shipping date filters (BGShipDate column)
            if (request.ShippingFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "BGShipDate",
                    request.ShippingFrom.Value
                ));
            }
            if (request.ShippingTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "BGShipDate",
                    request.ShippingTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Optional: Delivery date filters (BGDeliveryDate column)
            if (request.DeliveryFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "BGDeliveryDate",
                    request.DeliveryFrom.Value
                ));
            }
            if (request.DeliveryTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "BGDeliveryDate",
                    request.DeliveryTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Optional: Status filter (BGStatus is varchar)
            if (!string.IsNullOrEmpty(request.StatusName))
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Equal,
                    "BGStatus",
                    request.StatusName
                ));
            }

            // Execute query
            EntityCollection entities;
            try
            {
                entities = esq.GetEntityCollection(userConnection);
            }
            catch (Exception ex)
            {
                // Return empty with error info - caller will show diagnostic message
                throw new Exception("ESQ query failed: " + ex.Message);
            }

            foreach (var entity in entities)
            {
                // Use ordered dictionary to preserve column order for Excel output
                // Keys use VBA-friendly names (ITEM, DESCRIPCION, Qty, Amount) for header matching
                var row = new Dictionary<string, object>();
                foreach (var mapping in addedColumns)
                {
                    var esqColName = mapping.Item1;   // ESQ column name (BGItem, etc.)
                    var vbaColName = mapping.Item2;   // VBA header name (ITEM, etc.)
                    try
                    {
                        var value = entity.GetColumnValue(esqColName);
                        row[vbaColName] = value;
                    }
                    catch
                    {
                        row[vbaColName] = null;
                    }
                }
                results.Add(row);
            }

            return results;
        }

        /// <summary>
        /// Custom generator for "Customers did not buy" and similar reports using BGSalesByCustomerView.
        /// IntExcelExport library doesn't properly apply date filters, causing OutOfMemoryException.
        /// </summary>
        private UsrExcelReportResponse GenerateSalesByCustomerWithFilters(
            UserConnection userConnection,
            UsrExcelReportRequest request)
        {
            // Get template file
            var templateBytes = GetTemplateFile(userConnection, request.ReportId);
            if (templateBytes == null || templateBytes.Length == 0)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Template file not found for Sales By Customer report"
                };
            }

            // Get sheet name
            var sheetName = GetSheetName(userConnection, request.ReportId);

            // Query data with proper filters
            List<Dictionary<string, object>> data;
            try
            {
                data = QuerySalesByCustomerData(userConnection, request);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Query error: " + ex.Message
                };
            }

            if (data.Count == 0)
            {
                // Build diagnostic info
                var filters = new List<string>();
                if (request.CreatedFrom.HasValue) filters.Add("CreatedFrom=" + request.CreatedFrom.Value.ToString("yyyy-MM-dd"));
                if (request.CreatedTo.HasValue) filters.Add("CreatedTo=" + request.CreatedTo.Value.ToString("yyyy-MM-dd"));
                if (request.ShippingFrom.HasValue) filters.Add("ShipFrom=" + request.ShippingFrom.Value.ToString("yyyy-MM-dd"));
                if (request.ShippingTo.HasValue) filters.Add("ShipTo=" + request.ShippingTo.Value.ToString("yyyy-MM-dd"));
                if (request.DeliveryFrom.HasValue) filters.Add("DelFrom=" + request.DeliveryFrom.Value.ToString("yyyy-MM-dd"));
                if (request.DeliveryTo.HasValue) filters.Add("DelTo=" + request.DeliveryTo.Value.ToString("yyyy-MM-dd"));
                if (!string.IsNullOrEmpty(request.StatusName)) filters.Add("Status=" + request.StatusName);

                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "No data found. Filters: " + string.Join(", ", filters)
                };
            }

            // Check row limit (Excel max ~1M rows)
            if (data.Count > 1000000)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = $"Too many rows ({data.Count}). Please add more filters to reduce the data set."
                };
            }

            // Populate Excel template
            byte[] populatedBytes;
            try
            {
                populatedBytes = PopulateExcelTemplate(templateBytes, data, sheetName);
            }
            catch (Exception ex)
            {
                return new UsrExcelReportResponse
                {
                    success = false,
                    message = "Excel population failed: " + ex.Message
                };
            }

            // Cache the result
            var cacheKey = "ExportFilterKey_" + Guid.NewGuid().ToString("N");
            userConnection.SessionData[cacheKey] = populatedBytes;

            return new UsrExcelReportResponse
            {
                success = true,
                key = cacheKey,
                message = $"Sales By Customer report: {data.Count} rows"
            };
        }

        /// <summary>
        /// Queries BGSalesByCustomerView with date and status filters.
        /// Columns: BGStatus, BGCustomer, BGShipDate, BGInvoiceDate, BGDeliveryDate, BGAmount, etc.
        /// </summary>
        private List<Dictionary<string, object>> QuerySalesByCustomerData(
            UserConnection userConnection,
            UsrExcelReportRequest request)
        {
            var results = new List<Dictionary<string, object>>();

            var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGSalesByCustomerView");
            esq.PrimaryQueryColumn.IsAlwaysSelect = false;

            // Column mapping - add all columns the report template expects
            var columns = new List<string>
            {
                "BGStatus",
                "BGCustomer",
                "BGShipDate",
                "BGInvoiceDate",
                "BGDeliveryDate",
                "BGAmount",
                "BGPONumber",
                "BGNumber",
                "BGNumberInvoice",
                "BGInvoiceNumber",
                "BGSalesRep",
                "BGSalesGroup"
            };

            var addedColumns = new List<string>();
            foreach (var col in columns)
            {
                try
                {
                    esq.AddColumn(col);
                    addedColumns.Add(col);
                }
                catch
                {
                    // Column doesn't exist - skip
                }
            }

            // REQUIRED: At least one date filter must be present to prevent full table scan
            bool hasDateFilter = request.CreatedFrom.HasValue || request.CreatedTo.HasValue ||
                                 request.ShippingFrom.HasValue || request.ShippingTo.HasValue ||
                                 request.DeliveryFrom.HasValue || request.DeliveryTo.HasValue;

            if (!hasDateFilter)
            {
                throw new InvalidOperationException("At least one date filter is required for this report");
            }

            // Apply date filters - use BGInvoiceDate as primary (most common)
            if (request.CreatedFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "BGInvoiceDate",
                    request.CreatedFrom.Value.Date
                ));
            }
            if (request.CreatedTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "BGInvoiceDate",
                    request.CreatedTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Shipping date filters
            if (request.ShippingFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "BGShipDate",
                    request.ShippingFrom.Value.Date
                ));
            }
            if (request.ShippingTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "BGShipDate",
                    request.ShippingTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Delivery date filters
            if (request.DeliveryFrom.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.GreaterOrEqual,
                    "BGDeliveryDate",
                    request.DeliveryFrom.Value.Date
                ));
            }
            if (request.DeliveryTo.HasValue)
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.LessOrEqual,
                    "BGDeliveryDate",
                    request.DeliveryTo.Value.Date.AddDays(1).AddMilliseconds(-1)
                ));
            }

            // Status filter
            if (!string.IsNullOrEmpty(request.StatusName))
            {
                esq.Filters.Add(esq.CreateFilterWithParameters(
                    FilterComparisonType.Equal,
                    "BGStatus",
                    request.StatusName
                ));
            }

            // Execute query
            var entities = esq.GetEntityCollection(userConnection);

            foreach (var entity in entities)
            {
                var row = new Dictionary<string, object>();
                foreach (var col in addedColumns)
                {
                    try
                    {
                        row[col] = entity.GetColumnValue(col);
                    }
                    catch
                    {
                        row[col] = null;
                    }
                }
                results.Add(row);
            }

            return results;
        }

        #endregion

        private object CreateUtilitiesTarget(Type utilitiesType, UserConnection userConnection)
        {
            var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
            if (ctor != null)
            {
                return ctor.Invoke(new object[] { userConnection });
            }
            return Activator.CreateInstance(utilitiesType);
        }

        /// <summary>
        /// Builds a simple EntitySchemaQuery without lookup columns to avoid INNER JOIN issues.
        /// Used for FLT-004 workaround where BGYearMonthId is NULL.
        /// </summary>
        private EntitySchemaQuery BuildSimpleEsq(UserConnection userConnection, string entitySchemaName, string filtersConfig)
        {
            var dataEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, entitySchemaName);
            dataEsq.PrimaryQueryColumn.IsAlwaysSelect = true;

            // Add only simple columns, NOT lookup columns (to avoid INNER JOINs)
            var schema = userConnection.EntitySchemaManager.GetInstanceByName(entitySchemaName);
            foreach (var col in schema.Columns)
            {
                // Skip lookup/reference columns - these create INNER JOINs
                if (col.IsLookupType || col.ReferenceSchema != null)
                {
                    continue;
                }
                try
                {
                    dataEsq.AddColumn(col.Name);
                }
                catch
                {
                    // Skip problematic columns
                }
            }

            // Apply filters from FiltersConfig
            if (!string.IsNullOrEmpty(filtersConfig))
            {
                try
                {
                    Type dsFilterType = null;
                    foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        dsFilterType = assembly.GetType("Terrasoft.Nui.ServiceModel.DataContract.DataSourceFilterUtilities");
                        if (dsFilterType != null) break;
                    }

                    if (dsFilterType != null)
                    {
                        var deserializeMethod = dsFilterType.GetMethod("BuildFilterGroup",
                            new[] { typeof(EntitySchemaQuery), typeof(string) });
                        if (deserializeMethod != null)
                        {
                            var filterGroup = deserializeMethod.Invoke(null, new object[] { dataEsq, filtersConfig });
                            if (filterGroup is IEntitySchemaQueryFilterItem fg)
                            {
                                dataEsq.Filters.Add(fg);
                            }
                        }
                    }
                }
                catch
                {
                    // If filter deserialization fails, continue without filters
                }
            }

            return dataEsq;
        }

        /// <summary>
        /// Sanitizes ESQ JSON by removing filter items that contain @P<number>@ placeholder patterns.
        /// These placeholders are Creatio framework parameters that IntExcelExport library cannot parse,
        /// causing "Guid should contain 32 digits" errors. By clearing the items, the library can process
        /// the ESQ and filters are applied via FiltersConfig instead (same pattern as Commission report).
        /// </summary>
        private string SanitizeEsqJson(string esqJson)
        {
            if (string.IsNullOrEmpty(esqJson))
            {
                return esqJson;
            }

            // Check if there are any @P<number>@ patterns in the JSON
            if (!Regex.IsMatch(esqJson, @"@P\d+@"))
            {
                return esqJson;
            }

            try
            {
                // Simple approach: Replace the "items":{...} object content with empty object
                // when it contains @P<number>@ placeholders.
                // This mimics the working Commission report which has "items":{}
                // The nested JSON structure is too complex for regex extraction,
                // but we can use a balanced brace matching approach.

                // Find "items": followed by opening brace and match to closing brace
                var itemsPattern = @"""items""\s*:\s*\{";
                var match = Regex.Match(esqJson, itemsPattern);

                if (!match.Success)
                {
                    return esqJson;
                }

                // Find the matching closing brace for the items object
                int startIndex = match.Index + match.Length - 1; // Position of opening {
                int braceCount = 1;
                int endIndex = startIndex + 1;

                while (braceCount > 0 && endIndex < esqJson.Length)
                {
                    char c = esqJson[endIndex];
                    if (c == '{') braceCount++;
                    else if (c == '}') braceCount--;
                    endIndex++;
                }

                if (braceCount != 0)
                {
                    // Unbalanced braces - return original
                    return esqJson;
                }

                // Extract the items content (including braces)
                string itemsContent = esqJson.Substring(startIndex, endIndex - startIndex);

                // Only replace if it contains @P<number>@ patterns
                if (Regex.IsMatch(itemsContent, @"@P\d+@"))
                {
                    // Replace with empty items object
                    string sanitized = esqJson.Substring(0, startIndex) + "{}" + esqJson.Substring(endIndex);
                    return sanitized;
                }

                return esqJson;
            }
            catch
            {
                // If sanitization fails, return original to avoid breaking working reports
                return esqJson;
            }
        }

        /// <summary>
        /// Gets the IntEsq JSON string from the IntExcelReport record.
        /// Sanitizes placeholder filters that IntExcelExport cannot parse.
        /// </summary>
        private string GetIntEsqJson(UserConnection userConnection, Guid reportId)
        {
            var reportEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            reportEsq.AddColumn("IntEsq");
            var reportEntity = reportEsq.GetEntity(userConnection, reportId);
            if (reportEntity == null) return null;

            var rawEsq = reportEntity.GetTypedColumnValue<string>("IntEsq");

            // Sanitize ESQ to remove @P<number>@ placeholder filters that cause GUID parsing errors
            return SanitizeEsqJson(rawEsq);
        }

        /// <summary>
        /// Builds an EntitySchemaQuery from the IntEsq JSON stored in IntExcelReport.
        /// This bypasses the broken GetReportEsq -> GetReportData path that fails on template lookup.
        /// </summary>
        /// <param name="skipYearMonthColumn">If true, skips BGYearMonth columns (FLT-004 workaround)</param>
        private EntitySchemaQuery BuildEsqFromIntEsq(UserConnection userConnection, Guid reportId, string filtersConfig, bool skipYearMonthColumn = false)
        {
            // Read IntEsq from IntExcelReport
            var reportEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
            reportEsq.AddColumn("IntEsq");
            var reportEntity = reportEsq.GetEntity(userConnection, reportId);
            if (reportEntity == null)
            {
                return null;
            }

            var intEsqJson = reportEntity.GetTypedColumnValue<string>("IntEsq");
            if (string.IsNullOrEmpty(intEsqJson))
            {
                return null;
            }

            // Parse rootSchemaName from JSON
            var rootSchemaMatch = Regex.Match(intEsqJson, "\\\"rootSchemaName\\\"\\s*:\\s*\\\"(?<name>[^\\\"]+)\\\"");
            if (!rootSchemaMatch.Success)
            {
                return null;
            }
            var rootSchemaName = rootSchemaMatch.Groups["name"].Value;

            // Create ESQ for the data entity
            var dataEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, rootSchemaName);
            dataEsq.PrimaryQueryColumn.IsAlwaysSelect = true;

            // Parse and add columns from IntEsq JSON
            // Look for columns in the format: "ColumnCaption":{"caption":"...","expression":{"columnPath":"..."}}
            var columnsMatch = Regex.Match(intEsqJson, "\\\"columns\\\"\\s*:\\s*\\{\\s*\\\"className\\\"\\s*:\\s*\\\"[^\\\"]+\\\"\\s*,\\s*\\\"items\\\"\\s*:\\s*\\{([^}]+(?:\\{[^}]*\\}[^}]*)*)\\}\\}");
            if (columnsMatch.Success)
            {
                // Parse column paths from the items section
                var columnMatches = Regex.Matches(intEsqJson, "\\\"columnPath\\\"\\s*:\\s*\\\"(?<path>[^\\\"]+)\\\"");
                var addedColumns = new HashSet<string>();
                foreach (Match colMatch in columnMatches)
                {
                    var columnPath = colMatch.Groups["path"].Value;

                    // FLT-004: Skip BGYearMonth columns to avoid INNER JOIN on NULL values
                    if (skipYearMonthColumn && columnPath.Contains("BGYearMonth"))
                    {
                        continue;
                    }

                    if (!addedColumns.Contains(columnPath))
                    {
                        try
                        {
                            dataEsq.AddColumn(columnPath);
                            addedColumns.Add(columnPath);
                        }
                        catch
                        {
                            // Skip invalid column paths
                        }
                    }
                }
            }

            // Apply filters from FiltersConfig if provided
            if (!string.IsNullOrEmpty(filtersConfig))
            {
                try
                {
                    // Use Creatio's filter deserialization
                    var filters = dataEsq.CreateFilterWithParameters(
                        FilterComparisonType.Equal,
                        dataEsq.RootSchema.PrimaryColumn.Name,
                        Guid.Empty);
                    // Clear the dummy filter and deserialize the real one
                    dataEsq.Filters.Clear();

                    // Try to use DataSourceFilterUtilities if available
                    Type dsFilterType = null;
                    foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        dsFilterType = assembly.GetType("Terrasoft.Nui.ServiceModel.DataContract.DataSourceFilterUtilities");
                        if (dsFilterType != null) break;
                    }

                    if (dsFilterType != null)
                    {
                        var deserializeMethod = dsFilterType.GetMethod("BuildFilterGroup",
                            new[] { typeof(EntitySchemaQuery), typeof(string) });
                        if (deserializeMethod != null)
                        {
                            var filterGroup = deserializeMethod.Invoke(null, new object[] { dataEsq, filtersConfig });
                            if (filterGroup is IEntitySchemaQueryFilterItem fg)
                            {
                                dataEsq.Filters.Add(fg);
                            }
                        }
                    }
                }
                catch
                {
                    // If filter deserialization fails, continue without filters
                }
            }

            return dataEsq;
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

                // Log the incoming request for debugging
                System.Diagnostics.Debug.WriteLine($"UsrExcelReportService.Generate - ReportId: {request.ReportId}, YearMonthId: {request.YearMonthId}, SalesRepId: {request.SalesRepId}");

                // FLT-004 FIX: View SQL has been corrected to filter on so."BGInvoiceDate".
                // Now using IntExcelExport with BGExecutionId filtering (view handles Year-Month/SalesGroup).
                var entitySchemaName = GetReportEntitySchemaName(userConnection, request.ReportId);

                // FLT-002 FIX: IW_Commission with Year-Month filter requires custom generator
                // IntExcelExport library throws ArgumentNullException with DateTime filters in FiltersConfig
                if (entitySchemaName == "IWCommissionReportDataView" && request.YearMonthId != Guid.Empty)
                {
                    var yearMonthName = GetYearMonthName(userConnection, request.YearMonthId);
                    if (!string.IsNullOrEmpty(yearMonthName))
                    {
                        return GenerateIWCommissionWithDateFilter(userConnection, request, yearMonthName);
                    }
                }

                // BGSalesByItemView REPORTS: Custom generator required for all reports using this view
                // IntExcelExport library doesn't properly apply FiltersConfig to ESQ
                // BGSalesByItemView has 4.8M rows - MUST filter to avoid Excel row limit
                // Reports: Items by Customer, Sales By Item, Sales By Item By Type Of Customer
                if (entitySchemaName == "BGSalesByItemView")
                {
                    // Check if any meaningful filter is present
                    bool hasFilter = !string.IsNullOrEmpty(request.CustomerName) ||
                                    request.CreatedFrom.HasValue || request.CreatedTo.HasValue ||
                                    request.ShippingFrom.HasValue || request.ShippingTo.HasValue ||
                                    request.DeliveryFrom.HasValue || request.DeliveryTo.HasValue ||
                                    !string.IsNullOrEmpty(request.StatusName);
                    if (hasFilter)
                    {
                        return GenerateSalesByItemWithFilters(userConnection, request);
                    }
                }

// ROLLBACK:                 // CUSTOMERS DID NOT BUY FIX: Custom generator for BGSalesByCustomerView
// ROLLBACK:                 // IntExcelExport library causes OutOfMemoryException on large views without proper filters
// ROLLBACK:                 // Requires at least one date filter to prevent full table scan
// ROLLBACK:                 if (entitySchemaName == "BGSalesByCustomerView")
// ROLLBACK:                 {
// ROLLBACK:                     bool hasDateFilter = request.CreatedFrom.HasValue || request.CreatedTo.HasValue ||
// ROLLBACK:                                         request.ShippingFrom.HasValue || request.ShippingTo.HasValue ||
// ROLLBACK:                                         request.DeliveryFrom.HasValue || request.DeliveryTo.HasValue;
// ROLLBACK:                     if (hasDateFilter)
// ROLLBACK:                     {
// ROLLBACK:                         return GenerateSalesByCustomerWithFilters(userConnection, request);
// ROLLBACK:                     }
// ROLLBACK:                 }

                // DL-004/DL-005 FIX: Use library generation (preserves VBA macros) but capture bytes
                // Library returns ExportFilterKey but stores bytes in its own cache, not SessionData
                // After library Generate, we fetch bytes via its GetReport and store in our SessionData
                // This ensures our GetReport can find the bytes while preserving proper Excel format

                // Use IntExcelExport library
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

                // Try to create request using parameterless constructor first (initializes defaults).
                object serviceRequest = null;
                var defaultCtor = requestType.GetConstructor(Type.EmptyTypes);
                if (defaultCtor != null)
                {
                    serviceRequest = defaultCtor.Invoke(null);
                }
                else
                {
                    // Fallback to uninitialized object (may leave required fields null).
                    serviceRequest = FormatterServices.GetUninitializedObject(requestType);
                }

                var reportIdProp = requestType.GetProperty("ReportId");
                if (reportIdProp != null)
                {
                    reportIdProp.SetValue(serviceRequest, request.ReportId);
                }

                // Build and set FiltersConfig (this is what ReportUtilities.Generate actually reads in this env).
                // Note: entitySchemaName already declared above for the FLT-004 bypass check
                var filtersConfig = BuildFiltersConfig(userConnection, request, entitySchemaName);

                var filtersConfigProp = requestType.GetProperty("FiltersConfig") ?? requestType.GetProperty("filtersConfig");
                if (filtersConfigProp != null)
                {
                    filtersConfigProp.SetValue(serviceRequest, filtersConfig);
                }

                // SKIP IntExcelReportService.Generate - it's broken in DEV (null value error)
                // Go directly to ReportUtilities.Generate which may work differently

                // Look for QueryConfig property (some versions use this instead of / in addition to Esq).
                var queryConfigProp = requestType.GetProperty("QueryConfig") ?? requestType.GetProperty("queryConfig");

                // Set Esq if available (helps avoid relying on JSON IntEsq parsing in this custom service).
                var esqProp = requestType.GetProperty("Esq") ?? requestType.GetProperty("esq");
                var getReportEsqMethod = utilitiesType.GetMethod("GetReportEsq", new[] { typeof(Guid) });

                object target = null;
                if ((!generateMethod.IsStatic) || (getReportEsqMethod != null && !getReportEsqMethod.IsStatic))
                {
                    target = CreateUtilitiesTarget(utilitiesType, userConnection);
                }

                // REQUIRED (2026-01-19): Set queryConfig with the IntEsq JSON from IntExcelReport.
                // The IntExcelExport library requires this to generate reports.
                // Previous comment saying "Do NOT set" was INCORRECT and broke all reports.
                var intEsqJson = GetIntEsqJson(userConnection, request.ReportId);
                if (queryConfigProp != null && !string.IsNullOrEmpty(intEsqJson))
                {
                    queryConfigProp.SetValue(serviceRequest, intEsqJson);
                }

                object result;
                try
                {
                    result = generateMethod.Invoke(generateMethod.IsStatic ? null : target, new object[] { serviceRequest });
                }
                catch (TargetInvocationException genEx)
                {
                    var inner = genEx.InnerException;
                    // Include FULL stack trace to find the exact method calling Json.Deserialize
                    var stackInfo = inner?.StackTrace ?? "";
                    // Get multiple stack lines to trace the call path
                    var stackLines = new System.Text.StringBuilder();
                    if (!string.IsNullOrEmpty(stackInfo))
                    {
                        var lines = stackInfo.Split('\n');
                        int count = 0;
                        foreach (var line in lines)
                        {
                            var trimmed = line.Trim();
                            if (trimmed.Contains("IntExcelExport") || trimmed.Contains("ReportUtilities") ||
                                trimmed.Contains("Json.Deserialize") || trimmed.Contains("Generate"))
                            {
                                // Extract method name only (remove path info)
                                var methodPart = trimmed;
                                if (methodPart.Contains(" in "))
                                    methodPart = methodPart.Substring(0, methodPart.IndexOf(" in "));
                                if (methodPart.Length > 80)
                                    methodPart = methodPart.Substring(0, 80);
                                stackLines.Append("[" + count + "]" + methodPart + "|");
                                count++;
                                if (count >= 5) break;
                            }
                        }
                    }
                    return new UsrExcelReportResponse
                    {
                        success = false,
                        message = inner?.GetType().Name + ": " + inner?.Message + " STACK:" + stackLines.ToString()
                    };
                }
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
                        message = "Report generated (library fallback)"
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
                // Include request type info for debugging
                var reqTypeInfo = "";
                try
                {
                    foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        var ut = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                        if (ut != null)
                        {
                            var gm = ut.GetMethod("Generate");
                            if (gm != null)
                            {
                                var rt = gm.GetParameters()[0].ParameterType;
                                var props = rt.GetProperties().Select(p => p.Name).ToArray();
                                reqTypeInfo = " [Props: " + string.Join(",", props) + "]";
                            }
                            break;
                        }
                    }
                }
                catch { }

                return new UsrExcelReportResponse
                {
                    success = false,
                    message = inner?.GetType().Name + ": " + inner?.Message + reqTypeInfo
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

        private string SanitizeFileName(string name)
        {
            var n = (name ?? "").Trim();
            if (string.IsNullOrEmpty(n))
            {
                return "Report";
            }

            // Keep it conservative: remove characters that commonly break Content-Disposition.
            n = Regex.Replace(n, "[^a-zA-Z0-9 _.-]+", "_");
            n = n.Trim();
            return string.IsNullOrEmpty(n) ? "Report" : n;
        }

        private bool ContainsBytes(byte[] haystack, byte[] needle)
        {
            if (haystack == null || needle == null || needle.Length == 0 || haystack.Length < needle.Length)
            {
                return false;
            }

            for (int i = 0; i <= haystack.Length - needle.Length; i++)
            {
                bool match = true;
                for (int j = 0; j < needle.Length; j++)
                {
                    if (haystack[i + j] != needle[j])
                    {
                        match = false;
                        break;
                    }
                }

                if (match)
                {
                    return true;
                }
            }

            return false;
        }

        /// <summary>
        /// Download endpoint that serves the generated workbook with the correct extension.
        ///
        /// Why:
        /// - The exported workbooks may contain macros (xl/vbaProject.bin) but the marketplace
        ///   IntExcelReportService/GetReport endpoint serves them as .xlsx.
        /// - Some Excel installations refuse to open macro-enabled content when the
        ///   extension is .xlsx, producing "file format or file extension is not valid".
        ///
        /// This wrapper reads the cached bytes from UserConnection.SessionData, detects
        /// macro presence, and sets Content-Disposition to *.xlsm (macros) or *.xlsx (no macros).
        /// </summary>
        [OperationContract]
        [WebGet(UriTemplate = "GetReport/{key}/{reportNameSegment}")]
        public void GetReport(string key, string reportNameSegment)
        {
            var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];
            if (userConnection == null)
            {
                throw new InvalidOperationException("UserConnection not available");
            }

            var cacheObj = userConnection.SessionData[key];

            // DL-004/DL-005 FIX: If bytes not in our SessionData, try library's GetReport
            // Library stores bytes in its own cache, not ours - fetch via HTTP redirect
            if (cacheObj == null && key.StartsWith("ExportFilterKey_"))
            {
                // Redirect to library's endpoint which knows where its bytes are stored
                var libraryUrl = "/0/rest/IntExcelReportService/GetReport/" + key;
                HttpContext.Current.Response.Redirect(libraryUrl, true);
                return;
            }

            if (cacheObj == null)
            {
                throw new Exception("Report not found. Report key: " + key);
            }

            // Make the key single-use, matching the IntExcelReportService behavior.
            userConnection.SessionData.Remove(key);

            // Normalize cached content into bytes so we can reliably:
            // 1) detect whether this is macro-enabled (vbaProject.bin), and
            // 2) write the response body without consuming a one-shot stream.
            byte[] bytes;
            if (cacheObj is byte[] b)
            {
                bytes = b;
            }
            else if (cacheObj is Stream s)
            {
                using (s)
                using (var ms = new MemoryStream())
                {
                    s.CopyTo(ms);
                    bytes = ms.ToArray();
                }
            }
            else
            {
                throw new Exception("Unexpected cached report type: " + cacheObj.GetType().FullName);
            }

            var safeBase = SanitizeFileName(reportNameSegment);

            var hasVbaProject = false;
            try
            {
                hasVbaProject = ContainsBytes(bytes, Encoding.ASCII.GetBytes("xl/vbaProject.bin"));
            }
            catch
            {
                // If inspection fails, keep defaults below.
            }

            var extension = hasVbaProject ? ".xlsm" : ".xlsx";
            var fileName = safeBase + extension;

            // Set headers.
            var response = HttpContext.Current.Response;
            response.AddHeader("Content-Disposition", string.Format(
                "attachment; filename=\"{0}\"; filename*=UTF-8''{1}",
                fileName,
                HttpUtility.UrlEncode(fileName)
            ));

            response.ContentType = hasVbaProject
                ? "application/vnd.ms-excel.sheet.macroEnabled.12"
                : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

            response.OutputStream.Write(bytes, 0, bytes.Length);
            response.OutputStream.Flush();
            return;
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
                var methodInfo = string.Join("; ", methods.Select(m =>
                    m.Name + "(" + string.Join(",", m.GetParameters().Select(p => p.ParameterType.Name)) + ")->" + m.ReturnType.Name
                ));

                // Also get request type properties
                var generateMethod = utilitiesType.GetMethod("Generate");
                if (generateMethod != null)
                {
                    var requestType = generateMethod.GetParameters()[1].ParameterType;
                    var props = requestType.GetProperties();
                    methodInfo += " | RequestProps: " + string.Join(",", props.Select(p => p.Name + ":" + p.PropertyType.Name));
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
        [WebGet(UriTemplate = "GetFile/{key}")]
        public Stream GetFile(string key)
        {
            try
            {
                var userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                Type utilitiesType = null;
                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    utilitiesType = assembly.GetType("IntExcelExport.Utilities.ReportUtilities");
                    if (utilitiesType != null) break;
                }

                if (utilitiesType == null) return null;

                // Try to find GetReportFile method
                var getFileMethod = utilitiesType.GetMethod("GetReportFile")
                    ?? utilitiesType.GetMethod("GetFile")
                    ?? utilitiesType.GetMethod("Download");

                if (getFileMethod == null) return null;

                object target = null;
                if (!getFileMethod.IsStatic)
                {
                    var ctor = utilitiesType.GetConstructor(new[] { typeof(UserConnection) });
                    if (ctor != null)
                        target = ctor.Invoke(new object[] { userConnection });
                    else
                        target = Activator.CreateInstance(utilitiesType);
                }

                var result = getFileMethod.Invoke(target, new object[] { key });

                if (result is Stream stream)
                {
                    WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                    return stream;
                }
                else if (result is byte[] bytes)
                {
                    WebOperationContext.Current.OutgoingResponse.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                    return new MemoryStream(bytes);
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
