import os
import asyncio
import streamlit as st
from together import Together, AsyncTogether

from src.hey_bot.Backend_logic.Backend_app import main_mixture
# from src.hey_bot.Backend_logic.Backend_app import main_mixture  # Ensure this import works during asyncio
from src.hey_bot.config import (
    REFERENCE_MODELS,
    AGGREGATOR_MODEL,
    AGGREGATOR_SYSTEM_PROMPT,
)

st.set_page_config(page_title="Mixture-of-Agents LLM App")
st.title("Mixture-of-Agents LLM App")

together_api_key = st.text_input("Enter your Together API Key:", type="password")
user_prompt = st.text_input("Enter your question:")

if together_api_key:
    os.environ["TOGETHER_API_KEY"] = together_api_key
    client = Together(api_key=together_api_key)
    async_client = AsyncTogether(api_key=together_api_key)
else:
    st.warning("Please enter your Together API key to continue.")
    st.stop()

if st.button("Get Answer"):
    if user_prompt.strip():
        with st.spinner("Querying models..."):
            asyncio.run(main_mixture(user_prompt, async_client))
    else:
        st.warning("Please enter a question first.")
