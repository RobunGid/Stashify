from typing import Literal, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from schemas.quiz_question_schema import QuizQuestionBaseSchema

class ListResourcesQuizQuestionCallbackFactory(CallbackData, prefix="lst_rsc_qstn"):
    action: Union[Literal["answer"], None]
    option_number: int
    question_number: int
    
def list_resources_quiz_question_keyboard(
        question: QuizQuestionBaseSchema, 
        question_number: int 
    ):
    builder = InlineKeyboardBuilder()
    for index, option in enumerate(question.options):
        builder.button(text=option, callback_data=ListResourcesQuizQuestionCallbackFactory(action="answer", option_number=index, question_number=question_number))