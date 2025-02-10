import json
from fastapi import FastAPI, HTTPException, Query
from modules.interviewer.services.questions_generation import generate_interview_questions

app = FastAPI()


@app.post("/generate-questions/{employee_id}/{interview_phase}", response_model=object)
def generate_questions(
    employee_id: str, 
    interview_phase: str
):
    """
    Generate structured interview questions for a specific employee, including the interview phase.
    """
    try:
        questions_json = generate_interview_questions(employee_id, interview_phase)

        print("OpenAI API Response:", questions_json)

        return questions_json

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse OpenAI response. Invalid JSON.")
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
