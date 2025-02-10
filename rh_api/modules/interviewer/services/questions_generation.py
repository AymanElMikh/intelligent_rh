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

def load_system_prompt() -> str:
    """Load a system prompt file from the PROMPT folder."""
    file_path = PROMPT_DIR / "system_prompt.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Error: The prompt file system_prompt.txt was not found in {PROMPT_DIR}")
    
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


def parse_interview_response(json_data):
    """
    Parses the JSON data containing interview phases and questions.
    Returns a structured summary.
    """
    try:
        if isinstance(json_data, str):
           return  json.loads(json_data)
        elif isinstance(json_data, dict):
           return  json_data
        else:
            raise ValueError("Invalid input type: expected str or dict.")

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Error parsing response: {str(e)}")

def generate_interview_questions(employee_id: str, interview_phase: str) -> str:
    """Generate structured interview questions for an employee using OpenAI."""
    try:
        system_prompt = load_system_prompt()
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

        return parse_interview_response(response_text)

    except FileNotFoundError as e:
        raise ValueError(f"File Error: {str(e)}")
    except openai.OpenAIError as e:
        raise ValueError(f"OpenAI API Error: {str(e)}")
    except ValueError as ve:
        raise ValueError(f"Processing Error: {str(ve)}")

def get_custom_context(employee: dict, company: dict, interview_phase: str) -> dict:
    
    if interview_phase == "career_review":
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
    
    elif interview_phase == "career_perspectives":
        return {
            "employee_name": employee.get("employee_name"),
            "role": employee.get("role"),
            "years_in_company": employee.get("years_in_company"),
            "skills": employee.get("skills"),
            "current_challenges": employee.get("current_challenges"),
            "career_goals": employee.get("career_goals"),
            "leadership_interest": employee.get("leadership_interest"),
            "training_needs": employee.get("training_needs"),
            "num_questions": 10
        }
    elif interview_phase == "professional_development_plan":
        return {
            "employee_name": employee.get("employee_name"),
            "role": employee.get("role"),
            "years_in_company": employee.get("years_in_company"),
            "core_strengths": employee.get("skills"),
            "professional_goals": employee.get("career_goals"),
            "training_and_development_needs": employee.get("training_needs"),
            "mentorship_interest": employee.get("mentorship_interest"),
            "potential_growth_areas": employee.get("potential_growth_areas"),
            "company_development_opportunities": company.get("development_opportunities"),
            "num_questions": 10
        }

    else:
        return {
            **employee,
            **company,
            "num_questions": 10
        }