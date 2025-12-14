pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_HOST  = "<APP_PRIVATE_IP>"
        APP_USER  = "ubuntu"
        APP_DIR   = "/home/ubuntu/mcp-app"
        IMAGE     = "mcp-streamlit-app:latest"
        CONTAINER = "mcp-app"
        REPO_URL  = "https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([
                    string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY'),
                    sshUserPrivateKey(
                        credentialsId: 'APP_EC2_SSH',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                   sh '''
bash << 'SCRIPT'
set -euo pipefail

chmod 600 "$SSH_KEY"

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$APP_HOST" << 'EOF'
set -euo pipefail

mkdir -p ${APP_DIR}
cd ${APP_DIR}

if [ ! -d .git ]; then
  git clone ${REPO_URL} .
else
  git fetch origin
  git reset --hard origin/main
fi

cat > .env << ENV
GOOGLE_API_KEY=${GEMINI_API_KEY}
GEMINI_API_KEY=${GEMINI_API_KEY}
ENV

docker stop ${CONTAINER} || true
docker rm ${CONTAINER} || true
docker build -t ${IMAGE} .
docker run -d \
  --name ${CONTAINER} \
  --env-file .env \
  -p 80:8501 \
  --restart unless-stopped \
  ${IMAGE}

docker ps | grep ${CONTAINER}
EOF
SCRIPT
'''
                }
            }
        }
    }

    post {
        success { echo "✅ Deployment successful" }
        failure { echo "❌ Deployment failed" }
        always  { cleanWs() }
    }
}
