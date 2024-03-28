
import paramiko
import logging

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

server_file = "./server"
# server_file = "./server_test"

failed_server_list = []

def read_server():
    server_list = []
    with open(server_file) as data_file:
        for line in data_file:
            line = line.strip()
            # logging.info(f"{line}")
            server_list.append(line)
    return server_list


def ssh_connection_test(host):
    try:
        # command = "df"

        # Update the next three lines with your
        # server's information

      

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        # _stdin, _stdout,_stderr = client.exec_command("df")
        # print(_stdout.read().decode())
        # logging.info(f"Success : {host}")
        print(f"Success : {host}")
    except Exception as error:
        # logging.error(f"Failed : {host}")
        print(f"Failed : {host}")
        failed_server_list.append(host)
    finally:
        client.close()


if __name__ == "__main__":
    server_list = read_server()
    # logging.info(server_list)

    for idx, each_server in enumerate(server_list):
        # logging.info(f"{idx+1} : {each_server}")
        print(f"{idx+1} : {each_server}")
        ssh_connection_test(str(each_server).strip())

    # logging.info("\n")
    # logging.info(f"Failed server list : {failed_server_list}")
    # logging.info("\n")
    
    print("\n")
    print(f"Failed server list (Total Count: {len(failed_server_list)}): {failed_server_list}")
    print("\n")