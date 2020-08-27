.IGNORE: clean clean-docker clean-helm clean-k8 clean-quick restart-quick
.ONESHELL:
.PHONY: clean restart start set

BASE_PATH = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
AIRFLOW_DOCKER_PATH = $(BASE_PATH)/docker/puckel/docker-airflow/
SPARK_DOCKER_PATH = $(BASE_PATH)/docker/atherin/docker-spark/
AIRFLOW_HELM_PATH = $(BASE_PATH)/helm/official/charts/stable/airflow/
AIRFLOW_DAGS_PATH = $(BASE_PATH)/dags/
AIRFLOW_JOBS_PATH = $(BASE_PATH)/jobs/
APPLICATION_NAME = airflow
NAMESPACE = airflow
ENV = dev
# LOCAL = True
LOCAL = False
PROJECT_ID = engineering-sandbox-228018
# AIRFLOW_IMAGE = atherin/$(ENV)-airflow:1.10.4
# SPARK_IMAGE = atherin/$(ENV)-pyspark:2.4.4
AIRFLOW_IMAGE = gcr.io/$(PROJECT_ID)/$(ENV)-airflow:1.10.9
SPARK_IMAGE = gcr.io/$(PROJECT_ID)/$(ENV)-pyspark:2.4.4

bash-docker-airflow:
	docker run -v $(AIRFLOW_DAGS_PATH):/usr/dags/ -it --rm $(AIRFLOW_IMAGE) bash

bash-docker-spark:
	docker run  -v $(AIRFLOW_JOBS_PATH):/usr/jobs/ -it --rm $(SPARK_IMAGE) bash

bash-k8:
	$(eval _POD=$(shell kubectl get pods --namespace $(NAMESPACE) -l "component=worker,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl exec $(_POD) -c airflow-worker -it -- /bin/bash

browse-web:
	minikube service airflow-web -n $(NAMESPACE)

browse-dash:
	minikube dashboard

build-docker-airflow:
	docker build --build-arg APP_ENV=${ENV} -t $(AIRFLOW_IMAGE) $(AIRFLOW_DOCKER_PATH) --no-cache

build-docker-spark:
	docker build --build-arg APP_ENV=${ENV} -t $(SPARK_IMAGE) $(SPARK_DOCKER_PATH) --no-cache

clean: clean-quick
	if [ "${LOCAL}" == "True" ]; then \
		minikube delete; \
	fi

clean-k8:
	kubectl delete pods,services --all --namespace=$(NAMESPACE)
	kubectl delete secret airflow-aws

clean-helm:
	helm delete ${APPLICATION_NAME}

clean-docker:
	$(eval _IMAGES=$(shell docker images -q -f dangling=true))
	$(eval _VOLUMES=$(shell docker volume ls -qf dangling=true))
	if [ -n "${_IMAGES}" ]; then \
		docker rmi $(_IMAGES); \
	fi
	if [ -n "${_VOLUMES}" ]; then \
		docker volume rm $(_VOLUMES); \
	fi
	docker container prune --filter "until=24h" --force
	docker image prune --filter "until=24h" --force

clean-quick:
	make clean-helm
	make clean-k8
	make clean-docker
	if [ "${LOCAL}" == "True" ]; then \
		minikube service list; \
	fi

debug-k8:
	$(eval _POD=$(shell kubectl get pods --namespace $(NAMESPACE) -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl logs $(_POD) -p
	# kubectl describe pod $(_POD)
	# kubectl get all --namespace $(NAMESPACE) # --all-namespaces

push-docker-airflow:
	docker push $(AIRFLOW_IMAGE)

push-docker-spark:
	docker push $(SPARK_IMAGE)

restart: clean-quick
	sleep 10
	make start

start:
	sh deploy.sh ${ENV} ${LOCAL}
	sleep 580
	make browse-web

status-k8:
	# kubectl config get-contexts # troubleshoot contexts
	# kubectl config use-context minikube
	# kubectl get services --watch -n airflow
	# kubectl describe pods
	kubectl get pods --watch -n airflow

update-helm:
	helm dependency update ${AIRFLOW_HELM_PATH}
	helm dependency build ${AIRFLOW_HELM_PATH}

update-docker-images:
	make build-docker-airflow
	make push-docker-airflow
	make build-docker-spark
	make push-docker-spark
