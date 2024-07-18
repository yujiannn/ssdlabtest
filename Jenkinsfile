pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        FLASK_APP = 'app.py'
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$VENV_PATH/bin"
    }
    
    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        
        stage('Clone Repository') {
            steps {
                script {
                    // Ensure we are in a workspace directory
                    dir('workspace') {
                        git branch: 'main', url: 'https://github.com/motorfireman/Test.git'
                    }
                }
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                script {
                    sh 'python3 -m venv $VENV_PATH'
                    // Activate the virtual environment
                    sh 'source $VENV_PATH/bin/activate'
                }
            }
        }
        
        stage('Install dependencies') {
            steps {
                // Install any dependencies listed in requirements.txt
                sh 'source $VENV_PATH/bin/activate && pip install -r requirements.txt'
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
                // Start the Flask app container
                sh 'docker-compose up -d flask-app'
                // Wait to ensure the app has time to start
                sh 'sleep 10'
                // Check if Flask app is running
                sh 'curl -I http://localhost:5000 || echo "Flask app not running on port 5000"'
            }
        }
        
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
    }
}
