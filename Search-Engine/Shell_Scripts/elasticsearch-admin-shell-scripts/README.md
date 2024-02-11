# elasticsearch-admin-scripts

This repo stores the Cerebro team's scripts that make it easier to manage Elasticsearch. Detailed descriptions, including required arguments and example usages, are in the scripts themselves.

## Bash scripts

### indexUtil.sh
Every script makes use of `indexUtil.sh` for argument handling and url building. Possible arguments and examples follow.

### Required args
Every script requires two arguments:
* `env`: the environment of the cluster the script is run against. This is used to build the URL of the cluster the script will be run against. Options are:
  * `local`
  * `oscf-dev`
  * `oscf-stage`
  * `oscf-prod`
* `user`: a user name with access to the cluster in `env`. You will be prompted for the password when the script is run.

### Other arguments

#### `index`
Name of the index the command will run against. You can see what indexes are on your cluster by running `./indexList.sh` for the desired environment.

#### `docType`
The name of the type of document that the command will run against, e.g. `constituent`. You define document types on your index with a name and field mappings. An index may have multiple types.

#### `alias`
The index alias the script will be run against, e.g. `lonxt-current`. You can see what aliases have been created on your cluster with `./getIndexAliases.sh`.

#### `docMappingFile`
The path to a file with the json mapping for a document type. For example:
```json
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "type1" : {
            "properties" : {
                "field1" : { "type" : "text" }
            }
        }
    }
}
```

#### `query`
The path to a file containing the body of the search query request that will be made against an index. Note: must be valid json. Example:
```json
{
    "query": {
        "term": { "contact_id": "782cd1a5-a560-4c77-a9ed-904d8d1a582b" }
    }
}
```

#### `update`
The path of a file containing the body of the update request that will be made against an index. Note: must be valid json. Example:
```json
{
    "script": {
        "lang": "painless",
        "file": "delete_individual_gift",
        "params": {
            "gift_id": "1"
        }
    },
    "query": {
        "term": { "contact_id": "783cd1a5-a260-4c67-aaed-904d8d1a582b" }
    }
}
```

#### `file`
The path of a file containing some json used to add or update some aspect of the cluster or index. Script-dependent.

#### `slices`
A positive integer value indicating the number of slices Elasticsearch should use in an update by query. Note: this is only applicable to the `updateByQueryLongRunning` script. Note also that Elasticsearch suggests using a multiple of the number of shards on the index, with the best performance seen using the exact number of shards on the index.


#### Bash Test
```bash
python-platform-engine git:(master) ./Search-Engine/Shell_Scripts/elasticsearch-admin-shell-scripts/list-indices.sh f localhost 9203  
health status index                          uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test_ngram_v1                  cMk8KTfWSISrU2upxavdVA   1   0          1            0      4.4kb          4.4kb
green  open   test_performance_metrics_v1    PXVEjhJuQrqgKr2JP8fNHg   1   0          1            0      7.4kb          7.4kb
yellow open   test_index-20240201            -9OnSULZScucUE4jNG6CBA   1   1          1            0      5.4kb          5.4kb
yellow open   test_index11_restored          vx3XCzGJTQOctA4qfDGA6w   1   1          1            0      5.4kb          5.4kb
yellow open   myindex                        g9nto-dxQ-m1SEi5yOYGuw   2   1          0            0       494b           494b
yellow open   test_index-20240209            9M4w_pD2TL-L2VrevkxdSg   1   1          1            0      5.4kb          5.4kb
green  open   omnisearch_highlight_v2-000004 C9rBAxziQHyQX2UsGYUpdQ   1   0          0            0       247b           247b
yellow open   test_index1_restored           mYEZSS16TuKdZ8dsKvYkzA   1   1          1            0      5.4kb          5.4kb
yellow open   test_set                       tCuQ5xxBQraiDMIHRp_pfA   1   1          9            0     22.9kb         22.9kb
```


## Prettifying output
Output of the scripts being run is in unformatted json. We highly recommend you install and use `jq`.

## Task monitoring script
We have a handy dandy little python script to report out Elasticsearch task info, which is most useful like so:
```bash
watch -n 3 "curl -# --user 'elastic:PASSWORD' 'http://es-master.oscf-prod.blackbaudcloud.com:9200/_tasks?detailed=true&actions=*byquery' | python3 taskStatus.py
```

Things to note:
* `-n 3` indicates the watch will update every 3 seconds.
* `PASSWORD` will need to change.
* `actions=*byquery` specifically targets Update By Query tasks. This can be changed to monitor other tasks (e.g.`*reindex`).
