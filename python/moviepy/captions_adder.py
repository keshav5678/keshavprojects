"program to add captions/subtitles to whatever video using SpeechRecognition and moviepy and a custom TUI (just to make it a little bit complicated)"

import random
import multiprocessing
import time
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import speech_recognition as sr
from custom_text_user_interface.tui import BoxHeading, Text, tuiList, Root

header = BoxHeading("captions adder ")
txt = Text("\nHOW IT WORKS:", "left")
the_list = tuiList([
    "extracts audio from the video file given",
    "saves the audio file",
    "and recognises every 5 seconds of the audio using google speech recognition",
    "adds the subtitles to the video (for every 5 seconds)\n"
])
r = Root([header, txt, the_list])


def add_subtitles(source):
    "add subtitles and export video"
    video = VideoFileClip(source)
    subtitles = []
    clips = [video]

    for _ in range(5,int(video.duration),5):
        v = video.subclip(_-5,_)
        audio = v.audio
        audio_source = f"{random.randint(1000,9999)}.wav"
        audio.write_audiofile(audio_source)
        time.sleep(0.1)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_source) as src:
            r_audio = recognizer.record(src)
        try:
            subtitles.append(recognizer.recognize_google(r_audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        os.remove(audio_source)

    for i, val in enumerate(subtitles):
        subtitle = TextClip(val, color="white", bg_color="black", fontsize=45).set_start(i*5).set_position(("left", "bottom")).margin(bottom=50,left=50, opacity=0).set_duration(5)
        clips.append(subtitle)

    if video.duration % 5 != 0:
        excess = video.subclip(video.duration - (video.duration % 5), video.duration)
        audio = excess.audio
        audio_source = f"{random.randint(1000,9999)}.wav"
        audio.write_audiofile(audio_source)
        time.sleep(0.1)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_source) as src:
            r_audio = recognizer.record(src)
        try:
            the_txt = recognizer.recognize_google(r_audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        os.remove(audio_source)

        subtitle = TextClip(the_txt, color="white", bg_color="black", fontsize=45).set_start(video.duration - (video.duration % 5)).set_position(("left", "bottom")).margin(bottom=50,left=50, opacity=0).set_duration(video.duration % 5)
        clips.append(subtitle)

    final_video = CompositeVideoClip(clips)
    r.n = False
    final_src = input("enter output file src: ")
    final_video.write_videofile(final_src, threads=multiprocessing.cpu_count())

r.root(add_subtitles, n=True, placeholder="enter video source")
