# Tokenizer implementation for Day 3


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

prompt1 = "Hey There !"
prompt2 = "Explain the use of Dynamic Programing in details"
prompt3 = "What is recursion ?"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message_user = {
        "role": "user",
        "content":prompt
    }
    response = client.chat.completions.create(
        model = model,
        messages = [message_user],
        max_tokens = 100
    )

    # print(response.choices[0].message.content)
    usage = response.usage

    print(f"Prompt: {prompt} ;- User Tokens : {usage.prompt_tokens} and LLM tokens : {usage.completion_tokens} , total tokens :- {usage.total_tokens} Finish Reason = {response.choices[0].finish_reason}")