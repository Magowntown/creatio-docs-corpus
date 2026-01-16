//Test
using nsoftware.InQB;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;
using Terrasoft.Common;
using Terrasoft.Configuration.BGIntegrationHelpers;
using Terrasoft.Core;
using Terrasoft.Core.DB;
using Terrasoft.Core.Entities;
using Column = Terrasoft.Core.DB.Column;

//TODO: ADD BUYERS TO INTEGRATION
namespace Terrasoft.Configuration.BGQuickBooks {

	#region Constants

	public static class BGQBTransactionType {
		public const string Expense = "Expense";
		public const string Check = "Check";
		public const string CreditCardCredit = "CreditCardCredit";
		public const string JournalEntry = "JournalEntry";
		public const string CreditMemo = "CreditMemo";
		public const string Invoice = "Invoice";
	}

	public static class BGTransactionType {
		public const string Sales = "b4494f26-26c2-4aa6-951c-658d0828d0d0";
		public const string CreditMemo = "c26d3478-7ac1-49e9-97f9-1c0809552f1f";
	}

	public class BGQBApiException : Exception {

		public BGQBApiException() {
		}

		public BGQBApiException(string message) : base(message) {
		}

		public BGQBApiException(string message, Exception innerException) : base(message, innerException) {
		}
	}

	#endregion Constants

	public class BGQuickBooks {

		/// <summary>
		/// QB Connector Runtime from old pampa bay site, app seems deprecated and unable to transfer license to creatio
		/// </summary>
		private const string _runtimeLicense = "42424E3541414E5852464353433830313400000000000000000000000000000000000000000000003938484237434E5800004D353231434D544B4E475A370000";

		public const string CustomFieldNamePacking = "Packaging";

		#region Public Constants

		// Move these where they will be easier to configure
		public const int QBCONN_PORT = 99;  // Default port; otherwise, defined in Web.config.

		public const string QBCONN_USER = "";

		public const string QBCONN_APPNAME = "PampaBayQB";

		public const string QBACCT_ACCOUNT = "Sales Income";
		public const string QBACCT_DISCOUNT = "Discount";
		public const string QBACCT_COGS = "Sales Income";//"Cost of Goods Sold";
		public const string QBACCT_ASSET = "Inventory Asset";
		public const string QBACCT_SUBTOTAL = "Subtotal";
		public const string QBACCT_SUBTOTAL_DESCR = "Invoice Subtotal";
		public const string QBACCT_SHIPCHARGE = "Sales - Shipping";
		public const string QBACCT_SHIPCHARGE_NAME = "Shipping and Handling";
		public const string QBACCT_SHIPCHARGE_DESCR = "Customer-paid shipping";

		public const string QBPENDING_REQ_DELETE = "DEL";
		public const string QBPENDING_OBJ_FACTORYORDER = "FO";
		public const string QBPENDING_OBJ_INVOICE = "INV";

		public const string QBREQ_COMPANY_GET = "COMPANY_GET";
		public const string QBREQ_LISTS_ADD = "LISTS_ADD";

		public const string QBREQ_PURCHASEORDER_GET = "PO_GET";
		public const string QBREQ_PURCHASEORDER_ADD = "PO_ADD";
		public const string QBREQ_PURCHASEORDER_UPDATE = "PO_UPDATE";
		public const string QBREQ_PURCHASEORDER_DELETE = "PO_DELETE";

		public const string QBREQ_SALESORDER_GET = "SO_GET";
		public const string QBREQ_SALESORDER_ADD = "SO_ADD";
		public const string QBREQ_SALESORDER_UPDATE = "SO_UPDATE";

		public const string QBREQ_INVOICE_LOOKUP = "INVOICE_LOOKUP";
		public const string QBREQ_INVOICE_GET = "INVOICE_GET";
		public const string QBREQ_INVOICE_ADD = "INVOICE_ADD";
		public const string QBREQ_INVOICE_UPDATE = "INVOICE_UPDATE";
		public const string QBREQ_INVOICE_DELETE = "INVOICE_DELETE";

		public const string QBREQ_ITEM_LOOKUP = "ITEM_LOOKUP";
		public const string QBREQ_ITEM_GET = "ITEM_GET";
		public const string QBREQ_ITEM_ADD = "ITEM_ADD";
		public const string QBREQ_ITEM_UPDATE = "ITEM_UPDATE";

		public const string QBREQ_INVENTORYADJ_GET = "INVENTORYADJ_GET";
		public const string QBREQ_INVENTORYADJ_ADD = "INVENTORYADJ_ADD";
		public const string QBREQ_INVENTORYADJ_DELETE = "INVENTORYADJ_DELETE";

		public const string QBREQ_OTHERNAME_LOOKUP = "OTHERNAME_LOOKUP";
		public const string QBREQ_OTHERNAME_ADD = "OTHERNAME_ADD";

		public const string QBREQ_SALESREP_LOOKUP = "SALESREP_LOOKUP";

		public const string QBREQ_ITEMDISCOUNT_ADD = "ITEMDISCOUNT_ADD";
		public const string QBREQ_ITEMDISCOUNT_UPDATE = "ITEMDISCOUNT_UPDATE";
		public const string QBREQ_ITEMSUBTOTAL_ADD = "ITEMSUBTOTAL_ADD";
		public const string QBREQ_ITEMOTHERCHARGE_ADD = "ITEMOTHERCHARGE_ADD";

		public const string QBREQ_VENDOR_LOOKUP = "VENDOR_LOOKUP";
		public const string QBREQ_VENDOR_GET = "VENDOR_GET";
		public const string QBREQ_VENDOR_ADD = "VENDOR_ADD";
		public const string QBREQ_VENDOR_UPDATE = "VENDOR_UPDATE";

		public const string QBREQ_CUSTOMER_LOOKUP = "CUSTOMER_LOOKUP";
		public const string QBREQ_CUSTOMER_GET = "CUSTOMER_GET";
		public const string QBREQ_CUSTOMER_ADD = "CUSTOMER_ADD";
		public const string QBREQ_CUSTOMER_UPDATE = "CUSTOMER_UPDATE";
		public const string QBREQ_CUSTOMERJOB_ADD = "CUSTJOB_ADD";
		public const string QBREQ_CUSTOMERJOB_UPDATE = "CUSTJOB_UPDATE";

		public const int QB_ADDR_LINE_MAXLEN = 41;

		#endregion Public Constants

		#region Private Variables

		private string qbConnectorURL = "";//"http://localhost";//ConfigManager.QuickBooksLocation;
		private int qbConnectorPort = 0; //(ConfigManager.QuickBooksPort == null || ConfigManager.QuickBooksPort == String.Empty ? QBCONN_PORT : Convert.ToInt32(ConfigManager.QuickBooksPort));
		private string qbConnectorUser = "";
		private string qbConnectorPassword = "";
		private int qbConnectorTimeout = 90;
		private int qbConnectorReturnCode = 0;
		private string qbConnectorMessage = String.Empty;
		private bool qbIsLoggingEnabled = false;
		private UserConnection userConnection = null;

		#endregion Private Variables

		#region Public Properties

		public string RuntimeLicense => BGQuickBooks._runtimeLicense;

		public string QbConnectorURL {
			get { return qbConnectorURL; }
			set { qbConnectorURL = value; }
		}

		public int QbConnectorPort {
			get { return qbConnectorPort; }
			set { qbConnectorPort = value; }
		}

		public string QbConnectorUser {
			get { return qbConnectorUser; }
			set { qbConnectorUser = value; }
		}

		public int QbConnectorTimeout {
			get { return qbConnectorTimeout; }
			set { qbConnectorTimeout = value; }
		}

		public string QbConnectorPassword {
			get { return qbConnectorPassword; }
			set { qbConnectorPassword = value; }
		}

		public int QbConnectorReturnCode {
			get { return qbConnectorReturnCode; }
			set { qbConnectorReturnCode = value; }
		}

		public string QbConnectorMessage {
			get { return qbConnectorMessage; }
			set { qbConnectorMessage = value; }
		}

		public bool QbIsLoggingEnabled {
			get { return qbIsLoggingEnabled; }
			set { qbIsLoggingEnabled = value; }
		}

		public string ConnString {
			get {
				// QB Connection string has embedded quotes
				string connect = "URL=\"" + qbConnectorURL + ":" + qbConnectorPort.ToString() + "\"" +
					   " User=\"" + qbConnectorUser + "\"" + " Password=\"" + qbConnectorPassword + "\"";

				if (QbConnectorTimeout > -1)
					connect += " Timeout=\"" + QbConnectorTimeout.ToString() + "\"";

				return connect;
			}
		}

		#endregion Public Properties

		public BGQuickBooks(UserConnection userConnection) {
			this.userConnection = userConnection;

			ClearForNewQuery();

			qbConnectorUser = Terrasoft.Core.Configuration.SysSettings.GetValue<string>(userConnection, "BGQuickBooksLocalUser", "");
			qbConnectorPassword = Terrasoft.Core.Configuration.SysSettings.GetValue<string>(userConnection, "BGQuickBooksLocalPassword", "");
			qbConnectorURL = Terrasoft.Core.Configuration.SysSettings.GetValue<string>(userConnection, "BGQuickBooksLocalUrl", "");
			qbConnectorPort = Terrasoft.Core.Configuration.SysSettings.GetValue<int>(userConnection, "BGQuickBooksLocalPort", 99);
			qbConnectorTimeout = Terrasoft.Core.Configuration.SysSettings.GetValue<int>(userConnection, "BGQuickBooksLocalTimeout", 90);
		}

		/// <summary>
		/// Clears connector return values
		/// </summary>
		public void ClearForNewQuery() {
			qbConnectorReturnCode = 0;
			qbConnectorMessage = string.Empty;
		}

		public void LogException(string entity, InQBException ex) {
			QbConnectorReturnCode = ex.Code;
			QbConnectorMessage = ex.Code == 702 ? $"{entity} not found in QuickBooks." : $"Error: {ex.Message}";
		}
	}

	internal static class BGQuickBooksServiceHelpers {

		/// <summary>
		/// Converts <see cref="BGAccountAddress"/> from Creatio into a <see cref="Address"/> from QuickBooks
		/// </summary>
		/// <param name="accountAddress"></param>
		/// <returns></returns>
		internal static Address GetQuickBooksAddress(this BGAccountAddress accountAddress) {
			if (accountAddress.AddressTypeId == BGAccountAddressTypes.Billing)
				return accountAddress.GetQuickBooksBilllingAddress();

			if (accountAddress.AddressTypeId == BGAccountAddressTypes.Shipping)
				return accountAddress.GetQuickBooksShippingAddress();

			return new Address();
		}

		private static Address GetQuickBooksBilllingAddress(this BGAccountAddress accountAddress) {
			Address qbAddress = new Address {
				PostalCode = accountAddress.Zip,
				Line1 = accountAddress.Address?.Truncate(BGQuickBooks.QB_ADDR_LINE_MAXLEN) ?? ""
			};

			if (accountAddress.City != null)
				qbAddress.City = accountAddress.City.Name;
			if (accountAddress.State != null)
				qbAddress.State = accountAddress.State.Name;
			if (accountAddress.Country != null)
				qbAddress.Country = accountAddress.Country.Name;

			return qbAddress;
		}

		private static Address GetQuickBooksShippingAddress(this BGAccountAddress accountAddress) {
			Address qbAddress = new Address {
				PostalCode = accountAddress.Zip,
				Line1 = accountAddress.BGDestinationName?.Truncate(BGQuickBooks.QB_ADDR_LINE_MAXLEN) ?? "",
				Line2 = accountAddress.Address?.Truncate(BGQuickBooks.QB_ADDR_LINE_MAXLEN) ?? ""
			};

			if (!string.IsNullOrWhiteSpace(accountAddress.BGAddressLine2))
				qbAddress.Line3 = accountAddress.BGAddressLine2?.Truncate(BGQuickBooks.QB_ADDR_LINE_MAXLEN) ?? "";

			if (accountAddress.City != null)
				qbAddress.City = accountAddress.City.Name;
			if (accountAddress.State != null)
				qbAddress.State = accountAddress.State.Name;
			if (accountAddress.Country != null)
				qbAddress.Country = accountAddress.Country.Name;

			return qbAddress;
		}
	}

	#region QuickBooks

	internal class BGQuickBooksCustomer {

		/// <summary>
		/// Gets the customer by their QB Id, if the <paramref name="customer"/> doesn't have a QB Id it tries find it by the Name
		/// If not it creates a new record in QB for this <paramref name="customer"/> and updates the qbId of the customer in Creatio
		/// </summary>
		/// <param name="config"></param>
		/// <param name="customer"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Customer GetOrCreate(BGQuickBooks config, BGAccount customer, UserConnection userConnection) {
			Customer qbObj = null;

			try {
				//Get Customer By Id first
				if (!string.IsNullOrWhiteSpace(customer.BGQuickBooksId))
					qbObj = GetById(config, customer.BGQuickBooksId);

				//Not found by Id find by name (Name is unique in QB)
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					string cName = (!string.IsNullOrWhiteSpace(customer.BGQBName)) ? customer.BGQBName : customer.Name;

					qbObj = GetByName(config, cName);

					if (!string.IsNullOrWhiteSpace(qbObj?.RefId)) {
						customer.BGQuickBooksId = qbObj.RefId;
						customer.UpdateQuickBooksId(userConnection);
					}
				}

				//If it's still not found then create
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					qbObj = Create(config, customer);

					customer.BGQuickBooksId = qbObj.RefId;
					customer.UpdateQuickBooksId(userConnection);
				}
			}
			catch (Exception ex) {
				throw new Exception($"Failed to Find Or Create customer ({config.QbConnectorMessage}) [{qbObj?.RefId} | {customer.Id} | {customer.Name}] in QuickBooks\n", ex);
			}

			return qbObj;
		}

		/// <summary>
		/// Find Customer in QuickBooks by Id
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		internal static Customer GetById(BGQuickBooks config, string qbId) {
			Customer qbObj = new Customer();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Customer By Id ({qbId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.Get(qbId);
			}
			catch (InQBException ex) {
				if (!(ex?.Code == 881 && ex?.Message?.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Find Customer in QuickBooks By Name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbName"></param>
		/// <returns></returns>
		internal static Customer GetByName(BGQuickBooks config, string qbName) {
			Customer qbObj = new Customer();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Customer By Name ({qbName})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.GetByName(qbName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates the customer, customer address and contact in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="cust"></param>
		/// <returns></returns>
		internal static Customer Create(BGQuickBooks config, BGAccount cust) {
			Customer qbObj = new Customer() {
				CompanyName = string.IsNullOrWhiteSpace(cust.BGQBName) ? cust.Name : cust.BGQBName,
				CustomerName = string.IsNullOrWhiteSpace(cust.BGQBName) ? cust.Name : cust.BGQBName,
				QBConnectionString = config.ConnString,
				RuntimeLicense = config.RuntimeLicense
			};

			config.ClearForNewQuery();
			config.QbConnectorMessage = "Create Customer";

			//Create the address if doesn't exits
			if (cust.BillingAddress != null)
				qbObj.BillingAddress = cust.BillingAddress.GetQuickBooksAddress().Aggregate;

			if (!string.IsNullOrWhiteSpace(cust.Notes))
				qbObj.Notes = cust.Notes;

			if (cust.PrimaryContact != null) {
				if (!string.IsNullOrWhiteSpace(cust.PrimaryContact.Name))
					qbObj.ContactName = cust.PrimaryContact.Name;
				if (!string.IsNullOrWhiteSpace(cust.PrimaryContact.Phone))
					qbObj.Phone = cust.PrimaryContact.Phone;
				if (!string.IsNullOrWhiteSpace(cust.PrimaryContact.Fax))
					qbObj.Fax = cust.PrimaryContact.Fax;
				if (!string.IsNullOrWhiteSpace(cust.PrimaryContact.Email))
					qbObj.Email = cust.PrimaryContact.Email;
			}

			qbObj.Add();

			return qbObj;
		}
	}

	internal class BGQuickBooksBuyer {

		/// <summary>
		/// Gets the buyer by their QB Id, if the <paramref name="buyer"/> doesn't have a QB Id it tries find it by the Name
		/// If not it creates a new record in QB for this <paramref name="buyer"/> and updates the qbId of the buyer in Creatio
		/// </summary>
		/// <param name="config"></param>
		/// <param name="buyer"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		/// <exception cref="Exception"></exception>
		internal static Qblists GetOrCreate(BGQuickBooks config, BGContact buyer, UserConnection userConnection) {
			Qblists qbObj = new Qblists();

			try {
				//Get Customer By Id first
				if (!string.IsNullOrWhiteSpace(buyer.BGQuickBooksId))
					qbObj = GetById(config, buyer.BGQuickBooksId);

				//Not found by Id find by name (Name is unique in QB)
				if (string.IsNullOrWhiteSpace(qbObj?.RefId) && !string.IsNullOrWhiteSpace(buyer.BGBuyerCode)) {
					qbObj = GetByName(config, buyer.BGBuyerCode);

					if (!string.IsNullOrWhiteSpace(qbObj?.RefId)) {
						buyer.BGQuickBooksId = qbObj.RefId;
						buyer.UpdateQuickBooksId(userConnection);
					}
				}

				//If it's still not found then create
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					qbObj = Create(config, buyer);

					buyer.BGQuickBooksId = qbObj.RefId;
					buyer.UpdateQuickBooksId(userConnection);
				}
			}
			catch (Exception ex) {
				throw new Exception($"Failed to Find Or Create Buyer in QuickBooks ({config.QbConnectorMessage}): {buyer.BGBuyerCode}\n", ex);
			}

			return qbObj;
		}

		/// <summary>
		/// Find Sales Rep (buyer) by QuickBooks Id
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		private static Qblists GetById(BGQuickBooks config, string quickBooksId) {
			Qblists qbObj = new Qblists();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Buyer By Id ({quickBooksId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.ListType = QblistsListTypes.ltSalesRep;

				qbObj.Get(quickBooksId);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Find Sales Rep (buyer) in QuickBooks By Name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbName"></param>
		/// <returns></returns>
		internal static Qblists GetByName(BGQuickBooks config, string qbName) {
			Qblists qbObj = new Qblists();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Buyer By Name ({qbName})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.ListType = QblistsListTypes.ltSalesRep;

				qbObj.GetByName(qbName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates Sales Rep (Buyer) in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="cust"></param>
		/// <returns></returns>
		internal static Qblists Create(BGQuickBooks config, BGContact buyer) {
			// Before adding the sales rep, the name has to exist as a QuickBooks OtherName object.
			Qbobject other = BGQuickBooksOther.GetOrCreate(config, buyer.Name);
			//string otherKey = qbOther.GetProperty("ListID");
			Qblists qbObj = null;

			if (!string.IsNullOrWhiteSpace(other?.QBResponseAggregate)) {
				config.ClearForNewQuery();
				config.QbConnectorMessage = "Create Buyer";

				qbObj = new Qblists {
					QBConnectionString = config.ConnString,
					RuntimeLicense = config.RuntimeLicense,

					ListType = QblistsListTypes.ltSalesRep,
					QBName = buyer.BGBuyerCode.Trim(),
					SalesRepEntityName = buyer.Name.Trim()
				};

				qbObj.Add();
			}

			return qbObj;
		}
	}

	internal class BGQuickBooksOther {

		/// <summary>
		/// Get Or Create OtherName in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="otherName"></param>
		/// <returns></returns>
		/// <exception cref="Exception"></exception>
		internal static Qbobject GetOrCreate(BGQuickBooks config, string otherName) {
			Qbobject qbObj = null;

			if (!string.IsNullOrWhiteSpace(otherName)) {
				try {
					qbObj = GetByName(config, otherName);

					//If it's still not found then create
					if (string.IsNullOrWhiteSpace(qbObj?.QBResponseAggregate)) {
						qbObj = Create(config, otherName);
					}
				}
				catch (Exception ex) {
					throw new Exception($"Failed to Find Or Create Product in QuickBooks Name: {otherName}\n{ex}\n", ex);
				}
			}

			return qbObj;
		}

		/// <summary>
		/// Find OtherName in QuickBooks By Name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="otherName"></param>
		/// <returns></returns>
		internal static Qbobject GetByName(BGQuickBooks config, string otherName) {
			Qbobject qbObj = new Qbobject();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Other Name by Name ({otherName})";
				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.ObjectName = "OtherName";
				qbObj.ObjectType = "List";

				qbObj.GetByName(otherName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates OtherName in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="cust"></param>
		/// <returns></returns>
		internal static Qbobject Create(BGQuickBooks config, string otherName) {
			Qbobject qbObj = new Qbobject();

			config.ClearForNewQuery();
			config.QbConnectorMessage = $"Create Other Name ({otherName})";
			qbObj.QBConnectionString = config.ConnString;
			qbObj.RuntimeLicense = config.RuntimeLicense;

			qbObj.ObjectName = "OtherName";
			qbObj.ObjectType = "List";
			qbObj.AddProperty("Name", otherName);

			qbObj.Add();

			return qbObj;
		}
	}

	internal class BGQuickBooksVendor {

		/// <summary>
		/// Gets or Creates a <see cref="Vendor"/> in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="vendor"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		/// <exception cref="Exception"></exception>
		internal static Vendor GetOrCreate(BGQuickBooks config, BGAccount vendor, UserConnection userConnection) {
			Vendor qbObj = null;

			try {
				//Get vendor by Id first
				if (!string.IsNullOrWhiteSpace(vendor.BGQuickBooksId))
					qbObj = GetById(config, vendor.BGQuickBooksId);

				//Not found by Id find by name (Name is unique in QB)
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					string name = string.IsNullOrWhiteSpace(vendor.BGQBName) ? vendor.Name : vendor.BGQBName;
					qbObj = GetByName(config, name);

					if (!string.IsNullOrWhiteSpace(qbObj?.RefId)) {
						vendor.BGQuickBooksId = qbObj.RefId;
						vendor.UpdateQuickBooksId(userConnection);
					}
				}

				//If it's still not found then create
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					qbObj = Create(config, vendor);

					vendor.BGQuickBooksId = qbObj.RefId;
					vendor.UpdateQuickBooksId(userConnection);
				}
			}
			catch (Exception ex) {
				throw new Exception($"Failed to Find Or Create Vendor ({config.QbConnectorMessage}) [{vendor.Id} | {vendor.Name}] in QuickBooks\n", ex);
			}

			return qbObj;
		}

		/// <summary>
		/// Find vendor in QuickBooks by Id
		/// </summary>
		/// <param name="config"></param>
		/// <param name="quickBooksId"></param>
		/// <returns></returns>
		internal static Vendor GetById(BGQuickBooks config, string quickBooksId) {
			Vendor qbObj = new Vendor();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Vendor By Id ({quickBooksId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.Get(quickBooksId);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Find vendor in QuickBooks By Name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbName"></param>
		/// <returns></returns>
		internal static Vendor GetByName(BGQuickBooks config, string qbName) {
			Vendor qbObj = new Vendor();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Vendor By Name ({qbName})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.GetByName(qbName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates the vendor, vendor address and contact in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="vendor"></param>
		/// <returns></returns>
		internal static Vendor Create(BGQuickBooks config, BGAccount vendor) {
			string name = string.IsNullOrWhiteSpace(vendor.BGQBName) ? vendor.Name : vendor.BGQBName;

			Vendor qbObj = new Vendor() {
				CompanyName = name,
				VendorName = name
			};

			config.ClearForNewQuery();
			config.QbConnectorMessage = "Create Vendor";

			qbObj.QBConnectionString = config.ConnString;
			qbObj.RuntimeLicense = config.RuntimeLicense;

			//Create the address if doesn't exits
			if (vendor.BillingAddress != null)
				qbObj.Address = vendor.BillingAddress.GetQuickBooksAddress().Aggregate;

			if (!string.IsNullOrWhiteSpace(vendor.Notes))
				qbObj.Notes = vendor.Notes;

			if (vendor.PrimaryContact != null) {
				if (!string.IsNullOrWhiteSpace(vendor.PrimaryContact.Name))
					qbObj.ContactName = vendor.PrimaryContact.Name;
				if (!string.IsNullOrWhiteSpace(vendor.PrimaryContact.Phone))
					qbObj.Phone = vendor.PrimaryContact.Phone;
				if (!string.IsNullOrWhiteSpace(vendor.PrimaryContact.Fax))
					qbObj.Fax = vendor.PrimaryContact.Fax;
				if (!string.IsNullOrWhiteSpace(vendor.PrimaryContact.Email))
					qbObj.Email = vendor.PrimaryContact.Email;
			}

			qbObj.Add();

			return qbObj;
		}
	}

	internal class BGQuickBooksItem {

		/// <summary>
		/// Gets the products by their QB Ids, if the <paramref name="oProducts"/> don't have a QuickBooksId then it tries to find them by the SKU
		/// If not it creates a new record in QB for each <paramref name="oProducts"/> and updates the qbId of each Product in Creatio
		/// </summary>
		/// <param name="config"></param>
		/// <param name="oProducts"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static List<Item> GetOrCreate(BGQuickBooks config, List<BGOrderProduct> oProducts, UserConnection userConnection) {
			List<Item> qbObjs = new List<Item>();

			foreach (BGOrderProduct oProduct in oProducts) {
				Item item = GetOrCreate(config, oProduct.Product, userConnection);
				if (item != null)
					qbObjs.Add(item);
			}

			return qbObjs;
		}

		/// <summary>
		/// Gets the products by their QB Ids, if the <paramref name="inventoryProducts"/> don't have a QuickBooksId then it tries to find them by the SKU
		/// If not it creates a new record in QB for each <paramref name="inventoryProducts"/> and updates the qbId of each Product in Creatio
		/// </summary>
		/// <param name="config"></param>
		/// <param name="inventoryProducts"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static List<Item> GetOrCreate(BGQuickBooks config, List<BGProductsInInventoryAdjustment> inventoryProducts, UserConnection userConnection) {
			List<Item> qbObjs = new List<Item>();
			foreach (BGProductsInInventoryAdjustment inventoryProduct in inventoryProducts) {
				Item item = GetOrCreate(config, inventoryProduct.BGProduct, userConnection);
				if (item != null)
					qbObjs.Add(item);
			}

			return qbObjs;
		}

		/// <summary>
		/// Gets the product by the QB Id, if the <paramref name="item"/> doesn't have a QuickBooksId then it tries to find it by the SKU
		/// If not it creates a new record in QB for this <paramref name="item"/> and updates the qbId of the Products in Creatio
		/// </summary>
		/// <param name="config"></param>
		/// <param name="item"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Item GetOrCreate(BGQuickBooks config, BGProduct item, UserConnection userConnection) {
			Item qbObj = null;

			try {
				//Get Customer By Id first
				if (!string.IsNullOrWhiteSpace(item.BGQuickBooksId))
					qbObj = GetById(config, item.BGQuickBooksId);

				//Not found by Id find by name (Name is unique in QB)
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					qbObj = GetByName(config, item.Code);

					if (!string.IsNullOrWhiteSpace(qbObj?.RefId)) {
						item.BGQuickBooksId = qbObj.RefId;
						item.UpdateQuickBooksId(userConnection);
					}
				}

				//If it's still not found then create
				if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					qbObj = Create(config, item);

					item.BGQuickBooksId = qbObj.RefId;
					item.UpdateQuickBooksId(userConnection);
				}
			}
			catch (Exception ex) {
				throw new Exception($"Failed to Find Or Create Item in QuickBooks ({config.QbConnectorMessage}) Id: {item.Id} | Name: {item.Code}\n", ex);
			}

			return qbObj;
		}

		/// <summary>
		/// Find item by QuickBooks Id
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		private static Item GetById(BGQuickBooks config, string quickBooksId) {
			Item qbObj = new Item();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Item By Id ({quickBooksId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.Get(quickBooksId);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Find item by SKU
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		private static Item GetByName(BGQuickBooks config, string qbName) {
			Item qbObj = new Item();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Item By Name ({qbName})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.GetByName(qbName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates the item
		/// </summary>
		/// <param name="config"></param>
		/// <param name="cust"></param>
		/// <returns></returns>
		private static Item Create(BGQuickBooks config, BGProduct item) {
			config.ClearForNewQuery();
			config.QbConnectorMessage = "Create Item";

			Item qbObj = new Item {
				QBConnectionString = config.ConnString,
				ItemName = item.Code,
				Description = item.BGDescription,
				AccountName = BGQuickBooks.QBACCT_ACCOUNT,
				ItemType = ItemItemTypes.itInventory,
				RuntimeLicense = config.RuntimeLicense
			};
			qbObj.Purchase.Description = item.BGDescription;
			qbObj.Purchase.Cost = item.Price.ToString();

			qbObj.Purchase.COGSAccountName = BGQuickBooks.QBACCT_COGS;
			qbObj.Purchase.AssetAccountName = BGQuickBooks.QBACCT_ASSET;

			qbObj.Add();

			qbObj.SetCustomField(BGQuickBooks.CustomFieldNamePacking, item.BGItemsPerMaster.ToString());

			return qbObj;
		}

		#region Subtotal

		/// <summary>
		/// Find or adds a subtotal item for orders/invoices to use
		/// </summary>
		/// <returns></returns>
		internal static string FindOrAddSubtotalItem(BGQuickBooks config) {
			Item qbObj = GetByName(config, BGQuickBooks.QBACCT_SUBTOTAL);

			if (string.IsNullOrWhiteSpace(qbObj?.RefId))
				qbObj = CreateSubtotalItem(config, BGQuickBooks.QBACCT_SUBTOTAL, BGQuickBooks.QBACCT_SUBTOTAL_DESCR);

			return qbObj.RefId;
		}

		/// <summary>
		/// Creates the subtotal item in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="name"></param>
		/// <param name="description"></param>
		/// <returns></returns>
		private static Item CreateSubtotalItem(BGQuickBooks config, string name, string description) {
			Item qbObj = new Item();

			config.ClearForNewQuery();
			config.QbConnectorMessage = $"Create Subtotal Item, name: {name}, description: {description}";

			qbObj.QBConnectionString = config.ConnString;
			qbObj.RuntimeLicense = config.RuntimeLicense;

			qbObj = new Item {
				ItemType = ItemItemTypes.itSubtotal,
				ItemName = name,
				Description = description
			};

			qbObj.Add();

			return qbObj;
		}

		#endregion Subtotal

		#region Discount

		/// <summary>
		/// Find or adds a discount item for orders/invoices to use
		/// </summary>
		/// <returns></returns>
		internal static Item FindOrAddDiscountItem(BGQuickBooks config, decimal discPer, string discReason) {
			string discName = discPer.ToString("F2") + "% Discount";
			Item qbObj = GetByDiscountName(config, discName);

			if (string.IsNullOrWhiteSpace(qbObj?.RefId))
				qbObj = CreateDiscountItem(config, discPer, discReason, BGQuickBooks.QBACCT_DISCOUNT);

			return qbObj;
		}

		/// <summary>
		/// Find discount by name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		private static Item GetByDiscountName(BGQuickBooks config, string qbName) {
			config.ClearForNewQuery();
			config.QbConnectorMessage = $"Get Discount By Name {qbName}";

			Item qbObj = new Item();

			try {
				Objsearch qbSearch = new Objsearch {
					QueryType = ObjsearchQueryTypes.qtItemSearch,
					QBConnectionString = config.ConnString,
					RuntimeLicense = config.RuntimeLicense
				};

				qbSearch.SearchCriteria.ItemType = SearchItemTypes.sitDiscount;
				qbSearch.SearchCriteria.NameStartsWith = qbName;
				qbSearch.Search();

				if (qbSearch.Results.Count > 0) {
					qbObj = new Item {
						QBResponseAggregate = qbSearch.Results[0].Aggregate
					};
				}
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates the discount item in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="name"></param>
		/// <param name="discReason"></param>
		/// <returns></returns>
		private static Item CreateDiscountItem(BGQuickBooks config, decimal discount, string discReason, string discAcc) {
			Item qbObj = new Item();

			config.ClearForNewQuery();
			config.QbConnectorMessage = $"Create Discount Item, name: {discount.ToString("F2") + "% Discount"}, description {discReason}";
			;
			qbObj = new Item {
				ItemType = ItemItemTypes.itDiscount,
				ItemName = discount.ToString("F2") + "% Discount",
				Description = discReason,
				AccountName = discAcc,
				PricePercent = discount.ToString("F2"),
				RuntimeLicense = config.RuntimeLicense,
				QBConnectionString = config.ConnString
			};

			qbObj.Add();

			return qbObj;
		}

		#endregion Discount

		#region Other Charge

		/// <summary>
		/// Find or adds a subtotal item for orders/invoices to use
		/// </summary>
		/// <returns></returns>
		internal static Item FindOrAddOtherChargeItem(BGQuickBooks config, string name, string description, string account, string amountOrPct) {
			Item qbObj = GetByOtherChargeName(config, name);

			if (string.IsNullOrWhiteSpace(qbObj?.RefId))
				qbObj = CreateOtherChargeItem(config, name, description, account, amountOrPct);

			return qbObj;
		}

		/// <summary>
		/// Find Other Charge by Name
		/// </summary>
		/// <param name="config"></param>
		/// <param name="qbId"></param>
		/// <returns></returns>
		private static Item GetByOtherChargeName(BGQuickBooks config, string qbName) {
			Item qbObj = new Item();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Other Charge Name By Name {qbName}";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.GetByName(qbName);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Creates the other charge item in QuickBooks
		/// </summary>
		/// <param name="config"></param>
		/// <param name="name"></param>
		/// <param name="description"></param>
		/// <returns></returns>
		private static Item CreateOtherChargeItem(BGQuickBooks config, string name, string description, string account, string amountOrPct) {
			Item qbObj = new Item();

			config.ClearForNewQuery();
			config.QbConnectorMessage = $"Create Other Charge Item, name: {name}, description: {description}, account: {account}, amountOrPct: {amountOrPct}";
			qbObj = new Item {
				ItemType = ItemItemTypes.itOtherCharge,
				ItemName = name,
				Description = description,
				AccountName = account,
				RuntimeLicense = config.RuntimeLicense,
				QBConnectionString = config.ConnString
			};

			if (!string.IsNullOrEmpty(amountOrPct))
				qbObj.Price = amountOrPct;

			qbObj.Add();

			return qbObj;
		}

		#endregion Other Charge
	}

	internal class BGQuickBooksInvoice {

		/// <summary>
		/// Gets the Invoice by the <paramref name="quickBooksId"/> or <paramref name="invoiceNumber"/>
		/// (<paramref name="quickBooksId"/> has preference)
		/// </summary>
		/// <param name="serviceContext"></param>
		/// <param name="invoiceNumber"></param>
		/// <param name="quickBooksId"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Invoice GetInvoiceByInvoiceNumberOrQuickBooksId(BGQuickBooks config, BGOrder order, UserConnection userConnection) {
			Invoice qbObj = null;

			if (!string.IsNullOrWhiteSpace(order.BGQuickBooksId))
				qbObj = GetInvoiceByQuickBooksId(config, order.BGQuickBooksId);

			if (string.IsNullOrWhiteSpace(qbObj?.RefId)) {
				qbObj = GetInvoiceByInvoiceNumber(config, order.InvoiceNumber);

				//If Invoice is found by Invoice Number then update Creatio's Order}
				if (!string.IsNullOrWhiteSpace(qbObj?.RefId)) {
					order.BGQuickBooksId = qbObj.RefId;
					order.UpdateQuickBooksId(userConnection);
				}
			}

			return qbObj;
		}

		/// <summary>
		/// Gets an Invoice by the given <paramref name="quickBooksId"/>
		/// </summary>
		/// <param name="serviceContext"></param>
		/// <param name="quickBooksId"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Invoice GetInvoiceByQuickBooksId(BGQuickBooks config, string quickBooksId) {
			Invoice qbObj = new Invoice();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Invoice From QB ({quickBooksId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.Get(quickBooksId);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}

		/// <summary>
		/// Gets an Invoice by the given <paramref name="invoiceNumber"/>
		/// </summary>
		/// <param name="serviceContext"></param>
		/// <param name="invoiceNumber"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Invoice GetInvoiceByInvoiceNumber(BGQuickBooks config, string invoiceNumber) {
			Invoice qbObj = new Invoice();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get Invoice By Invoice Number ({invoiceNumber})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				Objsearch search = new Objsearch {
					QBConnectionString = config.ConnString,
					RuntimeLicense = config.RuntimeLicense,
					QueryType = ObjsearchQueryTypes.qtInvoiceSearch,
				};

				search.SearchCriteria.RefNumber = invoiceNumber;

				search.Search();

				if (search.Results.Count > 0) {
					qbObj.QBResponseAggregate = search.Results[0].Aggregate;

					if (search.Results.Count > 1) {
						config.QbConnectorReturnCode = -1;
						config.QbConnectorMessage = "Duplicate invoice numbers found.";
					}
				} else {
					config.QbConnectorReturnCode = 702;
					config.QbConnectorMessage = "Invoice not found in Quickbooks.";
				}
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}
	}

	internal class BGQuickBooksPurchaseOrder {

		/// <summary>
		/// Gets the purchase order by the quickBooksId
		/// </summary>
		/// <param name="config"></param>
		/// <param name="order"></param>
		/// <returns></returns>
		internal static Purchaseorder GetPurchaseOrderByQuickBooksId(BGQuickBooks config, BGOrder order) {
			Purchaseorder qbPurchaseOrder = new Purchaseorder();

			if (!string.IsNullOrWhiteSpace(order.BGQuickBooksId))
				qbPurchaseOrder = GetPurchaseOrderByQuickBooksId(config, order.BGQuickBooksId);

			return qbPurchaseOrder;
		}

		/// <summary>
		/// Gets an Invoice by the given <paramref name="quickBooksId"/>
		/// </summary>
		/// <param name="config"></param>
		/// <param name="quickBooksId"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		internal static Purchaseorder GetPurchaseOrderByQuickBooksId(BGQuickBooks config, string quickBooksId) {
			Purchaseorder qbObj = new Purchaseorder();

			try {
				config.ClearForNewQuery();
				config.QbConnectorMessage = $"Get PurchaseOrder By QuickBooksId ({quickBooksId})";

				qbObj.QBConnectionString = config.ConnString;
				qbObj.RuntimeLicense = config.RuntimeLicense;

				qbObj.Get(quickBooksId);
			}
			catch (InQBException ex) {
				if (!(ex.Code == 881 && ex.Message.Contains("could not be found") == true))
					throw ex;
			}

			return qbObj;
		}
	}

	#endregion QuickBooks

	public static class BGQuickBooksLogType {
		public const string Commission = "93d75da5-3101-49f2-9829-7eb7025205cc";
		public const string CustomerOrder = "14535998-d4c0-45ac-bbac-8c0185bfcc1a";
		public const string FactoryOrder = "1f2a682d-0d58-4a7a-89fa-3a7622d79c12";
		public const string InventoryAdjustment = "e918270e-770e-4265-98be-2c6436178aa6";
	}

	public static class BGQuickBooksLogStatus {
		public const string Error = "bdfc60c7-55fd-4cbd-9a2c-dca2def46d80";
		public const string Pending = "c97db3bc-634d-4c90-8432-ec7141c87640";
		public const string Processed = "e7428193-4cf1-4d1b-abae-00e93ab5e1c5";
		public const string Processing = "fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef";
		public const string ReProcess = "ff92e20c-da27-4255-96bc-57e32f0944f4";
	}

	public static class BGQuickBooksLogAction {
		public const string Delete = "1569077b-41ca-4267-b07c-96277fa979fc";
		public const string Insert = "facb63c3-3599-4cb5-b86d-179b0636a3cb";
		public const string Log = "44ff0873-6f74-490a-8088-10670bbd8180";
		public const string Update = "9065a18f-7c4c-49fb-a9ec-4f6f9d342c43";
	}

	public class BGQuickBooksLogDetail {
		public const string TableName = "BGQuickBooksIntegrationLogDetail";
		public string Id { get; set; }
		public string Name { get; set; }
		public string ActionId { get; set; }
		public string RecordId { get; set; }
		public string TypeId { get; set; }
		public string BGStatusId { get; set; }

		public string ErrorMsg { get; set; } = "";

		public BGOrder Order { get; set; }

		public BGInventoryAdjustment InventoryAdjustment { get; set; }

		public static void ProcessDetailLogs(UserConnection userConnection) {
			BGQuickBooks config = new BGQuickBooks(userConnection);

			ProcessCustomerOrders(config, userConnection);
			ProcessFactoryOrders(config, userConnection);
			ProcessInventoryAdjustments(config, userConnection);
		}

		#region Customer Orders

		/// <summary>
		///	Process all Customer ORders that need to be processed
		/// </summary>
		/// <param name="userConnection"></param>
		/// <exception cref="Exception"></exception>
		public static void ProcessCustomerOrders(BGQuickBooks config, UserConnection userConnection) {
			List<BGQuickBooksLogDetail> logDetails = GetQuickBooksPendingLogsByType(BGQuickBooksLogType.CustomerOrder, userConnection);

			bool anyError = false;

			//If there are no log Details exit as there are no Customer Orders to process
			if (logDetails is null || logDetails.Count == 0)
				return;

			try {
				//Set logs being processed as processing
				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Processing, userConnection);

				//Get Order Data
				List<string> orderIds = logDetails.Select(x => x.RecordId).Distinct().ToList();
				List<BGOrder> customerOrders = BGOrder.GetByIds(orderIds, userConnection);
				List<BGOrderProduct> ordersProducts = BGOrderProduct.GetAllByOrderIds(orderIds, userConnection);

				foreach (BGQuickBooksLogDetail logDetail in logDetails) {
					try {
						logDetail.Order = customerOrders?.FirstOrDefault(co => co.Id.ToString() == logDetail.RecordId);
						if (logDetail.Order != null) {
							logDetail.Order.BGSalesOrderItems = ordersProducts.Where(p => p.BGOrderId == logDetail.Order.Id)?.ToList();
							logDetail.Order.BGCustomer = BGAccount.GetById(logDetail.Order.BGCustomer.Id, userConnection);

							ProcessCustomerOrderLogDetail(config, logDetail, userConnection);
						} else {
							logDetail.ErrorMsg = $"Customer Order \"{logDetail.Name}\" was not found.";
							logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
							logDetail.UpdateLogStatus(userConnection);
						}
					}
					catch (Exception ex) {
						logDetail.ErrorMsg = ex.ToString() + $"\n({config.QbConnectorMessage})\nExtraDetails: \n" + logDetail.ErrorMsg;
						logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
						logDetail.UpdateLogStatus(userConnection);
						anyError = true;
					}
				}
			}
			//Issues in Creatio throw exception
			catch (Exception ex) {
				string errorMsg = "\n" + ex.ToString() + "\n" + ex.Message.ToString() + $"\n({config.QbConnectorMessage})\n";

				logDetails.ForEach(l => l.ErrorMsg = errorMsg);

				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Error, userConnection);
				CreateInvoiceErrorNotf(userConnection);

				throw new Exception(errorMsg);
			}

			if (anyError)
				CreateInvoiceErrorNotf(userConnection);
		}

		/// <summary>
		/// Adds data to quickbooks for the customer orders from the customer order log detail
		/// </summary>
		/// <param name="logDetail"></param>
		/// <param name="userConnection"></param>
		public static void ProcessCustomerOrderLogDetail(BGQuickBooks config, BGQuickBooksLogDetail logDetail, UserConnection userConnection) {
			BGOrder order = logDetail.Order;
			List<BGOrderProduct> orderProducts = logDetail.Order.BGSalesOrderItems;

			//Nothing to process return;
			if (orderProducts.Count <= 0 && !orderProducts.Any(x => x.BGItemQuantity > 0) && logDetail.ActionId.ToLower() != BGQuickBooksLogAction.Delete) {
				logDetail.ErrorMsg = "The order has no products or not a single product has a quantity greater than 0";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			//#########################################################
			Invoice qbInvoice = BGQuickBooksInvoice.GetInvoiceByInvoiceNumberOrQuickBooksId(config, order, userConnection);

			#region Delete

			//If it's a delete just simply stop after the delete
			if (logDetail.ActionId.ToLower() == BGQuickBooksLogAction.Delete) {
				if (!string.IsNullOrWhiteSpace(order.BGQuickBooksId)) {
					qbInvoice.Delete();
					config.QbConnectorMessage = "QBInvoice Delete";

					order.BGQuickBooksId = string.Empty;
					order.UpdateQuickBooksId(userConnection);
				}

				//If there are no execptions it means it has either created or updated the invoice
				logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				logDetail.ErrorMsg = "The customer order was deleted successfully.";
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			#endregion Delete

			//Find or Create products for later use
			_ = BGQuickBooksItem.GetOrCreate(config, orderProducts, userConnection);

			//Find or Create the Account in QuickBooks
			Customer qbCustomer = BGQuickBooksCustomer.GetOrCreate(config, order.BGCustomer, userConnection);

			Qblists qbRep = null;
			if (!string.IsNullOrWhiteSpace(order.BGBuyersName?.BGBuyerCode))
				qbRep = BGQuickBooksBuyer.GetOrCreate(config, order.BGBuyersName, userConnection);

			//If invoice is not found then a new invoice should be created
			bool isNewInvoice = false;
			if (string.IsNullOrWhiteSpace(order.BGQuickBooksId)) {
				qbInvoice = new Invoice();
				isNewInvoice = true;
			}

			qbInvoice.RuntimeLicense = config.RuntimeLicense;
			qbInvoice.QBConnectionString = config.ConnString;

			if (qbRep != null)
				qbInvoice.SalesRepId = qbRep.RefId;

			//Fill Invoice Data
			qbInvoice.CustomerId = qbCustomer.RefId;
			qbInvoice.TaxItemName = order.BGTaxCheckbox ? "NJ" : "NO_TAX";
			qbInvoice.RefNumber = order.InvoiceNumber;

			string poNumber = order.BGPONumber?.Replace(":", "")?.Truncate(25) ?? "";
			qbInvoice.PONumber = poNumber;

			qbInvoice.QBXMLVersion = "6.0";
			if (order.BGInvoiceDate != default || order.CreatedOn != default)
				qbInvoice.TransactionDate = string.Format("{0:yyyy-MM-dd}", order.BGInvoiceDate != default ? order.BGInvoiceDate : order.CreatedOn);

			if (order.BGInvoiceDueDate != default)
				qbInvoice.DueDate = string.Format("{0:yyyy-MM-dd}", order.BGInvoiceDueDate);

			if (order.BGShipDate != default)
				qbInvoice.ShipDate = string.Format("{0:yyyy-MM-dd}", order.BGShipDate);

			if (order.BGShippingAddress != null)
				qbInvoice.ShippingAddress = order.BGShippingAddress.GetQuickBooksAddress().Aggregate;

			List<InvoiceItem> lines = new List<InvoiceItem>();
			qbInvoice.LineItems.Clear();

			foreach (BGOrderProduct orderProduct in orderProducts) {
				//Old site doesn't expor products with no quantity set
				if (orderProduct.BGItemQuantity > 0) {
					InvoiceItem line = new InvoiceItem() {
						ItemId = orderProduct.Product.BGQuickBooksId,
						LineId = "-1",
						Quantity = orderProduct.BGItemQuantity.ToString(),
						Rate = orderProduct.BGItemPrice.ToString()
					};

					if (order.BGTaxCheckbox && orderProduct.IsSalesTax) {
						line.TaxCodeName = "TAX";
					} else {
						line.TaxCodeName = "NON";
					}

					if (orderProduct.BGUseInner) {
						line.Other2 = orderProduct.BGRequiredBoxesInner.ToString();
					} else if (orderProduct.BGUseMaster) {
						line.Other2 = orderProduct.BGRequiredBoxesMaster.ToString();
					}

					lines.Add(line);
				}
			}

			string subtotalKey = string.Empty;

			decimal productTotal = orderProducts.Sum(e => e.BGItemPrice * e.BGItemQuantity);
			decimal productTotalWithDiscounts = orderProducts.Sum(e => (e.BGItemPrice * e.BGItemQuantity) - (e.BGItemPrice * e.BGItemQuantity * (e.BGItemDiscount / 100)));
			order.BGDiscountPct = productTotal == 0m ? 0m : (productTotal - productTotalWithDiscounts) / productTotal * 100m;

			//throw new Exception(productTotal.ToString() + "|" + productTotalWithDiscounts.ToString());

			//If there is any discount or shpping charge add a subtotal
			if ((order.BGDiscountPct != 0) || (order.BGShippingCharge != 0)) {
				subtotalKey = BGQuickBooksItem.FindOrAddSubtotalItem(config);

				lines.Add(new InvoiceItem() {
					LineId = "-1",
					ItemId = subtotalKey
				});
			}

			if (order.BGDiscountPct > 0) {
				Item discount = BGQuickBooksItem.FindOrAddDiscountItem(config, order.BGDiscountPct, order.BGDiscountReason);

				lines.Add(new InvoiceItem() {
					LineId = "-1",
					ItemId = discount.RefId,
					Description = order.BGDiscountReason,
					TaxCodeName = "TAX"
				});
			}

			if (order.BGShippingCharge > 0) {
				Item shippingCharge = BGQuickBooksItem.FindOrAddOtherChargeItem(config, BGQuickBooks.QBACCT_SHIPCHARGE_NAME, BGQuickBooks.QBACCT_SHIPCHARGE_DESCR, BGQuickBooks.QBACCT_SHIPCHARGE, "0");
				lines.Add(new InvoiceItem() {
					LineId = "-1",
					ItemId = shippingCharge.RefId,
					TaxCodeName = "TAX",
					Rate = order.BGShippingCharge.ToString()
				});
			}

			qbInvoice.LineItems.AddRange(lines);

			if (isNewInvoice) {
				qbInvoice.Add();

				config.QbConnectorMessage = "QBInvoice Add";
				logDetail.ErrorMsg = "The customer order was added successfully";

				order.BGQuickBooksId = qbInvoice.RefId;
				order.UpdateQuickBooksId(userConnection);
			} else { //UPDATE
				qbInvoice.Update();
				config.QbConnectorMessage = "QBInvoice Update";
				logDetail.ErrorMsg = "The customer order was updated successfully";
			}

			//If there are no execptions it means it has either created or updated the invoice
			logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
			logDetail.UpdateLogStatus(userConnection);
			//#########################################################
		}

		#endregion Customer Orders

		#region Factory Orders

		/// <summary>
		///	Process all Factory Orders that need to be processed
		/// </summary>
		/// <param name="userConnection"></param>
		/// <exception cref="Exception"></exception>
		public static void ProcessFactoryOrders(BGQuickBooks config, UserConnection userConnection) {
			List<BGQuickBooksLogDetail> logDetails = GetQuickBooksPendingLogsByType(BGQuickBooksLogType.FactoryOrder, userConnection);

			bool anyError = false;

			//If there are no log Details exit as there are no Customer Orders to process
			if (logDetails is null || logDetails.Count == 0)
				return;

			try {
				//Set logs being processed as processing
				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Processing, userConnection);

				//Get Order Data
				List<string> orderIds = logDetails.Select(x => x.RecordId).Distinct().ToList();
				List<BGOrder> customerOrders = BGOrder.GetByIds(orderIds, userConnection);
				List<BGOrderProduct> ordersProducts = BGOrderProduct.GetAllByOrderIds(orderIds, userConnection);

				foreach (BGQuickBooksLogDetail logDetail in logDetails) {
					try {
						logDetail.Order = customerOrders?.FirstOrDefault(co => co.Id.ToString() == logDetail.RecordId);
						if (logDetail.Order != null) {
							logDetail.Order.BGSalesOrderItems = ordersProducts.Where(p => p.BGOrderId == logDetail.Order.Id).ToList();
							logDetail.Order.BGCustomer = BGAccount.GetById(logDetail.Order.BGCustomer.Id, userConnection);

							ProcessFactoryOrderLogDetail(config, logDetail, userConnection);
						} else {
							logDetail.ErrorMsg = $"Factory Order \"{logDetail.Name}\" was not found.";
							logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
							logDetail.UpdateLogStatus(userConnection);
						}
					}
					catch (Exception ex) {
						logDetail.ErrorMsg = ex.ToString() + $"\n({config.QbConnectorMessage})\nExtraDetails: \n" + logDetail.ErrorMsg;
						logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
						logDetail.UpdateLogStatus(userConnection);
						anyError = true;
					}
				}
			}

			//Issues in Creatio throw exception
			catch (Exception ex) {
				string errorMsg = "\n" + ex.ToString() + "\n" + ex.Message.ToString() + $"\n({config.QbConnectorMessage})\nExtraDetails: \n";

				logDetails.ForEach(l => l.ErrorMsg = errorMsg);

				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Error, userConnection);
				CreateFactoryOrderErrorNotf(userConnection);
				throw ex;
			}

			if (anyError)
				CreateFactoryOrderErrorNotf(userConnection);
		}

		/// <summary>
		/// Adds data to quickbooks for the factory orders from the factory order log detail
		/// </summary>
		/// <param name="config"></param>
		/// <param name="logDetail"></param>
		/// <param name="userConnection"></param>
		public static void ProcessFactoryOrderLogDetail(BGQuickBooks config, BGQuickBooksLogDetail logDetail, UserConnection userConnection) {
			BGOrder order = logDetail.Order;
			List<BGOrderProduct> orderProducts = logDetail.Order.BGSalesOrderItems;

			if (orderProducts.Count <= 0 && !orderProducts.Any(x => x.BGItemQuantity > 0) && logDetail.ActionId.ToLower() != BGQuickBooksLogAction.Delete) {
				logDetail.ErrorMsg = "The order has no products or not a single product has a quantity greater than 0";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			Purchaseorder qbPurchaseOrder = BGQuickBooksPurchaseOrder.GetPurchaseOrderByQuickBooksId(config, order);

			//If it's a delete just simply stop after the delete
			if (logDetail.ActionId.ToLower() == BGQuickBooksLogAction.Delete) {
				if (!string.IsNullOrWhiteSpace(order.BGQuickBooksId)) {
					qbPurchaseOrder.Delete();
					config.QbConnectorMessage = "QBPurchaseOrder Delete";

					order.BGQuickBooksId = string.Empty;
					order.UpdateQuickBooksId(userConnection);
				}

				//If there are no exceptions it means it has either created or updated the invoice
				logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				logDetail.ErrorMsg = "The factory order was deleted successfully";
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			_ = BGQuickBooksItem.GetOrCreate(config, orderProducts, userConnection);

			//Find or Create the Account in QuickBooks
			Vendor qbVendor = BGQuickBooksVendor.GetOrCreate(config, order.BGCustomer, userConnection);

			bool isNewPurchaseOrder = false;
			if (string.IsNullOrWhiteSpace(order.BGQuickBooksId)) {
				qbPurchaseOrder = new Purchaseorder();
				isNewPurchaseOrder = true;
			}

			qbPurchaseOrder.RuntimeLicense = config.RuntimeLicense;
			qbPurchaseOrder.QBConnectionString = config.ConnString;

			qbPurchaseOrder.VendorId = qbVendor.RefId;
			qbPurchaseOrder.RefNumber = order.BGPONumber;

			qbPurchaseOrder.TransactionDate = string.Format("{0:yyyy-MM-dd}", order.BGShipDate != default ? order.BGShipDate : DateTime.UtcNow.Date);

			if (order.BGEta != default)
				qbPurchaseOrder.ExpectedDate = string.Format("{0:yyyy-MM-dd}", order.BGEta);

			if (order.BGTerm != null)
				qbPurchaseOrder.TermsName = order.BGTerm.Name;

			if (order.BGShippingInFO != null)
				qbPurchaseOrder.ShipMethodName = order.BGShippingInFO.Name;

			qbPurchaseOrder.LineItems.Clear();

			foreach (BGOrderProduct orderProduct in orderProducts) {
				//Old site doesn't expor products with no quantity set
				if (orderProduct.BGItemQuantity > 0) {
					PurchaseOrderItem line = new PurchaseOrderItem() {
						LineId = "-1",
						ItemId = orderProduct.Product.BGQuickBooksId,
						Description = orderProduct.Product.BGDescription.Truncate(4000),
						Quantity = orderProduct.BGItemQuantity.ToString(),
						Rate = orderProduct.BGItemPrice.ToString()
					};

					qbPurchaseOrder.LineItems.Add(line);
				}
			}

			if (isNewPurchaseOrder) {
				qbPurchaseOrder.Add();

				config.QbConnectorMessage = "QBPurchaseOrder Add";
				logDetail.ErrorMsg = "The factory order was added successfully";

				order.BGQuickBooksId = qbPurchaseOrder.RefId;
				order.UpdateQuickBooksId(userConnection);
			} else { //UPDATE
				qbPurchaseOrder.Update();
				config.QbConnectorMessage = "QBPurchaseOrder Upadte";
				logDetail.ErrorMsg = "The factory order was updated successfully";
			}

			//If there are no execptions it means it has either created or updated the invoice
			logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
			logDetail.UpdateLogStatus(userConnection);
		}

		#endregion Factory Orders

		#region Inventory Adjustment

		/// <summary>
		/// Process all Inventory Adjustment that need to be processed
		/// </summary>
		/// <param name="config"></param>
		/// <param name="userConnection"></param>
		public static void ProcessInventoryAdjustments(BGQuickBooks config, UserConnection userConnection) {
			List<BGQuickBooksLogDetail> logDetails = GetQuickBooksPendingLogsByType(BGQuickBooksLogType.InventoryAdjustment, userConnection);

			bool anyError = false;

			if (logDetails is null || logDetails.Count == 0)
				return;

			try {
				//Set logs being processed as processing
				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Processing, userConnection);

				//Inventory Adjustment Data
				List<string> iAdjustIds = logDetails.Select(x => x.RecordId).Distinct().ToList();
				List<BGInventoryAdjustment> inventoryAdjustments = BGInventoryAdjustment.GetByIds(iAdjustIds, userConnection);
				List<BGProductsInInventoryAdjustment> inventoryProducts = BGProductsInInventoryAdjustment.GetAllByOrderIds(iAdjustIds, userConnection);

				foreach (BGQuickBooksLogDetail logDetail in logDetails) {
					try {
						logDetail.InventoryAdjustment = inventoryAdjustments?.FirstOrDefault(ia => ia.Id.ToString() == logDetail.RecordId);
						if (logDetail.InventoryAdjustment != null) {
							logDetail.InventoryAdjustment.BGInventoryProducts = inventoryProducts.Where(p => new Guid(p.BGInventoryAdjustmentId) == logDetail.InventoryAdjustment.Id).Distinct().ToList();

							ProcessInventoryAdjustmentLogDetail(config, logDetail, userConnection);
						} else {
							logDetail.ErrorMsg = $"Inventory Adjustment \"{logDetail.Name}\" was not found.";
							logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
							logDetail.UpdateLogStatus(userConnection);
						}
					}
					catch (Exception ex) {
						logDetail.ErrorMsg = ex.ToString() + $"\n({config.QbConnectorMessage})\nExtraDetails: \n" + logDetail.ErrorMsg;
						logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
						logDetail.UpdateLogStatus(userConnection);
						anyError = true;
					}
				}
			}
			//Issues in Creatio throw exception
			catch (Exception ex) {
				string errorMsg = "\n" + ex.ToString() + "\n" + ex.Message.ToString() + $"\n({config.QbConnectorMessage})\nExtraDetails: \n";

				logDetails.ForEach(l => l.ErrorMsg = errorMsg);

				UpdateLogsStatusByIds(logDetails, BGQuickBooksLogStatus.Error, userConnection);
				CreateInventoryAdjustmentErrorNotf(userConnection);
				throw ex;
			}

			if (anyError)
				CreateInventoryAdjustmentErrorNotf(userConnection);
		}

		/// <summary>
		/// Adds data to quickbooks for the inventory adjustment from the inventory adjustment log detail
		/// </summary>
		/// <param name="config"></param>
		/// <param name="logDetail"></param>
		/// <param name="userConnection"></param>
		public static void ProcessInventoryAdjustmentLogDetail(BGQuickBooks config, BGQuickBooksLogDetail logDetail, UserConnection userConnection) {
			BGInventoryAdjustment inventoryAdjustment = logDetail.InventoryAdjustment;
			List<BGProductsInInventoryAdjustment> inventoryProducts = logDetail.InventoryAdjustment.BGInventoryProducts;

			if (inventoryProducts.Count <= 0 && !inventoryProducts.Any(x => x.BGQuantity != 0)) {
				logDetail.ErrorMsg = "The inventory adjustment has no products or not a single product has a quantity different than 0";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			_ = BGQuickBooksItem.GetOrCreate(config, inventoryProducts, userConnection);

			Adjustinventory aInv = new Adjustinventory();
			config.ClearForNewQuery();
			aInv.QBConnectionString = config.ConnString;
			aInv.RuntimeLicense = config.RuntimeLicense;
			aInv.Config("QBConnectionMode=1");

			if (logDetail.ActionId.ToLower() == BGQuickBooksLogAction.Update) {
				aInv.Get(inventoryAdjustment.BGQuickBooksId);
				//Can't update
				aInv.Delete();
				config.QbConnectorMessage = "QBAdjustInvenotry Delete for Update";
			}

			//If it's a delete just simply stop after the delete
			if (logDetail.ActionId.ToLower() == BGQuickBooksLogAction.Delete) {
				if (!string.IsNullOrWhiteSpace(inventoryAdjustment.BGQuickBooksId)) {
					aInv.Delete();
					config.QbConnectorMessage = "QBAdjustInvenotry Delete";

					inventoryAdjustment.BGQuickBooksId = string.Empty;
					inventoryAdjustment.UpdateQuickBooksId(userConnection);
				}

				//If there are no execptions it means it has either created or updated the invoice
				logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				logDetail.ErrorMsg = "The inventory adjustment was deleted successfully";
				logDetail.UpdateLogStatus(userConnection);
				return;
			}

			aInv.AccountName = BGQuickBooks.QBACCT_COGS;
			aInv.Memo = inventoryAdjustment.BGReason;
			aInv.RefNumber = inventoryAdjustment.BGName;

			aInv.Adjustments.Clear();

			foreach (BGProductsInInventoryAdjustment inventoryProduct in inventoryProducts) {
				if (inventoryProduct?.BGProduct != null && inventoryProduct.BGQuantity != 0) {
					Adjustment item = new Adjustment() {
						ItemId = inventoryProduct.BGProduct.BGQuickBooksId,
						QuantityDifference = (-inventoryProduct.BGQuantity).ToString()
					};

					aInv.Adjustments.Add(item);
				}
			}

			//Always add. (Update already deleted the existing inventory adjustment)
			aInv.Add();
			config.QbConnectorMessage = "QBAdjustInvenotry Add Always";
			inventoryAdjustment.BGQuickBooksId = aInv.RefId;
			inventoryAdjustment.UpdateQuickBooksId(userConnection);

			//If there are no execptions it means it has either created or updated the inventory
			logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
			logDetail.ErrorMsg = "The inventory adjustment was added/updated successfully";
			logDetail.UpdateLogStatus(userConnection);
		}

		#endregion Inventory Adjustment

		/// <summary>
		/// Gets quickbooks pending logs from creatio
		/// </summary>
		/// <param name="logTypeId"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		public static List<BGQuickBooksLogDetail> GetQuickBooksPendingLogsByType(string logTypeId, UserConnection userConnection) {
			List<BGQuickBooksLogDetail> logDetails = new List<BGQuickBooksLogDetail>();
			EntitySchemaQuery esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, TableName);

			EntitySchemaQueryColumn colId = esq.AddColumn("Id");
			EntitySchemaQueryColumn colAction = esq.AddColumn("BGAction.Id");
			EntitySchemaQueryColumn colRecordId = esq.AddColumn("BGRecordId");
			EntitySchemaQueryColumn colType = esq.AddColumn("BGType.Id");
			EntitySchemaQueryColumn colStatusId = esq.AddColumn("BGStatus.Id");
			EntitySchemaQueryColumn colName = esq.AddColumn("BGName");

			esq.Filters.Add(esq.CreateFilterWithParameters(FilterComparisonType.Equal, "BGType.Id", logTypeId));
			esq.Filters.Add(esq.CreateFilterWithParameters(FilterComparisonType.Equal, "BGStatus.BGIsFinal", false));

			EntityCollection esqColl = esq.GetEntityCollection(userConnection);
			if (esqColl?.Count > 0) {
				foreach (Entity entity in esqColl) {
					logDetails.Add(new BGQuickBooksLogDetail() {
						Id = entity.GetTypedColumnValue<string>(colId.Name),
						ActionId = entity.GetTypedColumnValue<string>(colAction.Name),
						RecordId = entity.GetTypedColumnValue<string>(colRecordId.Name),
						TypeId = entity.GetTypedColumnValue<string>(colType.Name),
						BGStatusId = entity.GetTypedColumnValue<string>(colStatusId.Name),
						Name = entity.GetTypedColumnValue<string>(colName.Name)
					});
				}
			}

			return logDetails;
		}

		private static string GetLastQuickBooksIntegrationLogId(UserConnection userConnection) {
			EntitySchemaQuery esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGQuickBooksIntegrationLog");

			EntitySchemaQueryColumn colId = esq.AddColumn("Id");
			EntitySchemaQueryColumn colCreatedOn = esq.AddColumn("CreatedOn");
			colCreatedOn.OrderPosition = 0;
			colCreatedOn.OrderDirection = OrderDirection.Descending;

			esq.RowCount = 1;
			Entity entity = esq.GetEntityCollection(userConnection).FirstOrDefault();
			if (entity != null) {
				return entity.GetTypedColumnValue<string>(colId.Name);
			} else {
				return string.Empty;
			}
		}

		public static BGQuickBooksLogDetail CreateLogDetailForCommissions(UserConnection userConnection) {
			BGQuickBooksLogDetail logDetail = null;

			string integrationLogId = GetLastQuickBooksIntegrationLogId(userConnection);
			if (!string.IsNullOrWhiteSpace(integrationLogId)) {
				logDetail = new BGQuickBooksLogDetail() {
					Id = Guid.NewGuid().ToString(),
					ActionId = BGQuickBooksLogAction.Log,
					TypeId = BGQuickBooksLogType.Commission,
					BGStatusId = BGQuickBooksLogStatus.Processing
				};

				EntitySchema entity = userConnection.EntitySchemaManager.GetInstanceByName(TableName);
				Entity assignersEntity = entity.CreateEntity(userConnection);
				assignersEntity.SetDefColumnValues();
				assignersEntity.SetColumnValue("Id", new Guid(logDetail.Id));
				assignersEntity.SetColumnValue("CreatedOn", DateTime.Now);
				assignersEntity.SetColumnValue("ModifiedOn", DateTime.Now);
				assignersEntity.SetColumnValue("BGName", $"Commision Log - {DateTime.Now.ToString()}");
				assignersEntity.SetColumnValue("BGTypeId", logDetail.TypeId);
				assignersEntity.SetColumnValue("BGActionId", logDetail.ActionId);
				assignersEntity.SetColumnValue("BGStatusId", logDetail.BGStatusId);
				assignersEntity.SetColumnValue("BGDate", DateTime.Now);
				assignersEntity.SetColumnValue("BGQuickBooksIntegrationLogId", integrationLogId);
				assignersEntity.Save();
			}

			return logDetail;
		}

		/// <summary>
		/// "Bulk" updates logs status
		/// </summary>
		/// <param name="logs"></param>
		/// <param name="statusId"></param>
		/// <param name="userConnection"></param>
		public static void UpdateLogsStatusByIds(List<BGQuickBooksLogDetail> logs, string statusId, UserConnection userConnection) {
			foreach (BGQuickBooksLogDetail log in logs) {
				log.BGStatusId = statusId;
				log.UpdateLogStatus(userConnection);
			}
		}

		/// <summary>
		/// Updates the log status in Creatio
		/// </summary>
		/// <param name="userConnection"></param>
		public void UpdateLogStatus(UserConnection userConnection) {
			if (!string.IsNullOrWhiteSpace(Id) && new Guid(Id) != default) {
				Update update = (Update)new Update(userConnection, TableName)
					.Set("BGStatusId", Column.Parameter(BGStatusId))
					.Set("BGErrorMessage", Column.Parameter(ErrorMsg))
					.Where("Id").IsEqual(Column.Parameter(new Guid(Id)));

				update.Execute();
			}
		}

		public static void CreateInvoiceErrorNotf(UserConnection userConnection) => CreateErrorNotification("QuickBooks Integration: Error with invoice/s", userConnection);
		public static void CreateFactoryOrderErrorNotf(UserConnection userConnection) => CreateErrorNotification("QuickBooks Integration: Error with Factory Order/s", userConnection);
		public static void CreateInventoryAdjustmentErrorNotf(UserConnection userConnection) => CreateErrorNotification("QuickBooks Integration: Error with Inventory Adjustment/s", userConnection);

		public static void CreateErrorNotification(string errorMsg, UserConnection userConnection) {
			Guid? contactNotf = Terrasoft.Core.Configuration.SysSettings.GetValue<Guid?>(userConnection, "BGQBIntegrationNotificationUser", null);

			if (contactNotf != null) {
				EntitySchema remindingSchema = userConnection.EntitySchemaManager.GetInstanceByName("Reminding");
				Entity remindingEntity = remindingSchema.CreateEntity(userConnection);
				remindingEntity.SetDefColumnValues();
				remindingEntity.SetColumnValue("PopupTitle", errorMsg);
				remindingEntity.SetColumnValue("SubjectCaption", errorMsg);
				remindingEntity.SetColumnValue("Description", errorMsg);
				remindingEntity.SetColumnValue("IsRead", true);
				remindingEntity.SetColumnValue("NotificationTypeId", "685e7149-c015-4a4d-b4a6-2e5625a6314c"); //Notified
				remindingEntity.SetColumnValue("SysEntitySchemaId", "fffc451c-04e7-4754-8053-2f412f990401"); //QuickBooks Integration Log
				remindingEntity.SetColumnValue("RemindTime", DateTime.UtcNow);
				remindingEntity.SetColumnValue("ContactId", contactNotf);
				remindingEntity.Save();
			}
		}
	}

	#region Commissions

	public class BGQuickBooksCommissions {

		/// <summary>
		/// Processes QB Commission related tables in QB Cloud for Commission Calculation
		/// </summary>
		/// <param name="userConnection"></param>
		/// <param name="startDate"></param>
		/// <param name="endDate"></param>
		public void ProcessQuickBooksCommissions(UserConnection userConnection, DateTime startDate = default, DateTime endDate = default) {
			BGQuickBooks config = new BGQuickBooks(userConnection);
			List<BGCommissionReportQBDownload> commRepDownloads = new List<BGCommissionReportQBDownload>();
			BGQuickBooksLogDetail lastLogDetail = BGQuickBooksLogDetail.CreateLogDetailForCommissions(userConnection);

			//Invoice
			commRepDownloads.AddRange(GetQuickBooksReceivedPayments(config, lastLogDetail, startDate, endDate));
			//Credit
			commRepDownloads.AddRange(GetQuickBooksCreditMemos(config, lastLogDetail, startDate, endDate));

			lastLogDetail.ErrorMsg += $"\n Start: {startDate.ToString()} - End: {endDate.ToString()} \n Comm payments to be processed: {commRepDownloads.Count}. Test";

			CreateOrUpdate(commRepDownloads, lastLogDetail, userConnection);
		}

		/// <summary>
		/// Get QB Received Payments for later calculating commissions
		/// </summary>
		/// <param name="config"></param>
		/// <param name="startDate"></param>
		/// <param name="endDate"></param>
		/// <returns></returns>
		public List<BGCommissionReportQBDownload> GetQuickBooksReceivedPayments(BGQuickBooks config, BGQuickBooksLogDetail logDetail, DateTime startDate = default, DateTime endDate = default) {
			List<BGCommissionReportQBDownload> commRepDownloads = new List<BGCommissionReportQBDownload>();

			Objsearch qSearch = new Objsearch();
			config.ClearForNewQuery();
			qSearch.QBConnectionString = config.ConnString;
			qSearch.RuntimeLicense = config.RuntimeLicense;

			qSearch.MaxResults = 2500;

			qSearch.IncludeLineItems = true;

			qSearch.QueryType = ObjsearchQueryTypes.qtReceivePaymentSearch;

			if (startDate != default)
				qSearch.SearchCriteria.TransactionDateStart = startDate.ToString("MM/dd/yyyy");

			if (endDate != default)
				qSearch.SearchCriteria.TransactionDateEnd = endDate.ToString("MM/dd/yyyy");

			try {
				qSearch.Search();
				foreach (ObjSearchResult result in qSearch.Results) {
					Receivepayment qObj = new Receivepayment {
						QBResponseAggregate = result.Aggregate
					};

					foreach (AppliedTo appliedTo in qObj.AppliedTo) {
						BGCommissionReportQBDownload repDownload = new BGCommissionReportQBDownload() {
							BGQuickBooksId = qObj.RefId,
							BGTransactionTypeId = BGTransactionType.Sales,
							BGInvoiceNumber = appliedTo.RefNumber
						};

						string[] custSplit = qObj.CustomerName.Split(':');
						if (custSplit.Length > 1) {
							repDownload.BGDescription = custSplit[0];
							repDownload.BGPONumber = custSplit[0];
						} else {
							repDownload.BGDescription = qObj.CustomerName;
							repDownload.BGPONumber = "";
						}

						if (decimal.TryParse(appliedTo.Amount, out decimal amount))
							repDownload.BGAmount = amount;

						if (DateTime.TryParse(qObj.TransactionDate, out DateTime txnDate))
							repDownload.BGTransactionDate = txnDate;

						commRepDownloads.Add(repDownload);
					}
				}
			}
			catch (InQBException ex) {
				logDetail.ErrorMsg += $"\n Comm. Invoice Search \n{ex}";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
			}

			return commRepDownloads;
		}

		/// <summary>
		/// Get QB Credit Memos for later calculating commissions
		/// </summary>
		/// <param name="config"></param>
		/// <param name="startDate"></param>
		/// <param name="endDate"></param>
		/// <returns></returns>
		public List<BGCommissionReportQBDownload> GetQuickBooksCreditMemos(BGQuickBooks config, BGQuickBooksLogDetail logDetail, DateTime startDate = default, DateTime endDate = default) {
			List<BGCommissionReportQBDownload> commRepDownloads = new List<BGCommissionReportQBDownload>();

			Objsearch qSearch = new Objsearch();

			config.ClearForNewQuery();
			qSearch.QBConnectionString = config.ConnString;
			qSearch.RuntimeLicense = config.RuntimeLicense;

			qSearch.MaxResults = 2500;

			qSearch.IncludeLineItems = false;

			qSearch.QueryType = ObjsearchQueryTypes.qtCreditMemoSearch;

			if (startDate != default)
				qSearch.SearchCriteria.TransactionDateStart = startDate.ToString("MM/dd/yyyy");

			if (endDate != default)
				qSearch.SearchCriteria.TransactionDateEnd = endDate.ToString("MM/dd/yyyy");

			qSearch.SearchCriteria.PaidStatus = TPaidStatus.psPaid;

			try {
				qSearch.Search();
				foreach (ObjSearchResult result in qSearch.Results) {
					Creditmemo qObj = new Creditmemo {
						QBResponseAggregate = result.Aggregate
					};

					XDocument xmlDoc = XDocument.Parse(qObj.QBResponseAggregate);
					XElement credMemo = (xmlDoc.Root.Name == "CreditMemoRet") ? xmlDoc.Root : xmlDoc.Root.Element("CreditMemoRet");
					decimal creditRemaining = Convert.ToDecimal(credMemo.Element("CreditRemaining").Value);

					if (creditRemaining <= 0) {
						BGCommissionReportQBDownload repDownload = new BGCommissionReportQBDownload() {
							BGQuickBooksId = qObj.RefId,
							BGTransactionTypeId = BGTransactionType.CreditMemo,
							BGInvoiceNumber = qObj.RefNumber
						};

						string[] custSplit = qObj.CustomerName.Split(':');
						repDownload.BGDescription = (custSplit.Length > 1) ? custSplit[0] : qObj.CustomerName;

						if (decimal.TryParse(qObj.TotalAmount, out decimal amount))
							repDownload.BGAmount = -amount;

						if (DateTime.TryParse(qObj.TransactionDate, out DateTime txnDate))
							repDownload.BGTransactionDate = txnDate;

						commRepDownloads.Add(repDownload);
					}
				}
			}
			catch (InQBException ex) {
				logDetail.ErrorMsg += $"\n Comm. Credit Memo Search \n{ex}";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
			}

			return commRepDownloads;
		}

		/// <summary>
		/// Saves the commissions records to the system or updates it where it applies
		/// </summary>
		/// <param name="qbCommissions"></param>
		/// <param name="userConnection"></param>
		public void CreateOrUpdate(List<BGCommissionReportQBDownload> qbCommissions, BGQuickBooksLogDetail logDetail, UserConnection userConnection) {
			int updated = 0;
			int created = 0;
			int failed = 0;
			try {
				List<BGCommissionReportQBDownload> commCreatio = BGCommissionReportQBDownload.GetByQuickBooksId(qbCommissions.Select(c => c.BGQuickBooksId).ToList(), userConnection);

				foreach (BGCommissionReportQBDownload qbCommission in qbCommissions) {
					BGCommissionReportQBDownload commInCreatio = commCreatio.FirstOrDefault(c => c.BGQuickBooksId == qbCommission.BGQuickBooksId && c.BGInvoiceNumber == qbCommission.BGInvoiceNumber);

					try {
						if (commInCreatio != default) {
							qbCommission.Id = commInCreatio.Id;
							qbCommission.Update(userConnection);
							updated++;
						} else {
							qbCommission.Create(userConnection);
							created++;
						}
					}
					catch (Exception ex) {
						logDetail.ErrorMsg = $"\nError while {((commInCreatio != default) ? "Updating" : "Creating")} Comm Id: {qbCommission.BGQuickBooksId}, InvNumber: {qbCommission.BGInvoiceNumber}. {ex}";
						failed++;
					}
				}
			}
			catch (InQBException ex) {
				logDetail.ErrorMsg += $"\n Comm. CreateOrUpdate \n{ex}";
				logDetail.BGStatusId = BGQuickBooksLogStatus.Error;
			}
			finally {
				if (logDetail.BGStatusId == BGQuickBooksLogStatus.Processing) {
					logDetail.BGStatusId = BGQuickBooksLogStatus.Processed;
				}

				logDetail.ErrorMsg += $"\n Updated: {updated} | Created: {created} | Failed: {failed}";
				logDetail.UpdateLogStatus(userConnection);
			}
		}

		/// <summary>
		/// Calculates the total invoice by the given values
		/// </summary>
		/// <param name="salesOrder"></param>
		/// <param name="qbInvoices"></param>
		/// <param name="salesOrderItems"></param>
		/// <returns></returns>
		[Obsolete("No longer used as now it's a view")]
		public decimal GetTotalInvoice(BGOrder salesOrder, List<BGCommissionReportQBDownload> qbInvoices, List<BGOrderProduct> salesOrderItems) {
			decimal totalInvoice = 0m;

			decimal totalAmount = qbInvoices.Sum(c => c.BGAmount);
			if (salesOrder.BGShippingCharge == 0m) {
				totalInvoice = totalAmount;
			} else {
				decimal shippingTotalAmount = 0m;
				shippingTotalAmount = salesOrderItems.Sum(i => (i.BGItemQuantity * i.BGTotalAmount) - Math.Round(i.BGItemDiscount / 100m * i.BGItemQuantity * i.BGTotalAmount, 2));
				shippingTotalAmount -= salesOrder.BGShippingCharge;

				if (totalAmount == shippingTotalAmount) {
					totalInvoice = totalAmount - salesOrder.BGShippingCharge;
				} else {
					totalInvoice = totalAmount;
					totalInvoice -= Math.Round(((shippingTotalAmount != 0m) ? totalAmount / shippingTotalAmount : 0m) * salesOrder.BGShippingCharge, 2);
				}
			}

			return totalInvoice;
		}
	}

	public class BGCommissionReportQBDownload {
		public const string TableName = "BGCommissionReportQBDownload";
		public string Id { get; set; }
		public string BGOrderId { get; set; }
		public decimal BGAmount { get; set; }
		public decimal BGCommission { get; set; }
		public decimal BGCommissionRatePercentage { get; set; }
		public string BGCustomerId { get; set; }
		public string BGDescription { get; set; }
		public string BGInvoiceNumber { get; set; }
		public string BGPONumber { get; set; }
		public string BGSalesRepId { get; set; }
		public DateTime BGTransactionDate { get; set; }
		public string BGTransactionTypeId { get; set; }
		public string BGQuickBooksId { get; set; }

		/// <summary>
		/// Returns the invoice number stripped from any non numeric caracter
		/// </summary>
		/// <returns>Clean Invoice Number</returns>
		public int GetCleanInvoiceNumber() {
			string cleanInvoiceNumberString = System.Text.RegularExpressions.Regex.Replace(BGInvoiceNumber, "[^0-9]", "");
			int.TryParse(cleanInvoiceNumberString, out int cleanInvoiceNumber);
			return cleanInvoiceNumber;
		}

		/// <summary>
		/// Create new <see cref="BGCommissionReportQBDownload"/> record in creatio
		/// </summary>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		public string Create(UserConnection userConnection) {
			Id = Guid.NewGuid().ToString();

			Insert insert = new Insert(userConnection)
				.Into(TableName)
				.Set("Id", Column.Parameter(Id))
				.Set("BGAmount", Column.Parameter(BGAmount))
				.Set("BGCommission", Column.Parameter(BGCommission))
				.Set("BGCommissionRatePercentage", Column.Parameter(BGCommissionRatePercentage));

			if (BGTransactionDate != DateTime.MinValue)
				insert.Set("BGTransactionDate", Column.Parameter(BGTransactionDate));

			if (!string.IsNullOrWhiteSpace(BGTransactionTypeId))
				insert.Set("BGTransactionTypeId", Column.Parameter(BGTransactionTypeId));

			if (!string.IsNullOrWhiteSpace(BGTransactionTypeId))
				insert.Set("BGQuickBooksId", Column.Parameter(BGQuickBooksId));

			if (!string.IsNullOrWhiteSpace(BGCustomerId))
				insert.Set("BGCustomerId", Column.Parameter(BGCustomerId));

			if (!string.IsNullOrWhiteSpace(BGDescription))
				insert.Set("BGDescription", Column.Parameter(BGDescription));

			if (!string.IsNullOrWhiteSpace(BGInvoiceNumber)) {
				insert.Set("BGInvoiceNumber", Column.Parameter(BGInvoiceNumber));
				insert.Set("BGCleanInvoiceNumber", Column.Parameter(GetCleanInvoiceNumber()));
			}

			if (!string.IsNullOrWhiteSpace(BGPONumber))
				insert.Set("BGPoNumber", Column.Parameter(BGPONumber));

			if (!string.IsNullOrWhiteSpace(BGSalesRepId))
				insert.Set("BGSalesRepId", Column.Parameter(BGSalesRepId));

			if (!string.IsNullOrWhiteSpace(BGOrderId))
				insert.Set("BGOrderId", Column.Parameter(BGOrderId));

			insert.Execute();

			return Id;
		}

		/// <summary>
		/// Update <see cref="BGCommissionReportQBDownload"/> in creatio
		/// </summary>
		/// <param name="userConnection"></param>
		public void Update(UserConnection userConnection) {
			Update update = (Update)new Update(userConnection, TableName)
				.Set("ModifiedOn", Column.Parameter(DateTime.Now))
				.Where("Id").IsEqual(Column.Parameter(Guid.Parse(Id)));

			if (BGTransactionDate != DateTime.MinValue)
				update.Set("BGTransactionDate", Column.Parameter(BGTransactionDate));

			if (!string.IsNullOrWhiteSpace(BGDescription))
				update.Set("BGDescription", Column.Parameter(BGDescription));

			if (!string.IsNullOrWhiteSpace(BGInvoiceNumber)) {
				update.Set("BGInvoiceNumber", Column.Parameter(BGInvoiceNumber));
				update.Set("BGCleanInvoiceNumber", Column.Parameter(GetCleanInvoiceNumber()));
			}

			if (!string.IsNullOrWhiteSpace(BGPONumber))
				update.Set("BGPoNumber", Column.Parameter(BGPONumber));

			update.Execute();
		}

		/// <summary>
		/// Gets <see cref="BGCommissionReportQBDownload"/> by the <paramref name="quickBooksIds"/>
		/// </summary>
		/// <param name="quickBooksIds"></param>
		/// <param name="userConnection"></param>
		/// <returns></returns>
		public static List<BGCommissionReportQBDownload> GetByQuickBooksId(List<string> quickBooksIds, UserConnection userConnection) {
			List<BGCommissionReportQBDownload> commissions = new List<BGCommissionReportQBDownload>();

            if (quickBooksIds?.Count > 0) {
        			EntitySchemaQuery esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGCommissionReportQBDownload");
        
        			EntitySchemaQueryColumn colId = esq.AddColumn("Id");
        			EntitySchemaQueryColumn colQuickBookId = esq.AddColumn("BGQuickBooksId");
        			EntitySchemaQueryColumn colInvoiceNumber = esq.AddColumn("BGInvoiceNumber");
        
        			esq.Filters.Add(esq.CreateFilterWithParameters(FilterComparisonType.Equal, "BGQuickBooksId", quickBooksIds));
        
        			EntityCollection esqColl = esq.GetEntityCollection(userConnection);
        			if (esqColl?.Count > 0) {
        				foreach (Entity entity in esqColl) {
        					commissions.Add(new BGCommissionReportQBDownload() {
        						Id = entity.GetTypedColumnValue<string>(colId.Name),
        						BGQuickBooksId = entity.GetTypedColumnValue<string>(colQuickBookId.Name),
        						BGInvoiceNumber = entity.GetTypedColumnValue<string>(colInvoiceNumber.Name)
        					});
        				}
        			}
            }

			return commissions;
		}
	}

	#endregion Commissions
}
