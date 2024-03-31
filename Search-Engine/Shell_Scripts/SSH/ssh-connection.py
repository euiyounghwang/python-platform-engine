
import paramiko
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# server_file = "C://Users//euiyoung.hwang/server"
server_file = "C://Users//euiyoung.hwang/server_test"

credentials_file = "C://Users//euiyoung.hwang/ssh_credentials"

failed_server_list = []

def read_server():
    server_list = []
    with open(server_file) as data_file:
        for line in data_file:
            line = line.strip()
            # logging.info(f"{line}")
            server_list.append(line)
    return server_list


def read_credentials():
    credentials = []
    with open(credentials_file) as data_file:
        for line in data_file:
            line = line.strip().split(' ')
            # print("test", line)
            # logging.info(f"{line}")
            credentials.extend(line)
                
    credentials = [item for item in credentials if len(item) > 0]
    return credentials


def ssh_connection_test(host, username, password):
    try:
        # command = "df"

        # Update the next three lines with your
        # server's information

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        # _stdin, _stdout,_stderr = client.exec_command("df")
        # print(_stdout.read().decode())
        logging.info(f"Success : {host}")
    except Exception as error:
        # logging.error(f"Failed : {host}")
        print(f"Failed : {host}")
        failed_server_list.append(host)
    finally:
        client.close()


if __name__ == "__main__":
    server_list = read_server()
    credential = read_credentials()
    # logging.info(server_list)
    # print(server_list)
    # print(credential)

    for idx, each_server in enumerate(server_list):
        logging.info(f"{idx+1} : {each_server}")
        ssh_connection_test(str(each_server).strip(), credential[0], credential[1])
    
    logging.info("\n")
    logging.info(f"Failed server list (Total Count: {len(failed_server_list)}): {failed_server_list}")
    logging.info("\n")
