
pipeline {
    agent any

    // 1. Environment variables
    environment {
        APP_NAME = 'myapp'
        IMAGE_TAG = ''
        APP_PORT = '8081'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {

        // Explicit checkout from Git
        stage('Checkout') {
            steps {
                checkout scm

                // 2. Script: calculate Git commit SHA
                script {
                    env.IMAGE_TAG = bat(
                        returnStdout: true,
                        script: '@git rev-parse --short=12 HEAD'
                    ).trim()

                    echo "Building image: ${env.APP_NAME}:${env.IMAGE_TAG}"
                }
            }
        }

        // 3. Parallel execution
        stage('Test and Validate') {
            parallel {

                stage('Unit Tests') {
                    steps {
                        bat 'python test_app.py'
                    }
                }

                stage('Python Validation') {
                    steps {
                        bat 'python -m py_compile app.py test_app.py'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %APP_NAME%:%IMAGE_TAG% .'
            }
        }

        // 4. Manual approval
        stage('Approval') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/main' ||
                           env.GIT_BRANCH == 'main'
                }
            }

            steps {
                input message: 'Approve deployment to local Docker?', 
                      ok: 'Deploy'
            }
        }

        // 5. Deploy using Jenkins credentials
        stage('Deploy') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/main' ||
                           env.GIT_BRANCH == 'main'
                }
            }

            steps {
                withCredentials([
                    string(
                        credentialsId: 'local-app-secret',
                        variable: 'APP_SECRET'
                    )
                ]) {
                    bat '''
                        docker rm -f myapp >NUL 2>&1 || exit /b 0

                        docker run -d ^
                            --name myapp ^
                            -p 8081:8080 ^
                            -e APP_SECRET ^
                            %APP_NAME%:%IMAGE_TAG%
                    '''
                }
            }
        }

        stage('Health Check') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/main' ||
                           env.GIT_BRANCH == 'main'
                }
            }

            steps {
                bat '''
                    timeout /t 5 /nobreak >NUL
                    curl.exe -f http://localhost:8081/
                '''
            }
        }
    }

    // 6. Post-build actions
    post {
        always {
            echo 'Pipeline execution finished.'
        }

        success {
            echo "Deployment successful: ${env.APP_NAME}:${env.IMAGE_TAG}"
        }

        failure {
            echo 'Pipeline failed. Check the failed stage.'
        }
    }
}
