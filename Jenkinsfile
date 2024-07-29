pipeline {
    agent any

    environment {
        FLASK_APP = 'flask/app.py'  // Correct path to the Flask app
        SONARQUBE_SCANNER_HOME = tool name: 'SonarQube Scanner'
        SONARQUBE_TOKEN = 'your_sonarqube_token_here'
    }
    
    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/yujiannn/ssdlabtest.git'
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                dir('flask') {
                    sh 'python3 -m venv venv'
                }
            }
        }
        
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                dir('flask') {
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        
        stage('UI Testing') {
            steps {
                dir('flask') {
                    script {
                        // Debugging: Check the current directory and list contents
                        sh 'pwd'
                        sh 'ls -la'
                        // Activate the virtual environment and start the Flask app
                        sh '. venv/bin/activate && FLASK_APP=$FLASK_APP flask run &'
                        // Give the server a moment to start
                        sh 'sleep 5'
                        // Debugging: Check if the Flask app is running
                        sh 'curl -s http://127.0.0.1:5000 || echo "Flask app did not start"'
                        
                        // Test a strong password
                        sh '''
                        curl -s -X POST -F "password=StrongPass123" http://127.0.0.1:5000 | grep "Welcome"
                        '''
                        
                        // Test a weak password
                        sh '''
                        curl -s -X POST -F "password=password" http://127.0.0.1:5000 | grep "Password does not meet the requirements"
                        '''
                        
                        // Stop the Flask app
                        sh 'pkill -f "flask run"'
                    }
                }
            }
        }
        
        stage('Integration Testing') {
            steps {
                dir('flask') {
                    sh '. venv/bin/activate && pytest --junitxml=integration-test-results.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('flask') {
                    sh 'docker build -t flask-app .'
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    dir('flask') {
                        sh '''
                        ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=flask-app \
                        -Dsonar.sources=. \
                        -Dsonar.inclusions=app.py \
                        -Dsonar.host.url=http://sonarqube:9000 \
                        -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                }
            }
        }
        
        stage('Deploy Flask App') {
            steps {
                script {
                    echo 'Deploying Flask App...'
                    // Stop any running container on port 5000
                    sh 'docker ps --filter publish=5000 --format "{{.ID}}" | xargs -r docker stop'
                    // Remove the stopped container
                    sh 'docker ps -a --filter status=exited --filter publish=5000 --format "{{.ID}}" | xargs -r docker rm'
                    // Run the new Flask app container
                    sh 'docker run -d -p 5000:5000 flask-app'
                    sh 'sleep 10'
                }
            }
        }
    }
    
    post {
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
        always {
            archiveArtifacts artifacts: 'flask/integration-test-results.xml', allowEmptyArchive: true
        }
    }
}
