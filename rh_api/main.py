import json
from fastapi import FastAPI, HTTPException, Query
from modules.interviewer.dto import InterviewResponseDTO, QuestionDTO
from modules.interviewer.services.questions_generation import generate_interview_questions
from pymongo import MongoClient
from db.mongodb import DBConnection

app = FastAPI()

@app.post("/generate-questions/{employee_id}", response_model=InterviewResponseDTO)
def generate_questions(
    employee_id: str, 
    interview_phase: str = Query("career_growth", description="The interview phase to generate questions for")
):
    """
    Generate structured interview questions for a specific employee, including the interview phase.
    """
    try:
        questions_json = generate_interview_questions(employee_id, interview_phase)

        print("OpenAI API Response:", questions_json)

        parsed_response = json.loads(questions_json)

        if "interview_phase" not in parsed_response or "questions" not in parsed_response:
            raise ValueError("Missing 'interview_phase' or 'questions' key in OpenAI response.")

        questions_list = parsed_response["questions"]

        structured_questions = [
            QuestionDTO(
                id=idx + 1,
                type=q.get("type", "general"),
                question=q["question"]
            )
            for idx, q in enumerate(questions_list)
        ]

        return InterviewResponseDTO(
            interview_phase=parsed_response["interview_phase"],
            questions=structured_questions
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse OpenAI response. Invalid JSON.")
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
