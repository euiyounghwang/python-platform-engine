
# RabbitMQ
RabbitMQ-Repository

<i>RabbitMQ is an open-source message-broker software (sometimes called message-oriented middleware) that originally implemented the Advanced Message Queuing Protocol (AMQP) and has since been extended with a plug-in architecture to support Streaming Text Oriented Messaging Protocol (STOMP), MQ Telemetry Transport (MQTT), and other protocols.[1]


#### Using Python Virtual Environment
```bash
..         
➜(.venv) ➜  python-platform-engine git:(master) source ./RabbitMQ/create_virtual_env.sh 
VirtualEnv exists.
Created virtual enviroment >> + /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/RabbitMQ/.venv/bin/activate
Install requirements.txt
Requirement already satisfied: pip in ./RabbitMQ/.venv/lib/python3.9/site-packages (21.2.3)
Collecting pip
  Using cached pip-24.0-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.3
    Uninstalling pip-21.2.3:
      Successfully uninstalled pip-21.2.3
Successfully installed pip-24.0
Collecting kafka-python==2.0.2 (from -r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/RabbitMQ/requirements.txt (line 1))
  Using cached kafka_python-2.0.2-py2.py3-none-any.whl (246 kB)
Collecting pika==1.3.2 (from -r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/RabbitMQ/requirements.txt (line 2))
  Using cached pika-1.3.2-py3-none-any.whl (155 kB)
Collecting python-dotenv==0.20.0 (from -r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/RabbitMQ/requirements.txt (line 3))
  Using cached python_dotenv-0.20.0-py3-none-any.whl (17 kB)
Installing collected packages: kafka-python, python-dotenv, pika
Successfully installed kafka-python-2.0.2 pika-1.3.2 python-dotenv-0.20.0
Install Completely..
..
```
