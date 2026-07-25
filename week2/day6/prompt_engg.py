import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
my_api_key = "ollama"

# Initialize OpenAI client pointed to Ollama
client = OpenAI(
    base_url=ollama_base_url,
    api_key=my_api_key
)

model = os.getenv("OLLAMA_MODEL")


def llm_ans(prompt) :
    message = {
        "role":"user",
        "content":prompt
    }

    messages = [message]

    response = client.chat.completions.create(
        model = model,
        messages=messages
    )

    ans = response.choices[0].message.content

    return ans

bad_prompty = """
This is a user complaint:
My laptop is not working.
handle this
"""

good_prompt1 = """
#ROLE:
You are a chat assistant who is assigned to handle user complaint in a mobile shop.
#TASK:
You have to classify the issue in a category.
#CONSTRAINTS:
You have to classify the issue in one of three categories -
1. Billing,
2. Return,
3. Technical
#OUTPUT FORMAT:
Your answer should be one word only. The one word shoud be one of the categories mentioned in constraint.
#EXAMPLE:
For a instance if user complain described abound refund then the category should be return.
#FALLBACK:
If the user complaint is not related to any of the three categories mentioned in constraint, then the answer should be OTHER.

This is a user complaint:
My laptop is not working.

classify this
"""

good_prompty = """
You are a strict text classification assistant for a Mobile Phone and Mobile Accessories Shop.
Your domain is STRICTLY limited to mobile phones, chargers, phone cases, screen protectors, and mobile shop billing/returns.

### Task
Classify the customer complaint provided inside the `<complaint>` tags into exactly ONE of the following categories:
1. `Billing` - Invoices, double charges, payment failures, or pricing disputes for mobile purchases.
2. `Return` - Requests to refund, exchange, or return mobile devices or accessories.
3. `Technical` - Software issues, broken screens, battery failures, or hardware defects specifically in mobile phones or mobile accessories.
4. `OTHER` - Any issue, query, or text that does not belong to a mobile phone, mobile accessory, or the mobile shop (e.g., laptops, home appliances, general conversations, or questions).

### Constraints
- Output EXACTLY one word from the list: [Billing, Return, Technical, OTHER].
- Do NOT output any preamble, explanation, markdown formatting (no bolding, no backticks), or punctuation. 
- Do NOT be conversational. Return the category name only.

### Examples
- Input: <complaint>I bought a charger yesterday but it isn't charging my iPhone.</complaint>
  Output: Technical
- Input: <complaint>I need a refund for this phone case.</complaint>
  Output: Return
- Input: <complaint>My laptop screen is cracked and won't turn on.</complaint>
  Output: OTHER
- Input: <complaint>Hi, how are you doing today?</complaint>
  Output: OTHER

### Customer Complaint
<complaint>
My laptop is not working.
</complaint>

Output:"""

print("--- Testing Unstructured Bad Prompt (bad_prompty) ---")
print(f"Output: {llm_ans(bad_prompty).strip()}")

print("\n--- Testing Structured Prompt (good_prompt1) ---")
print(f"Output: {llm_ans(good_prompt1).strip()}")

print("\n--- Testing Optimized Prompt (good_prompty) ---")
print(f"Output: {llm_ans(good_prompty).strip()}")