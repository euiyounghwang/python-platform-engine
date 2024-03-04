# python-k8s
python-k8s


# k9s for mac
```bash
brew install k9s
```

# Install kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
```


# k9s for linux
```bash
curl -s -L https://github.com/derailed/k9s/releases/download/v0.26.7/k9s_Linux_x8
6_64.tar.gz -o k9s && tar -xvf k9s && chmod 755 k9s && rm LICENSE README.md  && sudo mv k9s /usr/local/bin
```

```bash
# ------------
# Docker image search
docker images fn-flask-api
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
fn-flask-api   test      a74a9b4858df   9 minutes ago    903MB
fn-flask-api   es        8bb326845134   10 minutes ago   907M
# ------------

# https://mydailylogs.tistory.com/120
kubectl cluster-info
kubectl get nodes

# ------------
# k8s dashboard setup
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.4.0/aio/deploy/recommended.yaml

kubectl get deployment -n kubernetes-dashboard
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
dashboard-metrics-scraper   1/1     1            1           44s
kubernetes-dashboard        1/1     1            1           45s

# Run
kubectl proxy
Starting to serve on 127.0.0.1:8001

# Dashboard
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login

# k8s instance connect
#kubectl exec -it -n <namespace> <pod_name> -- /bin/bash
kubectl exec -it -n dev fn-omnisearch-backend-69c8ddfbc5-j5vjk -- bash
kubectl exec -it -n dev fn-omnisearch-backend-69c8ddfbc5-j5vjk -- /bin/bash

# Test
kubectl --namespace=kube-system get pods
# ------------
```


#### Minikube Install for mac m1
```bash
https://minikube.sigs.k8s.io/docs/start/
https://medium.com/@seohee.sophie.kwon/how-to-run-a-minikube-on-apple-silicon-m1-8373c248d669

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube

minikube start --driver=docker --alsologtostderr

# Create minikube  instance on Docker Desktop
kubectl get deployments
kubectl delete deployment k8s-fn-flaks-api

eval $(minikube -p minikube docker-env)
minikube start
docker images

docker build -t euiyoung/fn-flask-api:es .
docker push euiyoung/fn-flask-api:es

#eval $(minikube -p minikube docker-env)
docker build -t fn-flaks-api:es .
#kubectl run k8s-fn-flask-api --image=fn-flask-api:es
kubectl create deployment k8s-fn-rest-api --image=euiyoung/fn-flask-api:es
➜  ~ deployment.apps/k8s-fn-flaks-api created
kubectl get pods
➜  ~ NAME                                READY   STATUS             RESTARTS      AGE
➜  ~ k8s-fn-flaks-api-996459675-flvx6    0/1     Completed          2 (25s ago)   39s
➜  ~ k8s-fn-flask-api                    0/1     ImagePullBackOff   0             16m
➜  ~ k8s-fn-flask-api-66cfc9d787-tbmdc   0/1     ImagePullBackOff   0             7m1s
kubectl expose pod "k8s-fn-flaks-api-996459675-flvx6" --type=NodePort --port=7091
➜  ~ service/k8s-fn-flaks-api-996459675-flvx6 exposed
minikube service k8s-fn-flaks-api-996459675-flvx6

➜  python-flask-connexion-example-openapi3-master git:(master) ✗ kubectl get service
NAME                                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
k8s-fn-flaks-api-996459675-flvx6        NodePort    10.96.202.68     <none>        7091:31060/TCP   48m
k8s-fn-flaks-api-new-86dc57c9dd-fbk5b   NodePort    10.104.118.31    <none>        8081:31596/TCP   40m
k8s-fn-flask-api                        NodePort    10.111.193.170   <none>        8080:31315/TCP   56m
kubernetes                              ClusterIP   10.96.0.1        <none>        443/TCP          5h43m

minikube dashboard
```