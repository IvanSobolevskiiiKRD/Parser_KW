from aiogram import Bot, Dispatcher
import asyncio
from Token import TOKEN
from models import async_main
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
import start_handler
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    


async def run_bot():
    await async_main()
    dp = Dispatcher()
    dp.include_router(start_handler.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())