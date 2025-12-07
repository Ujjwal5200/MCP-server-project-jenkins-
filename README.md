# MCP AI Assistant

A powerful AI assistant application built with Streamlit, LangGraph, and Google Gemini, featuring an MCP (Model Context Protocol) server that provides specialized tools for math operations and code generation.

## 🚀 Features

- **Interactive Chat Interface**: User-friendly Streamlit-based chat application for natural language interactions
- **MCP Server Integration**: Custom MCP server with specialized tools for enhanced AI capabilities
- **Math Operations**: Built-in tools for addition, subtraction, multiplication, and division
- **Code Generation**: Advanced Python and web development code generation powered by Google Gemini
- **LangGraph Workflow**: Orchestrates AI model calls and tool executions using LangGraph
- **Google Gemini Integration**: Leverages Gemini 2.5 Flash Lite for high-quality AI responses
- **Asynchronous Processing**: Efficient handling of concurrent operations using asyncio

## 🏗️ Architecture

The application consists of three main components:

### 1. Streamlit App (`app.py`)
- Frontend chat interface
- Manages user interactions and displays conversation history
- Integrates with LangGraph for AI processing
- Custom CSS styling for enhanced user experience

### 2. MCP Server (`MCP_server.py`)
- FastMCP-based server providing specialized tools
- Math tools: `add`, `sub`, `mul`, `div`
- Code generation tools: `code_generation`, `webcode_generation`
- General query handling with `normal_query`

### 3. LangGraph Client (`client_langraph.py`)
- Standalone client demonstrating MCP server integration
- Shows how to set up and use the MCP tools with LangGraph
- Example usage for testing and development

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Required Python packages (see Dependencies section)

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

## 💡 Examples

### Math Operations
- "What is 15 + 27?"
- "Calculate 100 divided by 5"
- "Multiply 8 by 9"

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

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
