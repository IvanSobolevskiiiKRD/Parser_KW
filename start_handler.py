from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import requests
import base64
import request as rq
import Text as Text
import stark_kb as start_kb


router = Router()

class Answer_order(StatesGroup):
    id_worker = State()
    id_order = State()
    price = State()
    name_order = State()
    lead_time = State()
    answer = State()


#ГЛАВНОЕ МЕНЮ НАЧАЛО
@router.message(CommandStart())
async def start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args:
        option, id_worker, id_order = command.args.split("_")
        if option == "setworker":
            await state.set_state(Answer_order.id_order)
            await state.update_data(id_order=id_order)
            await state.update_data(id_worker=id_worker)
            await state.set_state(Answer_order.name_order)
            await message.answer(Text.name_zadacha)

@router.callback_query(F.data == "rerite_otklik")
async def start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Answer_order.answer)
    await callback.message.answer(text=Text.write_my_answer)

@router.callback_query(F.data == "accept_ai_otcklik")
async def start(callback: CallbackQuery, state: FSMContext):
    data_states = await state.get_data()

    data_worker = await rq.get_data_one_worker_by_id(data_states["id_worker"])
    data_worker = data_worker.__dict__

    await callback.message.answer(text=Text.send_otklik.format(data_worker["name"], data_worker["name_order"], data_states["price"],
                                                      data_states["lead_time"], data_states["answer"],),
                                                      reply_markup=start_kb.access_answer)

@router.callback_query(F.data == "cansel_otpravka")
async def start(callback: CallbackQuery, state: FSMContext):
    data_states = await state.get_data()
    await rq.edit_data_order(data_states["id_order"], "id_worker_respons", data_states["answer"])
    await rq.edit_data_order(data_states["id_order"], "price_worker", data_states["price"])
    await rq.edit_data_order(data_states["id_order"], "lead_time", data_states["lead_time"])
    await callback.message.answer(text=Text.cansel_otpravka)

@router.callback_query(F.data == "otpravka")
async def start(callback: CallbackQuery, state: FSMContext):
    data_states = await state.get_data()
    await rq.edit_data_order(data_states["id_order"], "answer_worker", data_states["id_worker"])
    await rq.edit_data_order(data_states["id_order"], "answer_worker", data_states["answer"])
    await rq.edit_data_order(data_states["id_order"], "price_worker", data_states["price"])
    await rq.edit_data_order(data_states["id_order"], "lead_time", data_states["lead_time"])
    await callback.message.answer(text=Text.otpravka)


@router.message(Answer_order.name_order)
async def start(message: Message, state: FSMContext):
    await state.update_data(name_order=message.text)
    await state.set_state(Answer_order.price)
    await message.answer(text=Text.price)

@router.message(Answer_order.price)
async def start(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Answer_order.lead_time)
    await message.answer(text=Text.col_days_nead)


@router.message(Answer_order.lead_time)
async def start(message: Message, state: FSMContext):
    await state.update_data(lead_time=message.text)
    await message.answer(text=Text.genereate_otclik)
    states_data = await state.get_data()
    data_order = await rq.get_data_one_order_by_id(states_data["id_order"])
    data_order = data_order.__dict__

    data_worker = await rq.get_data_one_worker_by_id(states_data["id_worker"])
    data_worker = data_worker.__dict__

    description_ai = data_order["description_ai"]

    description_ai = description_ai.encode('utf-8')
    description_ai = base64.b64encode(description_ai)
    description_ai = description_ai.decode('utf-8')


    #url = 'http://localhost:5678/webhook-test/ff8aa89e-dd2d-4ec9-8e1b-ce1d4c39137f'
    url = 'https://lokatekonet.beget.app/webhook/ff8aa89e-dd2d-4ec9-8e1b-ce1d4c39137f'
    data_to_send = {'description_ai': f"{description_ai}", 'user_name': data_worker["name"]}
    response = requests.get(url, json=data_to_send)

    answer_ai = response.json()
    answer_ai = answer_ai["answer"]
    answer_ai = base64.b64decode(answer_ai)
    answer_ai = answer_ai.decode('utf-8')

    await state.update_data(answer=answer_ai)
    await message.answer(text=Text.Answer.format(answer_ai), reply_markup=start_kb.otklik_answer)

@router.message(Answer_order.answer)
async def start(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data_states = await state.get_data()

    data_worker = await rq.get_data_one_worker_by_id(data_states["id_worker"])
    data_worker = data_worker.__dict__

    await message.answer(text=Text.send_otklik.format(data_worker["name"], data_worker["name_order"], data_states["price"],
                                                      data_states["lead_time"], data_states["answer"],),
                                                      reply_markup=start_kb.access_answer)