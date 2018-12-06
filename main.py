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
import os
from os.path import isfile, join
import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("logs/oracle.log"),
        logging.StreamHandler()
    ])

bubbles = False
states_statments = json.load(open("states_statments.json","r"))

start_party_states = ['A1.mp3', 'A2.mp3', 'A3.mp3', 'A4.mp3']
start_answer = ['B1.mp3', 'B2.mp3', 'B3.mp3']
now_leave = ['C1.mp3', 'C2.mp3', 'C3.mp3', 'C4.mp3']
pressed_during_answer = ['D1.mp3', 'D2.mp3']
no_question = ['E1.mp3', 'E2.mp3', 'E3.mp3']
asked_recently = ['F1.mp3', 'F2.mp3']
no_actual_question = ['E3.mp3']


answers_dir = '/home/private/oracle/answers_mp3'
answers_files = [f for f in os.listdir(answers_dir) if isfile(join(answers_dir, f))]

def play_answer(answer):
    number, text = answer
    mp3_file = '%s.mp3' % number
    if mp3_file in answers_files:
        logging.info('answer mp3 file exist')
        party.play_a_file(os.path.join(answers_dir, mp3_file))
    else:
        tts.say(answer[1])


def play_statement(statement):
    logging.info(statement)
    full_path = os.path.join('statements', statement)
    party.play_a_file(full_path)

all_questions = []
def get_question(ar, wd):
    while True:
        if not ar.read_button():
            time.sleep(0.1)
            continue
        logging.info('button pushed')

        words = wd.detect()
        print(words)
        if len(words) < 2:
            logging.info('question not found')
            play_statement(random.choice(no_question))
            ar.flush_serial()
            continue
        if words in all_questions[-5:]:
            logging.info('question ask in the last 5 times')
            play_statement(random.choice(asked_recently))
            ar.flush_serial()
            continue
        if 4 <= datetime.datetime.now().hour <= 7:
            logging.info('push in the night')
            tts.say('I will answer you, but you should go to sleep afterward')

        all_questions.append(words)
        logging.info('question %s' % words)
        logging.info("number of questions from the begining of the world is %d" % len(all_questions))
        return words

legal_start_words = ['dont', 'do', 'how', 'are', 'should', 'i', 'will', 'does', 'what', 'lets', 'is', 'when', 'where', 'who', 'could', 'can', 'why', 'am']

def grammer_checker(question):
    return question.split()[0] in legal_start_words

def main_loop():
    wd = word_detector.WordDetector(retries=20)
    ar = arduino_driver.ArduinoController()
    logging.info('start loop')
    while True:
        question = get_question(ar, wd)
        if not grammer_checker(question):
            play_statement(random.choice(no_actual_question))
            ar.flush_serial()
            continue
        play_statement(random.choice(start_party_states))
        logging.info("start party")
        ar.set_party()
        party.play_random_song(wait=False)
        answer = answers.get_answer(question)

        logging.info('answer - %s' % str(answer))
        ar.flush_serial()
        time.sleep(2)
        while mixer.music.get_busy():
            # if ar.read_button():
            #     mixer.music.pause()
            #     play_statement(random.choice(pressed_during_answer))
            #     mixer.music.unpause()
            time.sleep(3)
        mixer.music.stop()
        logging.info('party end')
        ar.set_ambient()

        play_statement(random.choice(start_answer))
        play_answer(answer)
        time.sleep(0.4)
        play_statement(random.choice(now_leave))
        ar.flush_serial()


if __name__ == '__main__':
    mixer.init()
    main_loop()

    # while True:
    #     try:
    #         main_loop()
    #     except Exception as e:
    #         logging.info('problem ' + str(e))
    #play_answer(('s', 'You are not funny, stop pretend that you are'))
