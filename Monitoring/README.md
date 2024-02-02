
Prometheus has many ready-to-use exporters, but sometimes you may need to collect your own metrics.

For this, Prometheus provides client libraries that we can use to generate metrics with the necessary labels.

Such an exporter can be included directly in the code of your application, or it can be run as a separate service that will poll one of your services and receive data from it, which will then be converted into the Prometheus format and sent to the Prometheus server.

- Using Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate

Or

➜  python-platform-engine git:(master) ✗ source ./Monitoring/create_virtual_env.sh
VirtualEnv exists.
Created virtual enviroment >> + /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Monitoring/.venv/bin/activate
Install requirements.txt
Requirement already satisfied: pip in ./Monitoring/.venv/lib/python3.9/site-packages (21.2.3)
Collecting pip
  Using cached pip-23.3.2-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.3
    Uninstalling pip-21.2.3:
      Successfully uninstalled pip-21.2.3
Successfully installed pip-23.3.2
Collecting prometheus-client==0.19.0 (from -r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Monitoring/requirements.txt (line 1))
  Using cached prometheus_client-0.19.0-py3-none-any.whl.metadata (1.8 kB)
Using cached prometheus_client-0.19.0-py3-none-any.whl (54 kB)
Installing collected packages: prometheus-client
Successfully installed prometheus-client-0.19.0
Install Completely..
```

- Install the dependency
```bash
$ pip install prometheus_client
```
