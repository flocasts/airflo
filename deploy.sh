#!/bin/bash
set -eu

ENV=$1
LOCAL=$2
if [ -z "$ENV" ]; then
    ENV=dev
fi

if [ -z "$LOCAL" ]; then
    LOCAL=True
fi

APPLICATION_NAME="airflow"
NAMESPACE="airflow"
BASE_PATH=$(pwd)
AIRFLOW_DOCKER_PATH=${BASE_PATH}/docker/puckel/docker-airflow/
SPARK_DOCKER_PATH=${BASE_PATH}/docker/atherin/docker-spark/
AIRFLOW_HELM_PATH=${BASE_PATH}/helm/official/charts/stable/airflow/
AIRFLOW_DAGS_PATH=${BASE_PATH}/dags/
AIRFLOW_HELM_CHART=${BASE_PATH}/helm/official/charts/airflow.yaml
AIRFLOW_IMAGE=atherin/airflow:1.10.4
SPARK_IMAGE=atherin/pyspark:2.4.4
echo "Deploying ${APPLICATION_NAME}:${ENV}..."

docker-machine env default
eval $(docker-machine env default)
echo "Docker initiated at ${DOCKER_HOST}..."
docker build --build-arg APP_ENV=${ENV} -t ${AIRFLOW_IMAGE} ${AIRFLOW_DOCKER_PATH}
docker build --build-arg APP_ENV=${ENV} -t ${SPARK_IMAGE} ${SPARK_DOCKER_PATH}

if [ "${LOCAL}" == "True" ]; then
    if ! minikube status >/dev/null 2>&1; then
        minikube start --vm-driver=virtualbox --memory=6096 --disk-size=20000mb --kubernetes-version v1.15.0
    fi

    minikube docker-env
    eval $(minikube -p minikube docker-env)

    if ! kubectl get namespace ${NAMESPACE} >/dev/null 2>&1; then
        kubectl create namespace ${NAMESPACE}
    fi
    kubectl config set-context minikube --cluster=minikube --namespace=${NAMESPACE}
else
    echo "Not implemented..."
    CONTEXT="gke_engineering-sandbox-228018_us-central1-a_sandbox"
    if ! kubectl get namespace ${NAMESPACE} >/dev/null 2>&1; then
        kubectl create namespace ${NAMESPACE}
    fi
    kubectl config set-context --current --namespace=${NAMESPACE}
    if ! kubectl get serviceaccounts ${APPLICATION_NAME} >/dev/null 2>&1; then
        kubectl create serviceaccount ${APPLICATION_NAME} --namespace=${NAMESPACE}
    fi
    if ! kubectl get clusterrolebinding spark-role >/dev/null 2>&1; then
        kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=${NAMESPACE}:${APPLICATION_NAME} --namespace=${NAMESPACE}
    fi
fi

echo "Generating secrets..."
if ! kubectl get secret airflow-aws >/dev/null 2>&1; then
    {
        ACCOUNT=$(aws sts get-caller-identity --query "Account" --profile ${ENV}) &&\
        AWS_ACCOUNT=("${ACCOUNT[@]//\"/}") &&\
        eval $(aws ssm get-parameter --name ${ENV}-azathoth-aws --with-decryption --profile ${ENV}  | jq -r  '.Parameter.Value' | jq -r '. | @sh "export AWS_ACCESS_KEY_ID=\(.access_key)\nexport AWS_SECRET_ACCESS_KEY=\(.secret_access_key)\nexport AWS_ACCOUNT=\(.account)"')
    } &> /dev/null
    kubectl create secret generic airflow-aws \
    --from-literal=AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --from-literal=AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    --from-literal=AWS_ACCOUNT=${AWS_ACCOUNT}
fi
if ! kubectl get secret airflow-git >/dev/null 2>&1; then
    rsync -a ~/.ssh/ ${BASE_PATH}/ssh
    kubectl create secret generic airflow-git --from-file=id_rsa=${BASE_PATH}/ssh/id_rsa --from-file=known_hosts=${BASE_PATH}/ssh/known_hosts --from-file=id_rsa.pub=${BASE_PATH}/ssh/id_rsa.pub
    rm -rf ${BASE_PATH}/ssh
fi

if ! helm status ${APPLICATION_NAME} >/dev/null 2>&1; then
    echo "Configuring helm..."
    helm install ${APPLICATION_NAME} -f ${AIRFLOW_HELM_CHART} ${AIRFLOW_HELM_PATH}
fi

export SERVICE_IP=$(kubectl get svc airflow-web -o jsonpath='{.spec.clusterIP}' --namespace ${NAMESPACE})
echo "Web service initiated at ${SERVICE_IP}..."
