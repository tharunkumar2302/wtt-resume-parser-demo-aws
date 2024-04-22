pipeline {
    agent any
    tools {
   Docker 'Docker'
}
    
    environment {
        DOCKER_IMAGE_NAME = 'my-jenkins-image'
        DOCKER_CONTAINER_NAME = 'my-jenkins-container'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}", "-f /wtt-resume-parser-demo-aws/pms/Dockerfile .")
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    docker.run("-d --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }
    }
    
}
