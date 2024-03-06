
#!/bin/bash
set -e

minikube start
minikube dashboard

echo "build a docker image in our local machine and then deploy them to the minikube environment."
eval $(minikube docker-env)

echo "Running service in minikube cluser"
minikube service fastapi-basic --url