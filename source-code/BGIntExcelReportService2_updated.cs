 using System.Data;
using System.Text.RegularExpressions;
using Terrasoft.Core.DB;
using Terrasoft.Core.Entities;


namespace Terrasoft.Configuration.ReportService
{
	using System;
	using System.IO;
	using System.Runtime.Serialization;
	using System.Collections.Generic;
	using System.ServiceModel;
	using System.ServiceModel.Web;
	using System.ServiceModel.Activation;
	using System.Web;
	using Terrasoft.Common;
	using Terrasoft.Core;
	using Terrasoft.Core.Configuration;
	using Terrasoft.Core.Factories;
	using Terrasoft.Web.Common;
	using System.Net.Mail;
	using System.Net;

	/// <summary>
	/// Request class for Generate method with proper DataContract
	/// </summary>
	[DataContract]
	public class BGReportGenerateRequest {
		[DataMember(Name = "EsqString")]
		public string EsqString { get; set; }

		[DataMember(Name = "ReportId")]
		public Guid ReportId { get; set; }

		[DataMember(Name = "RecordCollection")]
		public List<Guid> RecordCollection { get; set; }
	}

	[ServiceContract]
	[AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
	class BGIntExcelReportService2 : BaseService
	{
		#region Constants: Protected


		private const int ChunkSize = 524288;

		/*
		private SystemUserConnection _systemUserConnection;
        private SystemUserConnection SystemUserConnection {
            get {
                return _systemUserConnection ?? (_systemUserConnection = (SystemUserConnection)AppConnection.SystemUserConnection);
            }
        }*/

        private UserConnection _systemUserConnection;
        private UserConnection SystemUserConnection {
            get {
                //return _systemUserConnection ?? (_systemUserConnection = (SystemUserConnection)AppConnection.SystemUserConnection);
               	return _systemUserConnection ?? (_systemUserConnection = (UserConnection)HttpContext.Current.Session["UserConnection"]);
            }
        }


		#endregion


		#region Methods: Private


		/// <summary>
		/// Remove special characters from fileName.
		/// </summary>
		/// <param name="fileName">File name.</param>
		/// <returns>File name without special characters.</returns>
		private string RemoveSpecialCharacters(string fileName) {
			return Regex.Replace(fileName, @"[^a-zA-Z\p{IsCyrillic}0-9_.,^&@£$€!½§~'=()\[\]{} «»<>~#*%+-]+",
				"_", RegexOptions.Compiled);
		}


		/// <summary>
		/// Sets outgoing response content type.
		/// </summary>
		private void SetOutgoingResponseContentType() {
			WebOperationContext.Current.OutgoingResponse.ContentType = "application/octet-stream";
		}


		/// <summary>
		/// Sets outgoing response content length.
		/// </summary>
		private void SetOutgoingResponseContentLength(int size) {
			WebOperationContext.Current.OutgoingResponse.ContentLength = size;
		}


		/// <summary>
		/// Gets response content disposition header value.
		/// </summary>
		/// <param name="fileName">File name.</param>
		/// <returns>Content disposition header value.</returns>
		private string GetResponseContentDisposition(string fileName) {
			string processedFileName;
			HttpRequest request = HttpContext.Current.Request;

			if (request.Browser.Browser == "IE" && (request.Browser.Version == "7.0"
				|| request.Browser.Version == "8.0")) {
				processedFileName = HttpUtility.UrlEncode(fileName);
			} else if (request.UserAgent != null && request.UserAgent.ToLowerInvariant().Contains("android")) {
				processedFileName = "\"" + RemoveSpecialCharacters(fileName) + "\"";
			} else if (request.Browser.Browser == "Safari") {
				processedFileName = RemoveSpecialCharacters(fileName);
			} else {
				processedFileName = "\"" + fileName + "\"; filename*=UTF-8''" + HttpUtility.UrlEncode(fileName);
			}

			return String.Format("attachment; filename={0}", processedFileName);
		}


		#endregion


		#region Methods: Public


		/// <summary>
		/// Generate report with proper DataContract deserialization
		/// </summary>
		[OperationContract]
		[WebInvoke(Method = "POST", UriTemplate = "Generate",
			RequestFormat = WebMessageFormat.Json,
			ResponseFormat = WebMessageFormat.Json,
			BodyStyle = WebMessageBodyStyle.Bare)]
		public IntExcelExport.Models.IntExcelReportServiceResponse Generate(BGReportGenerateRequest request) {
			try {
				var serviceRequest = new IntExcelExport.Models.IntExcelReportServiceRequest {
					EsqString = request.EsqString,
					ReportId = request.ReportId,
					RecordCollection = request.RecordCollection ?? new List<Guid>()
				};
				return IntExcelExport.Utilities.ReportUtilities.Generate(serviceRequest, SystemUserConnection);
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


		[OperationContract]
		[WebGet(UriTemplate = "GetExportFilteredData/{reportName}/{filtersContextKey}")]
		public void GetExportFilteredData(string reportName, string filtersContextKey) {
			byte[] reportBytes = SystemUserConnection.SessionData[filtersContextKey] as byte[];

			if (reportBytes == null)
			{
				throw new Exception("Report not found. Report key: " + filtersContextKey);
			}

			SystemUserConnection.SessionData.Remove(filtersContextKey);

			reportName += ".xlsm";

			string contentDisposition = GetResponseContentDisposition(reportName);
			HttpContext.Current.Response.AddHeader("Content-Disposition", contentDisposition);
			HttpContext.Current.Response.ContentType = "application/octet-stream";

			int size = Convert.ToInt32(reportBytes.Length);
			int offset = 0;
			int bufferOffset = 0;
			int chunkSize = size < ChunkSize ? size : ChunkSize;
			byte[] buffer = new byte[chunkSize];
			long realBytes = 0;
			int buffSize = 0;
			while (offset < size) {
				Array.Clear(buffer, 0, buffer.Length);
				buffSize = (size < (offset + chunkSize)) ? size - offset : chunkSize;
				buffer = new byte[buffSize];
				Buffer.BlockCopy(reportBytes, offset, buffer, bufferOffset, buffSize);

				realBytes = buffer.Length;
				if (realBytes <= 0) {
					break;
				}
				offset += Convert.ToInt32(realBytes);
				HttpContext.Current.Response.OutputStream.Write(buffer, 0, Convert.ToInt32(realBytes));
				HttpContext.Current.Response.OutputStream.Flush();
			}

		}


		[OperationContract]
		[WebGet(UriTemplate = "GetReport/{key}/{reportName}")]
		public void GetReport(string key, string reportName) {
			byte[] reportBytes = SystemUserConnection.SessionData[key] as byte[];

			if (reportBytes == null)
			{
				throw new Exception("Report not found. Report key: " + key);
			}

			SystemUserConnection.SessionData.Remove(key);

			reportName += ".xlsm";

			string contentDisposition = GetResponseContentDisposition(reportName);
			HttpContext.Current.Response.AddHeader("Content-Disposition", contentDisposition);
			HttpContext.Current.Response.ContentType = "application/octet-stream";

			int size = Convert.ToInt32(reportBytes.Length);
			int offset = 0;
			int bufferOffset = 0;
			int chunkSize = size < ChunkSize ? size : ChunkSize;
			byte[] buffer = new byte[chunkSize];
			long realBytes = 0;
			int buffSize = 0;
			while (offset < size) {
				Array.Clear(buffer, 0, buffer.Length);
				buffSize = (size < (offset + chunkSize)) ? size - offset : chunkSize;
				buffer = new byte[buffSize];
				Buffer.BlockCopy(reportBytes, offset, buffer, bufferOffset, buffSize);

				realBytes = buffer.Length;
				if (realBytes <= 0) {
					break;
				}
				offset += Convert.ToInt32(realBytes);
				HttpContext.Current.Response.OutputStream.Write(buffer, 0, Convert.ToInt32(realBytes));
				HttpContext.Current.Response.OutputStream.Flush();
			}

		}


		[OperationContract]
		[WebGet(UriTemplate = "GetTemplate/{fileId}")]
		public void GetTemplate(string fileId)
		{
			Guid templateId;

			if (!Guid.TryParse(fileId, out templateId))
				throw new ArgumentNullException("fileId");

			SetOutgoingResponseContentType();
			int size = 0;
			string fileName = string.Empty;

			Select selectData = (new Select(SystemUserConnection)
				.Column("IntName")
				.Column(Func.DataLength("IntFile")).As("Size")
				.Column("IntFile")
				.From("IntExcelReport")
				.Where("Id")
				.IsEqual(Column.Parameter(new Guid(fileId)))) as Select;

			using (DBExecutor executor = SystemUserConnection.EnsureDBConnection()) {
				using (IDataReader reader = selectData.ExecuteReader(executor, CommandBehavior.SequentialAccess)) {
					long offset = 0;
					int bufferOffset = 0;
					int chunkSize = 524288;
					byte[] buffer = new byte[chunkSize];
					long realBytes = 0;
					while (reader.Read()) {
						fileName = reader["IntName"].ToString() + ".xlsx";
						size = Convert.ToInt32(reader["Size"]);
						SetOutgoingResponseContentLength(size);
						string contentDisposition = GetResponseContentDisposition(fileName);
						HttpContext.Current.Response.AddHeader("Content-Disposition", contentDisposition);
						HttpContext.Current.Response.ContentType = "application/octet-stream";
						while (offset < size) {
							Array.Clear(buffer, 0, buffer.Length);
							realBytes = reader.GetBytes(2, offset, buffer, bufferOffset, chunkSize);

							if (realBytes <= 0)
								break;

							offset += realBytes;
							HttpContext.Current.Response.OutputStream.Write(buffer, 0, Convert.ToInt32(realBytes));
							HttpContext.Current.Response.OutputStream.Flush();
						}
					}
				}
			}
		}


		#endregion
	}
}
