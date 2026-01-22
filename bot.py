import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")  # Railwaydan olinadi

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Salom!\n\n"
        "Instagramdan video/muzika yuklab olish uchun link yuboring:\n\n"
        "Masalan:\n"
        "• https://www.instagram.com/reel/C123abc...\n"
        "• https://www.instagram.com/p/ABC123...\n\n"
        "Bot video + audio bilan yuklab beradi."
    )

@dp.message()
async def download_instagram(message: Message):
    url = message.text.strip()
    
    if "instagram.com" not in url:
        await message.answer("❌ Instagram linkini yuboring!")
        return

    await message.answer("⏳ Yuklanmoqda... Bir oz kuting")

    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        video_file = FSInputFile(filename)
        
        await message.answer_video(
            video=video_file,
            caption=f"✅ Yuklandi!\n\n🔗 {url}"
        )

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}\nLinkni tekshiring.")

async def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
