from typing import List
from pydantic import BaseModel
from typing import List



class QuestionDTO(BaseModel):
    id: int
    type: str
    question: str

class InterviewResponseDTO(BaseModel):
    questions: List[QuestionDTO]
