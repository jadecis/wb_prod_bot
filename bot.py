from loader import dp, bot
from aiogram.types import BotCommand
from src.commands import start_comm
import asyncio


# async def on_startup(dispatcher):
#     # asyncio.create_task(scheduler())
#     pass

async def main():
    await bot.set_my_commands([
        BotCommand(command= "start", description="restart bot"),
    ])
    
    dp.include_router(start_comm.router)
    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())