
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
    return image.resize((newWidth, newHeight))


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
    draw.text((190, 550), f"Title: {title[:70]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: 馃憫岬浲⑨祹岬栶潉熲彜蜔蜑蜔蜑鈨濔焽焽仇潗嬸潗勷潗嗮潗勷潗嶐潗冣梽鈴ね熗炩潃廷鉂� 鈨燄潗戰潗€饾悏嗉洁紟廷 (@JaiHindChatting)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/ytp", "Play"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer

    lel = await message.reply("**馃攧 皮嗓酶茍蓸ss嫂沙蕸...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "TRISHARobot"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
     
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+","https://t.me/joinchat/")
                except:
                    await lel.edit(
                        "<b>馃 皮森蓸蓱s蓸 蓞蕡 馃槣 F嫂嗓s蕡 獗慿蓸 馃構\n馃槝 獗� 蓞沙 馃挒 蓞蓷杀嫂沙 馃尫...</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "**馃拹 蓞ss嫂st蓱nt 馃 N酶蠅 馃尮 痞蓸蓱蓷y 馃懟\n馃槝 片酶 鉁岋笍 皮森蓱y 馃挒 獗媠嫂茍 馃尫...**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>馃挜 蓞ss嫂st蓱nt 馃様 F蓱嫂森蓸蓷 鈿狅笍 片酶 馃摰\n馃ズ J酶嫂沙 鉁岋笍 片搔嫂s 馃挒 茋搔蓱蕡 馃尫..."
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"**馃挜 蓞ss嫂st蓱nt 馃様 茲酶蕡 鈿狅笍 J酶嫂沙蓸蓷 馃摰\n馃ズ 片搔嫂s 馃挒 茋搔蓱蕡 馃尫...**"
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
                f"**馃挜 皮森蓱y 馃攰 獗媠嫂茍 馃捒 L蓸ss 鈿★笍\n馃 片搔蓱沙鈿★笍 {DURATION_LIMIT} 馃挒 獗┥呈嬍埳� ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/0f6f8a8a5ad69fe5ecf3d.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="馃挜 J酶嫂沙 隇樕ど� & S蕥匹匹酶嗓蕡 馃挒",
                            url=f"https://t.me/JaiHindChatting")

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
                            text="馃挜 J酶嫂沙 隇樕ど� & S蕥匹匹酶嗓蕡 馃挒",
                            url=f"https://t.me/JaiHindChatting")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/8fddb775d567de8a63940.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="馃挜 J酶嫂沙 隇樕ど� & S蕥匹匹酶嗓蕡 馃挒",
                            url=f"https://t.me/JaiHindChatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**馃挜 皮森蓱y 馃攰 獗媠嫂茍 馃捒 L蓸ss 鈿★笍\n馃 片搔蓱沙鈿★笍 {DURATION_LIMIT} 馃挒 獗┥呈嬍埳� ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**馃 茡嫂獗鄙� 馃檭 獗媠嫂茍 馃捒 茲蓱杀蓸 馃槏\n馃挒 片酶 馃攰 皮森蓱y 馃尫...**"
            )
        await lel.edit("**馃攷 S蓸蓱嗓茍搔嫂沙蕸 ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**馃攧 皮嗓酶茍蓸ss嫂沙蕸 ...**")
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
            await lel.edit(
                "**馃攰 獗媠嫂茍 馃槙 茲酶蕡 馃摰 F酶蕥沙蓷鉂楋笍\n馃挒 片嗓y 鈾笍 蓞沙酶蕡搔蓸嗓 馃尫...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="馃挜 J酶嫂沙 隇樕ど� & S蕥匹匹酶嗓蕡 馃挒",
                            url=f"https://t.me/JaiHindChatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**馃挜 皮森蓱y 馃攰 獗媠嫂茍 馃捒 L蓸ss 鈿★笍\n馃 片搔蓱沙鈿★笍 {DURATION_LIMIT} 馃挒 獗┥呈嬍埳� ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃 峁€峁翅範岣笁\n蓞蓷蓷蓸蓷 馃捒 S酶沙蕸鉂楋笍\n馃攰 蓞蕡 馃挒 皮酶s嫂蕡嫂酶沙 禄 `{}` 馃尫 ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
                message.chat.id, 
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
            caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃 M蕥s嫂茍  馃挒\n馃幐 N酶蠅 馃攰 皮森蓱y嫂沙蕸 馃槏 脴皮 馃 ...**".format(),
        )

    os.remove("final.png")
    return await lel.delete()
    
    
    
@Client.on_message(commandpro(["/pause", "Pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/8fddb775d567de8a63940.jpg", 
                             caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃 M蕥s嫂茍\n馃挒N酶蠅 馃 鈻讹笍 皮蓱蕥s蓸蓷 馃尫 ...**"
    )


@Client.on_message(commandpro(["/resume", "Resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/8fddb775d567de8a63940.jpg", 
                             caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃 M蕥s嫂茍\nN酶蠅 馃 鈴� 皮森蓱y嫂沙蕸 馃尫 ...**"
    )



@Client.on_message(commandpro(["/skip", "/next", "Skip", "Next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃 峁€峁翅範岣笁 馃挒\n茲酶蕡搔嫂沙蕸 馃攪 馃毇 皮森蓱y嫂沙蕸 馃尫 ...**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
            
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                    InputStream(
                        InputAudioStream(
                            callsmusic.queues.get(chat_id)["file"],
                        ),
                    ),
                )

    await message.reply_photo(
                             photo="https://telegra.ph/file/8fddb775d567de8a63940.jpg", 
                             caption=f'**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃攬 M蕥s嫂茍馃\nN酶蠅 馃 鈴� S茩嫂匹匹蓸蓷 馃尫 ...**'
   ) 


@Client.on_message(commandpro(["/end", "End", "/stop", "Stop"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/8fddb775d567de8a63940.jpg", 
                             caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃攬 M蕥s嫂茍\n馃N酶蠅 馃 鉂� S蕡酶匹匹蓸蓷 馃尫 ...**"
    )


@Client.on_message(commandpro(["reload", "refresh"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_photo(
                              photo="https://telegra.ph/file/8fddb775d567de8a63940.jpg",
                              caption="**馃挜 岣娽笗峁坚腑岣� 馃嚠馃嚦 岣︶竴岣夅覆岣曖箼 馃攬 M蕥s嫂茍馃\nN酶蠅 馃馃敟 痞蓸森酶蓱蓷蓸蓷 馃尫 ...**"
    )