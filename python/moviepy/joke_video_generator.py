import pyjokes, random, pyttsx3, string, time
from moviepy.editor import *
from moviepy import *

all_vids = []
engine = pyttsx3.init()
engine.setProperty('rate', 250)
jokes = pyjokes.get_jokes()

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def create_clips(the_vid_name):
    for _ in range(4):
        name = randomword(10)
        x = random.randint(1,3) * 5

        joke = jokes[random.randint(0, len(jokes)-1)]
        engine.save_to_file(text=joke, filename=f"{name}.mp3")
        engine.runAndWait()

        bg = VideoFileClip("bg.mp4").subclip(x-5,x)
        jokeTxtClip = TextClip(joke, fontsize=70, color='white', method="caption", size=(900, 1700))
        jokeClip = jokeTxtClip.set_position(('center', 'center')).set_duration(5)
        audio = AudioFileClip(f"{name}.mp3")

        video = CompositeVideoClip([bg, jokeClip])
        video = video.set_audio(audio)
        all_vids.append(video)

    final = concatenate_videoclips(all_vids)
    final.write_videofile(filename=f"videos/{the_vid_name}")

while True:
    create_clips(f'{randomword(15)}.mp4')
    all_vids = []
    time.sleep(120)
