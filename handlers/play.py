
import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
from youtube_search import YoutubeSearch
import converter
from datetime import datetime
from time import time
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: MR~BANNA-KING-xD° (@BANNA_XD)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command("play")
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):

    lel = await message.reply("🔥")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Aaru"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit("<b>ᴀᴅᴅ ᴍᴇ ᴀᴅᴍɪɴ ғɪʀsᴛ...🎀</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**ᴀᴀʀᴜ ᴀssɪsᴛᴀɴᴇᴄ ᴊᴏɪɴ ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ**"
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>❰ғʟᴏᴏᴅ 😒 ᴡᴀɪᴛ ᴇʀʀᴏʀ 😔❱</b>\nʜᴇʏ ᴀᴀʀᴜ ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴜʟᴅɴ'ᴛ ᴊᴏɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴜᴇ ᴛᴏ ʜᴇᴀᴠʏ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ . ᴍᴀᴋᴇ sᴜʀᴇ ᴜsᴇʀʙᴏᴛ ɪᴅ ɴᴏᴛ ʙᴀɴɴᴇᴅ 😔 ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ 😎🤟ʟᴀᴛᴇʀ :) "
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>❰ᴀᴀʀᴜ🇽 ʀᴏʙᴏᴛ❱ ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴛʜɪs ᴄʜᴀᴛ' ᴀsᴋ ᴀᴅᴍɪɴ ᴛᴏ sᴇɴᴅ /ᴊᴏɪɴ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀ ғɪʀsᴛ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ɪᴛ 😎🤟</i>"
        )
        return

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❰ᴠɪᴅᴇᴏ❱ ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ❤️🤞"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/45dbab70385b8dbdf6dc9.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="•★ᴄʜᴀɴɴᴇʟ★•", url=f"https://t.me/MISS_AARU_143"
                    ),
                    InlineKeyboardButton(text="•✰sᴜᴘᴘᴏʀᴛ✰•", url=f"https://t.me/love_birds_group"),
                ],[
                    InlineKeyboardButton(
                       text="•✯ᴏᴡɴᴇʀ✯•",url=f"https://t.me/BANNA_XD"
                    ),
                    InlineKeyboardButton(
                      text="•✵ɢʀᴏᴜᴘ✵•",url=f"https://t.me./LOVE_BIRDS_123"
                    ),
                 ]   
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
                [
                    [
                           InlineKeyboardButton(
                              text="•★ᴄʜᴀɴɴᴇʟ★•", url=f"https://t.me/MISS_AARU_143"
                           ),
                           InlineKeyboardButton(text="•✰sᴜᴘᴘᴏʀᴛ✰•", url=f"https://t.me/love_birds_group"),
                    ],[
                           InlineKeyboardButton(
                              text="•✯ᴏᴡɴᴇʀ✯•", url=f"https://t.me/BANNA_XD"
                           ),
                           InlineKeyboardButton(
                              text="•✵ɢʀᴏᴜᴘ✵•", url=f"https://t.me./LOVE_BIRDS_123"
                          ),
                     ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/9ae1b33912d9e5f38c353.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="•★ᴄʜᴀɴɴᴇʟ★•", url=f"https://t.me/MISS_AARU_143"
                        ),
                        InlineKeyboardButton(text="•✰sᴜᴘᴘᴏʀᴛ✰•", url=f"https://t.me/love_birds_group"),
                   ],[    
                        InlineKeyboardButton(
                            text="•✯ᴏᴡɴᴇʀ✯•", url=f"https://t.me/BANNA_XD"
                        ),
                        InlineKeyboardButton(
                           text="•✵ɢʀᴏᴜᴘ✵•", url=f"https://t.me/LOVE_BIRDS_123"
                        ),
                    ]
                ]
            )
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❰ᴠɪᴅᴇᴏ❱ ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ❤️🤞"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("**ᴡʜᴀᴛ's ᴛʜᴇ️ sᴏɴɢ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ..❄**")
        await lel.edit("🔥**ʟᴏᴅɪɴɢ sᴏɴɢ..**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🔥**ᴘʀᴏᴄᴇssɪɴɢ sᴏᴜɴᴅ..**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit("sᴘᴇʟɪɴɢ ᴘʀᴏʙʟᴇᴍ...")
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="•★ᴄʜᴀɴɴᴇʟ★•", url=f"https://t.me/MISS_AARU_143"
                    ),
                    InlineKeyboardButton(text="•✰sᴜᴘᴘᴏʀᴛ✰•", url=f"https://t.me/AARU_SUPPORT"),
               ],[
                    InlineKeyboardButton(
                       text="•✯ᴏᴡɴᴇʀ✯•", url=f"https://t.me/BANNA_XD"
                    ),
                    InlineKeyboardButton(
                       text="•✵ɢʀᴏᴜᴘ✵•", url=f"https://t.me/LOVE_BIRDS_123"
                    ),
                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❰ᴠɪᴅᴇᴏ❱ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ❤️🤞"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
 
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**s❣️ᴏɴɢ:** {}\n**🥀ᴅᴜʀᴀᴛɪᴏɴ:** {} ᴍɪɴ\n**ᴀ👿ᴅᴅᴇᴅ ʙʏ:** {}\n\n**ᴘᴏsɪᴛɪᴏɴ:** {}".format(
                title,
                duration,
                message.from_user.mention(),
                position,
            ),
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**❣️sᴏɴɢ:** {}\n**🥀ᴅᴜʀᴀᴛɪᴏɴ:** {} ᴍɪɴ\n**👿ᴀᴅᴅᴇᴅ ʙʏ:** {}\n\n**🦋ɴᴏᴡ ᴘʟᴀʏɪɴɢ ᴀᴛ `{}`...**".format(
                title, duration, message.from_user.mention(), message.chat.title
            ),
        )
        os.remove("final.png")
        return await lel.delete()

