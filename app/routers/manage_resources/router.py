from aiogram import Router

router = Router()

from .create_resource_handlers import *
from .delete_resource_handlers import *
from .edit_resource_handlers import *
from .main_handlers import *