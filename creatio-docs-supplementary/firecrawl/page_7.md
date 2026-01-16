<!-- Source: page_7 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/references/model#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

On this page

Level: intermediate

The `Model` class implements a data model to execute operations with data source records.

## Methods [​](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/references/model\#title-15180-1 "Direct link to Methods")

```js
load()
```

Retrieves a record from a data source. A configuration object is a key-value collection.

Parameters

```js
attributes
```

Specifies record columns to retrieve from the data source. The `attributes` property limits the retrieved data, which, in turn, improves performance and reduces unnecessary data transfer.

* * *

```js
parameters
```

An array of query filters.

Parameters

|     |     |
| --- | --- |
| type | The parameter type. The `ModelParameterType.Filter` value marks the parameter as a query filter. |
| value | The `BaseFilter` class instance that limits the retrieved data using the specified condition. |

To **retrieve a dedicated record**, set the `ModelParameterType.PrimaryColumnValue` value to the `type` parameter and record ID to the `value` parameter.

Example that retrieves a dedicated record

```js
const result = await model.load({
    attributes: ['Name'],
    parameters: [{\
        type: ModelParameterType.PrimaryColumnValue,\
        value: 'd4f93b6c-362c-4954-8bd6-1658e9206d4e'\
    }]
});
```

* * *

```js
loadOptions
```

Additional properties required to set up pagination, sorting and caching.

Parameters

|     |     |
| --- | --- |
| pagingConfig | Sets up pagination that controls rows of data to retrieve at once.

Parameters

|     |     |
| --- | --- |
| rowsOffset | An initial position (offset) to load the first portion of data. If you omit the property, Creatio sets the offset to "0." |
| rowCount | The number of records to upload to the page. | |
| sortingConfig | Sets up sorting of retrieved data.

Parameters

|     |     |
| --- | --- |
| columns | Specifies the initial data sorting settings.

Parameters

|     |     |
| --- | --- |
| columnName | Name of the column by which to sort data. |
| direction | Sorting order.

Available values

|     |     |
| --- | --- |
| asc | Ascending. |
| desc | Descending. | | | |
| cacheOperation | Manages caching of data retrieved from the data source.

Parameters

|     |     |
| --- | --- |
| updateCache | The flag that specifies whether the `load()` operation must retrieve data from the server and write it to the cache. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | Creatio Mobile retrieves data from the server and caches retrieved data. Creatio Mobile omits the `updateCache: true` parameter value in the following cases:<br>- The `readCacheMode` parameter is set to `ReadCacheMode.ForceLocal`.<br>- The **Mobile application operation mode** (`MobileApplicationMode` code) system setting is set to "offline" and the `EnableMobileDataAutoSynchronization` additional feature is disabled. |
| false | Creatio Mobile works with data directly from the cache, omitting the data source. This accelerates data retrieval. Creatio Mobile omits the `updateCache: false` parameter value in the following cases:<br>- The `readCacheMode` parameter is set to `ReadCacheMode.ForceRemote`.<br>- Creatio Mobile cannot retrieve the cached data from the data source. | |
| readCacheMode | Sets up how to retrieve data from the cache. By default, `ReadCacheMode.Auto`.

Available values

|     |     |
| --- | --- |
| ReadCacheMode.Auto | Creatio Mobile can retrieve data from the cache or directly from the data source based on the values of the **Mobile application operation mode** (`MobileApplicationMode` code) system setting and `updateCache` parameter. We recommend using the `ReadCacheMode.Auto` value regardless of the **Mobile application operation mode** (`MobileApplicationMode` code) system setting value. |
| ReadCacheMode.ForceLocal | Creatio Mobile retrieves data from the cache and omits updates in the data source. This is useful if you work in the offline mode or if you want to work with cached data only. |
| ReadCacheMode.ForceRemote | Creatio Mobile retrieves data directly from the data source, omitting the cache. This is useful if you want to work with up-to-date data only. | |
| cacheDataType | Determines whether to load records fully and set all columns required in the app. By default, `CacheDataType.Partial`.

Available values

|     |     |
| --- | --- |
| CacheDataType.Partial | Stores only a portion of data in the cache. It is used to load data collection. |
| CacheDataType.Full | Stores the data in the cache entirely. It is used to load a single record. When you use the `CacheDataType.Full` parameter value, make sure that all required columns are set to the `attributes` parameter. | |
| syncRuleName | Sets up a rule to synchronize the cache. Learn more: [SyncRules](https://academy.creatio.com/documents?id=15878&anchor=sync-rules). | |

* * *

```js
insert()
```

Adds a record to a data source. A configuration object is a key-value collection.

Parameters

```js
cacheOperation
```

Manages caching of data added to the data source.

Parameters

|     |     |
| --- | --- |
| updateCache | The flag that specifies whether the `insert()` operation must retrieve data from the server and write it to the cache. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | Creatio Mobile caches added data. Creatio Mobile omits the `updateCache: true` parameter value when the `EnableMobileDataAutoSynchronization` additional feature is enabled. |
| false | Creatio Mobile works with data directly from the cache, omitting the data source. | |

* * *

```js
copy()
```

Copies the original record from a data source. To add a new record, use the `model.insert()` method. Specify record ID that identifies a record to copy from the data source and a list of modified values for a new record.

* * *

```js
update()
```

Modifies a record in a data source. A configuration object is a key-value collection.

Parameters

```js
{DataSourceParameters}
```

An array of parameters that identify a record to modify.

Parameters

|     |     |
| --- | --- |
| type | The parameter type. The `ModelParameterType.PrimaryColumnValue` value marks the parameter as a record ID. |
| value | The record ID. |

* * *

```js
cacheOperation
```

Manages caching of data modified in the data source.

Parameters

|     |     |
| --- | --- |
| updateCache | The flag that specifies whether the `update()` operation must retrieve data from the server and write it to the cache. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | Creatio Mobile caches modified data. Creatio Mobile omits the `updateCache: true` parameter value when the `EnableMobileDataAutoSynchronization` additional feature is enabled. |
| false | Creatio Mobile works with data directly from the cache, omitting the data source. | |

* * *

```js
delete()
```

Deletes a record from a data source. A configuration object is a key-value collection.

Parameters

```js
{DataSourceParameters}
```

An array of parameters that identify a record to delete.

Parameters

|     |     |
| --- | --- |
| type | The parameter type. The `ModelParameterType.PrimaryColumnValue` value marks the parameter as a record ID. |
| value | The record ID. |

* * *

```js
cacheOperation
```

Manages caching of data deleted from the data source.

Parameters

|     |     |
| --- | --- |
| updateCache | The flag that specifies whether the `delete()` operation must retrieve data from the server and write it to the cache. By default, `true`.

Available values

|     |     |
| --- | --- |
| true | Creatio Mobile caches deleted data. Creatio Mobile omits the `updateCache: true` parameter value when the `EnableMobileDataAutoSynchronization` additional feature is enabled. |
| false | Creatio Mobile works with data directly from the cache, omitting the data source. | |

- [Methods](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/operations-with-data-source/references/model#title-15180-1)