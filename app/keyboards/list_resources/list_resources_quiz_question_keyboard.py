from typing import Literal, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from schemas.quiz_question_schema import QuizQuestionBaseSchema
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory
from i18n.translate import t

class ListResourcesQuizQuestionCallbackFactory(CallbackData, prefix="lst_rsc_qstn"):
    action: Union[Literal["answer"], None]
    option_number: int
    question_number: int
    
def list_resources_quiz_question_keyboard(
        question: QuizQuestionBaseSchema, 
        question_number: int,
        page: int,
        resource_id: UUID4,
        user_lang: str = "en"
    ):
    builder = InlineKeyboardBuilder()
    for index, option in enumerate(question.options):
        if option.startswith("!"):
            option = option[1:]
        builder.button(text=option, callback_data=ListResourcesQuizQuestionCallbackFactory(action="answer", option_number=index, question_number=question_number))
        builder.adjust(1)
        
    builder.button(text=t("common.back", user_lang), callback_data=ListResourcesChooseResourceCallbackFactory(action="change_page", page=page, resource_id=resource_id))
    builder.adjust(1)
    return builder.as_markup()