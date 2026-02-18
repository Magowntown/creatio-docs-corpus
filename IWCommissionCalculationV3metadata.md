{
"MetaData": {
"Schema": {
"ManagerName": "ProcessSchemaManager",
"UId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"Name": "IWCalculateCommissiononPaymentV3",
"CreatedInPackageId": "174185bc-2e8a-4649-aabc-71cea0369901",
"Methods": [],
"LocalizableStrings": [],
"Usings": [],
"PackageUId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"CreatedInVersion": "8.3.1.4481",
"Parameters": [
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "eab9b2d5-4600-4a94-840d-4243c218cd28",
"Name": "CalculatedSalesAmount",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"DataValueType": "969093e2-2b4e-463b-883a-3d3b8c61f0cd",
"SourceValue": {
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "39cc5200-2e45-44b4-ab96-59da60240dc8",
"Name": "CommissionAmount",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"DataValueType": "969093e2-2b4e-463b-883a-3d3b8c61f0cd",
"SourceValue": {
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "4d104428-0e17-4367-ad1c-c37c9a75bd9f",
"Name": "CommissionRate",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"DataValueType": "5cc8060d-6d10-4773-89fc-8c12d6f659a6",
"SourceValue": {
"Source": 3,
"Value": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{756c633c-0a6b-4a3a-b952-88d263cee609}].[EntityColumn:{9467a416-14c7-45ad-b86e-f1da6e817a7c}]#]",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "9f1fd7b4-95d5-4352-b5a1-3dd740dcaf56",
"Name": "IWCommissionStatus",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"DataValueType": "b295071f-7ea9-4e62-8d1a-919bf3732ff2",
"SourceValue": {
"Source": 3,
"Value": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{e6ee8013-d6ab-c660-c6a7-f08bca97e67f}]#]",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
},
"ReferenceSchemaUId": "94c61392-ccde-4274-88c6-7ffe7660250f"
}
],
"SerializeToDB": true,
"ParentSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"IsDelivered": true,
"Version": 1,
"UseSystemSecurityContext": true,
"Mappings": [
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "a241c275-fb00-4449-9c5c-e0a57851c9a7",
"Name": "StartSignal2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{46884467-984f-4940-89e3-8bf3cbce698f}].[Parameter:{639abaee-a176-49ac-8849-4e165ad5f8f6}]",
"TargetUId": "639abaee-a176-49ac-8849-4e165ad5f8f6",
"SourceParameterUId": "639abaee-a176-49ac-8849-4e165ad5f8f6",
"Source": {
"Source": 1,
"Value": ""
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "37d6d265-7e1f-4ace-a4c2-67f362fb8da5",
"Name": "StartSignal3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{cee0cee7-0694-4883-851d-8c0903a2f150}].[Parameter:{88ab1862-68cf-4b2b-a19e-433efaef44c2}]",
"TargetUId": "88ab1862-68cf-4b2b-a19e-433efaef44c2",
"SourceParameterUId": "88ab1862-68cf-4b2b-a19e-433efaef44c2",
"Source": {
"Source": 1,
"Value": ""
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "a1bae658-a8b1-499f-8165-b7553a8408c1",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{a0bc94c4-9e93-4414-9c0b-7de6bf70f807}]",
"TargetUId": "a0bc94c4-9e93-4414-9c0b-7de6bf70f807",
"SourceParameterUId": "5d9ac9a7-7782-49ce-8990-dcb1c73832b0",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{522b0a0f-2cb7-4fbb-9a9b-172c42e68634}].[Parameter:{b56f8976-e30d-44d0-a1e0-978f9986b632}]\\\",\\\"displayValue\\\":\\\"Payment Modified.Unique identifier of record\\\"}}}},\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{46884467-984f-4940-89e3-8bf3cbce698f}].[Parameter:{639abaee-a176-49ac-8849-4e165ad5f8f6}]\\\",\\\"displayValue\\\":\\\"Payment Added.Unique identifier of record\\\"}}}},\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{cee0cee7-0694-4883-851d-8c0903a2f150}].[Parameter:{88ab1862-68cf-4b2b-a19e-433efaef44c2}]\\\",\\\"displayValue\\\":\\\"Payment Deleted.Unique identifier of record\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{522b0a0f-2cb7-4fbb-9a9b-172c42e68634}].[Parameter:{b56f8976-e30d-44d0-a1e0-978f9986b632}]\\\"}}}},\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{46884467-984f-4940-89e3-8bf3cbce698f}].[Parameter:{639abaee-a176-49ac-8849-4e165ad5f8f6}]\\\"}}}},\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{cee0cee7-0694-4883-851d-8c0903a2f150}].[Parameter:{88ab1862-68cf-4b2b-a19e-433efaef44c2}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "8a2f53ae-f6bd-4ca2-ae3e-ad99f08f1e75",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{efd1e757-e793-449c-8c5a-3e5e7a3f4bcc}]",
"TargetUId": "efd1e757-e793-449c-8c5a-3e5e7a3f4bcc",
"SourceParameterUId": "643e4d6d-7ec8-49f0-842a-066a996fbe8b",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e9dcbd2b-6775-445d-b007-042a0e153a2f",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{83df4515-0e38-40bf-8a99-48534142242e}]",
"TargetUId": "83df4515-0e38-40bf-8a99-48534142242e",
"SourceParameterUId": "29115add-7520-4ad4-8371-d91f537ac913",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "0e3e1866-c4e7-4b57-9ff5-8503b8553e84",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{51558430-400a-415e-9eb6-103059125e8e}]",
"TargetUId": "51558430-400a-415e-9eb6-103059125e8e",
"SourceParameterUId": "f29e5660-c5ef-4d84-8331-9046c3093519",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "50"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d3de1874-26e4-43df-b19f-cab7232f562d",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{eb215463-45c3-4e25-9168-1068ca90bc13}]",
"TargetUId": "eb215463-45c3-4e25-9168-1068ca90bc13",
"SourceParameterUId": "94ba9876-18c1-4a68-bcef-08f7e7f0e25c",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "4fb09375-76c5-4577-8302-3313c61a7c3d",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{a52917e1-5e9d-4a4d-a2fc-efe7ba65a7fc}]",
"TargetUId": "a52917e1-5e9d-4a4d-a2fc-efe7ba65a7fc",
"SourceParameterUId": "cb5d6d26-7e81-4cbe-8730-8b7169000d14",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "26daf072-d9b1-414c-9664-bbdea441967c",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{28f6b9f1-8cfb-4cc6-8432-dc0d0c24c506}]",
"TargetUId": "28f6b9f1-8cfb-4cc6-8432-dc0d0c24c506",
"SourceParameterUId": "473e79e2-727e-40a7-8829-7eefc576b403",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "IWPaymentNumber:1:1",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "0f636332-9036-4a4c-bf11-1d048b67d115",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}]",
"TargetUId": "26dc550d-338f-467a-b7e3-3a969ad0ca23",
"SourceParameterUId": "e2fced10-4842-423e-ada0-523bf7ea8ad3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f83cca32-3ce6-470e-982c-bb3a5a6cf7e7",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{29c40ecd-0a3f-42ef-8b13-fb3fb430bb4f}]",
"TargetUId": "29c40ecd-0a3f-42ef-8b13-fb3fb430bb4f",
"SourceParameterUId": "2e63ea99-8125-4254-88bd-20d3610bd471",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e7d3b70c-434b-4a8d-9002-17d0762d11fe",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{151d96fb-3051-4a0a-b3a5-39e251392a9b}]",
"TargetUId": "151d96fb-3051-4a0a-b3a5-39e251392a9b",
"SourceParameterUId": "a3660fce-a8f9-4a68-a3c1-b4f2f7983635",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f19abf31-6bd4-4a33-ada4-f3519a7ad631",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{57b02acb-c780-4457-854c-167c24288c88}]",
"TargetUId": "57b02acb-c780-4457-854c-167c24288c88",
"SourceParameterUId": "9a594933-75da-4304-b6a3-5945dba159e3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e200d646-d447-4eaf-9a07-3045f1586cf5",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{6c33a2e4-1a20-4704-a6fd-198707d47541}]",
"TargetUId": "6c33a2e4-1a20-4704-a6fd-198707d47541",
"SourceParameterUId": "11fb235f-c06a-4111-84cd-a5dbf9a440d5",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "5eb2661d-d532-4c92-872e-0722575ab914",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{8d49421d-4c6c-4087-8c62-e1c96255ded2}]",
"TargetUId": "8d49421d-4c6c-4087-8c62-e1c96255ded2",
"SourceParameterUId": "78252e95-b759-416a-9c48-c128fbdf59ef",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f460e2f7-4303-477b-aad6-98a8175019f2",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{ae4c52f1-2ded-4167-90a5-d35f0587e7e5}]",
"TargetUId": "ae4c52f1-2ded-4167-90a5-d35f0587e7e5",
"SourceParameterUId": "2f797429-6f43-4594-96bb-62fbc7b7deec",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d5cb9a4c-6690-4545-8e42-0295f17c0fce",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{99fd1752-5b02-4d86-b321-53c46303d8b1}]",
"TargetUId": "99fd1752-5b02-4d86-b321-53c46303d8b1",
"SourceParameterUId": "be4a0d16-6a15-41cf-ac44-a8b757565428",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "26b1a660-6054-40f3-9dbb-8c2e9ac7b4ab",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{465fb92b-68b7-4b30-896d-48d8f82c0ef1}]",
"TargetUId": "465fb92b-68b7-4b30-896d-48d8f82c0ef1",
"SourceParameterUId": "cc12005f-f434-4a40-b9d0-dc8f81755545",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d5a655ef-efe6-45cc-b604-b83d9a6bff16",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{46400365-8cb5-42f1-989f-c7be33575d0a}]",
"TargetUId": "46400365-8cb5-42f1-989f-c7be33575d0a",
"SourceParameterUId": "6dada847-859b-4e0a-9297-b3c9572530b6",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "4f474bf4-c4ba-488c-a25e-10b1a5961cff",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{3f3b8998-3d97-4d6a-bddc-52f7a1fe3f87}]",
"TargetUId": "3f3b8998-3d97-4d6a-bddc-52f7a1fe3f87",
"SourceParameterUId": "555901ef-f707-4803-a887-1bc07e882096",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "ea4e18c2-0a45-440a-8b12-839d08ed1bae",
"Name": "ReadDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{9a964d10-142c-44fa-a0c4-b34ba19eb3d8}]",
"TargetUId": "9a964d10-142c-44fa-a0c4-b34ba19eb3d8",
"SourceParameterUId": "978b550e-1b81-448a-8700-9c9190c3a2a4",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "3a0dbe4a-1fa8-4e0e-beed-e07f5ce29de7",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{0d832abd-c624-4696-9b7e-40481370d84d}]",
"TargetUId": "0d832abd-c624-4696-9b7e-40481370d84d",
"SourceParameterUId": "5d9ac9a7-7782-49ce-8990-dcb1c73832b0",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{a8868023-f16d-d7d9-b77c-b69bae9b9118}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Order\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"Order\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{a8868023-f16d-d7d9-b77c-b69bae9b9118}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"Order\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "91c9c81a-25fe-4631-b151-069d9a71d123",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{4f764069-1d8d-4460-924d-63921866399e}]",
"TargetUId": "4f764069-1d8d-4460-924d-63921866399e",
"SourceParameterUId": "643e4d6d-7ec8-49f0-842a-066a996fbe8b",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f8960a73-72c0-4e19-a81a-1cebddf790b4",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{aa2162cf-832c-45e5-a295-97845a7c0ef7}]",
"TargetUId": "aa2162cf-832c-45e5-a295-97845a7c0ef7",
"SourceParameterUId": "29115add-7520-4ad4-8371-d91f537ac913",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e1ceaefa-4130-4944-bb5e-f3466ffe1d0c",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{204d755f-3b2e-44c1-bef4-1c5593b5415a}]",
"TargetUId": "204d755f-3b2e-44c1-bef4-1c5593b5415a",
"SourceParameterUId": "f29e5660-c5ef-4d84-8331-9046c3093519",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "50"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "98f085d4-7c3f-4d8b-b6e1-bd83cf01d08d",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{52aa8598-e1e0-4866-b034-d7b1492d13a5}]",
"TargetUId": "52aa8598-e1e0-4866-b034-d7b1492d13a5",
"SourceParameterUId": "94ba9876-18c1-4a68-bcef-08f7e7f0e25c",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "9f3a29c2-304c-4395-8f68-c4d0baa05c55",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{01b5c53c-bd0e-4c80-8c5f-bde62213c55e}]",
"TargetUId": "01b5c53c-bd0e-4c80-8c5f-bde62213c55e",
"SourceParameterUId": "cb5d6d26-7e81-4cbe-8730-8b7169000d14",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "1dab17e1-563b-48d7-af6f-4ee9a39855d9",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{9b3e3f65-513e-4b23-ac0d-d82ff1be2a3b}]",
"TargetUId": "9b3e3f65-513e-4b23-ac0d-d82ff1be2a3b",
"SourceParameterUId": "473e79e2-727e-40a7-8829-7eefc576b403",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "BGDisplayTitle:1:1"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "06ec57b5-9e54-426c-a18a-87795b1bbca3",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}]",
"TargetUId": "c4c34584-9b8a-40ea-ad64-98389ea1942c",
"SourceParameterUId": "e2fced10-4842-423e-ada0-523bf7ea8ad3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "2036e7ca-8d7b-46ba-b62e-90fa55ccb29a",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{048ed306-df62-45ee-91a0-4fbcc86b5254}]",
"TargetUId": "048ed306-df62-45ee-91a0-4fbcc86b5254",
"SourceParameterUId": "2e63ea99-8125-4254-88bd-20d3610bd471",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "3cdce8cf-794c-4f56-8359-abe1f0dae9cb",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{99cb532d-087f-48ea-9a7a-ea9ce5f0f738}]",
"TargetUId": "99cb532d-087f-48ea-9a7a-ea9ce5f0f738",
"SourceParameterUId": "a3660fce-a8f9-4a68-a3c1-b4f2f7983635",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "4c2524a3-8fe6-48c8-83a0-f770eaf682e7",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{8633bc18-e524-44d6-a303-ebe061a98f3a}]",
"TargetUId": "8633bc18-e524-44d6-a303-ebe061a98f3a",
"SourceParameterUId": "9a594933-75da-4304-b6a3-5945dba159e3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "6f12d3c7-4c3c-4191-9035-90e81c6ddc81",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{ae9002da-6df7-4b2f-8885-a3bd6057ef6b}]",
"TargetUId": "ae9002da-6df7-4b2f-8885-a3bd6057ef6b",
"SourceParameterUId": "11fb235f-c06a-4111-84cd-a5dbf9a440d5",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "23b015e7-4d0d-4a3a-ad6f-ef873fc5b06e",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{29497c5f-42a8-43be-98c2-530955acc62f}]",
"TargetUId": "29497c5f-42a8-43be-98c2-530955acc62f",
"SourceParameterUId": "78252e95-b759-416a-9c48-c128fbdf59ef",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "0862141f-db54-4e2d-9dc5-4e4549d1fbb6",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{a491be6c-c2b5-47f3-82fd-8bf2e666a7ae}]",
"TargetUId": "a491be6c-c2b5-47f3-82fd-8bf2e666a7ae",
"SourceParameterUId": "2f797429-6f43-4594-96bb-62fbc7b7deec",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "3ed86b47-f5c3-4696-8be4-4885d599e6f3",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{4f86e333-2fef-487b-bf47-b4d362e515f7}]",
"TargetUId": "4f86e333-2fef-487b-bf47-b4d362e515f7",
"SourceParameterUId": "be4a0d16-6a15-41cf-ac44-a8b757565428",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "2ac6fd1f-7354-48c7-9ef3-01ada4ba2c8d",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{de6a8dbb-7312-4e7b-a8a4-aebfad14ea3e}]",
"TargetUId": "de6a8dbb-7312-4e7b-a8a4-aebfad14ea3e",
"SourceParameterUId": "cc12005f-f434-4a40-b9d0-dc8f81755545",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "4442fc79-8a9d-41a2-9291-b4d5cc29416a",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{4fb41222-2c18-4172-9b16-99a0c73a45c0}]",
"TargetUId": "4fb41222-2c18-4172-9b16-99a0c73a45c0",
"SourceParameterUId": "6dada847-859b-4e0a-9297-b3c9572530b6",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "b75e8878-982b-41c4-b23b-f28479c2cc37",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{8c8298b3-98eb-4c63-b8fc-17b0c28b9ea2}]",
"TargetUId": "8c8298b3-98eb-4c63-b8fc-17b0c28b9ea2",
"SourceParameterUId": "555901ef-f707-4803-a887-1bc07e882096",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "eba909d8-80e8-401a-8a74-a9d9ae2dc11a",
"Name": "ReadDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{ccae91b4-1064-44f3-9a80-a3c9b57bb94e}]",
"TargetUId": "ccae91b4-1064-44f3-9a80-a3c9b57bb94e",
"SourceParameterUId": "978b550e-1b81-448a-8700-9c9190c3a2a4",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f2681d96-33b3-4ce6-81b1-a1be98906e4a",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{2f0c7f03-93de-44cd-a754-91603f9e469b}]",
"TargetUId": "2f0c7f03-93de-44cd-a754-91603f9e469b",
"SourceParameterUId": "5d9ac9a7-7782-49ce-8990-dcb1c73832b0",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\":{\\\"className\\\":\\\"Terrasoft.InFilter\\\",\\\"filterType\\\":4,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"BGOrder\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\",\\\"dataValueType\\\":10,\\\"leftExpressionCaption\\\":\\\"Order\\\",\\\"referenceSchemaName\\\":\\\"Order\\\",\\\"rightExpressions\\\":[{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Order Record.First item of resulting collection.Id\\\",\\\"Id\\\":\\\"df4e3e48-733e-40cc-be24-2635dd36107f\\\"}}}]}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"BGCommissionEarner\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\":{\\\"filterType\\\":4,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"BGOrder\\\"},\\\"rightExpressions\\\":[{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"Id\\\":\\\"df4e3e48-733e-40cc-be24-2635dd36107f\\\"}}}]}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"BGCommissionEarner\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f0802bd1-1f05-4940-9f3c-4f1f57240245",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{d0dfadb3-7375-422b-8815-5fa556e5714f}]",
"TargetUId": "d0dfadb3-7375-422b-8815-5fa556e5714f",
"SourceParameterUId": "643e4d6d-7ec8-49f0-842a-066a996fbe8b",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d48b111e-f83e-4984-9c51-b9c5e25d0f2e",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{7e3321a8-7e47-4198-8320-5d41f7751d6c}]",
"TargetUId": "7e3321a8-7e47-4198-8320-5d41f7751d6c",
"SourceParameterUId": "29115add-7520-4ad4-8371-d91f537ac913",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "118d1228-4400-4c24-ada4-d026d59597ae",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{241225af-0811-46e2-90f3-c6c93507cf23}]",
"TargetUId": "241225af-0811-46e2-90f3-c6c93507cf23",
"SourceParameterUId": "f29e5660-c5ef-4d84-8331-9046c3093519",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "50"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "b731d20c-97bf-4aab-b5eb-e114505d2def",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{01da7399-354f-405f-83cb-7f1db270562f}]",
"TargetUId": "01da7399-354f-405f-83cb-7f1db270562f",
"SourceParameterUId": "94ba9876-18c1-4a68-bcef-08f7e7f0e25c",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "0"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "0f207c6c-6b7c-4f79-b0f6-1f7526351b36",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{32b738ba-0854-4538-a1c9-c3f3ac074566}]",
"TargetUId": "32b738ba-0854-4538-a1c9-c3f3ac074566",
"SourceParameterUId": "cb5d6d26-7e81-4cbe-8730-8b7169000d14",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "a438bc0d-c828-41e5-8939-fc865e66c7e9",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{906d2c26-7851-42cf-85cb-35dab6fcde63}]",
"TargetUId": "906d2c26-7851-42cf-85cb-35dab6fcde63",
"SourceParameterUId": "473e79e2-727e-40a7-8829-7eefc576b403",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "BGName:1:1"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d546089f-ce85-4ca2-ad53-32a3a8732c46",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{756c633c-0a6b-4a3a-b952-88d263cee609}]",
"TargetUId": "756c633c-0a6b-4a3a-b952-88d263cee609",
"SourceParameterUId": "e2fced10-4842-423e-ada0-523bf7ea8ad3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "f9bff916-3f98-4568-ad8b-681a1a919eed",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{2bea4bac-a552-427c-836f-9ad66771699f}]",
"TargetUId": "2bea4bac-a552-427c-836f-9ad66771699f",
"SourceParameterUId": "2e63ea99-8125-4254-88bd-20d3610bd471",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "de76e78f-f7ec-405c-a3c6-b8b9a1493cbe",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{aa91e728-58e2-4a2a-8cb0-1a83245f016d}]",
"TargetUId": "aa91e728-58e2-4a2a-8cb0-1a83245f016d",
"SourceParameterUId": "a3660fce-a8f9-4a68-a3c1-b4f2f7983635",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e7bea7a9-a0f9-4d8b-ae61-f1e4c282aaba",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{bf2b144d-471f-4755-a0a6-b4e6eb09e416}]",
"TargetUId": "bf2b144d-471f-4755-a0a6-b4e6eb09e416",
"SourceParameterUId": "9a594933-75da-4304-b6a3-5945dba159e3",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "91736e44-338d-47bc-b9b6-84e63787e9a5",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{cddad1f0-ba98-4200-a942-2f8a1a5e5fa0}]",
"TargetUId": "cddad1f0-ba98-4200-a942-2f8a1a5e5fa0",
"SourceParameterUId": "11fb235f-c06a-4111-84cd-a5dbf9a440d5",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "ee281b97-e1e9-4bbb-b77b-1c633987cf92",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{3a3b4533-b37a-472d-bbb8-9a9f39173a05}]",
"TargetUId": "3a3b4533-b37a-472d-bbb8-9a9f39173a05",
"SourceParameterUId": "78252e95-b759-416a-9c48-c128fbdf59ef",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "c62f2a5c-197f-4df9-b45f-e2f00aceac2e",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{355ed94c-dec6-4fc1-9b6e-fdf56ee09e8b}]",
"TargetUId": "355ed94c-dec6-4fc1-9b6e-fdf56ee09e8b",
"SourceParameterUId": "2f797429-6f43-4594-96bb-62fbc7b7deec",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 1,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "1261ca3b-c69d-410e-bd7d-ef64e09cf97b",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{0201ed7f-9589-4058-94e5-48dcf5557631}]",
"TargetUId": "0201ed7f-9589-4058-94e5-48dcf5557631",
"SourceParameterUId": "be4a0d16-6a15-41cf-ac44-a8b757565428",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "fd0db552-9ab3-44ec-a577-2c9d78bd727b",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{9671c148-1b5d-4c35-bfb9-beae8c8db3c7}]",
"TargetUId": "9671c148-1b5d-4c35-bfb9-beae8c8db3c7",
"SourceParameterUId": "cc12005f-f434-4a40-b9d0-dc8f81755545",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "15d5f099-9fc3-4da6-9580-d4d48d8abb02",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{be37fdd8-33d3-4acd-8bcd-8e5fdc69b589}]",
"TargetUId": "be37fdd8-33d3-4acd-8bcd-8e5fdc69b589",
"SourceParameterUId": "6dada847-859b-4e0a-9297-b3c9572530b6",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "704a24d3-78d0-4cf9-aebb-3ddb2409b278",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{23fd3ebd-c2dc-4164-aaa4-d14bac3e16cc}]",
"TargetUId": "23fd3ebd-c2dc-4164-aaa4-d14bac3e16cc",
"SourceParameterUId": "555901ef-f707-4803-a887-1bc07e882096",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "369a7024-8283-4aff-b1e2-84cba005f6d3",
"Name": "ReadDataUserTask4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{ab0e601c-64b4-44c4-9671-43cae6cdc366}]",
"TargetUId": "ab0e601c-64b4-44c4-9671-43cae6cdc366",
"SourceParameterUId": "978b550e-1b81-448a-8700-9c9190c3a2a4",
"SourceSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "15bf872d-5e6c-4ad7-b074-d8a45ba9fe2d",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{6f62ea0c-ff4f-4784-b7f5-69d300b128bc}]",
"TargetUId": "6f62ea0c-ff4f-4784-b7f5-69d300b128bc",
"SourceParameterUId": "bd2cf1ae-bbc6-4d91-8d6e-c6b40f057e95",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e357b8b0-88c0-4524-80e9-b7f60caf7f88",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{84257f74-f5fb-46a6-8dbf-32f70cffe99e}]",
"TargetUId": "84257f74-f5fb-46a6-8dbf-32f70cffe99e",
"SourceParameterUId": "d6c84ba1-b6ca-4952-b517-880f22e21fdc",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "a39ba781-71b2-45ea-9776-6c4a0f3f3aa6",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{510e7cd3-2aa9-444c-8dbb-5a99621c2dfe}]",
"TargetUId": "510e7cd3-2aa9-444c-8dbb-5a99621c2dfe",
"SourceParameterUId": "03166c4b-2e15-4768-a343-750c16b69691",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "48c7ae25-6d5d-4d4e-94bd-752d2f7e360c",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{b33e0fd8-dc01-4d2c-987a-6c62337a1635}]",
"TargetUId": "b33e0fd8-dc01-4d2c-987a-6c62337a1635",
"SourceParameterUId": "effa11ce-90c7-4efe-8a02-be7a659d27e9",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"ee24d9db-785a-4222-8c7d-18401b8890eb\",\"columnMetaPath\":{\"value\":\"5ecc730b-5012-af19-04cb-98a7a433162e\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{39cc5200-2e45-44b4-ab96-59da60240dc8}]#]\"},\"displayValue\":{\"value\":\"[#Commission Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"b88b5def-ec97-44b5-88cc-48a407eb614f\",\"columnMetaPath\":{\"value\":\"c59d6063-8484-f2dd-7e52-34077171ac39\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"c6596222-57b4-443b-aae2-20f1f7c9754c\",\"columnMetaPath\":{\"value\":\"72360747-50bc-7a2e-24cd-c0f2bc94a294\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]\"},\"displayValue\":{\"value\":\"[#Calculated Sales Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"36141d5b-670a-436d-8f9c-95929d886383\",\"columnMetaPath\":{\"value\":\"e6ee8013-d6ab-c660-c6a7-f08bca97e67f\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#Lookup.94c61392-ccde-4274-88c6-7ffe7660250f.deb80242-b56a-4b94-967a-0e170e2198d8#]\"},\"displayValue\":{\"value\":\"[#Lookup.IW Commission Status.Done.deb80242-b56a-4b94-967a-0e170e2198d8#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"94c61392-ccde-4274-88c6-7ffe7660250f\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"27086172-0b27-474b-a7c2-7978c9f398fb\",\"columnMetaPath\":{\"value\":\"05c78c64-e9bb-166f-1021-88d4266003f9\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{81c8e318-76ac-4895-9a9b-9760b27c55ea}]#]\"},\"displayValue\":{\"value\":\"[#Read Order Record.First item of resulting collection.Owner#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"16be3651-8fe2-4159-8dd0-a803d4683dd3\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"3bd1c9d7-8dc4-4216-a07a-841f64724e63\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.False#]\"},\"displayValue\":{\"value\":\"[#Boolean value.False#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "68e69e3e-8d82-4db0-ad6a-a3a2d4482109",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{bd3363c0-dfd0-48d6-ad9a-b7c2eab55bac}]",
"TargetUId": "bd3363c0-dfd0-48d6-ad9a-b7c2eab55bac",
"SourceParameterUId": "b9bc395c-1f13-d564-1257-2505f236ab7b",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "e24ff945-e65d-452f-8825-584b18d6a506",
"Name": "ChangeDataUserTask1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{b7dc7a54-1524-4335-ab0d-60facfda268a}].[Parameter:{0fabbcf4-f6b3-4ae4-81ed-3e014bafef4b}]",
"TargetUId": "0fabbcf4-f6b3-4ae4-81ed-3e014bafef4b",
"SourceParameterUId": "0def8b99-56d1-2d16-0ae9-3625cc87f048",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 3,
"Value": "false",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "true"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "6d11c8bb-2299-44de-8b21-ede8dd5b4d2a",
"Name": "ChangeDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{e611ab1d-285b-49ce-866b-a652ceff6a8e}]",
"TargetUId": "e611ab1d-285b-49ce-866b-a652ceff6a8e",
"SourceParameterUId": "bd2cf1ae-bbc6-4d91-8d6e-c6b40f057e95",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "76009126-6d52-49fd-afb3-7ae69fceabec",
"Name": "ChangeDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{725130a9-fa65-43c7-905e-647b428e1e1c}]",
"TargetUId": "725130a9-fa65-43c7-905e-647b428e1e1c",
"SourceParameterUId": "d6c84ba1-b6ca-4952-b517-880f22e21fdc",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "a1c42bfb-8e65-46e7-9fb5-e4cdb887fb07",
"Name": "ChangeDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{b698554a-3c7b-4f00-af26-983e8bb51233}]",
"TargetUId": "b698554a-3c7b-4f00-af26-983e8bb51233",
"SourceParameterUId": "03166c4b-2e15-4768-a343-750c16b69691",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
"UId": "d3b65fa6-42c1-45fe-a7f5-85eccd280150",
"Name": "ChangeDataUserTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{cf1aa858-ae16-4537-bde4-2c78cf0117b8}]",
"TargetUId": "cf1aa858-ae16-4537-bde4-2c78cf0117b8",
"SourceParameterUId": "effa11ce-90c7-4efe-8a02-be7a659d27e9",
"SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"Source": {
"Source": 1,
"Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"80082c15-b028-40fe-8547-ce0244bd0ce4\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
            "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "f7f1ba5a-8092-4279-96b3-426698b3652d",
          "Name": "ChangeDataUserTask2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{6c372129-07da-4ddb-93e4-65e99d66cfd4}]",
          "TargetUId": "6c372129-07da-4ddb-93e4-65e99d66cfd4",
          "SourceParameterUId": "b9bc395c-1f13-d564-1257-2505f236ab7b",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 3,
            "Value": "true",
            "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
            "DefValueForExistingProcess": "false"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "214d62e9-59d7-4da5-aeec-41cc1414ab53",
          "Name": "ChangeDataUserTask2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{52baca83-7627-42d1-a3de-cf6dc10ba2d4}].[Parameter:{2728a6ca-66c8-41ad-bba6-79a73bca04a0}]",
          "TargetUId": "2728a6ca-66c8-41ad-bba6-79a73bca04a0",
          "SourceParameterUId": "0def8b99-56d1-2d16-0ae9-3625cc87f048",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 3,
            "Value": "false",
            "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
            "DefValueForExistingProcess": "true"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "1435da87-8467-436c-b908-1da24a66eebc",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{c0d4b0c6-3cd0-4880-a21d-cf646cd9d953}]",
          "TargetUId": "c0d4b0c6-3cd0-4880-a21d-cf646cd9d953",
          "SourceParameterUId": "bd2cf1ae-bbc6-4d91-8d6e-c6b40f057e95",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 1,
            "Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "e395939a-ce80-4c80-a175-2acd043c96d1",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{04b821a5-71d6-44d9-b27d-f8562e54bb8a}]",
          "TargetUId": "04b821a5-71d6-44d9-b27d-f8562e54bb8a",
          "SourceParameterUId": "d6c84ba1-b6ca-4952-b517-880f22e21fdc",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 3,
            "Value": "true",
            "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "d9dbdf40-3ee8-49b2-97b1-02447bad0d43",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{e8992e0f-f8e9-4490-8eaf-ed670269e347}]",
          "TargetUId": "e8992e0f-f8e9-4490-8eaf-ed670269e347",
          "SourceParameterUId": "03166c4b-2e15-4768-a343-750c16b69691",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 1,
            "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
            "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "c63065e0-b6f2-4e8a-bda1-8c7fba4d6e92",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{79c8293c-2b8e-44be-926d-45c2a272c37f}]",
          "TargetUId": "79c8293c-2b8e-44be-926d-45c2a272c37f",
          "SourceParameterUId": "effa11ce-90c7-4efe-8a02-be7a659d27e9",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 1,
            "Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"c6b48774-5693-4e8a-82d5-b003cce67a06\",\"columnMetaPath\":{\"value\":\"5ecc730b-5012-af19-04cb-98a7a433162e\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{39cc5200-2e45-44b4-ab96-59da60240dc8}]#]\"},\"displayValue\":{\"value\":\"[#Commission Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"78bb8611-b1da-4492-8832-e3e093c978af\",\"columnMetaPath\":{\"value\":\"c59d6063-8484-f2dd-7e52-34077171ac39\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"e6a57ded-b853-49a3-8d3f-e6cef69e3a30\",\"columnMetaPath\":{\"value\":\"72360747-50bc-7a2e-24cd-c0f2bc94a294\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]\"},\"displayValue\":{\"value\":\"[#Calculated Sales Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"523dbdaa-12f1-4286-a460-9d4435938692\",\"columnMetaPath\":{\"value\":\"e6ee8013-d6ab-c660-c6a7-f08bca97e67f\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#Lookup.94c61392-ccde-4274-88c6-7ffe7660250f.ee14b2ce-163a-4fb2-abea-e739636794ed#]\"},\"displayValue\":{\"value\":\"[#Lookup.IW Commission Status.Returned.ee14b2ce-163a-4fb2-abea-e739636794ed#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"94c61392-ccde-4274-88c6-7ffe7660250f\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"f9d86356-9683-4e1d-b725-35a1f0e26e0d\",\"columnMetaPath\":{\"value\":\"05c78c64-e9bb-166f-1021-88d4266003f9\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{81c8e318-76ac-4895-9a9b-9760b27c55ea}]#]\"},\"displayValue\":{\"value\":\"[#Read Order Record.First item of resulting collection.Owner#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"16be3651-8fe2-4159-8dd0-a803d4683dd3\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"7d127aeb-a201-45ef-a329-0aff0844245a\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
            "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "18a1ca5b-e12f-4dc4-8ba2-ba1d8f35612a",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{edcdfcd7-49a3-417a-83c0-e5f763d63047}]",
          "TargetUId": "edcdfcd7-49a3-417a-83c0-e5f763d63047",
          "SourceParameterUId": "b9bc395c-1f13-d564-1257-2505f236ab7b",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 3,
            "Value": "true",
            "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
            "DefValueForExistingProcess": "false"
          }
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaMapping",
          "UId": "c3746898-a6b5-42e2-ba0e-4520ca1b35e9",
          "Name": "ChangeDataUserTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "TargetMetaPath": "[Element:{d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c}].[Parameter:{50e14fd1-45d8-43c4-a9b5-acf014bcd475}]",
          "TargetUId": "50e14fd1-45d8-43c4-a9b5-acf014bcd475",
          "SourceParameterUId": "0def8b99-56d1-2d16-0ae9-3625cc87f048",
          "SourceSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "Source": {
            "Source": 3,
            "Value": "false",
            "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
            "DefValueForExistingProcess": "true"
          }
        }
      ],
      "NotificationCaption": {
        "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
        "UId": "cdd58be7-2dba-4a5e-869b-1ad5d6d7513a",
        "Name": "NotificationCaption",
        "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
        "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
        "DataValueType": "8b3f29bb-ea14-4ce5-a5c5-293a929b6ba2",
        "SourceValue": {
          "Source": 3,
          "Value": "[#[PropertyValue:Caption]#]"
        }
      },
      "TaskFillDefColor": "FFFFFFFF",
      "SequenceFlowStrokeDefColor": "FFBBBBBB",
      "LaneSets": [
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaLaneSet",
          "UId": "f1099bfe-c421-4677-8734-9e8f90ecead7",
          "Name": "LaneSet1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ManagerItemUId": "11a47caf-a0d5-41fa-a274-a0b11f77447a",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Direction": 0,
          "Lanes": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaLane",
              "UId": "108e3940-7b07-4c50-ac46-ea325af82370",
              "Name": "Lane1",
              "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
              "ContainerUId": "f1099bfe-c421-4677-8734-9e8f90ecead7",
              "ManagerItemUId": "abcd74b9-5912-414b-82ac-f1aa4dcd554e",
              "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
              "FlowElementRefs": [],
              "Artifacts": [],
              "LaneSetUId": "f1099bfe-c421-4677-8734-9e8f90ecead7",
              "UserContexts": []
            }
          ]
        }
      ],
      "Artifacts": [],
      "FlowElements": [
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaTerminateEvent",
          "UId": "67461fd9-b2a0-4ebc-a0be-895902c641b8",
          "Name": "TerminateEvent1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "2238;184",
          "ManagerItemUId": "1bd93619-0574-454e-bb4e-cf53b9eb9470",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "31;31",
          "IsLogging": true,
          "Parameters": []
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaStartSignalEvent",
          "UId": "522b0a0f-2cb7-4fbb-9a9b-172c42e68634",
          "Name": "StartSignal1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "UseBackgroundMode": true,
          "Position": "50;184",
          "ManagerItemUId": "1129e72f-0e8c-445a-b2ea-463517e86395",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "31;31",
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "b56f8976-e30d-44d0-a1e0-978f9986b632",
              "Name": "RecordId",
              "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ContainerUId": "522b0a0f-2cb7-4fbb-9a9b-172c42e68634",
              "DataValueType": "23018567-a13c-4320-8687-fd6f9e3699bd",
              "SourceValue": {
                "Source": 1,
                "Value": ""
              }
            }
          ],
          "EntitySchemaUId": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
          "IsInterrupting": false,
          "Signal": "null",
          "WaitingRandomSignal": false,
          "WaitingEntitySignal": true,
          "EntitySignal": 2,
          "NewEntityChangedColumns": "[]",
          "EntityFilters": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaStartSignalEvent",
          "UId": "46884467-984f-4940-89e3-8bf3cbce698f",
          "Name": "StartSignal2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "UseBackgroundMode": true,
          "Position": "50;92",
          "ManagerItemUId": "1129e72f-0e8c-445a-b2ea-463517e86395",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "31;31",
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "639abaee-a176-49ac-8849-4e165ad5f8f6",
              "Name": "RecordId",
              "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ContainerUId": "46884467-984f-4940-89e3-8bf3cbce698f",
              "DataValueType": "23018567-a13c-4320-8687-fd6f9e3699bd",
              "SourceValue": {
                "Source": 1,
                "Value": ""
              }
            }
          ],
          "EntitySchemaUId": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
          "IsInterrupting": false,
          "Signal": "null",
          "WaitingRandomSignal": false,
          "WaitingEntitySignal": true,
          "EntitySignal": 1,
          "NewEntityChangedColumns": "[]",
          "EntityFilters": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaStartSignalEvent",
          "UId": "cee0cee7-0694-4883-851d-8c0903a2f150",
          "Name": "StartSignal3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "50;273",
          "ManagerItemUId": "1129e72f-0e8c-445a-b2ea-463517e86395",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "31;31",
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "88ab1862-68cf-4b2b-a19e-433efaef44c2",
              "Name": "RecordId",
              "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
              "ContainerUId": "cee0cee7-0694-4883-851d-8c0903a2f150",
              "DataValueType": "23018567-a13c-4320-8687-fd6f9e3699bd",
              "SourceValue": {
                "Source": 1,
                "Value": ""
              }
            }
          ],
          "EntitySchemaUId": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
          "IsInterrupting": false,
          "Signal": "null",
          "WaitingRandomSignal": false,
          "WaitingEntitySignal": true,
          "EntitySignal": 4,
          "NewEntityChangedColumns": "[]",
          "EntityFilters": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
          "UId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
          "Name": "ReadDataUserTask1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "233;172",
          "ManagerItemUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "SerializeToDB": true,
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "a0bc94c4-9e93-4414-9c0b-7de6bf70f807",
              "Name": "DataSourceFilters",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{522b0a0f-2cb7-4fbb-9a9b-172c42e68634}].[Parameter:{b56f8976-e30d-44d0-a1e0-978f9986b632}]\\\",\\\"displayValue\\\":\\\"Payment Modified.Unique identifier of record\\\"}}}},\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{46884467-984f-4940-89e3-8bf3cbce698f}].[Parameter:{639abaee-a176-49ac-8849-4e165ad5f8f6}]\\\",\\\"displayValue\\\":\\\"Payment Added.Unique identifier of record\\\"}}}},\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{cee0cee7-0694-4883-851d-8c0903a2f150}].[Parameter:{88ab1862-68cf-4b2b-a19e-433efaef44c2}]\\\",\\\"displayValue\\\":\\\"Payment Deleted.Unique identifier of record\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"4a5214df-aedd-41f8-b0e2-bd61989f7fe7\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{522b0a0f-2cb7-4fbb-9a9b-172c42e68634}].[Parameter:{b56f8976-e30d-44d0-a1e0-978f9986b632}]\\\"}}}},\\\"fa644dce-1a4f-45c0-8508-d937c46bf4c2\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{46884467-984f-4940-89e3-8bf3cbce698f}].[Parameter:{639abaee-a176-49ac-8849-4e165ad5f8f6}]\\\"}}}},\\\"008a0e88-442c-4d92-9d95-bdb0f943550b\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{cee0cee7-0694-4883-851d-8c0903a2f150}].[Parameter:{88ab1862-68cf-4b2b-a19e-433efaef44c2}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "efd1e757-e793-449c-8c5a-3e5e7a3f4bcc",
              "Name": "ResultType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "83df4515-0e38-40bf-8a99-48534142242e",
              "Name": "ReadSomeTopRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "51558430-400a-415e-9eb6-103059125e8e",
              "Name": "NumberOfRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "50",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "eb215463-45c3-4e25-9168-1068ca90bc13",
              "Name": "FunctionType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "a52917e1-5e9d-4a4d-a2fc-efe7ba65a7fc",
              "Name": "AggregationColumnName",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "28f6b9f1-8cfb-4cc6-8432-dc0d0c24c506",
              "Name": "OrderInfo",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "IWPaymentNumber:1:1",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "26dc550d-338f-467a-b7e3-3a969ad0ca23",
              "Name": "ResultEntity",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "ebd85d37-0abf-4bbf-bb32-97dc3dffcc8c",
              "SourceValue": {
                "Source": 1,
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              },
              "ReferenceSchemaUId": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
              "IsResult": true
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "29c40ecd-0a3f-42ef-8b13-fb3fb430bb4f",
              "Name": "ResultCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "151d96fb-3051-4a0a-b3a5-39e251392a9b",
              "Name": "ResultIntegerFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "57b02acb-c780-4457-854c-167c24288c88",
              "Name": "ResultFloatFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "ff22e049-4d16-46ee-a529-92d8808932dc",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "6c33a2e4-1a20-4704-a6fd-198707d47541",
              "Name": "ResultDateTimeFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "d21e9ef4-c064-4012-b286-fa1a8171da44",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "8d49421d-4c6c-4087-8c62-e1c96255ded2",
              "Name": "ResultRowsCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "ae4c52f1-2ded-4167-90a5-d35f0587e7e5",
              "Name": "CanReadUncommitedData",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "99fd1752-5b02-4d86-b321-53c46303d8b1",
              "Name": "ResultEntityCollection",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "51fb23ba-3eb2-11e2-b7d5-b0c76188709b",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "465fb92b-68b7-4b30-896d-48d8f82c0ef1",
              "Name": "EntityColumnMetaPathes",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "46400365-8cb5-42f1-989f-c7be33575d0a",
              "Name": "IgnoreDisplayValues",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "3f3b8998-3d97-4d6a-bddc-52f7a1fe3f87",
              "Name": "ResultCompositeObjectList",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "651ec16f-d140-46db-b9e2-825c985a8ac2",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "9a964d10-142c-44fa-a0c4-b34ba19eb3d8",
              "Name": "ConsiderTimeInFilter",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
                "DefValueForExistingProcess": "false"
              }
            }
          ],
          "FillColor": "FFFFFFFF",
          "SchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
          "UId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
          "Name": "ReadDataUserTask2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "325;80",
          "ManagerItemUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "SerializeToDB": true,
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "0d832abd-c624-4696-9b7e-40481370d84d",
              "Name": "DataSourceFilters",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{a8868023-f16d-d7d9-b77c-b69bae9b9118}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Order\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"Order\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"68ac0e06-8b3b-43cd-b115-8c85e732bcaa\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{a8868023-f16d-d7d9-b77c-b69bae9b9118}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"Order\\\"}\"}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "4f764069-1d8d-4460-924d-63921866399e",
              "Name": "ResultType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "aa2162cf-832c-45e5-a295-97845a7c0ef7",
              "Name": "ReadSomeTopRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "204d755f-3b2e-44c1-bef4-1c5593b5415a",
              "Name": "NumberOfRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "50",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "52aa8598-e1e0-4866-b034-d7b1492d13a5",
              "Name": "FunctionType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "01b5c53c-bd0e-4c80-8c5f-bde62213c55e",
              "Name": "AggregationColumnName",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "9b3e3f65-513e-4b23-ac0d-d82ff1be2a3b",
              "Name": "OrderInfo",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "BGDisplayTitle:1:1",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "c4c34584-9b8a-40ea-ad64-98389ea1942c",
              "Name": "ResultEntity",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "ebd85d37-0abf-4bbf-bb32-97dc3dffcc8c",
              "SourceValue": {
                "Source": 1,
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              },
              "ReferenceSchemaUId": "80294582-06b5-4faa-a85f-3323e5536b71",
              "IsResult": true
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "048ed306-df62-45ee-91a0-4fbcc86b5254",
              "Name": "ResultCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "99cb532d-087f-48ea-9a7a-ea9ce5f0f738",
              "Name": "ResultIntegerFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "8633bc18-e524-44d6-a303-ebe061a98f3a",
              "Name": "ResultFloatFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "ff22e049-4d16-46ee-a529-92d8808932dc",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "ae9002da-6df7-4b2f-8885-a3bd6057ef6b",
              "Name": "ResultDateTimeFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "d21e9ef4-c064-4012-b286-fa1a8171da44",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "29497c5f-42a8-43be-98c2-530955acc62f",
              "Name": "ResultRowsCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "a491be6c-c2b5-47f3-82fd-8bf2e666a7ae",
              "Name": "CanReadUncommitedData",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "4f86e333-2fef-487b-bf47-b4d362e515f7",
              "Name": "ResultEntityCollection",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "51fb23ba-3eb2-11e2-b7d5-b0c76188709b",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "de6a8dbb-7312-4e7b-a8a4-aebfad14ea3e",
              "Name": "EntityColumnMetaPathes",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "4fb41222-2c18-4172-9b16-99a0c73a45c0",
              "Name": "IgnoreDisplayValues",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "8c8298b3-98eb-4c63-b8fc-17b0c28b9ea2",
              "Name": "ResultCompositeObjectList",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "651ec16f-d140-46db-b9e2-825c985a8ac2",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "ccae91b4-1064-44f3-9a80-a3c9b57bb94e",
              "Name": "ConsiderTimeInFilter",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
                "DefValueForExistingProcess": "false"
              }
            }
          ],
          "FillColor": "FFFFFFFF",
          "SchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaFormulaTask",
          "UId": "e739b215-25de-48a2-a5eb-9eb669921258",
          "Name": "FormulaTask1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "576;264",
          "ManagerItemUId": "d334d28f-b11a-477e-9ff0-0a95fa73d53b",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "IsLogging": true,
          "Parameters": [],
          "FillColor": "FFFFFFFF",
          "Body": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{6cb1e6eb-3723-6b5f-fc15-eeb00bfcb2db}]#]-([#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{9fc6f34e-4965-4e6f-bede-539e6b162f0b}]#]*[#[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{6cb1e6eb-3723-6b5f-fc15-eeb00bfcb2db}]#]/[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{f397997e-a5b6-474d-a12f-9a1449c29e96}]#])",
          "ResultParameterMetaPath": "eab9b2d5-4600-4a94-840d-4243c218cd28"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaFormulaTask",
          "UId": "48173478-a29d-4aac-926b-f43be5f628ec",
          "Name": "FormulaTask3",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "1450;264",
          "ManagerItemUId": "d334d28f-b11a-477e-9ff0-0a95fa73d53b",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "IsLogging": true,
          "Parameters": [],
          "FillColor": "FFFFFFFF",
          "Body": "[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]*([#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{4d104428-0e17-4367-ad1c-c37c9a75bd9f}]#]/100)",
          "ResultParameterMetaPath": "39cc5200-2e45-44b4-ab96-59da60240dc8"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
          "UId": "f95fa7ef-c895-4d06-816d-7436b030df07",
          "Name": "ReadDataUserTask4",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "325;261",
          "ManagerItemUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "SerializeToDB": true,
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "2f0c7f03-93de-44cd-a754-91603f9e469b",
              "Name": "DataSourceFilters",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\":{\\\"className\\\":\\\"Terrasoft.InFilter\\\",\\\"filterType\\\":4,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"BGOrder\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\",\\\"dataValueType\\\":10,\\\"leftExpressionCaption\\\":\\\"Order\\\",\\\"referenceSchemaName\\\":\\\"Order\\\",\\\"rightExpressions\\\":[{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Order Record.First item of resulting collection.Id\\\",\\\"Id\\\":\\\"df4e3e48-733e-40cc-be24-2635dd36107f\\\"}}}]}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"BGCommissionEarner\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"49e98694-d2c3-4cc7-98cd-9f209cbc1b00\\\":{\\\"filterType\\\":4,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"BGOrder\\\"},\\\"rightExpressions\\\":[{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"Id\\\":\\\"df4e3e48-733e-40cc-be24-2635dd36107f\\\"}}}]}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"BGCommissionEarner\\\"}\"}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "d0dfadb3-7375-422b-8815-5fa556e5714f",
              "Name": "ResultType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "7e3321a8-7e47-4198-8320-5d41f7751d6c",
              "Name": "ReadSomeTopRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "241225af-0811-46e2-90f3-c6c93507cf23",
              "Name": "NumberOfRecords",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "50",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "01da7399-354f-405f-83cb-7f1db270562f",
              "Name": "FunctionType",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {
                "Source": 1,
                "Value": "0",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "32b738ba-0854-4538-a1c9-c3f3ac074566",
              "Name": "AggregationColumnName",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "906d2c26-7851-42cf-85cb-35dab6fcde63",
              "Name": "OrderInfo",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "BGName:1:1",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "756c633c-0a6b-4a3a-b952-88d263cee609",
              "Name": "ResultEntity",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "ebd85d37-0abf-4bbf-bb32-97dc3dffcc8c",
              "SourceValue": {
                "Source": 1,
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              },
              "ReferenceSchemaUId": "6e61fb4d-6afa-48e2-9227-3164f9f301a1",
              "IsResult": true
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "2bea4bac-a552-427c-836f-9ad66771699f",
              "Name": "ResultCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "aa91e728-58e2-4a2a-8cb0-1a83245f016d",
              "Name": "ResultIntegerFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "bf2b144d-471f-4755-a0a6-b4e6eb09e416",
              "Name": "ResultFloatFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "ff22e049-4d16-46ee-a529-92d8808932dc",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "cddad1f0-ba98-4200-a942-2f8a1a5e5fa0",
              "Name": "ResultDateTimeFunction",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "d21e9ef4-c064-4012-b286-fa1a8171da44",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "3a3b4533-b37a-472d-bbb8-9a9f39173a05",
              "Name": "ResultRowsCount",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "6b6b74e2-820d-490e-a017-2b73d4ccf2b0",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "355ed94c-dec6-4fc1-9b6e-fdf56ee09e8b",
              "Name": "CanReadUncommitedData",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 1,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "0201ed7f-9589-4058-94e5-48dcf5557631",
              "Name": "ResultEntityCollection",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "51fb23ba-3eb2-11e2-b7d5-b0c76188709b",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "9671c148-1b5d-4c35-bfb9-beae8c8db3c7",
              "Name": "EntityColumnMetaPathes",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "be37fdd8-33d3-4acd-8bcd-8e5fdc69b589",
              "Name": "IgnoreDisplayValues",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "23fd3ebd-c2dc-4164-aaa4-d14bac3e16cc",
              "Name": "ResultCompositeObjectList",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "651ec16f-d140-46db-b9e2-825c985a8ac2",
              "SourceValue": {}
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "ab0e601c-64b4-44c4-9671-43cae6cdc366",
              "Name": "ConsiderTimeInFilter",
              "CreatedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
              "ContainerUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f",
                "DefValueForExistingProcess": "false"
              }
            }
          ],
          "FillColor": "FFFFFFFF",
          "SchemaUId": "cb455b6f-78ff-4b1e-b241-c2bbc0b37e9f"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaExclusiveGateway",
          "UId": "a0e575c7-f091-4a97-be40-25756464a7bc",
          "Name": "ExclusiveGateway1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "1236;172",
          "ManagerItemUId": "bd9f7570-6c97-4f16-90e5-663a190c6c7c",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "55;55",
          "IsLogging": true,
          "BranchingDecisions": []
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
          "UId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
          "Name": "ChangeDataUserTask1",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "1940;253",
          "ManagerItemUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "6f62ea0c-ff4f-4784-b7f5-69d300b128bc",
              "Name": "EntitySchemaUId",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "b295071f-7ea9-4e62-8d1a-919bf3732ff2",
              "SourceValue": {
                "Source": 1,
                "Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              },
              "ReferenceSchemaUId": "6c7394db-06ff-4050-91ef-8278e21dce15"
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "84257f74-f5fb-46a6-8dbf-32f70cffe99e",
              "Name": "IsMatchConditions",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "510e7cd3-2aa9-444c-8dbb-5a99621c2dfe",
              "Name": "DataSourceFilters",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"e3143cda-1317-4b3a-9b7a-e8bf66d1647f\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "b33e0fd8-dc01-4d2c-987a-6c62337a1635",
              "Name": "RecordColumnValues",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "b53eaa2a-4bb7-4a6b-9f4f-58ccab293e31",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"ee24d9db-785a-4222-8c7d-18401b8890eb\",\"columnMetaPath\":{\"value\":\"5ecc730b-5012-af19-04cb-98a7a433162e\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{39cc5200-2e45-44b4-ab96-59da60240dc8}]#]\"},\"displayValue\":{\"value\":\"[#Commission Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"b88b5def-ec97-44b5-88cc-48a407eb614f\",\"columnMetaPath\":{\"value\":\"c59d6063-8484-f2dd-7e52-34077171ac39\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"c6596222-57b4-443b-aae2-20f1f7c9754c\",\"columnMetaPath\":{\"value\":\"72360747-50bc-7a2e-24cd-c0f2bc94a294\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]\"},\"displayValue\":{\"value\":\"[#Calculated Sales Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"36141d5b-670a-436d-8f9c-95929d886383\",\"columnMetaPath\":{\"value\":\"e6ee8013-d6ab-c660-c6a7-f08bca97e67f\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#Lookup.94c61392-ccde-4274-88c6-7ffe7660250f.deb80242-b56a-4b94-967a-0e170e2198d8#]\"},\"displayValue\":{\"value\":\"[#Lookup.IW Commission Status.Done.deb80242-b56a-4b94-967a-0e170e2198d8#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"94c61392-ccde-4274-88c6-7ffe7660250f\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"27086172-0b27-474b-a7c2-7978c9f398fb\",\"columnMetaPath\":{\"value\":\"05c78c64-e9bb-166f-1021-88d4266003f9\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{81c8e318-76ac-4895-9a9b-9760b27c55ea}]#]\"},\"displayValue\":{\"value\":\"[#Read Order Record.First item of resulting collection.Owner#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"16be3651-8fe2-4159-8dd0-a803d4683dd3\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"3bd1c9d7-8dc4-4216-a07a-841f64724e63\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.False#]\"},\"displayValue\":{\"value\":\"[#Boolean value.False#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "bd3363c0-dfd0-48d6-ad9a-b7c2eab55bac",
              "Name": "ConsiderTimeInFilter",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
                "DefValueForExistingProcess": "false"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "0fabbcf4-f6b3-4ae4-81ed-3e014bafef4b",
              "Name": "IgnoreErrors",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ContainerUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "false",
                "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
                "DefValueForExistingProcess": "true"
              }
            }
          ],
          "FillColor": "FFFFFFFF",
          "SchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaExclusiveGateway",
          "UId": "b089222e-6f31-401a-93a3-7e0b6f8fd6a3",
          "Name": "ExclusiveGateway2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "821;172",
          "ManagerItemUId": "bd9f7570-6c97-4f16-90e5-663a190c6c7c",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "55;55",
          "IsLogging": true,
          "BranchingDecisions": []
        },
        {
          "TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
          "UId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
          "Name": "ChangeDataUserTask2",
          "CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
          "CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
          "ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
          "Position": "1024;80",
          "ManagerItemUId": "d3021ca7-7450-4678-a117-060171eb2976",
          "CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
          "Size": "69;55",
          "IsLogging": true,
          "Parameters": [
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "e611ab1d-285b-49ce-866b-a652ceff6a8e",
              "Name": "EntitySchemaUId",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
              "DataValueType": "b295071f-7ea9-4e62-8d1a-919bf3732ff2",
              "SourceValue": {
                "Source": 1,
                "Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              },
              "ReferenceSchemaUId": "6c7394db-06ff-4050-91ef-8278e21dce15"
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "725130a9-fa65-43c7-905e-647b428e1e1c",
              "Name": "IsMatchConditions",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
              "DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
              "SourceValue": {
                "Source": 3,
                "Value": "true",
                "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "b698554a-3c7b-4f00-af26-983e8bb51233",
              "Name": "DataSourceFilters",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
              "DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"66aeaeac-5e88-4dcb-970f-fdd7cd72f1ac\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":0,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
                "ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
              }
            },
            {
              "TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
              "UId": "cf1aa858-ae16-4537-bde4-2c78cf0117b8",
              "Name": "RecordColumnValues",
              "CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
              "CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
              "ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
              "DataValueType": "b53eaa2a-4bb7-4a6b-9f4f-58ccab293e31",
              "SourceValue": {
                "Source": 1,
                "Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"80082c15-b028-40fe-8547-ce0244bd0ce4\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "6c372129-07da-4ddb-93e4-65e99d66cfd4",
"Name": "ConsiderTimeInFilter",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
"DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
"SourceValue": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "2728a6ca-66c8-41ad-bba6-79a73bca04a0",
"Name": "IgnoreErrors",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ContainerUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
"DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
"SourceValue": {
"Source": 3,
"Value": "false",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "true"
}
}
],
"FillColor": "FFFFFFFF",
"SchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaExclusiveGateway",
"UId": "0017199f-49f2-4bf2-b68a-ae4cf7560203",
"Name": "ExclusiveGateway3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
"Position": "447;172",
"ManagerItemUId": "bd9f7570-6c97-4f16-90e5-663a190c6c7c",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"Size": "55;55",
"IsLogging": true,
"BranchingDecisions": []
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaFormulaTask",
"UId": "b5908e55-8033-4f9f-aea4-87fff5fef224",
"Name": "FormulaTask2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
"Position": "576;80",
"ManagerItemUId": "d334d28f-b11a-477e-9ff0-0a95fa73d53b",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"Size": "69;55",
"IsLogging": true,
"Parameters": [],
"FillColor": "FFFFFFFF",
"Body": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{6cb1e6eb-3723-6b5f-fc15-eeb00bfcb2db}]#]",
"ResultParameterMetaPath": "eab9b2d5-4600-4a94-840d-4243c218cd28"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaUserTask",
"UId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"Name": "ChangeDataUserTask3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
"Position": "1940;80",
"ManagerItemUId": "d3021ca7-7450-4678-a117-060171eb2976",
"CreatedInOwnerSchemaUId": "8cdd4845-4b27-45cd-9907-e9cc478bc3c5",
"Size": "69;55",
"IsLogging": true,
"Parameters": [
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "c0d4b0c6-3cd0-4880-a21d-cf646cd9d953",
"Name": "EntitySchemaUId",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "b295071f-7ea9-4e62-8d1a-919bf3732ff2",
"SourceValue": {
"Source": 1,
"Value": "e1169637-8d6e-48d6-a129-0362fbdb7f65",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
},
"ReferenceSchemaUId": "6c7394db-06ff-4050-91ef-8278e21dce15"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "04b821a5-71d6-44d9-b27d-f8562e54bb8a",
"Name": "IsMatchConditions",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
"SourceValue": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "e8992e0f-f8e9-4490-8eaf-ed670269e347",
"Name": "DataSourceFilters",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "394e160f-c8e0-46fa-9c0d-75d97e9e9169",
"SourceValue": {
"Source": 1,
"Value": "{\"className\":\"Terrasoft.FilterGroup\",\"serializedFilterEditData\":\"{\\\"className\\\":\\\"Terrasoft.FilterGroup\\\",\\\"items\\\":{\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\":{\\\"className\\\":\\\"Terrasoft.CompareFilter\\\",\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"className\\\":\\\"Terrasoft.ColumnExpression\\\",\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"isAggregative\\\":false,\\\"key\\\":\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\",\\\"dataValueType\\\":0,\\\"leftExpressionCaption\\\":\\\"Id\\\",\\\"rightExpression\\\":{\\\"className\\\":\\\"Terrasoft.ParameterExpression\\\",\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"className\\\":\\\"Terrasoft.Parameter\\\",\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\",\\\"displayValue\\\":\\\"Read Payments Record.First item of resulting collection.Id\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\",\\\"key\\\":\\\"\\\"}\",\"dataSourceFilters\":\"{\\\"items\\\":{\\\"ab92ce19-ffb8-416c-a873-7da4da900cfa\\\":{\\\"filterType\\\":1,\\\"comparisonType\\\":3,\\\"isEnabled\\\":true,\\\"trimDateTimeParameterToDate\\\":false,\\\"leftExpression\\\":{\\\"expressionType\\\":0,\\\"columnPath\\\":\\\"Id\\\"},\\\"rightExpression\\\":{\\\"expressionType\\\":2,\\\"parameter\\\":{\\\"dataValueType\\\":26,\\\"value\\\":{\\\"value\\\":\\\"[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{ae0e45ca-c495-4fe7-a39d-3ab7278e1617}]\\\"}}}}},\\\"logicalOperation\\\":1,\\\"isEnabled\\\":true,\\\"filterType\\\":6,\\\"rootSchemaName\\\":\\\"IWPayments\\\"}\"}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "79c8293c-2b8e-44be-926d-45c2a272c37f",
"Name": "RecordColumnValues",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"CreatedInPackageId": "66e9e705-64b4-4dda-925e-d1e05a389eb6",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "b53eaa2a-4bb7-4a6b-9f4f-58ccab293e31",
"SourceValue": {
"Source": 1,
"Value": "{\"$type\":\"Terrasoft.Core.Process.LocalizableParameterValuesList, Terrasoft.Core\",\"$values\":[{\"ItemUId\":\"c6b48774-5693-4e8a-82d5-b003cce67a06\",\"columnMetaPath\":{\"value\":\"5ecc730b-5012-af19-04cb-98a7a433162e\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{39cc5200-2e45-44b4-ab96-59da60240dc8}]#]\"},\"displayValue\":{\"value\":\"[#Commission Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"78bb8611-b1da-4492-8832-e3e093c978af\",\"columnMetaPath\":{\"value\":\"c59d6063-8484-f2dd-7e52-34077171ac39\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"e6a57ded-b853-49a3-8d3f-e6cef69e3a30\",\"columnMetaPath\":{\"value\":\"72360747-50bc-7a2e-24cd-c0f2bc94a294\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]\"},\"displayValue\":{\"value\":\"[#Calculated Sales Amount#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"969093e2-2b4e-463b-883a-3d3b8c61f0cd\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"523dbdaa-12f1-4286-a460-9d4435938692\",\"columnMetaPath\":{\"value\":\"e6ee8013-d6ab-c660-c6a7-f08bca97e67f\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#Lookup.94c61392-ccde-4274-88c6-7ffe7660250f.ee14b2ce-163a-4fb2-abea-e739636794ed#]\"},\"displayValue\":{\"value\":\"[#Lookup.IW Commission Status.Returned.ee14b2ce-163a-4fb2-abea-e739636794ed#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"94c61392-ccde-4274-88c6-7ffe7660250f\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"f9d86356-9683-4e1d-b725-35a1f0e26e0d\",\"columnMetaPath\":{\"value\":\"05c78c64-e9bb-166f-1021-88d4266003f9\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{81c8e318-76ac-4895-9a9b-9760b27c55ea}]#]\"},\"displayValue\":{\"value\":\"[#Read Order Record.First item of resulting collection.Owner#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"b295071f-7ea9-4e62-8d1a-919bf3732ff2\\\",\\\"ReferenceSchemaUId\\\":\\\"16be3651-8fe2-4159-8dd0-a803d4683dd3\\\",\\\"ResourceItemName\\\":null}\"}},{\"ItemUId\":\"7d127aeb-a201-45ef-a329-0aff0844245a\",\"columnMetaPath\":{\"value\":\"04921690-dcf6-d1c0-13c4-5c7b8c4444d6\"},\"schemaUId\":{\"value\":\"e1169637-8d6e-48d6-a129-0362fbdb7f65\"},\"value\":{\"value\":\"[#BooleanValue.True#]\"},\"displayValue\":{\"value\":\"[#Boolean value.True#]\"},\"parameterValue\":{\"value\":\"{\\\"$type\\\":\\\"Terrasoft.Core.Process.ProcessSchemaParameterValue, Terrasoft.Core\\\",\\\"Source\\\":3,\\\"DisplayValue\\\":\\\"\\\",\\\"Value\\\":\\\"\\\",\\\"MetaPath\\\":null,\\\"MetaDataValue\\\":null,\\\"ModifiedInSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"SchemaManagerName\\\":\\\"\\\",\\\"DataValueTypeUId\\\":\\\"90b65bf8-0ffc-4141-8779-2420877af907\\\",\\\"ReferenceSchemaUId\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ResourceItemName\\\":null}\"}}]}",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "edcdfcd7-49a3-417a-83c0-e5f763d63047",
"Name": "ConsiderTimeInFilter",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
"SourceValue": {
"Source": 3,
"Value": "true",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "false"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaParameter",
"UId": "50e14fd1-45d8-43c4-a9b5-acf014bcd475",
"Name": "IgnoreErrors",
"CreatedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"ContainerUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"DataValueType": "90b65bf8-0ffc-4141-8779-2420877af907",
"SourceValue": {
"Source": 3,
"Value": "false",
"ModifiedInSchemaUId": "d3021ca7-7450-4678-a117-060171eb2976",
"DefValueForExistingProcess": "true"
}
}
],
"FillColor": "FFFFFFFF",
"SchemaUId": "d3021ca7-7450-4678-a117-060171eb2976"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaExclusiveGateway",
"UId": "4150f8b0-73aa-44f8-bdbb-20787d7e618d",
"Name": "ExclusiveGateway4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ContainerUId": "108e3940-7b07-4c50-ac46-ea325af82370",
"Position": "1669;172",
"ManagerItemUId": "bd9f7570-6c97-4f16-90e5-663a190c6c7c",
"CreatedInOwnerSchemaUId": "8cdd4845-4b27-45cd-9907-e9cc478bc3c5",
"Size": "55;55",
"IsLogging": true,
"BranchingDecisions": []
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "0e1932d7-3ea3-4fc2-98e4-3b653f98ad2a",
"Name": "SequenceFlow2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
"TargetRefUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "0;1",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "268;172",
"SequenceFlowEndPointPosition": "325;108",
"PolylinePointPositions": {
"Item0": "268;108"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "441b533a-5171-4892-86ee-d0c49fedfef2",
"Name": "SequenceFlow7",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
"TargetRefUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SequenceFlowStartPointPosition": "360;135",
"SequenceFlowEndPointPosition": "360;261"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "11690780-1a2f-446c-b8a6-fccc69a7de99",
"Name": "SequenceFlow8",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "e739b215-25de-48a2-a5eb-9eb669921258",
"TargetRefUId": "b089222e-6f31-401a-93a3-7e0b6f8fd6a3",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "645;292",
"SequenceFlowEndPointPosition": "821;200",
"PolylinePointPositions": {
"Item0": "736;292",
"Item1": "736;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "caa3b891-a15f-4e8d-9345-f39959636664",
"Name": "SequenceFlow10",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "48173478-a29d-4aac-926b-f43be5f628ec",
"TargetRefUId": "4150f8b0-73aa-44f8-bdbb-20787d7e618d",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "0;-1",
"SequenceFlowStartPointPosition": "1519;292",
"SequenceFlowEndPointPosition": "1697;227",
"PolylinePointPositions": {
"Item0": "1697;292"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "fc9405a0-829d-4de9-9c8c-26ce47509263",
"Name": "SequenceFlow12",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "f95fa7ef-c895-4d06-816d-7436b030df07",
"TargetRefUId": "0017199f-49f2-4bf2-b68a-ae4cf7560203",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "394;289",
"SequenceFlowEndPointPosition": "447;200",
"PolylinePointPositions": {
"Item0": "421;289",
"Item1": "421;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaConditionalFlow",
"UId": "60b26c7d-c417-4714-a319-801ceae39eb7",
"Name": "ConditionalSequenceFlow1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "dac675d4-ea84-4e44-9056-38bf918618e9",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "a0e575c7-f091-4a97-be40-25756464a7bc",
"TargetRefUId": "48173478-a29d-4aac-926b-f43be5f628ec",
"ConditionExpression": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{f95fa7ef-c895-4d06-816d-7436b030df07}].[Parameter:{756c633c-0a6b-4a3a-b952-88d263cee609}].[EntityColumn:{9467a416-14c7-45ad-b86e-f1da6e817a7c}]#]>0",
"FlowType": 2,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "0;-1",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "1264;227",
"SequenceFlowEndPointPosition": "1450;292",
"PolylinePointPositions": {
"Item0": "1264;292"
},
"ProcessActivitiesSelectedResults": "{}",
"MatchBranchingDecisions": []
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "eb0d4110-5af3-4069-a0ff-6489ac4422a9",
"Name": "SequenceFlow13",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
"TargetRefUId": "67461fd9-b2a0-4ebc-a0be-895902c641b8",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "2009;281",
"SequenceFlowEndPointPosition": "2238;200",
"PolylinePointPositions": {
"Item0": "2103;281",
"Item1": "2103;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "ce6eefed-dc6a-4221-b7df-ea794d14e6a3",
"Name": "DefaultSequenceFlow1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "573ed909-e069-4161-b193-ae8dd9437c68",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "a0e575c7-f091-4a97-be40-25756464a7bc",
"TargetRefUId": "4150f8b0-73aa-44f8-bdbb-20787d7e618d",
"ConditionExpression": "null",
"FlowType": 1,
"StrokeColor": "FF939598",
"VisualType": 1,
"SequenceFlowStartPointPosition": "1291;200",
"SequenceFlowEndPointPosition": "1669;200"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "9fa6df14-162b-4817-b856-fc6b550c96ea",
"Name": "DefaultSequenceFlow2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "573ed909-e069-4161-b193-ae8dd9437c68",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "b089222e-6f31-401a-93a3-7e0b6f8fd6a3",
"TargetRefUId": "a0e575c7-f091-4a97-be40-25756464a7bc",
"ConditionExpression": "null",
"FlowType": 1,
"StrokeColor": "FF939598",
"VisualType": 1,
"SequenceFlowStartPointPosition": "876;200",
"SequenceFlowEndPointPosition": "1236;200"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaConditionalFlow",
"UId": "12d531a2-632c-4625-a429-1355d29bf1df",
"Name": "ConditionalSequenceFlow3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "dac675d4-ea84-4e44-9056-38bf918618e9",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "b089222e-6f31-401a-93a3-7e0b6f8fd6a3",
"TargetRefUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
"ConditionExpression": "[#[IsOwnerSchema:false].[IsSchema:false].[Parameter:{eab9b2d5-4600-4a94-840d-4243c218cd28}]#]<0",
"FlowType": 2,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "0;1",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "849;172",
"SequenceFlowEndPointPosition": "1022;108",
"PolylinePointPositions": {
"Item0": "849;108"
},
"ProcessActivitiesSelectedResults": "{}",
"MatchBranchingDecisions": []
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "70d1b8fe-17d1-4e89-9e23-fddb558e48a5",
"Name": "SequenceFlow9",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "52baca83-7627-42d1-a3de-cf6dc10ba2d4",
"TargetRefUId": "a0e575c7-f091-4a97-be40-25756464a7bc",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "0;1",
"SequenceFlowStartPointPosition": "1093;108",
"SequenceFlowEndPointPosition": "1264;172",
"PolylinePointPositions": {
"Item0": "1264;108"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "cc17d0d7-8a17-4788-897c-d4932e81c576",
"Name": "SequenceFlow11",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "46884467-984f-4940-89e3-8bf3cbce698f",
"TargetRefUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "81;108",
"SequenceFlowEndPointPosition": "233;200",
"PolylinePointPositions": {
"Item0": "157;108",
"Item1": "157;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "fe3bad98-aa90-4436-a9f0-9d30d94f0dd1",
"Name": "SequenceFlow14",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "522b0a0f-2cb7-4fbb-9a9b-172c42e68634",
"TargetRefUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SequenceFlowStartPointPosition": "81;200",
"SequenceFlowEndPointPosition": "233;200"
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "1020e4e0-3498-44ba-acdc-6d5ed3586ad2",
"Name": "SequenceFlow15",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "cee0cee7-0694-4883-851d-8c0903a2f150",
"TargetRefUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "81;289",
"SequenceFlowEndPointPosition": "233;200",
"PolylinePointPositions": {
"Item0": "157;289",
"Item1": "157;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaConditionalFlow",
"UId": "528a3990-7698-4a87-ad0c-e0c41ce65d28",
"Name": "ConditionalSequenceFlow2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "dac675d4-ea84-4e44-9056-38bf918618e9",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "0017199f-49f2-4bf2-b68a-ae4cf7560203",
"TargetRefUId": "e739b215-25de-48a2-a5eb-9eb669921258",
"ConditionExpression": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{145e999f-bfb3-4f4c-be2a-ec6cfa029a5e}].[Parameter:{c4c34584-9b8a-40ea-ad64-98389ea1942c}].[EntityColumn:{f397997e-a5b6-474d-a12f-9a1449c29e96}]#] > 0",
"FlowType": 2,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "0;-1",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "475;227",
"SequenceFlowEndPointPosition": "576;292",
"PolylinePointPositions": {
"Item0": "475;292"
},
"ProcessActivitiesSelectedResults": "{}",
"MatchBranchingDecisions": []
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "59a49bbc-b816-4101-9642-039e6316e010",
"Name": "DefaultSequenceFlow3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "573ed909-e069-4161-b193-ae8dd9437c68",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "0017199f-49f2-4bf2-b68a-ae4cf7560203",
"TargetRefUId": "b5908e55-8033-4f9f-aea4-87fff5fef224",
"ConditionExpression": "null",
"FlowType": 1,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "0;1",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "475;172",
"SequenceFlowEndPointPosition": "576;108",
"PolylinePointPositions": {
"Item0": "475;108"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "1953e1ff-3d30-4c3b-988f-cef6fc899774",
"Name": "SequenceFlow16",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "c2623b8a-338e-4adb-afbe-cb76b68368d9",
"SourceRefUId": "b5908e55-8033-4f9f-aea4-87fff5fef224",
"TargetRefUId": "b089222e-6f31-401a-93a3-7e0b6f8fd6a3",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "645;108",
"SequenceFlowEndPointPosition": "821;200",
"PolylinePointPositions": {
"Item0": "735;108",
"Item1": "735;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "1ad7d487-1f8f-43aa-80cb-84b5d4926a89",
"Name": "DefaultSequenceFlow4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "573ed909-e069-4161-b193-ae8dd9437c68",
"CreatedInOwnerSchemaUId": "8cdd4845-4b27-45cd-9907-e9cc478bc3c5",
"SourceRefUId": "4150f8b0-73aa-44f8-bdbb-20787d7e618d",
"TargetRefUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
"ConditionExpression": "null",
"FlowType": 1,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "1724;200",
"SequenceFlowEndPointPosition": "1940;281",
"PolylinePointPositions": {
"Item0": "1818;200",
"Item1": "1818;281"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaSequenceFlow",
"UId": "7382c68f-94f9-49f7-8ed8-f4b3584abe58",
"Name": "SequenceFlow1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "0d8351f6-c2f4-4737-bdd9-6fbfe0837fec",
"CreatedInOwnerSchemaUId": "8cdd4845-4b27-45cd-9907-e9cc478bc3c5",
"SourceRefUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"TargetRefUId": "67461fd9-b2a0-4ebc-a0be-895902c641b8",
"ConditionExpression": "null",
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "2009;108",
"SequenceFlowEndPointPosition": "2238;200",
"PolylinePointPositions": {
"Item0": "2102;108",
"Item1": "2102;200"
}
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaConditionalFlow",
"UId": "ad5903b6-fede-4f1a-9834-7e377f9ffe27",
"Name": "ConditionalSequenceFlow4",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"CreatedInPackageId": "21e7eb4b-a41b-42f1-913a-41046da1cb86",
"ManagerItemUId": "dac675d4-ea84-4e44-9056-38bf918618e9",
"CreatedInOwnerSchemaUId": "cf0b186b-2c88-4fe6-a52f-096c3031242b",
"SourceRefUId": "4150f8b0-73aa-44f8-bdbb-20787d7e618d",
"TargetRefUId": "d4cd2bf8-a1f6-439b-8a33-3df0b9802a4c",
"ConditionExpression": "[#[IsOwnerSchema:false].[IsSchema:false].[Element:{3f614fa3-2ef7-4f60-b3c7-01516d52ff0a}].[Parameter:{26dc550d-338f-467a-b7e3-3a969ad0ca23}].[EntityColumn:{e6ee8013-d6ab-c660-c6a7-f08bca97e67f}]#]==[#Lookup.94c61392-ccde-4274-88c6-7ffe7660250f.ee14b2ce-163a-4fb2-abea-e739636794ed#]",
"FlowType": 2,
"StrokeColor": "FF939598",
"VisualType": 1,
"SourceSequenceFlowPointLocalPosition": "1;0",
"TargetSequenceFlowPointLocalPosition": "-1;0",
"SequenceFlowStartPointPosition": "1724;200",
"SequenceFlowEndPointPosition": "1940;108",
"PolylinePointPositions": {
"Item0": "1818;200",
"Item1": "1818;108"
},
"ProcessActivitiesSelectedResults": "{}",
"MatchBranchingDecisions": []
}
],
"Associations": [],
"Tag": "Business Process",
"IsCreatedInSvg": true,
"IsInterpretable": true,
"CultureName": "en-US",
"Labels": [
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "82327fff-eb30-4f56-bfe9-2cab512c8a98",
"Name": "ReadDataUserTask1_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "3f614fa3-2ef7-4f60-b3c7-01516d52ff0a",
"X": -29
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "0772d5d7-6a17-479c-91ec-c1162de9e15b",
"Name": "ReadDataUserTask2_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "145e999f-bfb3-4f4c-be2a-ec6cfa029a5e",
"X": -18
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "b5bcd70c-99be-11e5-1be5-dcef42edaa19",
"Name": "ConditionalSequenceFlow1_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "60b26c7d-c417-4714-a319-801ceae39eb7",
"X": 59,
"Y": 126
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "0eede04a-ee59-dd5f-5e97-d2ac0f63b0b2",
"Name": "ConditionalSequenceFlow2_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "ce6eefed-dc6a-4221-b7df-ea794d14e6a3",
"X": 186,
"Y": 33
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "4f119479-1cc0-41f6-8c0c-56b12503e641",
"Name": "ExclusiveGateway1_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "a0e575c7-f091-4a97-be40-25756464a7bc",
"X": -37,
"Y": 55
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "01c5465e-47c9-95fa-bbbb-aa51e3c8d38d",
"Name": "ConditionalSequenceFlow2_label2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "9fa6df14-162b-4817-b856-fc6b550c96ea",
"X": 198
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "1a56cac3-6c91-4b9e-b270-4519e11b3ba2",
"Name": "ConditionalSequenceFlow3_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "12d531a2-632c-4625-a429-1355d29bf1df",
"X": 33,
"Y": -85
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "08959c98-8094-2cdc-c51a-3bb5cf32b0d6",
"Name": "ExclusiveGateway3_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "0017199f-49f2-4bf2-b68a-ae4cf7560203",
"X": -17
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "e528768b-69da-9ec3-805f-d67610eff125",
"Name": "ConditionalSequenceFlow2_label3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "528a3990-7698-4a87-ad0c-e0c41ce65d28",
"X": 2,
"Y": 122
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "5a115996-174e-ce7b-79a5-442182576d76",
"Name": "ConditionalSequenceFlow4_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "59a49bbc-b816-4101-9642-039e6316e010",
"X": -20,
"Y": -39
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "71a31f86-1f82-460e-a7aa-0505b7c37d24",
"Name": "ChangeDataUserTask1_label1",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "b7dc7a54-1524-4335-ab0d-60facfda268a",
"X": -29
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "ef802751-18e7-b377-c53e-4b26c79f3e16",
"Name": "ConditionalSequenceFlow4_label2",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "1ad7d487-1f8f-43aa-80cb-84b5d4926a89",
"X": 94,
"Y": 62
},
{
"TypeName": "Terrasoft.Core.Process.ProcessSchemaLabel",
"UId": "42579956-ae24-c9f6-b3ed-3b2b8de0026f",
"Name": "ConditionalSequenceFlow4_label3",
"CreatedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ModifiedInSchemaUId": "089ad409-d635-40c5-94b5-41c12fd112c2",
"ParentUId": "ad5903b6-fede-4f1a-9834-7e377f9ffe27",
"X": 91
}
],
"ExecutionContexts": []
}
}
}
