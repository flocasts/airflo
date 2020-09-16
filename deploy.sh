#!/bin/bash
set -eux

ENV=$1
LOCAL=$2
if [ -z "$ENV" ]; then
    ENV=dev
fi

if [ -z "$LOCAL" ]; then
    LOCAL=True
fi

PROJECT_ID="engineering-sandbox-228018"
APPLICATION_NAME="airflow"
NAMESPACE=ns-airflow
AIRFLOW_VERSION=1.10.10
BASE_PATH=$(pwd)
AIRFLOW_DOCKER_PATH=${BASE_PATH}/docker/docker-airflow/
SPARK_DOCKER_PATH=${BASE_PATH}/docker/docker-spark/
AIRFLOW_HELM_PATH=${BASE_PATH}/helm/official/charts/stable/airflow/
AIRFLOW_DAGS_PATH=${BASE_PATH}/dags/

echo "Deploying ${APPLICATION_NAME}:${ENV}..."
docker-machine env default
eval $(docker-machine env default)

if [ "${ENV}" == "prod" ]; then
    BUCKET="flosports-data-warehouse-sources"
else
    BUCKET="datawarehouse-staging-sources"
fi

if [ "${LOCAL}" == "True" ]; then
    AIRFLOW_HELM_CHART=${AIRFLOW_HELM_PATH}airflow-local.yaml

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
    REGION="us-central1-c"
    CLUSTER_NAME="sandbox"
    CONTEXT="gke_${PROJECT_ID}_${REGION}_${CLUSTER_NAME}"
    AIRFLOW_HELM_CHART=${AIRFLOW_HELM_PATH}airflow-${ENV}.yaml

    gcloud container clusters get-credentials ${CLUSTER_NAME}
    if ! kubectl get namespace ${NAMESPACE} >/dev/null 2>&1; then
        kubectl create namespace ${NAMESPACE}
    fi
    kubectl config set-context --current --namespace=${NAMESPACE}
    gcloud config set compute/zone ${REGION}
    gcloud config set compute/region ${REGION}
    gcloud config set composer/location ${REGION}

    if ! kubectl get serviceaccounts ${APPLICATION_NAME} --namespace=${NAMESPACE} >/dev/null 2>&1; then
        kubectl create serviceaccount ${APPLICATION_NAME} --namespace=${NAMESPACE}
    fi
    if ! kubectl get clusterrolebinding spark-role --namespace=${NAMESPACE} >/dev/null 2>&1; then
        kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=${NAMESPACE}:${APPLICATION_NAME} --namespace=${NAMESPACE}
    fi

    kubectl annotate serviceaccount $APPLICATION_NAME meta.helm.sh/release-name=$APPLICATION_NAME --overwrite
    kubectl annotate serviceaccount $APPLICATION_NAME meta.helm.sh/release-namespace=$NAMESPACE --overwrite
    kubectl label serviceaccount $APPLICATION_NAME app.kubernetes.io/managed-by=Helm --overwrite
fi

if ! kubectl get pvc nfs-airflow-logs --namespace ${NAMESPACE} >/dev/null 2>&1; then
    echo "Generating NFS..."
    sh nfs/create_nfs_logs_and_dags.sh
fi

echo "Generating secrets..."
if ! kubectl get secret airflow-aws --namespace ${NAMESPACE} >/dev/null 2>&1; then
    {
        ACCOUNT=$(aws sts get-caller-identity --query "Account" --profile ${ENV}) &&\
        AWS_ACCOUNT=("${ACCOUNT[@]//\"/}") &&\
        eval $(aws ssm get-parameter --name ${ENV}-azathoth-aws --with-decryption --profile ${ENV}  | jq -r  '.Parameter.Value' | jq -r '. | @sh "export AWS_ACCESS_KEY_ID=\(.access_key)\nexport AWS_SECRET_ACCESS_KEY=\(.secret_access_key)\nexport AWS_ACCOUNT=\(.account)"')
    } &> /dev/null
    kubectl create secret generic airflow-aws \
    --namespace ${NAMESPACE} \
    --from-literal=AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --from-literal=AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    --from-literal=AWS_ACCOUNT=${AWS_ACCOUNT}
fi
if ! kubectl get secret airflow-git --namespace ${NAMESPACE} >/dev/null 2>&1; then
    mkdir -p ${BASE_PATH}/config
    rsync -a ~/.ssh/ ${BASE_PATH}/config
    kubectl create secret generic airflow-git \
    --namespace ${NAMESPACE} \
    --from-file=id_rsa=${BASE_PATH}/config/id_rsa \
    --from-file=known_hosts=${BASE_PATH}/config/known_hosts \
    --from-file=id_rsa.pub=${BASE_PATH}/config/id_rsa.pub
    rm -rf ${BASE_PATH}/config
fi
if ! kubectl get secret gcr-json-key --namespace ${NAMESPACE} >/dev/null 2>&1; then
    mkdir -p ${BASE_PATH}/config
    aws s3api get-object --profile ${ENV} --bucket ${BUCKET} --key config/${PROJECT_ID}.json ${BASE_PATH}/config/${PROJECT_ID}.json
    kubectl create secret docker-registry gcr-json-key \
    --namespace ${NAMESPACE} \
    --docker-server=us.gcr.io \
    --docker-username=_json_key \
    --docker-password="$(cat ${BASE_PATH}/config/${PROJECT_ID}.json)" \
    --docker-email=cthulhu@flosports.tv
    rm -rf ${BASE_PATH}/config
    if [ "${LOCAL}" == "False" ]; then
        kubectl patch serviceaccount ${APPLICATION_NAME} -p '{"imagePullSecrets": [{"name": "gcr-json-key"}]}'
    fi
fi

if ! helm status nginx-ingress --namespace ${NAMESPACE}>/dev/null 2>&1; then
    echo "Helm Ingress install..."
    helm install nginx-ingress stable/nginx-ingress --namespace ${NAMESPACE} --set controller.service.externalTrafficPolicy=Local
fi

if ! helm status ${APPLICATION_NAME} --namespace ${NAMESPACE}>/dev/null 2>&1; then
    echo "Helm Airflow install..."
    helm install ${APPLICATION_NAME} -f ${AIRFLOW_HELM_CHART} ${AIRFLOW_HELM_PATH} --namespace ${NAMESPACE}
fi

export SERVICE_IP=$(kubectl get svc airflow-web -o jsonpath='{.spec.clusterIP}' --namespace ${NAMESPACE})
echo "Web service initiated at ${SERVICE_IP}..."
