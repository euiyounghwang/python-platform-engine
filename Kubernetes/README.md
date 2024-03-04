
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

