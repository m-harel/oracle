import time
import random
from pygame import mixer
from os import listdir
from os.path import isfile, join
party_songs_dir = '/home/private/oracle/party_songs'
party_songs_addres = [join(party_songs_dir, f) for f in listdir(party_songs_dir) if isfile(join(party_songs_dir, f))]

def get_random_song():
    return random.choice(party_songs_addres)

def play_a_file(file, wait=True):
    mixer.music.load(file)
    mixer.music.play()

    if wait:
        while mixer.music.get_busy():
            time.sleep(0.5)


def play_random_song(wait=True):
    song_addr = get_random_song()
    print("song is %s" % song_addr)
    mixer.music.load(song_addr)
    mixer.music.play()

    if wait:
        while mixer.music.get_busy():
            time.sleep(1)


if __name__ == '__main__':
    mixer.init()
    play_random_song()
