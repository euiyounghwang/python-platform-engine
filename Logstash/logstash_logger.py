
import sys

import socket
import json
from datetime import datetime


class TCP_SOCKET:
    """
    TCP SOCKET with Logstsh
    """
    def __init__(self, ip, port):
        self.target_server_ip = ip
        self.socket_port = port
        self.TCPClientSocket = None


    def Connect(self):
        self.TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPClientSocket.connect((self.target_server_ip, self.socket_port))


    def socket_logstash_handler(self, message):
        """

        :param message:
        :return:
        """
        # print("Socket Message Send..." + str(message))
        # message = '{"create_date" : "SNTC2020021821575900000004", "request_server_ip" : "127.0.0.1", "system_id":"law", "company_code" : "30"}'
        # message = '{create_date : SNTC2020021821575900000004, request_server_ip : 127.0.0.1, key : doc0900bf4b9ef20165, company_code : 30, system_id : law, login_id : euiyoung.hwang, Sentence : 배가스 조건 및 조성 . Parameters 포 항. 75MW 100MW. Gas Flow Nhr wet 345000 588000. Temperature 3, Predict : __label__pos, Percent: 0.999}'
        self.TCPClientSocket.send(json.dumps(message, ensure_ascii=False).encode())

    def Close(self):
        self.TCPClientSocket.close()
        # log.info('Socket Closed')
        # print('Socket Closed')



class UDP_SOCKET:
    """
    UDP SOCKET with Logstsh
    """

    def __init__(self, ip, port):
        self.target_server_ip = ip
        self.socket_port = port
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def socket_logstash_handler(self, message):
        # print('@@socket_logstash_handler@@', message)
        self.UDPClientSocket.sendto(json.dumps(message, ensure_ascii=False).encode("utf8"), (self.target_server_ip, self.socket_port))

       

if __name__ == '__main__':

    SOCKET_SERVER_IP = "127.0.0.1"
    
    # Monitoring
    log_sample_data = {
        "LOG_LEVEL": "INFO",
        "LOG_TEXT" : "MODEL_UPGRADE",
        "STATUS" : 200
    }
    
    # try:
    #     TCP_SOC = TCP_SOCKET(SOCKET_SERVER_IP, 5958)
    #     TCP_SOC.Connect()
        
    #     for _ in range(4):
    #         TCP_SOC.socket_logstash_handler(log_sample_data)
    # except Exception as e:
    #     print(e)
        
    # finally:
    #     TCP_SOC.Close()
        
    
    try:
        UDP_SOC = UDP_SOCKET(SOCKET_SERVER_IP, 5959)
        for _ in range(4):
            UDP_SOC.socket_logstash_handler(log_sample_data)
    except Exception as e:
        print(e)

    