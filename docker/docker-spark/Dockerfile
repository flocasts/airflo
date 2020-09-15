# VERSION 2.4.4
FROM python:3.7.6-slim
MAINTAINER atherin
ARG APP_ENV="dev"
ENV APP_ENV=${APP_ENV}
ENV SNOWFLAKE_VERSION="4.29.0"
ENV SCALA_VERSION="2.11.12"

# Reset to root to run installation tasks
USER 0

# PYTHON
# http://blog.stuart.axelbrooke.com/python-3-on-spark-return-of-the-pythonhashseed
ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ARG PYTHON_DEPS=" boto3 findspark pyspark pyyaml"

# HADOOP
ENV HADOOP_VERSION 2.7.0
ENV HADOOP_HOME /usr/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin

# SPARK
ARG SPARK_VERSION=2.4.4
ENV SPARK_VERSION=${SPARK_VERSION}
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-without-hadoop
ENV SPARK_HOME /usr/spark-${SPARK_VERSION}
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV SNOWFLAKE_CONNECTOR spark-snowflake_2.11-2.8.1-spark_2.4.jar
ENV SNOWFLAKE_CONNECTOR_URL "https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.11/2.8.1-spark_2.4/${SNOWFLAKE_CONNECTOR}"
ENV SNOWFLAKE_JDBC snowflake-jdbc-3.12.9.jar
ENV SNOWFLAKE_JDBC_URL "https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.12.9/${SNOWFLAKE_JDBC}"

ENV SPARK_JAR_PATH ${SPARK_HOME}/jars
ENV PATH $PATH:${SPARK_HOME}/bin

RUN mkdir -p /usr/share/man/man1 \
    && echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        curl \
        apt-transport-https \
    && apt-get install -y \
        openjdk-8-jre \
    && curl -sL --retry 3 \
        "https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
        | gunzip \
        | tar -x -C /usr/ \
    && rm -rf $HADOOP_HOME/share/doc \
    && chown -R root:root $HADOOP_HOME \
    && pip3 install -U pip setuptools wheel \
    && if [ -n "${PYTHON_DEPS}" ]; then pip3 install ${PYTHON_DEPS}; fi \
    && curl -sL --retry 3 \
        "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
        | gunzip \
        | tar x -C /usr/ \
    && mv /usr/$SPARK_PACKAGE $SPARK_HOME \
    && curl -sL --retry 3 \
        ${SNOWFLAKE_CONNECTOR_URL} -o ${SPARK_JAR_PATH}/${SNOWFLAKE_CONNECTOR} \
    && curl -sL --retry 3 \
        ${SNOWFLAKE_JDBC_URL} -o ${SPARK_JAR_PATH}/${SNOWFLAKE_JDBC} \
    && chown -R root:root $SPARK_HOME \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=root:root jobs /jobs
RUN ls -al /jobs/
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
WORKDIR ${SPARK_HOME}
