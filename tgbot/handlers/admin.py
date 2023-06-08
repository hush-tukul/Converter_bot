from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from windows import Main
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(m: Message, dialog_manager: DialogManager):
    await m.reply("Вітаю, адміне!")
    await m.answer_photo(
        photo='AgACAgQAAxkBAAIKdWRguSvRJu0RcWdgo455KA1FJTecAAKrvDEbMI8JU2popPRpkpu_AQADAgADeQADLwQ', chat=683497406)
    await m.answer(
        f"<b>Hi, I`m a Celestial!\nIf You want to see all my functions, please press command '/info'.</b>",
        parse_mode='HTML')
    await dialog_manager.start(Main.main_state, mode=StartMode.RESET_STACK)

#
