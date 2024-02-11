# from fabric.api import run,env,execute,task
from fabric.api import *
from fabric.operations import local,put
import os
import json
from contextlib import contextmanager as _contextmanager

# https://blog.ppuing.me/13

# Install Fabric into client enviroment
# conda create --yes --quiet --name fn_devops python=3.6
# conda activate fn_devops
# pip install fabric3

# sudo apt install python3.10-venv
# sudo apt-get install python3-pip
# python3 -m venv .venv
# source .venv/bin/activate
#  git clone git@github.com:euiyounghwang/python-flask-connexion-example-openapi3-master.git


# fab dev

env.roledefs = {
    'dev': ['devuser@192.168.64.2',],
    'staging' : ['devuser@192.168.64.3',],
    'prod' : ['devuser@192.168.64.2',],
}

'''
https://blog.naver.com/PostView.nhn?blogId=special9486&logNo=220289095822
ssh-keygen -t rsa
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
 
ssh-copy-id -i ./id_rsa.pub devuser@192.168.64.2
-- GitHub
pbcopy < ~/.ssh/id_rsa.pub OR cat ~/.ssh/id_rsa.pub | pbcopy
'''
# env.password = 'posco123'
env.keyfile = ['$HOME/.ssh/id_rsa']
env.directory = '/home/devuser/project/python-flask-connexion-example-openapi3-master'
env.activate = 'source .venv/bin/activate'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_settings(mode=None, services=None):
    ''' Loading env-setting.json to get all variables '''
    try:
        with open(os.path.join(PROJECT_DIR, "{}-settings.json".format(mode))) as f:
            envs = json.loads(f.read())
            print("Loading.. ", envs)
            if services not in envs.keys():
                print( "There isn't keys {} in the settings.json".format(services))
                return None
            print(envs[services]['REPO_URL'])
            return envs[services]
    except Exception as ex:
        print("Error ", ex)


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

@roles('dev')
def dev(user=None, services=None):
    envs = setup_settings(mode='dev', services=services)
    if envs is not None:
        deploy(mode="dev", user=user)


@roles('staging')
def staging(user=None, services=None):
    # deploy(mode="staging", user=user)
    run('uname -a')

@roles('prod')
def prod(user=None):
    deploy(mode="prod", user=user)


def deploy(mode="release", user=None):
    print("Deploying : {} from user : {}".format(mode, user))
    with virtualenv():
        run("git pull")
        # run("./service_start.sh")

def hostname():
        run('uname -a')

def ls():
        run('ls')

'''
Command : 
- fab dev:user="euiyoung.hwang",services="update_rest_service"
- fab staging:user="euiyoung.hwang",services="update_rest_service"
'''

