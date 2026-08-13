# LangGraph AI Agent

A multi-provider AI agent app with a FastAPI backend and a Streamlit frontend. Define a custom agent persona, choose your model provider, optionally enable web search, and chat with it through a clean web UI.

## Features

- Custom system prompt to define agent behavior
- Support for **Groq** and **OpenAI** models
- Optional web search
- FastAPI backend serving the agent
- Streamlit-based chat UI

## Project Structure

```
├── ai_agent.py       # Core AI agent logic
├── backend.py        # FastAPI backend server
├── frontend.py       # Streamlit frontend
├── requirements.txt / Pipfile
└── README.md
```

## Setup

### 1. Create a virtual environment

**Pipenv**
```bash
pip install pipenv
pipenv install
pipenv shell
```

**pip + venv**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Conda**
```bash
conda create --name myenv python=3.11
conda activate myenv
pip install -r requirements.txt
```

### 2. Configure environment variables
Add your API keys (Groq / OpenAI) to a `.env` file.

## Running the Project

Run each phase in order (separate terminals for backend and frontend):

```bash
# Phase 1: Core agent
python ai_agent.py

# Phase 2: Backend (FastAPI)
python backend.py

# Phase 3: Frontend (Streamlit)
python frontend.py
```

The frontend connects to the backend at `http://127.0.0.1:9999/chat`.

## License

MIT