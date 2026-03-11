import sys
import os

# ensure parent directory (workspace root) is on path so backend package is visible
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

import chainlit as cl
from backend.chatbot import setup_async_graph
from langchain_core.messages import HumanMessage

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Run CPU Tests",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
        ),

        cl.Starter(
            label="Run Memory Tests",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Run Disk Tests",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
            command="code",
        ),
        cl.Starter(
            label="Holistic Stress - CPU+Memory+Disk",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
        )
    ]


@cl.on_chat_start
async def start_chat():
    # 1. Initialize the async graph and database connection
    chatbot = await setup_async_graph()
    
    # 2. Store this specific chatbot instance in the user's session
    cl.user_session.set("chatbot", chatbot)
    
    # 3. Create and store their unique thread ID for the memory
    cl.user_session.set("thread_id", cl.user_session.get("id"))

# simple function to choose a thread id per user session
# chainlit stores context in user_session via cl.user_session

@cl.on_message
async def main(message):
    # extract text from chainlit message object (always coerce to str)


    if hasattr(message, "content"):
        user_text = message.content
    else:
        user_text = str(message)

    # debug: print full object attributes
    #print("received message text=", user_text)
    #print("message attributes:", vars(message))

    thread_id = cl.user_session.get("thread_id")
    chatbot = cl.user_session.get("chatbot")

    # stream langgraph chatbot with the new human message
    try:
        # Create an empty message to stream to
        msg = cl.Message(content="")
        await msg.send() 
        
        # Use astream() for async streaming, and fix the loop syntax
        async for chunk, metadata in chatbot.astream(
            {"messages": [HumanMessage(content=user_text)]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="messages"
        ):

            # --- DEBUGGING PRINT ---
            # This will print the raw chunks to your terminal so you can see the data!
            # print(f"DEBUG Chunk: {chunk.__class__.__name__} | Content: {chunk.content}")
           
          if chunk.content:
              await msg.stream_token(chunk.content)

        # # Finalize the message
          await msg.update()
        
    except Exception as e:
        reply_text = f"Error invoking chatbot: {e}"
        print("chatbot invocation error:", e)
        await cl.Message(content=reply_text).send()


