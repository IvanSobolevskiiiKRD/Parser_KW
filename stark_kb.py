from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

otklik_answer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🤖 Выбрать вариант от ИИ 🤖', callback_data="accept_ai_otcklik")],
    [InlineKeyboardButton(text='🙎🏻‍♂️ Написать свой вариант отклика 🙎🏻‍♂️', callback_data="rerite_otklik")]
])

access_answer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Отправить ✅', callback_data="otpravka")],
    [InlineKeyboardButton(text='❌ Отменить ❌', callback_data="cansel_otpravka")]
])