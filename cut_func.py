
import io

import os
from datetime import datetime

import aiofiles
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip











# >>>>>>>>>>>>>>>>WORKING CODE WITH DOWNLOADING>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
async def save_playlist(playlist_url, user_id):
    save_to_io = io.BytesIO()
    now = datetime.now()
    options = {
        'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': fr'C:\PY\Python_learn\Minions_Bots\Converter_bot\tgbot_template_v3\save_dir\%(title)s_{user_id}.mp4',
        'ignoreerrors': True,
        'playliststart': 1,
        'playlistend': None  # Download whole playlist
    }

    video_bytes_list = []
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        for entry in info['entries']:
            file_path = ydl.prepare_filename(entry)
            print(file_path)
            file_path = os.path.abspath(file_path)
            try:
                ydl.download(entry['webpage_url'])
                async with aiofiles.open(file_path, 'rb') as f:
                    video_bytes = await f.read()
                save_to_io = io.BytesIO(video_bytes)
                video_bytes_list.append((save_to_io, file_path.split('/')[-1]))
                os.remove(file_path)


            except yt_dlp.utils.DownloadError:
                print(f"Skipping {entry['title']}.")
                continue

    return video_bytes_list


# >>>>>>>>>>>>>>>>MULTIPROCESSING VERSION OF FUNC CODE WITH DOWNLOADING>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# async def process_video(entry, ydl):
#     file_path = ydl.prepare_filename(entry)
#     file_path = os.path.abspath(file_path)
#     try:
#         ydl.download(entry['webpage_url'])
#         with open(file_path, 'rb') as f:
#             video_bytes = f.read()
#         return (io.BytesIO(video_bytes), file_path.split('/')[-1])
#     except yt_dlp.utils.DownloadError:
#         print(f"Skipping {entry['title']}.")
#         return None
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
#     video_bytes_list = []
#     with yt_dlp.YoutubeDL(options) as ydl:
#         info = ydl.extract_info(playlist_url, download=False)
#         tasks = []
#         for entry in info['entries']:
#             tasks.append(asyncio.create_task(process_video(entry, ydl)))
#
#         for task in tasks:
#             result = await task
#             if result:
#                 video_bytes_list.append(result)
#
#     return video_bytes_list

async def save_full_video(video_url):
    print("Func save_video_piece started")
    save_to_io = io.BytesIO()
    output_file_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\save_dir\video_cut.mp4"

    # Create a YoutubeDL object
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info = ydl.extract_info(video_url, download=False)
    temp = ydl.prepare_filename(info)
    temp = os.path.abspath(temp)
    ydl.download([video_url])
    async with aiofiles.open(temp, 'rb') as f:
        video_bytes = await f.read()

    save_to_io.write(video_bytes)
    save_to_io.seek(0)

    print(f'Successfully saved video piece to {output_file_path} and deleted temporary file')
    os.remove(temp)
    return [save_to_io.getvalue(), temp]







# >>>>>>>>>>>>>>>>WORKING CODE WITH DOWNLOADING>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


async def save_video_piece(video_url, start_time, end_time):
    print("Func save_video_piece started")
    save_to_io = io.BytesIO()
    output_file_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\video_cut.mp4"

    # Create a YoutubeDL object
    ydl_opts = {
        'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s.%(ext)s',
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Download the video info
    info = ydl.extract_info(video_url, download=False)
    # duration = info.get('duration', 0)
    # stream_url = info['formats'][0]['url']

    # Download the video to a temporary file
    temp = ydl.prepare_filename(info)
    ydl.download([video_url])

    # Create a VideoFileClip object from the temporary file
    video = VideoFileClip(temp)

    # Cut the video and write it to the output file
    cut_video = video.subclip(start_time, end_time)
    cut_video.write_videofile(output_file_path, codec="libx264")

    # Read the output file as bytes asynchronously using aiofiles
    async with aiofiles.open(output_file_path, 'rb') as f:
        video_bytes = await f.read()

    # Write the bytes to the BytesIO object
    save_to_io.write(video_bytes)
    save_to_io.seek(0)

    print(f'Successfully saved video piece to {output_file_path} and deleted temporary file')

    # Close the VideoFileClip object to release resources
    video.close()

    # Remove the output file from the computer
    os.remove(temp)
    os.remove(output_file_path)
    return save_to_io.getvalue()






async def downloader(user_id, video_url, video_type, video_option, start_time=None, end_time=None):
    choose = {
            'youtube':
                {
                    'full': save_full_video(video_url),
                    'piece': save_video_piece(video_url, start_time, end_time),
                    'playlist': save_playlist(video_url, user_id),
                    # 'audio': lambda: conv_to_txt(file_path)
                }
            }
    return await choose[video_type][video_option]

# async def save_video_piece(video_url, start_time, end_time):
#     print("Func save_video_piece started")
#     save_to_io = io.BytesIO()
#     output_file_path = r"C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\video_cut.mp4"
#
#     # Create a YoutubeDL object
#     ydl_opts = {
#         'format': 'mp4',
#         'outtmpl': 'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\%(title)s.%(ext)s',
#     }
#     ydl = youtube_dl.YoutubeDL(ydl_opts)
#
#     # Download the video info
#     info = ydl.extract_info(video_url, download=False)
#     stream_url = info['url']
#
#     # Download the video to a temporary file
#     temp = ydl.prepare_filename(info)
#     ydl.extract_info(video_url, download=True)
#
#     # Create a VideoFileClip object from the temporary file
#     video = VideoFileClip(temp)
#
#     # Cut the video and write it to the output file
#     cut_video = video.subclip(start_time, end_time)
#     cut_video.write_videofile(output_file_path, codec="libx264")
#
#     # Read the output file as bytes asynchronously using aiofiles
#     async with aiofiles.open(output_file_path, 'rb') as f:
#         video_bytes = await f.read()
#
#     # Write the bytes to the BytesIO object
#     save_to_io.write(video_bytes)
#     save_to_io.seek(0)
#
#     print(f'Successfully saved video piece to {output_file_path} and deleted temporary file')
#
#     # Close the VideoFileClip object to release resources
#     video.close()
#
#     # Remove the output file from the computer
#     os.remove(output_file_path)
#
#     return save_to_io.getvalue()
#await f.close()
    # os.remove(f'C:\PY\Python_learn\Minions_Bots\Converter_bot\convert_directory\{title}')





# async def save_video_piece(video_url, start_time, end_time):
#     print("Func save_video_piece started")
#     save_to_io = io.BytesIO()
#     output_file_path = "video_cut.mp4"
#     youtube = pytube.YouTube(video_url)
#     video_stream = youtube.streams.filter(file_extension='mp4', progressive=True, res="480p").first()
#     temp_file_path = video_stream.download(output_path=".")
#
#     # Read the video duration using MoviePy
#     video = VideoFileClip(temp_file_path)
#
#     # Cut the video and save it to a bytes IO object
#     cut_video = video.subclip(start_time, end_time)
#
#     cut_video.write_videofile(output_file_path, codec="libx264")
#
#     async with aiofiles.open(output_file_path, 'rb') as f:
#         video_bytes = await f.read()
#
#     save_to_io.write(video_bytes)
#     save_to_io.seek(0)

    # Close the file before deleting it
    # await f.close()
    # os.remove(temp_file_path)

    # print(f'Successfully saved video piece to {output_file_path} and deleted temporary file')
    # return save_to_io.getvalue()
    # os.remove(temp_file_path)





# async def save_video_piece(video_url, start_time, end_time):
#     save_to_io = io.BytesIO()
#     print("Func save_video_piece started")
#     # Create an in-memory buffer to store the video
#     video_buffer = io.BytesIO()
#     video = mp.VideoFileClip(video_url)
#     cut_video = video.subclip(start_time, end_time)
#     cut_video_name = "cut_video.mp4"
#     cut_video.write_videofile(cut_video_name, codec="libx264")
#     with open(cut_video_name, 'rb') as f:
#         video_bytes = f.read()
#     save_to_io.write(video_bytes)
#     save_to_io.seek(0)
#     print(f'Successfully saved video piece')
#     return save_to_io.getvalue()







