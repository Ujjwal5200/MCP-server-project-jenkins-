import streamlit as st
import asyncio
from langchain_mcp_adapters import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("google_api_key")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
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

    async def call_model(state: MessagesState):
        messages = state["messages"]
        response = await model_with_tools.ainvoke(messages)
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tool_node", tool_node)
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", should_continue)
    builder.add_edge("tool_node", "call_model")
    graph = builder.compile()
    return graph

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stChatMessage {
        border-radius: 10px;
        margin: 5px 0;
    }
    .stChatInput {
        border-radius: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 MCP AI Assistant")
    st.markdown("An AI assistant powered by LangGraph and Google Gemini, integrated with MCP tools.")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.graph = None
        st.rerun()
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("- Chat with AI using natural language")
    st.markdown("- Access to MCP tools for enhanced capabilities")
    st.markdown("- Powered by Gemini 2.5 Flash")

st.title("💬 MCP AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    st.session_state.graph = None

# Welcome message if no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>Welcome to MCP AI Assistant! 👋</h2>
        <p>Start a conversation by typing a message below. I can help with various tasks using integrated tools.</p>
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
