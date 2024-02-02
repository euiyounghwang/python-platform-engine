import os
import requests
import time
from prometheus_client import start_http_server, Enum, Histogram
from dotenv import load_dotenv


load_dotenv()

hitl_psql_health_status = Enum("hitl_elasticsearch_health_status", "Elasticsearch connection health", states=["healthy", "unhealthy"])
hitl_psql_health_request_time = Histogram('hitl_elasticsearch_health_request_time', 'local Elasticsearch connection response time (seconds)')

def get_metrics():

    with hitl_psql_health_request_time.time():
        resp = requests.get(url=os.getenv('URL', 'http://localhost:8888/es/health'))
    
    # print(resp.status_code)
            
    if not (resp.status_code == 200):
        hitl_psql_health_status.state("unhealthy")
            
if __name__ == '__main__':
    start_http_server(9000)
    while True:
        get_metrics()
        time.sleep(1)