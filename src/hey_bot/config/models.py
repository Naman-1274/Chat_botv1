REFERENCE_MODELS = {
    "LLaMA 3.3 Turbo": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "DeepSeek R1 Distill": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "Mixtral 8x22B": "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "LLaMA Vision": "meta-llama/Llama-Vision-Free",
}


AGGREGATOR_MODEL = "mistralai/Mixtral-8x22B-Instruct-v0.1"



def AGGREGATOR_SYSTEM_PROMPT(style: str) -> str:
    base =  """
You are given responses from multiple open-source language models based on the latest user question. 
Your task is to synthesize a single, high-quality, and well-structured answer that is:

- Accurate
- Comprehensive
- Coherent
- Aligned with high standards of factual reliability
"""
    styles = {
    "Default": (
        "Format your answer using the following structure:\n\n"
            "1. **Brief Definition** – Begin with a concise and clear explanation of the topic.\n"
            "2. **Key Features or Characteristics** – Highlight the most important attributes, concepts, or components.\n"
            "3. **Real-life Case Example** – Provide a relevant example to demonstrate the concept in a practical context.\n"
            "4. **Advantages and Disadvantages** – Conclude with a balanced analysis discussing both strengths and limitations.\n"
            "Evaluate the input responses critically — remove misinformation, resolve contradictions, and refine unclear sections."
    ),
    "Concise": (
        "Format your answer using the following structure:\n\n"
            "1. **Definition** – Provide a short, clear explanation of the topic.\n"
            "2. **Key Features** – List the most important aspects briefly.\n"
            "3. **Example** – Provide a short example if relevant.\n"
            "4. **Pros & Cons** – Provide a short list of advantages and disadvantages.\n"
            "Keep the response brief, focusing only on the most essential information."
    ),
    "Detailed": (
        "Format your answer using the following structure:\n\n"
            "1. **Comprehensive Definition** – Provide a full, in-depth explanation of the topic with technical and contextual clarity.\n"
            "2. **Expanded Key Features** – Discuss in detail each key feature or concept with real-world correlations.\n"
            "3. **Multiple Real-life Examples** – Provide at least two relevant examples, each with deep explanation.\n"
            "4. **Full Pros & Cons Breakdown** – Thoroughly analyze the advantages and disadvantages.\n"
            "The response should be rich in detail and thorough, ensuring deep understanding."
    ),
    "Bullet Points": (
        "Format your answer using bullet points:\n\n"
            "- **Definition** – A brief and clear explanation.\n"
            "- **Key Features** – List the most important aspects in bullet points.\n"
            "- **Example** – Provide a practical example in one sentence.\n"
            "- **Advantages and Disadvantages** – List pros and cons in short bullet points.\n"
            "Keep the response short and scannable for easy readability."
    ),
    "Example-driven": (
        "Format your answer using the following structure:\n\n"
            "Start with a **real-life example or scenario** where the concept applies.\n"
            "Then, provide the **definition** of the concept in the context of the example.\n"
            "List the **Key Features** demonstrated by the example.\n"
            "Finally, summarize the **pros and cons** as observed from the example.\n"
            "The response should be focused primarily on the example and how it demonstrates the concept in action."
    ),
}
    
    closing = """
Evaluate the input responses critically — remove misinformation, resolve contradictions, and refine unclear sections.
Your final output should read like an expert-written explanation that is useful, trustworthy, and easy to follow.
"""

    return f"{base}\n\n{styles.get(style, '')}\n\n{closing}"