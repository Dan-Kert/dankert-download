#!/usr/bin/env python3

# Execute with
# $ python3 -m yt_dlp

import sys
from dankert_download.YoutubeDL import YoutubeDL

def get_ydl_opts(url):
    if "soundcloud.com" in url:
        return {
            'format': 'bestaudio/best',
            'merge_output_format': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',
        }
    else:
        return {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best',
            'merge_output_format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
        }

def run(url):
    ydl_opts = get_ydl_opts(url)
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    if len(sys.argv) < 2:
        print("Usage: dankert_download <URL>")
        sys.exit(1)
    run(sys.argv[1])

if __name__ == "__main__":
    main()
