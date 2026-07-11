from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class ValidCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, object]:
        if callback.from_user is None or callback.message is None or callback.data is None:
            return False
        return {"message": callback.message}
