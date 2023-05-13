from aiogram.fsm.state import StatesGroup, State


class Main(StatesGroup):

    main_state = State()
    first_state_download = State()
    second_state_download = State()
    first_state_convert = State()
    second_state_conv = State()
    third_state_conv = State()
    third_state_playlist = State()
    full_video_state = State()
    download_by_link_state = State()
    third_state_link = State()
    forth_state_link = State()
    fifth_state_link = State()
    sixth_state_link = State()
