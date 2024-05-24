from kafka import KafkaConsumer
from threading import Thread
import time
import logging
import sys
import queue
import argparse
import json
import jaydebeapi
import jpype
import datetime


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


Q = queue.Queue()  # limit concurrent threads to 2


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
    


# poetry add kafka-python
def work(topic, kafka_broker):
    try:
        # brokers = ['localhost:29092', 'localhost:39092']
        brokers = kafka_broker.split(",")
        # topic = 'test-topic'
        logging.info("'{} - {}".format(topic, brokers))

        # https://taptorestart.tistory.com/entry/Q-kafka%EC%97%90%EC%84%9C-groupid%EB%A5%BC-%EC%84%A4%EC%A0%95%ED%95%98%EB%A9%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%90%A0%EA%B9%8C
        # https://firststep-de.tistory.com/38
        
        consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

        for message in consumer:
            # logging.info(f'{message, message.value, message.value.decode("utf-8")}')
            logging.info(f'{message.value.decode("utf-8")}')
            Q.put(message.value.decode("utf-8"))
            logging.info("-- consumer checking..--")
        logging.info("-- job finished..--")
        
    except Exception as e:
            logging.info(e)
    
    
def thread_background(topic, brokers):
    while True:
        try:
            # print('create --', type(read_config_yaml()))
            logging.info('--thread_background--')
            work(topic, brokers)
        
        except Exception as e:
            logging.info(e)
            # pass
        time.sleep(1)  # TODO poll other things



def queue_background(database_object, db_run, master_tb, sql):
    '''
    database_object : Object for class
    Topic Queue
    '''

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


    while True:
        try:
            # print('create --', type(read_config_yaml()))
            consumer_json = Q.get()
             
            # -- Running 
            raw_json = json.loads(str(consumer_json).replace("'",'"'))
            print(f"\nQ receiving -- {raw_json}, type : {type(raw_json)}")

            if db_run:
                process_name = raw_json.get("PROCESSNAME")    
                # transform_str_json_to_get_keys(raw_json)
                json_vw_name = database_object.excute_oracle_query(master_tb.format(process_name))
            
                # - main sql
                result_json_value = database_object.excute_oracle_query(sql.format(json_vw_name, transform_str_json_to_get_keys(raw_json)))
                print('# Result_json_value -> ', result_json_value)
            else:
                transform_str_json_to_get_keys(raw_json)
            # -- 

        except Exception as e:
            print(e)
            # pass
        # time.sleep(1)  # TODO poll other things


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



if __name__ == "__main__":

    ''' 
    python ./db-kafka-consumer.py --topic users_tb_topic --brokers localhost:9092 --url jdbc:oracle:thin:test/1234@localhost:1234/test --sql "SELECT DBMS_LOB.SUBSTR(JSON_OBJECT, DBMS_LOB.GETLENGTH(JSON_OBJECT)) AS JSON_OBJECT FROM {} WHERE {}" --master_tb "SELECT JSON_SRC_VW FROM test WHERE PROCESS_NAME = '{}'"
    '''
    parser = argparse.ArgumentParser(description="Running Kafka-Consumer using this script")
    parser.add_argument('-e', '--topic', dest='topic', default="test", help='the name of topic')
    parser.add_argument('-i', '--brokers', dest='brokers', default="localhost:9092,localhost:9093", help='kafka brokers')
    parser.add_argument('-r', '--db_run', dest="db_run", default="False", help='If true, executable will run after compilation.')
    parser.add_argument('-u', '--url', dest='url', default="postgresql://postgres:1234@localhost:5432/postgres", help='db url')
    parser.add_argument('-s', '--sql', dest='sql', default="select * from test", help='sql')
    parser.add_argument('-m', '--master_tb', dest='master_tb', default="SELECT JSON_SRC_VW FROM test WHERE PROCESS_NAME = '{}'", help='master table')
    args = parser.parse_args()
    
    if args.topic:
        topic = args.topic
    
    if args.brokers:
        brokers = args.brokers

    if args.db_run:
        db_run = args.db_run

    if args.url:
        db_url = args.url

    if args.sql:
        sql = args.sql

    if args.master_tb:
        master_tb = args.master_tb

    # db_run = bool(str(db_run).upper())
    # print(db_run, type(db_run), bool(db_run))
    db_run = True if str(db_run).upper() == "TRUE" else False
    print(db_run, type(db_run))

    if db_run:
        database_object = oracle_database(db_url)
    else:
        database_object = None

    try:
        T = []
        
        th1 = Thread(target=queue_background, args=(database_object, db_run, master_tb, sql,))
        th1.daemon = True
        th1.start()
        T.append(th1)
        
        #for topic in ['users_tb_topic']:
        for topic in [topic]:
            # Create thread as background
            th2 = Thread(target=thread_background, args=(topic, brokers))
            th2.daemon = True
            th2.start()
            T.append(th2)
        
        # wait for all threads to terminate
        for t in T:
            while t.is_alive():
                t.join(0.5)

    except (KeyboardInterrupt, SystemExit):
        print('# Interrupted')
        # sys.exit(0) 

    finally:
        if db_run:
            database_object.set_db_disconnection()
            database_object.set_init_JVM_shutdown()
        
           
    