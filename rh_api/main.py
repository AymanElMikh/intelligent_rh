import json
from fastapi import FastAPI, HTTPException
from modules.interviewer.dto import InterviewContextDTO, InterviewResponseDTO, QuestionDTO
from modules.interviewer.services.questions_generation import generate_interview_questions

app = FastAPI()

@app.post("/generate-questions", response_model=InterviewResponseDTO)
def generate_questions(context: InterviewContextDTO):
    """
    Generate structured professional interview questions based on the employee's profile.
    """
    try:
        questions_json = generate_interview_questions(context)

        print("OpenAI API Response:", questions_json)

        parsed_response = json.loads(questions_json)

        if "interview_phase" not in parsed_response or "questions" not in parsed_response:
            raise ValueError("Missing 'interview_phase' or 'questions' key in OpenAI response.")

        questions_list = parsed_response["questions"]

        structured_questions = [
            QuestionDTO(id=idx + 1, type=q.get("type", "general"), question=q["question"])
            for idx, q in enumerate(questions_list)
        ]

        return InterviewResponseDTO(
            employee_name=context.employee_name,
            role=context.role,
            department=context.department,
            years_in_company=context.years_in_company,
            experience=context.experience,
            last_promotion_date=context.last_promotion_date,
            last_training=context.last_training,
            performance_feedback=context.performance_feedback,
            key_responsibilities=context.key_responsibilities,
            career_goals=context.career_goals,
            company_name=context.company_name,
            company_growth_strategy=context.company_growth_strategy,
            available_trainings=context.available_trainings,
            internal_mobility_policies=context.internal_mobility_policies,
            interview_type=context.interview_type,
            num_questions=context.num_questions,
            interview_phase=parsed_response["interview_phase"],
            questions=structured_questions
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse OpenAI response. Invalid JSON.")
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
