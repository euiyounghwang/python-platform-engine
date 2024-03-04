
# Kubernetes

- <i>__Minikube__ : `minikube` is local Kubernetes, focusing on making it easy to learn and develop for Kubernetes. All you need is Docker (or similarly compatible) container or a Virtual Machine environment, and Kubernetes is a single command away: `minikube start` (<i>https://minikube.sigs.k8s.io/docs/start/</i>)

    - To install the latest minikube stable release on x86-64 macOS using binary download:
    ```bash
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
    sudo install minikube-darwin-amd64 /usr/local/bin/minikube
    ```
    - Start your cluster
    ```bash
    minikube start
    ```
    - Interact with your cluster
    If you already have kubectl installed (see documentation), you can now use it to access your shiny new cluster:
    ```bash
    kubectl get po -A
    ```
    Alternatively, minikube can download the appropriate version of kubectl and you should be able to use it like this:
    ```bash 
    minikube kubectl -- get po -A
    ```
    You can also make your life easier by adding the following to your shell config: (for more details see: kubectl)
    ```bash 
    alias kubectl="minikube kubectl --"
    ```
    - Deploy applications : Create a sample deployment and expose it on port 8080:
    ```bash 
    kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
    kubectl expose deployment hello-minikube --type=NodePort --port=8080
    ```
    It may take a moment, but your deployment will soon show up when you run:
    ```bash 
    kubectl get services hello-minikube
    ```
    The easiest way to access this service is to let minikube launch a web browser for you:
    ```bash 
    minikube service hello-minikube
    ```
    Alternatively, use kubectl to forward the port:
    ```bash 
    kubectl port-forward service/hello-minikube 7080:8080
    ```
    

