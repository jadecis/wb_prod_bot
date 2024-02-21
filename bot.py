from loader import aioDB, bot, dp
from src.database.aioconnection import loop
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
    
    await aioDB.user_launch()
    
    dp.include_router(start_comm.router)
    
    print("Bot is running")
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    loop.run_until_complete(main())