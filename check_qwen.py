import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="nscale",
    api_key=os.environ.get("HF_TOKEN"),  # Or replace with your "hf_..." token string if hardcoded
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-3B-Instruct",
    messages=[{"role": "user", "content": "Write a Python function to reverse a string."}],
    max_tokens=100,
)

print(response.choices[0].message.content)