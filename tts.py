import time
import pyttsx3
from pygame import mixer
TEMP_FILE = "temp.mp3"

tts_eng = pyttsx3.init()
tts_eng.setProperty('volume', 10)
tts_eng.setProperty('rate', 50)


def text_to_file(s):
    tts_eng.say(s)
    tts_eng.runAndWait()


def say_file(file, block=False):
    mixer.music.load(file)
    mixer.music.play()
    if block:
        while mixer.music.get_busy():
            time.sleep(0.1)

def say(s):
    file = text_to_file(s)
   # say_file(file, block=True)


if __name__ == '__main__':
    mixer.init()
 #   print('check tts')
    say("don't stop believing")
    # say('I am not from here, but I can solve you problems')
    # say('check text to speech, it is our new feature')
