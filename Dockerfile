# Start from the Airflow base image
FROM apache/airflow:2.10.5-python3.9

# Become root to install system dependencies and Java
USER root

# Install basic utilities
RUN apt-get update && apt-get install -y curl wget unzip && rm -rf /var/lib/apt/lists/*

# Install Temurin JDK 11
RUN mkdir -p /opt/java && \
    curl -L -o /tmp/openjdk.tar.gz https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.26+4/OpenJDK11U-jdk_x64_linux_hotspot_11.0.26_4.tar.gz && \
    tar -xzf /tmp/openjdk.tar.gz -C /opt/java --strip-components=1 && \
    rm /tmp/openjdk.tar.gz

ENV JAVA_HOME=/opt/java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Apache Spark
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
RUN curl -L -o /tmp/spark.tgz https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf /tmp/spark.tgz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm /tmp/spark.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y gnupg2 curl apt-transport-https unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy base requirements and install as airflow user
COPY base-requirements.txt /base-requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /base-requirements.txt

# Copy additional requirements and install
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt


# 🟢 Switch back to airflow user for pip installs
USER airflow

RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt
