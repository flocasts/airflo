# Airflow in Kubernetes Executor

### Caveats
- Currently set to run locally.
- In-progress

### Pre-requisite
- Download Docker Desktop from [here](https://www.docker.com/products/docker-desktop] and setup in your local machine)
- Download Virtualbox from [here](https://www.virtualbox.org/wiki/Downloads) and setup in your local machine
- Install Minikube, Helm & add package repo
    ```
    bash
    brew update

    # install minikube
    brew install minikube

    # install helm
    brew install kubernetes-helm

    # add package repository to helm
    helm repo add stable https://kubernetes-charts.storage.googleapis.com

    # initialize docker-machine
    docker-machine start
    docker-machine env
    eval $(docker-machine env)
    ```

## Building Locally

```
bash

# If the Airflow UI doesn't load, wait until the K8s dashboard is healthy (~6-10 min).
$ make start

# Once `make-start` completes, the following can be run on different terminals.
$ kubectl get pods --watch  # to monitor the pod health
$ minikube dashboard  # to get the K8S dashboard

# Once you are done with the services you can stop everything with the following:
$ make clean
```
