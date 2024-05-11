# pip install psycopg2-binary

import psycopg2
import jaydebeapi
import jpype
import os, sys
import pandas.io.sql as pd_sql
import pandas as pd
from pandas import DataFrame
from urllib.parse import urlparse
import argparse
import json
import datetime

"""
JayDeBeApi      1.2.3
JPype1          1.5.0
kafka-python    2.0.2
packaging       24.0
pip             20.2.3
psycopg2-binary 2.9.9
setuptools      49.2.1
"""

# (.venv) [devuser@localhost db_test]$ pwd
# /home/devuser/Git_Repo/db_test
# (.venv) [devuser@localhost db_test]$ python ./test_db_connection.py
# ('euiyoung', 'ehwang', 11, None)
# (.venv) [devuser@localhost db_test]$

def postgres(connection_str, sql):
    '''
    import psycopg2-binary
    '''
    try:
        p = urlparse(connection_str)
        # print(p.hostname)

        pg_connection_dict = {
            'dbname': p.path[1:],
            'user': p.username,
            'password': p.password,
            'port': p.port,
            'host': p.hostname
        }

        print('pg_connection_dict - ', pg_connection_dict)
        conn = psycopg2.connect(**pg_connection_dict)

        # conn = psycopg2.connect(dbname="postgres",
        #                         user="postgres",
        #                         host="172.25.224.1",
        #                         password="1234",
        #                         port="5432")

        if conn:
            print("Connected to Oracle database successfully!")
        else:
            print("Failed to connect to Oracle database.")

        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print('record - ', row)
            break

    except Exception as e:
        print(e)
        pass

    conn.close()
    print("Disconnected to Oracle database successfully!")



class oracle_database:

    def __init__(self, db_url) -> None:
        self.db_url = db_url
        self.set_db_connection()
        

    def set_init_JVM(self):
        '''
        Init JPYPE StartJVM
        '''

        if jpype.isJVMStarted():
            return
    
        jar = r'./ojdbc8.jar'
        args = '-Djava.class.path=%s' % jar

        # print('Python Version : ', sys.version)
        # print('JAVA_HOME : ', os.environ["JAVA_HOME"])
        # print('JDBC_Driver Path : ', JDBC_Driver)
        # print('Jpype Default JVM Path : ', jpype.getDefaultJVMPath())

        # jpype.startJVM("-Djava.class.path={}".format(JDBC_Driver))
        jpype.startJVM(jpype.getDefaultJVMPath(), args, '-Xrs')


    def set_init_JVM_shutdown(self):
        jpype.shutdownJVM() 
   

    def set_db_connection(self):
        ''' DB Connect '''
        print('connect-str : ', self.db_url)
        
        StartTime = datetime.datetime.now()

        # -- Init JVM
        self.set_init_JVM()
        # --
        
        # - DB Connection
        self.db_conn = jaydebeapi.connect("oracle.jdbc.driver.OracleDriver", self.db_url)
        # --
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        print("# DB Connection Running Time - {}".format(str(Delay_Time)))

    
    def set_db_disconnection(self):
        ''' DB Disconnect '''
        self.db_conn.close()
        print("Disconnected to Oracle database successfully!") 

    
    def get_db_connection(self):
        return self.db_conn
    

    def excute_oracle_query(self, sql):
        '''
        DB Oracle : Excute Query
        '''
        print('excute_oracle_query -> ', sql)
        # Creating a cursor object
        cursor = self.get_db_connection().cursor()

        # Executing a query
        cursor.execute(sql)
        
        # Fetching the results
        results = cursor.fetchall()
        cols = list(zip(*cursor.description))[0]
        # print(type(results), cols)

        target_value = ''
        for row in results:
            # print(type(row), row)
            target_value = row[0]
            # print('target -', row[0])

        cursor.close()
        
        return target_value
    

def oracle(db_url, sql, master_tb, json_data):
    ''' main process '''
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


    def transform_str_json_to_get_keys(raw_json):
        '''
        {'test': 'test|1', 'KEY1_NAME': 'id', 'KEY1_VALUE': '1', 'KEY2_NAME': None, 'KEY2_VALUE': None, 'KEY3_NAME': None, 'KEY3_VALUE': None} -> ID,1 for set_WHERE_clauses
        '''
        concat_get_keys = []
        for k, v in raw_json.items():
            if str(k).upper().startswith("KEY"):
                if v is not None:
                    # concat_get_keys.append(str(k))
                    concat_get_keys.append(str(v).upper())

        print("# Transform_str_json_to_get_keys - {}".format(','.join(concat_get_keys)))
        return set_WHERE_clauses(','.join(concat_get_keys))

    database_object = oracle_database(db_url)

    try:

        """
        # pd_sql.execute(sql, conn)
        # df = pd_sql.read_sql(sql, conn, index_col = None)
        # print(df.head())
        # df_all = pd_sql.read_sql_query(sql, conn, params=None)
        df_all = pd.read_sql(sql, conn, params=None)
        print('df_all.size = {}'.format(df_all.shape))
        # print(df_all.keys(), len(df_all.keys()))
        print(df_all)

        # for loop in range(0, len(df_all._get_values)):
        #     for column in df_all.keys():
        #         print(loop, column, df_all.get(column)[loop])
        """
        # https://tech.sadaalomma.com/python/python-connect-to-sql-server-using-jdbc/

        StartTime = datetime.datetime.now()
        # -- Running 
        raw_json = json.loads(str(json_data).replace("'",'"'))
        process_name = raw_json.get("PROCESSNAME")
                              
        json_vw_name = database_object.excute_oracle_query(master_tb.format(process_name))

        # - main sql
        result_json_value = database_object.excute_oracle_query(sql.format(json_vw_name, transform_str_json_to_get_keys(raw_json)))
        print('# Result_json_value -> ', result_json_value)

        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        print("# DB Query Running Time - {}".format(str(Delay_Time)))

        # df = pd.DataFrame(results, columns=tuple(zip(*cursor.description))[0])
        # print(df.head())

    except Exception as e:
        print(e)
        pass

    database_object.set_db_disconnection()
    database_object.set_init_JVM_shutdown()



if __name__ == "__main__":
    ''' 
    python ./test_db_connection.py --db postgres --url postgresql://postgres:1234@localhost:5432/postgres --sql "SELECT * FROM postgres.user"
    python ./test_db_connection.py --db oracle --url jdbc:oracle:thin:test/test@localhost:12343/test --sql "SELECT * FROM SELECT DBMS_LOB.SUBSTR(JSON_OBJECT, DBMS_LOB.GETLENGTH(JSON_OBJECT)) * FROM test" --json_data "{'test': 'test|1', 'KEY1_NAME': 'id', 'KEY1_VALUE': '1'}" --master_tb "SELECT JSON_SRC_VW FROM test WHERE PROCESS_NAME = '{}'"
    '''
    parser = argparse.ArgumentParser(description="Running db test script")
    parser.add_argument('-d', '--db', dest='db', default="postgres", help='choose one of db')
    parser.add_argument('-u', '--url', dest='url', default="postgresql://postgres:1234@localhost:5432/postgres", help='db url')
    parser.add_argument('-s', '--sql', dest='sql', default="jdbc:oracle:thin:test/test@localhost:12343/test", help='sql')
    parser.add_argument('-m', '--master_tb', dest='master_tb', default="SELECT JSON_SRC_VW FROM test WHERE PROCESS_NAME = '{}'", help='master table')
    parser.add_argument('-k', '--json_data', dest='json_data', default="{'test': 'test|1', 'KEY1_NAME': 'id', 'KEY1_VALUE': '1', 'KEY2_NAME': None, 'KEY2_VALUE': None, 'KEY3_NAME': None, 'KEY3_VALUE': None}", help='json data from Kafka connect')
    args = parser.parse_args()
    
    if args.db:
        db = args.db

    if args.url:
        db_url = args.url
    
    if args.sql:
        sql = args.sql

    if args.master_tb:
        master_tb = args.master_tb

    if args.json_data:
        json_data = args.json_data

    if db == 'postgres':
        postgres(db_url, sql)

    elif db == 'oracle':
        # -- db_url, sql, processname, key-pairs for WHERE Clause
        oracle(db_url, sql, master_tb, json_data)

        