import imghdr
import logging
import re
import time
import urllib
from datetime import datetime
from io import BytesIO
from typing import Any

import aiofiles
import yt_dlp
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from big_list import options
from conv_func import conv_to, conv_to_pdf
from cut_func import downloader
from db import save_file
from insta_downloader import download_instagram_video
from run import bot
from states import Main
from tiktok_downloader import download_tiktok_video


async def close_menu(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()



"""Choose what action do You want to do"""
async def conv_or_download(**kwargs):
    c_or_d = [
        ("Converter", 'convert'),
        ("Downloader", 'download'),
    ]
    return {
        "c_or_d": c_or_d,
    }

async def w_conv_or_download(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, choice: str):
     dialog_manager.dialog_data.update(
        c_or_d=choice
        )
     if choice == 'download':
         await dialog_manager.switch_to(Main.first_state_download)
     else:
         await dialog_manager.switch_to(Main.first_state_convert)

     print("You choose: ", choice)


"""Chosen action - DOWNLOAD, chose which site from do You want to download"""

async def download(dialog_manager: DialogManager, **kwargs):
    source = [
        ("Youtube", 'youtube'),
        ("Instagram", 'instagram'),
        ("TikTok", 'tiktok'),

    ]
    return {
        "source": source
    }

async def w_download(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, source: str):
    print("You choose: ", source)
    dialog_manager.dialog_data.update(
        source=source
    )
    await dialog_manager.switch_to(Main.second_state_download)


async def download_source(dialog_manager: DialogManager, **kwargs):
    c_or_d = dialog_manager.dialog_data.get('c_or_d')
    source = dialog_manager.dialog_data.get('source')
    action = options[c_or_d][source]
    return {
        "action": action
    }

async def w_download_source(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, action: str):
    print("You choose: ", action)
    dialog_manager.dialog_data.update(
        action=action
    )
    f = {
        'piece': Main.third_state_link,
        'full': Main.full_video_state,       #11111111111111111111111111111111111111111111111111
        'playlist': Main.third_state_playlist,
        'insta_video': Main.download_by_link_state,
        'tiktok_video': Main.download_by_link_state
    }
    await dialog_manager.switch_to(f[action])


async def conv_options_from(**kwargs):
    types_from = [
        (".png", 'png'),
        (".jpeg", 'jpeg'),
        (".pdf", 'pdf'),
        (".docx", 'docx'),
        #(".txt", 'txt'),
        (".pptx", 'pptx'),
    ]
    return {
        "types_from_1": types_from[:3],
        "types_from_2": types_from[3:],
    }

async def w_conv_options_from(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, type_from: str):
    dialog_manager.dialog_data.update(
        type_from=type_from,
    )
    print("You choose: ", type_from)
    await dialog_manager.switch_to(Main.second_state_conv)


async def conv_options_to(dialog_manager: DialogManager, **kwargs):
    show_type_from = dialog_manager.dialog_data.get('type_from', 0)
    c_or_d = dialog_manager.dialog_data.get('c_or_d')
    types_to = options[c_or_d][show_type_from]
    return {
        "show_type_from": show_type_from,
        "types_to": types_to,
    }

async def w_conv_options_to(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, types_to: str):
    type_from = dialog_manager.dialog_data.get('type_from')
    type_to = dialog_manager.dialog_data.update(
        types_to=types_to
    )

    await dialog_manager.switch_to(Main.third_state_conv)

    print("You choose: ", types_to)



async def upload_file(dialog_manager: DialogManager, **kwargs):
    show_type_from = dialog_manager.dialog_data.get('type_from', 0)
    show_type_to = dialog_manager.dialog_data.get('types_to', 0)
    file = [("Please upload Your file and press", "upload")]
    # filename = [(f"Download: {dialog_manager.dialog_data.get('filename')}", 'filename')]

    return {
        "show_type_from": show_type_from,
        "show_type_to": show_type_to,
        "file": file

    }


async def w_upload_file(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, confirm: str):
    print("You choose: ", confirm)



async def handle_download_by_link(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)

    return {
        "source": source,
    }


async def w_download_by_link(message: Message, input: MessageInput, dialog_manager: DialogManager):
    print("You get to w_download_by_link")
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    now = datetime.now()
    g = {
        'instagram': [['www.instagram.com/p', 'www.instagram.com/reel'], download_instagram_video(message.text)],
        'tiktok': [['tiktok.com/@', 'vm.tiktok.com/'], download_tiktok_video(message.text)]
    }
    if any([True if i in message.text else False for i in g[source][0]]):
        try:
            save_file(message.message_id, source, action, message.from_user.id,
                      message.from_user.username)
            start = time.time()
            r = await g[source][1]
            if type(r[0]) == tuple:
                for i in r:
                    input_file_d = BufferedInputFile(i[0].getvalue(),
                                                     filename=f'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\{i[1]}')
                    end = time.time()
                    await message.answer_video(input_file_d,
                                               caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
            else:
                input_file_d = BufferedInputFile(r[0], filename=r[1])
                end = time.time()
                await message.answer_video(input_file_d,
                                               caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
        except (yt_dlp.utils.DownloadError, urllib.error.HTTPError) as e:
            print(f"Video is unavailable on server.")
            await bot.send_message(chat_id=message.chat.id, text=f"Sorry:(\nVideo is unavailable on server.")
    else:
        await bot.send_message(chat_id=message.chat.id, text=f"Wrong link! Please send correct link.")




async def handle_playlist(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    return {
        "source": source,
        "action": action,
    }


async def w_handle_playlist(message: Message, input: MessageInput, dialog_manager: DialogManager):
    print("You get to w_handle_playlist")
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    now = datetime.now()
    if 'youtube.com/playlist' in message.text or '&list' in message.text:
        save_file(message.message_id, source, action, message.from_user.id,
                  message.from_user.username)
        start = time.time()
        link = message.text
        source = dialog_manager.dialog_data.get('source', 0)
        r = await downloader(message.from_user.id, link, source, action)
        for i in r:
            input_file_d = BufferedInputFile(i[0].getvalue(), filename=f'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\{i[1]}')
            end = time.time()
            await message.answer_video(input_file_d,
                                       caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")

    else:
        await bot.send_message(chat_id=message.chat.id, text=f"Wrong link! Please send correct link.")


async def full_video_downloader(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    return {
        "source": source,
        "action": action,
    }


async def w_full_video_downloader(message: Message, input: MessageInput, dialog_manager: DialogManager):
    print("You get to w_full_video_downloader")
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    g = [
        'youtube.com/watch?', 'm.youtube.com/watch?', 'youtu.be/',
        'm.youtube.com/v', 'www.youtube.com/v']
    if any([True if i in message.text else False for i in g]):
        save_file(message.message_id, source, action, message.from_user.id,
                  message.from_user.username)
        start = time.time()
        link = message.text
        cut_start = dialog_manager.dialog_data.get('start', 0)
        cut_end = dialog_manager.dialog_data.get('end', 0)
        r = await downloader(message.from_user.id, link, source, action, cut_start, cut_end)

        input_file_d = BufferedInputFile(r[0], filename=f'{r[1]}')
        end = time.time()
        await message.answer_document(input_file_d,
                                   caption=f"File downloaded successfully!\nTime: {round(end - start, 3)} seconds")






async def handle_links_1(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    return {
        "show_type_from": source,
        "show_type_to": action,
    }



async def w_handle_links_1(message: Message, input: MessageInput, dialog_manager: DialogManager):
    symbol = set(re.sub(r'\d+', '', message.text))
    if len(symbol) == 1:
        dt_start = datetime.strptime(message.text, "%H:%M:%S")
        start = dt_start.second + dt_start.minute * 60 + dt_start.hour * 3600
        dialog_manager.dialog_data.update(
            start=start,
        )
        await dialog_manager.switch_to(Main.forth_state_link)
        print(f"{message.from_user.username} choose: ", message.text)
    else:
        print('Wrong time format!')



async def handle_links_2(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    show_start = dialog_manager.dialog_data.get('start')
    return {
        "show_type_from": source,
        "show_type_to": action,
        "show_start": show_start,
    }




async def w_handle_links_2(message: Message, input: MessageInput, dialog_manager: DialogManager):
    symbol = set(re.sub(r'\d+', '', message.text))
    if len(symbol) == 1:
        dt_end = datetime.strptime(message.text, "%H:%M:%S")
        end = dt_end.second + dt_end.minute * 60 + dt_end.hour * 3600
        dialog_manager.dialog_data.update(
            end=end,
        )
        await dialog_manager.switch_to(Main.fifth_state_link)
        print(f"{message.from_user.username} choose: ", message.text)
    else:
        print('Wrong time format!')

async def handle_links_3(dialog_manager: DialogManager, **kwargs):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    show_start = dialog_manager.dialog_data.get('start')
    show_end = dialog_manager.dialog_data.get('end')
    return {
        "show_type_from": source,
        "show_type_to": action,
        "show_start": show_start,
        "show_end": show_end,
    }



async def handle_links_4(message: Message, input: MessageInput, dialog_manager: DialogManager):
    source = dialog_manager.dialog_data.get('source', 0)
    action = dialog_manager.dialog_data.get('action', 0)
    g = [
        'youtube.com/watch?', 'm.youtube.com/watch?', 'youtu.be/',
         'm.youtube.com/v', 'www.youtube.com/v']
    if any([True if i in message.text else False for i in g]):
        save_file(message.message_id, source, action, message.from_user.id,
                  message.from_user.username)
        start = time.time()
        link = message.text
        cut_start = dialog_manager.dialog_data.get('start', 0)
        cut_end = dialog_manager.dialog_data.get('end', 0)
        r = await downloader(message.from_user.id, link, source, action, cut_start, cut_end)
        end = time.time()
        input_file_d = BufferedInputFile(r, filename="cut_video.mp4")
        await message.answer_video(input_file_d,
                                      caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")




async def handle_docs(message: Message, input: MessageInput, dialog_manager: DialogManager):
    if message.document:
        start = time.time()
        file_type = message.document.file_name.split('.')[-1]
        show_type_from = dialog_manager.dialog_data.get('type_from', 0)
        show_type_to = dialog_manager.dialog_data.get('types_to', 0)

        if file_type == show_type_from or file_type == 'jpg' and show_type_from == 'jpeg':
            logging.info('You`re in handle_docs')
            save_file(message.document.file_id, show_type_from, show_type_to, message.from_user.id, message.from_user.username)

            #doc_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\tgbot_template_v3\save_dir\temp." + file_type
            save_to_io = BytesIO()
            file_id = message.document.file_id
            #logging.info(file_id)
            file = await bot.get_file(file_id=file_id)
            # logging.info(file)
            # async with aiofiles.open(file.file_path, "rb") as f:
            #     video_bytes = await f.read()
            # save_to_io.write(video_bytes)
            # save_to_io.seek(0)

            #input_file_d = BufferedInputFile(save_to_io.getvalue(), message.document.file_name)       #THIS IS WORKING!!!!!!!!!!!!!!!!!!!!!!!!!
            #await message.answer_document(input_file_d, caption='File returned!')                     #THIS IS WORKING!!!!!!!!!!!!!!!!!!!!!!!!!


            r = await conv_to(file.file_path, file_id, show_type_from, show_type_to, message.from_user.id)
            end = time.time()
            input_file_d = BufferedInputFile(r, filename=f"{message.document.file_name.split('.')[0]}.{show_type_to}")
            await message.answer_document(input_file_d, caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
        else:
            await bot.send_message(chat_id=message.chat.id, text=f"Wrong file type! Please upload correct file.")

    elif message.photo:
        #await bot.send_message(chat_id=message.chat.id, text=f"Wrong file type! Please upload photo as file.")
        start = time.time()
        show_type_from = dialog_manager.dialog_data.get('type_from', 0)
        show_type_to = dialog_manager.dialog_data.get('types_to', 0)
        save_to_io = BytesIO()
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        #logging.info(message.photo)
        file_type = file.file_path.rsplit('.')[-1]
        logging.info(file_type)
        #end = time.time()
        #input_file_d = BufferedInputFile(file.file_path, filename=f"new_file.{show_type_to}")

        #await message.answer_document(document=file.file_path, caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")     #THIS CODE WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if file_type == show_type_from or file_type == 'jpg' and show_type_from == 'jpeg' or show_type_from == 'png' and file_type in ['jpg', 'jpeg']:
            save_file(file_id, show_type_from, show_type_to, message.from_user.id, message.from_user.username)
            # photo_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\tgbot_template_v3\save_dir\temp." + image_type
            # async with aiofiles.open(photo_path, "wb") as file:
            #     await file.write(save_to_io.getbuffer())
            r = await conv_to(file.file_path, file_id, show_type_from, show_type_to, message.from_user.id)
            end = time.time()
            input_file_p = BufferedInputFile(r, filename=f"{message.photo[0].file_id.split('.')[0]}.{show_type_to}")
            await message.answer_document(input_file_p, caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")

        else:
            await bot.send_message(chat_id=message.chat.id, text=f"Wrong file type! Please upload correct file.")


    # elif message.video:
    #     start = time.time()
    #     show_type_from = dialog_manager.dialog_data.get('type_from', 0)
    #     show_type_to = dialog_manager.dialog_data.get('types_to', 0)
    #     save_to_io = BytesIO()
    #     photo = message.photo[-1]
    #     await bot.download(photo, destination=save_to_io)
    #     image_type = imghdr.what(save_to_io)
    #
    #     if image_type == show_type_from or image_type == 'jpg' and show_type_from == 'jpeg':
    #         photo_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\temp." + image_type
    #         async with aiofiles.open(photo_path, "wb") as file:
    #             await file.write(save_to_io.getbuffer())
    #         r = await conv_to(photo_path, show_type_from, show_type_to)
    #         end = time.time()
    #         input_file_p = BufferedInputFile(r, filename=f"{message.photo[0].file_id.split('.')[0]}.{show_type_to}")
    #         await message.answer_document(input_file_p,
    #                                       caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
    #
    #     else:
    #         await bot.send_message(chat_id=message.chat.id, text=f"Wrong file type! Please upload correct file.")
    #
    #         #r = await conv_to_pdf(message.document.file_name, input_file_d.data, message.from_user.id)
    #
    #         await bot.send_message(chat_id=message.chat.id, text=f"File was uploaded")
    #
    # elif message.photo:
    #     save_to_io = BytesIO()
    #     photo = message.photo[-1]
    #     await bot.download(photo, destination=save_to_io)
    #     #save_file(message.photo[0].file_id, file_p.getvalue(), message.from_user.id, time_now)
    #     input_file_p = BufferedInputFile(save_to_io.getvalue(), filename=photo.file_id)
    #     await message.answer_document(input_file_p, caption="Photo converted successfully!")
    #     await bot.send_message(chat_id=message.chat.id, text=f"{input_file_p.filename} was uploaded")









# async def ships(dialog_manager: DialogManager, **kwargs):
#     info = dialog_manager.dialog_data.get('planet', 0)
#     comp_info = dialog_manager.dialog_data.get('comp_info', 0)
#     ships_info = items('ships')
#     return {
#         "planet_info": info,
#         "comp_info": comp_info,
#         "ships_info": ships_info,
#
#     }
#
#
#
# async def wships(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, ship: str):
#     print("You choose: ", ship)
#     dialog_manager.dialog_data.update(
#         ship=table_info('ships', ship)
#     )
#     await dialog_manager.switch_to(Main.fifth_state)
#
#
# async def ready(dialog_manager: DialogManager, **kwargs):
#     info = dialog_manager.dialog_data.get('planet', 0)
#     comp_info = dialog_manager.dialog_data.get('comp_info', 0)
#     ship = dialog_manager.dialog_data.get('ship', 0)
#     confirm_button = [("Confirm", "confirm")]
#     return {
#         "planet_info": info,
#         "comp_info": comp_info,
#         "ship": ship,
#         "confirm_button": confirm_button,
#     }
#
# async def wready(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, confirm: str):
#     print("You choose: ", confirm)





