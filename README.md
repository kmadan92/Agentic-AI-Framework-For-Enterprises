# Async LangGraph & Chainlit Chatbot

A fully asynchronous, stateful AI chatbot built with **LangGraph** and
**Chainlit**, powered by **Azure OpenAI**.

The application supports:

-   Google authentication
-   Persistent chat history
-   LangGraph checkpoint memory
-   Real-time streaming responses
-   Multi-user safe conversations

Each conversation thread is persisted and restored automatically,
allowing users to switch between chats while maintaining memory.

------------------------------------------------------------------------

# Tech Stack

## Frontend / UI

-   Chainlit --- conversational UI, authentication, and chat history

## Agent Logic / Backend

-   LangGraph --- stateful agent execution and checkpointing
-   LangChain --- LLM interface

## LLM Provider

-   Azure OpenAI (AzureChatOpenAI)

## Persistence Layers

Two independent databases are used:

  Component     Database                 Purpose
  ------------- ------------------------ ------------------------------
  Chainlit UI   chainlit_ui_history.db   Chat history, threads, steps
  LangGraph     checkpoints.sqlite       Conversation memory state

## Other Tools

-   SQLite
-   aiosqlite
-   python-dotenv

------------------------------------------------------------------------

# Features

## Google Authentication

Users authenticate with Google before accessing the chatbot.

Authentication is implemented using Chainlit's OAuth callback system.\
Each authenticated user receives isolated chat threads.

------------------------------------------------------------------------

## Persistent Chat History

All conversations are stored in the Chainlit SQLite database.

Users can: - Switch between conversations - Resume previous chats -
Continue conversations later

The sidebar automatically displays saved threads.

------------------------------------------------------------------------

## LangGraph Memory Persistence

Conversation memory is stored using LangGraph checkpointing.

Each conversation thread maps to a unique checkpoint state.

Example flow:

Chainlit Thread ID\
→ LangGraph thread_id\
→ SQLite checkpoints.sqlite

This ensures that when a chat is resumed, the model retains context.

------------------------------------------------------------------------

## Real-Time Streaming Responses

The chatbot streams responses token-by-token using:

    astream(stream_mode="messages")

This produces a typewriter-style response in the UI.

------------------------------------------------------------------------

## Fully Asynchronous Pipeline

The entire stack runs asynchronously:

User\
→ Chainlit UI\
→ LangGraph Execution\
→ Azure OpenAI API\
→ SQLite Checkpoint Storage

All components use async/await to prevent blocking.

------------------------------------------------------------------------

## Multi-User Safe Architecture

The server runs a single shared LangGraph instance.

Conversation isolation is maintained using thread IDs:

User A → thread_id = T1\
User B → thread_id = T2\
User C → thread_id = T3

Checkpoint state is stored separately for each thread.

This allows multiple users to chat simultaneously without memory
overlap.

------------------------------------------------------------------------

# Conversation Thread Flow

1.  User sends a message in Chainlit\
2.  Chainlit assigns a thread ID\
3.  The message carries message.thread_id\
4.  LangGraph receives the same ID

Example:

``` python
chatbot.astream(
    {"messages": [HumanMessage(content=user_text)]},
    config={"configurable": {"thread_id": message.thread_id}}
)
```

5.  LangGraph loads the checkpoint for that thread\
6.  Model response is generated and stored

------------------------------------------------------------------------

# Getting Started

## 1. Prerequisites

-   Python 3.10+
-   Azure OpenAI resource
-   Google OAuth credentials

------------------------------------------------------------------------

## 2. Install Dependencies

``` bash
pip install chainlit langgraph langchain-openai aiosqlite python-dotenv
```

------------------------------------------------------------------------

## 3. Configure Environment Variables

Create a `.env` file in the root directory:

    AZURE_OPENAI_API_KEY="your_azure_key"
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
    AZURE_OPENAI_DEPLOYMENT="your-model-deployment"
    AZURE_OPENAI_API_VERSION="2024-02-15-preview"

------------------------------------------------------------------------

## 4. Configure Google OAuth

Add Google OAuth credentials to the `.env` file:

    OAUTH_GOOGLE_CLIENT_ID="your_google_client_id"
    OAUTH_GOOGLE_CLIENT_SECRET="your_google_secret"

------------------------------------------------------------------------

## 5. Run the Application

    chainlit run app.py -w

The application will start at:

http://localhost:8000

------------------------------------------------------------------------

# Project Structure

    project-root
    │
    ├── app.py
    ├── backend/
    │   └── chatbot.py
    │
    ├── .env
    ├── .gitignore
    ├── README.md
    │
    ├── checkpoints.sqlite
    ├── chainlit_ui_history.db
    │
    └── venv/

## Key Files

### app.py

Handles: - Chainlit UI - Authentication - Message streaming - Thread ID
routing

### backend/chatbot.py

Defines: - LangGraph state graph - Azure OpenAI integration - Async
SQLite checkpoint saver

------------------------------------------------------------------------

# Security

Sensitive files are excluded via `.gitignore`:

    .env
    *.sqlite
    venv/
    __pycache__/

Never commit API keys or local databases.

------------------------------------------------------------------------

# Future Improvements

Planned enhancements:

-   PostgreSQL checkpoint storage for production
-   Vector memory for long-term recall
-   Tool integrations
-   Retrieval-Augmented Generation (RAG)
-   Rate limiting and usage tracking
-   Container or cloud deployment

------------------------------------------------------------------------

# License

MIT License
