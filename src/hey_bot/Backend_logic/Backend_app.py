import asyncio
import streamlit as st
from together import AsyncTogether
from src.hey_bot.config import REFERENCE_MODELS, AGGREGATOR_MODEL, AGGREGATOR_SYSTEM_PROMPT

async def run_llm(model_name: str, prompt: str, async_client: AsyncTogether) -> str:
    try:
        response = await async_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error from {model_name}: {e}"

async def main_mixture(
    prompt: str,
    async_client: AsyncTogether,
    delay_between: float = 1.0,
    stream_delay: float = 0.2,
):
    st.subheader("Individual Model Responses")
    results = []
    for model_name in REFERENCE_MODELS:
        output = await run_llm(model_name, prompt, async_client)
        results.append(output)
        with st.expander(f"Response from {model_name}"):
            st.markdown(output)
        await asyncio.sleep(delay_between)

    st.subheader("Aggregated Response")
    final_container = st.empty()
    final_answer = ""

    stream = await async_client.chat.completions.create(
        model=AGGREGATOR_MODEL,
        messages=[
            {"role": "system", "content": AGGREGATOR_SYSTEM_PROMPT},
            {"role": "user", "content": "\n\n".join(results)},
        ],
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        final_answer += delta
        final_container.markdown(final_answer + "▌")
        await asyncio.sleep(stream_delay)

    final_container.markdown(final_answer)
