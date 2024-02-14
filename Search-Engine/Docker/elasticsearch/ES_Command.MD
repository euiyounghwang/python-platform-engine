
#### Elasticsearch Command
```bash
# Elasticsearch
curl -H 'Content-Type: application/json' -XPOST http://my-elasticsearch-host:9200/_reindex?wait_for_completion=false -d' {
  "conflicts": "proceed",
  "source": {
    "index": "old-index-name"
  },
  "dest": {
      "index": "new-index-name",
      "op_type": "create"
  }
}'

curl -H 'Content-Type: application/json' -XPOST http://my-elasticsearch-host:9200/_reindex?wait_for_completion=false -d' {
  "conflicts": "proceed",
  "source": {
    "index": "old-index-name",
    "_source": {
      "includes": ["field1", "field2"]
    }
  },
  "dest": {
      "index": "new-index-name",
      "op_type": "create"
  }
}'

curl -H 'Content-Type: application/json' -XPOST http://my-elasticsearch-host:9200/_reindex?wait_for_completion=false -d' {
  "conflicts": "proceed",
  "source": {
    "index": "old-index-name",
    "_source": {
      "includes": ["field1", "field2"]
    },
    "size": 10000,
    "query": {
      "bool": {
        "filter": [
          {
            "match_phrase": {
              "field1": "search_keyword"
            }
          },
          {
            "range": {
              "datetime": {
                "gte": "2018-07-05T05:05:54.000Z"
              }
            }
          }
        ]
      }
    }
  },
  "dest": {
      "index": "new-index-name",
      "op_type": "create"
  }
}'

curl -H 'Content-Type: application/json' -XPOST http://my-elasticsearch-host:9200/_reindex?wait_for_completion=false -d' {
  "conflicts": "proceed",
  "source": {
    "index": "old-index-name",
    "remote": {
      "host": "http://my-old-es-cluster-host:9200",
      "username": "user",
      "password": "pass"
    },
  },
  "dest": {
      "index": "new-index-name",
      "op_type": "create"
  }
}'


curl -H 'Content-Type: application/json' -GET http://localhost:9221/_cat/indices

curl -XPOST -u elastic:gsaadmin "http://localhost:9221/test_omnisearch_v2/_search/?pretty" -H 'Content-Type: application/json' -d' {
  "track_total_hits" : true,
  "query": {
    "match_all": {
    }
  }
}'
```