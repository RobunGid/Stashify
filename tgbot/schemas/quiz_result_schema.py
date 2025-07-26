from datetime import datetime

from pydantic import BaseModel, Field

class QuizResultSchema(BaseModel):
    id: str
    
    quiz_id: str
    quiz: "QuizSchema"
    
    user_id: str
    user: "UserSchema"
    
    completed_at: datetime
    percent: int
    
from user_schema import UserSchema
from quiz_schema import QuizSchema