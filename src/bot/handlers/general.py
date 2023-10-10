from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from .. import resultgenerator
from ..keyboards import generalkeyboards
from .. import states
from ..res import replicas


router = Router()


@router.message(Command("begin"))
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        replicas.get_replica("selecting_action"),
        reply_markup=generalkeyboards.keyboard_selecting_action()
    )
    await state.set_data({"action": None, "price": None, "platform": None})
    await state.set_state(states.BeginStates.selecting_action)


@router.message(states.BeginStates.selecting_action)
async def action_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    values = replicas.get_inputs("selecting_action")
    if message.text.capitalize() not in values or not data:
        return

    data["action"] = values.index(message.text.capitalize())

    if data["action"] == 2:
        await message.answer(
            replicas.get_replica("selecting_price"),
            reply_markup=generalkeyboards.keyboard_selecting_price()
        )
        await state.set_state(states.BeginStates.selecting_price)
        await state.set_data(data)

    else:
        await message.answer(resultgenerator.answer(data))
        await state.clear()


@router.message(states.BeginStates.selecting_price)
async def price_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    values = replicas.get_inputs("selecting_price")
    if message.text.capitalize() not in values or not data:
        return

    data["price"] = values.index(message.text.capitalize())

    await message.answer(
        replicas.get_replica("selecting_platform"),
        reply_markup=generalkeyboards.keyboard_selecting_platform()
    )
    await state.set_state(states.BeginStates.selecting_platform)
    await state.set_data(data)


@router.message(states.BeginStates.selecting_platform)
async def platform_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    values = replicas.get_inputs("selecting_platform")
    if message.text.capitalize() not in values or not data:
        return

    data["platform"] = message.text.capitalize()

    await message.answer(resultgenerator.answer(data))
    await state.clear()
