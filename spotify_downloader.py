import yt_dlp
import logging

from savify import Savify
from savify.types import Type, Format, Quality
from savify.utils import PathHolder




from savify import Savify
from savify.types import Type, Format, Quality

s = Savify()
Savify(api_credentials=None, quality=Quality.BEST, download_format=Format.MP3,
       path_holder=PathHolder(downloads_path='C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory'))
# Spotify URL
s.download("https://open.spotify.com/episode/43D9PMFx0j9BdbpcS9meBY?si=26b989d4c4144cbe")



#
# def spotify_loader(video_url: str) -> None:
#     ydl_opts = {
#         'outtmpl': 'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s.%(ext)s',
#         'format': 'bestvideo+bestaudio/best',
#         'merge_output_format': 'mp4'
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#
#
# url = "https://open.spotify.com/episode/43D9PMFx0j9BdbpcS9meBY?si=26b989d4c4144cbe"
# spotify_loader(url)



