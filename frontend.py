# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# Step1: Setup UI with streamlit (model provider, model, system prompt, web_search, query)
import html
import json

import requests
import streamlit as st

st.set_page_config(
    page_title="LangGraph Agent UI",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Design tokens & styling ----------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

        :root {
            color-scheme: light;
            --paper: #F4F5F7;
            --surface: #FFFFFF;
            --line: #E1E4EA;
            --ink: #14181F;
            --muted: #626C7A;
            --signal: #146C52;
            --signal-dark: #0E5240;
            --signal-soft: #E4F3EC;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp, .main {
            background-color: var(--paper) !important;
            color: var(--ink);
            color-scheme: light;
        }

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .block-container {
            padding-top: 2.75rem;
            padding-bottom: 3.5rem;
            max-width: 720px;
        }

        /* ---------- Masthead ---------- */
        .eyebrow {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--signal);
            margin-bottom: 0.5rem;
        }
        h1 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: var(--ink) !important;
            font-size: 2.1rem !important;
            margin-bottom: 0.3rem !important;
        }
        .subtitle {
            color: var(--muted);
            font-size: 1rem;
            margin-top: 0;
            margin-bottom: 2rem;
        }

        /* ---------- Section labels ---------- */
        .section-label {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
            border-left: 3px solid var(--signal);
            padding-left: 0.6rem;
            margin-bottom: 0.9rem;
        }

        /* ---------- Card containers ---------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
            padding: 0.4rem 0.2rem !important;
            margin-bottom: 1.4rem !important;
            box-shadow: 0 1px 2px rgba(20, 24, 31, 0.04);
        }

        /* ---------- Text areas ---------- */
        div[data-testid="stTextArea"] textarea {
            background-color: var(--surface) !important;
            color: var(--ink) !important;
            caret-color: var(--ink) !important;
            border: 1px solid var(--line) !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stTextArea"] textarea::placeholder {
            color: var(--muted) !important;
            opacity: 1 !important;
        }
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--signal) !important;
            box-shadow: 0 0 0 3px var(--signal-soft) !important;
        }

        /* ---------- Select / dropdown ---------- */
        div[data-baseweb="select"] > div {
            background-color: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="select"] * {
            color: var(--ink) !important;
            fill: var(--ink) !important;
        }
        ul[data-baseweb="menu"] {
            background-color: var(--surface) !important;
        }
        ul[data-baseweb="menu"] li {
            color: var(--ink) !important;
        }
        ul[data-baseweb="menu"] li:hover {
            background-color: var(--signal-soft) !important;
        }

        /* ---------- Radio & checkbox ---------- */
        div[data-testid="stRadio"] label p,
        div[data-testid="stCheckbox"] label p {
            color: var(--ink) !important;
            font-weight: 500;
        }
        div[data-testid="stRadio"] > label p {
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.02em;
        }

        /* ---------- Config readout ---------- */
        .config-readout {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            color: var(--muted);
            margin-top: 0.6rem;
            padding-top: 0.6rem;
            border-top: 1px dashed var(--line);
        }
        .config-readout b {
            color: var(--ink);
            font-weight: 600;
        }

        /* ---------- Button ---------- */
        div.stButton > button {
            width: 100%;
            background-color: var(--signal);
            color: #FFFFFF;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.65rem 0;
            border-radius: 10px;
            border: none;
            margin-top: 0.4rem;
            transition: background-color 0.15s ease-in-out;
        }
        div.stButton > button:hover {
            background-color: var(--signal-dark);
            color: #FFFFFF;
        }
        div.stButton > button:focus-visible {
            outline: 2px solid var(--signal);
            outline-offset: 2px;
        }

        /* ---------- Response ---------- */
        .response-eyebrow {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--muted);
            margin-top: 1.6rem;
            margin-bottom: 0.6rem;
        }
        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: var(--signal);
            animation: pulse 1.8s infinite;
        }
        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0 rgba(20, 108, 82, 0.45); }
            70%  { box-shadow: 0 0 0 6px rgba(20, 108, 82, 0); }
            100% { box-shadow: 0 0 0 0 rgba(20, 108, 82, 0); }
        }
        .response-card {
            position: relative;
            background-color: var(--surface);
            color: var(--ink);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1.25rem 1.4rem;
            font-size: 0.96rem;
            line-height: 1.6;
        }
        .response-card::before,
        .response-card::after {
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
            border: 2px solid var(--signal);
            opacity: 0.55;
        }
        .response-card::before {
            top: -1px;
            left: -1px;
            border-right: none;
            border-bottom: none;
        }
        .response-card::after {
            bottom: -1px;
            right: -1px;
            border-left: none;
            border-top: none;
        }

        @media (max-width: 640px) {
            .block-container { padding-left: 1.2rem; padding-right: 1.2rem; }
            h1 { font-size: 1.7rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="eyebrow">LangGraph &middot; Agent Runtime</div>', unsafe_allow_html=True)
st.title("AI Chatbot Agents")
st.markdown('<p class="subtitle">Configure a custom agent, then send it a query.</p>', unsafe_allow_html=True)

# ---------- Agent Configuration ----------
with st.container(border=True):
    st.markdown('<div class="section-label">Agent Persona</div>', unsafe_allow_html=True)
    system_prompt = st.text_area(
        "Define your AI Agent:",
        height=70,
        placeholder="Describe how this agent should behave...",
        label_visibility="collapsed",
    )

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

with st.container(border=True):
    st.markdown('<div class="section-label">Model Settings</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

    with col2:
        if provider == "Groq":
            selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
        else:
            selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

    allow_web_search = st.checkbox("Allow Web Search")

    st.markdown(
        f'<div class="config-readout">PROVIDER: <b>{provider.upper()}</b> &nbsp;&middot;&nbsp; '
        f'MODEL: <b>{selected_model}</b> &nbsp;&middot;&nbsp; '
        f'WEB SEARCH: <b>{"ON" if allow_web_search else "OFF"}</b></div>',
        unsafe_allow_html=True,
    )

# ---------- Query Input ----------
with st.container(border=True):
    st.markdown('<div class="section-label">Your Query</div>', unsafe_allow_html=True)
    user_query = st.text_area(
        "Enter your query:",
        height=150,
        placeholder="Ask anything...",
        label_visibility="collapsed",
    )

API_URL = "https://langraph-ai-agent.onrender.com/chat"


def extract_response_text(data):
    """Pull a readable string out of whatever shape the backend returns."""
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in ("response", "output", "answer", "content", "result", "message"):
            value = data.get(key)
            if isinstance(value, str):
                return value
        messages = data.get("messages")
        if isinstance(messages, list) and messages:
            last = messages[-1]
            if isinstance(last, dict):
                return last.get("content") or json.dumps(last, indent=2, ensure_ascii=False)
            return str(last)
    return json.dumps(data, indent=2, ensure_ascii=False)


if st.button("Run Agent"):
    if not user_query.strip():
        st.warning("Enter a query before running the agent.")
    else:
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search,
        }

        try:
            with st.spinner("Running agent..."):
                response = requests.post(API_URL, json=payload, timeout=60)
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not reach the agent backend: {exc}")
        else:
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, dict) and "error" in response_data:
                    st.error(response_data["error"])
                else:
                    text = extract_response_text(response_data)
                    safe_text = html.escape(text).replace("\n", "<br>")
                    st.markdown(
                        '<div class="response-eyebrow"><span class="status-dot"></span>Agent Output</div>'
                        f'<div class="response-card">{safe_text}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.error(f"Request failed with status code {response.status_code}.")