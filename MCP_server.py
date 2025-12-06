from mcp.server.fastmcp import FastMCP
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import asyncio
import typing

load_dotenv()
api_key = os.getenv("google_api_key")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

mcp = FastMCP("math")

# tool for maths operation 
@mcp.tool()
def add(a: int, b: int) -> int:
    "add two numbers"
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    "subtract two numbers"
    return a - b

@mcp.tool()
def mul(a: int, b: int) -> int:
    "multiply two numbers"
    return a * b

@mcp.tool()
def div(a: int, b: int) -> float:
    "divide two numbers"
    return a / b   

@mcp.tool()
async def normal_query(query: str) -> str:
    """Handle general queries that are not math-related"""
    response = await model.ainvoke(query)
    return response.content



  # Always mention necessary imports

@mcp.tool()
async def code_generation(query: str) -> str:
    """
    Generate clean, well-commented Python code for any type of code request.

    Args:
        query (str): User's description for desired code.

    Returns:
        str: Generated Python code with comments and required imports.
    
    Raises:
        ValueError: If the query is empty.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    # Prompt engineering as recommended by AI code generation experts.
    prompt = (
        "Act as an expert Python developer.\n"
        "Generate code with precise logic. "
        "Add comprehensive inline comments for clarity, "
        "list required import statements, "
        "and ensure the code has no syntax errors.\n"
        "Deliver the code as a complete, runnable snippet ready for copy-pasting.\n"
    )
    full_query = f"{prompt}{query}"
    response = await model.ainvoke(full_query)
    # Basic length validation for output (optional but helps detect model failures)
    if not response or len(response.content.strip()) < 10:
        raise RuntimeError("Generated code is unexpectedly short.")
    return response.content





@mcp.tool()
async def webcode_generation(query: str) -> str:
    """
    Generate robust web development code in one file with comments and all necessary imports.

    Args:
        query (str): User's web application description.

    Returns:
        str: Web code (e.g., for Flask, Django, FastAPI, or JS frameworks) fully commented and import-ready.
    
    Raises:
        ValueError: If the query is not a non-empty string.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    # Prompt is precisely engineered for web code generation.
    prompt = (
        "Act as a senior web developer.\n"
        "Write the required code with correct logic and comments, "
        "put all logic in a single file for direct copy-paste use, "
        "and list every required import.\n"
        "Make sure the generated web app runs without syntax errors and is easy to test.\n"
    )
    full_query = f"{prompt}{query}"
    response = await model.ainvoke(full_query)
    if not response or len(response.content.strip()) < 10:
        raise RuntimeError("Generated code output is insufficient.")
    return response.content



if __name__ == "__main__":
    mcp.run(transport="stdio")
