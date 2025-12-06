import asyncio
from langchain_mcp_adapters import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import tool_node, ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv



#lode model 

load_dotenv()
api_key=os.getenv("google_api_key")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

async def main():
    # setup mcp client
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                # pull path to mcp_server.py
                "args":["MCP_server.py"],
                "transport":"stdio",
            }
        }
    )

    tools = await client.get_tools()
    model_with_tools=model.bind_tools(tools)
    tool_node=ToolNode(tools)

    def should_continue(state:MessagesState):
        messages=state["messages"]
        last_message=messages[-1]
        if last_message.tool_calls:
            return "tool_node"
        return END

    async def call_model(state:MessagesState):
        messages=state["messages"]
        response= await model_with_tools.ainvoke(messages)
        return {"messages":[response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model",call_model)
    builder.add_node("tool_node",tool_node)

    builder.add_edge(START,"call_model")
    builder.add_conditional_edges("call_model",should_continue)
    builder.add_edge("tool_node","call_model")

    graph=builder.compile()

    results = await graph.ainvoke({"messages": [HumanMessage(content="python code to add 2 no.")]})
    print(results["messages"][-1].content)


if __name__=="__main__":
    asyncio.run(main())
