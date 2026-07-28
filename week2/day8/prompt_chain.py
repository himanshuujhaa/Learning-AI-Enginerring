import os
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

JD = """
We are hiring a backend python developer.

Requirenments:
- Strong Python
- FAST API or Django
- PostgresSQL
- Docker
- AWS
- Rest APIs
- 2+ yrs of experience
"""

RESUME = """
Name: 
Himanshu Jha

Experience: 
4 years as a Software Developer

Skills:
Python, Java, FastAPIs, MySQL, Docker, Rest APIs

Projects:
Build a food delivery backend using FastAPIs & MySQL.

Deployed applicatio using docker.
"""

def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role":"system",
        "content":system_prompt
    }

    user_message = {
        "role":"user",
        "content":user_prompt
    }

    messages = [system_message, user_message]
    
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message.content

def resume_extractor():
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills, no other information. Do not invent any skills by yourself.
    """

    user_prompt = f"""
    This is Candidate Resume:

    {RESUME}
    
    Extract Skills:    
    """

    return ask_llm(system_prompt, user_prompt)

def JD_extractor():
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the Job description provided.
    Only return the skills, no other information. Do not invent any skills by yourself.
    """

    user_prompt = f"""
    This is Job Description:

    {JD}
    
    Extract Skills:    
    """

    return ask_llm(system_prompt, user_prompt)

def match_skills(resume_skills, jd_skills):
    system_prompt = """
    You are a professional HR assistant. Compare the candidate skills with the skills required in the job description & produce a final score between 1 and 100.
    also produce a short verdict weather the candidate is good fit for a role.
    """

    user_prompt = f"""
    Compare & match the skills:
    Resume Skills: {resume_skills}
    JD Skills: {jd_skills}
    """

    return ask_llm(system_prompt, user_prompt)

candidate = resume_extractor()
sleep(5)
print(candidate)

jd = JD_extractor()
sleep(5)
print(jd)

score = match_skills(candidate, jd)
sleep(5)
print(score)
    