from pydantic import BaseModel
from typing import Optional


class InterviewContextDTO(BaseModel):
    employee_name: str
    role: str
    department: str
    years_in_company: int
    experience: int
    last_promotion_date: Optional[str] = None
    last_training: Optional[str] = None
    performance_feedback: Optional[str] = None
    key_responsibilities: str
    career_goals: Optional[str] = None
    company_name: str
    company_growth_strategy: str
    available_trainings: str
    internal_mobility_policies: str
    interview_type: str
    num_questions: int