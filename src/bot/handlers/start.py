from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..res import replicas


router = Router()


@router.message(Command("start"))
async def command_start(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(replicas.get_replica("start"))
