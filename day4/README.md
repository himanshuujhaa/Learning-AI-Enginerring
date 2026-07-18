# Structured JSON Output Using Pydantic

Welcome to **Day 4** of the AI Engineering workspace! Today's work focused on transitioning from raw text LLM responses to structured JSON outputs, utilizing Pydantic models for validation, and iteratively refining prompt strategies to resolve common LLM parsing behaviors.

Below is a detailed log of the input, code iterations, and corresponding outputs of the `json_pydantic.py` script.

---

## 📋 Table of Contents
1. [Environment Setup](#environment-setup)
2. [Iteration 1: Simple LLM Text Generation](#iteration-1-simple-llm-text-generation)
3. [Iteration 2: Detailed Prompting & Pydantic Field Validation](#iteration-2-detailed-prompting-and-pydantic-field-validation)
4. [Iteration 3: Simplified Prompt & Cleaned Input](#iteration-3-simplified-prompt--cleaned-input)
5. [Iteration 4: Schema Enforcement Prompt & Successful Pydantic Validation (Latest Status)](#iteration-4-schema-enforcement-prompt--successful-pydantic-validation-latest-status)

---

## 🛠️ Environment Setup

Dependencies were configured inside `week1/day4/pyproject.toml` and synced with the workspace-wide virtual environment (`week1/.venv`):
```bash
uv add openai python-dotenv pydantic ollama
```

---

## 📂 Iteration 1: Simple LLM Text Generation
Initially, the script was set up to call the chat completions endpoint directly to extract information without specifying JSON requirements.

* **Code State**: Main calling logic structure was simple without any schemas defined.
* **Input Text**: 
  ```text
  "My name is Himanshu Jha, I had a very bad experince with flipkart services, I tried to conatct support team on contact information 6204376778 using my phone no 7070987129 and also mailed them using himanshi123@gmail.com and on support@flipkart.com"
  ```
* **Raw Output**:
  ```text
  The personal information extracted from the customer ticket is:
  * Name: Himanshu Jha
  * Phone number: 7070987129
  * Email address:
      + himanshi123@gmail.com
      + support@flipkart.com
  ```

---

## 📂 Iteration 2: Detailed Prompting and Pydantic Field Validation
To convert the unstructured text to structured data, we defined a Pydantic `Ticket` model and passed validation parameters. 

### Implementation Notes:
1. **Schema Injection Issue**: When passing the raw JSON schema `{schema}` directly to the prompt, local models (like `llama3`) get confused and echo the schema meta-properties (`properties`, `type`, `title`) in the response. We resolved this by explaining the keys in plain English.
2. **List-to-String Validation Failures**: Even when told to return a string, LLMs sometimes output collections (e.g. `["7070987129"]`). We used Pydantic `@field_validator` to safely unpack these lists.
3. **Filtering Corporate Information**: Specific guidelines were added to prevent corporate emails (like `support@flipkart.com`) and contact numbers (like `6204376778`) from leaking into the user's personal fields.

### Code Snippet:
```python
class Ticket(BaseModel):
    name: str
    email: str
    phone: str
    issue: str

    @field_validator('email', 'phone', mode='before')
    @classmethod
    def convert_list_to_string(cls, v):
        if isinstance(v, list):
            return v[0] if v else ""
        return v
```

### Output:
```json
{
  "name": "Himanshu Jha",
  "email": ["himanshi123@gmail.com", "support@flipkart.com"], 
  "phone": ["7070987129"],
  "issue": "Summarize the customer's complaint here (bad experience with flipkart services)"
}
```
* **Validation Result**: Successfully parsed and validated into Pydantic model (`name='Himanshu Jha'`, `phone='7070987129'`, `email='himanshi123@gmail.com'`).

---

## 📂 Iteration 3: Simplified Prompt & Cleaned Input
In the third iteration, the input text was cleaned of corporate support info at the source, the system prompt was shortened to refer to the schema, and Pydantic validation was commented out.

### Execution Output:
```json
{ 
  "name": "Himanshu Jha", 
  "phone_number": "7070987129", 
  "email": "himanshi123@gmail.com" 
}
```
*(Note: Because the prompt was highly simplified and lacked specific constraint guidelines, the LLM returned `phone_number` instead of `phone` and omitted `issue`, causing a ValidationError when Pydantic validation was uncommented.)*

---

## 📂 Iteration 4: Schema Enforcement Prompt & Successful Pydantic Validation (Latest Status)
In the final iteration, the system prompt was modified to strictly enforce the exact field keys without passing the complex JSON schema syntax that confused the LLM. Validation was performed by deserializing the JSON response and instantiating the Pydantic `Ticket` model.

### Current Code:
```python
# Structured JSON Output Using Pydantic

import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, field_validator
from typing import Union, List

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"

client = OpenAI(
    base_url = ollama_base_url,
    api_key = my_api_key
)

model = os.getenv("OLLAMA_MODEL")

class Ticket(BaseModel):
    name: str
    email: str
    phone: str
    issue: str

schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

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

# Input Text (Cleaned of corporate support contacts)
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

import json
raw_json = json_response
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print("name : " + ticket.name)
print("phone : " + ticket.phone)
print("email : " + ticket.email)
print("issue : " + ticket.issue)    
```

### Successful Run Output:
```text
{
    "name": "Himanshu Jha",
    "email": "himanshi123@gmail.com",
    "phone": "7070987129",
    "issue": "very bad experince with flipkart services"
}
name : Himanshu Jha
phone : 7070987129
email : himanshi123@gmail.com
issue : very bad experince with flipkart services
```
