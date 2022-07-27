import asyncio

from helpers.filters import command
from config import BOT_NAME as bn, BOT_USERNAME as bu, SUPPORT_GROUP, OWNER_USERNAME as me, START_IMG
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("start") & filters.private & ~filters.group & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.delete()
    await message.reply_photo(
        photo=f"https://telegra.ph/file/1ebc3393692680b98c7ef.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 𝙃𝙚𝙡𝙡𝙤, 𝙄 𝘼𝙢 𝙎𝙪𝙥𝙚𝙧 𝙁𝙖𝙨𝙩 𝙈𝙪𝙨𝙞𝙘 𝙋𝙡𝙖𝙮𝙚𝙧
𝘽𝙤𝙩 𝙁𝙤𝙧 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙂𝙧𝙤𝙪𝙥𝙨 ...
┏━━━━━━━━━━━━━━━━━┓
┣★ 𝘾𝙧𝙚𝙖𝙩𝙤𝙧 : [𓆩 𝐂𝐎𝐃𝐄𝐑 𓆪](https://t.me/LEGEND_CODER)
┣★ 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 : [𝗝𝗮𝗶🇮🇳𝗛𝗶𝗻𝗱](https://t.me/JaiHindChatting)
┣★ 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 : [𝗥𝗬𝗠 𝗧𝗘𝗔𝗠](https://t.me/RYMOFFICIAL)
┗━━━━━━━━━━━━━━━━━┛

━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "•✯⭐ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ⭐✯•", url=f"https://t.me/BROKEN_MUSIC_ROBOT?startgroup=true"
                       ),
                  ],[
                    InlineKeyboardButton(
                        "•★🥀sᴏᴜʀᴄᴇ🥀★•", url=f"https://github.com/BANNA-XD143/Aaru_Music"
                    ),
                    InlineKeyboardButton(
                        "•✫❤️sᴜᴘᴘᴏʀᴛ❤️✫•", url=f"https://t.me/AARU_SUPPORT"
                    )
                ],[
                    InlineKeyboardButton(
                        "•✵📡ᴄʜᴀɴɴᴇʟ📡✵•", url="https://t.me/MISS_AARU_143"
                    ),
                    InlineKeyboardButton(
                        "•✞︎💥ᴅᴇᴠᴇʟᴏᴘᴇʀ💥✞︎︎︎•", url="https://t.me/BANNA_XD"
                    )]
            ]
       ),
    )

