import streamlit as st
import asyncio
import nest_asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

import os
from dotenv import load_dotenv

nest_asyncio.apply()


# Theme configuration
THEMES = {
    "dark": {
        "bg": "#0a0a0a",
        "secondary_bg": "#1a1a1a",
        "text": "#ffffff",
        "accent": "#00ffff",
        "border": "#333333",
        "glow": "0 0 10px #00ffff",
    },
    "light": {
        "bg": "#ffffff",
        "secondary_bg": "#f0f0f0",
        "text": "#000000",
        "accent": "#0066cc",
        "border": "#cccccc",
        "glow": "0 0 10px #0066cc",
    },
}

load_dotenv()
api_key = os.getenv("google_api_key")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

async def setup_graph():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["MCP_server.py"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    model_with_tools = model.bind_tools(tools)
    tool_node = ToolNode(tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tool_node"
        return END

    def call_model(state: MessagesState):
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tool_node", tool_node)
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", should_continue)
    builder.add_edge("tool_node", "call_model")
    graph = builder.compile()
    return graph

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Get current theme
current_theme = THEMES[st.session_state.theme]

# Custom CSS for better styling with themes and animations
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    * {{
        font-family: 'Roboto Mono', monospace;
    }}

    .main {{
        background-color: {current_theme['bg']};
        color: {current_theme['text']};
        transition: background-color 0.5s ease, color 0.5s ease;
    }}

    .stChatMessage {{
        border-radius: 15px;
        margin: 10px 0;
        padding: 15px;
        background-color: {current_theme['secondary_bg']};
        border: 1px solid {current_theme['border']};
        box-shadow: {current_theme['glow']};
        animation: fadeIn 0.5s ease-in;
        transition: all 0.3s ease;
    }}

    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px {current_theme['accent']}40;
    }}

    .stChatInput {{
        border-radius: 25px;
        border: 2px solid {current_theme['accent']};
        background-color: {current_theme['secondary_bg']};
        color: {current_theme['text']};
        transition: all 0.3s ease;
    }}

    .stChatInput:focus {{
        box-shadow: {current_theme['glow']};
        border-color: {current_theme['accent']};
    }}

    .sidebar .sidebar-content {{
        background-color: {current_theme['secondary_bg']};
        color: {current_theme['text']};
        border-right: 2px solid {current_theme['accent']};
        box-shadow: inset 0 0 10px {current_theme['accent']}20;
    }}

    .stButton>button {{
        background-color: {current_theme['accent']};
        color: {current_theme['bg']};
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: {current_theme['glow']};
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px {current_theme['accent']};
    }}

    .stSpinner {{
        animation: spin 1s linear infinite;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* Particle effect for futuristic look */
    .particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }}

    .particle {{
        position: absolute;
        background-color: {current_theme['accent']};
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); opacity: 0.5; }}
        50% {{ transform: translateY(-20px) rotate(180deg); opacity: 1; }}
    }}

    /* Responsive design */
    @media (max-width: 768px) {{
        .stChatMessage {{
            margin: 5px;
            padding: 10px;
            font-size: 14px;
        }}
        .sidebar .sidebar-content {{
            width: 200px !important;
        }}
        .main {{
            padding: 10px;
        }}
        .particles {{
            display: none; /* Hide particles on mobile for performance */
        }}
    }}

    @media (max-width: 480px) {{
        .stChatMessage {{
            margin: 2px;
            padding: 8px;
            font-size: 12px;
        }}
        .stChatInput {{
            font-size: 14px;
        }}
        .stButton>button {{
            font-size: 12px;
            padding: 8px 16px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Add particle effect
st.markdown("""
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 7s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 8s;"></div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖  AI Assistant")
    st.markdown("An AI assistant powered by LangGraph and Google Gemini, integrated with MCP tools.")
    st.markdown("---")
    # Theme toggle
    theme_options = ["dark", "light"]
    selected_theme = st.selectbox("Choose Theme", theme_options, index=theme_options.index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.graph = None
        st.rerun()
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("- Chat with AI using natural language")
    st.markdown("- Access to MCP tools for enhanced capabilities")
    st.markdown("- CICD and managed by Jenkins")
    st.markdown("- Powered by Gemini 2.5 Flash & AWS")
    st.markdown("- MADE BY UJJWAL KAUSHIK")

st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 3em; font-weight: bold; color: #00ffff; text-shadow: 0 0 20px #00ffff; animation: glow 2s ease-in-out infinite alternate;">
        NEXUS
    </h1>
    <p style="font-size: 1.2em; color: #ffffff; opacity: 0.8;">Futuristic AI Assistant</p>
</div>
""", unsafe_allow_html=True)

# Add glow animation for the title
st.markdown("""
<style>
@keyframes glow {
    from { text-shadow: 0 0 20px #00ffff; }
    to { text-shadow: 0 0 30px #00ffff, 0 0 40px #00ffff; }
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    st.session_state.graph = None

# Welcome message if no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h3>Welcome to nexus, your AI assistant! 👋</h3>
        <p>Start a conversation by typing a message below. I can help with various tasks using integrated MCP tools .</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user", avatar="👤").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant", avatar="🤖").write(msg.content)

# Input for new query
query = st.chat_input("Enter your query:")

if query:
    # Add user message
    user_msg = HumanMessage(content=query)
    st.session_state.messages.append(user_msg)
    st.chat_message("user").write(query)

    # Setup graph if not done
    if st.session_state.graph is None:
        st.session_state.graph = asyncio.run(setup_graph())

    # Process query
    with st.spinner("Processing..."):
        result = asyncio.run(st.session_state.graph.ainvoke({"messages": st.session_state.messages}))
        ai_response = result["messages"][-1]
        st.session_state.messages.append(ai_response)
        st.chat_message("assistant").write(ai_response.content)
        st.rerun()
