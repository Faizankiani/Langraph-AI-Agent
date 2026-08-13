# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()


#Step1: Setup UI with streamlit (model provider, model, system prompt, web_search, query)
import streamlit as st

st.set_page_config(
    page_title="LangGraph Agent UI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- Custom Styling ----------
st.markdown("""
    <style>
        .main {
            background-color: #f7f8fa;
        }
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 780px;
        }
        h1 {
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #1a1a2e;
        }
        .subtitle {
            color: #6b7280;
            font-size: 1.05rem;
            margin-top: -10px;
            margin-bottom: 1.8rem;
        }
        .section-label {
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #4b5563;
            border-left: 3px solid #4f46e5;
            padding-left: 0.6rem;
            margin-top: 1.4rem;
            margin-bottom: 0.5rem;
        }
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="textarea"],
        div[data-baseweb="base-input"] {
            background-color: #ffffff !important;
            color: #111827 !important;
            caret-color: #111827 !important;
            border-radius: 10px !important;
            border: 1px solid #d1d5db !important;
        }
        div[data-testid="stTextArea"] textarea::placeholder {
            color: #9ca3af !important;
            opacity: 1 !important;
        }
        div[data-testid="stSelectbox"] > div {
            border-radius: 10px;
        }
        .stRadio > label {
            font-weight: 600;
        }
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #4f46e5, #6366f1);
            color: white;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.6rem 0;
            border-radius: 10px;
            border: none;
            margin-top: 1.5rem;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #4338ca, #4f46e5);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
        }
        .response-card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-top: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        hr {
            margin: 1.8rem 0;
            border: none;
            border-top: 1px solid #e5e7eb;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("AI Chatbot Agents")
st.markdown('<p class="subtitle">Create and interact with your own custom AI agents.</p>', unsafe_allow_html=True)

# ---------- Agent Configuration ----------
st.markdown('<div class="section-label">Agent Persona</div>', unsafe_allow_html=True)
system_prompt = st.text_area(
    "Define your AI Agent:",
    height=70,
    placeholder="Type your system prompt here...",
    label_visibility="collapsed"
)

st.markdown("<hr>", unsafe_allow_html=True)

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

st.markdown('<div class="section-label">Model Settings</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

with col2:
    if provider == "Groq":
        selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
    elif provider == "OpenAI":
        selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- Query Input ----------
st.markdown('<div class="section-label">Your Query</div>', unsafe_allow_html=True)
user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask Anything!",
    label_visibility="collapsed"
)

API_URL = "https://langraph-ai-agent.onrender.com/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        #Step2: Connect with backend via URL
        import requests

        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.markdown('<div class="section-label">Agent Response</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="response-card">{response_data}</div>', unsafe_allow_html=True)