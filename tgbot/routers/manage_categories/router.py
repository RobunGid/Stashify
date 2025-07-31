from aiogram import Router

router = Router()

from .main_handlers import *
from .create_category_handlers import *
from .delete_category_handlers import *
from .edit_category_handlers import *