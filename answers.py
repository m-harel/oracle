from pyexcel_ods import get_data
from collections import Counter, OrderedDict
import json
import word_detector
import random

try:
    qna = json.load(open("qna.json", "r"))
except:
    qna = {}

def get_answer(question):
    if question in qna.keys():
        list_of_answers = [(ans_id, a) for ans_id, a in qna[question].items()]
        return random.choice(list_of_answers)

    question_rank = OrderedDict()
    for q in qna.keys():
        question_rank[q] = rate_questions(question, q)

    best_answers = get_the_best_n_answer_from_dict(question_rank, 2)
    return random.choice(best_answers)


def get_the_best_n_answer_from_dict(question_rank, n):
    best_answers = []
    question_sorted_by_rank = sorted(question_rank.items(), key=lambda kv: kv[1])
    question_sorted_by_rank.reverse()
    print(question_sorted_by_rank[:10])
    for question in question_sorted_by_rank:
        for ans_id, a in qna[question[0]].items():
            best_answers.append((ans_id, a))

        if len(best_answers) >= n:
            break

    return best_answers


def rate_questions(a, b):
    rank = 0
    b_words = b.split()
    for a_word in a.split():
        if a_word in b_words:
            rank += word_detector.words_dict[a_word]['rank']

    if b_words[0] == a.split()[0]:
        rank += 20

    return rank

def sanitize(phrase):
    phrase = "".join([c for c in phrase if c.isalpha() or c.isspace()])
    phrase = phrase.lower().strip()
    return phrase


def update_from_ods():
    data = get_data('rsp.ods')

    output = {}

    for line in data["Form Responses 1"][1:]:
        if len(line) < 3:
            continue
        print(line)
        number = line[0]
        question = sanitize(line[2])
        answer = line[3]
        if question not in output.keys():
            output[question] = {}
        output[question][number] = answer

    print(output)
    print(sum([len(question[1].keys()) for question in output.items()]))
    json.dump(dict(output), open("qna.json", "w"))

def create_histogram():
    counter = Counter()
    print(qna.keys())
    i = 0
    for question in qna.keys():
        for word in question.split():
            counter[word] += 1
            i += 1

    print('counter size is %d' % len(counter))
    print(counter)
    counter_keys = list(counter.keys())
    counter_keys.sort()
    words_dict = json.load(open("words.json", "r"))
    words = words_dict.keys()
    i = 0
    for word in counter_keys:
        if word not in words:
            print(word)
            i+=1
    print(i)
    return counter_keys

def create_empty_word_dict(words):
    output = {}

    for word in words:
        output[word] = {'rank': 1, 'id': -1}

    print(output)
    json.dump(dict(output), open("words.json", "w"))

def start_question_words():
    star_words = set()
    for question in qna.keys():
        star_words.add(question.split()[0])

    print(star_words)

if __name__ == '__main__':
    #update_from_ods()
    #words = create_histogram()
    # create_empty_word_dict(words)
    #start_question_words()
    print(get_answer('why the sun is so bright'))
