from pygame import mixer
import time
import word_detector
import arduino_driver
import party
import answers
import argparse
import random
import json
import logging
from pygame import mixer
import tts

bubbles = False
states_statments = json.load(open("states_statments.json","r"))

all_questions = []
def get_question(ar, wd):
    while True:
        if not ar.read_button():
            time.sleep(0.1)
            continue
        logging.info('button pushed')
        words = wd.detect(True)
        if words == None:
            logging.info('question not found')
            tts.say(random.choice(states_statments['No_question']))
            ar.flush_serial()
            continue
        if words in all_questions[-5:]:
            logging.info('question ask in the last 5 times')
            tts.say(random.choice(states_statments['Asked_recently']))
            ar.flush_serial()
            continue
        all_questions.append(words)
        logging.log("number of questions from the begining of the world is %d" % len(all_questions))
        return words

def grammer_checker(question):
    return True

def main_loop():
    wd = word_detector.WordDetector()
    ar = arduino_driver.ArduinoController()
    logging.info('start loop')
    while True:
        question = get_question(ar, wd)
        if not grammer_checker(question):
            tts.say(random.choice(states_statments['Not_actual_english']))
            continue

        tts.say(random.choice(states_statments['start_party']))
        logging.info("start party")
        ar.set_party()
        party.play_random_song(wait=False)
        answer = answers.get_answer(question)

        full_answer = random.choice(states_statments['start_answer']) + answer
        while mixer.music.get_busy():
            if ar.read_button():
                mixer.music.pause()
                tts.say(random.choice(states_statments['Pressed_during_answer']))
                mixer.music.unpause()
            time.sleep(3)

        ar.set_ambient()

        tts.say(full_answer)
        tts.say(random.choice(states_statments['Now_leave']))
        ar.flush_serial()

        if bubbles:
            time.sleep(180)


if __name__ == '__main__':
    mixer.init()
    main_loop()
