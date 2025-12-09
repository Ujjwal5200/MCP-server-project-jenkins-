pipeline {
    agent any

    // Load Gemini key from Jenkins Credentials
    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                // Use your repo URL
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
