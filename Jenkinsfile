pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_HOST  = "<APP_PRIVATE_IP>"   // e.g. 10.0.1.15
        APP_USER  = "ubuntu"
        APP_DIR   = "/home/ubuntu/mcp-app"
        IMAGE     = "mcp-streamlit-app"
        CONTAINER = "mcp-app"
        REPO_URL  = "https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git"
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
                whoami
                java -version
                docker --version || true
                '''
            }
        }

        stage('Deploy to App EC2') {
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
#!/usr/bin/env bash
set -euxo pipefail

chmod 600 "$SSH_KEY"

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$APP_HOST" << 'EOF'
#!/usr/bin/env bash
set -euxo pipefail

echo "== System check =="
whoami
free -h
docker --version

echo "== App directory =="
mkdir -p /home/ubuntu/mcp-app
cd /home/ubuntu/mcp-app

echo "== Git sync =="
if [ ! -d .git ]; then
  git clone https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git .
else
  git fetch origin
  git reset --hard origin/main
fi

echo "== Writing env file =="
cat > .env << 'ENV'
GOOGLE_API_KEY=$GEMINI_API_KEY
GEMINI_API_KEY=$GEMINI_API_KEY
ENV

echo "== Docker cleanup =="
docker stop mcp-app || true
docker rm mcp-app || true

echo "== Docker build =="
docker build -t mcp-streamlit-app:latest .

echo "== Docker run =="
docker run -d \
  --name mcp-app \
  --env-file .env \
  -p 80:8501 \
  --restart unless-stopped \
  mcp-streamlit-app:latest

echo "== Running containers =="
docker ps | grep mcp-app
EOF
'''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful"
        }
        failure {
            echo "❌ Deployment failed — check logs above"
        }
        always {
            cleanWs()
        }
    }
}
