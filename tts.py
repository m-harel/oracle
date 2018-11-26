from gtts import gTTS


def say(self, s):
    tts = gTTS(text=s, lang='en')
    tts.save("temp.mp3")
    mixer.music.load("temp.mp3")
    mixer.music.play()