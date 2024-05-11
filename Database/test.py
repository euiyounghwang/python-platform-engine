

import json


def set_WHERE_clauses(key_list):
    '''
    key_list : a,b -> A = 'B' -> WHERE A = 'B'
    key_list : a,b,c,d -> A = 'B' AND C = 'D' --> WHERE A = 'B' AND C = 'D'
    '''
    key_list = key_list.split(",")
    clauses = []
    for i in range(0, len(key_list), 2):
        # print(key_list[i], key_list[i+1])
        clauses.append("{} = '{}'".format(str(key_list[i]).upper(), str(key_list[i+1]).upper()))
    WHERE = " AND " .join(clauses)
    print("# WHERE -> ", WHERE)

    return WHERE


def transform_str_json_to_get_keys(consumer_json):
    transform = json.loads(consumer_json)
    print(transform)
    # print(json.loads(transform))
    concat_get_keys = []
    for k, v in transform.items():
        if str(k).upper().startswith("KEY"):
            if v is not None:
                # concat_get_keys.append(str(k))
                concat_get_keys.append(str(v).upper())

    print(','.join(concat_get_keys))
    print(set_WHERE_clauses(','.join(concat_get_keys)))
    return ','.join(concat_get_keys)


# transform_str_json_to_get_keys('{"test":"test|1","KEY1_NAME":"id","KEY1_VALUE":"1","KEY2_NAME":null,"KEY2_VALUE":null,"KEY3_NAME":null,"KEY3_VALUE":null}')
transform_str_json_to_get_keys('{"test":"test|1","KEY1_NAME":"id","KEY1_VALUE":"1","KEY2_NAME":"test_a","KEY2_VALUE":1,"KEY3_NAME":"test_b","KEY3_VALUE":"b"}')