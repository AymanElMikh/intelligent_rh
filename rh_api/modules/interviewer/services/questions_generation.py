import openai
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from db.mongodb import DBConnection 

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "promptsv2"

def load_prompt(interview_phase: str) -> str:
    """Load a prompt file from the PROMPT folder."""
    file_path = PROMPT_DIR / interview_phase / "prompt.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Error: The prompt file '{interview_phase}' was not found in {PROMPT_DIR}")
    
    return file_path.read_text(encoding="utf-8").strip()

def fetch_employee_and_company(employee_id: str):
    """Retrieve employee and company information from MongoDB."""
    db = DBConnection()
    
    employee_collection = db.get_collection("employees")
    employee = employee_collection.find_one({"employee_id": employee_id})
    
    if not employee:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")
    
    company_collection = db.get_collection("company_info")
    company = company_collection.find_one({})
    
    if not company:
        raise ValueError("Company information not found.")

    return employee, company

def format_content_prompt(content_prompt, context):
    """Replaces only dynamic placeholders while preserving static content."""
    for key, value in context.items():
        content_prompt = content_prompt.replace(f"{{{key}}}", str(value))
    return content_prompt

def clean_json_response(response_text: str) -> str:
    """Ensure JSON validity by stripping unwanted characters and validating structure."""
    try:
        cleaned_text = re.sub(r"```json|```", "", response_text).strip()

        if not cleaned_text:
            raise ValueError("OpenAI API returned an empty response.")

        response_data = json.loads(cleaned_text)

        if "interview_phase" not in response_data or "questions" not in response_data:
            raise ValueError("Missing 'interview_phase' or 'questions' key in OpenAI response.")

        return json.dumps(response_data, ensure_ascii=False, indent=2)

    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format from OpenAI response: {response_text}")

def generate_interview_questions(employee_id: str, interview_phase: str) -> str:
    """Generate structured interview questions for an employee using OpenAI."""
    try:
        system_prompt = load_prompt("system_prompt.txt")
        content_prompt = load_prompt(interview_phase)

        employee, company = fetch_employee_and_company(employee_id)

        context = get_custom_context(employee, company, interview_phase)

        formatted_content = format_content_prompt(content_prompt, context)

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_content}
            ],
            temperature=1,
            max_completion_tokens=6700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_text = response.choices[0].message.content.strip()

        print(f"🔹 OpenAI Raw Response: {response_text}")

        if not response_text:
            raise ValueError("OpenAI API returned an empty response.")

        return clean_json_response(response_text)

    except FileNotFoundError as e:
        raise ValueError(f"File Error: {str(e)}")
    except openai.OpenAIError as e:
        raise ValueError(f"OpenAI API Error: {str(e)}")
    except ValueError as ve:
        raise ValueError(f"Processing Error: {str(ve)}")

def get_custom_context(employee: dict, company: dict, interview_phase: str) -> dict:
    
    if interview_phase == "career_growth":
        return {
            "employee_name": employee.get("employee_name"),
            "role": employee.get("role"),
            "years_in_company": employee.get("years_in_company"),
            "last_training": employee.get("last_training"),
            "performance_feedback": employee.get("performance_feedback"),
            "skills": employee.get("skills"),
            "current_projects": employee.get("current_projects"),
            "num_questions": 10 
        }
    
    elif interview_phase == "technical":
        return {
            "employee_name": employee.get("employee_name"),
            "role": employee.get("role"),
            "skills": employee.get("skills"),
            "current_projects": employee.get("current_projects"),
            "experience": employee.get("experience"),
            "num_questions": 10
        }
    else:
        return {
            **employee,
            **company,
            "num_questions": 10
        }
