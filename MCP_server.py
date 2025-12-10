from mcp.server.fastmcp import FastMCP
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
import os
from dotenv import load_dotenv
import asyncio
import typing

load_dotenv()
api_key = os.getenv("google_api_key")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

mcp = FastMCP("math")






# tool for general query of user operation
@mcp.tool()
async def normal_query(query: str) -> str:
    """Handle general queries or the task that user ask with precision(essay,story,facts,questions,summary,reasoning) etc tasks."""
    try:
        response = await model.ainvoke(query)
        return response.content
    except ResourceExhausted:
        return "Free AI quota exhausted for today, try again tomorrow 🫠"



  # Always mention necessary 

@mcp.tool()
async def math_generation(query: str) -> str:
    """
    Generate clean, well-commented  maths ans with explaination .

    Args:
        query (str): User's description for desired math operation.

    Returns:
        str: Generated ans  with comments and explanation.
    
    Raises:
        ValueError: If the query is empty.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    # Prompt engineering as recommended by AI  experts.
    prompt = (
        "Act as an expert and experienced math resaercher with access to the latest libraries and best practices and tools.\n"
        "Generate logic with precise logic. "
        "Add comprehensive inline comments for clarity, "
        "and ensure the code has no syntax errors.\n"
        
    )
    full_query = f"{prompt}{query}"
    try:
        response = await model.ainvoke(full_query)
        # Basic length validation for output (optional but helps detect model failures)
        if not response or len(response.content.strip()) < 10:
            raise RuntimeError("Generated code is unexpectedly short.")
        return response.content
    except ResourceExhausted:
        return "Free AI quota exhausted for today, try again tomorrow 🫠"

@mcp.tool()
async def normal_query(query: str) -> str:
    """Handle general queries that are  math-related"""
    try:
        response = await model.ainvoke(query)
        return response.content
    except ResourceExhausted:
        return "Free AI quota exhausted for today, try again tomorrow 🫠"



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
        "Act as an expert and experienced Python developer with access to the latest libraries and best practices and tools.\n"
        "Generate code with precise logic. "
        "Add comprehensive inline comments for clarity, "
        "list required import statements, "
        "and ensure the code has no syntax errors.\n"
        
    )
    full_query = f"{prompt}{query}"
    try:
        response = await model.ainvoke(full_query)
        # Basic length validation for output (optional but helps detect model failures)
        if not response or len(response.content.strip()) < 10:
            raise RuntimeError("Generated code is unexpectedly short.")
        return response.content
    except ResourceExhausted:
        return "Free AI quota exhausted for today, try again tomorrow 🫠"





@mcp.tool()
async def webcode_generation(query: str) -> str:
    """
    Generate robust web development code or landing page for website request  with comments and all necessary imports.

    Args:
        query (str): User's web application description.

    Returns:
        str: Web code  for  website in (html,css,js) fully commented and import-ready.
    
    Raises:
        ValueError: If the query is not a non-empty string.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    # Prompt is precisely engineered for web code generation.
    prompt = (
        "Act as a senior and experienced web developer.\n"
        "Write the required code with correct logic and comments, "
        "put all code in single snippet "
        "and list every required import.\n"
        "Make sure the genrated code has no syntax errors.\n"
    )
    full_query = f"{prompt}{query}"
    response = await model.ainvoke(full_query)
    if not response or len(response.content.strip()) < 10:
        raise RuntimeError("Generated code output is insufficient.")
    return response.content



if __name__ == "__main__":
    mcp.run(transport="stdio")
