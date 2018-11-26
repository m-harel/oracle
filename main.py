from pygame import mixer
import time
import word_detector
import arduino_driver
import party
import answers
import tts
import argparse
import os
import json
import logging
from pygame import mixer

bubbles = False

def main_loop(words_dict):
    _tts = tts.textToSpeech()
    wd = word_detector.WordDetector(words=words_dict)
    ar = arduino_driver.ArduinoController()
    logging.info('start loop')
    while True:
        if not ar.read_button():
            time.sleep(0.1)
            continue
        logging.info('button pushed')
        words = wd.detect(True)
        if words == None:
            logging.info('question not found')
            _tts.say('you did not ask anything!')
            ar.flush_serial()
            continue

        logging.info("start party")
        ar.set_party()
        party.play_random_song(wait=False)
        answer = answers.get_answer(words)

        while mixer.music.get_busy():
            time.sleep(1)

        ar.set_ambient()

        _tts.say(answer)
        ar.flush_serial()

        if bubbles:
            time.sleep(180)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read lines of arucos.')
    parser.add_argument("--words", type=str, default="words.json", help="Load number-to-word json")
    args = parser.parse_args()

    words_dict =  {}
    if args.words and os.path.isfile(args.words):
        words_dict = json.load(open(args.words,"r"))

    mixer.init()
    main_loop(words_dict)