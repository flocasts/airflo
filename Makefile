AIRFLOW_VERSION ?= 1.8.0
KUBECTL_VERSION ?= 1.6.1
KUBE_AIRFLOW_VERSION ?= 0.10

REPOSITORY ?= mumoshu/kube-airflow
TAG ?= $(AIRFLOW_VERSION)-$(KUBECTL_VERSION)-$(KUBE_AIRFLOW_VERSION)
IMAGE ?= $(REPOSITORY):$(TAG)
ALIAS ?= $(REPOSITORY):$(AIRFLOW_VERSION)-$(KUBECTL_VERSION)

BUILD_ROOT ?= build/$(TAG)
DOCKERFILE ?= $(BUILD_ROOT)/Dockerfile
ROOTFS ?= $(BUILD_ROOT)/rootfs
AIRFLOW_CONF ?= $(BUILD_ROOT)/config/airflow.cfg
ENTRYPOINT_SH ?= $(BUILD_ROOT)/script/entrypoint.sh
GIT_SYNC ?= $(BUILD_ROOT)/script/git-sync
DAGS ?= $(BUILD_ROOT)/dags
AIRFLOW_REQUIREMENTS ?= $(BUILD_ROOT)/requirements/airflow.txt
DAGS_REQUIREMENTS ?= $(BUILD_ROOT)/requirements/dags.txt
DOCKER_CACHE ?= docker-cache
SAVED_IMAGE ?= $(DOCKER_CACHE)/image-$(AIRFLOW_VERSION)-$(KUBECTL_VERSION).tar
AIRFLOW_HOME=/usr/local/airflow

NAMESPACE ?= ns-andrew-tan
HELM_APPLICATION_NAME ?= dev-airflo
HELM_VALUES ?= ./values.yaml
CHART_LOCATION ?= ./airflow
CHART_PKG_LOCATION ?= stable/airflow
# CHART_PKG_LOCATION ?= ./airflow-5.2.5.tgz
EMBEDDED_DAGS_LOCATION ?= "./dags"
REQUIREMENTS_TXT_LOCATION ?= "requirements/dags.txt"
PASS_GEN ?= "$ (openssl rand -base64 13)"

.PHONY: build clean

clean:
	rm -Rf build

start:
	helm upgrade -f $(HELM_VALUES) \
				 --namespace=$(NAMESPACE) \
	             --install \
	             --debug \
	             $(HELM_APPLICATION_NAME) \
	             $(CHART_PKG_LOCATION)

check:
	helm install --dry-run \
	             --namespace=$(NAMESPACE) \
	             --debug \
	             -f $(HELM_VALUES) \
				 $(HELM_APPLICATION_NAME) \
				 $(CHART_PKG_LOCATION)

ls:
	helm ls --namespace=$(NAMESPACE)

stop: delete
	helm delete $(HELM_APPLICATION_NAME)

build: clean $(DOCKERFILE) $(ROOTFS) $(DAGS) $(AIRFLOW_CONF) $(ENTRYPOINT_SH) $(GIT_SYNC) $(AIRFLOW_REQUIREMENTS) $(DAGS_REQUIREMENTS)
	cd $(BUILD_ROOT) && docker build -t $(IMAGE) . && docker tag $(IMAGE) $(ALIAS)

publish:
	docker push $(IMAGE) && docker push $(ALIAS)

$(DOCKERFILE): $(BUILD_ROOT)
	sed -e 's/%%KUBECTL_VERSION%%/'"$(KUBECTL_VERSION)"'/g;' \
	    -e 's/%%AIRFLOW_VERSION%%/'"$(AIRFLOW_VERSION)"'/g;' \
	    -e 's#%%EMBEDDED_DAGS_LOCATION%%#'"$(EMBEDDED_DAGS_LOCATION)"'#g;' \
	    -e 's#%%REQUIREMENTS_TXT_LOCATION%%#'"$(REQUIREMENTS_TXT_LOCATION)"'#g;' \
	    Dockerfile.template > $(DOCKERFILE)

$(ROOTFS): $(BUILD_ROOT)
	mkdir -p rootfs
	cp -R rootfs $(ROOTFS)

$(AIRFLOW_CONF): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(AIRFLOW_CONF))
	cp config/airflow.cfg $(AIRFLOW_CONF)

$(ENTRYPOINT_SH): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(ENTRYPOINT_SH))
	cp script/entrypoint.sh $(ENTRYPOINT_SH)

$(GIT_SYNC): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(GIT_SYNC))
	cp script/git-sync $(GIT_SYNC)

$(AIRFLOW_REQUIREMENTS): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(AIRFLOW_REQUIREMENTS))
	cp requirements/airflow.txt $(AIRFLOW_REQUIREMENTS)

$(DAGS_REQUIREMENTS): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(DAGS_REQUIREMENTS))
	cp $(REQUIREMENTS_TXT_LOCATION) $(DAGS_REQUIREMENTS)

$(DAGS): $(BUILD_ROOT)
	mkdir -p $(shell dirname $(DAGS))
	cp -R $(EMBEDDED_DAGS_LOCATION) $(DAGS)

$(BUILD_ROOT):
	mkdir -p $(BUILD_ROOT)

travis-env:
	travis env set DOCKER_EMAIL $(DOCKER_EMAIL)
	travis env set DOCKER_USERNAME $(DOCKER_USERNAME)
	travis env set DOCKER_PASSWORD $(DOCKER_PASSWORD)

test:
	@echo There are no tests available for now. Skipping

save-docker-cache: $(DOCKER_CACHE)
	docker save $(IMAGE) $(shell docker history -q $(IMAGE) | tail -n +2 | grep -v \<missing\> | tr '\n' ' ') > $(SAVED_IMAGE)
	ls -lah $(DOCKER_CACHE)

load-docker-cache: $(DOCKER_CACHE)
	if [ -e $(SAVED_IMAGE) ]; then docker load < $(SAVED_IMAGE); fi

$(DOCKER_CACHE):
	mkdir -p $(DOCKER_CACHE)

create: set-config
	if ! kubectl get namespace $(NAMESPACE) >/dev/null 2>&1; then \
	  kubectl create namespace $(NAMESPACE); \
	fi
	helm package $(CHART_LOCATION)

ref:
	@echo export RAND_PASS=$ openssl rand -base64 13
	@echo kubectl exec $ WORKER -c airflow-worker -it -- /bin/bash
	@echo kubectl create secret generic $(HELM_APPLICATION_NAME)-git --from-file=id_rsa=./id_rsa --from-file=known_hosts=./known_hosts --from-file=id_rsa.pub=./id_rsa.pub
	@echo kubectl create secret generic $(HELM_APPLICATION_NAME)-postgres --from-literal=postgres-password='RAND_PASS'
	@echo kubectl create secret generic $(HELM_APPLICATION_NAME)-postgresql --from-literal=postgresql-password='RAND_PASS'
	@echo kubectl create secret generic $(HELM_APPLICATION_NAME)-redis --from-literal=redis-password='RAND_PASS'
	@echo docker-machine start default
	@echo docker-machine env

browse-web:
	minikube service web -n $(NAMESPACE)

browse-flower:
	minikube service flower -n $(NAMESPACE)

delete:
	kubectl delete pods,services --all --namespace=$(NAMESPACE)
	# Alternative (last-resort)
	# kubectl delete -f airflow.all.yaml --namespace=$(NAMESPACE) --all

get-all:
	kubectl get all --namespace $(NAMESPACE)
	# kubectl get all --all-namespaces

get-config:
	kubectl config get-contexts

status:
	helm status $(HELM_APPLICATION_NAME)

set-config:
	kubectl config set-context --current --namespace=$(NAMESPACE)
