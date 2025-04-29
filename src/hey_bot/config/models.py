REFERENCE_MODELS = [
    
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "mistralai/mistral-7b-v0.1",
    "EleutherAI/gpt-j-6B",
    "openchat/openchat-3.5-1210", 
    
]

AGGREGATOR_MODEL = "mistralai/Mixtral-8x22B-Instruct-v0.1"



AGGREGATOR_SYSTEM_PROMPT = """
You have been provided with a set of responses from various open-source models
to the latest user query. Your task is to synthesize these responses into a
single, high-quality answer. Critically evaluate the information: some may be
biased or incorrect. Your final reply should be accurate, comprehensive, coherent,
and adhere to high standards of reliability.
""".strip()