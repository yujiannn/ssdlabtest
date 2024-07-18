FROM jenkins/jenkins:lts

USER root

# Install Python and Docker CLI
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv apt-transport-https ca-certificates curl gnupg2 lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    groupadd docker || true && \
    usermod -aG docker jenkins && \
    chmod 666 /var/run/docker.sock || true && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000
