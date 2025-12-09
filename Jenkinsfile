pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Ujjwal5200/MCP-server-project-jenkins-.git'
            }
        }

        stage('Build & Deploy Docker') {
            steps {
                withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')]) {
                    sh '''
                        echo "=== Creating .env for app ==="
                        cat > .env <<EOF
GOOGLE_API_KEY=${GEMINI_API_KEY}
GEMINI_API_KEY=${GEMINI_API_KEY}
EOF

                        echo "=== Building Docker image ==="
                        docker build -t mcp-streamlit-app .

                        echo "=== Stopping old container (if exists) ==="
                        docker stop mcp-streamlit-app || true
                        docker rm mcp-streamlit-app || true

                        echo "=== Running new container ==="
                        docker run -d --name mcp-streamlit-app \
                          -p 80:8501 \
                          --env-file .env \
                          mcp-streamlit-app
                    '''
                }
            }
        }
    }
}
