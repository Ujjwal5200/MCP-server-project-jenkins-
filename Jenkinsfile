pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_HOST = "<APP_PRIVATE_IP>"     
        APP_USER = "ubuntu" 
        APP_DIR  = "/home/ubuntu/mcp-app"
        IMAGE    = "mcp-streamlit-app"
        CONTAINER = "mcp-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Jenkins Environment') {
            steps {
                sh '''
                  echo "Running on Jenkins node"
                  whoami
                  java -version
                '''
            }
        }

        stage('Deploy to App EC2') {
            steps {
                withCredentials([
                    string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')
                ]) {
                    sshagent(['APP_EC2_SSH']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${APP_USER}@${APP_HOST} << 'EOF'
                        set -euxo pipefail

                        echo "== System check =="
                        free -h
                        docker --version

                        echo "== App directory =="
                        mkdir -p ${APP_DIR}
                        cd ${APP_DIR}

                        echo "== Git sync =="
                        if [ ! -d .git ]; then
                            git clone https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git .
                        else
                            git fetch origin
                            git reset --hard origin/main
                        fi

                        echo "== Writing env =="
                        cat > .env << ENV
GOOGLE_API_KEY=${GEMINI_API_KEY}
GEMINI_API_KEY=${GEMINI_API_KEY}
ENV

                        echo "== Docker cleanup =="
                        docker stop ${CONTAINER} || true
                        docker rm ${CONTAINER} || true

                        echo "== Docker build =="
                        docker build -t ${IMAGE}:latest .

                        echo "== Docker run =="
                        docker run -d \\
                          --name ${CONTAINER} \\
                          --env-file .env \\
                          -p 80:8501 \\
                          --restart unless-stopped \\
                          ${IMAGE}:latest

                        echo "== Deployment complete =="
                        docker ps | grep ${CONTAINER}
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful"
        }
        failure {
            echo "❌ Deployment failed — check console logs ABOVE"
        }
        always {
            cleanWs()
        }
    }
}
