pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                userRemoteConfigs: [[url: 'https://github.com/motorfireman/Test.git']]])
            }
        }
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        stage('Clone Repository') {
            steps {
                script {
                    dir('workspace') {
                        git url: 'https://github.com/motorfireman/Test.git', branch: 'main'
                    }
                }
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                script {
                    sh 'bash -c "python3 -m venv venv"'
                }
            }
        }
        stage('Install dependencies') {
            steps {
                script {
                    sh 'bash -c "venv/bin/pip install -r requirements.txt"'
                }
            }
        }
        stage('Dependency Check') {
            steps {
                script {
                    sh 'bash -c "venv/bin/pip check"'
                }
            }
        }
        stage('UI Testing') {
            steps {
                script {
                    sh 'bash -c "venv/bin/python run_tests.py"'
                }
            }
        }
        stage('Deploy Flask App') {
            steps {
                script {
                    sh 'bash -c "venv/bin/python app.py"'
                }
            }
        }
    }
    post {
        always {
            script {
                echo 'Cleaning up...'
                dir('workspace') {
                    sh 'rm -rf venv'
                }
            }
        }
    }
}
