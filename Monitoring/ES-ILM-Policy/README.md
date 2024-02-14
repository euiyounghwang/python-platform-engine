# Elasticsearch ILM(Index Life-Cycle Management)

<i>You can configure index lifecycle management (ILM) policies to automatically manage indices according to your performance, resiliency, and retention requirements. For example, you could use ILM to:
- Spin up a new index when an index reaches a certain size or number of documents
- Create a new index each day, week, or month and archive previous ones
- Delete stale indices to enforce data retention standards

You can create and manage index lifecycle policies through Kibana Management or the ILM APIs. Default index lifecycle management policies are created automatically when you use Elastic Agent, Beats, or the Logstash Elasticsearch output plugin to send data to the Elastic Stack


```bash
# ILM roll over with index_template

# default : 10 minutes
PUT _cluster/settings
{
  "transient": {
    "indices.lifecycle.poll_interval" : "5s"
  }
}

GET _cluster/settings

DELETE _ilm/policy/omnisearch_highlight_policy

# policy
# max_primary_shard_size
# hot : 15d, colde : 15d, delete : 1d (evenry 15d create new index)
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

GET _ilm/policy/

GET _template

DELETE omnisearch_highlight_v2-*

DELETE _index_template/rolling

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


GET _cat/indices


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
    "index": "omnisearch_highlight_v2-000001",
    "op_type": "create"
  }
}

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


POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "omnisearch_highlight_v2-000001",
        "alias": "rolling-write-index",
        "is_write_index" : true
      }
    }
  ]
}

GET omnisearch_highlight_v2-000002
GET omnisearch_highlight_v2-000002/_ilm/explain

GET omnisearch_highlight_v2-000003

GET _cat/indices

```