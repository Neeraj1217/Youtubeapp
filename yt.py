import os
import yt_dlp
import subprocess

def ytdownload(link):
    # Path to ffmpeg.exe
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')

    # yt-dlp options
    ydl_opts = {
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b',  
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  
        'ffmpeg_location': ffmpeg_path,
        'noplaylist': True,  
        'quiet': False,  

        # sub opts
        'writeautomaticsub': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'best',
        'embedsubtitles': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        video_file = ydl.prepare_filename(info).replace(".webm", ".mp4")

        subs = info.get('requested_subtitles')
        if subs:
            lang = list(subs.keys())[0]
            sub_file = os.path.splitext(video_file)[0] + f".{lang}.vtt"
            burned_file = os.path.splitext(video_file)[0] + "_subtitled.mp4"

            # Burn subtitles into video
            subprocess.run([
                ffmpeg_path, "-i", video_file,
                "-vf", f"subtitles={sub_file}",
                "-c:a", "copy", burned_file
            ])

            # Delete the original video (without subs)
            os.remove(video_file)

if __name__ == "__main__":
    link = input("Enter the YouTube link: ")
    ytdownload(link)
