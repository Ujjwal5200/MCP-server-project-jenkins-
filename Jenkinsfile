pipeline {
    agent any

    environment {
        APP_HOST = "<APP_PRIVATE_IP>"
        APP_DIR  = "/home/ubuntu/app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git'
            }
        }

        stage('Deploy to App EC2') {
            steps {
                sshagent(['APP_EC2_SSH']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_HOST} '
                        set -e
                        mkdir -p ${APP_DIR}
                        cd ${APP_DIR}

                        if [ ! -d .git ]; then
                            git clone https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git .
                        else
                            git pull origin main
                        fi

                        echo "GOOGLE_API_KEY=${GEMINI_API_KEY}" > .env
                        echo "GEMINI_API_KEY=${GEMINI_API_KEY}" >> .env

                        docker stop mcp-app || true
                        docker rm mcp-app || true

                        docker build -t mcp-app .
                        docker run -d --name mcp-app \
                          --env-file .env \
                          -p 80:8501 mcp-app
                    '
                    """
                }
            }
        }
    }
}
