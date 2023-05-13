import io
import os

import aiofiles
import aiohttp
import yt_dlp


async def download_instagram_video(video_link):
    save_to_io = io.BytesIO()
    output_file_path = fr"C:\PY\Python_learn\Minions_Bots\Converter_bot\tgbot_template_v3\save_dir\%(title)s.%(ext)s"
    ydl_opts = {
        'outtmpl': output_file_path,
        'nooverwrites': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_link, download=False)
        if 'entries' in info:
            video_bytes_list = []
            paths_list = []
            info = ydl.extract_info(video_link, download=False)
            for entry in info['entries']:
                file_path = ydl.prepare_filename(entry)
                file_path = os.path.abspath(file_path)
                paths_list.append(file_path)
                try:
                    ydl.download(entry['webpage_url'])
                    async with aiofiles.open(file_path, 'rb') as f:
                        video_bytes = await f.read()
                    save_to_io = io.BytesIO(video_bytes)
                    video_bytes_list.append((save_to_io, file_path.split('/')[-1]))



                except yt_dlp.utils.DownloadError:
                    print(f"Skipping {entry['title']}.")
                    continue

            for i in paths_list:
                os.remove(i)

            return video_bytes_list
        else:
            file_path = ydl.prepare_filename(info)
            file_path = os.path.abspath(file_path)
            ydl.download([video_link])
            async with aiofiles.open(file_path, 'rb') as f:
                video_bytes = await f.read()

            save_to_io.write(video_bytes)
            save_to_io.seek(0)
            os.remove(file_path)
            return [save_to_io.getvalue(), file_path.split('/')[-1]]

"""-------------------------WORKED FUNC---------------------------------------"""
# async def download_instagram_video(video_link):
#     save_to_io = io.BytesIO()
#     output_file_path = f"C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s.%(ext)s"
#     ydl = yt_dlp.YoutubeDL({'outtmpl': output_file_path})
#     info = ydl.extract_info(video_link, download=False)
#     if 'entries' in info:
#         video_bytes_list = []
#         paths_list = []
#         with ydl:
#             info = ydl.extract_info(video_link, download=False)
#             for entry in info['entries']:
#                 file_path = ydl.prepare_filename(entry)
#                 file_path = os.path.abspath(file_path)
#                 paths_list.append(file_path)
#                 try:
#                     ydl.download(entry['webpage_url'])
#                     async with aiofiles.open(file_path, 'rb') as f:
#                         video_bytes = await f.read()
#                     save_to_io = io.BytesIO(video_bytes)
#                     video_bytes_list.append((save_to_io, file_path.split('/')[-1]))
#
#
#
#                 except yt_dlp.utils.DownloadError:
#                     print(f"Skipping {entry['title']}.")
#                     continue
#
#         for i in paths_list:
#             os.remove(i)
#
#         return video_bytes_list
#     else:
#         file_path = ydl.prepare_filename(info)
#         file_path = os.path.abspath(file_path)
#         ydl.download([video_link])
#         async with aiofiles.open(file_path, 'rb') as f:
#             video_bytes = await f.read()
#
#         save_to_io.write(video_bytes)
#         save_to_io.seek(0)
#         os.remove(file_path)
#         return [save_to_io.getvalue(), file_path.split('/')[-1]]




# async def download_instagram_video(video_link):
#     save_to_io = io.BytesIO()
#     output_file_path = "C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s.%(ext)s"
#     ydl = yt_dlp.YoutubeDL({'outtmpl': output_file_path})
#     info = ydl.extract_info(video_link, download=False)
#     if 'entries' in info:
#         video_bytes_list = []
#         paths_list = []
#         with ydl:
#             info = ydl.extract_info(video_link, download=False)
#             for entry in info['entries']:
#                 file_path = ydl.prepare_filename(entry)
#                 file_path = os.path.abspath(file_path)
#                 paths_list.append(file_path)
#                 try:
#                     async with aiohttp.ClientSession() as session:
#                         async with session.get(entry['webpage_url']) as resp:
#                             if resp.status == 200:
#                                 video_bytes = await resp.read()
#                                 save_to_io = io.BytesIO(video_bytes)
#                                 video_bytes_list.append((save_to_io, file_path.split('/')[-1]))
#                             else:
#                                 raise Exception(f"Failed to download {entry['title']}.")
#                 except Exception as e:
#                     print(f"Skipping {entry['title']}: {e}")
#                     continue
#
#         for i in paths_list:
#             os.remove(i)
#
#         return video_bytes_list
#     else:
#         file_path = ydl.prepare_filename(info)
#         file_path = os.path.abspath(file_path)
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(video_link) as resp:
#                     if resp.status == 200:
#                         video_bytes = await resp.read()
#                         save_to_io.write(video_bytes)
#                         save_to_io.seek(0)
#                         os.remove(file_path)
#                         return [save_to_io.getvalue(), file_path.split('/')[-1]]
#                     else:
#                         raise Exception(f"Failed to download {info['title']}.")
#         except Exception as e:
#             print(f"Skipping {info['title']}: {e}")
#             return None




#download_instagram_video('https://www.instagram.com/p/CraLdvLoCrX/')

# async def save_playlist(playlist_url, user_id):
#     save_to_io = io.BytesIO()
#     now = datetime.now()
#     options = {
#         'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#         'outtmpl': f'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s_{user_id}.mp4',
#         'ignoreerrors': True,
#         'playliststart': 1,
#         'playlistend': None  # Download whole playlist
#     }
#
#     video_bytes_list = []
#     with yt_dlp.YoutubeDL(options) as ydl:
#         info = ydl.extract_info(playlist_url, download=False)
#         for entry in info['entries']:
#             file_path = ydl.prepare_filename(entry)
#             print(file_path)
#             file_path = os.path.abspath(file_path)
#             try:
#                 ydl.download(entry['webpage_url'])
#                 async with aiofiles.open(file_path, 'rb') as f:
#                     video_bytes = await f.read()
#                 save_to_io = io.BytesIO(video_bytes)
#                 video_bytes_list.append((save_to_io, file_path.split('/')[-1]))
#                 os.remove(file_path)
#
#
#             except yt_dlp.utils.DownloadError:
#                 print(f"Skipping {entry['title']}.")
#                 continue
#
#     return video_bytes_list