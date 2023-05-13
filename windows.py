import operator


from aiogram.enums import ParseMode, ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, MessageHandlerFunc
from aiogram_dialog.widgets.kbd import Select, SwitchTo, Column, Button, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format, Text

from windows_func import w_conv_options_from, conv_options_from, conv_options_to, w_conv_options_to, \
    upload_file, handle_docs, close_menu, w_handle_links_1, w_handle_links_2, \
    handle_links_2, handle_links_1, handle_links_3, handle_links_4, handle_playlist, w_handle_playlist, \
    conv_or_download, w_conv_or_download, download, w_download, handle_download_by_link, w_download_by_link, \
    download_source, w_download_source, full_video_downloader, w_full_video_downloader
from windows_func import Main





main_window = Window(
    Const('Converter and Downloader'),
    Const('Please choose an option: '),
    Row(
        Select(
            Format("{item[0]}"),
            id="main_window",
            item_id_getter=operator.itemgetter(1),
            items="c_or_d",
            on_click=w_conv_or_download,

        ),
    ),
    parse_mode=ParseMode.HTML,
    state=Main.main_state,
    getter=conv_or_download

    )




first_window_convert = Window(
    Const('Converter'),
    Const(f"<b>FROM: </b>"),
    Row(
        Select(
            Format("{item[0]}"),
            id="conv_list_1",
            item_id_getter=operator.itemgetter(1),
            items="types_from_1",
            on_click=w_conv_options_from,

        ),
    ),
    Row(
        Select(
            Format("{item[0]}"),
            id="conv_list_2",
            item_id_getter=operator.itemgetter(1),
            items="types_from_2",
            on_click=w_conv_options_from,

        ),
    ),
    SwitchTo(Const("Back"), id="Back", state=Main.main_state),
    parse_mode=ParseMode.HTML,
    state=Main.first_state_convert,
    getter=conv_options_from
)


first_window_download = Window(
    Const('Downloader'),
    Row(
        Select(
            Format("{item[0]}"),
            id="download_list",
            item_id_getter=operator.itemgetter(1),
            items='source',
            on_click=w_download
        ),
    ),
    SwitchTo(Const("Back"), id="Back", state=Main.main_state),
    parse_mode=ParseMode.HTML,
    state=Main.first_state_download,
    getter=download
)


second_window_download = Window(
    Const('Downloader'),
    Const('Please choose an action: '),
    Row(
        Select(
            Format("{item[0]}"),
            id="second_window_c",
            item_id_getter=operator.itemgetter(1),
            items='action',
            on_click=w_download_source
        ),
    ),
    SwitchTo(Const("Back"), id="Back", state=Main.first_state_download),
    parse_mode=ParseMode.HTML,
    state=Main.second_state_download,
    getter=download_source
)

second_window_conv = Window(
    Const('Converter And Cutter'),
    Format("FROM: {show_type_from}"),
    Const(f"<b>TO: </b>"),
    Row(
        Select(
            Format("{item[0]}"),
            id="second_window_c",
            item_id_getter=operator.itemgetter(1),
            items='types_to',
            on_click=w_conv_options_to
        ),
    ),
    SwitchTo(Const("Back"), id="Back", state=Main.first_state_convert),
    parse_mode=ParseMode.HTML,
    state=Main.second_state_conv,
    getter=conv_options_to
)

third_window_conv = Window(
    Const('Converter'),
    Format("FROM: {show_type_from}"),
    Format("TO: {show_type_to}"),
    Const('Please upload Your file..'),
    MessageInput(handle_docs, ContentType.ANY),

    SwitchTo(Const("Back"), id="Back", state=Main.second_state_conv),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.third_state_conv,
    getter=upload_file
)

download_by_link_window = Window(
    Const('Downloader'),
    Format("Please write {source}-video link to download: "),
    Const('(ATTENTION - The longer the video, the longer it will be downloaded)'),
    MessageInput(w_download_by_link, ContentType.TEXT),
    SwitchTo(Const("Back"), id="Back", state=Main.first_state_download),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.download_by_link_state,
    getter=handle_download_by_link
)




playlist_window = Window(
    Const('Downloader'),
    Format("OPTION: {source}"),
    Format("ACTION: {action}"),
    Const('Please write Youtube video link for a playlist: '),
    Const('(ATTENTION - The longer the video, the longer the segment will be processed)'),
    MessageInput(w_handle_playlist, ContentType.TEXT),

    SwitchTo(Const("Back"), id="Back", state=Main.first_state_download),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.third_state_playlist,
    getter=handle_playlist
)

full_video_window = Window(
    Const('Downloader'),
    Format("OPTION: {source}"),
    Format("ACTION: {action}"),
    Const('Please write Youtube video link: '),
    Const('(ATTENTION - The longer the video, the longer the segment will be processed)'),
    MessageInput(w_full_video_downloader, ContentType.TEXT),
    SwitchTo(Const("Back"), id="Back", state=Main.first_state_download),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.full_video_state,
    getter=full_video_downloader
)



third_window_link = Window(
    Const('Cutter'),
    Format("FROM: {show_type_from}"),
    Format("TO: {show_type_to}"),
    Const('Please write timecode start in format - 00:00:00'),
    Const('Please upload file\n(ATTENTION - The longer the video, the longer the segment will be processed)'),
    MessageInput(w_handle_links_1, ContentType.TEXT),

    SwitchTo(Const("Back"), id="Back", state=Main.first_state_download),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.third_state_link,
    getter=handle_links_1
)

forth_window_link = Window(
    Const('Cutter'),
    Format("FROM: {show_type_from}"),
    Format("TO: {show_type_to}"),
    Format("TIMECODE START: {show_start}"),
    Const('Please write timecode end in format - 00:00:00'),
    MessageInput(w_handle_links_2, ContentType.TEXT),

    SwitchTo(Const("Back"), id="Back", state=Main.third_state_link),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.forth_state_link,
    getter=handle_links_2
)
fifth_window_link = Window(
    Const('Cutter'),
    Format("FROM: {show_type_from}"),
    Format("TO: {show_type_to}"),
    Format("TIMECODE START: {show_start}"),
    Format("TIMECODE END: {show_end}"),
    Const('Please write Youtube video link: '),
    MessageInput(handle_links_4, ContentType.TEXT),

    SwitchTo(Const("Back"), id="Back", state=Main.forth_state_link),
    Button(Const("Close menu"), id="close_menu", on_click=close_menu),
    parse_mode=ParseMode.HTML,
    state=Main.fifth_state_link,
    getter=handle_links_3
)


#
#
# forth_window = Window(
#     Const(f"<b>Choose Your ship, Traveller.</b>"),
#     Format("{planet_info}"),
#     Format("{comp_info}"),
#     Button(
#         Const('Choose your ship: '),
#         id="ship_title",
#     ),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="choosed_ship",
#             item_id_getter=operator.itemgetter(1),
#             items="ships_info",
#             on_click=wships,
#         ),
#     ),
#     SwitchTo(Const("Back"), id="Back", state=Main.third_state),
#     parse_mode=ParseMode.HTML,
#     state=Main.forth_state,
#     getter=ships
# )
#
#
# fifth_window = Window(
#     Const(f"<b>Now, You are ready!</b>"),
#     Format("{planet_info}"),
#     Format("{comp_info}"),
#     Format("{ship}"),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="ready_window",
#             item_id_getter=operator.itemgetter(1),
#             items="confirm_button",
#             on_click=wready,
#         ),
#     ),
#     SwitchTo(Const("Back"), id="Back", state=Main.forth_state),
#     parse_mode=ParseMode.HTML,
#     state=Main.fifth_state,
#     getter=ready
# )


# StaticMedia(
#             path=os.path.join(src_dir, "python_logo.png"),
#             type=ContentType.PHOTO,
#         ),