# DevOps-Deploy

<i>Fabric(https://www.fabfile.org/) is a high level Python (2.7, 3.4+) library designed to execute shell commands remotely over SSH, yielding useful Python objects in return. 
- It builds on top of Invoke (subprocess command execution and command-line features) and Paramiko (SSH protocol implementation), extending their APIs to complement one another and provide additional functionality.


#### Using Python Virtual Environment
```bash
..     
conda create --yes --quiet --name fn_devops python=3.6
conda activate fn_devops

OR

..         
➜  python-platform-engine git:(master) source ./Fabric/create_virtual_env.sh 
VirtualEnv exists.
Created virtual enviroment >> + /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/.venv/bin/activate
Install requirements.txt
Requirement already satisfied: pip in ./Fabric/.venv/lib/python3.9/site-packages (21.2.3)
Collecting pip
  Using cached pip-24.0-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.3
    Uninstalling pip-21.2.3:
      Successfully uninstalled pip-21.2.3
Successfully installed pip-24.0
Collecting Fabric3==1.14.post1 (from -r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached Fabric3-1.14.post1-py3-none-any.whl (92 kB)
Collecting paramiko<3.0,>=2.0 (from Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached paramiko-2.12.0-py2.py3-none-any.whl (213 kB)
Collecting six>=1.10.0 (from Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting bcrypt>=3.1.3 (from paramiko<3.0,>=2.0->Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached bcrypt-4.1.2-cp39-abi3-macosx_10_12_universal2.whl.metadata (9.5 kB)
Collecting cryptography>=2.5 (from paramiko<3.0,>=2.0->Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached cryptography-42.0.2-cp39-abi3-macosx_10_12_universal2.whl.metadata (5.3 kB)
Collecting pynacl>=1.0.1 (from paramiko<3.0,>=2.0->Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached PyNaCl-1.5.0-cp36-abi3-macosx_10_10_universal2.whl (349 kB)
Collecting cffi>=1.12 (from cryptography>=2.5->paramiko<3.0,>=2.0->Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached cffi-1.16.0-cp39-cp39-macosx_10_9_x86_64.whl.metadata (1.5 kB)
Collecting pycparser (from cffi>=1.12->cryptography>=2.5->paramiko<3.0,>=2.0->Fabric3==1.14.post1->-r /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Fabric/requirements.txt (line 1))
  Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
Using cached bcrypt-4.1.2-cp39-abi3-macosx_10_12_universal2.whl (528 kB)
Using cached cryptography-42.0.2-cp39-abi3-macosx_10_12_universal2.whl (5.9 MB)
Using cached cffi-1.16.0-cp39-cp39-macosx_10_9_x86_64.whl (182 kB)
Installing collected packages: six, pycparser, bcrypt, cffi, pynacl, cryptography, paramiko, Fabric3
Successfully installed Fabric3-1.14.post1 bcrypt-4.1.2 cffi-1.16.0 cryptography-42.0.2 paramiko-2.12.0 pycparser-2.21 pynacl-1.5.0 six-1.16.0
Install Completely..
..
```


#### Run the script via Fabric
```bash
- fab dev:user="euiyoung.hwang",services="update_rest_service"
- fab staging:user="euiyoung.hwang",services="update_rest_service"
```