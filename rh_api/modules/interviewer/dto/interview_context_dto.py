from pydantic import BaseModel
from typing import Optional, List



class CompanyContextDTO(BaseModel):
    """DTO representing the company's context."""
    company_id: str
    company_name: str
    industry: str
    location: str
    employees_count: int
    growth_strategy: str
    internal_mobility_policies: str
    available_trainings: List[str]
    performance_review_policy: str
    remote_work_policy: str
    benefits: List[str]

class EmployeeDTO(BaseModel):
    """DTO representing the employee's context."""
    employee_id: str
    employee_name: str
    role: str
    department: str
    years_in_company: int
    experience: int
    last_promotion_date: Optional[str] = None
    last_training: Optional[str] = None
    performance_feedback: Optional[str] = None
    key_responsibilities: str
    skills: List[str]
    current_projects: List[str]
    career_goals: Optional[str] = None
    manager: str

class InterviewContextDTO(BaseModel):
    """DTO combining both the employee and company context for the professional interview."""
    employee: EmployeeDTO
    company: CompanyContextDTO
    interview_type: str
    num_questions: int
