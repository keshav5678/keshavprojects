"""
# Meme Video Generator
a project to create videos that have two memes and a background.
uses meme-api.com to fetch memes and moviepy to compile them into a video.
"""

import requests
from moviepy.editor import *
import sys

img_files = [] 
api_url = "https://meme-api.com/gimme/2"
output_src = ""

# send the request
resp = requests.get(api_url)
resp_json = resp.json()

# save memes in the memes folder
for meme in resp_json["memes"]:
    file_name = f'memes\\{ meme["url"].split("/")[-1] }'
    img_files.append(file_name)

    img = requests.get(meme["url"])
    if img.status_code == 200:
        fp = open(file_name,"wb") 
        for chunk in img.iter_content(100000):
            fp.write(chunk)
        fp.close()
    else:
        exit()

# moviepy work
background = VideoFileClip("videos\\background.mp4").subclip(0,5)
img_1 = ImageClip(img_files[0])
img_2 = ImageClip(img_files[1])
img_1 = img_1.set_position(("center", "top"))
img_2 = img_2.set_position(("center", "bottom"))
img_1 = img_1.margin(top=50, opacity=0)
img_2 = img_2.margin(bottom=50, opacity=0)
img_1 = img_1.resize(width=1000)
img_2 = img_2.resize(width=1000)

# write the file
video = CompositeVideoClip([background, img_1.set_duration(5), img_2.set_duration(5)])
if not sys.argv[1]:
    video_name = input("enter video file name: ") + ".mp4"
    video_name = f"videos\\{video_name}"
else:
    video_name = sys.argv[1]
video.write_videofile(video_name, threads=2)
