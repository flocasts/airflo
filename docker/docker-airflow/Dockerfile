# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# THIS DOCKERFILE IS INTENDED FOR PRODUCTION USE AND DEPLOYMENT.
# NOTE! IT IS ALPHA-QUALITY FOR NOW - WE ARE IN A PROCESS OF TESTING IT
#
#
# This is a multi-segmented image. It actually contains two images:
#
# airflow-build-image  - there all airflow dependencies can be installed (and
#                        built - for those dependencies that require
#                        build essentials). Airflow is installed there with
#                        --user switch so that all the dependencies are
#                        installed to ${HOME}/.local
#
# main                 - this is the actual production image that is much
#                        smaller because it does not contain all the build
#                        essentials. Instead the ${HOME}/.local folder
#                        is copied from the build-image - this way we have
#                        only result of installation and we do not need
#                        all the build essentials. This makes the image
#                        much smaller.
#
FROM apache/airflow:1.10.10-python3.7
MAINTAINER atherin

ARG APP_ENV="dev"
ENV APP_ENV=${APP_ENV}

ARG AIRFLOW_VERSION="1.10.10"
ENV AIRFLOW_VERSION=${AIRFLOW_VERSION}

ARG AIRFLOW_EXTRAS="kubernetes"
ENV AIRFLOW_EXTRAS=${AIRFLOW_EXTRAS}

ARG PYTHON_MAJOR_MINOR_VERSION="3.7"
ENV PYTHON_MAJOR_MINOR_VERSION=${PYTHON_MAJOR_MINOR_VERSION}

ARG AIRFLOW_CONSTRAINTS_URL="https://raw.githubusercontent.com/apache/airflow/${AIRFLOW_VERSION}/requirements/requirements-python${PYTHON_MAJOR_MINOR_VERSION}.txt"
ENV AIRFLOW_CONSTRAINTS_URL=${AIRFLOW_CONSTRAINTS_URL}

RUN pip install "apache-airflow[${AIRFLOW_EXTRAS}]==${AIRFLOW_VERSION}" \
    --constraint "${AIRFLOW_CONSTRAINTS_URL}"

COPY --chown=airflow:root jobs /jobs
RUN ls -al /jobs/
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["airflow", "--help"]
