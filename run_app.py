import os
import asyncio
import streamlit as st
from together import Together, AsyncTogether
from streamlit_lottie import st_lottie
import requests
import io
from fpdf import FPDF

from src.hey_bot.Backend_logic.Backend_app import main_mixture
from src.hey_bot.config import (
    REFERENCE_MODELS,
    AGGREGATOR_MODEL,
    AGGREGATOR_SYSTEM_PROMPT,
)


# ----------------------
# Page Config & Styles
# ----------------------
st.set_page_config(
    page_title="Mixture-of-Agents LLM App",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------
# Theme Toggle
# ----------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


st.sidebar.button(
    "Toggle Light/Dark Theme",
    on_click=toggle_theme
)


if st.session_state.theme == "dark":
    st.markdown(
        """<style>
           body { background-color: #0f172a; color: #f1f5f9; }
           .stButton>button { background: #334155; color: #f1f5f9; }
           </style>""",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """<style>
           body { background-color: #fafafa; color: #0f172a; }
           .stButton>button { background: #e2e8f0; color: #0f172a; }
           </style>""",
        unsafe_allow_html=True,
    )


# ----------------------
# Helper: load Lottie animation
# ----------------------
def load_lottie_url(url: str):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

backgrounds = {
    "AI Robot Loader": "https://assets8.lottiefiles.com/packages/lf20_khsc0bzl.json",
    "AI Brain": "https://lottie.host/753efe02-9bf9-43f7-8560-8e2ad1978b6c/JOcswhdJsa.json",
}
bg_choice = st.sidebar.selectbox(
    "🎨 Background Animation",
    options=list(backgrounds.keys()),
    index=0,
)

lottie_url = backgrounds[bg_choice]
lottie_json = load_lottie_url(lottie_url)
if lottie_json:
    st_lottie(lottie_json, height=150, loop=True, quality="high")


# ----------------------
# Sidebar for configuration
# ----------------------
st.sidebar.title("Settings")
with st.sidebar.expander("API Configuration", expanded=True):
    together_api_key = st.text_input("Together API Key", type="password")

with st.sidebar.expander("Agent Models", expanded=False):
    selected_labels = st.multiselect(
    "🧠 Choose Reference Models:",
    options=list(REFERENCE_MODELS.keys()),
    default=list(REFERENCE_MODELS.keys())[:2],
    
    )
    selected_aggregator = st.selectbox(
        "Aggregator Model",
        options=[AGGREGATOR_MODEL],
    )

if together_api_key:
    os.environ["TOGETHER_API_KEY"] = together_api_key
    client = Together(api_key=together_api_key)
    async_client = AsyncTogether(api_key=together_api_key)
else:
    st.warning("Please enter your Together API key to continue.")
    st.stop()


# ----------------------
# Main UI
# ----------------------

selected_references = [REFERENCE_MODELS[label] for label in selected_labels]


st.header("Ask the Apex-LLM-V-0.0.001")
user_prompt = st.text_area(
    "Enter your question:",
    height=150,
    placeholder="What would you like to ask today?",
)

style = st.selectbox(
    "Response Style",
    options=["Default", "Concise", "Detailed", "Bullet Points", "Example-driven"],
)

if st.button("Get Answer", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("⏳ Querying agents..."):
            final_answer = asyncio.run(main_mixture(
                prompt=user_prompt,
                async_client=async_client,
                references=selected_references,
                aggregator=selected_aggregator,
                style=style,
            ))

            #-----------------------
            # Download as Markdown  
            #-----------------------
            md_bytes = final_answer.encode("utf-8")
            st.download_button(
                "📥 Download as Markdown",
                data=md_bytes,
                file_name="answer.md",
                mime="text/markdown",
        )
            
            #-----------------------
            # Download as PDF
            #-----------------------
            def make_pdf(text: str) -> bytes:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in text.split("\n"):
                    pdf.multi_cell(0, 5, line)
                pdf_str = pdf.output(dest="S")
                return pdf_str.encode("latin-1")

            pdf_bytes = make_pdf(final_answer)
            st.download_button(
            "📥 Download as PDF",
            data=pdf_bytes,
            file_name="answer.pdf",
            mime="application/pdf",
        )
            #-----------------------
            # History
            #-----------------------
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((user_prompt, final_answer))

            st.sidebar.title("💬 Chat History")
            with st.sidebar.expander("Conversation", expanded=False):
                for u, b in reversed(st.session_state.history):
                    st.markdown(f"**You:** {u}", unsafe_allow_html=True)
                    st.markdown(f"**Bot:** {b}", unsafe_allow_html=True)
                    st.markdown("---")
            
    else:
        st.error("Please enter a question and select at least one model")
