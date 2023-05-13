import io
import os

import aiofiles
import yt_dlp


async def download_tiktok_video(video_link):
    save_to_io = io.BytesIO()
    output_file_path = fr"C:\PY\Python_learn\Minions_Bots\Converter_bot\tgbot_template_v3\save_dir\3%(title)s.%(ext)s"
    ydl = yt_dlp.YoutubeDL({'outtmpl': output_file_path})
    info = ydl.extract_info(video_link, download=False)
    file_path = ydl.prepare_filename(info)
    file_path = os.path.abspath(file_path)
    ydl.download([video_link])
    async with aiofiles.open(file_path, 'rb') as f:
        video_bytes = await f.read()

    save_to_io.write(video_bytes)
    save_to_io.seek(0)
    os.remove(file_path)
    return [save_to_io.getvalue(), file_path.split('/')[-1]]

