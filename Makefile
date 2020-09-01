.IGNORE: browse-web clean clean-docker clean-helm clean-k8 clean-quick restart-quick
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
LOCAL = False
PROJECT_ID = engineering-sandbox-228018
DH_AIRFLOW_IMAGE = atherin/airflow:1.10.9
DH_SPARK_IMAGE = atherin/pyspark:2.4.4
GCR_AIRFLOW_IMAGE = gcr.io/$(PROJECT_ID)/$(ENV)-airflow:1.10.9
GCR_SPARK_IMAGE = gcr.io/$(PROJECT_ID)/$(ENV)-pyspark:2.4.4

bash-docker-airflow:
	if [ "${LOCAL}" == "True" ]; then \
		docker run -v $(AIRFLOW_DAGS_PATH):/usr/dags/ -it --rm $(DH_AIRFLOW_IMAGE) bash; \
	else \
		docker run -v $(AIRFLOW_DAGS_PATH):/usr/dags/ -it --rm $(GCR_AIRFLOW_IMAGE) bash; \
	fi

bash-docker-spark:
	if [ "${LOCAL}" == "True" ]; then \
		docker run  -v $(AIRFLOW_JOBS_PATH):/usr/jobs/ -it --rm $(DH_SPARK_IMAGE) bash; \
	else \
		docker run  -v $(AIRFLOW_JOBS_PATH):/usr/jobs/ -it --rm $(GCR_SPARK_IMAGE) bash; \
	fi

bash-k8:
	$(eval _POD=$(shell kubectl get pods --namespace $(NAMESPACE) -l "component=worker,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl exec $(_POD) -c airflow-worker -it -- /bin/bash

browse-web:
	$(eval _POD=$(shell kubectl get pods --namespace airflow -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	open "http://127.0.0.1:8080"
	kubectl port-forward --namespace airflow $(_POD) 8080:8080

browse-dash:
	if [ "${LOCAL}" == "True" ]; then \
		minikube dashboard; \
	else \
		open "https://console.cloud.google.com/kubernetes/workload"; \
	fi

build-docker-airflow:
	if [ "${LOCAL}" == "True" ]; then \
		docker build --build-arg APP_ENV=${ENV} -t $(DH_AIRFLOW_IMAGE) $(AIRFLOW_DOCKER_PATH) --no-cache; \
	else \
		docker build --build-arg APP_ENV=${ENV} -t $(GCR_AIRFLOW_IMAGE) $(AIRFLOW_DOCKER_PATH) --no-cache; \
	fi

build-docker-spark:
	if [ "${LOCAL}" == "True" ]; then \
		docker build --build-arg APP_ENV=${ENV} -t $(DH_SPARK_IMAGE) $(SPARK_DOCKER_PATH) --no-cache; \
	else \
		docker build --build-arg APP_ENV=${ENV} -t $(GCR_SPARK_IMAGE) $(SPARK_DOCKER_PATH) --no-cache; \
	fi

clean: clean-quick
	if [ "${LOCAL}" == "True" ]; then \
		minikube delete; \
	fi

clean-k8:
	# kubectl get pv | tail -n+2 | awk '{print $1}' | xargs -I{} kubectl patch pv {} --type='merge' -p '{"metadata":{"finalizers": null}}'
	# kubectl delete pv,pvc,pod --all --namespace=airflow
	kubectl delete namespace $(NAMESPACE)

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

debug-k8:
	$(eval _POD=$(shell kubectl get pods --namespace $(NAMESPACE) -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl logs $(_POD) -p
	# lsof -i :8080
	# kubectl describe pod $(_POD)
	# kubectl get all --namespace $(NAMESPACE) # --all-namespaces

push-docker-airflow:
	if [ "${LOCAL}" == "True" ]; then \
		docker push $(DH_AIRFLOW_IMAGE); \
	else \
		docker push $(GCR_AIRFLOW_IMAGE); \
	fi

push-docker-spark:
	if [ "${LOCAL}" == "True" ]; then \
		docker push $(DH_SPARK_IMAGE); \
	else \
		docker push $(GCR_SPARK_IMAGE); \
	fi

restart: clean-quick
	sleep 10
	make start

start:
	sh deploy.sh ${ENV} ${LOCAL}
	sleep 520
	make browse-web

status-k8:
	if [ "${LOCAL}" == "True" ]; then \
		minikube service list; \
	else \
		kubectl get pods --watch -n airflow; \
	fi

update-helm:
	helm dependency update ${AIRFLOW_HELM_PATH}
	helm dependency build ${AIRFLOW_HELM_PATH}

update-docker-images:
	make build-docker-airflow
	make push-docker-airflow
	make build-docker-spark
	make push-docker-spark
