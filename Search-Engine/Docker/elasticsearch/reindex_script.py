import json

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import argparse
import datetime
import warnings

warnings.filterwarnings('ignore')

def get_headers():
    ''' Elasticsearch Header '''
    return {'Content-type': 'application/json', 'Connection': 'close'}

def get_es_instance(_host):
    # create a new instance of the Elasticsearch client class
    es_client = Elasticsearch(hosts=_host, headers=get_headers(), timeout=600)
    return es_client


def work_reindex_api(src_es, dest_es, src_idx, dest_idx):
    ''' processing using _reindex api '''
    
    print(f'src_es - {src_es}')
    # scroll_time='60s'
    scroll_time='1m'
    batch_size='1000'
    
    ''' 
    It's not working and you can see the following error message if your es cluster is higher than the current cluster and you ar using _reindex_api
    TransportError(500, 'exception', 'Error parsing the response, remote is likely not an Elasticsearch instance')
    '''
    '''
    query = {
        "conflicts": "proceed",
        "source": {
            "remote": {
                "host": "http://host.docker.internal:9209",
                "username": "elastic",
                "password": "gsaadmin"
            },
            "index": src_idx,
            "query": {
                "match_all": {}
            }
        },
        "dest": {
            "index": dest_idx,
            "op_type" : "create"
        }
    }
    
    response = dest_es.reindex(
        query,
        wait_for_completion=True, 
        request_timeout=300
    )
    '''
    
    query = {
        "track_total_hits" : True,
        "query": { 
            "match_all" : {}
        }
    }
    response = helpers.reindex(
                    client=src_es, 
                    target_client=dest_es,
                    source_index=src_idx, 
                    target_index=dest_idx, 
                    query=query,
                    chunk_size=int(batch_size), 
                    # op_type='_index',
                    scroll=scroll_time, 
                    # bulk_kwargs={
                    #     'wait_for_completion': True
                    # }
    )
    
    print(json.dumps(query, indent=2))
    print(json.dumps(response, indent=2))
    

def work_scroll_api(src_es, dest_es, src_idx, dest_idx):
    ''' 
    The best way to reindex is to use Elasticsearch's builtin Reindex API as it is well supported and resilient to known issues.
    The Elasticsaerch Reindex API uses scroll and bulk indexing in batches , and allows for scripted transformation of data. 
    In Python, a similar routine could be developed:
    '''
    
    # scroll_time='60s'
    scroll_time='1m'
    batch_size='1000'
    total_progressing = 0
    
    body = {
        "track_total_hits" : True,
        "query": { 
            "match_all" : {}
        }
    }

    def transform(hits):
        for h in hits:
            h['_index'] = dest_idx
            yield h

    rs = src_es.search(index=[src_idx],
        scroll=scroll_time,
        size=batch_size,
        body=body
    )

    # print(f'Current Size : {len(rs["hits"]["hits"])}')
    helpers.bulk(dest_es, transform(rs['hits']['hits']), chunk_size=batch_size)
    total_progressing += int(batch_size)
    print(f'Ingest data .. : {str(total_progressing)}')
    
    while True:
        # print(f'scroll : {rs["_scroll_id"]}')
        scroll_id = rs['_scroll_id']
        rs = src_es.scroll(scroll_id=scroll_id, scroll=scroll_time)
        if len(rs['hits']['hits']) > 0:
            success, failed = helpers.bulk(dest_es, transform(rs['hits']['hits']), chunk_size=batch_size, raise_on_error=True)
            total_progressing += success
            print(f'Ingest data .. : {str(total_progressing)}')
        else:
            break;
     
    '''
    curl -XPOST -u elastic:gsaadmin "http://localhost:9221/cp_test_omnisearch_v2/_search/?pretty" -H 'Content-Type: application/json' -d' {
        "track_total_hits" : true,
        "query": {
            "match_all": {
            }
        },
        "size" : 0
    }'
    
    '''    
    rs = dest_es.search(index=[dest_idx],
        body=body
    )

    print('-'*10)
    print(f'Validation Search Size : {rs["hits"]["total"]["value"]}')
    print('-'*10)


if __name__ == "__main__":
    '''
    python tools/elasticsearch/reindex_script.py
    python tools/elasticsearch/reindex_script.py --src_index=test_omnisearch_v2 --dest_index=cp_test_omnisearch_v2
    python tools/elasticsearch/reindex_script.py --src_index=.monitoring-es-7-2023.12.15 --dest_index=.monitoring-es-7-2023.12.15
    python tools/elasticsearch/reindex_script.py --type=reindex --src_index=test_omnisearch_v2 --dest_index=cp_test_omnisearch_v2
    '''
    parser = argparse.ArgumentParser(description="Reindex from old index to new index using _reindex_api")
    parser.add_argument('-t', '--type', dest='type', default="scroll", help='scroll,reindex')
    parser.add_argument('-s', '--src', dest='src', default="http://localhost:9209", help='source cluster')
    parser.add_argument('-d', '--des', dest='des', default="http://localhost:9203", help='dest cluster')
    parser.add_argument('-si', '--src_index', dest='src_index', default="test_omnisearch_v2", help='source index')
    parser.add_argument('-di', '--dest_index', dest='dest_index', default="cp_test_omnisearch_v2", help='dest index')
    args = parser.parse_args()
    
    try:
        
        if args.type:
            reindex_type = args.type
            
        if args.src:
            src_host = args.src
        
        if args.des:
            des_host = args.des
            
        if args.src_index:
            src_index = args.src_index
        
        if args.dest_index:
            des_index = args.dest_index
            
        StartTime, EndTime, Delay_Time = 0, 0, 0

        print(f'source es : {src_host}, dest es : {des_host}')
        print(f'source index : {src_index}, dest index : {des_index}')
        # exit()
        
        # --
        # Instance for the response time log
        src_es_host = get_es_instance(src_host)
        des_es_host = get_es_instance(des_host)
        # --
        
        StartTime = datetime.datetime.now()
        # --
        if reindex_type == 'scroll':
            work_scroll_api(src_es_host, des_es_host, src_index, des_index)
        elif reindex_type == 'reindex':
            work_reindex_api(src_es_host, des_es_host, src_index, des_index)
        # --
        EndTime = datetime.datetime.now()
    
    except Exception as e:
        print(e)
        
    finally:
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        print(f'Running Time : {Delay_Time}s')