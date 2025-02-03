import openai
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define base paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompts"

def load_prompt(filename: str) -> str:
    """Load a prompt file from the PROMPT folder."""
    file_path = PROMPT_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Error: The prompt file '{filename}' was not found in {PROMPT_DIR}")
    
    return file_path.read_text(encoding="utf-8").strip()

def ensure_filled_values(employee_context):
    """Ensure all required fields in the employee context are filled with default values."""
    
    defaults = {
        "employee_name": "Not Provided",
        "role": "Not Provided",
        "department": "Not Provided",
        "years_in_company": 0,
        "experience": 0,
        "last_promotion_date": "No recent promotion",
        "last_training": "No training recorded",
        "performance_feedback": "No feedback available",
        "key_responsibilities": "Not specified",
        "career_goals": "Not defined",
        "company_name": "Company Confidential",
        "company_growth_strategy": "No strategy shared",
        "available_trainings": "No training programs available",
        "internal_mobility_policies": "No mobility policy",
        "interview_type": "General Review",
        "num_questions": 5
    }

    return {field: getattr(employee_context, field, defaults[field]) or defaults[field] for field in defaults}


def clean_json_response(response_text: str) -> str:
    """Ensure JSON validity by stripping unwanted characters and validating structure."""
    try:
        # Remove unwanted markdown formatting
        cleaned_text = re.sub(r"```json|```", "", response_text).strip()

        if not cleaned_text:
            raise ValueError("OpenAI API returned an empty response.")

        response_data = json.loads(cleaned_text)

        if "interview_phase" not in response_data or "questions" not in response_data:
            raise ValueError("Missing 'interview_phase' or 'questions' key in OpenAI response.")

        return json.dumps(response_data, ensure_ascii=False, indent=2)

    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format from OpenAI response: {response_text}")

def format_content_prompt(content_prompt, filled_context):
    """
    Replaces only the dynamic placeholders in the content prompt while preserving static content.
    """

    placeholders = [
        "employee_name", "role", "department", "years_in_company", "experience",
        "last_promotion_date", "last_training", "performance_feedback",
        "key_responsibilities", "career_goals", "company_name",
        "company_growth_strategy", "available_trainings", "internal_mobility_policies",
        "num_questions"
    ]

    for key in placeholders:
        content_prompt = content_prompt.replace(f"{{{key}}}", str(filled_context[key]))

    return content_prompt


def generate_interview_questions(employee_context) -> str:
    """Generate structured interview questions using OpenAI's API."""
    try:
        system_prompt = load_prompt("system_prompt.txt")
        content_prompt = load_prompt("content_prompt.txt")

        filled_context = ensure_filled_values(employee_context)
        formatted_content = format_content_prompt(content_prompt, filled_context)

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_content}
            ]
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
