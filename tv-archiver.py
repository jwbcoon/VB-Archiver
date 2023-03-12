from __future__ import unicode_literals
import youtube_dl
#import win32com

ydl_opts = { '--config-location .\\config.txt' }
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

