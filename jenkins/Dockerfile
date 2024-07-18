# Jenkins Dockerfile
FROM jenkins/jenkins:lts

USER root

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
