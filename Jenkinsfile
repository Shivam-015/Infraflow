pipeline {

    agent any

    environment {
        NOTIFICATION_EMAIL = credentials('NOTIFICATION_EMAIL')
    }

    stages {

        stage("code clone") {
            steps {
                git url: "https://github.com/Shivam-015/Infraflow.git", branch: "main"
            }
        }

        stage("build") {
            steps {
                sh "docker build -t infraflow-app:latest ./app"
            }
        }

        stage("Run Automated Unit Tests") {
            steps {
                sh '''
                    docker compose up -d mysql

                    echo "Waiting for MySQL..."

                    sleep 30

                    docker run --rm \
                        --network infraflow_default \
                        -e SECRET_KEY="django-insecure-test-key" \
                        -e DEBUG="True" \
                        -e DB_NAME="cloudarc" \
                        -e DB_USER="admin" \
                        -e DB_PASSWORD="admin" \
                        -e DB_HOST="mysql" \
                        -e DB_PORT="3306" \
                        infraflow-app:latest \
                        python manage.py test
                '''
            }

            post {
                always {
                    sh 'docker compose down || true'
                }
            }
        }

        stage("push to docker Hub") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "dockerhubcred",
                        passwordVariable: "dockerhubPass",
                        usernameVariable: "dockerhubUser"
                    )
                ]) {

                    sh "docker login -u ${env.dockerhubUser} -p ${dockerhubPass}"

                    sh "docker image tag infraflow-app ${env.dockerhubUser}/infraflow-app"

                    sh "docker push ${env.dockerhubUser}/infraflow-app:latest"
                }
            }
        }
    }

    post {

        success {
            emailext(
                subject: "Build Successful",
                body: "Good News: Your build was successful!",
                to: '${env.NOTIFICATION_EMAIL}'
            )
        }

        failure {
            emailext(
                subject: "Build Failed",
                body: "Bad News: Your build was Failed!",
                to: '${env.NOTIFICATION_EMAIL}'
            )
        }
    }
}