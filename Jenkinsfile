pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        FLASK_APP = 'app.py'
        PATH = "$VENV_PATH/bin:$PATH"
    }
    
    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        
        stage('Clone Repository') {
            steps {
                dir('workspace') {
                    git branch: 'main', url: 'https://github.com/motorfireman/Test.git'
                }
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                dir('workspace/flask') {
                    sh 'python3 -m venv $VENV_PATH'
                }
            }
        }
        
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                dir('workspace/flask') {
                    sh '. $VENV_PATH/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        
        stage('Dependency Check') {
            steps {
                echo 'Running dependency check...'
            }
        }
        
        stage('UI Testing') {
            steps {
                echo 'Running UI tests...'
            }
        }
    }
    
    post {
        success {
            script {
                echo 'Deploying Flask App...'
                sh 'docker ps --filter publish=5000 --format "{{.ID}}" | xargs -r docker stop'
                sh 'docker ps -a --filter status=exited --filter publish=5000 --format "{{.ID}}" | xargs -r docker rm'
                sh 'docker-compose up -d flask-app'
                sh 'sleep 10'
                script {
                    def response = sh(script: 'curl -I http://localhost:5000', returnStatus: true)
                    if (response != 0) {
                        echo 'Flask app not running on port 5000, fetching logs...'
                        sh 'docker logs $(docker ps -q --filter "ancestor=flask-app")'
                        error 'Flask app failed to start'
                    }
                }
            }
        }
        
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
    }
}
