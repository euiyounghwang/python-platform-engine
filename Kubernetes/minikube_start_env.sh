
#!/bin/bash
set -e

eval $(minikube docker-env)
minikube start
minikube dashboard
