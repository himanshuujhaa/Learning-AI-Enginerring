# Structured JSON Output Using Pydantic

import os
# from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI

from pydantic import BaseModel

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"

client = OpenAI(
    base_url = ollama_base_url,
    api_key = my_api_key
)

model = os.getenv("OLLAMA_MODEL")

from pydantic import BaseModel, field_validator
from typing import Union, List

class Ticket(BaseModel):
    name: str
    email: str
    phone: str
    issue: str

    # @field_validator('email', 'phone', mode='before')
    # @classmethod
    # def convert_list_to_string(cls, v):
    #     if isinstance(v, list):
    #         return v[0] if v else ""
    #     return v


schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

### system prompt must instruct the model in plain English without injecting schema dictionary
# system_prompt = f"""
# You are a precise data extraction assistant. Your task is to extract ONLY the customer's personal details from the customer ticket.

# Guidelines:
# 1. For 'phone': Extract ONLY the customer's personal phone number as a single string. Do NOT extract company helpdesk/support phone numbers (like 6204376778).
# 2. For 'email': Extract ONLY the customer's personal email address as a single string. Do NOT extract company support emails (like support@flipkart.com) and do NOT output a list.
# 3. For 'name': Extract the customer's name.
# 4. For 'issue': Extract the actual issue or complaint description from the ticket (do not copy the placeholder text from the example).

# You must output a JSON object with exactly these keys (all values must be plain strings, not lists):
# - "name" (string)
# - "email" (string)
# - "phone" (string)
# - "issue" (string)

# Example JSON format:
# {{
#   "name": "John Doe",
#   "email": "john@example.com",
#   "phone": "1234567890",
#   "issue": "Summarize the customer's complaint here"
# }}
# """

system_prompt = """
Extract the customer's information.

Return ONLY valid JSON.

The JSON MUST contain exactly these fields:

{
    "name": "",
    "email": "",
    "phone": "",
    "issue": ""
}

Do not change field names.
Do not use phone_number.
Do not omit issue.
Every value must be a string.
"""

message_system = {
    "role" : "system",
    "content": system_prompt
}

text = "My name is Himanshu Jha, I had a very bad experince with flipkart services, I tried to conatct support team using my phone no 7070987129 and also mailed them using himanshi123@gmail.com but got no response"

prompt = f"""
this is a customer ticket please extract the personal in formation from this {text}
"""

message = {
    "role":"user",
    "content":prompt
}


response = client.chat.completions.create(
    model = model,
    messages = [message_system ,message],
    response_format = response_format
)

json_response = response.choices[0].message.content
# print("Raw LLM Output:")
print(json_response)

# Parse and validate using Pydantic
# try:
#     ticket = Ticket.model_validate_json(json_response)
#     print("\nSuccessfully parsed and validated into Pydantic model:")
#     print(ticket)
#     print(f"\nExtracted Personal Phone: {ticket.phone}")
#     print(f"Extracted Personal Email: {ticket.email}")
# except Exception as e:
#     print("\nValidation Failed:")
#     print(e)

import json
raw_json = json_response
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print("name : " + ticket.name)
print("phone : " + ticket.phone)
print("email : " + ticket.email)
print("issue : " + ticket.issue)    
