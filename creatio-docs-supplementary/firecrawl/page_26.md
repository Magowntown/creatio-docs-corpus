<!-- Source: page_26 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

Execute operations with data sources implemented via the `BaseDataSource` class using the `Model` class that implements a data model and includes the `DataSourceCacheableLoadOptions` interface. The interface is a wrapper to execute the following operations with the data source:

- retrieve record
- add record
- modify record
- delete record

To execute operations, **create an instance** of the `Model` class using the `Model.create()` method. This method receives the code of the data source to interact with the instance. I. e., the model instance is associated with the data source and the model will be able to execute operations with records from the specified data source.

View the example that creates a `Model` class instance, which, in turn, interacts with the `Contact` data source below.

Example that creates a Model class instance

```js
const model = await Model.create('Contact');
```

## Retrieve record [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview\#title-15179-1 "Direct link to Retrieve record")

Use the `model.load()` method to retrieve records from a data source. The `model.load()` method lets you use attributes (`attributes` parameter), parameters (`parameters` parameter) and options of additional data processing (`loadOptions` parameter). Learn more: [Model class](https://academy.creatio.com/documents?id=15180).

View the example that retrieves records from the **Contact** section below.

Example that retrieves records from the Contact section

```js
const result = await model.load({
    attributes: ['SomeAttribute'],
    parameters: [{\
        type: ModelParameterType.Filter,\
        value: new CompareFilter(\
            ComparisonType.Contain,\
            new ColumnExpression({ columnPath: 'SomeColumn1' }),\
            new ParameterExpression({ value: 'SomeColumn1Value' }),\
        )\
    }],
    loadOptions: {
        pagingConfig: {
            rowsOffset: 0,
            rowCount: 5
        },
        sortingConfig: {
            columns: [{\
                columnName: 'SomeColumn2',\
                direction: 'desc'\
            }]
        },
        cacheOperation: {
            updateCache: true,
            readCacheMode: ReadCacheMode.Auto,
            cacheDataType: CacheDataType.Full,
            syncRuleName: 'ActivityModuleSyncRule'
        }
    }
});
```

## Add record [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview\#title-15179-2 "Direct link to Add record")

Use the `model.insert()` method to add a record to a data source. This method receives a JSON object that is a key-value collection. The key is the column name and the value is the column value. Learn more: [Model class](https://academy.creatio.com/documents?id=15180).

View the example that adds a record to the **Contact** section below.

Example that adds a record to the Contact section

```js
const result = await model.insert({

    /* Add a column whose value is a "string." */
    SomeColumn1: 'SomeColumn1Value',

    /* Add a column whose value is a lookup value. */
    SomeColumn2: '384d4b84-58e6-df11-971b-001d60e938c6',

    /* Add a column whose value is a "Datetime" type. */
    SomeColumn3: new Date().toUTCString(),

    /* Add a column whose value is a number. */
    SomeColumn4: 15,

    cacheOperation: {
        updateCache: false
    }
});
```

Creatio Mobile lets you **add a new record created from an existing record**. To do this, use the `model.copy()` method that copies the original record from a data source and the `model.insert()` method that adds a new record. This method receives a record ID that identifies a record to copy and a list of modified values for a new record. Other column values in a new record and original record are the same. Creatio Mobile is able to copy only columns whose `clonable` property is set to `true`. Learn more: [Model class](https://academy.creatio.com/documents?id=15180).

View the example that adds a record created from an existing record whose ID is "d4f93b6c-362c-4954-8bd6-1658e9206d4e" to the **Contact** section below.

Example that adds a record created from an existing record to the Contact section

```js
const record = await model.copy(
    'd4f93b6c-362c-4954-8bd6-1658e9206d4e',
    {
        'SomeColumn': 'SomeNewColumnValue'
    }
);

const result = await model.insert(record);
```

## Modify record [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview\#title-15179-3 "Direct link to Modify record")

Use the `model.update()` method to modify a record in a data source. This method receives a JSON object that is a key-value collection and an array of parameters that identify a record to modify. The key is the column name and the value is a new column value. Learn more: [Model class](https://academy.creatio.com/documents?id=15180).

View the example that modifies a record in the **Contact** section whose ID is "d4f93b6c-362c-4954-8bd6-1658e9206d4e" below.

Example that modifies a record in the Contact section

```js
const result = await model.update(
    {
        'SomeColumn': 'SomeNewColumnValue'
    },
    [{\
        type: ModelParameterType.PrimaryColumnValue,\
        value: 'd4f93b6c-362c-4954-8bd6-1658e9206d4e'\
    }],
    {
        cacheOperation: {
            updateCache: false
        }
    }
)
```

## Delete record [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview\#title-15179-4 "Direct link to Delete record")

Use the `model.delete()` method to delete a record from a data source. This method receives a JSON object that is a key-value collection and an array of parameters that identify a record to delete. The key is the column name and the value is a new column value. Learn more: [Model class](https://academy.creatio.com/documents?id=15180).

View the example that deletes a record from the **Contact** section whose ID is "d4f93b6c-362c-4954-8bd6-1658e9206d4e" below.

Example that deletes a record from the Contact section

```js
const result = await model.delete(
    {
        'SomeColumn': 'SomeColumnValue'
    },
    [{\
        type: ModelParameterType.PrimaryColumnValue,\
        value: 'd4f93b6c-362c-4954-8bd6-1658e9206d4e'\
    }],
    {
        cacheOperation: {
            updateCache: false
        }
    }
)
```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview\#see-also "Direct link to See also")

[Model class](https://academy.creatio.com/documents?id=15180)

- [Retrieve record](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#title-15179-1)
- [Add record](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#title-15179-2)
- [Modify record](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#title-15179-3)
- [Delete record](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#title-15179-4)
- [See also](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/overview#see-also)