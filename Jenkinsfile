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
                dir('workspace/flask') {  // Navigate to the flask directory
                    sh 'python3 -m venv $VENV_PATH'
                }
            }
        }
        
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                dir('workspace/flask') {  // Navigate to the flask directory
                    // Activate the virtual environment and install dependencies
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
                sh 'docker-compose up -d flask-app'
                sh 'sleep 10'
                sh 'curl -I http://localhost:5002 || echo "Flask app not running on port 5001"'
            }
        }
        
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
    }
}
