import os
import re
from time import sleep
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

def get_product_price(product):
    if product == "iphone 17":
        return 1000
    if product == "iphone 15":
        return 500
    return 0

def calculate(experssion):
    try:
        return eval(experssion)
    except:
        return "Cal errors !"

tools = {
    "get_product_price": get_product_price,
    "calculate": calculate
}

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculate(experssion)

IMPORTANT:
Call tools exactlty like these examples

Action: get_product_price("iphone 17")
Action: calculate(5000 - 1000)

Never write:
get_product_price(product = "iphone 17")

Never Write:
calculate(experssion = "5000 - 1000")

Follow these rules:
1. Decide what you need to do.
2. Call only one tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete give the result.

Format:

Thought: What you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):
    messages = [
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role":"user",
            "content":question
        }
    ]

    for step in range(5):
        print("\n=========")
        print("Step", step + 1)
        print("\n=========")

        response = client.chat.completions.create(
            model = model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        if "Final Answer" in answer:
            break

        #Find the Action
        match = re.search(
            r"Action: \s*(\w+)\((.*?)\)",
            answer
        )

        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)

            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"')

            #Run the tool
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)

            else :
                observation = "Tool not found"

            print("Observation :", observation)

            #Add LLM response to memory for remberning in next setp, LLm role is assistant
            messages.append({
                "role":"assistant",
                "content":answer
            })
            
            #Give tool result back to LLM
            messages.append({
                "role": "user",
                "content":"Observation: "+str(observation)
            })

            sleep(5)

            

prompt = """
I have 5000 rupees. What is the price of an iphone 17?
and how much money will I have left ?
"""

run_agent(prompt)