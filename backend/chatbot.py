import sys
import os

# ensure parent directory (workspace root) is on path so utilities package is visible
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import asyncio
import os
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# load environment variables from .env (endpoint, key, deployment, version)
load_dotenv()

# require deployment and version to be set
azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
if not azure_deployment:
    raise RuntimeError("AZURE_OPENAI_DEPLOYMENT must be set in .env")

api_version = os.getenv("AZURE_OPENAI_API_VERSION")
if not api_version:
    raise RuntimeError("AZURE_OPENAI_API_VERSION must be set in .env")

# instantiate Azure chat model
llm = AzureChatOpenAI(
    azure_deployment=azure_deployment,
    api_version=api_version,
    # additional params like temperature, max_tokens are optional
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def chat_node(state: ChatState):
    """Async chat node that calls the LLM asynchronously"""
    messages = state['messages']
    response = await llm.ainvoke(messages)
    return {"messages": [response]}

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Initialize SQLite checkpointer for conversation persistence with async support
async def setup_async_graph():
    # Now we can safely use 'await' because we are inside an async function
    conn = await aiosqlite.connect("checkpoints.sqlite")
    saver = AsyncSqliteSaver(conn=conn)
    
    # Compile and return the chatbot
    return graph.compile(checkpointer=saver)


##------Test Backend Code------
# async def run_test():
#     print("Initializing async graph...")
#     # 1. We must AWAIT the setup function to get the actual graph object
#     chatbot = await setup_async_graph()
    
#     print("Sending message to Azure (Streaming)...\n")
#     print("AI: ", end="", flush=True) # Prepare the terminal line
    
#     # 2. Because we are streaming, we must iterate over the chunks using 'async for'
#     async for chunk, metadata in chatbot.astream(
#         {"messages": [HumanMessage(content="Hello from the graph!")]},
#         config={"configurable": {"thread_id": "test"}},
#         stream_mode="messages" # Corrected from stream="messages"
#     ):
#         # 3. Print the AI chunks to the terminal exactly as they arrive
#         #if chunk.content and getattr(chunk, "type", "") == "ai":
#         print(chunk.content, end="", flush=True)

#     print("\n\n[Stream finished successfully!]")
#     await chatbot.checkpointer.conn.close()

# # 3. This is how you run an async function in a standalone Python script
# if __name__ == "__main__":
#     asyncio.run(run_test())

