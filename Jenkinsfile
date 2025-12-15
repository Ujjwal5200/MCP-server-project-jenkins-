pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        APP_HOST = "<APP_PRIVATE_IP>"
        APP_USER = "ubuntu"
        APP_DIR  = "/home/ubuntu/mcp-app"

        IMAGE    = "mcp-streamlit-app"
        CONTAINER = "mcp-app"
        PORT     = "8501"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Deploy to App EC2') {
            steps {
                withCredentials([
                    string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')
                ]) {
                    sshagent(['APP_EC2_SSH']) {
                        sh '''
                        set -e

                        ssh -o StrictHostKeyChecking=no ${APP_USER}@${APP_HOST} << 'EOF'
                        set -euxo pipefail

                        echo "=== System Info ==="
                        free -h || true
                        df -h || true

                        echo "=== Preparing app directory ==="
                        mkdir -p ${APP_DIR}
                        cd ${APP_DIR}

                        echo "=== Syncing repo ==="
                        if [ ! -d .git ]; then
                          git clone https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git .
                        else
                          git fetch origin
                          git reset --hard origin/main
                        fi

                        echo "=== Writing env file ==="
                        cat > .env << ENV
GEMINI_API_KEY=${GEMINI_API_KEY}
ENV

                        echo "=== Stopping old container ==="
                        docker stop ${CONTAINER} || true
                        docker rm ${CONTAINER} || true

                        echo "=== Cleaning unused images ==="
                        docker image prune -af || true

                        echo "=== Building image (on APP EC2) ==="
                        docker build --no-cache -t ${IMAGE} .

                        echo "=== Running container ==="
                        docker run -d \
                          --name ${CONTAINER} \
                          --env-file .env \
                          -p 80:${PORT} \
                          --restart unless-stopped \
                          ${IMAGE}

                        echo "=== Running containers ==="
                        docker ps

                        EOF
                        '''
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
            echo "❌ Deployment failed — check logs carefully"
        }
        always {
            cleanWs()
        }
    }
}
