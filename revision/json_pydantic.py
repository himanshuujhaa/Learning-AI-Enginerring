from pydantic import constr
from pydantic import EmailStr
import os
from dotenv import load_dotenv

from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"

client = OpenAI(
    base_url=ollama_base_url,
    api_key=my_api_key
)

model = os.getenv("OLLAMA_MODEL")

Phone = constr(pattern=r"^\+?[0-9]{7,15}$")

class Issue(BaseModel):
    description: str

class Ticket(BaseModel):

    name: str | None = None
    email: list[EmailStr] = []
    phone: list[Phone] = []
    issue: list[Issue] = []

# schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = """
Extract information and return ONLY valid JSON.

Output format:

{
  "name": "string or null",
  "email": ["string"],
  "phone": ["string"],
  "issue": [
    {
      "description": "string"
    }
  ]
}

Rules:
- Do not invent information.
- Return empty arrays if nothing is found.
- Do not include schema keywords like $ref, properties, type, $defs.
"""

text = "My Name is Himanshu Jha, I had a very bad experience with zomato. I had ordere chicken butter masala but got paneer chilli, I tried to reach customer care on 1800180011 using my contanct no. 7070987127, I also mailed them on issue@zomato.com using HimanshuPrincejha2001@Gmail.COM, but dont get any information."

user_prompt = f"""
Extract ONLY the customer's personal contact information.

Rules:
- Include customer name
- Include customer complaint/issues
- Include only phone numbers that belong to the customer.
- Include only email addresses that belong to the customer.
- Ignore company, restaurant, support, or customer-care phone numbers.
- Ignore company support email addresses.
- The contact information must identify or belong to the customer.

you have to use {text} for extracting the informations.

Return ONLY valid JSON
"""

system_message = {
    "role":"system",
    "content":system_prompt
}

user_message = {
    "role":"user",
    "content":user_prompt
}

response = client.chat.completions.create(
    model=model,
    messages=[system_message, user_message],
    response_format=response_format
)

result = response.choices[0].message.content

print("Raw API result:")
print(result)

# Parse the JSON string into the Pydantic model
ticket = Ticket.model_validate_json(result)

print("\nAccessing Pydantic Ticket fields directly:")
print("Name:", ticket.name)
print("Email:", ticket.email)
print("Phone:", ticket.phone)
print("Issue:", ticket.issue)

## playing with raw json

raw_json = result

print("\n==================")
print("\n using class ticekt")

import json
ticket_data = json.loads(raw_json)
ans = Ticket(**ticket_data)

print(ans)


