FROM jenkins/jenkins:lts

USER root

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Optionally, create a symlink for `python` to `python3`
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000