from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, BufferedInputFile, InputFile
from aiogram_dialog import DialogManager, StartMode



echo_router = Router()


# @echo_router.message(F.text, StateFilter(None))
# async def bot_echo(message: types.Message):
#     text = [
#         "Ехо без стану.",
#         "Повідомлення:",
#         message.text
#     ]
#
#     await message.answer('\n'.join(text))
#
#
# @echo_router.message(F.text)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state_name = await state.get_state()
#     text = [
#         f'Ехо у стані {hcode(state_name)}',
#         'Зміст повідомлення:',
#         hcode(message.text)
#     ]
#     await message.answer('\n'.join(text))

# @echo_router.message(Command('start'))
# async def start(m: Message, dialog_manager: DialogManager):
#     await m.answer_photo(photo='AgACAgQAAxkBAAIN42RREcHUcmeHtWhxf4CttRmQ8MDcAAIVuTEb8raJUrb-roV7mMTJAQADAgADeQADLwQ', chat=683497406)
#     await m.answer(
#         f"<b>Hi, I`m a Celestial!\nIf You want to see all my functions, please press command '/info'.</b>",
#         parse_mode='HTML')
#     await dialog_manager.start(Main.main_state, mode=StartMode.RESET_STACK)


