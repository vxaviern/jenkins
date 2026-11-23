
pipeline {
    agent any

    // 1. Environment variables
    environment {
        APP_NAME = 'myapp'
        APP_PORT = '8081'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    def scmInfo = checkout scm

                    def commitId = scmInfo.GIT_COMMIT

                    if (!commitId) {
                        error('Git commit ID is missing')
                    }

                    env.GIT_SHA_TAG = commitId.substring(0, 12)

                    echo "Full Git commit: ${commitId}"
                    echo "Docker image tag: ${env.GIT_SHA_TAG}"
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
                echo "Building ${env.APP_NAME}:${env.GIT_SHA_TAG}"

                bat 'docker build -t %APP_NAME%:%GIT_SHA_TAG% .'
            }
        }

        // 4. Manual approval
        stage('Approval') {
            // when {
            //     expression {
            //         env.BRANCH_NAME == 'main' ||
            //         env.GIT_BRANCH == 'origin/main'
            //     }
            // }

            steps {
                input message: 'Approve deployment to local Docker?', 
                      ok: 'Deploy'
            }
        }

        // 5. Deploy using Jenkins credentials
        stage('Deploy') {
            // when {
            //     expression {
            //         return env.GIT_BRANCH == 'origin/main' ||
            //                env.GIT_BRANCH == 'main'
            //     }
            // }

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
                             %APP_NAME%:%GIT_SHA_TAG%
                    '''
                }
            }
        }

        stage('Health Check') {
            // when {
            //     expression {
            //         return env.GIT_BRANCH == 'origin/main' ||
            //                env.GIT_BRANCH == 'main'
            //     }
            // }

            steps {
                bat '''
                    timeout /t 5 /nobreak >NUL
                    curl.exe -f http://localhost:8081/
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }

        success {
            echo "Deployment successful: ${env.APP_NAME}:${env.GIT_SHA_TAG}"
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
