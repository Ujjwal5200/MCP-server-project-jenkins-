pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_USER = "ubuntu"
        APP_HOST = "172.31.25.217"
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

        stage('Deploy to App EC2') {
            steps {
                withCredentials([
                    string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')
                ]) {
                    sshagent(['APP_EC2_SSH']) {
                       sh '''
ssh -o StrictHostKeyChecking=no ${APP_USER}@${APP_HOST} <<EOF
set -euxo pipefail

mkdir -p ${APP_DIR}
cd ${APP_DIR}

if [ ! -d .git ]; then
    git clone https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git .
else
    git fetch origin
    git reset --hard origin/main
fi

cat > .env <<ENV
GEMINI_API_KEY=${GEMINI_API_KEY}
GOOGLE_API_KEY=${GEMINI_API_KEY}
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
'''

                    }
                }
            }
        }
    }
}
