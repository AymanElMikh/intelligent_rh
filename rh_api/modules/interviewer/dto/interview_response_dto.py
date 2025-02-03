from typing import List
from pydantic import BaseModel
from typing import List



class QuestionDTO(BaseModel):
    id: int
    type: str  # Example: "behavioral", "technical", "motivational"
    question: str

class InterviewResponseDTO(BaseModel):
    role: str
    experience: int
    interview_type: str
    num_questions: int
    questions: List[QuestionDTO]
