import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
ollama_api_key = "ollama"

client = OpenAI(
    base_url=ollama_base_url,
    api_key=ollama_api_key
)

model = os.getenv("OLLAMA_MODEL")

class Resume(BaseModel):
    name: str
    email: str
    phone: int
    yoe: int
    linkedin: str
    github: str
    protfolio: str
    codingProfile: str
    achievements: str
    finalScore: int
    feedback: str
    skills: list

schema = Resume.model_json_schema()

response_format = {
    "type": "json_object"
}

reader = PdfReader("resume.pdf")
resume = ""
for page in reader.pages:
    resume += page.extract_text()

system_prompt = """
You are an expert HR AI assistant. Your task is to extract candidate details from a resume and evaluate their fit for a given Job Description.

Return ONLY valid JSON matching this exact structure:

based on {schema}

Rules:
1. Do not change key names or add extra nested objects.
2. 'yoe' (Years of Experience) must be a number.
3. 'finalScore' must be an integer from 0 to 100 based on how well the candidate meets minimum and preferred qualifications.
4. 'feedback' must explain why the score was given (matched vs missing skills).
5. All values must match their required type (string, integer, float, or list).
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

job_description = """
Job Area

Engineering Group, Engineering Group > Software Engineering

General Summary

As a leading technology innovator, Qualcomm pushes the boundaries of what's possible to enable next-generation experiences and drives digital transformation to help create a smarter, connected future for all. As a Qualcomm Software Engineer, you will design, develop, create, modify, and validate embedded and cloud edge software, applications, and/or specialized utility programs that launch cutting-edge, world class products that meet and exceed customer needs. Qualcomm Software Engineers collaborate with systems, hardware, architecture, test engineers, and other teams to design system-level software solutions and obtain information on performance requirements and interfaces.

Minimum Qualifications

 Bachelor's degree in Engineering, Information Systems, Computer Science, or related field.


Preferred Qualifications

 1+ year of experience with Programming Language such as C, C++, Java, Python, etc.
 1+ year of experience with Database Management Software.
 1+ year of experience with API.
 1+ year of work experience with Git, Perforce, or Source Code Management System.


Principal Duties And Responsibilities

 Applies Software knowledge to assist and support the design, development, creation, modification, and validation of embedded and cloud edge software, applications, and/or specialized utility programs.
 Analyzes user needs and software requirements.
 Designs and implements small software features for products and systems.
 Participates in the design, coding for small features, unit testing, minor debugging fixes, and integration efforts to ensure projects are completed on schedule.
 Assists in performing code reviews and regression tests as well as the triaging of issues to ensure the quality of code.
 Collaborates with others inside project team to accomplish project objectives.
 Writes technical documentation for Software projects.


Level Of Responsibility

 Works under supervision.
 Decision-making affects direct area of work and/or work group.
 Requires verbal and written communication skills to convey basic, routine factual information.
 Tasks require multiple steps which can be performed in various orders; some planning, problem-solving, and prioritization must occur to complete the tasks effectively.


Applicants: Qualcomm is an equal opportunity employer. If you are an individual with a disability and need an accommodation during the application/hiring process, rest assured that Qualcomm is committed to providing an accessible process. You may e-mail disability-accomodations@qualcomm.com or call Qualcomm's toll-free number found here. Upon request, Qualcomm will provide reasonable accommodations to support individuals with disabilities to be able participate in the hiring process. Qualcomm is also committed to making our workplace accessible for individuals with disabilities. (Keep in mind that this email address is used to provide reasonable accommodations for individuals with disabilities. We will not respond here to requests for updates on applications or resume inquiries).

Qualcomm expects its employees to abide by all applicable policies and procedures, including but not limited to security and other requirements regarding protection of Company confidential information and other confidential and/or proprietary information, to the extent those requirements are permissible under applicable law.

To all Staffing and Recruiting Agencies: Our Careers Site is only for individuals seeking a job at Qualcomm. Staffing and recruiting agencies and individuals being represented by an agency are not authorized to use this site or to submit profiles, applications or resumes, and any such submissions will be considered unsolicited. Qualcomm does not accept unsolicited resumes or applications from agencies. Please do not forward resumes to our jobs alias, Qualcomm employees or any other company location. Qualcomm is not responsible for any fees related to unsolicited resumes/applications.
"""

prompt = f"""
### Candidate Resume:
{resume}

---

### Job Description:
{job_description}

---

Task: Extract candidate details from the resume, compare them against the job description requirements, and return the populated JSON object.
"""


message_user = {
    "role": "user",
    "content": prompt
}

response = client.chat.completions.create(
    model=model,
    messages=[message_system, message_user],
    response_format=response_format
)

json_response = response.choices[0].message.content
print(json_response)
