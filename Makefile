.IGNORE: browse-web clean clean-docker clean-helm clean-k8 clean-quick restart-quick update-scripts
.ONESHELL:
.PHONY: clean restart start set

BASE_PATH = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
AIRFLOW_DOCKER_PATH = $(BASE_PATH)/docker/docker-airflow/
SPARK_DOCKER_PATH = $(BASE_PATH)/docker/docker-spark/
AIRFLOW_HELM_PATH = $(BASE_PATH)/helm/official/charts/stable/airflow/
AIRFLOW_DAGS_PATH = $(BASE_PATH)/dags/
AIRFLOW_JOBS_PATH = $(BASE_PATH)/jobs/
TEMPLATE_PATH = $(BASE_PATH)/templates/
SCRIPTS_PATH = $(BASE_PATH)/scripts/
APPLICATION_NAME = airflow
NAMESPACE = ns-airflow
ENV = dev
LOCAL = False
PROJECT_ID = engineering-sandbox-228018
ifeq ($(LOCAL), True)
	AIRFLOW_IMG_NAME = atherin/airflow
	SPARK_IMG_NAME = atherin/pyspark
	HELM_CHART = airflow-local.yaml
	HELM_CHART_PATH = $(AIRFLOW_HELM_PATH)$(HELM_CHART)
else
	AIRFLOW_IMG_NAME = gcr.io/$(PROJECT_ID)/$(ENV)-airflow
	SPARK_IMG_NAME = gcr.io/$(PROJECT_ID)/$(ENV)-pyspark
	HELM_CHART = airflow-$(ENV).yaml
	HELM_CHART_PATH = $(AIRFLOW_HELM_PATH)$(HELM_CHART)
endif
AIRFLOW_IMG_TAG = 1.10.10
SPARK_IMG_TAG = 2.4.4
AIRFLOW_IMG = $(AIRFLOW_IMG_NAME):$(AIRFLOW_IMG_TAG)
SPARK_IMG = $(SPARK_IMG_NAME):$(SPARK_IMG_TAG)
AWK_STR='{gsub(/R_FERNET/,R_FERNET);gsub(/R_IMG/,R_IMG);gsub(/R_SPACE/,R_SPACE);gsub(/R_ITAG/,R_ITAG);}1'

bash-docker-airflow:
	docker run -it --entrypoint /bin/bash --rm $(AIRFLOW_IMG); \

bash-docker-spark:
	docker run -it --rm $(SPARK_IMG) bash; \

bash-k8-scheduler:
	$(eval _POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=scheduler,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl exec ${_POD} -c airflow-scheduler -n ${NAMESPACE} -it -- /bin/bash

bash-k8-web:
	$(eval _POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl exec ${_POD} -c airflow-web -n ${NAMESPACE} -it -- /bin/bash

bash-k8-worker:
	$(eval _POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=worker,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	kubectl exec ${_POD} -c airflow-worker -n ${NAMESPACE} -it -- /bin/bash

browse-web:
	$(eval INGRESS_IP=$(shell kubectl get svc -n ${NAMESPACE} --selector=app=nginx-ingress,component=controller -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'))
	echo 'Ingress at ${INGRESS_IP}'
	$(eval _POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}"))
	open "http://127.0.0.1:8080"
	kubectl port-forward -n ${NAMESPACE} ${_POD} 8080:8080

browse-dash:
	if [ "${LOCAL}" == "True" ]; then \
		minikube dashboard; \
	else \
		open "https://console.cloud.google.com/kubernetes/workload"; \
	fi

build-docker-airflow:
	cp -R jobs/ $(AIRFLOW_DOCKER_PATH)jobs/
	docker build --build-arg APP_ENV=${ENV} --build-arg AIRFLOW_VERSION=${AIRFLOW_IMG_TAG} -t $(AIRFLOW_IMG) $(AIRFLOW_DOCKER_PATH) --no-cache; \

build-docker-spark:
	cp -R jobs/ $(SPARK_DOCKER_PATH)jobs/
	docker build --build-arg APP_ENV=${ENV} --build-arg SPARK_VERSION=${SPARK_IMG_TAG} -t $(SPARK_IMG) $(SPARK_DOCKER_PATH) --no-cache; \

clean: clean-quick update-scripts
	if [ "${LOCAL}" == "True" ]; then \
		minikube delete; \
	fi

clean-k8:
	sh ${SCRIPTS_PATH}delete_nfs.sh
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

hooks:
	@for filename in $(BASE_PATH)/scripts/hooks/*; do \
		FILE="$$(basename $${filename})"; \
		DIR="$(BASE_PATH)/.git/hooks/"; \
		if [ -d $${DIR} ] ; then \
			cp $(BASE_PATH)/scripts/hooks/$${FILE} $(BASE_PATH)/.git/hooks/$${FILE}; \
			chmod 755 $(BASE_PATH)/.git/hooks/$${FILE}; \
		fi \
	done

push-docker-airflow:
	docker push $(AIRFLOW_IMG); \

push-docker-spark:
	docker push $(SPARK_IMG); \

restart: clean-quick
	sleep 10
	make start

start: update-scripts
	sh deploy.sh ${ENV} ${LOCAL}
	sleep 520
	make browse-web

status-k8:
	if [ "${LOCAL}" == "True" ]; then \
		minikube service list; \
	else \
		kubectl get pods --watch -n ${NAMESPACE}; \
	fi

tail-k8-web:
	$(eval POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=web" -o jsonpath="{.items[0].metadata.name}"))
	kubectl logs $(POD) -c airflow-web -n ${NAMESPACE} -f

tail-k8-scheduler:
	$(eval POD=$(shell kubectl get pods -n $(NAMESPACE) -l "component=scheduler" -o jsonpath="{.items[0].metadata.name}"))
	kubectl logs $(POD) -c airflow-scheduler -n ${NAMESPACE} -f

update: update-scripts
	helm upgrade ${APPLICATION_NAME} --install -f ${HELM_CHART_PATH} ${AIRFLOW_HELM_PATH} -n ${NAMESPACE}
	sleep 520
	make browse-web

update-helm:
	helm dependency update ${AIRFLOW_HELM_PATH}
	helm dependency build ${AIRFLOW_HELM_PATH}

update-scripts:
	$(eval FERNET=$(shell python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"))
	rm ${HELM_CHART_PATH}
	awk -v R_FERNET='${FERNET}' -v R_IMG='${AIRFLOW_IMG_NAME}' -v R_SPACE='${NAMESPACE}' -v R_ITAG='${AIRFLOW_IMG_TAG}' ${AWK_STR} ${TEMPLATE_PATH}${HELM_CHART} > ${HELM_CHART_PATH}
	rm ${SCRIPTS_PATH}delete_nfs.sh
	awk -v R_IMG='${AIRFLOW_IMG_NAME}' -v R_SPACE='${NAMESPACE}' ${AWK_STR} ${TEMPLATE_PATH}delete_nfs.sh > ${SCRIPTS_PATH}delete_nfs.sh
	rm ${BASE_PATH}/deploy.sh
	awk -v R_IMG='${AIRFLOW_IMG_NAME}' -v R_SPACE='${NAMESPACE}' -v R_ITAG='${AIRFLOW_IMG_TAG}' ${AWK_STR} ${TEMPLATE_PATH}airflow-deploy.sh > ${BASE_PATH}/deploy.sh

update-docker-airflow:
	make build-docker-airflow
	make push-docker-airflow

update-docker-spark:
	make build-docker-spark
	make push-docker-spark
