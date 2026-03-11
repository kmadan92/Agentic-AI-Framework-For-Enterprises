# Async LangGraph & Chainlit Chatbot

A fully asynchronous, stateful AI chatbot built with LangGraph and Chainlit, powered by Azure OpenAI. This project features real-time token streaming, persistent local conversation memory, and strict user-session isolation.

## 🛠 Tech Stack

* **Frontend Framework:** [Chainlit](https://docs.chainlit.io/) (for the conversational web UI and WebSocket management)
* **Agent Logic / Backend:** [LangGraph](https://python.langchain.com/docs/langgraph) & LangChain
* **LLM Provider:** Azure OpenAI (`AzureChatOpenAI`)
* **Database / Memory:** SQLite with `aiosqlite` (via LangGraph's `AsyncSqliteSaver`)
* **Environment Management:** Python `venv` (`mcp`), `python-dotenv`

## ✨ Features & Work Completed So Far

* **Azure OpenAI Integration:** Securely authenticates and routes requests to a specific Azure model deployment.
* **Fully Asynchronous Pipeline:** From the Chainlit UI to the LangGraph nodes to the SQLite database, every step utilizes `async/await` to ensure the server never blocks or freezes during LLM processing.
* **Real-time Streaming:** Implemented `astream` with `stream_mode="messages"` to create a native, typewriter-style token streaming effect in the Chainlit UI.
* **Isolated User Sessions:** Utilizes Chainlit's automatic WebSocket session IDs (`cl.user_session.get("id")`) to map unique LangGraph `thread_id`s to individual users. Multiple users can chat simultaneously without seeing each other's memory.
* **Persistent SQLite Memory:** Conversation history is automatically saved to a local `checkpoints.sqlite` file. If a user refreshes their session, the agent remembers the context.
* **Custom UI Starters:** Pre-configured chat starter buttons for quick testing.
* **Secure Repo Configuration:** A strict `.gitignore` is in place to protect Azure API keys, database files, and the local `mcp` virtual environment.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed. You will also need access to an Azure OpenAI resource.

### 2. Environment Setup
Clone the repository and activate your virtual environment (named `mcp`):

**Windows:**
`.\mcp\Scripts\activate`

**macOS/Linux:**
`source mcp/bin/activate`

Install the required dependencies (ensure you have `chainlit`, `langgraph`, `langchain-openai`, `aiosqlite`, and `python-dotenv` installed).

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your Azure OpenAI credentials:

AZURE_OPENAI_API_KEY="your_azure_key_here"
AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"

*(Note: Do not commit this file to version control. It is already ignored in `.gitignore`.)*

### 4. Running the Application
Start the Chainlit server in watch mode (auto-reloads on file changes):

`chainlit run app.py -w`

The application will automatically open in your browser at `http://localhost:8000`.

## 📁 Project Structure

* `.env` - Azure credentials (ignored by Git)
* `.gitignore` - Git ignore rules for secrets, venv, and DBs
* `README.md` - Project documentation
* `app.py` - Chainlit frontend and async UI streaming logic
* `backend/`
  * `chatbot.py` - LangGraph state graph, LLM config, and async SQLite checkpointer
* `checkpoints.sqlite` - Local persistent memory database (ignored by Git)
* `mcp/` - Python virtual environment (ignored by Git)