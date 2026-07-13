
import os
# from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"

client = OpenAI(
    base_url = ollama_base_url,
    api_key = my_api_key
)

model = os.getenv("OLLAMA_MODEL")
role = "user"
prompt = "I dont Want to do waok right now, I am leaving"
Messages = [
    {
        "role": "system",
        "content": "You are my manager and I am your employee. You are very strict and only want best quality work. You also make sure that your employee takes breaks."
    },
    {
        "role": role,
        "content": prompt
    }
]

response = client.chat.completions.create(
    model=model,
    messages=Messages
)

print(response.choices[0].message.content)