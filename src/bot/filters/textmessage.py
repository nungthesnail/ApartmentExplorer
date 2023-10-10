from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextMessage(BaseFilter):
    def __init__(self, msg: str):
        self.msg = msg.lower()

    async def __call__(self, message: Message) -> bool:
        return self.msg == message.text.lower()

