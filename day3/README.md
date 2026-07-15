# Day 3: Local LLM Integration, Token Usage & Generation Limits

Welcome to **Day 3** of the AI Engineering workspace! Today's work focused on setting up a local LLM integration using Ollama, interacting with it using the OpenAI SDK, tracking token counts, limiting response lengths, and inspecting execution termination reasons.

---

## 📋 Table of Contents
1. [Environment Setup](#environment-setup)
2. [Configuration](#configuration)
3. [File Structure & Code](#file-structure--code)
4. [How to Run](#how-to-run)
5. [Sample Output & Metrics](#sample-output--metrics)

---

## 🛠️ Environment Setup

We configured a Python 3.11 virtual environment and installed the required SDKs to make API requests to local or remote LLMs.

### 1. Initialize Virtual Environment
Created a virtual environment using `uv`:
```bash
uv venv --python 3.11
source .venv/bin/activate
```

### 2. Install Dependencies
We installed `python-dotenv` for loading environment configurations and `openai` as the API client:
```bash
uv pip install python-dotenv openai
```

---

## ⚙️ Configuration

The project utilizes environment variables defined in a `.env` file at the workspace root to customize the LLM server's endpoint and the target model:

* **`.env` contents:**
  ```env
  OLLAMA_BASE_URL=http://localhost:11434/v1
  OLLAMA_MODEL=llama3:latest
  ```

---

## 📂 File Structure & Code

### `tokens.py`
This script loads configuration variables, initializes the OpenAI client to point to the local Ollama instance, sends a sequence of prompts (limiting completions to 100 tokens), and monitors the tokens consumed along with the finish reason (e.g., `stop` or `length`).

```python
# Tokenizer implementation for Day 3

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"  # Ollama doesn't require a real API key

client = OpenAI(
    base_url = ollama_base_url,
    api_key = my_api_key
)

model = os.getenv("OLLAMA_MODEL")

# Define Prompts
prompt1 = "Hey There !"
prompt2 = "Explain the use of Dynamic Programing in details"
prompt3 = "What is recursion ?"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message_user = {
        "role": "user",
        "content": prompt
    }
    
    # Request completion from Ollama (limiting response to 100 tokens)
    response = client.chat.completions.create(
        model = model,
        messages = [message_user],
        max_tokens = 100
    )

    # Extract token usage metadata
    usage = response.usage
    finish_reason = response.choices[0].finish_reason

    print(f"Prompt: {prompt} ;- User Tokens : {usage.prompt_tokens} and LLM tokens : {usage.completion_tokens} , total tokens :- {usage.total_tokens} Finish Reason = {finish_reason}")
```

---

## 🚀 How to Run

1. Make sure your local **Ollama** app/service is running.
2. Download/pull the target model if you haven't already:
   ```bash
   ollama pull llama3:latest
   ```
3. Run the script:
   ```bash
   python3 tokens.py
   ```

---

## 📊 Sample Output & Metrics

Executing `python3 tokens.py` produces token metrics and finish reasons for each prompt:

```text
Prompt: Hey There ! ;- User Tokens : 13 and LLM tokens : 27 , total tokens :- 40 Finish Reason = stop
Prompt: Explain the use of Dynamic Programing in details ;- User Tokens : 20 and LLM tokens : 100 , total tokens :- 120 Finish Reason = length
Prompt: What is recursion ? ;- User Tokens : 14 and LLM tokens : 100 , total tokens :- 114 Finish Reason = length
```

### Understanding the Metrics:
* **`User Tokens`**: Number of tokens in your prompt message.
* **`LLM tokens`**: Number of tokens generated in the response.
* **`Finish Reason`**:
  * `stop`: The LLM completed its response naturally.
  * `length`: The LLM response was cut off because it reached the limit set by `max_tokens = 100`.

