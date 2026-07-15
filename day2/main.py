
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

message_system =  {
    "role": "system",
    "content": "You are my Senior Engineer."
}

message_user = {
    "role": "user",
    "content": "What is dynamic Programming"
}

Messages = [
   message_system, message_user
]

response = client.chat.completions.create(
    model=model,
    messages=Messages,
    temperature = 2
)

print(response.choices[0].message.content)