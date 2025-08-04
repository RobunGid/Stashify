from database.orm import AsyncSessionLocal
from database.models.quiz import QuizModel
from schemas.quiz_schema import QuizSchema
from database.models.quiz_question import QuizQuestionModel

async def create_quiz(quiz_data: QuizSchema):
    async with AsyncSessionLocal() as session:
        quiz = QuizModel(**quiz_data.model_dump(exclude=("questions", "resource")))
        quiz_questions = [QuizQuestionModel(**quiz_question_data.model_dump(exclude=("quiz",))) for quiz_question_data in quiz_data.questions]
        session.add(quiz)
        session.add_all(quiz_questions)
        await session.commit()