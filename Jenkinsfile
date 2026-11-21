pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                bat 'docker build -t myapp:latest .'
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                    docker rm -f myapp || true
                    docker run -d \
                        --name myapp \
                        -p 8081:8080 \
                        myapp:latest
                '''
            }
        }

        stage('Verify') {
            steps {
                bat 'curl -f http://localhost:8081'
            }
        }
    }
}