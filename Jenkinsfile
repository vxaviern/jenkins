pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat 'python test_app.py'
            }
        }

        stage('Validate') {
            steps {
                bat 'python -m py_compile app.py'
                echo 'Validation successful'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                bat '''
                    docker rm -f myapp || true
                    docker run -d \
                        --name myapp \
                        -p 8081:8080 \
                        myapp:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                bat 'curl -f http://localhost:8081'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}