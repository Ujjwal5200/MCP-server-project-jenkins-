# NEXUS AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

A powerful AI assistant application built with Streamlit, LangGraph, and Google Gemini, featuring an MCP (Model Context Protocol) server that provides specialized tools for math operations and code generation. This project is built and managed using Jenkins with GitHub CI/CD for automated testing, building, and deployment.

## 🚀 Features

- **Interactive Chat Interface**: User-friendly Streamlit-based chat application for natural language interactions
- **MCP Server Integration**: Custom MCP server with specialized tools for enhanced AI capabilities
- **Math Operations**: Built-in tools for addition, subtraction, multiplication, and division
- **Code Generation**: Advanced Python and web development code generation powered by Google Gemini
- **LangGraph Workflow**: Orchestrates AI model calls and tool executions using LangGraph
- **Google Gemini Integration**: Leverages Gemini 2.5 Flash Lite for high-quality AI responses
- **Asynchronous Processing**: Efficient handling of concurrent operations using asyncio
- **Customizable Themes**: Dark and light themes with futuristic UI animations
- **Docker Support**: Containerized deployment for easy scalability
- **CI/CD Pipeline**: Automated build and deployment via Jenkins and GitHub Actions
- **AWS Hosting**: Deployed on Amazon Web Services for scalable and reliable cloud infrastructure

## 🏗️ Architecture

The MCP AI Assistant follows a modular, microservices-inspired architecture designed for scalability, maintainability, and seamless AI integration. The system employs a layered approach that separates concerns between user interface, business logic orchestration, and external service integrations.

### System Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │◄──►│  LangGraph       │◄──►│   MCP Server    │
│   (Frontend)    │    │  Orchestrator    │    │   (Tools)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────────┐
                    │  Google Gemini AI   │
                    │     (LLM Model)     │
                    └─────────────────────┘
```

### Core Components

#### 1. Streamlit Frontend (`app.py`)
- **Role**: User interface and interaction management
- **Features**:
  - Responsive chat interface with dark/light theme support
  - Real-time message handling with asynchronous processing
  - Custom CSS animations and particle effects for enhanced UX
  - Session state management for conversation persistence
  - Mobile-first responsive design with adaptive layouts

#### 2. LangGraph Orchestrator (`client_langraph.py`)
- **Role**: Workflow engine and AI model coordination
- **Features**:
  - Graph-based state management for complex conversation flows
  - Conditional routing between direct AI responses and tool execution
  - Asynchronous processing with asyncio for concurrent operations
  - Tool binding and execution orchestration
  - Error handling and retry logic for robust operation

#### 3. MCP Server (`MCP_server.py`)
- **Role**: Specialized tool provider using Model Context Protocol
- **Tools Available**:
  - **Math Operations**: `add`, `subtract`, `multiply`, `divide` - Precise arithmetic calculations
  - **Code Generation**: `code_generation` (Python), `webcode_generation` (HTML/CSS/JS) - AI-powered code creation with comments and imports
  - **General Queries**: `normal_query` - Fallback for non-specialized conversations
- **Features**:
  - FastMCP framework for efficient tool execution
  - Input validation and error handling
  - Asynchronous tool processing for performance

#### 4. Google Gemini Integration
- **Role**: Large Language Model backend
- **Configuration**:
  - Gemini 2.5 Flash Lite model for optimal performance/cost balance
  - Configurable temperature, token limits, and retry mechanisms
  - Secure API key management via environment variables

### Data Flow

1. **User Input** → Streamlit UI captures and displays messages
2. **Processing** → LangGraph evaluates context and determines tool needs
3. **Tool Execution** → MCP Server provides specialized capabilities when required
4. **AI Response** → Google Gemini generates contextual responses
5. **Output** → Results flow back through LangGraph to Streamlit for display

### CI/CD and Deployment Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   GitHub    │────►│   Jenkins   │────►│  Docker Registry │────►│     AWS     │
│ Repository  │     │   Pipeline  │     │                 │     │ Deployment  │
└─────────────┘     └─────────────┘     └─────────────────┘     └─────────────┘
       ▲                   │                       │                       │
       │                   ▼                       ▼                       ▼
       └─────────── Test Results ────────── Build Artifacts ──────── Production ───────
```

### Deployment Architecture

- **Containerization**: Docker-based deployment for consistent environments across development, staging, and production
- **CI/CD Pipeline**:
  - **Jenkins**: Orchestrates the entire CI/CD process with automated triggers from GitHub
  - **GitHub Integration**: Webhooks trigger Jenkins pipelines on code pushes and pull requests
  - **Automated Testing**: Unit tests, integration tests, and security scans run in isolated containers
  - **Build Process**: Docker images are built, tagged, and pushed to secure registry
  - **Deployment**: Automated rollout to AWS with blue-green deployment strategy
- **AWS Infrastructure**:
  - **ECS/ECR**: Container orchestration and registry for scalable container management
  - **Load Balancing**: Application Load Balancer distributes traffic across multiple instances
  - **Auto Scaling**: EC2 Auto Scaling groups ensure high availability and cost optimization
  - **RDS**: Managed database services for data persistence (if needed)
  - **CloudWatch**: Monitoring and logging for performance metrics and alerts
  - **VPC**: Secure network isolation with proper security groups and subnets
- **Environment Management**: Secure configuration using AWS Systems Manager Parameter Store and `.env` files
- **Security**: IAM roles, encrypted secrets, and compliance with AWS security best practices

## 📋 Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- Google Gemini API key

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MCP_STREAMLIT
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Setup

1. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```
   google_api_key=your_google_gemini_api_key_here
   ```

2. **API Key Setup:**
   - Obtain a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add the key to your `.env` file

## 🚀 Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

This will start the web application at `http://localhost:8501`.

### Using the MCP Server Directly

```bash
python MCP_server.py
```

### Testing with the Client Script

```bash
python client_langraph.py
```

### Docker Deployment

Build and run the application using Docker:

```bash
docker build -t mcp-ai-assistant .
docker run -p 8501:8501 --env-file .env mcp-ai-assistant
```

## 🔄 CI/CD Pipeline

This project utilizes Jenkins integrated with GitHub for continuous integration and deployment:

- **Automated Testing**: Jenkins runs unit tests and integration tests on every push to the main branch
- **Build Process**: Docker images are built and pushed to a container registry
- **Deployment**: Automated deployment to staging and production environments
- **Monitoring**: Pipeline status and logs are monitored via Jenkins dashboard

To set up the CI/CD pipeline:
1. Configure Jenkins with GitHub webhooks for automatic triggering
2. Set up necessary credentials and environment variables in Jenkins
3. Use the provided Jenkinsfile for pipeline configuration

## 💡 Examples

### Math Operations
- "What is 15 + 27?"
- "Calculate 100 divided by 5"
- "Multiply 8 by 9 " 

### Code Generation
- "Generate a Python function to sort a list"
- "Create a Flask web application for a blog"
- "Write HTML and CSS for a responsive navigation bar"

### General Queries
- "Explain how recursion works in programming"
- "What are the benefits of using virtual environments?"

## 📦 Dependencies

- `streamlit`: Web application framework
- `langchain-google-genai`: Google Gemini integration
- `langchain-mcp-adapters`: MCP client adapters
- `langgraph`: Workflow orchestration
- `python-dotenv`: Environment variable management
- `mcp`: Model Context Protocol library
- `nest-asyncio`: Asyncio compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- LangChain and LangGraph for orchestration
- Streamlit for the web interface
- MCP community for the protocol specification
- Jenkins and GitHub for CI/CD infrastructure

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
