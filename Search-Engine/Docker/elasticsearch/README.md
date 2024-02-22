
# The summary of Elasticsearch


### Create Shell script for running/stopping the instance of Elasticsearch
```bash 
$ echo 'bin/elasticsearch -d -p es.pid' > start.sh
$ echo 'kill `cat es.pid`' > stop.sh
$ chmod 755 start.sh stop.sh
```

### The option for running the instance of Elasticsearch
```bash 
$ bin/elasticsearch -E cluster.name=my-cluster -E node.name="node-1"
```

### CRUD in Elasticsearch
```bash 
#--- index, create, update, delete

POST _bulk
{"index":{"_index":"test", "_id":"1"}}
{"field":"value one"}
{"index":{"_index":"test", "_id":"2"}}
{"field":"value two"}
{"delete":{"_index":"test", "_id":"2"}}
{"create":{"_index":"test", "_id":"3"}}
{"field":"value three"}
{"update":{"_index":"test", "_id":"1"}}
{"doc":{"field":"value two"}}

# Bulk json using file
$ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json


POST _bulk
{ "index": { "_index": "my-index-b", "_id" : "1"} }
{ "field1": "value1" }

POST _bulk
{ "update": { "_index": "my-index-b", "_id": "1" } }
{ "doc": { "field1": "value1" }, "doc_as_upsert": true }
#--- upsert, doc_as_upsert, script, params

POST my-index-b/_search
{
  "query": {
    "match_all": {}
  }
}

#--
DELETE logs-debug
PUT logs-debug
{
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "message": {
        "type": "text"
      },
      "level": {
        "type": "constant_keyword",
        "value": "debug"
      }
    }
  }
}

POST logs-debug/_doc
{
  "date": "2019-12-12",
  "message": "Starting up Elasticsearch",
  "type": "log",
  "level": "debug"
}

POST logs-debug/_doc
{
  "date": "2019-12-12",
  "type": "log1",
  "message": "Starting up Elasticsearch"
}

POST logs-debug/_search
{
  "query": {
    "match_all": {}
  }
}

POST logs-debug/_update_by_query
{
  "script": {
    "source": "ctx._source['update'] = 'test'"
  },
  "query": {
    "term": {
      "type.keyword": "log1"
    }
  }
}
```


### Join in Elasticsearch
```bash 

DELETE my_index

PUT my_index
{
  "mappings": {
      "properties": {
        "acl_join_field": { 
          "type": "join",
          "relations": {
            "parent": "child" 
          }
        }
    }
  }
}


# parent index
PUT _bulk
{"index":{"_index":"my_index","_id":"1"}}
{"text":"This is a question","acl_join_field":{"name":"parent"}}


# child index
PUT _bulk?routing=1&refresh
{"index":{"_index":"my_index","_id":"3"}}
{"text":"This is a child","authz":["1","2"], "acl_join_field":{"name":"child","parent":"1"}}


GET my_index
GET my_index/_search

GET _cat/indices

GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "has_child": {
            "type": "child",
            "query": {
              "terms": {
                "authz": [
                  "1",
                  "100"
                ]
              }
            }
          }
        }
      ]
    }
  }
}
```


### reindex in Elasticsearch
- The new cluster doesn’t have to start fully-scaled out. As you migrate indices and shift the load to the new cluster, you can add nodes to the new cluster and remove nodes from the old one.
- Create an index with the appropriate mappings and settings. Set the refresh_interval to -1 and set number_of_replicas to 0 for faster reindexing.

```bash 
# - reindex.remote.whitelist="192.168.68.1:*,host.docker.internal:*,localhost:*"

# "refresh_interval" : "1s"
PUT test-000001/_settings
{
  "index" : {
    "number_of_replicas" : 0,
    "refresh_interval" : -1
  }
}


POST _reindex?wait_for_completion=false
{
  "conflicts": "proceed",
  "source": {
    "index": "test_set",
    "query": {
      "bool": {
        "must_not": [
          {
            "exists": {
              "field": "query"
            }
          }
        ]
      }
    }
  },
  "dest": {
    "index": "test-000001",
    "op_type": "create"
  }
}

POST _reindex?wait_for_completion=true
{
  "source": {
    "remote": {
      "host": "http://host.docker.internal:9209",
      "username": "elastic",
      "password": "your_password"
    },
    "index": "performance_metrics",
    "query": {
     "match_all": {}
    }
  },
  "dest": {
    "index": "cp99_performance_metrics"
  }
}

GET _cat/indices

GET _tasks?detailed=true&actions=*reindex

GET _tasks/BH_UUNP2RjafE0aNHGi_Hw:216731707
```

### Configuration
```bash 

#--
# configuration
# default 1 second
PUT my_index
{
  "settings": {
    "refresh_interval": "30s"
  }
}

# search_analyzer, analyzer
# normalizer : Elasticsearch normalizers are a crucial component in the text analysis process, specifically when dealing with keyword fields
PUT blogs
{
  "settings": {
    "analysis": {
      "analyzer": {
        "engram_a": {
          "tokenizer": "standard",
          "filter": [ "lowercase", "engram_f" ]
        }
      },
      "filter": {
        "engram_f": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 5
        }
      },
      "normalizer": {
        "norm_low": {
          "type": "custom",
          "filter": [ "lowercase", "asciifolding" ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "normalizer": "norm_low"
          }
        }
      },
      "author": {
        "type": "text",
        "analyzer": "engram_a",
        "search_analyzer": "standard",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "synopsis": {
        "type": "text",
        "fielddata": true
      },
      "category": {
        "type": "keyword"
      },
      "content": {
        "type": "text",
        "index": false
      }
    }
  }
}

POST blogs/_analyze
{
  "normalizer": "norm_low",
  "text": "2 Quick Foxes."
}
```


### ILM in Elasticsearch
- You can configure index lifecycle management (ILM) policies to automatically manage indices according to your performance, resiliency, and retention requirements
- Spin up a new index when an index reaches a certain size or number of documents
- Create a new index each day, week, or month and archive previous ones
- Delete stale indices to enforce data retention standards

```bash 
# test
PUT /_ilm/policy/omnisearch_highlight_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "5GB",
            "max_docs": 2,
            "max_age": "15d"
          }
        }
      },
      "cold": {
        "min_age": "0m",
        "actions": {}
      },
      "delete": {
        "min_age": "5m",
        "actions": {
          "delete": {
            "delete_searchable_snapshot": true
          }
        }
      }
    }
  }
}


# need to update the alias
PUT _index_template/rolling
{
  "index_patterns": [
    "omnisearch_highlight_v*"
  ],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "index.lifecycle.name": "omnisearch_highlight_policy",
      "index.lifecycle.rollover_alias": "rolling-write-index",
      "analysis": {
        "analyzer": {
          "test_analyzer": {
            "filter": [
              "lowercase",
              "stop",
              "snowball"
            ],
            "char_filter": [
              "test_char_filter"
            ],
            "tokenizer": "whitespace"
          }
        },
        "char_filter": {
          "test_char_filter": {
            "type": "mapping",
            "mappings": [
              "+ => _plus_",
              "- => _minus_"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "my_keyword_field": {
          "type": "keyword"
        }
      }
    }
  }
}


# different index
PUT _bulk
{"index":{"_index":"test_set"}}
{"my_keyword_field": "man"}



GET omnisearch_highlight_v2-000001
GET omnisearch_highlight_v2-000001/_ilm/explain


GET omnisearch_highlight_v2-*/_search
{
  "track_total_hits": true, 
  "query": {
    "match_all": {}
  },
  "size": 200
}

GET _cat/aliases


# ilm alias
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "omnisearch_highlight_v2-000001",
        "alias": "rolling-write-index"
      }
    }
  ]
}


PUT _bulk
{"index":{"_index":"rolling-write-index"}}
{"my_keyword_field": "man"}



GET omnisearch_highlight_v2-000002
GET omnisearch_highlight_v2-000002/_ilm/explain

GET omnisearch_highlight_v2-000003

GET _cat/indices?v

GET myindex-create-from-curator2/_settings
GET myindex-create-from-curator2/_mapping

```


### snapshot in Elasticsearch
```bash 

# register snapshot
PUT /_snapshot/my_backup
{
  "type": "fs",
  "settings": {
    "compress": true,
    "location": "/usr/share/elasticsearch/backup"
  }
}

GET /_snapshot/my_backup


# take a snapshot
PUT /_snapshot/my_backup/backup_20240209?wait_for_completion=true
{
  "indices": "test_index1",
  "ignore_unavailable": true,
  "include_global_state": true
}

DELETE _snapshot/my_backup/test_index-20240210

GET /_snapshot/my_backup/backup_20240209
GET /_snapshot/my_backup/backup_20240209/_status

POST _snapshot/my_backup/backup_20240209/_restore
{
  "indices": "test_index1",
   "ignore_unavailable": true,
  "include_global_state": false,              
  "rename_pattern": "(.+)",
  "rename_replacement": "$1_restored",
  "include_aliases": false
}
```


### Search in Elasticsearch
```bash 

# --
POST my_index/_bulk
{"index":{"_id":1}}
{"message":"The quick brown fox"}
{"index":{"_id":2}}
{"message":"The quick brown fox jumps over the lazy dog"}
{"index":{"_id":3}}
{"message":"The quick brown fox jumps over the quick dog"}
{"index":{"_id":4}}
{"message":"Brown fox brown dog"}
{"index":{"_id":5}}
{"message":"Lazy jumping dog"}


GET my_index/_search
{
  "query": {
    "match": {
      "message": {
        "query": "quick dog",
        "operator": "and"
      }
    }
  },
  "highlight": {
    "require_field_match": true,
    "order": "score",
    "pre_tags": [
      "<b>"
    ],
    "post_tags": [
      "</b>"
    ],
    "fields": {
      "*": {
        "number_of_fragments": 1,
        "type": "plain",
        "fragment_size": 150
      }
    }
  }
}


GET my_index/_search
{
  "query": {
    "match_phrase": {
      "message": {
        "query": "lazy dog",
        "slop": 1
      }
    }
  }
}

```

### Search-Profiler on Dev Console in Kibana
![Alt text](../../../screenshot/Search-Profiler.png)


### Analyze
```bash 
#--
GET _analyze
{
  "text": "The quick brown fox jumps over the lazy dog",
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    "stop",
    "snowball"
  ]
}

# same result with lowercase, stop token filter
GET _analyze
{
  "text": "The quick brown fox jumps over the lazy dog",
  "analyzer": "snowball"
}

GET my_index2

PUT my_index2
{
  "mappings": {
    "properties": {
      "message": {
        "type": "text",
        "analyzer": "snowball"
      }
    }
  }
}

PUT my_index2/_doc/1
{
  "message": "The quick brown fox jumps over the lazy dog"
}


GET my_index2/_search
{
  "query": {
    "match": {
      "message": "jumping"
    }
  }
}

# Cheeck termvectors
GET my_index2/_termvectors/1?fields=message



DELETE my_index3

PUT my_index3
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_custom_analyzer": {
            "type": "custom",
            "tokenizer": "whitespace",
            "filter": [
              "lowercase",
              "my_stop_filter",
              "snowball"
            ]
          }
        },
        "filter": {
          "my_stop_filter": {
            "type": "stop",
            "stopwords": [
              "brown"
            ]
          }
        }
      }
    }
  }
}

GET my_index3/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": [
    "The quick brown fox jumps over the lazy dog"
  ]
}


# character filter
POST _analyze
{
  "tokenizer": "keyword",
  "char_filter": [
    "html_strip"
  ],
  "text": "<p>I&apos;m so <b>happy</b>!</p>"
}

PUT coding
{
  "settings": {
    "analysis": {
      "analyzer": {
        "coding_analyzer": {
          "char_filter": [
            "cpp_char_filter"
          ],
          "tokenizer": "whitespace",
          "filter": [ "lowercase", "stop", "snowball" ]
        }
      },
      "char_filter": {
        "cpp_char_filter": {
          "type": "mapping",
          "mappings": [ "+ => _plus_", "- => _minus_" ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "language": {
        "type": "text",
        "analyzer": "coding_analyzer"
      }
    }
  }
}

POST coding/_bulk
{"index":{"_id":"1"}}
{"language":"Java"}
{"index":{"_id":"2"}}
{"language":"C"}
{"index":{"_id":"3"}}
{"language":"C++"}

GET coding/_termvectors/3?fields=language

GET coding/_search
{
  "query": {
    "match": {
      "language": "C++"
    }
  }
}


# tokenizer
GET _analyze
{
  "tokenizer": "standard",
  "text": "THE quick.brown_FOx jumped! @ 3.5 meters."
}

GET _analyze
{
  "tokenizer": "standard",
  "text": "email address is my-name@email.com and website is https://www.elastic.co"
}

# token filter
GET _analyze
{
  "filter": [ "lowercase" ],
  "text": [ "Harry Potter and the Philosopher's Stone" ]
}

# add stop filter
PUT my_stop
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords_path": "user_dic/my_stop_dic.txt"
        }
      }
    }
  }
}

GET my_stop/_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    "my_stop_filter"
  ],
  "text": [ "Around the World in Eighty Days" ]
}

GET _analyze
{
  "tokenizer": "standard",
  "filter": [
    "lowercase",
    "unique"
  ],
  "text": [
    "white fox, white rabbit, white bear"
  ]
}
```


### nGram/Edge
```bash 

DELETE my_ngram

PUT my_ngram
{
  "settings": {
    "analysis": {
      "filter": {
        "my_ngram_f": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      }
    }
  }
}

GET my_ngram/_analyze
{
  "tokenizer": "keyword",
  "filter": [
    "my_ngram_f"
  ],
  "text": "house"
}

PUT my_shingle
{
  "settings": {
    "analysis": {
      "filter": {
        "my_shingle_f": {
          "type": "shingle",
          "min_shingle_size": 3,
          "max_shingle_size": 4
        }
      }
    }
  }
}

GET my_shingle/_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "my_shingle_f"
  ],
  "text": "this is my sweet home"
}

PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "my_tokenizer"
        }
      },
      "tokenizer": {
        "my_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "analyzer": "my_analyzer",
  "text": "2 Quick Foxes."
}
```

### Aggregations

```bash 
# -- 
# aggregation

GET my_stations

PUT my_stations/_bulk
{"index": {"_id": "1"}}
{"date": "2019-06-01", "line": "1호선", "station": "종각", "passangers": 2314}
{"index": {"_id": "2"}}
{"date": "2019-06-01", "line": "2호선", "station": "강남", "passangers": 5412}
{"index": {"_id": "3"}}
{"date": "2019-07-10", "line": "2호선", "station": "강남", "passangers": 6221}
{"index": {"_id": "4"}}
{"date": "2019-07-15", "line": "2호선", "station": "강남", "passangers": 6478}
{"index": {"_id": "5"}}
{"date": "2019-08-07", "line": "2호선", "station": "강남", "passangers": 5821}
{"index": {"_id": "6"}}
{"date": "2019-08-18", "line": "2호선", "station": "강남", "passangers": 5724}
{"index": {"_id": "7"}}
{"date": "2019-09-02", "line": "2호선", "station": "신촌", "passangers": 3912}
{"index": {"_id": "8"}}
{"date": "2019-09-11", "line": "3호선", "station": "양재", "passangers": 4121}
{"index": {"_id": "9"}}
{"date": "2019-09-20", "line": "3호선", "station": "홍제", "passangers": 1021}
{"index": {"_id": "10"}}
{"date": "2019-10-01", "line": "3호선", "station": "불광", "passangers": 971}


GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "all_passangers": {
      "sum": {
        "field": "passangers"
      }
    }
  }
}

GET my_stations/_search
{
  "query": {
    "match": {
      "station": "불광"
    }
  },
  "size": 0,
  "aggs": {
    "gangnam_passangers": {
      "sum": {
        "field": "passangers"
      }
    }
  }
}


GET my_stations/_search
{
  "size": 0, 
  "aggs": {
    "passangers_stats": {
      "stats": {
        "field": "passangers"
      }
    }
  }
}

GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "uniq_lines": {
      "cardinality": {
        "field": "line.keyword"
      }
    }
  }
}

GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "pass_percentiles": {
      "percentiles": {
        "field": "passangers",
        "percents": [ 20, 60, 80 ]
      }
    }
  }
}


GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "passangers_range": {
      "range": {
        "field": "passangers",
        "ranges": [
          {
            "to": 1000
          },
          {
            "from": 1000,
            "to": 4000
          },
          {
            "from": 4000
          }
        ]
      }
    }
  }
}


GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "passangers_his": {
      "histogram": {
        "field": "passangers",
        "interval": 2000
      }
    }
  }
}

GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "date_his": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "month"
      }
    }
  }
}

GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "stations": {
      "terms": {
        "field": "station.keyword"
      }
    }
  }
}

GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "stations": {
      "terms": {
        "field": "station.keyword"
      },
      "aggs": {
        "avg_psg_per_st": {
          "avg": {
            "field": "passangers"
          }
        }
      }
    }
  }
}


GET my_stations/_search
{
  "size": 0,
  "aggs": {
    "lines": {
      "terms": {
        "field": "line.keyword"
      },
      "aggs": {
        "stations_per_lines": {
          "terms": {
            "field": "station.keyword"
          }
        }
      }
    }
  }
}
```



### Point in Time

```json 
# Point in time for deep pagination
# use the search_after parameter with a point in time (PIT).
# In your reponse, you need to look at the last hit and take the sort value from that last hit
# Then in your next search call, you'll specify that value in search_after
# "search_after": [ "100000012", "98" ],  
POST test_index1_restored/_pit?keep_alive=1m

POST /_search
{
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ], 
  "size": 100,
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "tags": [
              "elasticsearch"
            ]
          }
        }
      ]
    }
  },
  "pit": {
    "id": "45XtAwEUdGVzdF9pbmRleDFfcmVzdG9yZWQWbVlFWlNTMTZUdUtkWjhkc0t2WWt6QQAWekdqYzZ4QXFTU2V4MktHMzlyVDFfZwAAAAAAAABgHxZZVzF3VUlnUlJDUzkwNHZzSWg5TVR3AAEWbVlFWlNTMTZUdUtkWjhkc0t2WWt6QQAA",
    "keep_alive": "1m"
  }
}

DELETE /_pit
{
    "id" : "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
}
```