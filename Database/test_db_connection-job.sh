#!/bin/bash
set -e


python ./test_db_connection.py --db postgres --url postgresql://postgres:1234@localhost:5432/postgres --sql "SELECT * FROM postgres.user"
#python ./test_db_connection.py --db oracle --url jdbc:oracle:thin:test/test@localhost:12343/test --sql "SELECT * FROM SELECT DBMS_LOB.SUBSTR(JSON_OBJECT, DBMS_LOB.GETLENGTH(JSON_OBJECT)) * FROM test" --json_data "{'test': 'test|1', 'KEY1_NAME': 'id', 'KEY1_VALUE': '1', 'KEY2_NAME': None, 'KEY2_VALUE': None, 'KEY3_NAME': None, 'KEY3_VALUE': None}"
