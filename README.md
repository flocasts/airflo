# Airflow in Kubernetes Executor

### Pre-requisite
- Download Docker Desktop from [here](https://www.docker.com/products/docker-desktop] and setup in your local machine)
- Download Virtualbox from [here](https://www.virtualbox.org/wiki/Downloads) and setup in your local machine
- Install Minikube, Helm & add package repo
    ```
    bash
    brew update

    # install minikube for local development
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

## Deployment

```
bash

# Set params on Makefile
# Setting LOCAL = False will deploy to GCP

# If the Airflow UI doesn't load, wait until the K8s dashboard is healthy (~6-10 min).
$ make start

# Once `make-start` completes, the following can be run on different terminals for monitoring.
$ kubectl get pods --watch  # to monitor the pod health
$ make browse-dash  # to get the K8s dashboard
$ make tail-k8-web  # tails log for web pod
$ make tail-k8-scheduler  # tails log for scheduler pod

# Once you are done with the services you can stop everything with the following:
$ make clean
```
