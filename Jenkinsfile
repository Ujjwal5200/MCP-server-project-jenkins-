pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Install Docker if needed') {
            steps {
                sh '''
                if ! command -v docker >/dev/null 2>&1; then
                  echo "Docker not found, installing..."
                  sudo apt-get update -y
                  sudo apt-get install -y docker.io
                  sudo systemctl enable docker || true
                  sudo systemctl start docker || true
                else
                  echo "Docker already installed"
                fi
                '''
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git'
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t mcp-streamlit-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                # Stop and remove old container if exists
                docker rm -f mcp-streamlit-app || true

                # Run new container
                docker run -d \
                  --name mcp-streamlit-app \
                  -p 8501:8501 \
                  -e google_api_key=$GEMINI_API_KEY \
                  mcp-streamlit-app
                '''
            }
        }
    }
}

