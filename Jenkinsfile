pipeline {
    agent any

    environment {
        FLASK_APP = 'flask/app.py'
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

        stage('Build Docker Image') {
            steps {
                dir('flask') {
                    sh 'docker build -t flask-app .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop any running container on port 5000
                    sh 'docker ps --filter publish=5000 --format "{{.ID}}" | xargs -r docker stop'
                    // Remove the stopped container
                    sh 'docker ps -a --filter status=exited --filter publish=5000 --format "{{.ID}}" | xargs -r docker rm'
                    // Run the new Flask app container
                    sh 'docker run -d --name flask_container -p 5000:5000 flask-app'
                    sleep 10 // Allow time for the Flask app to start
                    sh 'docker logs flask_container' // Check container logs
                }
            }
        }

        stage('UI Testing') {
            steps {
                script {
                    // Test application
                    sh 'curl -s http://localhost:5000 || echo "Flask app did not start"'
                    // Test a strong password
                    sh '''
                    curl -s -X POST -F "password=StrongPass123" http://localhost:5000 | grep "Welcome"
                    '''
                    // Test a weak password
                    sh '''
                    curl -s -X POST -F "password=password" http://localhost:5000 | grep "Password does not meet the requirements"
                    '''
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
                    // Additional deployment steps if necessary
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
        cleanup {
            // Cleanup the Docker container
            sh 'docker stop flask_container || true'
            sh 'docker rm flask_container || true'
        }
    }
}
