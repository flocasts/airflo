#!/usr/bin/env bash

set -e

REGION="us-central1-c"
# NODE_POOL="default-pool"
# CLUSTER_NAME="sandbox"
MACHINE_TYPE="n1-standard-2"
NODE_POOL="${MACHINE_TYPE}-pool"
CLUSTER_NAME="airflow-sandbox"
CONTEXT="gke_${PROJECT_ID}_${REGION}_${CLUSTER_NAME}"
AIRFLOW_HELM_CHART=${AIRFLOW_HELM_PATH}airflow-${ENV}.yaml

if ! gcloud container clusters describe ${CLUSTER_NAME} --region ${REGION} >/dev/null 2>&1; then
    gcloud container clusters create ${CLUSTER_NAME} \
    --region ${REGION} \
    --machine-type n1-standard-1 \
    --enable-autoscaling \
    --max-nodes 10 \
    --min-nodes 1
fi

if ! gcloud container node-pools describe ${NODE_POOL} --cluster ${CLUSTER_NAME} --region ${REGION} >/dev/null 2>&1; then
    gcloud container node-pools create ${NODE_POOL} \
    --cluster ${CLUSTER_NAME} \
    --region ${REGION} \
    --num-nodes 0 \
    --disk-size 100 \
    --enable-autoscaling \
    --preemptible \
    --machine-type ${MACHINE_TYPE} \
    --enable-autoscaling \
    --node-taints=node-pool=${NODE_POOL}:NoExecute \
    --min-nodes=0 \
    --max-nodes=4
fi
