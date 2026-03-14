from pyrogram import Client, filters
import os
import yt_dlp
import re
import aiohttp
import urllib.parse

API_ID = 21123122
API_HASH = 'a4d997c1f7c46a88908a2ee7b7113eab'
BOT_TOKEN = '7979427548:AAGPqNOYnLf7hGaofOYb3FNBeu1MC_viwC0'


bot = Client("Audio_adminbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def clean_filename(name):
    # Noto'g'ri belgilarni olib tashlash
    return re.sub(r'[\\/*?:"<>|]', "", name)

@bot.on_message(filters.command("help"))
async def help_handler(_, message):
    await message.reply(
        "ℹ️ <b>Foydalanish qo‘llanmasi</b>\n\n"
        "<b>🎵 MP3 yuklab olish:</b>\n"
        "1. YouTube havolasini yuboring (masalan: https://youtu.be/abc123)\n"
        "2. Bot MP3 formatga aylantiradi\n"
        "3. Sizga audio faylni yuboradi\n\n"
        "<b>🖼 Rasm yaratish:</b>\n"
        "/rasm &lt;matn&gt; — matn asosida AI yordamida rasm yaratadi\n"
        "Misol: /rasm quyoshli dengiz manzarasi\n\n"
        "🛠 Yuklanmagan bo‘lsa, video bloklangan yoki fayl hajmi juda katta bo‘lishi mumkin.",
        parse_mode="html"
    )

@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply(
        "👋 Salom! Quyidagi buyruqlardan foydalanishingiz mumkin:\n\n"
        "🎵 YouTube havolasini yuboring — MP3 yuklab olish uchun\n"
        "🖼 /rasm <matn> — matn asosida rasm yaratish"
    )


@bot.on_message(filters.command("rasm"))
async def image_generator(_, message):
    prompt = " ".join(message.command[1:]).strip()
    if not prompt:
        return await message.reply("❌ Iltimos, rasm uchun matn kiriting.\nMisol: /rasm tog'li manzara")

    msg = await message.reply("🎨 Rasm tayyorlanmoqda, kuting...")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                if resp.status != 200:
                    return await msg.edit(f"❌ Rasm yaratishda xatolik yuz berdi (HTTP {resp.status}). Qayta urinib ko'ring.")
                image_bytes = await resp.read()

        await msg.delete()
        await message.reply_photo(photo=image_bytes, caption=f"🖼 {prompt}")

    except Exception:
        await msg.edit("❌ Rasm yaratishda kutilmagan xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

@bot.on_message(filters.private & filters.text)
async def mp3_downloader(_, message):
    url = message.text.strip()
    if "youtu" not in url:
        return await message.reply("❌ Iltimos, to‘g‘ri YouTube havolasini yuboring.")

    msg = await message.reply("🔄 MP3 tayyorlanmoqda, kuting...")

    try:
        out_dir = "downloads"
        os.makedirs(out_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = clean_filename(info.get('title', 'audio'))
            filename = os.path.join(out_dir, title + ".mp3")

        await msg.edit("✅ MP3 tayyor! Yuborilmoqda...")

        # Faylni ochib yuborish
        with open(filename, "rb") as f:
            await message.reply_audio(audio=f, caption=f"🎵 {title}")

        os.remove(filename)

    except Exception as e:
        await msg.edit(f"❌ Xatolik:\n{str(e)}")

bot.run()