import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key="ollama"
)

response = client.chat.completions.create(
    model=os.getenv("OLLAMA_MODEL"),
    messages=[
        {"role": "user", "content": "Why is the sky blue?"}
    ]
)

print(response.choices[0].message.content)