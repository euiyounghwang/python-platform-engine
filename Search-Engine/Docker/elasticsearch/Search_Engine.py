
from elasticsearch import Elasticsearch
import json
import os
from datetime import datetime
import pandas as pd
import re


class Search():
    ''' elasticsearch class '''
    
    def __init__(self, host):
        self.timeout = 60
        self.MAX_BYTES = 1048576
        
        # self.es_client = Elasticsearch(hosts=host, headers=self.get_headers(), timeout=self.timeout)
        # create a new instance of the Elasticsearch client class
        # Elasticseach < 8.x basic auth example:
        self.es_client = Elasticsearch(hosts=host, headers=self.get_headers(), http_auth=('elastic','gsaadmin'), timeout=self.timeout)
        
        # Elasticsearch >= 8.x
        # self.es_client = Elasticsearch(hosts=_host, headers=self.get_headers(), basic_auth=('elastic','gsaadmin'), timeout=self.timeout)
    
    
    def close(self):
        self.es_client.close()
        
    
    def get_headers(self):
        ''' Elasticsearch Header '''
        return {
            'Content-type': 'application/json', 
            'Connection': 'close'
        }
        
    
    def Get_Buffer_Length(self, docs):
        """
        :param docs:
        :return:
        """
        max_len = 0
        for doc in docs:
            max_len += len(str(doc))

        return max_len
    
        
    def create_index(self, _index):
        ''' sample index & mapping '''
        print(self.es_client)
        
        mapping = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
        }
        
        def try_delete_create_index(index):
            try:
                if self.es_client.indices.exists(index):
                    print('Successfully deleted: {}'.format(index))
                    self.es_client.indices.delete(index)
                    # now create a new index
                    self.es_client.indices.create(index=_index, body=mapping)
                    # es_client.indices.put_alias(index, "omnisearch_search")
                    self.es_client.indices.refresh(index=_index)
                    print("Successfully created: {}".format(_index))
            
            except NotFoundError:
                pass
            
        ''' delete and create index into ES '''
        try_delete_create_index(index=_index)
        
    
    def post_search(self, _index):
        ''' search after indexing as validate '''
        response = self.es_client.search(
            index=_index,
            body={
                    "query" : {
                       "match_all" : {
                       }
                    }
            }
        )
        print("Total counts for search - {}".format(json.dumps(response['hits']['total']['value'], indent=2)))
        # print("response for search - {}".format(json.dumps(response['hits']['hits'][0], indent=2)))
    
    
    def transform_df_to_clean_characters(self, df):
        ''' Clean dataframe '''
        df = df.fillna('')
        return df
    
    
    def transform_json_clean_characters(self, to_replace):
        ''' Clean dataframe '''
        if isinstance(to_replace, (str)):
            to_replace = to_replace.strip()
            to_replace = re.sub(r'\n|\\n', ' ', to_replace)
            to_replace = re.sub(r'\t|\\t', ' ', to_replace)
            to_replace = re.sub(r'\f|\\f', ' ', to_replace)
            to_replace = re.sub(r'\s+', ' ', to_replace)
            to_replace = re.sub(r'string', '', to_replace)
            to_replace = re.sub(r'_id', '', 'key')
        
        return to_replace
        

    def buffered_json_to_es(self, df, _index):
        ''' df : Dataframe format, _index: Elasticsearch index name that you want to save '''
        print("buffered_json_to_es Loading..")
        ''' Nan to black for each field value '''
        
        try:
            df = self.transform_df_to_clean_characters(df)
            actions = []
        
            # creating a list of dataframe columns 
            columns = list(df) 
            print(columns)
            for row in list(df.values.tolist()):
                rows_dict = {}
                for i, colmun_name in enumerate(columns):
                    rows_dict.update({self.transform_json_clean_characters(colmun_name) : self.transform_json_clean_characters(row[i])})
                # print(rows_dict)
                actions.append({'index': {'_index': _index}})
                actions.append(rows_dict)
                # print(json.dumps(actions, indent=2))
                if self.Get_Buffer_Length(actions) > self.MAX_BYTES:
                    response = self.es_client.bulk(body=actions)
                    print("** indexing Error - True/False ** : {}".format(json.dumps(response['errors'], indent=2)))
                    del actions[:]
            
            # --
            # Index for the remain Dataset
            # --
            response = self.es_client.bulk(body=actions)
            # print(response)
            print("** Remain indexing Error - True/False ** : {}".format(json.dumps(response['errors'], indent=2)))
            
            # --
            # refresh
            self.es_client.indices.refresh(index=_index)
        
        except Exception as e:
            print('buffered_json_to_es exception : {}'.format(str(e)))