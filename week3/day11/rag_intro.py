import os
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


# step1 :- create knowledge base
knowledge_base = {
    "striver":"Raj Vikramaditya, also known as Striver, is an Indian EdTech creator, who had worked at google, media.net previously.",
    "actual name":"Raj Vikramaditya"
}

# step2 :- retrieval (fetch relevant facts)
def reterival_info(question):
    question = question.lower()
    if "striver" in question:
        return knowledge_base.get("striver")
    elif "actual name" in question or "name" in question:
        return knowledge_base.get("actual name")
    else:
        return None

def ask_llm(question):
    # step3 :- retrieve matching context for the user's question
    context = reterival_info(question)

    # step4 :- prompt augmentation (inject context into system prompt)
    sys_prompt = f"""answer in one line. Answer only based on this Context, do not Hallucinate. Context: {context}"""

    system_message = {
        "role":"system",
        "content":sys_prompt
    }

    message = {
        "role":"user",
        "content":question
    }

    messages = [system_message, message]

    # step5 :- generation (send augmented query to LLM)
    ans = client.chat.completions.create(
        model = model,
        messages=messages,
        max_tokens=2200
    )

    return ans.choices[0].message.content

question = "who is striver ?"

ans = ask_llm(question)
print(ans)