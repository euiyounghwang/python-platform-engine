
from typing import *

import requests
import json
from datetime import datetime, timedelta


# 오늘 날짜부터 days 전 까지 index_name-yyMMdd 형태의 샘플 데이터 생성
# ex) test-200126
def index_sample_data(index_name: str, days: int) -> None:
    data = []
    for d in range(days):
        yymmdd = (datetime.now() - timedelta(days=d)).strftime('%y%m%d')
        data.append(json.dumps({'index': {'_index': '{}-{}'.format(index_name, yymmdd)}}))
        data.append(json.dumps({'@timestamp': str(datetime.now())}))
    response = requests.post(
        url='http://localhost:9209/_bulk',
        headers={'Content-Type': 'application/json', 'Authorization':'Basic ZWxhc3RpYzpnc2FhZG1pbg==',},
        data='\n'.join(data) + '\n'
    )
    print(f"response code : {response.status_code}, results : {json.dumps(response.json(), indent=2)}")


if __name__ == '__main__':
    index_sample_data(index_name='curator_manual_create_1', days=15)
    index_sample_data(index_name='curator_manual_create_2', days=15)
