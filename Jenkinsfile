pipeline{
    agent any;
    stages{
        stage("code clone"){
            steps{
                git url: "https://github.com/Shivam-015/Infraflow.git" ,branch:"main"
            }
        }
        
        stage("build"){
            steps{
                sh "docker build -t infraflow-app ."
            }
        }
        
        stage("test"){
            steps{
                echo "test"
            }
        }
        stage ("push to docker Hub"){
            steps{
                withCredentials([usernamePassword(
                    credentialsId:"dockerhubcred",
                    passwordVariable:"dockerhubPass",
                    usernameVariable:"dockerhubUser"
                    )]){
                    
                    sh "docker login -u ${env.dockerhubUser} -p ${dockerhubPass}"
                    sh "docker image tag infraflow-app ${env.dockerhubUser}/infraflow-app"
                    sh "docker push  ${env.dockerhubUser}/infraflow-app:latest"
                }
            }
        }
    }

post {
    success {
        emailext(
            subject:"Build Successful",
            body: "Good News: Your build was successful!",
            to: ''
        )
    }
    failure{
        emailext(
            subject:"Build Failed",
            body: "Bad News: Your build was Failed!",
            to: ''
        )  
    }
}    
}