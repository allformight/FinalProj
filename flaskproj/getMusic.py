from __future__ import unicode_literals
import youtube_dl
import argparse
import os
from time import strftime
import zipfile
filename = ''


class MyLogger(object): #youtube_dl log
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d): #converting message
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def downloader(url): # download file config
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])


def zipdir(path): #zip(compression) the playlist folder
    zipf = zipfile.ZipFile( path+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

def getFileName(path):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            path,
            download=False # We just want to extract the info
        )
    video = result

    title = (path.split("=")[1])
    title = video['title'] + '-' + title
    filename = title+".mp3"
    return filename

def getMusic(url): #main function
    global filename
    checkYtube = "https://www.youtube.com" # check youtube url
    checkYtubeWatch = "https://www.youtube.com/watch" #check video 
    checkYtubeList = "https://www.youtube.com/playlist" #check playlist
    if (url.startswith(checkYtube)): # check youtube url
        ###############Single Video###############
        if(url.startswith(checkYtubeWatch)): #check video
            if "&" in url: 
                url = url.split("&")[0] 
            print("You input a video.")
            print(url)
            now = strftime('%Y-%m-%d %H:%M:%S')
            dir_name = now # folder name
            if not os.path.exists("singleMusic"):  #confirm the folder isn't exist 
                os.makedirs("singleMusic") # build a folder to put .mp3 file
            os.chdir("singleMusic") # change dir (cd)
            if not os.path.exists(dir_name):  #confirm the folder isn't exist
                os.makedirs(dir_name)
            os.chdir(dir_name) # change dir (cd) pwd: {dir_name}
            downloader(url)
            os.chdir("../") # change dir (cd) pwd: {/}
            
            zipdir(dir_name)
            # zipf = zipfile.ZipFile( dir_name+'.zip', 'w', zipfile.ZIP_DEFLATED)
            # zipf.close()

            os.chdir("../")# change dir (cd) pwd: {/}
            filename = "singleMusic/" + dir_name +".zip"
        ###############Play List###############
        elif(url.startswith(checkYtubeList)): #check playlist
            # print("You input a video list.")
            # print("Name your playlist:", end='') # input your playlist name
            # dir_name = input("")
            now = strftime('%Y-%m-%d %H:%M:%S')
            dir_name = now # folder name

            if not os.path.exists("listMusic"):  #confirm the folder isn't exist
                os.makedirs("listMusic") # build a folder to put playlist file
            os.chdir("listMusic") # change dir (cd) pwd: listMusic
            if not os.path.exists(dir_name):  #confirm the folder isn't exist
                os.makedirs(dir_name)

            os.chdir(dir_name) # change dir (cd) pwd: {dir_name}
            filename = "listMusic/" + dir_name +".zip"

            downloader(url) #download all the video form the list
            #zip the folder to a .zip file
            os.chdir("../") # pwd: listMusic
            zipdir(dir_name) #call compression function
            os.chdir("../")# change dir (cd) pwd: {/}
    else:
        print("Not a youtube URL.")

if __name__ == '__main__':
    print("Please input a youtube URL:",end='')
    url = input()
    getMusic(url)