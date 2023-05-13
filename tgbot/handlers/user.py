from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from windows import Main # MAYBE A PROBLEMATIC PLACE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
user_router = Router()


@user_router.message(CommandStart())
async def start(m: Message, dialog_manager: DialogManager):
    # await m.answer_photo(photo='AgACAgQAAxkBAAIN42RREcHUcmeHtWhxf4CttRmQ8MDcAAIVuTEb8raJUrb-roV7mMTJAQADAgADeQADLwQ', chat=683497406)
    await m.answer(
        f"<b>Hi, I`m a Celestial!\nIf You want to see all my functions, please press command '/info'.</b>",
        parse_mode='HTML')
    await dialog_manager.start(Main.main_state, mode=StartMode.RESET_STACK)


@user_router.message(Command('info'))
async def info(m: Message, dialog_manager: DialogManager):
    await m.answer(
        f"<b>Hi, I`m a Celestial!\nBelow You can find all my functions for today. Enjoy my service and be carefull with Your wishes."
        f"\n---------------------------------------FUNCTIONS---------------------------------------"
        f"\n"
        f"\nCONVERTING: "
        f"\n  -docx:"
        f"\n      -to pdf;"
        f"\n      -to txt;"
        f"\n  -pdf:"
        f"\n      -to docx;"
        f"\n  -jpeg or png:"
        f"\n      -to txt;"
        f"\n  -pptx (PowerPoint doc):"
        f"\n      -to txt;"
        f"\n"
        f"\nDOWNLOADING: "
        f"\n  -Youtube:"
        f"\n      -slice from YT-video;"
        f"\n      -whole YT-playlist;"
        f"\n  -Instagram:"
        f"\n      -insta-video;"
        f"\n  -TikTok:"
        f"\n      -tt-video;</b>",

        parse_mode='HTML')
