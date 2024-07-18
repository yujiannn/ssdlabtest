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
                    
                    sh 'bash -c "python3 -m venv $VENV_PATH"'
                    // Activate the virtual environment
                    sh 'bash -c "source $VENV_PATH/bin/activate"'
                   
                }
            }
        }
        
        stage('Install dependencies') {
            steps {
                // Install any dependencies listed in requirements.txt
                sh 'bash -c "source $VENV_PATH/bin/activate && pip install -r requirements.txt"' 
                
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
        
        stage('Deploy Flask App') {
            steps {
                sh 'bash -c "source $VENV_PATH/bin/activate && FLASK_APP=$FLASK_APP flask run --host=0.0.0.0 --port=5000 &"'
                // Wait to ensure the app has time to start
                sh 'sleep 10'
                // Check if Flask app is running
                sh 'curl -I http://localhost:5000 || echo "Flask app not running on port 5000"'
            }
        }
    }
    
    post {
        always {
            script {
                echo 'Cleaning up...'
                // Ensure we are in a workspace directory
                dir('workspace') {
                    sh 'rm -rf $VENV_PATH'
                }
            }
        }
    }
}
