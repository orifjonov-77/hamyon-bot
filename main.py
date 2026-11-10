import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from database import init_db
from handlers import router

# .env faylini yuklash
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    # Log sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    if not TOKEN:
        logging.error("XATOLIK: .env faylida BOT_TOKEN topilmadi yoki bo'sh! Iltimos, .env fayliga bot tokenini kiriting.")
        sys.exit(1)

    # SQLite bazani ishga tushirish (jadvallarni yaratish)
    init_db()
    logging.info("Ma'lumotlar bazasi (SQLite) tayyorlandi.")

    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Handler routerini ulash
    dp.include_router(router)

    logging.info("Bot ishga tushdi va xabarlarni qabul qilishga tayyor...")

    # Bot boshlanishidan oldin to'planib qolgan eski xabarlarni o'chirish (drop pending updates)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
